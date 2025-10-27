#!/usr/bin/env python3
import json
import subprocess
import os
import time
import socket
from Cryptodome.Util.number import long_to_bytes
import gmpy2
from functools import reduce

# Leer el token
with open('.env', 'r') as f:
    env_content = f.read()
    token = env_content.split('HTB_TOKEN=')[1].split('\n')[0]

env = os.environ.copy()
env['HTB_TOKEN'] = token

print("[*] Obteniendo IP del challenge mediante MCP...")

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

# Obtener IP de la máquina/challenge activo
print("[*] Obteniendo IP del challenge activo...")
p.stdin.write('{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"get_machine_ip","arguments":{}}}\n')
p.stdin.flush()
response = p.stdout.readline()
print(f"Respuesta get_machine_ip: {response}")

# Si no funciona, intentar con start_challenge para obtener info
p.stdin.write('{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"start_challenge","arguments":{"challenge_id":365}}}\n')
p.stdin.flush()
start_response = p.stdout.readline()
print(f"Respuesta start_challenge: {start_response}")

# Parsear para obtener información
try:
    data = json.loads(start_response)
    if 'result' in data and 'content' in data['result']:
        content = data['result']['content'][0]['text']
        instance_info = json.loads(content)
        print(f"\nInstancia: {instance_info}")
        
        # La IP debería estar en la respuesta o necesitamos obtenerla de otra forma
        # Intentar obtener más información
        instance_id = instance_info.get('id')
        
        # Esperar un poco para que se inicie
        print(f"[*] Instancia {instance_id} creada, esperando...")
        time.sleep(10)
        
except Exception as e:
    print(f"Error: {e}")

p.terminate()

# La IP debe estar en algún lugar de la respuesta del MCP
# Voy a intentar con la IP que el MCP debería devolver
print("\n[*] Buscando la IP en la respuesta del challenge...")

# Intentar conectar directamente a localhost ya que estamos en el mismo servidor
ips_to_try = [
    "127.0.0.1",
    "localhost",
    "172.17.0.2",  # Docker default
    "172.17.0.3",
    "172.17.0.4",
]

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
            s.settimeout(5)
            s.connect((host, port))
            
            # Recibir prompt
            data = s.recv(4096)
            print(f"    Recibido: {data.decode('utf-8', errors='ignore')[:50]}")
            
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

# Probar IPs locales primero
for ip in ips_to_try:
    try:
        print(f"\n[*] Probando {ip}:1337...")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        s.connect((ip, 1337))
        
        data = s.recv(1024)
        if b"Qubit" in data or b"capsule" in data.lower():
            print(f"[+] ¡Challenge encontrado en {ip}!")
            s.close()
            
            flag = solve_challenge(ip)
            if flag and 'HTB{' in flag:
                flag_start = flag.find('HTB{')
                flag_end = flag.find('}', flag_start) + 1
                clean_flag = flag[flag_start:flag_end]
                
                print(f"\n[+] ¡FLAG ENCONTRADA!: {clean_flag}")
                
                # Enviar la flag
                print("\n[*] Enviando flag a HTB...")
                p = subprocess.Popen(['./htb-mcp-server'], 
                                    stdin=subprocess.PIPE, 
                                    stdout=subprocess.PIPE, 
                                    stderr=subprocess.PIPE,
                                    env=env, 
                                    text=True)
                
                p.stdin.write('{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"0.1.0"}}\n')
                p.stdin.flush()
                p.stdout.readline()
                
                p.stdin.write(f'{{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{{"name":"submit_challenge_flag","arguments":{{"challenge_id":365,"flag":"{clean_flag}"}}}}}}\n')
                p.stdin.flush()
                
                response = p.stdout.readline()
                print(f"Respuesta: {response}")
                
                p.terminate()
                exit(0)
        
        s.close()
    except:
        continue