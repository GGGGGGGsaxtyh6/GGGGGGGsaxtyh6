#!/usr/bin/env python3
"""
Start HTB Challenge
"""

import json
import subprocess
import sys
import time

def start_challenge(challenge_id):
    """Start a specific challenge by ID"""
    
    # Get token
    with open('/workspace/htb-mcp-server/.env', 'r') as f:
        for line in f:
            if line.startswith('HTB_TOKEN='):
                token = line.strip().split('=', 1)[1]
                break
    
    print(f"=== Iniciando Challenge ID: {challenge_id} ===\n")
    
    # Try different possible endpoints
    endpoints = [
        f"https://labs.hackthebox.com/api/v4/challenge/{challenge_id}/start",
        f"https://labs.hackthebox.com/api/v4/challenge/start/{challenge_id}",
        f"https://labs.hackthebox.com/api/v4/challenge/spawn/{challenge_id}",
        f"https://labs.hackthebox.com/api/v4/challenge/{challenge_id}/spawn"
    ]
    
    for endpoint in endpoints:
        print(f"Probando: {endpoint}")
        
        cmd = f'curl -s -X POST -H "Authorization: Bearer {token}" -H "Accept: application/json" -H "Content-Type: application/json" "{endpoint}" -d "{{}}"'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        try:
            response = json.loads(result.stdout)
            
            # Check if successful
            if "success" in response or "challenge" in response or "instance" in response:
                print(f"\n✅ Challenge iniciado exitosamente!")
                print(f"Respuesta: {json.dumps(response, indent=2)}")
                
                # Get challenge info
                get_info_cmd = f'curl -s -H "Authorization: Bearer {token}" -H "Accept: application/json" "https://labs.hackthebox.com/api/v4/challenge/{challenge_id}"'
                info_result = subprocess.run(get_info_cmd, shell=True, capture_output=True, text=True)
                
                try:
                    info = json.loads(info_result.stdout)
                    if "challenge" in info:
                        ch = info["challenge"]
                        print(f"\n📋 Información del Challenge:")
                        print(f"  Nombre: {ch.get('name', 'N/A')}")
                        print(f"  Categoría: {ch.get('category_name', 'N/A')}")
                        print(f"  Dificultad: {ch.get('difficulty', 'N/A')}")
                        print(f"  Puntos: {ch.get('points', 0)}")
                        print(f"  Descripción: {ch.get('description', 'N/A')}")
                        
                        # Check for docker instance
                        if "docker_ip" in ch or "docker_port" in ch:
                            print(f"\n🐳 Instancia Docker:")
                            print(f"  IP: {ch.get('docker_ip', 'N/A')}")
                            print(f"  Puerto: {ch.get('docker_port', 'N/A')}")
                        
                        # Check for download link
                        if "download" in ch:
                            print(f"\n📥 Descarga: {ch.get('download', 'N/A')}")
                            
                except Exception as e:
                    print(f"No se pudo obtener información adicional: {e}")
                
                return True
                
            elif "message" in response:
                if "not found" not in response["message"].lower():
                    print(f"  Respuesta: {response['message']}")
                    
        except json.JSONDecodeError:
            if result.stdout:
                print(f"  Respuesta no JSON: {result.stdout[:100]}")
    
    print("\n❌ No se pudo iniciar el challenge")
    print("Puede que el challenge ya esté activo o que el ID no sea válido")
    return False

def main():
    if len(sys.argv) < 2:
        print("Uso: python3 start_challenge.py <challenge_id>")
        print("\nEjemplos de IDs de challenges:")
        print("  - 2: The Art of Reversing (Easy)")
        print("  - 6: Weak RSA (Easy)")
        print("  - 100: interdimensional internet (Medium)")
        print("  - 87: Illumination (Easy)")
        sys.exit(1)
    
    challenge_id = sys.argv[1]
    start_challenge(challenge_id)

if __name__ == "__main__":
    main()