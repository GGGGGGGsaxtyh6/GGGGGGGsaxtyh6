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

# Enviar la flag
client = HTBMCPClient()
print("=== ENVIANDO FLAG DE SURVIVAL OF THE FITTEST ===\n")

# Inicializar
client.initialize()

# Enviar flag
print("Enviando flag: HTB{g0t_y0u2_f1r5t_b100d}")
result = client.call_tool("submit_challenge_flag", {
    "challenge_id": 500,
    "flag": "HTB{g0t_y0u2_f1r5t_b100d}"
})

if 'result' in result:
    content = result['result'].get('content', [])
    if content and len(content) > 0:
        text = content[0].get('text', '')
        print(f"\nRespuesta: {text}")
else:
    print(f"\nError: {result}")

client.close()
print("\n✅ FLAG ENVIADA!")