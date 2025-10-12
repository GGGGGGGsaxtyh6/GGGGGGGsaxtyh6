#!/usr/bin/env python3
"""
¿Qué pasa si creo mi PROPIO subdominio que termine en motherland.com?

Usaré un servicio DNS público que me permita crear subdominios arbitrarios.

Servicios conocidos:
- nip.io: 10.0.0.1.nip.io resuelve a 10.0.0.1
- sslip.io: similar
- xip.io: similar

PERO necesito que el subdominio TERMINE en motherland.com

¿Existe algún servicio que me permita X.motherland.com que YO controle?

NO, a menos que controle motherland.com

PERO... ¿qué pasa si registro un dominio que SE LLAME "something-motherland.com"?

No, el regex verifica que TERMINE con motherland.com, no que contenga el string.

Regex: /motherland\.com$/

El $ es anchoring al final. No hay bypass obvio.

A MENOS que haya un bug en el regex engine de PHP 7.0...

PCRE en PHP 7.0 tiene algunos bugs conocidos con:
- Newlines y el anchor $
- Unicode characters
- Null bytes

Ya probé newlines y null bytes, no funcionaron.

¿Unicode?
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

# Probar con caracteres Unicode en el dominio
test_urls_unicode = [
    "http://motherland.com\u0000/",  # Null byte Unicode
    "http://motherland.com\u200b/",  # Zero-width space
    "http://motherland.com\ufeff/",  # Zero-width no-break space (BOM)
    "http://motherland.com\u2028/",  # Line separator
    "http://motherland.com\u2029/",  # Paragraph separator
    "http://moth\u0065rland.com/",  # Unicode 'e'
    "http://motherla\u006Ed.com/",  # Unicode 'n'
]

print("[*] Probando URLs con caracteres Unicode...")
for url in test_urls_unicode:
    print(f"[*] URL: {repr(url)}")
    data_req = {
        'url': url,
        'data[test]': 'value'
    }
    
    try:
        resp = session.post(f"{TARGET}/communicate.php", data=data_req, timeout=10)
        
        if "Wrong URL" in resp.text:
            print(f"    [-] Wrong URL")
        elif "Failed when parsing" in resp.text:
            print(f"    [-] Failed parsing")
        elif "cURL Error" in resp.text:
            import re
            match = re.search(r'cURL Error: ([^<]+)', resp.text)
            if match:
                error = match.group(1).strip()
                print(f"    Error: {error[:70]}")
        else:
            print(f"    [?] Respuesta inesperada")
    except Exception as e:
        print(f"    Exception: {e}")
