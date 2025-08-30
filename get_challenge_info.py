#!/usr/bin/env python3
import requests
import json
import os
from dotenv import load_dotenv

# Cargar el token desde .env
load_dotenv('/workspace/HTB-MCP-MEJORADO/.env')
token = os.getenv('HTB_TOKEN')

if not token:
    print("[!] No se encontró el token HTB_TOKEN")
    exit(1)

# Headers con el token
headers = {
    'Authorization': f'Bearer {token}',
    'User-Agent': 'HTB-MCP-Client/1.0',
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}

# ID del challenge
challenge_id = 972

print(f"[*] Obteniendo información del challenge ID {challenge_id}...")

# Endpoint para obtener información del challenge
url = f"https://labs.hackthebox.com/api/v4/challenge/info/{challenge_id}"

try:
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        
        # Extraer información relevante
        if 'challenge' in data:
            challenge = data['challenge']
            print(f"\n[+] Nombre: {challenge.get('name', 'N/A')}")
            print(f"[+] Categoría: {challenge.get('category_name', 'N/A')}")
            print(f"[+] Dificultad: {challenge.get('difficulty_text', 'N/A')}")
            print(f"[+] Puntos: {challenge.get('points', 'N/A')}")
            print(f"[+] Solves: {challenge.get('solves', 'N/A')}")
            print(f"[+] Likes: {challenge.get('likes', 'N/A')}")
            print(f"[+] Dislikes: {challenge.get('dislikes', 'N/A')}")
            
            # Descripción del challenge
            description = challenge.get('description', '')
            if description:
                print(f"\n[+] DESCRIPCIÓN DEL RETO:")
                print("="*60)
                print(description)
                print("="*60)
            
            # Archivos adjuntos
            if 'challenge_files' in challenge:
                files = challenge['challenge_files']
                if files:
                    print(f"\n[+] Archivos adjuntos:")
                    for file in files:
                        print(f"    - {file.get('name', 'N/A')}")
            
            # Tags
            if 'tags' in challenge:
                tags = challenge['tags']
                if tags:
                    print(f"\n[+] Tags:")
                    for tag in tags:
                        print(f"    - {tag.get('name', 'N/A')}")
            
            # Información de la instancia
            if 'docker_ip' in challenge and challenge['docker_ip']:
                print(f"\n[+] IP de la instancia: {challenge['docker_ip']}")
                if 'docker_ports' in challenge:
                    print(f"[+] Puerto: {challenge['docker_ports']}")
        else:
            print("[!] No se pudo obtener la información del challenge")
            print(f"[!] Respuesta: {data}")
    else:
        print(f"[!] Error: {response.status_code}")
        print(f"[!] Respuesta: {response.text}")
        
except Exception as e:
    print(f"[!] Error: {e}")

# También intentar obtener más detalles
print("\n[*] Intentando obtener más detalles...")
url2 = f"https://labs.hackthebox.com/api/v4/challenge/{challenge_id}"
try:
    response = requests.get(url2, headers=headers)
    if response.status_code == 200:
        data = response.json()
        # Buscar cualquier información adicional
        if 'hint' in data:
            print(f"[+] PISTA: {data['hint']}")
        if 'author' in data:
            print(f"[+] Autor: {data['author']}")
except:
    pass