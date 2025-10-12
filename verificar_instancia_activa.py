#!/usr/bin/env python3
"""
Verificar que la instancia esté funcionando correctamente
"""
import requests

TARGET = "http://94.237.49.23:45329"

print("[*] Verificando estado del servidor...")
print()

try:
    resp = requests.get(f"{TARGET}/", timeout=10)
    print(f"[+] Servidor responde: {resp.status_code}")
    print(f"[+] Longitud de respuesta: {len(resp.text)} bytes")
    
    if "login.php" in resp.text or resp.status_code == 302:
        print(f"[+] Servidor redirige a login (normal)")
    
    # Verificar que el formulario de registro funciona
    resp2 = requests.get(f"{TARGET}/register.php", timeout=10)
    if "Register" in resp2.text or "register" in resp2.text.lower():
        print(f"[+] Página de registro accesible")
    
    # Verificar communicate.php
    resp3 = requests.get(f"{TARGET}/communicate.php", timeout=10)
    if "mother" in resp3.text.lower():
        print(f"[+] Página communicate accesible")
        
    print()
    print("[*] El servidor parece estar funcionando correctamente")
    print("[*] PERO motherland.com no resuelve")
    print()
    print("[*] Posibles razones:")
    print("    1. El servidor fue reconfigurado sin /etc/hosts entry")
    print("    2. Hay otro método de resolver que no he encontrado")
    print("    3. El reto requiere acceso VPN o configuración especial")
    
except Exception as e:
    print(f"[-] Error: {e}")
