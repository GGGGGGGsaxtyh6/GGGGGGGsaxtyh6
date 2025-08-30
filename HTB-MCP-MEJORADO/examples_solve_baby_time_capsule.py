#!/usr/bin/env python3
"""
Baby Time Capsule - Solver
Vulnerabilidad: Hastad's Broadcast Attack
El servidor usa RSA con exponente pequeño (e=5) y genera múltiples cifrados del mismo mensaje.
"""

import socket
import json
from Cryptodome.Util.number import long_to_bytes
import gmpy2
from functools import reduce

def chinese_remainder_theorem(remainders, moduli):
    """
    Implementación del Teorema Chino del Resto
    """
    total = 0
    prod = reduce(lambda a, b: a * b, moduli)
    
    for r_i, n_i in zip(remainders, moduli):
        p = prod // n_i
        total += r_i * gmpy2.invert(p, n_i) * p
    
    return total % prod

def nth_root(num, n):
    """
    Calcula la raíz n-ésima de un número grande
    """
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

def collect_capsules(host, port, count=5):
    """
    Conecta al servidor y recolecta múltiples time capsules
    """
    capsules = []
    
    for i in range(count):
        print(f"[+] Recolectando cápsula {i+1}/{count}...")
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        
        # Recibir prompt inicial
        data = s.recv(4096)
        print(f"    Servidor: {data.decode().strip()}")
        
        # Enviar 'Y' para obtener una cápsula
        s.send(b'Y\n')
        
        # Recibir la cápsula
        response = s.recv(4096).decode().strip()
        print(f"    Respuesta recibida")
        
        # Parsear JSON
        capsule_data = json.loads(response)
        
        # Extraer valores
        c = int(capsule_data['time_capsule'], 16)
        n = int(capsule_data['pubkey'][0], 16)
        e = int(capsule_data['pubkey'][1], 16)
        
        print(f"    n = {n}")
        print(f"    e = {e}")
        print(f"    c = {c}")
        
        capsules.append((c, n, e))
        
        s.close()
    
    return capsules

def hastad_attack(capsules):
    """
    Implementa el ataque de Hastad para recuperar el mensaje
    """
    print("\n[+] Ejecutando ataque de Hastad...")
    
    # Verificar que todos tienen el mismo exponente
    e = capsules[0][2]
    for _, _, exp in capsules:
        if exp != e:
            print("[-] Error: Los exponentes no son iguales")
            return None
    
    print(f"[+] Exponente común: e = {e}")
    
    # Extraer cifrados y módulos
    ciphertexts = [c for c, _, _ in capsules]
    moduli = [n for _, n, _ in capsules]
    
    # Verificar que los módulos son coprimos
    print("[+] Verificando que los módulos son coprimos...")
    for i in range(len(moduli)):
        for j in range(i+1, len(moduli)):
            if gmpy2.gcd(moduli[i], moduli[j]) != 1:
                print(f"[-] Error: Los módulos {i} y {j} no son coprimos")
                return None
    
    print("[+] Todos los módulos son coprimos")
    
    # Aplicar CRT
    print("[+] Aplicando Teorema Chino del Resto...")
    m_e = chinese_remainder_theorem(ciphertexts, moduli)
    
    # Calcular la raíz e-ésima
    print(f"[+] Calculando raíz {e}-ésima...")
    m = nth_root(m_e, e)
    
    # Verificar que la raíz es exacta
    if m ** e == m_e:
        print("[+] Raíz exacta encontrada!")
    else:
        print("[!] La raíz no es exacta, pero intentando de todos modos...")
    
    # Convertir a bytes
    flag = long_to_bytes(m)
    
    return flag

