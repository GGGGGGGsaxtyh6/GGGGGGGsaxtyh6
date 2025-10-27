#!/usr/bin/env python3
import subprocess
import time
import sys
import signal
import socket
import struct

def signal_handler(sig, frame):
    print('\n[!] Deteniendo monitoreo...')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

print("[+] Monitoreando conexiones de red...")
print("[+] Presiona Ctrl+C para detener\n")

seen_connections = set()

while True:
    try:
        # Obtener conexiones TCP
        result = subprocess.run(['ss', '-tunapn'], capture_output=True, text=True)
        lines = result.stdout.split('\n')
        
        for line in lines:
            if 'ESTAB' in line or 'SYN-SENT' in line or 'TIME-WAIT' in line:
                parts = line.split()
                if len(parts) >= 5:
                    local = parts[3]
                    remote = parts[4]
                    
                    # Filtrar conexiones locales
                    if not remote.startswith('127.0.0.1') and not remote.startswith('::1'):
                        connection = f"{local} -> {remote}"
                        if connection not in seen_connections:
                            seen_connections.add(connection)
                            print(f"[NEW CONNECTION] {connection}")
                            
                            # Intentar resolver el hostname
                            try:
                                remote_ip = remote.split(':')[0]
                                if remote_ip:
                                    hostname = socket.gethostbyaddr(remote_ip)[0]
                                    print(f"  └─> Hostname: {hostname}")
                            except:
                                pass
        
        # También verificar conexiones UDP
        result = subprocess.run(['ss', '-unapn'], capture_output=True, text=True)
        lines = result.stdout.split('\n')
        
        for line in lines:
            if 'UNCONN' not in line and len(line) > 10:
                parts = line.split()
                if len(parts) >= 5:
                    local = parts[3]
                    remote = parts[4]
                    
                    if not remote.startswith('127.0.0.1') and not remote.startswith('*:*'):
                        connection = f"UDP: {local} -> {remote}"
                        if connection not in seen_connections:
                            seen_connections.add(connection)
                            print(f"[NEW UDP] {connection}")
        
        time.sleep(1)
        
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(1)