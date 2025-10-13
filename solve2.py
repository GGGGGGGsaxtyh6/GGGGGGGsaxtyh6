#!/usr/bin/env python3
import requests
import string
import sys

URL = "https://e9a470dcc2070b45.247ctf.com/encrypt"
BLOCK_SIZE = 16

def encrypt(plaintext_bytes):
    """Envía plaintext en hex y recibe el cifrado"""
    plaintext_hex = plaintext_bytes.hex()
    r = requests.get(URL, params={'plaintext': plaintext_hex}, timeout=10)
    return r.text.strip()

print("[*] Probando conexión...")
sys.stdout.flush()
test = encrypt(b'A')
print(f"[+] Conexión OK: {test[:32]}...")
sys.stdout.flush()

# Ataque byte por byte
flag = b''
print("[*] Iniciando ataque...")
sys.stdout.flush()

# Caracteres posibles - primero los más comunes en flags, luego todos
charset_common = b'247CTF{}_abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()-=+ABCDEFGHIJKLMNOPQRSTUVWXYZ'
charset_all = bytes(range(256))

for i in range(80):
    print(f"[*] Buscando byte {i}...", end='', flush=True)
    
    # Padding: necesitamos BLOCK_SIZE - 1 - (i % BLOCK_SIZE) bytes
    # para que el byte i de la flag esté al final de un bloque
    padding_length = BLOCK_SIZE - 1 - (i % BLOCK_SIZE)
    padding = b'A' * padding_length
    
    # Cifrado objetivo: padding + flag (sin conocer el siguiente byte)
    target_cipher = encrypt(padding)
    
    # El bloque que contiene el byte i
    block_num = (padding_length + i) // BLOCK_SIZE
    target_block = target_cipher[block_num * 32:(block_num + 1) * 32]
    
    # Probar cada carácter - primero comunes, luego todos
    found = False
    for c in charset_common:
        # Construir: padding + flag_conocida + byte_candidato
        test_input = padding + flag + bytes([c])
        test_cipher = encrypt(test_input)
        test_block = test_cipher[block_num * 32:(block_num + 1) * 32]
        
        if test_block == target_block:
            flag += bytes([c])
            flag_str = flag.decode('utf-8', errors='ignore')
            print(f" {chr(c) if 32 <= c < 127 else f'0x{c:02x}'} -> {flag_str}")
            sys.stdout.flush()
            found = True
            
            if c == ord('}'):
                print(f"\n[!] FLAG: {flag_str}")
                sys.exit(0)
            break
    
    # Si no se encontró en comunes, probar todos
    if not found:
        for c in charset_all:
            if c in charset_common:
                continue
            test_input = padding + flag + bytes([c])
            test_cipher = encrypt(test_input)
            test_block = test_cipher[block_num * 32:(block_num + 1) * 32]
            
            if test_block == target_block:
                flag += bytes([c])
                flag_str = flag.decode('utf-8', errors='ignore')
                print(f" 0x{c:02x} -> {flag_str}")
                sys.stdout.flush()
                found = True
                break
    
    if not found:
        print(f" NO ENCONTRADO")
        print(f"[*] Flag parcial: {flag}")
        break

print(f"\n[*] Flag final: {flag.decode('utf-8', errors='ignore')}")
