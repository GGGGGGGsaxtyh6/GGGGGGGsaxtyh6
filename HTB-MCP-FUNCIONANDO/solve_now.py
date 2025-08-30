#!/usr/bin/env python3
import requests
import json
import socket
from Cryptodome.Util.number import long_to_bytes
import gmpy2
from functools import reduce
import subprocess
import os

# Leer el token
with open('.env', 'r') as f:
    env_content = f.read()
    token = env_content.split('HTB_TOKEN=')[1].split('\n')[0]

print("[*] Obteniendo información del challenge Baby Time Capsule...")

# Obtener información del challenge
headers = {"Authorization": f"Bearer {token}"}
r = requests.get(f"https://labs.hackthebox.com/api/v4/challenge/info/365", headers=headers)

if r.status_code == 200:
    data = r.json()
    if 'challenge' in data:
        challenge = data['challenge']
        docker_ip = challenge.get('docker_ip')
        docker_ports = challenge.get('docker_ports', [])
        
        print(f"[+] Challenge info:")
        print(f"    Nombre: {challenge.get('name')}")
        print(f"    Docker IP: {docker_ip}")
        print(f"    Docker Ports: {docker_ports}")
        
        if docker_ip:
            # El puerto debería ser 1337 o el primero en docker_ports
            port = docker_ports[0] if docker_ports else 1337
            
            print(f"\n[*] Conectando a {docker_ip}:{port}...")
            
            # Resolver el challenge
            def solve_challenge(host, port):
                print(f"\n[*] Resolviendo challenge...")
                
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
                            print(f"    ✓ Cápsula obtenida (e={e})")
                        
                        s.close()
                    except Exception as e:
                        print(f"    Error: {e}")
                        return None
                
                if len(capsules) < 5:
                    print("[-] No se pudieron obtener suficientes cápsulas")
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
            
            # Resolver
            flag = solve_challenge(docker_ip, port)
            
            if flag and 'HTB{' in flag:
                # Extraer la flag limpia
                flag_start = flag.find('HTB{')
                flag_end = flag.find('}', flag_start) + 1
                clean_flag = flag[flag_start:flag_end]
                
                print(f"\n[+] ¡FLAG ENCONTRADA!: {clean_flag}")
                
                # Guardar la flag
                with open('flag.txt', 'w') as f:
                    f.write(clean_flag)
                print("[+] Flag guardada en flag.txt")
                
                # Enviar la flag a HTB
                print("\n[*] Enviando flag a HackTheBox...")
                env = os.environ.copy()
                env['HTB_TOKEN'] = token
                
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
                print(f"[*] Respuesta: {response}")
                
                if "correct" in response.lower() or "success" in response.lower() or "true" in response:
                    print("\n[+] ¡FLAG CORRECTA! Challenge completado exitosamente.")
                else:
                    print("\n[!] Respuesta de HTB - verificar manualmente si la flag fue aceptada")
                
                p.terminate()
            else:
                print(f"[-] No se pudo obtener la flag. Respuesta: {flag}")
        else:
            print("[-] No hay IP de docker disponible. El challenge podría no estar activo.")
else:
    print(f"[-] Error obteniendo información del challenge: {r.status_code}")
    print(r.text)