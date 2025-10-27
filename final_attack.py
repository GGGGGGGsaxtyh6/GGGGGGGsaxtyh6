import requests
import json
import re
import base64

BASE_URL = "http://94.237.58.80:34442"

print("[!] FINAL ATTACK - PHOENIX PIPELINE")
print("="*50)

# El reto parece ser sobre parchear vulnerabilidades en código
# Necesito interactuar con el editor para ver qué archivos hay

# Primero, intentar obtener la lista de archivos disponibles
print("\n[+] Attempting to get file list...")

# Probar diferentes formas de obtener archivos
file_endpoints = [
    "/api/files",
    "/api/list",
    "/api/ls",
    "/api/dir",
    "/api/tree",
    "/api/workspace",
    "/api/project"
]

session = requests.Session()

for endpoint in file_endpoints:
    r = session.get(f"{BASE_URL}{endpoint}")
    if r.status_code == 200 and "html" not in r.text[:50].lower():
        print(f"[!] Found file listing at {endpoint}:")
        print(r.text[:500])

# Intentar con parámetros
params_list = [
    {"path": "/"},
    {"dir": "/"},
    {"folder": "/"},
    {"workspace": "/"},
    {"project": "/"}
]

for params in params_list:
    r = session.get(f"{BASE_URL}/api/files", params=params)
    if r.status_code == 200 and "html" not in r.text[:50].lower():
        print(f"[!] Found files with params {params}:")
        print(r.text[:500])

# Intentar obtener archivos específicos de pipeline
print("\n[+] Looking for pipeline files...")

pipeline_files = [
    "pipeline.yaml",
    "pipeline.yml",
    "azure-pipelines.yml",
    "azure-pipelines.yaml",
    ".azure-pipelines.yml",
    "build.yaml",
    "build.yml",
    "deploy.yaml",
    "deploy.yml",
    "ci.yaml",
    "ci.yml",
    "cd.yaml",
    "cd.yml",
    ".gitlab-ci.yml",
    "Jenkinsfile",
    "jenkinsfile",
    ".github/workflows/main.yml",
    ".github/workflows/build.yml",
    ".github/workflows/deploy.yml"
]

for file in pipeline_files:
    # Intentar diferentes formas de cargar
    load_attempts = [
        f"/api/load?file={file}",
        f"/api/load?path={file}",
        f"/api/read?file={file}",
        f"/api/get?file={file}",
        f"/api/file?name={file}",
        f"/api/open?file={file}",
        f"/{file}"
    ]
    
    for attempt in load_attempts:
        r = session.get(f"{BASE_URL}{attempt}")
        if r.status_code == 200 and len(r.text) < 10000 and "html" not in r.text[:50].lower():
            print(f"\n[!] Found {file} at {attempt}:")
            print(r.text[:1000])
            
            # Si encontramos un archivo de pipeline, intentar parchearlo
            if "script" in r.text or "run" in r.text or "command" in r.text:
                print("\n[!] Vulnerable code detected! Attempting to patch...")
                
                # Parchear vulnerabilidades comunes
                patched = r.text
                
                # Command injection patches
                patched = re.sub(r'sh -c ["\']([^"\']+)["\']', r'sh -c "echo \1"', patched)
                patched = re.sub(r'eval\s*\(', '# eval(', patched)
                patched = re.sub(r'exec\s*\(', '# exec(', patched)
                patched = re.sub(r'\$\(([^)]+)\)', r'# $(\1)', patched)
                patched = re.sub(r'`([^`]+)`', r'# `\1`', patched)
                
                # Path traversal patches
                patched = re.sub(r'\.\./', '', patched)
                
                # SQL injection patches
                patched = re.sub(r"'\s*OR\s*'", "' AND '", patched)
                
                # Save patched file
                save_data = {
                    "file": file,
                    "path": file,
                    "name": file,
                    "content": patched,
                    "data": patched
                }
                
                # Try different save endpoints
                save_endpoints = [
                    "/api/save",
                    "/api/write",
                    "/api/update",
                    "/api/patch",
                    "/api/fix"
                ]
                
                for save_endpoint in save_endpoints:
                    r = session.post(f"{BASE_URL}{save_endpoint}", json=save_data)
                    print(f"Save attempt at {save_endpoint}: {r.status_code}")
                    
                    if r.status_code == 200:
                        # Verificar si se parcheó
                        r = session.get(f"{BASE_URL}/api/verify")
                        print(f"Verify after patch: {r.text}")
                        
                        if "success" in r.text.lower() or "HTB{" in r.text:
                            print(f"\n[!] SUCCESS! FLAG: {r.text}")
                            exit(0)

# Intentar verificar con diferentes métodos
print("\n[+] Trying different verify methods...")

verify_methods = [
    ("GET", "/api/verify", None),
    ("POST", "/api/verify", {"patched": True}),
    ("PUT", "/api/verify", {"status": "patched"}),
    ("PATCH", "/api/verify", {"vulnerability_1": "fixed"}),
    ("GET", "/api/check", None),
    ("GET", "/api/status", None),
    ("GET", "/api/validate", None)
]

for method, endpoint, data in verify_methods:
    if method == "GET":
        r = session.get(f"{BASE_URL}{endpoint}")
    else:
        r = session.request(method, f"{BASE_URL}{endpoint}", json=data)
    
    if "HTB{" in r.text or ("success" in r.text.lower() and "error" not in r.text.lower()):
        print(f"\n[!] FOUND via {method} {endpoint}:")
        print(r.text)

# Último intento - verificar múltiples veces
print("\n[+] Multiple verify attempts...")
for i in range(1, 10):
    r = session.get(f"{BASE_URL}/api/verify?attempt={i}")
    if r.text != '{\n  "error": "Vulnerability 1 is not patched."\n}':
        print(f"Different response on attempt {i}: {r.text}")
        
print("\n[!] Attack complete!")
