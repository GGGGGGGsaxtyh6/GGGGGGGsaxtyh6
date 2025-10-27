#!/usr/bin/env python3
"""
Get information about Survival of the Fittest challenge
"""

import json
import subprocess

# Get token
with open('/workspace/htb-mcp-server/.env', 'r') as f:
    for line in f:
        if line.startswith('HTB_TOKEN='):
            token = line.strip().split('=', 1)[1]
            break

print("=== SURVIVAL OF THE FITTEST ===\n")
print("Challenge ID: 500")
print("Instance ID: 1658449")
print("Category: Blockchain")
print("Difficulty: Very Easy")
print()

# Try to get more info about the challenge
endpoints = [
    ("https://labs.hackthebox.com/api/v4/challenge/500", "Challenge Info"),
    ("https://labs.hackthebox.com/api/v4/challenge/info/500", "Challenge Details"),
    ("https://labs.hackthebox.com/api/v4/challenge/instance", "Active Instance"),
]

for endpoint, description in endpoints:
    print(f"Checking {description}...")
    cmd = f'curl -s -H "Authorization: Bearer {token}" -H "Accept: application/json" "{endpoint}"'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    try:
        data = json.loads(result.stdout)
        if "message" not in data or "not found" not in data.get("message", "").lower():
            print(f"  Response: {json.dumps(data, indent=2)[:500]}")
        else:
            print(f"  Endpoint not available")
    except:
        print(f"  No valid response")
    print()

print("\n=== INFORMACIÓN DEL CHALLENGE ===")
print("Este es un challenge de Blockchain de dificultad Very Easy.")
print("Los challenges de Blockchain generalmente involucran:")
print("  - Smart contracts")
print("  - Análisis de transacciones")
print("  - Vulnerabilidades en contratos")
print("  - Manipulación de estados")
print("\nLa instancia está activa con ID: 1658449")
print("\nPara resolver el challenge, probablemente necesitarás:")
print("  1. Conectarte a la instancia del blockchain")
print("  2. Analizar el smart contract")
print("  3. Encontrar la vulnerabilidad")
print("  4. Explotar para obtener la flag")
print("\nPara enviar la flag cuando la encuentres:")
print('client.call_tool("submit_challenge_flag", {"challenge_id": 500, "flag": "HTB{...}"})')