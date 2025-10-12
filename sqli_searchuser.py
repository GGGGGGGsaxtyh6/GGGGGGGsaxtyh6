#!/usr/bin/env python3
"""
Si pudiera inyectar en searchUser directamente...
El problema es que $_SESSION['name'] se usa.
¿Puedo manipular la sesión de alguna forma?
"""
import requests
import random
import string

TARGET = "http://94.237.49.23:45329"

def random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

# Crear múltiples usuarios y ver si puedo interferir con sesiones
print("[*] Probando manipulación de sesiones...")

for i in range(3):
    session = requests.Session()
    username = random_string()
    password = random_string()
    
    data = {'name': f'user{i}', 'username': username, 'password': password}
    session.post(f"{TARGET}/register.php", data=data)
    session.post(f"{TARGET}/login.php", data={'username': username, 'password': password})
    
    # Obtener cookie
    cookies = session.cookies.get_dict()
    print(f"[*] User {i}: PHPSESSID = {cookies.get('PHPSESSID', 'N/A')}")
    
    # Ver si puedo acceder con cookie modificada
    resp = session.get(f"{TARGET}/")
    if f"user{i}" in resp.text:
        print(f"    [+] Nombre correcto: user{i}")

# Intentar session fixation o manipulation
print("\n[*] Probando cookies manipuladas...")
s = requests.Session()
s.cookies.set('PHPSESSID', 'a'*26)  # Session ID controlado
resp = s.get(f"{TARGET}/")
print(f"    Status: {resp.status_code}, Redirect: {resp.url}")
