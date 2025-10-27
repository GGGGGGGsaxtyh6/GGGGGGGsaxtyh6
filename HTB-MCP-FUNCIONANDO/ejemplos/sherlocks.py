#!/usr/bin/env python3
"""
Script para trabajar con Sherlocks de HTB
"""
import sys
import subprocess
import json

def get_token():
    with open('.env', 'r') as f:
        for line in f:
            if line.startswith('HTB_TOKEN='):
                return line.strip().split('=', 1)[1]
    return None

def listar_sherlocks():
    token = get_token()
    cmd = f'curl -s -H "Authorization: Bearer {token}" "https://labs.hackthebox.com/api/v4/sherlocks"'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    data = json.loads(result.stdout)
    
    print("=== SHERLOCKS DISPONIBLES ===\n")
    for s in data.get('data', []):
        print(f"ID: {s['id']}")
        print(f"Nombre: {s['name']}")
        print(f"Dificultad: {s['difficulty']}")
        print(f"Estado: {s['state']}")
        print(f"Categoría: {s.get('category_name', 'N/A')}")
        print("-" * 40)

def descargar_sherlock(sherlock_id):
    token = get_token()
    
    # Obtener info
    cmd = f'curl -s -H "Authorization: Bearer {token}" "https://labs.hackthebox.com/api/v4/sherlocks/{sherlock_id}"'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    data = json.loads(result.stdout)
    
    if 'data' in data:
        info = data['data']
        print(f"\n=== SHERLOCK: {info['name']} ===")
        print(f"Dificultad: {info['difficulty']}")
        print(f"Categoría: {info['category_name']}")
        
        # Descargar archivo
        print("\nDescargando archivo...")
        download_cmd = f'curl -H "Authorization: Bearer {token}" "https://labs.hackthebox.com/api/v4/sherlocks/download/{sherlock_id}" -o sherlock_{sherlock_id}.zip'
        subprocess.run(download_cmd, shell=True)
        print(f"Archivo guardado como: sherlock_{sherlock_id}.zip")
        print("Contraseña del ZIP: hackthebox")
    else:
        print("Error obteniendo información del Sherlock")

def enviar_respuesta(sherlock_id, pregunta_num, respuesta):
    token = get_token()
    
    # Los Sherlocks tienen preguntas que responder
    cmd = f'''curl -X POST -H "Authorization: Bearer {token}" \
              -H "Content-Type: application/json" \
              "https://labs.hackthebox.com/api/v4/sherlocks/{sherlock_id}/submit" \
              -d '{{"question": {pregunta_num}, "answer": "{respuesta}"}}'
    '''
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(result.stdout)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso:")
        print("  python3 sherlocks.py listar")
        print("  python3 sherlocks.py descargar <id>")
        print("  python3 sherlocks.py responder <id> <pregunta> <respuesta>")
        sys.exit(1)
    
    comando = sys.argv[1]
    
    if comando == "listar":
        listar_sherlocks()
    elif comando == "descargar" and len(sys.argv) > 2:
        descargar_sherlock(sys.argv[2])
    elif comando == "responder" and len(sys.argv) > 4:
        enviar_respuesta(sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        print("Comando no válido")