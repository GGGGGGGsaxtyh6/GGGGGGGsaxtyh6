#!/usr/bin/env python3
"""
Script para iniciar un challenge en HackTheBox usando el servidor MCP
"""

import subprocess
import json
import os
import sys
import time

def start_challenge(challenge_id):
    """
    Inicia un challenge usando el servidor MCP
    """
    
    # Verificar que existe el archivo .env
    if not os.path.exists('.env'):
        print("[-] ERROR: No se encuentra el archivo .env")
        print("[*] Copia .env.example a .env y añade tu token")
        return False
    
    # Leer el token
    with open('.env', 'r') as f:
        env_content = f.read()
        try:
            token = env_content.split('HTB_TOKEN=')[1].split('\n')[0]
        except:
            print("[-] ERROR: No se pudo leer el token del archivo .env")
            return False
    
    if token == 'TU_TOKEN_AQUI':
        print("[-] ERROR: Debes reemplazar TU_TOKEN_AQUI con tu token real en .env")
        return False
    
    env = os.environ.copy()
    env['HTB_TOKEN'] = token
    
    print(f"[*] Iniciando challenge {challenge_id} usando el servidor MCP...")
    
    # Iniciar el servidor MCP
    p = subprocess.Popen(['./htb-mcp-server'], 
                        stdin=subprocess.PIPE, 
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE,
                        env=env, 
                        text=True)
    
    try:
        # Inicializar el servidor
        p.stdin.write('{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"0.1.0"}}\n')
        p.stdin.flush()
        init_response = p.stdout.readline()
        
        # Iniciar el challenge
        start_msg = f'{{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{{"name":"start_challenge","arguments":{{"challenge_id":"{challenge_id}"}}}}}}\n'
        p.stdin.write(start_msg)
        p.stdin.flush()
        
        # Leer respuesta
        response = p.stdout.readline()
        
        try:
            data = json.loads(response)
            if 'result' in data:
                result = data['result']
                if 'content' in result:
                    for content in result['content']:
                        if content.get('type') == 'text':
                            text = content.get('text', '')
                            try:
                                instance_data = json.loads(text)
                                print(f"[+] Challenge iniciado exitosamente")
                                print(f"    Instance ID: {instance_data.get('id', 'Unknown')}")
                                return True
                            except:
                                if 'already' in text.lower():
                                    print("[*] El challenge ya está activo")
                                    return True
                                print(f"Respuesta: {text}")
                                return True
            elif 'error' in data:
                print(f"[-] Error: {data['error']}")
                return False
        except:
            print(f"[-] Error procesando respuesta: {response}")
            return False
            
    finally:
        p.terminate()
    
    return False

def main():
    if len(sys.argv) != 2:
        print("Uso: python3 start_challenge.py <challenge_id>")
        print("Ejemplo: python3 start_challenge.py 365")
        sys.exit(1)
    
    try:
        challenge_id = int(sys.argv[1])
    except ValueError:
        print("[-] El ID del challenge debe ser un número")
        sys.exit(1)
    
    if start_challenge(challenge_id):
        print(f"\n[*] Esperando 5 segundos para que el challenge se inicialice...")
        time.sleep(5)
        
        # Ahora obtener la IP
        print(f"\n[*] Obteniendo IP del challenge...")
        os.system(f"python3 get_challenge_ip.py {challenge_id}")
    else:
        print("\n[-] No se pudo iniciar el challenge")

if __name__ == "__main__":
    main()