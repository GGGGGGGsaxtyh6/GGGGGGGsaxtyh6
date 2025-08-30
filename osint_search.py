#!/usr/bin/env python3
import requests
import json
import re
import base64

# Información encontrada
username = "TechReviewer2024"
email = "alex.morgan@tempmail.com"

print(f"[*] Información del objetivo:")
print(f"    Username: {username}")
print(f"    Email: {email}")
print()

# Buscar en la propia aplicación
BASE_URL = "http://94.237.57.115:35694"

# Intentar diferentes endpoints
endpoints = [
    f"/profile/{username}",
    f"/user/{username}",
    f"/api/user/{username}",
    f"/api/profile/{username}",
    f"/{username}",
    "/api/users",
    "/api/profiles",
    "/users",
    "/profiles",
    "/reviews",
    "/api/reviews",
    f"/reviews/{username}",
    f"/api/reviews/{username}",
]

print("[*] Probando endpoints en la aplicación...")
for endpoint in endpoints:
    try:
        url = BASE_URL + endpoint
        r = requests.get(url, timeout=3)
        if r.status_code != 404 and r.status_code != 500:
            print(f"[+] {endpoint} - Status: {r.status_code}")
            if r.status_code == 200:
                # Buscar información interesante en la respuesta
                content = r.text
                if "HTB{" in content:
                    flag = re.search(r'HTB\{[^}]+\}', content)
                    if flag:
                        print(f"    [!] FLAG ENCONTRADA: {flag.group()}")
                if username in content or email in content:
                    print(f"    [+] Contiene información del usuario")
                # Buscar otros usuarios o información
                other_users = re.findall(r'["\']([\w\-\.]+@[\w\-\.]+)["\']', content)
                if other_users:
                    print(f"    [+] Otros emails encontrados: {set(other_users)}")
    except:
        pass

# Buscar en el código fuente patrones específicos
print("\n[*] Analizando más a fondo el código JavaScript...")
r = requests.get(BASE_URL + "/assets/index-fPbXfhd6.js")
js_content = r.text

# Buscar referencias a GitHub, social media, etc.
social_patterns = [
    r'github\.com/([^"\'\\s]+)',
    r'twitter\.com/([^"\'\\s]+)',
    r'linkedin\.com/in/([^"\'\\s]+)',
    r'instagram\.com/([^"\'\\s]+)',
    r'facebook\.com/([^"\'\\s]+)',
    r'reddit\.com/u/([^"\'\\s]+)',
    r'medium\.com/@([^"\'\\s]+)',
]

for pattern in social_patterns:
    matches = re.findall(pattern, js_content, re.IGNORECASE)
    if matches:
        site = pattern.split('\.')[0].split('\\')[-1]
        print(f"[+] {site} profiles encontrados: {set(matches)}")

# Buscar strings codificadas en base64
print("\n[*] Buscando strings codificadas...")
b64_pattern = r'[A-Za-z0-9+/]{20,}={0,2}'
b64_matches = re.findall(b64_pattern, js_content)
for match in b64_matches[:20]:  # Solo los primeros 20
    try:
        decoded = base64.b64decode(match).decode('utf-8', errors='ignore')
        if any(c.isprintable() for c in decoded) and len(decoded) > 5:
            if 'HTB' in decoded or 'flag' in decoded.lower() or username in decoded:
                print(f"[+] Base64 decodificado: {decoded[:100]}")
    except:
        pass

# Buscar en comentarios HTML
print("\n[*] Buscando en comentarios HTML...")
r = requests.get(BASE_URL)
html_comments = re.findall(r'<!--(.*?)-->', r.text, re.DOTALL)
for comment in html_comments:
    if comment.strip():
        print(f"[+] Comentario HTML: {comment.strip()[:200]}")

# Buscar archivos comunes
print("\n[*] Buscando archivos comunes...")
common_files = [
    "/robots.txt",
    "/sitemap.xml",
    "/.git/config",
    "/README.md",
    "/package.json",
    "/.env",
    "/config.json",
    "/api/config",
    "/api",
    "/admin",
    "/login",
    "/register",
    "/dashboard",
    "/profile",
    "/settings",
]

for file in common_files:
    try:
        r = requests.get(BASE_URL + file, timeout=2)
        if r.status_code == 200:
            print(f"[+] Encontrado: {file}")
            if len(r.text) < 1000:
                print(f"    Contenido: {r.text[:500]}")
    except:
        pass

# Información específica del usuario TechReviewer2024
print(f"\n[*] Buscando información específica de {username}...")
# El nombre sugiere que es un revisor de tecnología del 2024
# Podría tener un blog, GitHub, o perfil en sitios de reviews

# Intentar variaciones del username
usernames_to_try = [
    username,
    username.lower(),
    "techreviewer",
    "tech-reviewer-2024",
    "tech_reviewer_2024",
    "alexmorgan",
    "alex-morgan",
    "alex_morgan",
    "amorgan",
]

print("[*] Probando variaciones del username...")
for uname in usernames_to_try:
    for endpoint in [f"/{uname}", f"/user/{uname}", f"/profile/{uname}", f"/api/{uname}"]:
        try:
            r = requests.get(BASE_URL + endpoint, timeout=2)
            if r.status_code == 200 and r.text != "<!doctype html>":
                print(f"[+] Encontrado: {endpoint}")
        except:
            pass