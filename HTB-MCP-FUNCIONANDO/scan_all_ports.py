#!/usr/bin/env python3
"""
Escanea todos los puertos en las IPs conocidas para encontrar el challenge
Ya que podría estar en un puerto diferente a 1337
"""

import socket
import concurrent.futures

# IPs que sabemos que tienen servicios activos
known_ips = [
    "94.237.49.102",
    "94.237.49.118",
    "94.237.49.125",
    "94.237.49.154",
    "94.237.49.152",
    "94.237.49.142",
    "94.237.49.155",
]

# Puertos comunes para challenges de HTB
common_ports = [
    1337, 31337, 8080, 8000, 9000, 9001, 
    30000, 30001, 30002, 31000, 31001,
    32000, 32001, 32002, 33000, 33001,
    40000, 40001, 50000, 50001, 60000,
    # Puertos altos aleatorios que HTB suele usar
    32768, 32769, 32770, 32771, 32772,
    32773, 32774, 32775, 32776, 32777,
]

def check_port(ip, port, timeout=1):
    """Verifica si un puerto está abierto y qué responde"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        result = s.connect_ex((ip, port))
        
        if result == 0:
            # Puerto abierto, intentar recibir banner
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(2)
                s.connect((ip, port))
                
                # Recibir datos
                data = s.recv(1024)
                s.close()
                
                # Verificar si parece ser el challenge
                if data:
                    decoded = data.decode('utf-8', errors='ignore')
                    if "Qubit" in decoded or "capsule" in decoded.lower() or "Welcome" in decoded:
                        return True, port, decoded
                    
                return False, port, None
            except:
                return False, port, None
        
        return False, port, None
    except:
        return False, port, None

print("=" * 60)
print("Escaneando puertos en IPs conocidas")
print("=" * 60)

for ip in known_ips:
    print(f"\n[*] Escaneando {ip}...")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        futures = []
        
        # Escanear puertos comunes
        for port in common_ports:
            future = executor.submit(check_port, ip, port)
            futures.append(future)
        
        # También escanear rango de puertos altos
        for port in range(30000, 33000, 100):
            future = executor.submit(check_port, ip, port)
            futures.append(future)
        
        for future in concurrent.futures.as_completed(futures):
            try:
                is_challenge, port, banner = future.result()
                if is_challenge:
                    print(f"\n[+] ¡CHALLENGE ENCONTRADO!")
                    print(f"    IP: {ip}")
                    print(f"    Puerto: {port}")
                    print(f"    Banner: {banner[:100]}")
                    print(f"\n[*] Ejecuta: python3 solve_baby_time_capsule.py {ip} {port}")
                    
                    # Intentar resolverlo directamente
                    print("\n[*] Intentando resolver automáticamente...")
                    import subprocess
                    result = subprocess.run(
                        ["python3", "solve_baby_time_capsule.py", ip, str(port)],
                        capture_output=True,
                        text=True,
                        timeout=30
                    )
                    
                    if "FLAG" in result.stdout:
                        print(result.stdout)
                        exit(0)
            except:
                pass

print("\n[-] No se encontró el challenge en ningún puerto conocido")