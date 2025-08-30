#!/usr/bin/env python3
"""
Ejemplo: Enviar una flag a HTB
"""

import json
import subprocess
import os
import sys

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

def main():
    if len(sys.argv) < 4:
        print("Uso: python3 submit_flag.py <tipo> <id> <flag>")
        print("\nTipos disponibles:")
        print("  challenge - Para challenges")
        print("  user      - Para flag de usuario en máquinas")
        print("  root      - Para flag de root en máquinas")
        print("\nEjemplos:")
        print("  python3 submit_flag.py challenge 500 'HTB{flag_here}'")
        print("  python3 submit_flag.py user 701 'HTB{user_flag}'")
        print("  python3 submit_flag.py root 701 'HTB{root_flag}'")
        sys.exit(1)
    
    flag_type = sys.argv[1].lower()
    entity_id = int(sys.argv[2])
    flag = sys.argv[3]
    
    print(f"=== Enviando Flag ===\n")
    print(f"Tipo: {flag_type}")
    print(f"ID: {entity_id}")
    print(f"Flag: {flag[:10]}...{flag[-5:]}")
    print()
    
    client = HTBMCPClient()
    
    # Inicializar
    print("Inicializando servidor MCP...")
    client.initialize()
    
    # Enviar flag según el tipo
    if flag_type == "challenge":
        print(f"Enviando flag de challenge {entity_id}...")
        result = client.call_tool("submit_challenge_flag", {
            "challenge_id": entity_id,
            "flag": flag
        })
    elif flag_type == "user":
        print(f"Enviando flag de usuario para máquina {entity_id}...")
        result = client.call_tool("submit_user_flag", {
            "machine_id": entity_id,
            "flag": flag
        })
    elif flag_type == "root":
        print(f"Enviando flag de root para máquina {entity_id}...")
        result = client.call_tool("submit_root_flag", {
            "machine_id": entity_id,
            "flag": flag
        })
    else:
        print(f"ERROR: Tipo '{flag_type}' no válido")
        client.close()
        sys.exit(1)
    
    # Mostrar resultado
    if 'result' in result:
        content = result['result'].get('content', [])
        if content:
            text = content[0].get('text', '')
            if 'congratulations' in text.lower() or 'correct' in text.lower():
                print(f"\n✅ ¡FLAG CORRECTA!")
            else:
                print(f"\nRespuesta: {text}")
    else:
        error = result.get('error', {})
        if isinstance(error, dict):
            print(f"\n❌ Error: {error.get('message', 'Error desconocido')}")
        else:
            print(f"\n❌ Error: {error}")
    
    client.close()
    print("\n✅ Proceso completado")

if __name__ == "__main__":
    main()