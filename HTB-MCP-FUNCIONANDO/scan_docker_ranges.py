#!/usr/bin/env python3
"""
Escanea rangos de docker típicos de HTB para encontrar el challenge
"""

import socket
import concurrent.futures
import sys
from Cryptodome.Util.number import long_to_bytes
import gmpy2
from functools import reduce
import json

# Rangos de docker más comunes en HTB
DOCKER_RANGES = [
    # Docker bridge networks
    ("172.17.0.", 1, 255),
    ("172.18.0.", 1, 255),
    ("172.19.0.", 1, 255),
    ("172.20.0.", 1, 255),
    
    # HTB docker ranges
    ("10.10.10.", 1, 255),
    ("10.10.11.", 1, 255),
    ("10.10.14.", 1, 255),
    ("10.10.15.", 1, 255),
    
    # Academy ranges
    ("10.129.0.", 1, 255),
    ("10.129.1.", 1, 255),
    ("10.129.2.", 1, 255),
    
    # Otros rangos comunes
    ("192.168.1.", 1, 255),
    ("192.168.0.", 1, 255),
]

def check_challenge(ip, port=1337, timeout=1):
    """Verifica si el servidor es Baby Time Capsule"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((ip, port))
        
        # Recibir datos iniciales
        data = s.recv(1024)
        s.close()
        
        # Verificar si es el challenge
        if b"Qubit" in data or b"capsule" in data.lower() or b"Welcome" in data:
            return True, data.decode('utf-8', errors='ignore')
        
        return False, None
    except:
        return False, None

def scan_range(base, start, end):
    """Escanea un rango de IPs"""
    found = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        futures = {}
        
        for i in range(start, end + 1):
            ip = f"{base}{i}"
            future = executor.submit(check_challenge, ip)
            futures[future] = ip
        
        for future in concurrent.futures.as_completed(futures):
            ip = futures[future]
            try:
                is_challenge, banner = future.result()
                if is_challenge:
                    print(f"\n[+] ¡ENCONTRADO! {ip}:1337")
                    print(f"    Banner: {banner[:100]}")
                    found.append((ip, banner))
            except:
                pass
    
    return found

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
    
    # Recolectar cápsulas
    capsules = []
    for i in range(5):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            s.connect((host, port))
            
            # Recibir prompt
            data = s.recv(4096)
            
            # Enviar Y
            s.send(b'Y\n')
            
            # Recibir cápsula
            response = s.recv(4096).decode('utf-8', errors='ignore')
            
            # Parsear JSON
            json_start = response.find('{')
            if json_start != -1:
                json_str = response[json_start:]
                capsule_data = json.loads(json_str)
                
                c = int(capsule_data['time_capsule'], 16)
                n = int(capsule_data['pubkey'][0], 16)
                e = int(capsule_data['pubkey'][1], 16)
                
                capsules.append((c, n, e))
                print(f"    Cápsula {i+1}/5 obtenida")
            
            s.close()
        except Exception as e:
            print(f"    Error: {e}")
    
    if len(capsules) < 5:
        return None
    
    # Aplicar Hastad
    print("[+] Aplicando ataque de Hastad...")
    e = capsules[0][2]
    ciphertexts = [c for c, _, _ in capsules]
    moduli = [n for _, n, _ in capsules]
    
    m_e = chinese_remainder_theorem(ciphertexts, moduli)
    m = nth_root(m_e, e)
    flag = long_to_bytes(m).decode('utf-8', errors='ignore')
    
    return flag

# Escanear todos los rangos
print("=" * 60)
print("Escaneando rangos de docker para Baby Time Capsule")
print("=" * 60)

all_found = []

for base, start, end in DOCKER_RANGES:
    print(f"\n[*] Escaneando {base}{start}-{end}...")
    found = scan_range(base, start, end)
    all_found.extend(found)
    
    # Si encontramos algo, intentar resolverlo
    for ip, banner in found:
        try:
            flag = solve_challenge(ip)
            if flag and 'HTB{' in flag:
                print(f"\n[+] ¡FLAG ENCONTRADA!: {flag}")
                
                # Guardar la flag
                with open('flag.txt', 'w') as f:
                    f.write(flag)
                print("[+] Flag guardada en flag.txt")
                
                # Salir con éxito
                sys.exit(0)
        except Exception as e:
            print(f"[-] Error resolviendo: {e}")

if not all_found:
    print("\n[-] No se encontró el challenge en ningún rango")
else:
    print(f"\n[*] Se encontraron {len(all_found)} servidores pero ninguno tenía la flag correcta")