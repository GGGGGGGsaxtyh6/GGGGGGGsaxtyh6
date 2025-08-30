#!/usr/bin/env python3
"""
Script para obtener la IP de un challenge de HackTheBox
Autor: HTB MCP Tools
"""

import requests
import json
import sys
import os

def get_challenge_ip(challenge_id):
    """
    Obtiene la IP y puerto de un challenge de HackTheBox
    
    Args:
        challenge_id: ID del challenge (ej: 365 para Baby Time Capsule)
    
    Returns:
        tuple: (ip, port) o (None, None) si no se encuentra
    """
    
    # Leer el token del archivo .env
    if not os.path.exists('.env'):
        print("[-] ERROR: No se encuentra el archivo .env")
        print("[*] Copia .env.example a .env y añade tu token")
        return None, None
    
    with open('.env', 'r') as f:
        env_content = f.read()
        try:
            token = env_content.split('HTB_TOKEN=')[1].split('\n')[0]
        except:
            print("[-] ERROR: No se pudo leer el token del archivo .env")
            return None, None
    
    if token == 'TU_TOKEN_AQUI':
        print("[-] ERROR: Debes reemplazar TU_TOKEN_AQUI con tu token real en .env")
        return None, None
    
    # Headers para la API
    headers = {
        "Authorization": f"Bearer {token}",
        "User-Agent": "HTB MCP Server",
        "Accept": "application/json"
    }
    
    # Endpoint correcto para obtener información del challenge
    url = f"https://labs.hackthebox.com/api/v4/challenge/info/{challenge_id}"
    
    print(f"[*] Obteniendo información del challenge {challenge_id}...")
    
    try:
        r = requests.get(url, headers=headers, timeout=10)
        
        if r.status_code == 200:
            data = r.json()
            
            if 'challenge' in data:
                challenge = data['challenge']
                name = challenge.get('name', 'Unknown')
                docker_ip = challenge.get('docker_ip')
                docker_ports = challenge.get('docker_ports', [])
                
                print(f"[+] Challenge: {name}")
                print(f"[+] Dificultad: {challenge.get('difficulty', 'Unknown')}")
                
                if docker_ip and docker_ports:
                    port = docker_ports[0] if docker_ports else None
                    print(f"[+] IP: {docker_ip}")
                    print(f"[+] Puerto: {port}")
                    return docker_ip, port
                else:
                    print("[-] El challenge no tiene una instancia activa")
                    print("[*] Necesitas iniciar el challenge primero")
                    return None, None
            else:
                print("[-] Respuesta inesperada de la API")
                return None, None
                
        elif r.status_code == 401:
            print("[-] Token inválido o expirado")
            return None, None
        elif r.status_code == 404:
            print(f"[-] Challenge con ID {challenge_id} no encontrado")
            return None, None
        else:
            print(f"[-] Error: Status {r.status_code}")
            return None, None
            
    except requests.exceptions.RequestException as e:
        print(f"[-] Error de conexión: {e}")
        return None, None
    except Exception as e:
        print(f"[-] Error inesperado: {e}")
        return None, None

def main():
    if len(sys.argv) != 2:
        print("Uso: python3 get_challenge_ip.py <challenge_id>")
        print("Ejemplo: python3 get_challenge_ip.py 365")
        print("\nChallenges comunes:")
        print("  365 - Baby Time Capsule (Crypto)")
        print("  500 - Otro challenge")
        sys.exit(1)
    
    try:
        challenge_id = int(sys.argv[1])
    except ValueError:
        print("[-] El ID del challenge debe ser un número")
        sys.exit(1)
    
    ip, port = get_challenge_ip(challenge_id)
    
    if ip and port:
        print(f"\n[*] Conexión: nc {ip} {port}")
        print(f"[*] O usa: python3 tu_exploit.py {ip} {port}")
    else:
        print("\n[!] No se pudo obtener la IP del challenge")
        print("[*] Posibles razones:")
        print("    1. El challenge no está iniciado")
        print("    2. El token es inválido")
        print("    3. El challenge ID es incorrecto")

if __name__ == "__main__":
    main()