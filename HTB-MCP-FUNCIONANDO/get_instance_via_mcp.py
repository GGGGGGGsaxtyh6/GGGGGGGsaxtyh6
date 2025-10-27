#!/usr/bin/env python3
"""
Obtiene la información del challenge mediante el servidor MCP
y luego resuelve el challenge automáticamente
"""

import json
import subprocess
import os
import time
import socket
from Cryptodome.Util.number import long_to_bytes
import gmpy2
from functools import reduce
import requests

# Leer el token
with open('.env', 'r') as f:
    env_content = f.read()
    token = env_content.split('HTB_TOKEN=')[1].split('\n')[0]

env = os.environ.copy()
env['HTB_TOKEN'] = token

def get_active_challenges_api():
    """Intenta obtener challenges activos via API directa"""
    headers = {
        "Authorization": f"Bearer {token}",
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }
    
    # El endpoint correcto para challenges activos
    urls = [
        "https://labs.hackthebox.com/api/v4/challenge/active",
        "https://www.hackthebox.com/api/v4/challenge/active",
        "https://app.hackthebox.com/api/v4/challenge/active",
    ]
    
    for url in urls:
        try:
            print(f"[*] Intentando: {url}")
            r = requests.get(url, headers=headers, timeout=5)
            if r.status_code == 200:
                try:
                    data = r.json()
                    if 'data' in data:
                        for challenge in data['data']:
                            if challenge.get('id') == 365 or 'Baby Time Capsule' in challenge.get('name', ''):
                                print(f"[+] Challenge encontrado via API!")
                                if 'ip' in challenge:
                                    return challenge['ip']
                                if 'docker_ip' in challenge:
                                    return challenge['docker_ip']
                except:
                    pass
        except Exception as e:
            continue
    
    return None

def solve_with_hastad(host, port=1337):
    """Resuelve el challenge usando Hastad's attack"""
    print(f"\n[*] Conectando a {host}:{port} para resolver el challenge...")
    
    def chinese_remainder_theorem(remainders, moduli):
        total = 0
        prod = reduce(lambda a, b: a * b, moduli)
        for r_i, n_i in zip(remainders, moduli):
            p = prod // n_i
            total += r_i * gmpy2.invert(p, n_i) * p
        return total % prod
    
    def nth_root(num, n):
        high = 1
        while high ** n < num:
            high *= 2
        low = high // 2
        while low < high:
            mid = (low + high + 1) // 2
            if mid ** n > num:
                high = mid - 1
            else:
                low = mid
        return low
    
    # Recolectar 5 cápsulas
    capsules = []
    for i in range(5):
        try:
            print(f"[+] Recolectando cápsula {i+1}/5...")
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            s.connect((host, port))
            
            # Recibir prompt
            data = s.recv(4096)
            print(f"    Prompt: {data.decode('utf-8', errors='ignore')[:50]}...")
            
            # Enviar Y
            s.send(b'Y\n')
            
            # Recibir respuesta
            response = s.recv(4096).decode('utf-8', errors='ignore')
            
            # Buscar JSON en la respuesta
            json_start = response.find('{')
            if json_start != -1:
                json_str = response[json_start:]
                capsule_data = json.loads(json_str)
                
                c = int(capsule_data['time_capsule'], 16)
                n = int(capsule_data['pubkey'][0], 16)
                e = int(capsule_data['pubkey'][1], 16)
                
                capsules.append((c, n, e))
                print(f"    ✓ Cápsula obtenida (e={e})")
            
            s.close()
        except Exception as e:
            print(f"    Error: {e}")
            return None
    
    if len(capsules) < 5:
        return None
    
    # Aplicar Hastad's attack
    print("\n[+] Aplicando ataque de Hastad...")
    e = capsules[0][2]
    ciphertexts = [c for c, _, _ in capsules]
    moduli = [n for _, n, _ in capsules]
    
    # CRT
    m_e = chinese_remainder_theorem(ciphertexts, moduli)
    
    # Raíz e-ésima
    m = nth_root(m_e, e)
    
    # Convertir a bytes
    flag = long_to_bytes(m).decode('utf-8', errors='ignore')
    
    return flag

# Primero intentar obtener IP via API
print("[*] Intentando obtener IP del challenge via API...")
ip = get_active_challenges_api()

if not ip:
    print("\n[*] No se pudo obtener IP via API, usando servidor MCP...")
    
    # Usar servidor MCP
    p = subprocess.Popen(['./htb-mcp-server'], 
                        stdin=subprocess.PIPE, 
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE,
                        env=env, 
                        text=True)
    
    # Inicializar
    p.stdin.write('{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"0.1.0"}}\n')
    p.stdin.flush()
    p.stdout.readline()
    
    # Detener cualquier instancia previa y crear una nueva
    print("[*] Deteniendo instancias previas...")
    p.stdin.write('{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"stop_challenge","arguments":{"challenge_id":365}}}\n')
    p.stdin.flush()
    p.stdout.readline()
    
    time.sleep(2)
    
    print("[*] Iniciando nueva instancia...")
    p.stdin.write('{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"start_challenge","arguments":{"challenge_id":365}}}\n')
    p.stdin.flush()
    response = p.stdout.readline()
    
    print(f"[*] Respuesta: {response[:200]}...")
    
    # Esperar a que la instancia se inicie
    print("[*] Esperando 30 segundos para que la instancia se inicie...")
    time.sleep(30)
    
    p.terminate()

# Intentar con las IPs conocidas que tienen puerto 1337 abierto
print("\n[*] Probando IPs conocidas con puerto 1337...")
known_ips = [
    "94.237.49.102",
    "94.237.49.118", 
    "94.237.49.125",
    "94.237.49.154",
    "94.237.49.152",
    "94.237.49.142",
    "94.237.49.155"
]

for ip in known_ips:
    print(f"\n[*] Probando {ip}:1337...")
    
    # Verificar si es el challenge correcto
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(3)
        s.connect((ip, 1337))
        
        # Intentar recibir banner
        data = s.recv(1024)
        
        if b"Qubit" in data or b"capsule" in data.lower():
            print(f"[+] ¡Challenge encontrado en {ip}!")
            s.close()
            
            # Resolver el challenge
            flag = solve_with_hastad(ip)
            
            if flag and 'HTB{' in flag:
                print(f"\n[+] ¡FLAG ENCONTRADA!: {flag}")
                
                # Guardar la flag
                with open('flag.txt', 'w') as f:
                    f.write(flag)
                
                # Enviar la flag a HTB
                print("\n[*] Enviando flag a HackTheBox...")
                # Aquí iría el código para enviar la flag
                
                exit(0)
        
        s.close()
    except Exception as e:
        continue

print("\n[-] No se pudo encontrar o resolver el challenge")
print("[*] Es posible que necesites iniciar la instancia manualmente desde la web de HTB")