#!/usr/bin/env python3
"""
Investigar el campo planet
"""
import requests
import random
import string
import re

TARGET = "http://94.237.49.23:45329"

def random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

# El planet se elige aleatoriamente en register.php
# Pero ¿se usa en algún lugar vulnerable?

# index.php línea 31: $planet_emoji = pick_emoji($planet);
# emoji.php define pick_emoji

# ¿Hay SQLi en cómo se obtiene el planet?
# searchUser devuelve planet del usuario

session = requests.Session()
username = random_string()
password = random_string()

data = {'name': 'user1', 'username': username, 'password': password}
session.post(f"{TARGET}/register.php", data=data)
session.post(f"{TARGET}/login.php", data={'username': username, 'password': password})

print(f"[*] Usuario: {username}:{password}\n")

# Ver qué planet tengo
resp = session.get(f"{TARGET}/")
match = re.search(r'Currently you are in <span>([^<]+)</span>', resp.text)
if match:
    planet_emoji = match.group(1)
    print(f"[*] Planet emoji: {planet_emoji}")
    
    # Determinar planet basado en emoji
    if planet_emoji == "🌎":
        planet = "Earth"
    elif planet_emoji == "🌕":
        planet = "Moon"
    else:
        planet = "Somewhere (unknown)"
    
    print(f"[*] Planet: {planet}")

# El planet NO parece ser vulnerable directamente
# PERO... ¿puedo de alguna forma modificar mi planet en la BD?

# Crear múltiples usuarios para tener diferentes planets
print("\n[*] Creando múltiples usuarios para analizar planets...")
for i in range(5):
    s = requests.Session()
    u = random_string()
    p = random_string()
    
    data = {'name': f'user{i}', 'username': u, 'password': p}
    s.post(f"{TARGET}/register.php", data=data)
    s.post(f"{TARGET}/login.php", data={'username': u, 'password': p})
    
    resp = s.get(f"{TARGET}/")
    match = re.search(r'Currently you are in <span>([^<]+)</span>', resp.text)
    if match:
        print(f"    User {i}: {match.group(1)}")
