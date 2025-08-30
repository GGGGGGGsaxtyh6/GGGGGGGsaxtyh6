#!/usr/bin/env python3
import requests
import re

username = "TechReviewer2024"
print(f"[*] Intentando obtener el perfil de {username} en X/Twitter...")

# Headers que simulan un navegador real
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

# Intentar diferentes URLs
urls = [
    f"https://x.com/{username}",
    f"https://twitter.com/{username}",
    f"https://mobile.x.com/{username}",
    f"https://mobile.twitter.com/{username}",
]

for url in urls:
    print(f"\n[*] Intentando: {url}")
    try:
        session = requests.Session()
        r = session.get(url, headers=headers, allow_redirects=True, timeout=10)
        
        print(f"    Status: {r.status_code}")
        
        if r.status_code == 200:
            content = r.text
            
            # Buscar emails con formato Nombre.Apellido
            email_pattern = r'([A-Z][a-z]+\.[A-Z][a-z]+@[a-z]+\.[a-z]+)'
            emails = re.findall(email_pattern, content)
            for email in emails:
                print(f"[!] Email encontrado: {email}")
            
            # Buscar la flag directamente
            flag_pattern = r'HTB\{([^}]+)\}'
            flags = re.findall(flag_pattern, content, re.IGNORECASE)
            for flag in flags:
                print(f"[!] FLAG ENCONTRADA: HTB{{{flag}}}")
            
            # Buscar información en JSON-LD o meta tags
            meta_patterns = [
                r'<meta[^>]*property="og:description"[^>]*content="([^"]+)"',
                r'<meta[^>]*name="description"[^>]*content="([^"]+)"',
                r'"description":"([^"]+)"',
                r'"email":"([^"]+)"',
            ]
            
            for pattern in meta_patterns:
                matches = re.findall(pattern, content)
                for match in matches:
                    if '@' in match:
                        print(f"[+] Meta info: {match}")
            
            # Buscar en el contenido de la bio
            bio_patterns = [
                r'"description":"([^"]+)"',
                r'data-testid="UserDescription"[^>]*>([^<]+)',
                r'class="[^"]*bio[^"]*"[^>]*>([^<]+)',
            ]
            
            for pattern in bio_patterns:
                matches = re.findall(pattern, content)
                for match in matches:
                    if match and len(match) > 10:
                        print(f"[+] Bio: {match[:200]}")
            
            # Guardar el contenido para análisis manual
            if len(content) > 1000:  # Si tiene contenido sustancial
                with open(f'/workspace/twitter_profile_{username}.html', 'w') as f:
                    f.write(content)
                print(f"[+] Contenido guardado en twitter_profile_{username}.html")
                
                # Buscar todos los emails en el contenido
                all_emails = re.findall(r'[\w\.\-]+@[\w\.\-]+\.[\w]+', content)
                unique_emails = set(all_emails)
                if unique_emails:
                    print("[+] Todos los emails encontrados:")
                    for email in unique_emails:
                        if 'twitter' not in email and 'x.com' not in email:
                            print(f"    - {email}")
    except Exception as e:
        print(f"    Error: {e}")

print("\n[*] Si no se encontró el email, posibles opciones:")
print("    1. El perfil requiere JavaScript para cargar")
print("    2. El email está en los tweets del usuario")
print("    3. El perfil no existe o está protegido")
print("    4. Necesitas buscar manualmente en x.com/TechReviewer2024")