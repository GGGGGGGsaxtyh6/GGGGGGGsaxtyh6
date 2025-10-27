#!/usr/bin/env python3
"""
Escanea rangos de IP típicos de HTB para encontrar el challenge Baby Time Capsule
El challenge escucha en el puerto 1337
"""

import socket
import threading
import time
from queue import Queue

# Rangos de IP típicos de HTB
HTB_RANGES = [
    "94.237.49.",   # Rango EU típico
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
    "178.62.",      # Otro rango común
    "178.128.",
    "167.99.",
    "206.189.",
    "83.136.249.",  # Rango Academy
    "83.136.250.",
    "83.136.251.",
    "83.136.252.",
    "83.136.253.",
    "83.136.254.",
    "83.136.255.",
]

found_servers = []
queue = Queue()

def check_port(ip, port=1337):
    """Verifica si el puerto está abierto y es el challenge correcto"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        result = s.connect_ex((ip, port))
        
        if result == 0:
            # Puerto abierto, verificar si es el challenge correcto
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(3)
                s.connect((ip, port))
                
                # Recibir el banner
                data = s.recv(1024)
                s.close()
                
                # Verificar si es el challenge Baby Time Capsule
                if b"time capsule" in data.lower() or b"qubit" in data.lower():
                    return True, data.decode('utf-8', errors='ignore')
            except:
                pass
        
        s.close()
        return False, None
    except:
        return False, None

def worker():
    """Worker thread para escanear IPs"""
    while True:
        ip = queue.get()
        if ip is None:
            break
        
        is_challenge, banner = check_port(ip)
        if is_challenge:
            print(f"\n[+] ¡ENCONTRADO! {ip}:1337")
            print(f"    Banner: {banner[:100]}")
            found_servers.append((ip, banner))
        else:
            # Solo verificar si el puerto está abierto
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.5)
                if s.connect_ex((ip, 1337)) == 0:
                    print(f"[!] Puerto 1337 abierto en {ip} (verificar manualmente)")
                s.close()
            except:
                pass
        
        queue.task_done()

def scan_range(base_range, start=1, end=255):
    """Escanea un rango de IPs"""
    for i in range(start, end):
        ip = f"{base_range}{i}"
        queue.put(ip)

def main():
    print("=" * 60)
    print("Escáner de rangos HTB - Baby Time Capsule")
    print("Buscando servidor en puerto 1337...")
    print("=" * 60)
    
    # Crear threads
    threads = []
    num_threads = 50
    
    for i in range(num_threads):
        t = threading.Thread(target=worker)
        t.daemon = True
        t.start()
        threads.append(t)
    
    # Escanear rangos más probables primero
    print("\n[*] Escaneando rangos prioritarios...")
    priority_ranges = [
        "94.237.49.",
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
    ]
    
    for base in priority_ranges:
        print(f"[*] Escaneando {base}0/24...")
        scan_range(base)
    
    # Esperar a que termine
    queue.join()
    
    # Detener workers
    for i in range(num_threads):
        queue.put(None)
    
    for t in threads:
        t.join()
    
    print("\n" + "=" * 60)
    if found_servers:
        print("[+] Servidores encontrados:")
        for ip, banner in found_servers:
            print(f"\n  IP: {ip}")
            print(f"  Banner: {banner[:200]}")
            print(f"\n  Ejecuta: python3 solve_baby_time_capsule.py {ip} 1337")
    else:
        print("[-] No se encontraron servidores del challenge")
        print("\n[*] Es posible que:")
        print("  1. La instancia no esté activa")
        print("  2. Esté en un rango de IP diferente")
        print("  3. Use un puerto diferente")

if __name__ == "__main__":
    main()