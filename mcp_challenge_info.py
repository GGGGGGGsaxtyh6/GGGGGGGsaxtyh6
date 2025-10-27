#!/usr/bin/env python3
import json
import subprocess
import os

class HTBMCPClient:
    def __init__(self):
        env_path = '/workspace/htb-mcp-server/.env'
        self.token = None
        if os.path.exists(env_path):
            with open(env_path, 'r') as f:
                for line in f:
                    if line.startswith('HTB_TOKEN='):
                        self.token = line.strip().split('=', 1)[1]
                        break
        
        env = os.environ.copy()
        env['HTB_TOKEN'] = self.token
        env['LOG_LEVEL'] = 'INFO'
        
        self.process = subprocess.Popen(
            ['/workspace/htb-mcp-server/htb-mcp-server'],
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

# Crear cliente y obtener información
client = HTBMCPClient()

# Inicializar
print("Inicializando MCP...")
client.initialize()

# Obtener información del challenge
print("\n=== INFORMACIÓN DEL CHALLENGE SURVIVAL OF THE FITTEST ===\n")

# Obtener estado del servidor
print("1. Estado del servidor MCP:")
result = client.call_tool("get_server_status", {})
if 'result' in result and 'content' in result['result']:
    content = result['result']['content']
    if isinstance(content, list) and len(content) > 0:
        print(content[0].get('text', '')[:500])

print("\n2. Información del usuario:")
result = client.call_tool("get_user_profile", {})
if 'result' in result and 'content' in result['result']:
    content = result['result']['content']
    if isinstance(content, list) and len(content) > 0:
        text = content[0].get('text', '')
        # Extraer solo información relevante
        lines = text.split('\n')
        for line in lines[:10]:
            if line.strip():
                print(f"  {line.strip()}")

print("\n3. Para enviar la flag cuando la encuentres:")
print("   Usa el servidor MCP con:")
print('   client.call_tool("submit_challenge_flag", {')
print('       "challenge_id": 500,')
print('       "flag": "HTB{la_flag_que_encuentres}"')
print('   })')

print("\n4. Challenge activo:")
print("   - ID: 500")
print("   - Nombre: Survival of the Fittest")
print("   - Categoría: Blockchain")
print("   - Instance ID: 1658449")
print("   - Estado: ACTIVO")

client.close()
print("\n=== FIN ===")