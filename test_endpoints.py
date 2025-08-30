#!/usr/bin/env python3
"""
Test HTB API endpoints to find the correct ones
"""

import json
import subprocess
import time

# Get token
with open('/workspace/htb-mcp-server/.env', 'r') as f:
    for line in f:
        if line.startswith('HTB_TOKEN='):
            token = line.strip().split('=', 1)[1]
            break

def test_endpoint(method, endpoint, data=None):
    """Test an API endpoint"""
    if method == "GET":
        cmd = f'curl -s -H "Authorization: Bearer {token}" -H "Accept: application/json" "{endpoint}"'
    else:
        data_str = json.dumps(data) if data else "{}"
        cmd = f'curl -s -X {method} -H "Authorization: Bearer {token}" -H "Accept: application/json" -H "Content-Type: application/json" "{endpoint}" -d \'{data_str}\''
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    try:
        response = json.loads(result.stdout)
        return response
    except:
        return {"raw": result.stdout}

print("=== Testing HTB API Endpoints ===\n")

# Base URL
base = "https://labs.hackthebox.com/api/v4"

# Test endpoints
endpoints_to_test = [
    # User endpoints
    ("GET", f"{base}/user/info", "User Info"),
    ("GET", f"{base}/user/profile", "User Profile"),
    
    # Machine endpoints
    ("GET", f"{base}/machine/list", "Machine List"),
    ("GET", f"{base}/machine/active", "Active Machine"),
    ("POST", f"{base}/vm/spawn", "Spawn Machine (vm/spawn)"),
    ("POST", f"{base}/machine/spawn", "Spawn Machine (machine/spawn)"),
    
    # Challenge endpoints  
    ("GET", f"{base}/challenge/list", "Challenge List"),
    ("GET", f"{base}/challenge/list/retired", "Retired Challenges"),
    ("GET", f"{base}/challenge/active", "Active Challenge"),
    ("POST", f"{base}/challenge/spawn", "Spawn Challenge"),
    ("POST", f"{base}/challenge/start", "Start Challenge"),
    
    # New possible endpoints
    ("GET", f"{base}/challenges", "Challenges (plural)"),
    ("GET", f"{base}/machines", "Machines (plural)"),
    ("POST", f"{base}/vm/terminate", "Terminate VM"),
]

working_endpoints = []

for method, endpoint, description in endpoints_to_test:
    print(f"Testing: {description}")
    print(f"  {method} {endpoint}")
    
    if "spawn" in endpoint and method == "POST":
        # For spawn endpoints, include machine_id
        response = test_endpoint(method, endpoint, {"machine_id": 701})
    else:
        response = test_endpoint(method, endpoint)
    
    if response:
        if "message" in response and "not found" in response.get("message", "").lower():
            print(f"  ❌ Not found")
        elif "raw" in response:
            print(f"  ⚠️  Non-JSON response: {response['raw'][:50]}...")
        else:
            print(f"  ✅ Working!")
            working_endpoints.append((method, endpoint, description))
            # Show sample of response
            resp_str = json.dumps(response, indent=2)[:200]
            print(f"     Response: {resp_str}...")
    else:
        print(f"  ❌ No response")
    
    print()
    time.sleep(0.5)  # Be nice to the API

print("\n=== WORKING ENDPOINTS ===")
for method, endpoint, desc in working_endpoints:
    print(f"✅ {desc}: {method} {endpoint}")