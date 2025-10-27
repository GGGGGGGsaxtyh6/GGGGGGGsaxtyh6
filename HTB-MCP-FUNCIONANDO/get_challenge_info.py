#!/usr/bin/env python3
import requests
import json
import time

# Leer el token
with open('.env', 'r') as f:
    env_content = f.read()
    token = env_content.split('HTB_TOKEN=')[1].split('\n')[0]

challenge_id = 365
headers = {"Authorization": f"Bearer {token}"}

print("Obteniendo información del challenge...")

# Intentar obtener la información del challenge varias veces
for attempt in range(5):
    try:
        # Obtener información del challenge
        r = requests.get(
            f"https://labs.hackthebox.com/api/v4/challenge/info/{challenge_id}",
            headers=headers
        )
        
        if r.status_code == 200:
            data = r.json()
            print(f"\nRespuesta completa: {json.dumps(data, indent=2)}")
            
            if 'challenge' in data:
                challenge = data['challenge']
                if 'docker_ip' in challenge and challenge['docker_ip']:
                    print(f"\n=== Información del Challenge ===")
                    print(f"IP: {challenge['docker_ip']}")
                    if 'docker_ports' in challenge and challenge['docker_ports']:
                        print(f"Puerto(s): {challenge['docker_ports']}")
                    break
                else:
                    print(f"Intento {attempt+1}: Challenge iniciándose, esperando...")
                    time.sleep(5)
        else:
            print(f"Error: {r.status_code}")
            print(r.text)
            
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(3)

# También intentar obtener las instancias activas
print("\n\nObteniendo instancias activas...")
try:
    r = requests.get(
        "https://labs.hackthebox.com/api/v4/challenge/active",
        headers=headers
    )
    if r.status_code == 200:
        active = r.json()
        print(f"Instancias activas: {json.dumps(active, indent=2)}")
except Exception as e:
    print(f"Error obteniendo instancias activas: {e}")