#!/usr/bin/env python3
import requests
import json
import re
import hashlib

BASE_URL = "http://94.237.57.115:35694"

# Información conocida
username = "TechReviewer2024"
email = "alex.morgan@tempmail.com"
display_name = "Tech Reviewer"
location = "San Francisco, CA"

print("[*] Realizando búsqueda profunda...")
print(f"[*] Usuario: {username}")
print(f"[*] Email: {email}")
print()

# El nombre "The Suspicious Reviewer" sugiere que hay algo sospechoso sobre las reviews
# Voy a buscar si hay alguna API o endpoint para obtener reviews

# Probar diferentes métodos HTTP
methods = ['GET', 'POST', 'PUT']
endpoints = [
    '/api/search',
    '/api/users/TechReviewer2024',
    '/api/reviews/TechReviewer2024',
    '/api/posts/TechReviewer2024',
    '/search',
    '/reviews',
    '/posts',
    '/api/profile/TechReviewer2024',
    '/api/user/TechReviewer2024/reviews',
    '/api/user/TechReviewer2024/posts',
    '/api/user/TechReviewer2024/comments',
    '/api/user/TechReviewer2024/social',
    '/api/user/TechReviewer2024/links',
]

print("[*] Probando diferentes métodos y endpoints...")
for endpoint in endpoints:
    for method in methods:
        try:
            if method == 'GET':
                r = requests.get(BASE_URL + endpoint, timeout=2)
            elif method == 'POST':
                r = requests.post(BASE_URL + endpoint, json={}, timeout=2)
            elif method == 'PUT':
                r = requests.put(BASE_URL + endpoint, json={}, timeout=2)
            
            if r.status_code != 404 and r.status_code != 405:
                if 'doctype' not in r.text.lower()[:20]:  # No es HTML
                    print(f"[+] {method} {endpoint} - Status: {r.status_code}")
                    if r.text and len(r.text) < 5000:
                        print(f"    Respuesta: {r.text[:500]}")
                        if 'HTB{' in r.text:
                            flag = re.search(r'HTB\{[^}]+\}', r.text)
                            if flag:
                                print(f"[!] FLAG ENCONTRADA: {flag.group()}")
        except:
            pass

# Buscar con parámetros
print("\n[*] Probando con parámetros de búsqueda...")
params_list = [
    {'username': username},
    {'user': username},
    {'q': username},
    {'search': username},
    {'query': username},
    {'name': username},
    {'email': email},
    {'id': username},
]

for params in params_list:
    try:
        r = requests.get(BASE_URL + '/api/search', params=params, timeout=2)
        if r.status_code == 200 and 'doctype' not in r.text.lower()[:20]:
            print(f"[+] Búsqueda con {params}: {r.status_code}")
            if r.text and len(r.text) < 5000:
                print(f"    Respuesta: {r.text[:500]}")
    except:
        pass

# El usuario podría tener perfiles en otras plataformas
# Buscar variaciones del username
print("\n[*] Generando variaciones del username para búsqueda externa...")
variations = [
    username,
    username.lower(),
    username.replace('2024', ''),
    username.replace('TechReviewer', 'Tech-Reviewer'),
    username.replace('TechReviewer', 'Tech_Reviewer'),
    'alexmorgan',
    'alex.morgan',
    'alex-morgan',
    'alex_morgan',
    'amorgan',
    'techreviewer',
    'tech.reviewer',
    'tech-reviewer',
    'tech_reviewer',
    'alexmorgan2024',
    'alex.morgan.2024',
    'suspicious.reviewer',
    'suspiciousreviewer',
    'the.suspicious.reviewer',
]

print("[*] Variaciones generadas:")
for var in variations[:10]:
    print(f"    - {var}")

# Buscar en el JavaScript información adicional
print("\n[*] Analizando JavaScript en busca de pistas...")
r = requests.get(BASE_URL + "/assets/index-fPbXfhd6.js")
js = r.text

# Buscar menciones de plataformas sociales
platforms = ['github', 'twitter', 'linkedin', 'instagram', 'facebook', 'reddit', 
             'youtube', 'medium', 'discord', 'telegram', 'mastodon', 'threads']

for platform in platforms:
    if platform in js.lower():
        # Buscar el contexto
        pattern = f'.{{0,100}}{platform}.{{0,100}}'
        matches = re.findall(pattern, js, re.IGNORECASE)
        for match in matches[:3]:
            if username.lower() in match.lower() or 'alex' in match.lower():
                print(f"[+] Referencia a {platform}: {match[:200]}")

# Buscar hashes o strings codificadas
print("\n[*] Buscando strings codificadas o hashes...")
# MD5
md5_pattern = r'[a-f0-9]{32}'
md5_matches = re.findall(md5_pattern, js)
for match in set(md5_matches[:10]):
    print(f"[+] Posible MD5: {match}")

# SHA1
sha1_pattern = r'[a-f0-9]{40}'
sha1_matches = re.findall(sha1_pattern, js)
for match in set(sha1_matches[:5]):
    print(f"[+] Posible SHA1: {match}")

# Buscar números que podrían ser IDs
print("\n[*] Buscando IDs o números relevantes...")
id_patterns = [
    r'"id"\s*:\s*(\d+)',
    r'"userId"\s*:\s*(\d+)',
    r'"reviewId"\s*:\s*(\d+)',
    r'"postId"\s*:\s*(\d+)',
]

for pattern in id_patterns:
    matches = re.findall(pattern, js)
    for match in set(matches):
        print(f"[+] ID encontrado: {match}")

# Generar hash del username (a veces se usa como ID)
print("\n[*] Generando hashes del username...")
print(f"[+] MD5({username}): {hashlib.md5(username.encode()).hexdigest()}")
print(f"[+] SHA1({username}): {hashlib.sha1(username.encode()).hexdigest()}")
print(f"[+] SHA256({username}): {hashlib.sha256(username.encode()).hexdigest()}")

# Buscar si hay alguna mención de steganografía o imágenes modificadas
print("\n[*] Buscando referencias a steganografía...")
stego_keywords = ['steg', 'hidden', 'secret', 'embed', 'conceal', 'hide']
for keyword in stego_keywords:
    if keyword in js.lower():
        pattern = f'.{{0,100}}{keyword}.{{0,100}}'
        matches = re.findall(pattern, js, re.IGNORECASE)
        for match in matches[:3]:
            print(f"[+] Referencia a {keyword}: {match[:200]}")