def solve_local():
    """
    Resuelve el challenge localmente simulando el servidor
    """
    print("\n[*] Resolviendo localmente con servidor simulado...")
    
    # Primero vamos a crear un servidor local para probar
    from Cryptodome.Util.number import bytes_to_long, getPrime
    
    # Flag de prueba
    test_flag = b'HTB{test_flag_for_local_testing}'
    
    class LocalTimeCapsule:
        def __init__(self, msg):
            self.msg = msg
            self.bit_size = 1024
            self.e = 5
        
        def _get_new_pubkey(self):
            while True:
                p = getPrime(self.bit_size // 2)
                q = getPrime(self.bit_size // 2)
                n = p * q
                phi = (p - 1) * (q - 1)
                try:
                    pow(self.e, -1, phi)
                    break
                except ValueError:
                    pass
            return n, self.e
        
        def get_new_time_capsule(self):
            n, e = self._get_new_pubkey()
            m = bytes_to_long(self.msg)
            c = pow(m, e, n)
            return c, n, e
    
    # Generar múltiples cápsulas
    print("[+] Generando cápsulas de prueba...")
    tc = LocalTimeCapsule(test_flag)
    capsules = []
    
    for i in range(5):
        c, n, e = tc.get_new_time_capsule()
        capsules.append((c, n, e))
        print(f"    Cápsula {i+1} generada")
    
    # Aplicar el ataque
    recovered = hastad_attack(capsules)
    
    if recovered:
        print(f"\n[+] Flag recuperada: {recovered.decode()}")
        if recovered == test_flag:
            print("[+] ¡Prueba local exitosa! El exploit funciona correctamente.")
            return True
    else:
        print("[-] No se pudo recuperar la flag")
        return False

def main():
    print("=" * 60)
    print("Baby Time Capsule - Exploit")
    print("Hastad's Broadcast Attack para RSA con exponente pequeño")
    print("=" * 60)
    
    # Primero probar localmente
    if not solve_local():
        print("[-] El exploit local falló. Abortando.")
        return
    
    print("\n" + "=" * 60)
    print("[*] Intentando conectar al servidor remoto...")
    
    # Intentar diferentes puertos comunes
    possible_ports = [1337, 31337, 32000, 30000, 40000, 50000]
    host = "94.237.49.212"  # IP típica de HTB
    
    for port in possible_ports:
        print(f"\n[*] Probando {host}:{port}...")
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            s.connect((host, port))
            s.close()
            print(f"[+] Puerto {port} abierto!")
            
            # Recolectar cápsulas
            capsules = collect_capsules(host, port, 5)
            
            # Ejecutar el ataque
            flag = hastad_attack(capsules)
            
            if flag:
                print(f"\n[+] FLAG ENCONTRADA: {flag.decode()}")
                
                # Guardar la flag
                with open('flag.txt', 'w') as f:
                    f.write(flag.decode())
                print("[+] Flag guardada en flag.txt")
                
                return flag.decode()
            
        except (socket.timeout, ConnectionRefusedError):
            continue
        except Exception as e:
            print(f"[-] Error: {e}")
            continue
    
    print("\n[-] No se pudo conectar al servidor remoto")
    print("[*] El servidor podría no estar activo o necesitar una IP/puerto diferente")
    
    # Mostrar instrucciones para cuando tengamos la IP correcta
    print("\n[*] Cuando tengas la IP y puerto correctos, ejecuta:")
    print("    python3 solve_baby_time_capsule.py <IP> <PUERTO>")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) == 3:
        host = sys.argv[1]
        port = int(sys.argv[2])
        
        print(f"[*] Conectando a {host}:{port}...")
        
        try:
            # Recolectar cápsulas
            capsules = collect_capsules(host, port, 5)
            
            # Ejecutar el ataque
            flag = hastad_attack(capsules)
            
            if flag:
                print(f"\n[+] FLAG ENCONTRADA: {flag.decode()}")
                
                # Guardar la flag
                with open('flag.txt', 'w') as f:
                    f.write(flag.decode())
                print("[+] Flag guardada en flag.txt")
        except Exception as e:
            print(f"[-] Error: {e}")
    else:
        main()