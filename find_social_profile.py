#!/usr/bin/env python3
import requests
import re

# Información del usuario
username = "TechReviewer2024"
print(f"[*] Buscando el perfil real de {username} en redes sociales...")
print("[*] Este es un challenge OSINT - el email real debe estar en algún perfil social")
print()

# Intentar X/Twitter con diferentes métodos
print("[*] Intentando X/Twitter...")
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

# Probar el perfil directamente
urls_to_try = [
    f"https://x.com/{username}",
    f"https://twitter.com/{username}",
    f"https://mobile.twitter.com/{username}",
]

for url in urls_to_try:
    try:
        r = requests.get(url, headers=headers, allow_redirects=True, timeout=5)
        if r.status_code == 200:
            # Buscar información en el HTML
            # Buscar emails
            emails = re.findall(r'[\w\.\-]+@[\w\.\-]+\.[\w]+', r.text)
            for email in emails:
                if 'twitter' not in email and 'x.com' not in email:
                    print(f"[+] Email encontrado en {url}: {email}")
            
            # Buscar el patrón HTB{...}
            htb_flags = re.findall(r'HTB\{[^}]+\}', r.text, re.IGNORECASE)
            for flag in htb_flags:
                print(f"[!] FLAG ENCONTRADA: {flag}")
            
            # Buscar información en la bio
            bio_pattern = r'"description":"([^"]+)"'
            bio_matches = re.findall(bio_pattern, r.text)
            for bio in bio_matches:
                if '@' in bio or 'email' in bio.lower():
                    print(f"[+] Bio con información: {bio}")
    except Exception as e:
        pass

# Intentar con la API de nitter (instancia pública de Twitter sin JS)
print("\n[*] Intentando con Nitter (visor alternativo de Twitter)...")
nitter_instances = [
    "nitter.net",
    "nitter.cz", 
    "nitter.poast.org",
    "nitter.privacydev.net",
]

for instance in nitter_instances:
    try:
        url = f"https://{instance}/{username}"
        r = requests.get(url, headers=headers, timeout=5)
        if r.status_code == 200:
            print(f"[+] Encontrado en {instance}")
            # Buscar información
            content = r.text
            
            # Buscar emails
            emails = re.findall(r'[\w\.\-]+@[\w\.\-]+\.[\w]+', content)
            for email in emails:
                if 'nitter' not in email:
                    print(f"[+] Email: {email}")
            
            # Buscar HTB flags
            flags = re.findall(r'HTB\{[^}]+\}', content, re.IGNORECASE)
            for flag in flags:
                print(f"[!] FLAG: {flag}")
            
            # Buscar en la bio
            bio_pattern = r'<div class="profile-bio">([^<]+)</div>'
            bio_matches = re.findall(bio_pattern, content)
            for bio in bio_matches:
                if '@' in bio:
                    print(f"[+] Bio: {bio}")
            
            break
    except:
        continue

print("\n[*] Si no se encontró la flag, es posible que:")
print("    1. El perfil esté en otra red social")
print("    2. La información esté en los tweets/posts del usuario")
print("    3. Necesites buscar manualmente en X.com/TechReviewer2024")