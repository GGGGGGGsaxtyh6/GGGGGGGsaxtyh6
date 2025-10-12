#!/usr/bin/env python3
"""
¿Puedo llamar a los stored procedures directamente de alguna forma?
¿Hay algún endpoint MySQL expuesto?
"""
import requests
import socket

TARGET_HOST = "94.237.49.23"
TARGET_PORT = 45329

print("[*] Escaneando puertos cercanos...")
for port in [3306, 3307, 45330, 45328, 1337]:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    result = sock.connect_ex((TARGET_HOST, port))
    if result == 0:
        print(f"    [+] Puerto {port} ABIERTO")
    sock.close()

print("\n[*] Probando endpoints SQL...")
# Algunos frameworks exponen endpoints SQL
test_endpoints = [
    '/mysql',
    '/phpmyadmin',
    '/pma',
    '/db',
    '/database',
    '/sql',
    '/api/sql',
    '/api/query',
]

for endpoint in test_endpoints:
    resp = requests.get(f"http://{TARGET_HOST}:{TARGET_PORT}{endpoint}", timeout=5)
    if resp.status_code != 404:
        print(f"    [{resp.status_code}] {endpoint}")
