#!/usr/bin/env python3
import requests
import re
import json
import base64

BASE_URL = "http://94.237.57.115:35694"

print("[*] Buscando el email REAL detrás del perfil falso...")
print("[*] El email alex.morgan@tempmail.com es claramente falso (tempmail)")
print()

# Obtener el JavaScript
r = requests.get(BASE_URL + "/assets/index-fPbXfhd6.js")
js = r.text

# Buscar TODOS los emails en el código
print("[*] Buscando todos los emails en el código...")
email_pattern = r'[\w\.-]+@[\w\.-]+\.[\w]+'
emails = re.findall(email_pattern, js)
for email in set(emails):
    if email != "alex.morgan@tempmail.com":
        print(f"[+] Email encontrado: {email}")

# Buscar variaciones del objeto del usuario
print("\n[*] Buscando objetos con información adicional...")
# Buscar objetos JSON más grandes que puedan contener más información
json_objects = re.findall(r'\{[^{}]*["\']\w+["\'][^{}]*\}', js)
for obj in json_objects:
    if 'TechReviewer' in obj or 'email' in obj:
        # Buscar emails en este objeto
        emails_in_obj = re.findall(email_pattern, obj)
        for email in emails_in_obj:
            if email != "alex.morgan@tempmail.com":
                print(f"[+] Email en objeto: {email}")
                print(f"    Contexto: {obj[:200]}")

# Buscar campos ocultos o adicionales
print("\n[*] Buscando campos ocultos o adicionales...")
hidden_patterns = [
    r'hidden["\']?\s*:\s*["\'](.*?)["\']',
    r'realEmail["\']?\s*:\s*["\'](.*?)["\']',
    r'actualEmail["\']?\s*:\s*["\'](.*?)["\']',
    r'contactEmail["\']?\s*:\s*["\'](.*?)["\']',
    r'privateEmail["\']?\s*:\s*["\'](.*?)["\']',
    r'secretEmail["\']?\s*:\s*["\'](.*?)["\']',
    r'contact["\']?\s*:\s*["\'](.*?)["\']',
    r'real["\']?\s*:\s*["\'](.*?)["\']',
]

for pattern in hidden_patterns:
    matches = re.findall(pattern, js, re.IGNORECASE)
    if matches:
        for match in matches:
            if '@' in match:
                print(f"[+] Campo oculto encontrado: {match}")

# Buscar en comentarios
print("\n[*] Buscando en comentarios...")
comments = re.findall(r'//[^\n]+|/\*[\s\S]*?\*/', js)
for comment in comments:
    emails_in_comment = re.findall(email_pattern, comment)
    for email in emails_in_comment:
        print(f"[+] Email en comentario: {email}")

# Buscar strings codificadas que podrían contener emails
print("\n[*] Buscando strings codificadas...")
# ROT13
def rot13(text):
    result = []
    for char in text:
        if 'a' <= char <= 'z':
            result.append(chr((ord(char) - ord('a') + 13) % 26 + ord('a')))
        elif 'A' <= char <= 'Z':
            result.append(chr((ord(char) - ord('A') + 13) % 26 + ord('A')))
        else:
            result.append(char)
    return ''.join(result)

# Buscar strings que podrían estar en ROT13
strings = re.findall(r'["\']([\w\.\-@]+)["\']', js)
for s in strings:
    decoded = rot13(s)
    if '@' in decoded and '.' in decoded:
        print(f"[+] Posible ROT13: {s} -> {decoded}")

# Buscar en base64
b64_pattern = r'[A-Za-z0-9+/]{20,}={0,2}'
b64_matches = re.findall(b64_pattern, js)
for match in set(b64_matches[:100]):
    try:
        decoded = base64.b64decode(match).decode('utf-8', errors='ignore')
        emails_in_b64 = re.findall(email_pattern, decoded)
        for email in emails_in_b64:
            print(f"[+] Email en Base64: {email}")
    except:
        pass

# Buscar información sobre el "contacto real"
print("\n[*] Buscando información sobre el contacto real...")
contact_patterns = [
    r'contact[^:]*:\s*{([^}]+)}',
    r'real[^:]*:\s*{([^}]+)}',
    r'actual[^:]*:\s*{([^}]+)}',
    r'private[^:]*:\s*{([^}]+)}',
]

for pattern in contact_patterns:
    matches = re.findall(pattern, js, re.IGNORECASE)
    for match in matches:
        if '@' in match or 'email' in match.lower():
            print(f"[+] Información de contacto: {match}")

# Buscar si hay algún segundo perfil o información adicional
print("\n[*] Buscando perfiles adicionales o información secundaria...")
profile_patterns = [
    r'profile[^:]*:\s*{([^}]+)}',
    r'user[^:]*:\s*{([^}]+)}',
    r'account[^:]*:\s*{([^}]+)}',
]

for pattern in profile_patterns:
    matches = re.findall(pattern, js, re.IGNORECASE)
    for match in matches:
        if 'TechReviewer' not in match and '@' in match:
            print(f"[+] Perfil adicional: {match}")

# Buscar específicamente el patrón HTB{...}
print("\n[*] Buscando el patrón HTB{...}...")
htb_pattern = r'HTB\{([^}]+)\}'
htb_matches = re.findall(htb_pattern, js, re.IGNORECASE)
for match in htb_matches:
    print(f"[!] FLAG ENCONTRADA: HTB{{{match}}}")

# Buscar nombres que podrían ser el contacto real
print("\n[*] Buscando nombres reales...")
name_patterns = [
    r'["\']([\w]+\.[\w]+@[\w\.-]+)["\']',  # Formato Nombre.Apellido@email
    r'["\']([\w]+_[\w]+@[\w\.-]+)["\']',   # Formato Nombre_Apellido@email
    r'["\']([A-Z][\w]+\.[A-Z][\w]+@[\w\.-]+)["\']',  # Formato capitalizado
]

for pattern in name_patterns:
    matches = re.findall(pattern, js)
    for match in matches:
        if match != "alex.morgan@tempmail.com":
            print(f"[+] Posible email real: {match}")