#!/usr/bin/env python3
import json
import subprocess
import os
import time
import requests

# Leer el token del archivo .env
with open('.env', 'r') as f:
    env_content = f.read()
    token = env_content.split('HTB_TOKEN=')[1].split('\n')[0]

env = os.environ.copy()
env['HTB_TOKEN'] = token

print("Obteniendo instancia activa del challenge...")

# Obtener instancia activa usando la API directamente
headers = {"Authorization": f"Bearer {token}"}

try:
    # Obtener instancias activas
    r = requests.get(
        "https://labs.hackthebox.com/api/v4/challenge/active",
        headers=headers
    )
    
    if r.status_code == 200:
        active = r.json()
        print(f"Respuesta de instancias activas: {json.dumps(active, indent=2)}")
        
        if 'data' in active and active['data']:
            for instance in active['data']:
                if instance.get('id') == 365 or 'Baby Time Capsule' in instance.get('name', ''):
                    print(f"\n=== INSTANCIA ENCONTRADA ===")
                    print(f"ID: {instance.get('id')}")
                    print(f"Nombre: {instance.get('name')}")
                    if 'ip' in instance:
                        print(f"IP: {instance['ip']}")
                    if 'port' in instance:
                        print(f"Puerto: {instance['port']}")
    else:
        print(f"Error obteniendo instancias: {r.status_code}")
        print(r.text)
        
except Exception as e:
    print(f"Error: {e}")

# También intentar con el servidor MCP
print("\n\nIntentando con servidor MCP...")
p = subprocess.Popen(['./htb-mcp-server'], 
                    stdin=subprocess.PIPE, 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE,
                    env=env, 
                    text=True)

# Inicializar
p.stdin.write('{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"0.1.0"}}\n')
p.stdin.flush()
init_response = p.stdout.readline()

# Obtener IP del challenge
p.stdin.write('{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"get_challenge_ip","arguments":{"challenge_id":365}}}\n')
p.stdin.flush()
ip_response = p.stdout.readline()
print(f"Respuesta IP: {ip_response}")

time.sleep(1)
p.terminate()