#!/usr/bin/env python3
import requests
import re
import json

BASE_URL = "http://94.237.57.115:35694"

print("[*] Inspeccionando la aplicación SocialConnect más a fondo...")
print("[*] Buscando el email REAL del contacto...")
print()

# Obtener el JavaScript completo
r = requests.get(BASE_URL + "/assets/index-fPbXfhd6.js")
js = r.text

# Buscar específicamente alrededor del objeto del usuario
print("[*] Analizando el objeto del usuario...")
# Buscar el objeto completo
start = js.find('username:"TechReviewer2024"')
if start != -1:
    # Obtener contexto alrededor
    context = js[max(0, start-500):min(len(js), start+1000)]
    print("Contexto alrededor del usuario:")
    print(context)
    print("\n" + "="*60 + "\n")

# Buscar si hay algún estado o configuración
print("[*] Buscando estados o configuraciones...")
state_patterns = [
    r'state\s*=\s*\{[^}]+\}',
    r'config\s*=\s*\{[^}]+\}',
    r'data\s*=\s*\{[^}]+\}',
    r'profile\s*=\s*\{[^}]+\}',
]

for pattern in state_patterns:
    matches = re.findall(pattern, js)
    for match in matches[:5]:
        if 'email' in match.lower() or '@' in match:
            print(f"[+] Estado/Config encontrado: {match[:300]}")

# Buscar funciones que manejen el contacto
print("\n[*] Buscando funciones relacionadas con contacto...")
function_patterns = [
    r'showContact[^{]*\{[^}]+\}',
    r'hideContact[^{]*\{[^}]+\}',
    r'toggleContact[^{]*\{[^}]+\}',
    r'getContact[^{]*\{[^}]+\}',
    r'revealContact[^{]*\{[^}]+\}',
]

for pattern in function_patterns:
    matches = re.findall(pattern, js, re.IGNORECASE)
    for match in matches[:3]:
        print(f"[+] Función: {match[:200]}")

# Buscar si hay algún array con múltiples usuarios o perfiles
print("\n[*] Buscando arrays de usuarios o perfiles...")
array_pattern = r'\[[^\]]*TechReviewer[^\]]*\]'
arrays = re.findall(array_pattern, js)
for array in arrays[:3]:
    print(f"[+] Array: {array[:300]}")

# Buscar si hay algún condicional que muestre información diferente
print("\n[*] Buscando condicionales...")
conditional_patterns = [
    r'if[^{]*email[^{]*\{[^}]+\}',
    r'if[^{]*contact[^{]*\{[^}]+\}',
    r'\?[^:]*email[^:]*:[^;]+',
]

for pattern in conditional_patterns:
    matches = re.findall(pattern, js, re.IGNORECASE)
    for match in matches[:5]:
        if '@' in match:
            print(f"[+] Condicional: {match[:200]}")

# Buscar todos los emails únicos
print("\n[*] Lista de TODOS los emails únicos encontrados:")
email_pattern = r'[\w\.\-]+@[\w\.\-]+\.[\w]+'
all_emails = re.findall(email_pattern, js)
unique_emails = set(all_emails)
for email in unique_emails:
    print(f"    - {email}")
    # Obtener contexto de cada email
    pos = js.find(email)
    if pos != -1:
        context = js[max(0, pos-50):min(len(js), pos+50)]
        print(f"      Contexto: {context}")

# Buscar si hay algún texto que sugiera el email real
print("\n[*] Buscando pistas textuales...")
hint_patterns = [
    r'real[^:]*:\s*"([^"]+)"',
    r'actual[^:]*:\s*"([^"]+)"',
    r'true[^:]*:\s*"([^"]+)"',
    r'genuine[^:]*:\s*"([^"]+)"',
    r'authentic[^:]*:\s*"([^"]+)"',
]

for pattern in hint_patterns:
    matches = re.findall(pattern, js, re.IGNORECASE)
    for match in matches:
        if '@' in match or 'email' in match.lower():
            print(f"[+] Pista: {match}")

# Buscar el componente de React que maneja el perfil
print("\n[*] Analizando componentes React...")
# Buscar JSX
jsx_pattern = r'jsx[^(]*\([^)]+\)'
jsx_matches = re.findall(jsx_pattern, js)
for match in jsx_matches[:20]:
    if 'email' in match.lower() or 'contact' in match.lower():
        print(f"[+] JSX: {match[:200]}")