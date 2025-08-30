#!/usr/bin/env python3
import socket
import time

def test_server(host, port):
    """Prueba la conexión y muestra lo que responde el servidor"""
    print(f"\nProbando {host}:{port}")
    print("-" * 40)
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect((host, port))
        
        print("[+] Conectado exitosamente")
        
        # Esperar y recibir datos
        print("[*] Esperando respuesta del servidor...")
        time.sleep(1)
        
        # Intentar recibir datos sin enviar nada primero
        s.settimeout(3)
        try:
            data = s.recv(4096)
            if data:
                print(f"[+] Banner recibido:\n{data.decode('utf-8', errors='ignore')}")
                
                # Si recibimos algo, intentar enviar Y
                if b"time capsule" in data.lower() or b"qubit" in data.lower():
                    print("\n[+] ¡Parece ser el challenge correcto!")
                    print("[*] Enviando 'Y'...")
                    s.send(b'Y\n')
                    
                    # Recibir respuesta
                    response = s.recv(4096)
                    print(f"[+] Respuesta:\n{response.decode('utf-8', errors='ignore')}")
            else:
                print("[-] No se recibió banner")
                
                # Intentar enviar algo de todos modos
                print("[*] Enviando 'Y' de todos modos...")
                s.send(b'Y\n')
                response = s.recv(4096)
                if response:
                    print(f"[+] Respuesta:\n{response.decode('utf-8', errors='ignore')}")
                
        except socket.timeout:
            print("[-] Timeout esperando banner")
            
            # Intentar enviar algo
            print("[*] Intentando enviar datos...")
            s.send(b'\n')
            time.sleep(1)
            try:
                data = s.recv(4096)
                if data:
                    print(f"[+] Respuesta después de enviar newline:\n{data.decode('utf-8', errors='ignore')}")
            except:
                pass
        
        s.close()
        
    except Exception as e:
        print(f"[-] Error: {e}")

# Probar todas las IPs encontradas
ips = [
    "94.237.49.102",
    "94.237.49.118",
    "94.237.49.125",
    "94.237.49.154",
    "94.237.49.152",
    "94.237.49.142",
    "94.237.49.155"
]

print("=" * 50)
print("Probando servidores encontrados")
print("=" * 50)

for ip in ips:
    test_server(ip, 1337)
    print()