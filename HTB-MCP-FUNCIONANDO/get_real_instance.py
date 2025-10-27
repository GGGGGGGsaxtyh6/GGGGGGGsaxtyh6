#!/usr/bin/env python3
import requests
import json
import time

# Leer el token
with open('.env', 'r') as f:
    env_content = f.read()
    token = env_content.split('HTB_TOKEN=')[1].split('\n')[0]

headers = {
    "Authorization": f"Bearer {token}",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json",
    "Referer": "https://app.hackthebox.com/"
}

print("[*] Obteniendo información de la instancia activa...")

# Intentar obtener la instancia por su ID
instance_id = 1661347  # La última instancia creada

# Intentar diferentes endpoints de la API v4
api_endpoints = [
    "https://www.hackthebox.com/api/v4",
    "https://app.hackthebox.com/api/v4",
    "https://labs.hackthebox.com/api/v4",
    "https://www.hackthebox.eu/api/v4"
]

for base_url in api_endpoints:
    print(f"\n[*] Probando base URL: {base_url}")
    
    # Obtener información del usuario primero
    try:
        r = requests.get(f"{base_url}/user/info", headers=headers, timeout=5)
        if r.status_code == 200:
            print(f"[+] API válida encontrada: {base_url}")
            user_data = r.json()
            print(f"[+] Usuario: {user_data.get('info', {}).get('name', 'Unknown')}")
            
            # Ahora intentar obtener las instancias activas
            endpoints_to_try = [
                f"{base_url}/challenge/active",
                f"{base_url}/challenge/own",
                f"{base_url}/challenge/spawned",
                f"{base_url}/sp/machines",
                f"{base_url}/sp/challenges"
            ]
            
            for endpoint in endpoints_to_try:
                try:
                    print(f"\n[*] Intentando: {endpoint}")
                    r = requests.get(endpoint, headers=headers, timeout=5)
                    if r.status_code == 200:
                        data = r.json()
                        if data:
                            print(f"[+] Datos encontrados: {json.dumps(data, indent=2)[:500]}")
                            
                            # Buscar Baby Time Capsule
                            if isinstance(data, dict) and 'data' in data:
                                for item in data['data']:
                                    if 'baby' in str(item).lower() or 'time' in str(item).lower() or 'capsule' in str(item).lower():
                                        print(f"\n[+] ENCONTRADO: {json.dumps(item, indent=2)}")
                except Exception as e:
                    continue
            
            break
    except Exception as e:
        continue

# Intentar con la API de spawning platform
print("\n[*] Intentando API de Spawning Platform...")
sp_headers = headers.copy()
sp_headers["X-Requested-With"] = "XMLHttpRequest"

try:
    # Obtener máquinas/challenges activos en spawning platform
    r = requests.get("https://app.hackthebox.com/api/v4/sp/overview", headers=sp_headers, timeout=5)
    if r.status_code == 200:
        data = r.json()
        print(f"[+] Spawning Platform data: {json.dumps(data, indent=2)[:1000]}")
except Exception as e:
    print(f"[-] Error: {e}")

# Intentar obtener directamente por el ID de la instancia
print(f"\n[*] Intentando obtener instancia {instance_id} directamente...")
for base_url in api_endpoints:
    try:
        r = requests.get(f"{base_url}/challenge/instance/{instance_id}/connection", headers=headers, timeout=5)
        if r.status_code == 200:
            data = r.json()
            print(f"[+] Conexión encontrada: {json.dumps(data, indent=2)}")
            break
    except:
        pass