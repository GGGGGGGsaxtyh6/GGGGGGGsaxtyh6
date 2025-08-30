#!/usr/bin/env python3
import requests
import json

# Leer el token
with open('.env', 'r') as f:
    env_content = f.read()
    token = env_content.split('HTB_TOKEN=')[1].split('\n')[0]

headers = {
    "Authorization": f"Bearer {token}",
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

# Probar TODOS los endpoints posibles de la API v4
base_urls = [
    "https://www.hackthebox.com/api/v4",
    "https://labs.hackthebox.com/api/v4",
    "https://app.hackthebox.com/api/v4",
    "https://api.hackthebox.com/v4"
]

endpoints = [
    "/challenge/active",
    "/challenge/active/365",
    "/challenge/365/instance",
    "/challenge/365/connection",
    "/challenge/365/spawn",
    "/challenge/365/status",
    "/challenge/instance/active",
    "/challenge/instance/365",
    "/user/challenge/active",
    "/user/challenge/365",
    "/user/challenge/instance",
    "/user/active/challenge",
    "/user/active/challenge/365",
    "/user/instance/challenge",
    "/user/instance/365",
    "/instance/challenge/365",
    "/instance/active",
    "/instance/active/challenge",
    "/docker/challenge/365",
    "/docker/active",
    "/spawn/challenge/365",
    "/spawn/active",
    "/connection/challenge/365",
    "/connection/active"
]

print("[*] Probando todos los endpoints posibles...")

for base in base_urls:
    for endpoint in endpoints:
        url = base + endpoint
        try:
            r = requests.get(url, headers=headers, timeout=3)
            if r.status_code == 200:
                print(f"\n✓ ENCONTRADO: {url}")
                print(f"Status: {r.status_code}")
                try:
                    data = r.json()
                    print(json.dumps(data, indent=2))
                    
                    # Buscar IPs
                    text = json.dumps(data)
                    import re
                    ips = re.findall(r'\b(?:94\.237\.|83\.136\.|10\.)(?:[0-9]{1,3}\.){2}[0-9]{1,3}\b', text)
                    if ips:
                        print(f"\n[+] IPs ENCONTRADAS: {ips}")
                        
                except:
                    print(f"Respuesta: {r.text[:200]}")
            elif r.status_code not in [404, 401, 403]:
                print(f"  {url} -> {r.status_code}")
        except:
            continue

print("\n[*] Probando con el ID de instancia que conocemos...")

# Sabemos que la instancia ID es 1661710
instance_ids = ["1661710", "1661473", "1661434"]

for instance_id in instance_ids:
    endpoints = [
        f"/instance/{instance_id}",
        f"/instance/{instance_id}/connection",
        f"/instance/{instance_id}/status",
        f"/challenge/instance/{instance_id}",
        f"/user/instance/{instance_id}",
    ]
    
    for base in base_urls:
        for endpoint in endpoints:
            url = base + endpoint
            try:
                r = requests.get(url, headers=headers, timeout=3)
                if r.status_code == 200:
                    print(f"\n✓ ENCONTRADO con instance {instance_id}: {url}")
                    try:
                        data = r.json()
                        print(json.dumps(data, indent=2))
                    except:
                        print(f"Respuesta: {r.text[:200]}")
            except:
                continue