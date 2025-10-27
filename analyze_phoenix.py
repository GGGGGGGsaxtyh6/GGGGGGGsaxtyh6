import requests
import json
import websocket
import time

BASE_URL = "http://94.237.58.80:34442"

print("[+] Phoenix Pipeline HTB Editor Analysis")
print("="*50)

# Encontré referencias a WebSocket y auto-save
# También veo rutas como /challenge/, /verify, etc.

# Probar endpoints encontrados en el JS
endpoints = [
    "/challenge/",
    "/api/files",
    "/api/execute", 
    "/api/run",
    "/api/compile",
    "/api/save",
    "/api/load",
    "/api/verify",
    "/socket.io/",
    "/ws",
    "/websocket"
]

print("\n[+] Testing endpoints...")
for endpoint in endpoints:
    try:
        r = requests.get(f"{BASE_URL}{endpoint}", timeout=3)
        if r.status_code != 404:
            print(f"[!] {endpoint} - Status: {r.status_code}")
            if len(r.text) < 500 and r.status_code != 200:
                print(f"    Response: {r.text[:200]}")
    except:
        pass

# Probar WebSocket
print("\n[+] Testing WebSocket connections...")
ws_urls = [
    "ws://94.237.58.80:34442/socket.io/?EIO=4&transport=websocket",
    "ws://94.237.58.80:34442/ws",
    "ws://94.237.58.80:34442/websocket"
]

for ws_url in ws_urls:
    try:
        print(f"[*] Trying: {ws_url}")
        ws = websocket.create_connection(ws_url, timeout=2)
        print(f"[!] Connected to {ws_url}")
        
        # Enviar mensaje de prueba
        test_msg = json.dumps({"type": "ping"})
        ws.send(test_msg)
        
        # Recibir respuesta
        result = ws.recv()
        print(f"    Received: {result[:100]}")
        
        ws.close()
    except Exception as e:
        print(f"    Failed: {str(e)[:50]}")

# Buscar archivos de configuración del editor
print("\n[+] Looking for editor configuration...")
config_endpoints = [
    "/api/config",
    "/api/settings",
    "/config.json",
    "/manifest.json",
    "/.env",
    "/api/workspace",
    "/api/projects"
]

for endpoint in config_endpoints:
    try:
        r = requests.get(f"{BASE_URL}{endpoint}", timeout=3)
        if r.status_code == 200 and len(r.text) < 2000:
            print(f"[!] Found {endpoint}:")
            if "application/json" in r.headers.get("Content-Type", ""):
                try:
                    data = r.json()
                    print(f"    {json.dumps(data, indent=2)[:500]}")
                except:
                    print(f"    {r.text[:200]}")
    except:
        pass

print("\n[+] Testing file operations...")
# Intentar operaciones de archivo
headers = {"Content-Type": "application/json"}

# Intentar guardar un archivo
save_data = {
    "fileName": "test.txt",
    "content": "test content",
    "path": "/"
}

r = requests.post(f"{BASE_URL}/api/save", json=save_data, headers=headers)
print(f"[*] Save file: {r.status_code}")
if r.status_code != 404:
    print(f"    Response: {r.text[:200]}")

# Intentar cargar un archivo
load_data = {"fileName": "flag.txt", "path": "/"}
r = requests.post(f"{BASE_URL}/api/load", json=load_data, headers=headers)
print(f"[*] Load file: {r.status_code}")
if r.status_code != 404:
    print(f"    Response: {r.text[:200]}")

# Intentar ejecutar código
execute_data = {
    "code": "print('test')",
    "language": "python"
}
r = requests.post(f"{BASE_URL}/api/execute", json=execute_data, headers=headers)
print(f"[*] Execute code: {r.status_code}")
if r.status_code != 404:
    print(f"    Response: {r.text[:200]}")

print("\n[+] Analysis complete!")
