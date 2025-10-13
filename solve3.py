#!/usr/bin/env python3
import requests
import concurrent.futures
import sys

URL = "https://e9a470dcc2070b45.247ctf.com/encrypt"
BLOCK_SIZE = 16

def encrypt(plaintext_bytes):
    """Envía plaintext en hex y recibe el cifrado"""
    plaintext_hex = plaintext_bytes.hex()
    r = requests.get(URL, params={'plaintext': plaintext_hex}, timeout=10)
    return r.text.strip()

def try_char(args):
    """Intenta un carácter específico"""
    c, test_input, block_num = args
    try:
        test_cipher = encrypt(test_input)
        test_block = test_cipher[block_num * 32:(block_num + 1) * 32]
        return (c, test_block)
    except:
        return (c, None)

print("[*] Iniciando ataque paralelo...")
sys.stdout.flush()

flag = b''
charset = b'247CTF{}_abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()-=+ABCDEFGHIJKLMNOPQRSTUVWXYZ'
charset_all = bytes(range(256))

for i in range(80):
    print(f"[*] Byte {i}...", end='', flush=True)
    
    padding_length = BLOCK_SIZE - 1 - (i % BLOCK_SIZE)
    padding = b'A' * padding_length
    
    target_cipher = encrypt(padding)
    block_num = (padding_length + i) // BLOCK_SIZE
    target_block = target_cipher[block_num * 32:(block_num + 1) * 32]
    
    # Preparar argumentos para threading
    args_list = []
    for c in charset:
        test_input = padding + flag + bytes([c])
        args_list.append((c, test_input, block_num))
    
    # Probar en paralelo
    found = False
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        for c, test_block in executor.map(try_char, args_list):
            if test_block and test_block == target_block:
                flag += bytes([c])
                print(f" {chr(c)} -> {flag.decode('utf-8', errors='ignore')}")
                sys.stdout.flush()
                found = True
                
                if c == ord('}'):
                    print(f"\n[!] FLAG: {flag.decode('utf-8', errors='ignore')}")
                    sys.exit(0)
                break
    
    if found:
        continue
    
    # Si no se encontró en charset común, probar todos
    args_list = []
    for c in charset_all:
        if c not in charset:
            test_input = padding + flag + bytes([c])
            args_list.append((c, test_input, block_num))
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        for c, test_block in executor.map(try_char, args_list):
            if test_block and test_block == target_block:
                flag += bytes([c])
                print(f" 0x{c:02x} -> {flag.decode('utf-8', errors='ignore')}")
                sys.stdout.flush()
                found = True
                break
    
    if not found:
        print(f" NO ENCONTRADO")
        print(f"[*] Flag parcial: {flag}")
        break

print(f"\n[*] Flag final: {flag.decode('utf-8', errors='ignore')}")
