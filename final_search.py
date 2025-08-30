#!/usr/bin/env python3
import requests
import re
import json

BASE_URL = "http://94.237.57.115:35694"

print("[*] Búsqueda final - Analizando todo el código JavaScript...")

# Obtener todo el JS
r = requests.get(BASE_URL + "/assets/index-fPbXfhd6.js")
js = r.text

# Buscar CUALQUIER cosa que parezca una flag
print("\n[*] Buscando patrones de flag...")
flag_patterns = [
    r'HTB\{[^}]+\}',
    r'flag["\']?\s*[:=]\s*["\'](.*?)["\']',
    r'FLAG["\']?\s*[:=]\s*["\'](.*?)["\']',
    r'ctf\{[^}]+\}',
    r'CTF\{[^}]+\}',
]

for pattern in flag_patterns:
    matches = re.findall(pattern, js, re.IGNORECASE)
    if matches:
        for match in matches:
            print(f"[!] Encontrado: {match}")

# Buscar URLs sospechosas o inusuales
print("\n[*] Buscando URLs...")
url_pattern = r'https?://[^\s"\',;)]+' 
urls = re.findall(url_pattern, js)
for url in set(urls):
    if 'hackthebox' not in url and 'react' not in url and 'w3.org' not in url:
        if 'github' in url or 'gist' in url or 'pastebin' in url or 'discord' in url:
            print(f"[+] URL interesante: {url}")

# Buscar comentarios con información
print("\n[*] Buscando comentarios con información...")
comments = re.findall(r'//[^\n]+|/\*[\s\S]*?\*/', js)
for comment in comments:
    if 'todo' in comment.lower() or 'fixme' in comment.lower() or 'note' in comment.lower() or 'hack' in comment.lower() or 'secret' in comment.lower():
        print(f"[+] Comentario: {comment[:200]}")

# Buscar objetos con datos del usuario
print("\n[*] Extrayendo todos los datos del usuario...")
# Buscar el objeto completo del usuario
user_pattern = r'\{[^{}]*username["\']?\s*:\s*["\'"]TechReviewer2024[^{}]*\}'
user_matches = re.findall(user_pattern, js, re.DOTALL)
for match in user_matches:
    print(f"[+] Datos del usuario encontrados:")
    print(match)
    
    # Buscar si hay algún campo adicional
    fields = re.findall(r'["\']([\w]+)["\']?\s*:\s*["\']([^"\']+)["\']', match)
    for field, value in fields:
        print(f"    {field}: {value}")

# Buscar strings en base64 que podrían contener información
print("\n[*] Decodificando strings base64...")
import base64
b64_pattern = r'[A-Za-z0-9+/]{20,}={0,2}'
b64_matches = re.findall(b64_pattern, js)
for match in set(b64_matches[:50]):
    try:
        decoded = base64.b64decode(match).decode('utf-8', errors='ignore')
        if 'HTB' in decoded or 'flag' in decoded.lower() or 'tech' in decoded.lower() or 'review' in decoded.lower():
            print(f"[+] Base64 decodificado: {decoded[:200]}")
    except:
        pass

# Buscar si hay algún endpoint oculto
print("\n[*] Buscando endpoints ocultos...")
endpoint_patterns = [
    r'["\'/]api/[^"\'\\s]+',
    r'["\'/]hidden/[^"\'\\s]+',
    r'["\'/]secret/[^"\'\\s]+',
    r'["\'/]admin/[^"\'\\s]+',
    r'["\'/]debug/[^"\'\\s]+',
    r'["\'/]test/[^"\'\\s]+',
]

for pattern in endpoint_patterns:
    matches = re.findall(pattern, js)
    for match in set(matches):
        print(f"[+] Endpoint: {match}")

# Buscar menciones de otras plataformas sociales específicas
print("\n[*] Buscando plataformas sociales específicas...")
social_patterns = [
    r'github\.com/([^"\'\\s/]+)',
    r'gist\.github\.com/([^"\'\\s/]+)',
    r'pastebin\.com/([^"\'\\s/]+)',
    r'discord\.gg/([^"\'\\s/]+)',
    r'twitter\.com/([^"\'\\s/]+)',
    r'x\.com/([^"\'\\s/]+)',
    r'linkedin\.com/in/([^"\'\\s/]+)',
    r'reddit\.com/u/([^"\'\\s/]+)',
    r'reddit\.com/user/([^"\'\\s/]+)',
]

for pattern in social_patterns:
    matches = re.findall(pattern, js, re.IGNORECASE)
    if matches:
        for match in set(matches):
            print(f"[+] Encontrado: {pattern.split('.')[0].split('\\')[-1]} -> {match}")

# Buscar en el HTML también
print("\n[*] Analizando HTML...")
r = requests.get(BASE_URL)
html = r.text

# Buscar comentarios HTML
html_comments = re.findall(r'<!--(.*?)-->', html, re.DOTALL)
for comment in html_comments:
    if comment.strip():
        print(f"[+] Comentario HTML: {comment.strip()}")

# Buscar meta tags
meta_tags = re.findall(r'<meta[^>]+>', html)
for tag in meta_tags:
    if 'property' in tag or 'name' in tag:
        print(f"[+] Meta tag: {tag}")

print("\n[*] Búsqueda completa. Si no se encontró la flag, probablemente esté en una plataforma externa.")
print("[*] Revisar manualmente las redes sociales del usuario TechReviewer2024")