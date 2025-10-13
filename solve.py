#!/usr/bin/env python3
import requests
import string
import sys

URL = "https://e9a470dcc2070b45.247ctf.com/encrypt"
BLOCK_SIZE = 16

def encrypt(plaintext_bytes):
    """Envía plaintext en hex y recibe el cifrado"""
    try:
        plaintext_hex = plaintext_bytes.hex()
        r = requests.get(URL, params={'plaintext': plaintext_hex}, timeout=10)
        return r.text.strip()
    except Exception as e:
        print(f"[!] Error en encrypt: {e}", file=sys.stderr)
        return None

# Ataque: El servicio cifra (plaintext + flag) con padding
# Si controlamos plaintext, podemos descubrir la flag byte por byte
# Estrategia: enviar padding para alinear bloques y comparar

flag = b''
print("[*] Iniciando ataque byte por byte...")

# Caracteres posibles en la flag
charset = (string.ascii_letters + string.digits + string.punctuation + ' ').encode()

max_flag_length = 80

for i in range(max_flag_length):
    # Padding para alinear: necesitamos que el próximo byte de la flag
    # esté exactamente al final de un bloque
    # Si ya tenemos 'i' bytes de la flag descubiertos,
    # necesitamos (BLOCK_SIZE - 1 - i % BLOCK_SIZE) bytes de padding
    
    padding_length = BLOCK_SIZE - 1 - (i % BLOCK_SIZE)
    padding = b'A' * padding_length
    
    # Obtener cifrado objetivo (con el padding pero sin conocer el siguiente byte de flag)
    target_cipher = encrypt(padding)
    if not target_cipher:
        print("[-] Error de conexión")
        break
    
    # El bloque que contiene el byte que queremos descubrir
    block_num = (padding_length + i) // BLOCK_SIZE
    target_block = target_cipher[block_num * 32:(block_num + 1) * 32]
    
    # Probar cada carácter posible
    found = False
    for c in charset:
        # Construimos: padding + flag_conocida + byte_candidato
        test_input = padding + flag + bytes([c])
        test_cipher = encrypt(test_input)
        
        if test_cipher:
            test_block = test_cipher[block_num * 32:(block_num + 1) * 32]
            
            if test_block == target_block:
                flag += bytes([c])
                try:
                    flag_str = flag.decode('utf-8')
                except:
                    flag_str = flag.decode('latin-1')
                
                print(f"[+] Byte {i}: {chr(c)} -> {flag_str}")
                found = True
                
                # Si encontramos '}', probablemente hemos terminado
                if c == ord('}'):
                    print(f"\n[!] FLAG: {flag_str}")
                    exit(0)
                break
    
    if not found:
        print(f"[-] No se encontró el byte {i}")
        print(f"[*] Flag parcial: {flag}")
        break

print(f"\n[*] Flag final: {flag}")
