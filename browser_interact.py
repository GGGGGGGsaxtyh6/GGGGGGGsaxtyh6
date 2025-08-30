#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import time
import json
import re

BASE_URL = "http://94.237.57.115:35694"

# Como es una SPA, necesito ejecutar el JavaScript
# Voy a usar requests-html o buscar en el JS directamente

print("[*] Analizando el JavaScript de la aplicación más detalladamente...")

# Obtener el JS
r = requests.get(BASE_URL + "/assets/index-fPbXfhd6.js")
js_content = r.text

# Buscar objetos JSON en el código
print("\n[*] Buscando objetos JSON en el código...")
# Buscar patrones de objetos con información del usuario
json_patterns = [
    r'\{[^{}]*"username"\s*:\s*"TechReviewer2024"[^{}]*\}',
    r'\{[^{}]*"email"\s*:\s*"alex\.morgan@tempmail\.com"[^{}]*\}',
    r'\{[^{}]*TechReviewer2024[^{}]*\}',
]

for pattern in json_patterns:
    matches = re.findall(pattern, js_content, re.DOTALL)
    for match in matches:
        if len(match) < 5000:  # No mostrar matches muy largos
            print(f"[+] Objeto encontrado: {match[:500]}")
            # Intentar extraer más información
            if "HTB{" in match:
                flag = re.search(r'HTB\{[^}]+\}', match)
                if flag:
                    print(f"[!] FLAG: {flag.group()}")

# Buscar información específica del perfil
print("\n[*] Buscando información del perfil...")
# Buscar el contexto alrededor de TechReviewer2024
context_pattern = r'.{0,200}TechReviewer2024.{0,200}'
contexts = re.findall(context_pattern, js_content)
for context in contexts[:10]:  # Solo los primeros 10
    if 'HTB' in context or 'flag' in context.lower() or 'github' in context.lower() or 'social' in context.lower():
        print(f"[+] Contexto: {context}")

# Buscar URLs específicas
print("\n[*] Buscando URLs de redes sociales...")
url_patterns = [
    r'(https?://[^\s"\']+github[^\s"\']+)',
    r'(https?://[^\s"\']+twitter[^\s"\']+)',
    r'(https?://[^\s"\']+linkedin[^\s"\']+)',
    r'(https?://[^\s"\']+instagram[^\s"\']+)',
    r'(https?://[^\s"\']+facebook[^\s"\']+)',
    r'(https?://[^\s"\']+reddit[^\s"\']+)',
    r'(https?://[^\s"\']+medium[^\s"\']+)',
    r'(https?://[^\s"\']+youtube[^\s"\']+)',
    r'(https?://[^\s"\']+twitch[^\s"\']+)',
    r'(https?://[^\s"\']+discord[^\s"\']+)',
]

for pattern in url_patterns:
    matches = re.findall(pattern, js_content, re.IGNORECASE)
    if matches:
        for match in set(matches):
            print(f"[+] URL encontrada: {match}")

# Buscar el componente React del perfil
print("\n[*] Buscando componentes React...")
# Buscar el componente que renderiza el perfil
profile_patterns = [
    r'Profile[^{]*\{[^}]+\}',
    r'UserProfile[^{]*\{[^}]+\}',
    r'SocialConnect[^{]*\{[^}]+\}',
]

for pattern in profile_patterns:
    matches = re.findall(pattern, js_content)
    for match in matches[:5]:
        if 'TechReviewer' in match or 'alex' in match:
            print(f"[+] Componente: {match[:300]}")

# Buscar datos hardcodeados
print("\n[*] Buscando datos hardcodeados...")
# Buscar arrays o objetos con información
data_patterns = [
    r'const\s+\w+\s*=\s*\[[^\]]+\]',
    r'const\s+\w+\s*=\s*\{[^}]+\}',
    r'let\s+\w+\s*=\s*\[[^\]]+\]',
    r'let\s+\w+\s*=\s*\{[^}]+\}',
    r'var\s+\w+\s*=\s*\[[^\]]+\]',
    r'var\s+\w+\s*=\s*\{[^}]+\}',
]

for pattern in data_patterns:
    matches = re.findall(pattern, js_content)
    for match in matches:
        if 'TechReviewer' in match or 'alex' in match or 'HTB' in match:
            print(f"[+] Dato: {match[:500]}")

# Buscar en localStorage o sessionStorage
print("\n[*] Buscando referencias a storage...")
storage_patterns = [
    r'localStorage\.\w+\([^)]+\)',
    r'sessionStorage\.\w+\([^)]+\)',
    r'localStorage\[[\'"]\w+[\'"]\]',
    r'sessionStorage\[[\'"]\w+[\'"]\]',
]

for pattern in storage_patterns:
    matches = re.findall(pattern, js_content)
    for match in set(matches):
        print(f"[+] Storage: {match}")

# Buscar comentarios de desarrollador
print("\n[*] Buscando comentarios de desarrollador...")
comment_patterns = [
    r'//.*TODO.*',
    r'//.*FIXME.*',
    r'//.*NOTE.*',
    r'//.*HACK.*',
    r'//.*DEBUG.*',
    r'/\*.*TODO.*\*/',
    r'/\*.*FIXME.*\*/',
]

for pattern in comment_patterns:
    matches = re.findall(pattern, js_content, re.IGNORECASE)
    for match in set(matches):
        if len(match) < 200:
            print(f"[+] Comentario: {match}")

# Buscar información en formato específico
print("\n[*] Buscando información en formatos específicos...")
# El username sugiere que es un revisor, buscar reviews
review_patterns = [
    r'"review[^"]*"[^:]*:[^,}]+',
    r'"rating[^"]*"[^:]*:[^,}]+',
    r'"comment[^"]*"[^:]*:[^,}]+',
    r'"post[^"]*"[^:]*:[^,}]+',
    r'"blog[^"]*"[^:]*:[^,}]+',
]

for pattern in review_patterns:
    matches = re.findall(pattern, js_content, re.IGNORECASE)
    for match in set(matches):
        if 'TechReviewer' in match or 'alex' in match:
            print(f"[+] Review data: {match[:200]}")

# Imagen de perfil de Pexels - buscar si hay más información
print("\n[*] Analizando la imagen de perfil...")
img_url = "https://images.pexels.com/photos/220453/pexels-photo-220453.jpeg"
print(f"[+] Imagen de perfil: {img_url}")
print("[*] Esta es una imagen stock de Pexels, probablemente no contiene la flag")

# Buscar si hay alguna referencia a una imagen diferente o modificada
img_patterns = [
    r'(https?://[^\s"\']+\.(jpg|jpeg|png|gif|webp)[^\s"\']*)',
    r'src=["\'](/[^\s"\']+\.(jpg|jpeg|png|gif|webp)[^\s"\']*)["\']',
]

for pattern in img_patterns:
    matches = re.findall(pattern, js_content)
    for match in matches[:10]:
        if isinstance(match, tuple):
            match = match[0]
        if 'pexels' not in match and 'unsplash' not in match:
            print(f"[+] Otra imagen: {match}")