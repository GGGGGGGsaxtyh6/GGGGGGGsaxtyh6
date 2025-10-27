#!/usr/bin/env python3
import subprocess
import json
import os
import time

# Leer el token
with open('.env', 'r') as f:
    env_content = f.read()
    token = env_content.split('HTB_TOKEN=')[1].split('\n')[0]

env = os.environ.copy()
env['HTB_TOKEN'] = token

print("[*] Iniciando servidor MCP para obtener información...")

# Iniciar el servidor MCP
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
print(f"Init: {init_response[:100]}")

# Listar herramientas disponibles
p.stdin.write('{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}\n')
p.stdin.flush()
tools = p.stdout.readline()
print(f"\n[*] Herramientas disponibles:")
try:
    tools_data = json.loads(tools)
    if 'result' in tools_data and 'tools' in tools_data['result']:
        for tool in tools_data['result']['tools']:
            print(f"  - {tool['name']}: {tool.get('description', '')[:60]}")
except:
    pass

# Intentar obtener información del challenge 365
print("\n[*] Obteniendo información del challenge 365...")

# Buscar el challenge
p.stdin.write('{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"search_content","arguments":{"query":"Baby Time Capsule"}}}\n')
p.stdin.flush()
search_result = p.stdout.readline()
print(f"Búsqueda: {search_result[:200]}")

# Intentar obtener info específica
p.stdin.write('{"jsonrpc":"2.0","id":4,"method":"tools/call","params":{"name":"search_content","arguments":{"query":"365 docker ip port"}}}\n')
p.stdin.flush()
info_result = p.stdout.readline()
print(f"Info: {info_result[:200]}")

# Ver si hay alguna herramienta para obtener IPs de challenges
p.stdin.write('{"jsonrpc":"2.0","id":5,"method":"tools/call","params":{"name":"get_active_instances","arguments":{}}}\n')
p.stdin.flush()
active = p.stdout.readline()
print(f"Active: {active[:200]}")

p.terminate()

print("\n[*] Intentando con la API directamente con el token...")

import requests

headers = {
    "Authorization": f"Bearer {token}",
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

# El endpoint correcto según el README del MCP
url = "https://labs.hackthebox.com/api/v4/challenge/info/365"
print(f"\nProbando: {url}")
r = requests.get(url, headers=headers)
print(f"Status: {r.status_code}")

if r.status_code == 200:
    try:
        data = r.json()
        if 'challenge' in data:
            challenge = data['challenge']
            print(f"\n[+] Información del challenge:")
            print(f"  Nombre: {challenge.get('name')}")
            print(f"  ID: {challenge.get('id')}")
            
            # Buscar IP y puerto
            if 'docker_ip' in challenge:
                print(f"  Docker IP: {challenge['docker_ip']}")
            if 'docker_ports' in challenge:
                print(f"  Docker Ports: {challenge['docker_ports']}")
                
            # Buscar en todo el objeto
            text = json.dumps(challenge)
            import re
            ips = re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', text)
            if ips:
                print(f"\n[+] IPs encontradas en la respuesta: {ips}")
                
                # Si encontramos una IP, resolver el challenge
                for ip in ips:
                    if ip.startswith('94.') or ip.startswith('83.'):
                        print(f"\n[+] Resolviendo challenge en {ip}:1337...")
                        result = subprocess.run(
                            ["python3", "solve_baby_time_capsule.py", ip, "1337"],
                            capture_output=True,
                            text=True,
                            timeout=60
                        )
                        if "FLAG" in result.stdout or "HTB{" in result.stdout:
                            print(result.stdout)
                            exit(0)
        else:
            print(json.dumps(data, indent=2))
    except Exception as e:
        print(f"Error: {e}")
        print(f"Respuesta: {r.text[:500]}")
else:
    print(f"Error: {r.text[:200]}")