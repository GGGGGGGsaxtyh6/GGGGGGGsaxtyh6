#!/usr/bin/env python3
"""
HTB Challenges Explorer - Lista y gestiona challenges
"""

import json
import subprocess
import sys
import os
from typing import Dict, Any, Optional

class HTBMCPClient:
    def __init__(self):
        # Get HTB token from environment
        env_path = '/workspace/htb-mcp-server/.env'
        self.token = None
        if os.path.exists(env_path):
            with open(env_path, 'r') as f:
                for line in f:
                    if line.startswith('HTB_TOKEN='):
                        self.token = line.strip().split('=', 1)[1]
                        break
        
        if not self.token:
            raise ValueError("HTB_TOKEN not found in .env file")
        
        # Start the MCP server process
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
        
    def _send_request(self, method: str, params: Optional[Dict] = None) -> Dict:
        """Send a JSON-RPC request and get response"""
        self.request_id += 1
        request = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": method,
            "params": params or {}
        }
        
        # Send request
        request_str = json.dumps(request) + '\n'
        self.process.stdin.write(request_str)
        self.process.stdin.flush()
        
        # Read response
        response_line = self.process.stdout.readline()
        if not response_line:
            return {"error": "No response from server"}
        
        try:
            response = json.loads(response_line)
            return response
        except json.JSONDecodeError as e:
            return {"error": f"Failed to parse response: {response_line}"}
    
    def initialize(self):
        """Initialize the MCP session"""
        return self._send_request("initialize", {
            "protocolVersion": "0.1.0",
            "capabilities": {},
            "clientInfo": {
                "name": "htb-client",
                "version": "1.0.0"
            }
        })
    
    def call_tool(self, tool_name: str, arguments: Dict[str, Any]):
        """Call a specific tool"""
        return self._send_request("tools/call", {
            "name": tool_name,
            "arguments": arguments
        })
    
    def close(self):
        """Close the MCP server process"""
        if self.process:
            self.process.terminate()
            self.process.wait()

def parse_challenge_data(text):
    """Parse challenge data from text response"""
    challenges = []
    try:
        # Try to parse as JSON first
        data = json.loads(text)
        if isinstance(data, list):
            return data
    except:
        pass
    
    # Parse text format
    lines = text.split('\n')
    current_challenge = {}
    
    for line in lines:
        line = line.strip()
        if line.startswith('{'):
            # Start of JSON object
            try:
                current_challenge = json.loads(line)
                challenges.append(current_challenge)
            except:
                pass
        elif '"id":' in line:
            # Extract challenge info from formatted text
            if current_challenge:
                challenges.append(current_challenge)
                current_challenge = {}
    
    return challenges

def main():
    """List and manage HTB challenges"""
    client = HTBMCPClient()
    
    try:
        print("=== HTB Challenges Explorer ===\n")
        
        # Initialize session
        print("Inicializando sesión...")
        result = client.initialize()
        if 'result' not in result:
            print(f"Error: {result}")
            return
        print("✓ Sesión iniciada\n")
        
        # List challenges by category
        categories = ["Web", "Crypto", "Pwn", "Reversing", "Forensics", "Mobile", "OSINT", "Misc", "Hardware"]
        
        print("Buscando challenges por categoría...\n")
        
        all_challenges = {}
        
        for category in categories:
            print(f"📁 Categoría: {category}")
            
            # Get challenges for this category
            result = client.call_tool("list_challenges", {
                "category": category,
                "limit": 100,
                "status": "active"
            })
            
            if 'result' in result:
                result_data = result['result']
                if isinstance(result_data, dict) and 'content' in result_data:
                    content = result_data['content']
                    if isinstance(content, list) and len(content) > 0:
                        text = content[0].get('text', '')
                        
                        # Try to parse challenges
                        if text and not text.startswith("Error"):
                            try:
                                # Parse JSON array from text
                                if text.strip().startswith('['):
                                    challenges = json.loads(text)
                                    all_challenges[category] = challenges
                                    print(f"   ✓ {len(challenges)} challenges encontrados")
                                    
                                    # Show first 3 challenges
                                    for i, ch in enumerate(challenges[:3]):
                                        print(f"     - {ch.get('name', 'Unknown')} (ID: {ch.get('id', '?')}, {ch.get('difficulty', '?')}, {ch.get('points', 0)} pts)")
                                    if len(challenges) > 3:
                                        print(f"     ... y {len(challenges)-3} más")
                                else:
                                    print(f"   ⚠ Formato no reconocido")
                            except Exception as e:
                                print(f"   ⚠ No se pudieron parsear los challenges")
                        else:
                            print(f"   ⚠ Sin challenges o error en la respuesta")
            else:
                print(f"   ✗ Error obteniendo challenges")
            
            print()
        
        # Summary
        print("\n=== RESUMEN ===")
        total = sum(len(chs) for chs in all_challenges.values())
        print(f"Total de challenges encontrados: {total}")
        
        for cat, chs in all_challenges.items():
            if chs:
                print(f"  • {cat}: {len(chs)} challenges")
        
        # Try to start a challenge (example)
        print("\n=== EJEMPLO: Iniciar un Challenge ===")
        print("Para iniciar un challenge, usa el comando:")
        print('client.call_tool("start_challenge", {"challenge_id": "ID_DEL_CHALLENGE"})')
        
        # Show how to submit a flag
        print("\n=== EJEMPLO: Enviar una Flag ===")
        print("Para enviar una flag de challenge:")
        print('client.call_tool("submit_challenge_flag", {"challenge_id": "ID", "flag": "HTB{...}"})')
        
    finally:
        client.close()
        print("\n=== Fin ===")

if __name__ == "__main__":
    main()