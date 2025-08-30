#!/usr/bin/env python3
"""
Script para enviar flags a HackTheBox
"""

import requests
import json
import sys
import os

def get_challenge_difficulty(challenge_id, token):
    """Obtiene la dificultad de un challenge"""
    headers = {
        "Authorization": f"Bearer {token}",
        "User-Agent": "HTB MCP Server",
        "Accept": "application/json"
    }
    
    url = f"https://labs.hackthebox.com/api/v4/challenge/info/{challenge_id}"
    r = requests.get(url, headers=headers)
    
    if r.status_code == 200:
        data = r.json()
        if 'challenge' in data:
            return data['challenge'].get('difficulty', 'Very Easy')
    
    return 'Very Easy'

def submit_flag(challenge_id, flag):
    """
    Envía una flag a HackTheBox
    
    Args:
        challenge_id: ID del challenge
        flag: La flag a enviar
    
    Returns:
        bool: True si la flag fue aceptada, False en caso contrario
    """
    
    # Leer el token
    if not os.path.exists('.env'):
        print("[-] ERROR: No se encuentra el archivo .env")
        return False
    
    with open('.env', 'r') as f:
        env_content = f.read()
        try:
            token = env_content.split('HTB_TOKEN=')[1].split('\n')[0]
        except:
            print("[-] ERROR: No se pudo leer el token del archivo .env")
            return False
    
    if token == 'TU_TOKEN_AQUI':
        print("[-] ERROR: Debes reemplazar TU_TOKEN_AQUI con tu token real en .env")
        return False
    
    print(f"[*] Enviando flag para challenge {challenge_id}")
    print(f"[*] Flag: {flag}")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "User-Agent": "HTB MCP Server",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    # Mapeo de dificultades
    difficulty_map = {
        "Very Easy": 10,
        "Easy": 20,
        "Medium": 30,
        "Hard": 40,
        "Insane": 50
    }
    
    # Obtener dificultad
    print("\n[*] Obteniendo información del challenge...")
    diff_text = get_challenge_difficulty(challenge_id, token)
    difficulty_value = difficulty_map.get(diff_text, 10)
    print(f"    Dificultad: {diff_text}")
    
    # Enviar la flag
    print("\n[*] Enviando flag a HackTheBox...")
    url = "https://labs.hackthebox.com/api/v4/challenge/own"
    payload = {
        "challenge_id": challenge_id,
        "flag": flag,
        "difficulty": difficulty_value
    }
    
    try:
        r = requests.post(url, json=payload, headers=headers, timeout=10)
        
        if r.status_code == 200:
            try:
                data = r.json()
                message = data.get('message', '').lower()
                
                if 'congratulations' in message or 'correct' in message:
                    print("\n✅ ¡FLAG CORRECTA! Challenge completado exitosamente.")
                    print(f"    Mensaje: {data.get('message')}")
                    return True
                elif 'already' in message or 'owned' in message:
                    print("\n✅ La flag ya había sido enviada anteriormente.")
                    print("    Challenge ya completado.")
                    return True
                else:
                    print(f"\n[-] Respuesta: {data.get('message')}")
                    return False
            except:
                print(f"[-] Error procesando respuesta: {r.text[:200]}")
                return False
        else:
            # Intentar sin difficulty
            print("[*] Intentando sin parámetro de dificultad...")
            payload = {
                "challenge_id": challenge_id,
                "flag": flag
            }
            r = requests.post(url, json=payload, headers=headers, timeout=10)
            
            if r.status_code == 200:
                data = r.json()
                if 'congratulations' in str(data).lower() or 'correct' in str(data).lower():
                    print("\n✅ ¡FLAG CORRECTA! Challenge completado.")
                    return True
            
            print(f"[-] Error: {r.text[:200]}")
            return False
            
    except Exception as e:
        print(f"[-] Error: {e}")
        return False

def main():
    if len(sys.argv) != 3:
        print("Uso: python3 submit_flag.py <challenge_id> <flag>")
        print('Ejemplo: python3 submit_flag.py 365 "HTB{flag_here}"')
        sys.exit(1)
    
    try:
        challenge_id = int(sys.argv[1])
    except ValueError:
        print("[-] El ID del challenge debe ser un número")
        sys.exit(1)
    
    flag = sys.argv[2]
    
    if not flag.startswith("HTB{") or not flag.endswith("}"):
        print("[!] Advertencia: La flag no tiene el formato HTB{...}")
        response = input("[?] ¿Continuar de todos modos? (s/n): ")
        if response.lower() != 's':
            sys.exit(0)
    
    if submit_flag(challenge_id, flag):
        print("\n[+] Flag enviada exitosamente")
    else:
        print("\n[-] No se pudo enviar la flag")

if __name__ == "__main__":
    main()