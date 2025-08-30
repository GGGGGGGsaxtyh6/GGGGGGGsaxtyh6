#!/usr/bin/env python3
"""
Survival of the Fittest Challenge Helper
"""

import json
import subprocess
import os

# Get token
with open('/workspace/htb-mcp-server/.env', 'r') as f:
    for line in f:
        if line.startswith('HTB_TOKEN='):
            token = line.strip().split('=', 1)[1]
            break

print("=" * 60)
print("       SURVIVAL OF THE FITTEST - BLOCKCHAIN CHALLENGE")
print("=" * 60)
print()

print("📋 INFORMACIÓN DEL CHALLENGE:")
print("-" * 40)
print("  Challenge ID: 500")
print("  Nombre: Survival of the Fittest")
print("  Categoría: Blockchain")
print("  Dificultad: Very Easy")
print("  Instance ID: 1658449")
print("  Estado: ✅ ACTIVO")
print()

print("🔗 INFORMACIÓN DE CONEXIÓN:")
print("-" * 40)
print("  Los challenges de Blockchain normalmente proporcionan:")
print("  - Una URL RPC para conectarse al blockchain")
print("  - Un contrato desplegado con una dirección específica")
print("  - Credenciales o llaves privadas (si es necesario)")
print()
print("  Para ver la información de conexión:")
print("  1. Ve a https://app.hackthebox.com/challenges")
print("  2. Busca 'Survival of the Fittest'")
print("  3. La información de conexión aparecerá ahí")
print()

print("🎯 CÓMO RESOLVER:")
print("-" * 40)
print("  1. Conectarte al blockchain usando Web3 o ethers.js")
print("  2. Analizar el smart contract")
print("  3. Encontrar la vulnerabilidad")
print("  4. Explotar para obtener la flag")
print()

print("📝 PARA ENVIAR LA FLAG:")
print("-" * 40)
print("  Cuando encuentres la flag (formato: HTB{...}), úsala así:")
print()
print("  Opción 1 - Usando el MCP Server:")
print('  >>> client.call_tool("submit_challenge_flag", {')
print('  ...     "challenge_id": 500,')
print('  ...     "flag": "HTB{tu_flag_aqui}"')
print('  ... })')
print()
print("  Opción 2 - Usando curl directamente:")
print(f'  curl -X POST \\')
print(f'    -H "Authorization: Bearer {token[:20]}..." \\')
print(f'    -H "Content-Type: application/json" \\')
print(f'    "https://labs.hackthebox.com/api/v4/challenge/own" \\')
print(f'    -d \'{{"challenge_id": 500, "flag": "HTB{{tu_flag_aqui}}", "difficulty": 10}}\'')
print()

print("💡 TIPS PARA BLOCKCHAIN CHALLENGES:")
print("-" * 40)
print("  • Usa Remix IDE (https://remix.ethereum.org) para analizar contratos")
print("  • Herramientas útiles: web3.py, ethers.js, mythril, slither")
print("  • Busca funciones públicas vulnerables")
print("  • Revisa los modificadores y require statements")
print("  • Presta atención a integer overflow/underflow")
print("  • Verifica reentrancy vulnerabilities")
print()

# Intentar obtener más información
print("🔍 INTENTANDO OBTENER MÁS INFORMACIÓN...")
print("-" * 40)

# Probar endpoint de submit para ver el formato
cmd = f'curl -s -H "Authorization: Bearer {token}" -H "Accept: application/json" "https://labs.hackthebox.com/api/v4/challenge/own"'
result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
try:
    data = json.loads(result.stdout)
    if "message" in data:
        print(f"  Endpoint /challenge/own: {data['message'][:100]}")
except:
    pass

print()
print("=" * 60)
print("¡El challenge está activo y listo para resolver!")
print("Visita la página web de HTB para ver los detalles de conexión")
print("=" * 60)