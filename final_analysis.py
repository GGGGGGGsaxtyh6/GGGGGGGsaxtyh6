#!/usr/bin/env python3
import requests
import re
import json

BASE_URL = "http://94.237.57.115:35694"

print("[*] Análisis final del challenge 'The Suspicious Reviewer'")
print("[*] Necesito encontrar el email REAL detrás del perfil fraudulento")
print()

# Obtener el JavaScript
r = requests.get(BASE_URL + "/assets/index-fPbXfhd6.js")
js = r.text

# Buscar el objeto del usuario más detalladamente
print("[*] Analizando el objeto del usuario...")
# Encontrar el objeto completo
user_data_pattern = r'\{[^{}]*username:"TechReviewer2024"[^}]*\}'
matches = re.findall(user_data_pattern, js)
for match in matches:
    print(f"Objeto usuario: {match}")
    print()

# Buscar si hay algún condicional que muestre diferente información
print("[*] Buscando lógica condicional...")
# Buscar patrones como: showContact ? realEmail : fakeEmail
conditional_patterns = [
    r'[\w]+\s*\?\s*"([^"]+@[^"]+)"\s*:\s*"([^"]+@[^"]+)"',
    r'if\s*\([^)]+\)[^{]*\{[^}]*"([^"]+@[^"]+)"[^}]*\}',
    r'contact[^:]*:\s*"([^"]+@[^"]+)"',
]

for pattern in conditional_patterns:
    matches = re.findall(pattern, js)
    for match in matches:
        print(f"[+] Patrón encontrado: {match}")

# Buscar si hay algún estado que contenga el email real
print("\n[*] Buscando en estados y configuraciones...")
# Buscar useState o state con emails
state_patterns = [
    r'useState\([^)]*"([^"]+@[^"]+)"[^)]*\)',
    r'state\s*=\s*\{[^}]*email[^:]*:\s*"([^"]+@[^"]+)"',
    r'realEmail[^:]*:\s*"([^"]+@[^"]+)"',
    r'actualEmail[^:]*:\s*"([^"]+@[^"]+)"',
]

for pattern in state_patterns:
    matches = re.findall(pattern, js)
    for match in matches:
        if match != "alex.morgan@tempmail.com":
            print(f"[+] Email en estado: {match}")

# Buscar si hay algún componente que maneje el "Show Contact"
print("\n[*] Buscando componente 'Show Contact'...")
show_contact_pattern = r'Show Contact[^}]*\}[^{]*\{[^}]*\}'
matches = re.findall(show_contact_pattern, js)
for match in matches[:3]:
    print(f"[+] Componente: {match[:200]}")

# Buscar TODOS los strings que parezcan emails con formato Nombre.Apellido
print("\n[*] Buscando emails con formato Nombre.Apellido...")
# Patrón más específico para emails reales
real_email_pattern = r'"([A-Z][a-z]+\.[A-Z][a-z]+@[a-z]+\.[a-z]+)"'
matches = re.findall(real_email_pattern, js)
for match in matches:
    print(f"[!] Posible email real: {match}")

# Buscar variaciones
email_variations = [
    r'"(emily[^"]*@[^"]+)"',
    r'"(thompson[^"]*@[^"]+)"',
    r'"(e\.thompson[^"]*@[^"]+)"',
    r'"(emily\.thompson[^"]*@[^"]+)"',
]

for pattern in email_variations:
    matches = re.findall(pattern, js, re.IGNORECASE)
    for match in matches:
        if '@' in match:
            print(f"[+] Variación encontrada: {match}")

# Buscar en el contexto alrededor de "contact"
print("\n[*] Analizando contexto de 'contact'...")
contact_contexts = re.findall(r'.{0,100}contact.{0,100}', js, re.IGNORECASE)
for context in contact_contexts[:10]:
    if '@' in context or 'email' in context.lower():
        # Extraer emails del contexto
        emails_in_context = re.findall(r'[\w\.\-]+@[\w\.\-]+\.[\w]+', context)
        for email in emails_in_context:
            if email != "alex.morgan@tempmail.com":
                print(f"[+] Email en contexto de contact: {email}")
                print(f"    Contexto: {context}")

# Última búsqueda exhaustiva de cualquier email
print("\n[*] Búsqueda exhaustiva de emails...")
all_emails = re.findall(r'[\w\.\-]+@[\w\.\-]+\.[\w]+', js)
unique_emails = set(all_emails)
print(f"[*] Total de emails únicos encontrados: {len(unique_emails)}")
for email in unique_emails:
    if email != "alex.morgan@tempmail.com" and not email.endswith('.js'):
        print(f"    - {email}")

print("\n[*] Si el email real no está en el código, probablemente:")
print("    1. Está en un perfil real de X/Twitter del usuario TechReviewer2024")
print("    2. Necesitas interactuar con la aplicación (hacer clic en 'Show Contact')")
print("    3. Está codificado o cifrado de alguna manera")