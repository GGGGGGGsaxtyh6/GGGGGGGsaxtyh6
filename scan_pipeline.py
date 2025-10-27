import requests
import json

BASE_URL = "http://94.237.58.80:34442"

# Endpoints comunes en editores y pipelines
endpoints = [
    "/api",
    "/api/v1",
    "/api/pipeline",
    "/api/build",
    "/api/deploy",
    "/.svn",
    "/.git",
    "/svn",
    "/repo",
    "/repository",
    "/pipeline",
    "/pipelines",
    "/build",
    "/builds",
    "/azure",
    "/azure-pipelines.yml",
    "/.azure",
    "/devops",
    "/ci",
    "/cd",
    "/jenkins",
    "/.jenkins",
    "/gitlab-ci.yml",
    "/.gitlab-ci.yml",
    "/config",
    "/config.json",
    "/package.json",
    "/webpack.config.js",
    "/api/files",
    "/api/execute",
    "/api/run",
    "/api/compile",
    "/api/save",
    "/api/load",
    "/api/projects",
    "/api/workspace",
    "/ws",
    "/websocket",
    "/socket.io",
    "/api/auth",
    "/api/login",
    "/api/register",
    "/api/user",
    "/api/users",
    "/api/admin",
    "/api/debug",
    "/api/logs",
    "/api/status",
    "/api/health",
    "/api/version",
    "/api/info",
    "/_debug",
    "/debug",
    "/test",
    "/tests",
    "/api/test",
    "/api/tests"
]

print("[+] Escaneando endpoints en HTB Editor...")
print(f"    Base URL: {BASE_URL}\n")

found = []

for endpoint in endpoints:
    try:
        r = requests.get(f"{BASE_URL}{endpoint}", timeout=3)
        if r.status_code != 404:
            print(f"[!] {endpoint} - Status: {r.status_code} - Size: {len(r.text)}")
            found.append(endpoint)
            
            # Si es JSON, mostrar parte del contenido
            if "application/json" in r.headers.get("Content-Type", ""):
                try:
                    data = r.json()
                    print(f"    JSON: {str(data)[:100]}...")
                except:
                    pass
        else:
            print(f"[-] {endpoint} - 404")
    except requests.exceptions.Timeout:
        print(f"[?] {endpoint} - Timeout")
    except Exception as e:
        print(f"[x] {endpoint} - Error: {str(e)[:50]}")

print(f"\n[+] Endpoints encontrados: {found}")

# Probar métodos HTTP en endpoints encontrados
print("\n[+] Probando diferentes métodos HTTP...")
for endpoint in found:
    for method in ["POST", "PUT", "DELETE", "PATCH", "OPTIONS"]:
        try:
            r = requests.request(method, f"{BASE_URL}{endpoint}", timeout=3)
            if r.status_code not in [404, 405]:
                print(f"[!] {method} {endpoint} - Status: {r.status_code}")
        except:
            pass

# Buscar archivos de configuración específicos
config_files = [
    "/assets/config.json",
    "/assets/app.config.js",
    "/config/default.json",
    "/config/production.json",
    "/.env",
    "/.env.local",
    "/.env.production",
    "/env.js",
    "/config.js",
    "/settings.json"
]

print("\n[+] Buscando archivos de configuración...")
for file in config_files:
    try:
        r = requests.get(f"{BASE_URL}{file}", timeout=3)
        if r.status_code == 200:
            print(f"[!] Encontrado: {file}")
            print(f"    Contenido: {r.text[:200]}...")
    except:
        pass
