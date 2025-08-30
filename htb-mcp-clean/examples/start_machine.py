#!/usr/bin/env python3
"""
Ejemplo: Iniciar una máquina en HTB
"""

import json
import subprocess
import os
import sys

class HTBMCPClient:
    def __init__(self):
        # Leer token del .env
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
        
        # Configurar entorno
        env = os.environ.copy()
        env['HTB_TOKEN'] = self.token
        env['LOG_LEVEL'] = 'INFO'
        
        # Iniciar proceso del servidor
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
    if len(sys.argv) < 2:
        print("Uso: python3 start_machine.py <machine_id>")
        print("Ejemplo: python3 start_machine.py 701")
        sys.exit(1)
    
    machine_id = int(sys.argv[1])
    
    print(f"=== Iniciando Máquina ID: {machine_id} ===\n")
    
    client = HTBMCPClient()
    
    # Inicializar
    print("Inicializando servidor MCP...")
    client.initialize()
    
    # Iniciar máquina
    print(f"Iniciando máquina {machine_id}...")
    result = client.call_tool("start_machine", {"machine_id": machine_id})
    
    if 'result' in result:
        content = result['result'].get('content', [])
        if content:
            print(f"\nRespuesta: {content[0].get('text', 'Sin respuesta')}")
    else:
        print(f"\nError: {result.get('error', 'Error desconocido')}")
    
    # Obtener IP
    print("\nObteniendo IP de la máquina...")
    result = client.call_tool("get_machine_ip", {})
    
    if 'result' in result:
        content = result['result'].get('content', [])
        if content:
            print(f"IP: {content[0].get('text', 'No disponible')}")
    
    client.close()
    print("\n✅ Proceso completado")

if __name__ == "__main__":
    main()