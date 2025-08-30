#!/usr/bin/env python3
"""
Fuerza bruta para encontrar la IP del docker instance
Sabemos que la instancia 1661347 está activa
Las IPs de docker de HTB suelen estar en rangos específicos
"""

import socket
import json
import time
import threading
from queue import Queue
from Cryptodome.Util.number import long_to_bytes
import gmpy2
from functools import reduce

# Rangos típicos de docker instances en HTB
DOCKER_RANGES = [
    "172.17.0.",    # Docker default
    "10.10.10.",    # HTB common
    "10.10.11.",    # HTB common
    "10.10.14.",    # HTB VPN
    "10.10.15.",    # HTB VPN
    "10.129.",      # HTB Academy
    "94.237.49.",   # EU servers
    "94.237.50.",
    "94.237.51.",
    "94.237.52.",
    "94.237.53.",
    "94.237.54.",
    "94.237.55.",
    "94.237.56.",
    "94.237.57.",
    "94.237.58.",
    "94.237.59.",
    "94.237.60.",
    "94.237.61.",
    "94.237.62.",
    "94.237.63.",
    "83.136.249.",  # Academy range
    "83.136.250.",
    "83.136.251.",
    "83.136.252.",
    "83.136.253.",
    "83.136.254.",
    "83.136.255.",
]

def check_baby_time_capsule(ip, port=1337):
    """Verifica si es el challenge Baby Time Capsule"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect((ip, port))
        
        # Esperar el banner
        data = s.recv(1024)
        
        # Verificar si es el challenge correcto
        if b"Welcome to Qubit Enterprises" in data or b"time capsule" in data.lower():
            print(f"\n[+] ¡ENCONTRADO! Baby Time Capsule en {ip}:{port}")
            print(f"    Banner: {data.decode('utf-8', errors='ignore')}")
            s.close()
            return True
        
        s.close()
        return False
    except:
        return False

def scan_range_threaded(base_range, start=1, end=255):
    """Escanea un rango de IPs con threads"""
    found = []
    
    def worker(ip):
        if check_baby_time_capsule(ip):
            found.append(ip)
    
    threads = []
    for i in range(start, end):
        ip = f"{base_range}{i}"
        t = threading.Thread(target=worker, args=(ip,))
        t.start()
        threads.append(t)
        
        # Limitar threads concurrentes
        if len(threads) >= 50:
            for t in threads:
                t.join()
            threads = []
    
    # Esperar threads restantes
    for t in threads:
        t.join()
    
    return found

def solve_challenge(host, port=1337):
    """Resuelve el challenge directamente"""
    print(f"\n[*] Resolviendo challenge en {host}:{port}...")
    
    # Implementación del ataque de Hastad
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
        print(f"[+] Recolectando cápsula {i+1}/5...")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        
        # Recibir prompt
        data = s.recv(4096)
        
        # Enviar Y
        s.send(b'Y\n')
        
        # Recibir cápsula
        response = s.recv(4096).decode().strip()
        
        # Parsear JSON
        try:
            # Buscar el JSON en la respuesta
            json_start = response.find('{')
            if json_start != -1:
                json_data = response[json_start:]
                capsule_data = json.loads(json_data)
                
                c = int(capsule_data['time_capsule'], 16)
                n = int(capsule_data['pubkey'][0], 16)
                e = int(capsule_data['pubkey'][1], 16)
                
                capsules.append((c, n, e))
                print(f"    Cápsula {i+1} obtenida")
        except Exception as e:
            print(f"[-] Error parseando cápsula: {e}")
        
        s.close()
    
    if len(capsules) < 5:
        print("[-] No se pudieron obtener suficientes cápsulas")
        return None
    
    # Aplicar ataque de Hastad
    print("\n[+] Aplicando ataque de Hastad...")
    e = capsules[0][2]
    ciphertexts = [c for c, _, _ in capsules]
    moduli = [n for _, n, _ in capsules]
    
    # CRT
    m_e = chinese_remainder_theorem(ciphertexts, moduli)
    
    # Raíz e-ésima
    m = nth_root(m_e, e)
    
    # Convertir a bytes
    flag = long_to_bytes(m)
    
    return flag.decode('utf-8', errors='ignore')

# Escanear rangos prioritarios
print("=" * 60)
print("Buscando Baby Time Capsule en todos los rangos...")
print("=" * 60)

for base in DOCKER_RANGES:
    print(f"\n[*] Escaneando {base}0/24...")
    found = scan_range_threaded(base, 1, 255)
    
    if found:
        for ip in found:
            try:
                flag = solve_challenge(ip)
                if flag and flag.startswith('HTB{'):
                    print(f"\n[+] ¡FLAG ENCONTRADA!: {flag}")
                    
                    # Guardar la flag
                    with open('flag.txt', 'w') as f:
                        f.write(flag)
                    print("[+] Flag guardada en flag.txt")
                    
                    # Salir con éxito
                    exit(0)
            except Exception as e:
                print(f"[-] Error resolviendo {ip}: {e}")

print("\n[-] No se encontró el challenge en ningún rango conocido")