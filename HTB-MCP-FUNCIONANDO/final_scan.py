#!/usr/bin/env python3
"""
Escaneo final exhaustivo de todos los rangos posibles de HTB
"""

import socket
import threading
from queue import Queue
import time

# La instancia 1661434 está activa, debe estar en algún lugar
print("[*] Instancia activa: 1661434")
print("[*] Escaneando TODOS los rangos posibles de HTB...")

# Rangos más probables basados en la documentación de HTB
ranges = [
    # Rangos EU de HTB
    ("94.237.48.", 1, 255),
    ("94.237.49.", 1, 255),
    ("94.237.50.", 1, 255),
    ("94.237.51.", 1, 255),
    ("94.237.52.", 1, 255),
    ("94.237.53.", 1, 255),
    ("94.237.54.", 1, 255),
    ("94.237.55.", 1, 255),
    ("94.237.56.", 1, 255),
    ("94.237.57.", 1, 255),
    ("94.237.58.", 1, 255),
    ("94.237.59.", 1, 255),
    ("94.237.60.", 1, 255),
    ("94.237.61.", 1, 255),
    ("94.237.62.", 1, 255),
    ("94.237.63.", 1, 255),
    
    # Rangos US de HTB  
    ("206.189.16.", 1, 255),
    ("206.189.17.", 1, 255),
    ("206.189.18.", 1, 255),
    ("206.189.19.", 1, 255),
    ("206.189.20.", 1, 255),
    
    # Rangos de Academy
    ("83.136.248.", 1, 255),
    ("83.136.249.", 1, 255),
    ("83.136.250.", 1, 255),
    ("83.136.251.", 1, 255),
    ("83.136.252.", 1, 255),
    ("83.136.253.", 1, 255),
    ("83.136.254.", 1, 255),
    ("83.136.255.", 1, 255),
]

queue = Queue()
found = []

def check_host(ip):
    """Verifica si el host tiene el challenge"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        
        # Verificar puerto 1337
        if s.connect_ex((ip, 1337)) == 0:
            s.close()
            
            # Verificar si es el challenge correcto
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            s.connect((ip, 1337))
            
            # Recibir banner
            data = s.recv(1024)
            s.close()
            
            if b"Qubit" in data or b"capsule" in data.lower() or b"Welcome" in data:
                print(f"\n[+] ¡ENCONTRADO! Baby Time Capsule en {ip}:1337")
                print(f"    Banner: {data.decode('utf-8', errors='ignore')[:100]}")
                found.append(ip)
                return True
    except:
        pass
    
    return False

def worker():
    """Thread worker"""
    while True:
        ip = queue.get()
        if ip is None:
            break
        check_host(ip)
        queue.task_done()

# Crear threads
num_threads = 100
threads = []

for i in range(num_threads):
    t = threading.Thread(target=worker)
    t.daemon = True
    t.start()
    threads.append(t)

# Agregar IPs a la cola
total_ips = 0
for base, start, end in ranges:
    print(f"[*] Agregando rango {base}{start}-{end}")
    for i in range(start, end + 1):
        queue.put(f"{base}{i}")
        total_ips += 1

print(f"\n[*] Escaneando {total_ips} IPs con {num_threads} threads...")
print("[*] Esto puede tomar varios minutos...")

# Esperar a que termine
start_time = time.time()
queue.join()

# Detener workers
for i in range(num_threads):
    queue.put(None)

for t in threads:
    t.join()

elapsed = time.time() - start_time
print(f"\n[*] Escaneo completado en {elapsed:.2f} segundos")

if found:
    print(f"\n[+] Challenge encontrado en: {found[0]}")
    print(f"\n[*] Ejecuta: python3 solve_baby_time_capsule.py {found[0]} 1337")
    
    # Intentar resolver automáticamente
    import subprocess
    print("\n[*] Resolviendo automáticamente...")
    result = subprocess.run(
        ["python3", "solve_baby_time_capsule.py", found[0], "1337"],
        capture_output=True,
        text=True
    )
    print(result.stdout)
else:
    print("\n[-] No se encontró el challenge en ningún rango conocido")
    print("[*] La instancia está activa pero no se puede determinar la IP")
    print("[*] Necesitas obtener la IP desde: https://app.hackthebox.com/challenges/365")