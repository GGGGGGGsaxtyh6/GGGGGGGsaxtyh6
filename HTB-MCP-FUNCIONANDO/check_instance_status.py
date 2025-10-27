#!/usr/bin/env python3
import json
import subprocess
import os
import time
import sys

# Leer el token del archivo .env
with open('.env', 'r') as f:
    env_content = f.read()
    token = env_content.split('HTB_TOKEN=')[1].split('\n')[0]

env = os.environ.copy()
env['HTB_TOKEN'] = token

print("Verificando estado de la instancia del challenge...")

# Iniciar servidor MCP
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

# Intentar obtener el estado del challenge
print("\n1. Verificando si el challenge está iniciado...")
challenge_id = 365

# Intentar iniciar el challenge nuevamente para obtener la IP
print(f"\n2. Iniciando/verificando challenge {challenge_id}...")
p.stdin.write(f'{{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{{"name":"start_challenge","arguments":{{"challenge_id":{challenge_id}}}}}}}\n')
p.stdin.flush()

response = p.stdout.readline()
print(f"Respuesta: {response}")

try:
    data = json.loads(response)
    if 'result' in data and 'content' in data['result']:
        content = data['result']['content'][0]['text']
        print(f"\nContenido de la respuesta:")
        print(content)
        
        # Intentar parsear el contenido como JSON
        try:
            instance_data = json.loads(content)
            print(f"\nDatos de la instancia:")
            print(f"ID: {instance_data.get('id')}")
            print(f"Mensaje: {instance_data.get('message')}")
            
            # Si tenemos un ID, podríamos necesitar esperar a que se inicie
            if instance_data.get('id'):
                print(f"\n3. Esperando 30 segundos para que la instancia se inicie completamente...")
                time.sleep(30)
                
                # Intentar obtener información actualizada
                print("\n4. Obteniendo información actualizada...")
                # Aquí podríamos hacer otra llamada para obtener la IP
                
        except json.JSONDecodeError:
            print("El contenido no es JSON válido")
            
except Exception as e:
    print(f"Error procesando respuesta: {e}")

print("\n5. Información para conectar manualmente:")
print("- El challenge 'Baby Time Capsule' usa el puerto 1337 por defecto")
print("- La instancia ID es: 1661326")
print("- Necesitas obtener la IP de la instancia desde la interfaz web de HTB")
print("\nPasos manuales:")
print("1. Ve a https://app.hackthebox.com/challenges")
print("2. Busca 'Baby Time Capsule'")
print("3. Click en 'Start Instance' si no está iniciada")
print("4. Copia la IP que aparece")
print("5. Ejecuta: python3 solve_baby_time_capsule.py <IP> 1337")

time.sleep(1)
p.terminate()