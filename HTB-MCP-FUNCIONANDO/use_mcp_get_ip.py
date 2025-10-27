#!/usr/bin/env python3
"""
Usa el servidor MCP directamente para obtener la IP del challenge
"""

import json
import subprocess
import os
import time

# Leer el token
with open('.env', 'r') as f:
    env_content = f.read()
    token = env_content.split('HTB_TOKEN=')[1].split('\n')[0]

env = os.environ.copy()
env['HTB_TOKEN'] = token

print("[*] Usando servidor MCP para obtener información del challenge...")

p = subprocess.Popen(['./htb-mcp-server'], 
                    stdin=subprocess.PIPE, 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE,
                    env=env, 
                    text=True)

# Inicializar
p.stdin.write('{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"0.1.0"}}\n')
p.stdin.flush()
init = p.stdout.readline()
print(f"Init: {init}")

# Listar herramientas disponibles
print("\n[*] Herramientas disponibles:")
p.stdin.write('{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}\n')
p.stdin.flush()
tools = p.stdout.readline()
try:
    tools_data = json.loads(tools)
    if 'result' in tools_data and 'tools' in tools_data['result']:
        for tool in tools_data['result']['tools']:
            print(f"  - {tool['name']}: {tool.get('description', '')[:50]}...")
except:
    pass

# Intentar obtener IP del challenge
print("\n[*] Intentando obtener IP del challenge 365...")

# Probar diferentes comandos
commands = [
    '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"get_challenge_ip","arguments":{"challenge_id":365}}}',
    '{"jsonrpc":"2.0","id":4,"method":"tools/call","params":{"name":"get_challenge_connection","arguments":{"challenge_id":365}}}',
    '{"jsonrpc":"2.0","id":5,"method":"tools/call","params":{"name":"get_docker_ip","arguments":{"challenge_id":365}}}',
    '{"jsonrpc":"2.0","id":6,"method":"tools/call","params":{"name":"get_instance_ip","arguments":{"instance_id":1661428}}}',
    '{"jsonrpc":"2.0","id":7,"method":"tools/call","params":{"name":"challenge_info","arguments":{"challenge_id":365}}}',
]

for cmd in commands:
    print(f"\n[*] Ejecutando: {cmd[:80]}...")
    p.stdin.write(cmd + '\n')
    p.stdin.flush()
    response = p.stdout.readline()
    
    try:
        data = json.loads(response)
        if 'result' in data and 'content' in data['result']:
            content = data['result']['content'][0]['text']
            print(f"Respuesta: {content[:500]}")
            
            # Buscar IPs en la respuesta
            import re
            ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
            ips = re.findall(ip_pattern, content)
            if ips:
                print(f"[+] IPs encontradas: {ips}")
    except:
        print(f"Respuesta raw: {response[:200]}")

# Intentar reiniciar el challenge para obtener nueva IP
print("\n[*] Reiniciando challenge para obtener IP...")
p.stdin.write('{"jsonrpc":"2.0","id":8,"method":"tools/call","params":{"name":"stop_challenge","arguments":{"challenge_id":365}}}\n')
p.stdin.flush()
p.stdout.readline()

time.sleep(3)

p.stdin.write('{"jsonrpc":"2.0","id":9,"method":"tools/call","params":{"name":"start_challenge","arguments":{"challenge_id":365}}}\n')
p.stdin.flush()
start_response = p.stdout.readline()

print(f"\n[*] Respuesta de inicio: {start_response}")

try:
    data = json.loads(start_response)
    if 'result' in data and 'content' in data['result']:
        content = json.loads(data['result']['content'][0]['text'])
        instance_id = content.get('id')
        print(f"[+] Nueva instancia: {instance_id}")
        
        # Esperar y obtener información
        print("[*] Esperando 60 segundos para que se inicie...")
        time.sleep(60)
        
        # Intentar obtener información de la nueva instancia
        p.stdin.write(f'{{"jsonrpc":"2.0","id":10,"method":"tools/call","params":{{"name":"get_instance_info","arguments":{{"instance_id":{instance_id}}}}}}}\n')
        p.stdin.flush()
        info = p.stdout.readline()
        print(f"Info: {info}")
except:
    pass

p.terminate()

print("\n[*] Si no se pudo obtener la IP, la instancia está creada pero HTB no expone la IP via API")
print("[*] Necesitas obtener la IP manualmente desde https://app.hackthebox.com/challenges/365")