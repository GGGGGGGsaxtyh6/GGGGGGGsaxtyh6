#!/usr/bin/env python3
"""
Start Previous machine on HackTheBox
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

def main():
    """Start Previous machine"""
    client = HTBMCPClient()
    
    try:
        print("=== Starting Previous Machine (ID: 701) ===\n")
        
        # Initialize session
        print("Initializing MCP session...")
        result = client.initialize()
        if 'result' in result:
            print("✓ Session initialized\n")
        else:
            print(f"✗ Failed to initialize: {result}\n")
            return
        
        # Start the machine
        print("Starting Previous machine...")
        start_result = client.call_tool("start_machine", {
            "machine_id": 701
        })
        
        if 'result' in start_result:
            result_data = start_result['result']
            if isinstance(result_data, dict) and 'content' in result_data:
                content = result_data['content']
                if isinstance(content, list) and len(content) > 0:
                    text = content[0].get('text', '')
                    print(f"\n{text}")
                    
                    # Try to extract IP if available
                    if "successfully" in text.lower() or "started" in text.lower():
                        print("\n✓ Machine started successfully!")
                        
                        # Wait a moment and try to get the IP
                        print("\nWaiting for machine to fully initialize...")
                        time.sleep(5)
                        
                        # Get machine IP
                        print("Getting machine IP address...")
                        ip_result = client.call_tool("get_machine_ip", {})
                        
                        if 'result' in ip_result:
                            ip_data = ip_result['result']
                            if isinstance(ip_data, dict) and 'content' in ip_data:
                                ip_content = ip_data['content']
                                if isinstance(ip_content, list) and len(ip_content) > 0:
                                    ip_text = ip_content[0].get('text', '')
                                    print(f"\n{ip_text}")
                    else:
                        print(f"\nMachine status: {text}")
            else:
                print(f"Start result: {json.dumps(result_data, indent=2)}")
        else:
            error_msg = start_result.get('error', 'Unknown error')
            print(f"✗ Failed to start machine: {error_msg}")
            
            # If it's already running, try to get the IP
            if "already" in str(error_msg).lower():
                print("\nMachine might already be running. Checking IP...")
                ip_result = client.call_tool("get_machine_ip", {})
                
                if 'result' in ip_result:
                    ip_data = ip_result['result']
                    if isinstance(ip_data, dict) and 'content' in ip_data:
                        ip_content = ip_data['content']
                        if isinstance(ip_content, list) and len(ip_content) > 0:
                            ip_text = ip_content[0].get('text', '')
                            print(f"\n{ip_text}")
            
    finally:
        client.close()
        print("\n=== Done ===")

if __name__ == "__main__":
    main()