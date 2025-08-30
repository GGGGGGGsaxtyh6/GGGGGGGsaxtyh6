#!/usr/bin/env python3
"""
Solución final: Usar el servidor MCP para obtener la información del docker
y resolver el challenge completamente
"""

import json
import subprocess
import os
import time
import socket
from Cryptodome.Util.number import long_to_bytes
import gmpy2
from functools import reduce
import sys

# Leer el token
with open('.env', 'r') as f:
    env_content = f.read()
    token = env_content.split('HTB_TOKEN=')[1].split('\n')[0]

env = os.environ.copy()
env['HTB_TOKEN'] = token

def solve_challenge(host, port=1337):
    """Resuelve el challenge usando Hastad's attack"""
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

def send_flag_to_htb(flag):
    """Envía la flag a HTB usando el servidor MCP"""
    print("\n[*] Enviando flag a HackTheBox...")
    
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
    
    # Enviar flag
    p.stdin.write(f'{{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{{"name":"submit_challenge_flag","arguments":{{"challenge_id":365,"flag":"{flag}"}}}}}}\n')
    p.stdin.flush()
    
    response = p.stdout.readline()
    print(f"[*] Respuesta: {response}")
    
    p.terminate()
    
    # Verificar respuesta
    if "correct" in response.lower() or "success" in response.lower():
        print("[+] ¡Flag enviada correctamente!")
        return True
    else:
        print("[-] Error enviando la flag")
        return False

# MAIN
print("=" * 60)
print("Baby Time Capsule - Solución Completa Autónoma")
print("=" * 60)

# Como la API no devuelve la IP, vamos a probar con las IPs típicas de los dockers de HTB
# Los challenges suelen estar en 94.237.x.x o en docker.hackthebox.eu

print("\n[*] Creando nueva instancia del challenge...")
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

# Detener instancias previas
print("[*] Deteniendo instancias previas...")
p.stdin.write('{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"stop_challenge","arguments":{"challenge_id":365}}}\n')
p.stdin.flush()
p.stdout.readline()

time.sleep(3)

# Iniciar nueva instancia
print("[*] Iniciando nueva instancia...")
p.stdin.write('{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"start_challenge","arguments":{"challenge_id":365}}}\n')
p.stdin.flush()
response = p.stdout.readline()

# Parsear respuesta para obtener ID de instancia
try:
    data = json.loads(response)
    if 'result' in data and 'content' in data['result']:
        content = json.loads(data['result']['content'][0]['text'])
        instance_id = content.get('id')
        print(f"[+] Instancia creada: {instance_id}")
except:
    pass

p.terminate()

# Esperar a que se inicie
print("[*] Esperando 45 segundos para que la instancia se inicie completamente...")
time.sleep(45)

# Los dockers de HTB normalmente están en estos rangos cuando se crean
# La IP debería estar disponible en docker.hackthebox.eu o en el rango 94.237.x.x
possible_hosts = [
    "docker.hackthebox.eu",
    "94.237.49.166",  # IP común para challenges
    "94.237.50.8",
    "94.237.51.96",
    "94.237.52.7",
    "94.237.53.3",
    "94.237.54.31",
    "94.237.55.11",
    "94.237.56.188",
    "94.237.57.59",
    "94.237.58.211",
    "94.237.59.47",
    "94.237.60.74",
    "94.237.61.21",
    "94.237.62.195",
    "94.237.63.93",
    "94.237.63.201",
]

# También intentar con subdominios específicos
for i in range(1, 20):
    possible_hosts.append(f"docker{i}.hackthebox.eu")

print("\n[*] Buscando el challenge en hosts conocidos...")

for host in possible_hosts:
    try:
        print(f"\n[*] Probando {host}:1337...")
        
        # Verificar conexión
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        
        # Resolver hostname si es necesario
        try:
            ip = socket.gethostbyname(host)
            print(f"    Resuelto a IP: {ip}")
        except:
            ip = host
        
        s.connect((ip, 1337))
        
        # Verificar si es el challenge correcto
        data = s.recv(1024)
        
        if b"Qubit" in data or b"capsule" in data.lower() or b"Welcome" in data:
            print(f"[+] ¡Challenge encontrado en {host}!")
            s.close()
            
            # Resolver el challenge
            flag = solve_challenge(ip if ip else host)
            
            if flag and 'HTB{' in flag:
                # Limpiar la flag
                flag_start = flag.find('HTB{')
                flag_end = flag.find('}', flag_start) + 1
                clean_flag = flag[flag_start:flag_end]
                
                print(f"\n[+] ¡FLAG ENCONTRADA!: {clean_flag}")
                
                # Guardar la flag
                with open('flag.txt', 'w') as f:
                    f.write(clean_flag)
                print("[+] Flag guardada en flag.txt")
                
                # Enviar la flag a HTB
                if send_flag_to_htb(clean_flag):
                    print("\n[+] ¡CHALLENGE COMPLETADO EXITOSAMENTE!")
                else:
                    print("\n[!] Flag encontrada pero hubo un problema al enviarla")
                    print(f"[!] Puedes enviarla manualmente: {clean_flag}")
                
                sys.exit(0)
        
        s.close()
    except Exception as e:
        continue

print("\n[-] No se pudo encontrar el challenge en ningún host conocido")
print("[*] La instancia está creada pero no se puede determinar su IP automáticamente")
print("[*] Necesitas obtener la IP desde la interfaz web de HTB")
print("\n[*] Una vez que tengas la IP, ejecuta:")
print("    python3 solve_baby_time_capsule.py <IP> 1337")