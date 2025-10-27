#!/usr/bin/env python3
import json
import subprocess
import os
import time

# Leer el token del archivo .env
with open('.env', 'r') as f:
    env_content = f.read()
    token = env_content.split('HTB_TOKEN=')[1].split('\n')[0]

env = os.environ.copy()
env['HTB_TOKEN'] = token

print("Iniciando servidor MCP...")
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
print(f"Init: {init_response}")

# Listar tools disponibles
print("\nListando tools disponibles...")
p.stdin.write('{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}\n')
p.stdin.flush()
tools_response = p.stdout.readline()
print(f"Tools: {tools_response}")

# Obtener perfil del usuario
print("\nObteniendo perfil del usuario...")
p.stdin.write('{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"get_user_profile","arguments":{}}}\n')
p.stdin.flush()
profile_response = p.stdout.readline()
print(f"Perfil: {profile_response}")

# Listar challenges
print("\nListando challenges...")
p.stdin.write('{"jsonrpc":"2.0","id":4,"method":"tools/call","params":{"name":"list_challenges","arguments":{}}}\n')
p.stdin.flush()
challenges_response = p.stdout.readline()
print(f"Challenges: {challenges_response}")

# Buscar el challenge 365 específicamente
print("\nBuscando Baby Time Capsule (ID 365)...")
try:
    challenges_data = json.loads(challenges_response)
    if 'result' in challenges_data and 'content' in challenges_data['result']:
        content = challenges_data['result']['content'][0]['text']
        # Parsear el contenido JSON
        challenges = json.loads(content)
        for challenge in challenges:
            if challenge.get('id') == 365 or 'Baby Time Capsule' in challenge.get('name', ''):
                print(f"Encontrado: {json.dumps(challenge, indent=2)}")
except Exception as e:
    print(f"Error parseando challenges: {e}")

time.sleep(1)
p.terminate()