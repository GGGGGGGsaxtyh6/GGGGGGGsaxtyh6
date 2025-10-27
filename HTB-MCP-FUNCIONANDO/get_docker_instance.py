#!/usr/bin/env python3
import requests
import json
import time

# Leer el token
with open('.env', 'r') as f:
    env_content = f.read()
    token = env_content.split('HTB_TOKEN=')[1].split('\n')[0]

challenge_id = 365
headers = {
    "Authorization": f"Bearer {token}",
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

print("Obteniendo información del docker del challenge...")

# Intentar diferentes endpoints
endpoints = [
    f"https://www.hackthebox.com/api/v4/challenge/active",
    f"https://app.hackthebox.com/api/v4/challenge/active",
    f"https://www.hackthebox.com/api/v4/challenge/{challenge_id}/instance",
    f"https://app.hackthebox.com/api/v4/challenge/{challenge_id}/instance",
    f"https://www.hackthebox.com/api/v4/challenge/instance/{challenge_id}",
    f"https://app.hackthebox.com/api/v4/challenge/instance/{challenge_id}",
]

for endpoint in endpoints:
    print(f"\nProbando: {endpoint}")
    try:
        r = requests.get(endpoint, headers=headers, timeout=5)
        print(f"Status: {r.status_code}")
        if r.status_code == 200:
            data = r.json()
            print(f"Respuesta: {json.dumps(data, indent=2)}")
            break
        elif r.status_code != 404:
            print(f"Respuesta: {r.text[:500]}")
    except Exception as e:
        print(f"Error: {e}")

# Intentar obtener la instancia específica que creamos
print("\n\nObteniendo instancia específica 1661326...")
instance_id = 1661326
instance_endpoints = [
    f"https://www.hackthebox.com/api/v4/challenge/instance/{instance_id}",
    f"https://app.hackthebox.com/api/v4/challenge/instance/{instance_id}",
    f"https://www.hackthebox.com/api/v4/docker/{instance_id}",
    f"https://app.hackthebox.com/api/v4/docker/{instance_id}",
]

for endpoint in instance_endpoints:
    print(f"\nProbando: {endpoint}")
    try:
        r = requests.get(endpoint, headers=headers, timeout=5)
        print(f"Status: {r.status_code}")
        if r.status_code == 200:
            data = r.json()
            print(f"Respuesta: {json.dumps(data, indent=2)}")
            break
        elif r.status_code != 404:
            print(f"Respuesta: {r.text[:500]}")
    except Exception as e:
        print(f"Error: {e}")