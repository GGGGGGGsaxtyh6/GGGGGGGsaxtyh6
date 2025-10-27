#!/usr/bin/env python3
import json
import subprocess
import os
import sys
import time

# Leer el token del archivo .env
with open('.env', 'r') as f:
    env_content = f.read()
    token = env_content.split('HTB_TOKEN=')[1].split('\n')[0]

env = os.environ.copy()
env['HTB_TOKEN'] = token

# Iniciar el servidor MCP
print("Iniciando servidor MCP...")
p = subprocess.Popen(['./htb-mcp-server'], 
                    stdin=subprocess.PIPE, 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE,
                    env=env, 
                    text=True)

# Inicializar el protocolo
print("Inicializando protocolo...")
p.stdin.write('{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"0.1.0"}}\n')
p.stdin.flush()
init_response = p.stdout.readline()
print(f"Respuesta init: {init_response}")

# Iniciar el challenge 365 (Baby Time Capsule)
challenge_id = "365"
print(f"Iniciando challenge {challenge_id}...")
p.stdin.write(f'{{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{{"name":"start_challenge","arguments":{{"challenge_id":{challenge_id}}}}}}}\n')
p.stdin.flush()

response = p.stdout.readline()
print(f"Respuesta: {response}")

# Obtener información del challenge
print("Obteniendo información del challenge...")
p.stdin.write(f'{{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{{"name":"get_challenge_info","arguments":{{"challenge_id":{challenge_id}}}}}}}\n')
p.stdin.flush()

info_response = p.stdout.readline()
print(f"Info del challenge: {info_response}")

# Parsear la respuesta para obtener IP y puerto
try:
    data = json.loads(response)
    if 'result' in data:
        result = data['result']
        print("\n=== Challenge iniciado ===")
        print(f"Resultado completo: {json.dumps(result, indent=2)}")
except Exception as e:
    print(f"Error parseando respuesta: {e}")

# Mantener el proceso vivo un momento para asegurar que se inició
time.sleep(2)
p.terminate()