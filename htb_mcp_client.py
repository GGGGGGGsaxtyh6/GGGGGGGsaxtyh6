#!/usr/bin/env python3
"""
HTB MCP Client - Proper MCP protocol client for HackTheBox server
"""

import json
import subprocess
import sys
import os
from typing import Dict, Any, Optional, List

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
    
    def list_tools(self):
        """List available tools"""
        return self._send_request("tools/list")
    
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

def main():
    """Main function to interact with HTB"""
    client = HTBMCPClient()
    
    try:
        print("=== HTB MCP Client ===\n")
        
        # Initialize session
        print("Initializing MCP session...")
        result = client.initialize()
        if 'result' in result:
            print("✓ Session initialized\n")
        else:
            print(f"✗ Failed: {result}\n")
        
        # List available tools
        print("Available tools:")
        tools_response = client.list_tools()
        if 'result' in tools_response and 'tools' in tools_response['result']:
            for tool in tools_response['result']['tools']:
                print(f"  - {tool['name']}: {tool.get('description', 'No description')}")
        print()
        
        # Search for machines
        print("Searching for machines...")
        search_result = client.call_tool("search_content", {
            "query": "Distract Destroy",
            "type": "machine"
        })
        
        if 'result' in search_result:
            print(f"Search results: {json.dumps(search_result['result'], indent=2)}")
        else:
            print(f"Search failed: {search_result}")
        
        # List active machines
        print("\nListing machines...")
        machines_result = client.call_tool("list_machines", {
            "status": "active",
            "limit": 10
        })
        
        if 'result' in machines_result:
            result_data = machines_result['result']
            if isinstance(result_data, dict) and 'content' in result_data:
                content = result_data['content']
                if isinstance(content, list) and len(content) > 0:
                    # Parse the text content
                    text = content[0].get('text', '')
                    print(f"Machines:\n{text}")
                else:
                    print("No machines found")
            else:
                print(f"Result: {json.dumps(result_data, indent=2)}")
        else:
            print(f"Failed to list machines: {machines_result}")
        
        # Get user profile
        print("\nGetting user profile...")
        profile_result = client.call_tool("get_user_profile", {})
        
        if 'result' in profile_result:
            result_data = profile_result['result']
            if isinstance(result_data, dict) and 'content' in result_data:
                content = result_data['content']
                if isinstance(content, list) and len(content) > 0:
                    text = content[0].get('text', '')
                    print(f"User Profile:\n{text}")
            else:
                print(f"Profile: {json.dumps(result_data, indent=2)}")
        else:
            print(f"Failed to get profile: {profile_result}")
            
    finally:
        client.close()
        print("\nClient closed.")

if __name__ == "__main__":
    main()