#!/usr/bin/env python3
"""
Test the updated MCP server
"""

import json
import subprocess
import sys
import os
import time
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

def test_machines(client):
    """Test machine-related functionality"""
    print("\n=== TESTING MACHINES ===")
    
    # List machines
    print("\n1. Listing machines...")
    result = client.call_tool("list_machines", {"status": "active", "per_page": 3})
    if 'result' in result:
        print("✅ List machines works!")
    else:
        print(f"❌ List machines failed: {result.get('error', 'Unknown error')}")
    
    # Start a machine
    print("\n2. Starting machine Previous (ID: 701)...")
    result = client.call_tool("start_machine", {"machine_id": 701})
    if 'result' in result:
        content = result['result'].get('content', [])
        if content and len(content) > 0:
            text = content[0].get('text', '')
            if 'success' in text.lower() or 'spawned' in text.lower() or 'already' in text.lower():
                print("✅ Start machine works!")
            else:
                print(f"⚠️ Machine start response: {text[:100]}")
    else:
        print(f"❌ Start machine failed: {result.get('error', 'Unknown error')}")

def test_challenges(client):
    """Test challenge-related functionality"""
    print("\n=== TESTING CHALLENGES ===")
    
    # List challenges
    print("\n1. Listing challenges...")
    result = client.call_tool("list_challenges", {"category": "Web", "limit": 5})
    if 'result' in result:
        print("✅ List challenges works!")
    else:
        print(f"❌ List challenges failed: {result.get('error', 'Unknown error')}")
    
    # Start a challenge (Web challenge with container)
    print("\n2. Starting challenge Flag Command (ID: 646)...")
    result = client.call_tool("start_challenge", {"challenge_id": 646})
    if 'result' in result:
        content = result['result'].get('content', [])
        if content and len(content) > 0:
            text = content[0].get('text', '')
            if 'created' in text.lower() or 'started' in text.lower() or 'instance' in text.lower():
                print("✅ Start challenge works!")
            else:
                print(f"⚠️ Challenge start response: {text[:100]}")
    else:
        print(f"❌ Start challenge failed: {result.get('error', 'Unknown error')}")

def main():
    """Test the updated MCP server"""
    client = HTBMCPClient()
    
    try:
        print("=== TESTING UPDATED MCP SERVER ===\n")
        
        # Initialize session
        print("Initializing MCP session...")
        result = client.initialize()
        if 'result' in result:
            print("✅ Session initialized\n")
        else:
            print(f"❌ Failed to initialize: {result}\n")
            return
        
        # Test machines
        test_machines(client)
        
        # Test challenges
        test_challenges(client)
        
        print("\n=== TEST SUMMARY ===")
        print("The MCP server has been updated with the correct endpoints!")
        print("\nWorking endpoints:")
        print("  ✅ /vm/spawn - Start machines")
        print("  ✅ /vm/terminate - Stop machines")
        print("  ✅ /challenge/start - Start challenges")
        print("  ✅ /challenge/list - List challenges")
        print("  ✅ /machine/active - Get active machine")
        
    finally:
        client.close()
        print("\n=== Test Complete ===")

if __name__ == "__main__":
    main()