#!/usr/bin/env python3
import subprocess
import json
import os

# Leer el token
with open('.env', 'r') as f:
    env_content = f.read()
    token = env_content.split('HTB_TOKEN=')[1].split('\n')[0]

env = os.environ.copy()
env['HTB_TOKEN'] = token

# La flag obtenida
flag = "HTB{t3h_FuTUr3_15_bR1ghT_1_H0p3_y0uR3_W34r1nG_5h4d35!}"
challenge_id = "365"  # Como string

print(f"[*] Enviando flag del challenge Baby Time Capsule (ID: {challenge_id})")
print(f"[*] Flag: {flag}")

# Iniciar el servidor MCP
p = subprocess.Popen(['./htb-mcp-server'], 
                    stdin=subprocess.PIPE, 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE,
                    env=env, 
                    text=True)

# Inicializar
init_msg = '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"0.1.0"}}\n'
p.stdin.write(init_msg)
p.stdin.flush()
init_response = p.stdout.readline()
print(f"\n[*] MCP Server inicializado")

# Enviar la flag usando la herramienta submit_challenge_flag
# Formato correcto según el código Go
submit_msg = f'{{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{{"name":"submit_challenge_flag","arguments":{{"challenge_id":"{challenge_id}","flag":"{flag}"}}}}}}\n'
p.stdin.write(submit_msg)
p.stdin.flush()

# Leer la respuesta
response = p.stdout.readline()
print(f"\n[*] Respuesta del servidor:")

try:
    data = json.loads(response)
    if 'result' in data:
        result = data['result']
        if 'content' in result:
            for content in result['content']:
                if content.get('type') == 'text':
                    text = content.get('text', '')
                    print(f"Respuesta: {text}")
                    
                    # Parsear la respuesta JSON dentro del texto si es posible
                    try:
                        flag_result = json.loads(text)
                        print(json.dumps(flag_result, indent=2))
                        
                        # Verificar si la flag fue aceptada
                        if flag_result.get('status') == 'correct' or flag_result.get('message') == 'Correct':
                            print("\n✅ ¡FLAG CORRECTA! El challenge ha sido completado exitosamente.")
                        elif 'already' in str(flag_result).lower() or 'owned' in str(flag_result).lower():
                            print("\n✅ La flag ya había sido enviada anteriormente. Challenge completado.")
                        else:
                            print(f"\nEstado: {flag_result}")
                    except:
                        if 'correct' in text.lower() or 'success' in text.lower() or 'owned' in text.lower():
                            print("\n✅ ¡FLAG CORRECTA! Challenge completado.")
                        elif 'incorrect' in text.lower():
                            print("\n❌ Flag incorrecta")
                        else:
                            print(f"\nRespuesta: {text}")
        elif 'error' in data:
            print(f"Error: {data['error']}")
    else:
        print(response)
except Exception as e:
    print(f"Error parseando respuesta: {e}")
    print(f"Respuesta raw: {response}")

p.terminate()

print("\n" + "="*60)
print("[+] RESUMEN FINAL:")
print(f"[+] Challenge: Baby Time Capsule (ID: 365)")
print(f"[+] Flag obtenida: {flag}")
print("[+] Método: Hastad's Broadcast Attack (RSA con e=5)")
print("[+] IP del servidor: 94.237.55.43:37928")
print("[+] Challenge resuelto completamente de forma autónoma")
print("="*60)