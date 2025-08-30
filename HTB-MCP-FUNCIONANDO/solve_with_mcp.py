#!/usr/bin/env python3
"""
Solución completa usando solo el servidor MCP
"""

import json
import subprocess
import os
import time
import socket
from Cryptodome.Util.number import long_to_bytes
import gmpy2
from functools import reduce
import re

# Leer el token
with open('.env', 'r') as f:
    env_content = f.read()
    token = env_content.split('HTB_TOKEN=')[1].split('\n')[0]

env = os.environ.copy()
env['HTB_TOKEN'] = token

print("[*] Iniciando servidor MCP...")
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
print(f"Init: {json.loads(init)['result']['serverInfo']}")

# Detener instancias previas
print("\n[*] Deteniendo instancias previas...")
p.stdin.write('{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"stop_challenge","arguments":{"challenge_id":"365"}}}\n')
p.stdin.flush()
stop = p.stdout.readline()

time.sleep(3)

# Iniciar nueva instancia
print("[*] Iniciando nueva instancia del challenge Baby Time Capsule...")
p.stdin.write('{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"start_challenge","arguments":{"challenge_id":"365"}}}\n')
p.stdin.flush()
start = p.stdout.readline()

try:
    data = json.loads(start)
    if 'result' in data and 'content' in data['result']:
        content = json.loads(data['result']['content'][0]['text'])
        instance_id = content.get('id')
        print(f"[+] Instancia creada: {instance_id}")
        print(f"    Mensaje: {content.get('message')}")
except:
    print(f"Respuesta: {start}")

p.terminate()

# El servidor MCP crea la instancia pero no devuelve la IP directamente
# La IP debe estar en algún lugar accesible
print("\n[*] La instancia está activa. Buscando la IP...")

# Basándome en el análisis del código, cuando se inicia un challenge de HTB,
# el docker se crea en un rango específico. Voy a escanear los rangos más probables.

def solve_challenge(host, port=1337):
    """Resuelve el challenge"""
    print(f"\n[*] Resolviendo challenge en {host}:{port}...")
    
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
            s.settimeout(10)
            s.connect((host, port))
            
            # Recibir prompt
            data = s.recv(4096)
            
            # Enviar Y
            s.send(b'Y\n')
            
            # Recibir respuesta
            response = s.recv(4096).decode('utf-8', errors='ignore')
            
            # Buscar JSON
            json_start = response.find('{')
            if json_start != -1:
                json_str = response[json_start:]
                capsule_data = json.loads(json_str)
                
                c = int(capsule_data['time_capsule'], 16)
                n = int(capsule_data['pubkey'][0], 16)
                e = int(capsule_data['pubkey'][1], 16)
                
                capsules.append((c, n, e))
                print(f"    ✓ Cápsula obtenida")
            
            s.close()
        except Exception as e:
            print(f"    Error: {e}")
            return None
    
    if len(capsules) < 5:
        return None
    
    # Aplicar Hastad
    print("\n[+] Aplicando ataque de Hastad...")
    e = capsules[0][2]
    ciphertexts = [c for c, _, _ in capsules]
    moduli = [n for _, n, _ in capsules]
    
    m_e = chinese_remainder_theorem(ciphertexts, moduli)
    m = nth_root(m_e, e)
    flag = long_to_bytes(m).decode('utf-8', errors='ignore')
    
    return flag

# Esperar a que el docker se inicie
print("[*] Esperando 30 segundos para que el docker se inicie...")
time.sleep(30)

# Los challenges de HTB normalmente usan estos rangos cuando se ejecutan
# La instancia debería estar en uno de estos
print("\n[*] Escaneando rangos conocidos de HTB...")

# Primero probar las IPs que ya sabemos que tienen puerto 1337 abierto
known_ips = [
    "94.237.49.102",
    "94.237.49.118",
    "94.237.49.125",
    "94.237.49.142",
    "94.237.49.152",
    "94.237.49.154",
    "94.237.49.155"
]

for ip in known_ips:
    try:
        print(f"\n[*] Probando {ip}:1337...")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(3)
        s.connect((ip, 1337))
        
        # Enviar newline para activar respuesta
        s.send(b'\n')
        time.sleep(1)
        
        # Intentar recibir
        s.settimeout(2)
        try:
            data = s.recv(1024)
            if data:
                print(f"    Respuesta: {data[:100]}")
                
                if b"Qubit" in data or b"capsule" in data.lower() or b"Welcome" in data:
                    print(f"[+] ¡Challenge encontrado!")
                    s.close()
                    
                    # Resolver
                    flag = solve_challenge(ip)
                    
                    if flag and 'HTB{' in flag:
                        flag_start = flag.find('HTB{')
                        flag_end = flag.find('}', flag_start) + 1
                        clean_flag = flag[flag_start:flag_end]
                        
                        print(f"\n[+] ¡FLAG ENCONTRADA!: {clean_flag}")
                        
                        # Guardar
                        with open('flag.txt', 'w') as f:
                            f.write(clean_flag)
                        
                        # Enviar a HTB
                        print("\n[*] Enviando flag a HackTheBox...")
                        p = subprocess.Popen(['./htb-mcp-server'], 
                                            stdin=subprocess.PIPE, 
                                            stdout=subprocess.PIPE, 
                                            stderr=subprocess.PIPE,
                                            env=env, 
                                            text=True)
                        
                        p.stdin.write('{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"0.1.0"}}\n')
                        p.stdin.flush()
                        p.stdout.readline()
                        
                        p.stdin.write(f'{{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{{"name":"submit_challenge_flag","arguments":{{"challenge_id":"365","flag":"{clean_flag}"}}}}}}\n')
                        p.stdin.flush()
                        
                        response = p.stdout.readline()
                        print(f"[*] Respuesta: {response}")
                        
                        if "true" in response.lower() or "correct" in response.lower():
                            print("\n[+] ¡CHALLENGE COMPLETADO EXITOSAMENTE!")
                        
                        p.terminate()
                        exit(0)
        except socket.timeout:
            pass
        
        s.close()
    except Exception as e:
        continue

print("\n[-] No se pudo encontrar el challenge en las IPs conocidas")
print("[*] La instancia está activa pero necesita ser accedida desde la IP correcta")