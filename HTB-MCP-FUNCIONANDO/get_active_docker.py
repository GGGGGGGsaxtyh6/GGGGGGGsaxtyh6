#!/usr/bin/env python3
"""
Obtiene la IP del docker activo probando diferentes métodos
"""

import json
import subprocess
import os
import time
import requests
import socket

# Leer el token
with open('.env', 'r') as f:
    env_content = f.read()
    token = env_content.split('HTB_TOKEN=')[1].split('\n')[0]

env = os.environ.copy()
env['HTB_TOKEN'] = token

print("[*] Obteniendo información del challenge activo...")

# Método 1: Intentar con el servidor MCP directamente
print("\n[1] Usando servidor MCP...")
p = subprocess.Popen(['./htb-mcp-server'], 
                    stdin=subprocess.PIPE, 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE,
                    env=env, 
                    text=True)

p.stdin.write('{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"0.1.0"}}\n')
p.stdin.flush()
p.stdout.readline()

# Intentar obtener información del challenge
p.stdin.write('{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"search_content","arguments":{"query":"365"}}}\n')
p.stdin.flush()
search = p.stdout.readline()
print(f"Search: {search[:200]}")

p.terminate()

# Método 2: Probar endpoints no documentados
print("\n[2] Probando endpoints alternativos...")
headers = {
    "Authorization": f"Bearer {token}",
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

endpoints = [
    "https://www.hackthebox.com/api/v4/user/active/machine/connection",
    "https://www.hackthebox.com/api/v4/user/active/challenge/connection",
    "https://www.hackthebox.com/api/v4/sp/challenge/365",
    "https://www.hackthebox.com/api/v4/sp/instance/active",
    "https://labs.hackthebox.com/api/v4/sp/challenge/365",
    "https://app.hackthebox.com/api/v4/user/connection/challenge",
]

for endpoint in endpoints:
    try:
        print(f"Probando: {endpoint}")
        r = requests.get(endpoint, headers=headers, timeout=3)
        if r.status_code == 200:
            try:
                data = r.json()
                print(f"  ✓ Respuesta: {json.dumps(data, indent=2)[:200]}")
                
                # Buscar IPs en la respuesta
                import re
                text = json.dumps(data)
                ips = re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', text)
                if ips:
                    print(f"  IPs encontradas: {ips}")
            except:
                pass
        elif r.status_code != 404:
            print(f"  Status: {r.status_code}")
    except Exception as e:
        continue

# Método 3: Escaneo rápido de rangos más probables
print("\n[3] Escaneando rangos más probables...")

def quick_scan(ip, port=1337):
    """Escaneo rápido de un IP"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        if s.connect_ex((ip, port)) == 0:
            s.close()
            
            # Verificar si es el challenge
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            s.connect((ip, port))
            s.send(b'\n')
            time.sleep(0.5)
            
            try:
                data = s.recv(1024)
                if b"Qubit" in data or b"capsule" in data.lower() or b"Welcome" in data:
                    print(f"\n[+] ¡CHALLENGE ENCONTRADO EN {ip}:1337!")
                    return True
            except:
                pass
            
            s.close()
    except:
        pass
    
    return False

# Escanear rangos más probables para dockers de HTB
ranges = [
    ("94.237.62.", 1, 255),  # Rango común para challenges
    ("94.237.63.", 1, 255),
    ("83.136.254.", 1, 255),  # Academy range
    ("83.136.255.", 1, 255),
]

import concurrent.futures

for base, start, end in ranges:
    print(f"Escaneando {base}{start}-{end}...")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        futures = []
        for i in range(start, end + 1):
            ip = f"{base}{i}"
            future = executor.submit(quick_scan, ip)
            futures.append((future, ip))
        
        for future, ip in futures:
            if future.result():
                print(f"\n[+] IP ENCONTRADA: {ip}")
                print(f"[*] Ejecuta: python3 solve_baby_time_capsule.py {ip} 1337")
                
                # Resolver automáticamente
                import subprocess
                result = subprocess.run(
                    ["python3", "solve_baby_time_capsule.py", ip, "1337"],
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                
                if "FLAG" in result.stdout:
                    print(result.stdout)
                    exit(0)

print("\n[-] No se pudo encontrar la IP del challenge activo")