#!/usr/bin/env python3
"""
Ejemplo: Iniciar un challenge y obtener información de conexión
"""

import json
import subprocess
import os
import sys
import time

class HTBMCPClient:
    def __init__(self):
        self.token = None
        if os.path.exists('.env'):
            with open('.env', 'r') as f:
                for line in f:
                    if line.startswith('HTB_TOKEN='):
                        self.token = line.strip().split('=', 1)[1]
                        break
        
        if not self.token:
            print("ERROR: No se encontró HTB_TOKEN en .env")
            sys.exit(1)
        
        env = os.environ.copy()
        env['HTB_TOKEN'] = self.token
        env['LOG_LEVEL'] = 'INFO'
        
        self.process = subprocess.Popen(
            ['./htb-mcp-server'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
            text=True,
            bufsize=1
        )
        self.request_id = 0
        
    def _send_request(self, method, params=None):
        self.request_id += 1
        request = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": method,
            "params": params or {}
        }
        
        request_str = json.dumps(request) + '\n'
        self.process.stdin.write(request_str)
        self.process.stdin.flush()
        
        response_line = self.process.stdout.readline()
        if not response_line:
            return {"error": "No response from server"}
        
        try:
            return json.loads(response_line)
        except json.JSONDecodeError:
            return {"error": f"Failed to parse response: {response_line}"}
    
    def initialize(self):
        return self._send_request("initialize", {
            "protocolVersion": "0.1.0",
            "capabilities": {},
            "clientInfo": {"name": "htb-client", "version": "1.0.0"}
        })
    
    def call_tool(self, tool_name, arguments):
        return self._send_request("tools/call", {
            "name": tool_name,
            "arguments": arguments
        })
    
    def close(self):
        if self.process:
            self.process.terminate()
            self.process.wait()

def get_challenge_info(challenge_id, token):
    """Obtener información del challenge usando curl"""
    import subprocess
    
    cmd = f'curl -s -H "Authorization: Bearer {token}" "https://labs.hackthebox.com/api/v4/challenge/info/{challenge_id}"'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    try:
        data = json.loads(result.stdout)
        if 'challenge' in data:
            ch = data['challenge']
            return {
                'name': ch.get('name'),
                'category': ch.get('category_name'),
                'difficulty': ch.get('difficulty'),
                'docker_ip': ch.get('docker_ip'),
                'docker_ports': ch.get('docker_ports', []),
                'download': ch.get('download'),
                'play_methods': ch.get('play_methods', [])
            }
    except:
        pass
    return None

def main():
    if len(sys.argv) < 2:
        print("Uso: python3 start_challenge.py <challenge_id>")
        print("Ejemplo: python3 start_challenge.py 500")
        sys.exit(1)
    
    challenge_id = int(sys.argv[1])
    
    print(f"=== Challenge ID: {challenge_id} ===\n")
    
    client = HTBMCPClient()
    
    # Inicializar
    print("Inicializando servidor MCP...")
    client.initialize()
    
    # Iniciar challenge
    print(f"Iniciando challenge {challenge_id}...")
    result = client.call_tool("start_challenge", {"challenge_id": challenge_id})
    
    if 'result' in result:
        content = result['result'].get('content', [])
        if content:
            text = content[0].get('text', '')
            print(f"\nRespuesta: {text}")
            
            if 'created' in text.lower() or 'instance' in text.lower():
                print("\n✅ Challenge iniciado exitosamente!")
                
                # Esperar un momento
                print("Esperando a que el challenge se inicialice...")
                time.sleep(3)
                
                # Obtener información de conexión
                print("\nObteniendo información de conexión...")
                info = get_challenge_info(challenge_id, client.token)
                
                if info:
                    print(f"\n📋 INFORMACIÓN DEL CHALLENGE:")
                    print(f"  Nombre: {info['name']}")
                    print(f"  Categoría: {info['category']}")
                    print(f"  Dificultad: {info['difficulty']}")
                    
                    if info['docker_ip'] and info['docker_ports']:
                        print(f"\n🔗 CONEXIÓN:")
                        print(f"  IP: {info['docker_ip']}")
                        print(f"  Puerto(s): {', '.join(map(str, info['docker_ports']))}")
                        print(f"\n  URL: http://{info['docker_ip']}:{info['docker_ports'][0]}")
                        
                        if info['category'] == 'Blockchain':
                            print(f"  RPC: http://{info['docker_ip']}:{info['docker_ports'][0]}/rpc")
                    
                    if info['download']:
                        print(f"\n📥 Archivos descargables disponibles")
                        print(f"  (La contraseña del ZIP es: hackthebox)")
                else:
                    print("No se pudo obtener información adicional")
    else:
        print(f"\nError: {result.get('error', 'Error desconocido')}")
    
    client.close()
    print("\n✅ Proceso completado")

if __name__ == "__main__":
    main()