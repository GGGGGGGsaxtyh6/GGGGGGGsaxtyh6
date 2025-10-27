#!/usr/bin/env python3
import requests
import json

# Leer el token
with open('.env', 'r') as f:
    env_content = f.read()
    token = env_content.split('HTB_TOKEN=')[1].split('\n')[0]

headers = {
    "Authorization": f"Bearer {token}",
    "User-Agent": "HTB MCP Server",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

print("[*] Obteniendo instancias activas...")

# Endpoint correcto según el código del MCP
url = "https://labs.hackthebox.com/api/v4/challenge/active"
print(f"Probando: {url}")

r = requests.get(url, headers=headers)
print(f"Status: {r.status_code}")

if r.status_code == 200:
    try:
        data = r.json()
        print(json.dumps(data, indent=2))
        
        # Buscar la instancia de Baby Time Capsule
        for item in data:
            if isinstance(item, dict):
                if item.get('challenge_id') == 365 or 'Baby Time Capsule' in str(item):
                    print(f"\n[+] Instancia encontrada: {item}")
                    
                    # Buscar IPs
                    text = json.dumps(item)
                    import re
                    ips = re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', text)
                    if ips:
                        print(f"[+] IPs: {ips}")
    except Exception as e:
        print(f"Error parsing JSON: {e}")
        print(f"Respuesta raw: {r.text[:500]}")
else:
    print(f"Respuesta: {r.text[:500]}")

# Probar obtener info del challenge directamente
print("\n[*] Obteniendo info del challenge 365...")
url = "https://labs.hackthebox.com/api/v4/challenge/365"
r = requests.get(url, headers=headers)
print(f"Status: {r.status_code}")

if r.status_code == 200:
    try:
        data = r.json()
        print(json.dumps(data, indent=2))
    except:
        print(f"Respuesta: {r.text[:500]}")

# Probar con el endpoint de activity
print("\n[*] Obteniendo actividad...")
url = "https://labs.hackthebox.com/api/v4/challenge/activity"
r = requests.get(url, headers=headers)
print(f"Status: {r.status_code}")

if r.status_code == 200:
    try:
        data = r.json()
        if isinstance(data, list):
            for item in data:
                if '365' in str(item) or 'Baby' in str(item):
                    print(f"Actividad relacionada: {item}")
    except:
        pass

# Probar obtener la conexión
print("\n[*] Obteniendo conexión del challenge...")
url = "https://labs.hackthebox.com/api/v4/connection/status"
r = requests.get(url, headers=headers)
print(f"Status: {r.status_code}")

if r.status_code == 200:
    try:
        data = r.json()
        print(json.dumps(data, indent=2))
    except:
        print(f"Respuesta: {r.text[:500]}")