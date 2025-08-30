#!/usr/bin/env python3
"""
Ejemplo: Listar máquinas y challenges disponibles
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

def parse_machines(text):
    """Parsear la respuesta de máquinas"""
    machines = []
    try:
        # Intentar parsear como JSON
        data = json.loads(text)
        if isinstance(data, list):
            for m in data:
                machines.append({
                    'id': m.get('id'),
                    'name': m.get('name'),
                    'os': m.get('os'),
                    'difficulty': m.get('difficultyText', m.get('difficulty')),
                    'points': m.get('points')
                })
    except:
        # Si no es JSON, intentar extraer de texto
        lines = text.split('\n')
        for line in lines:
            if '"id":' in line and '"name":' in line:
                # Extraer información básica
                pass
    return machines

def parse_challenges(text):
    """Parsear la respuesta de challenges"""
    challenges = []
    try:
        data = json.loads(text)
        if isinstance(data, list):
            for c in data:
                challenges.append({
                    'id': c.get('id'),
                    'name': c.get('name'),
                    'category': c.get('category_name'),
                    'difficulty': c.get('difficulty'),
                    'points': c.get('points')
                })
    except:
        pass
    return challenges

def main():
    print("=== HTB Content Lister ===\n")
    
    client = HTBMCPClient()
    
    # Inicializar
    print("Inicializando servidor MCP...")
    client.initialize()
    
    # Menú
    while True:
        print("\n¿Qué deseas listar?")
        print("1. Máquinas activas")
        print("2. Máquinas retiradas")
        print("3. Challenges por categoría")
        print("4. Mi perfil")
        print("5. Buscar contenido")
        print("0. Salir")
        
        choice = input("\nOpción: ").strip()
        
        if choice == "1":
            print("\n📦 MÁQUINAS ACTIVAS:")
            result = client.call_tool("list_machines", {
                "status": "active",
                "per_page": 20
            })
            
            if 'result' in result:
                content = result['result'].get('content', [])
                if content:
                    text = content[0].get('text', '')
                    machines = parse_machines(text)
                    
                    if machines:
                        for m in machines[:10]:
                            print(f"  [{m['id']}] {m['name']} - {m['os']} - {m['difficulty']} ({m['points']} pts)")
                    else:
                        print(text[:500])
                        
        elif choice == "2":
            print("\n📦 MÁQUINAS RETIRADAS:")
            result = client.call_tool("list_machines", {
                "status": "retired",
                "per_page": 20
            })
            
            if 'result' in result:
                content = result['result'].get('content', [])
                if content:
                    text = content[0].get('text', '')
                    print(text[:1000])
                    
        elif choice == "3":
            category = input("Categoría (Web/Crypto/Pwn/Reversing/Forensics/Misc): ").strip()
            print(f"\n🎯 CHALLENGES DE {category.upper()}:")
            
            result = client.call_tool("list_challenges", {
                "category": category,
                "limit": 20
            })
            
            if 'result' in result:
                content = result['result'].get('content', [])
                if content:
                    text = content[0].get('text', '')
                    challenges = parse_challenges(text)
                    
                    if challenges:
                        for c in challenges[:10]:
                            print(f"  [{c['id']}] {c['name']} - {c['difficulty']} ({c['points']} pts)")
                    else:
                        print(text[:500])
                        
        elif choice == "4":
            print("\n👤 MI PERFIL:")
            result = client.call_tool("get_user_profile", {})
            
            if 'result' in result:
                content = result['result'].get('content', [])
                if content:
                    text = content[0].get('text', '')
                    try:
                        profile = json.loads(text)
                        print(f"  Usuario: {profile.get('name')}")
                        print(f"  Email: {profile.get('email')}")
                        print(f"  VIP: {profile.get('isVip')}")
                        print(f"  Server ID: {profile.get('server_id')}")
                    except:
                        print(text[:500])
                        
        elif choice == "5":
            query = input("Buscar: ").strip()
            print(f"\n🔍 RESULTADOS PARA '{query}':")
            
            result = client.call_tool("search_content", {
                "query": query,
                "type": "all"
            })
            
            if 'result' in result:
                content = result['result'].get('content', [])
                if content:
                    text = content[0].get('text', '')
                    print(text[:1000])
                    
        elif choice == "0":
            break
    
    client.close()
    print("\n✅ Sesión terminada")

if __name__ == "__main__":
    main()