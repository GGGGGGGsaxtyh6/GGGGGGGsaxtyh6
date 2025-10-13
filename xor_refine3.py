#!/usr/bin/env python3

def xor_decrypt(data, key):
    if isinstance(key, str):
        key = key.encode()
    result = bytearray(len(data))
    keylen = len(key)
    for i in range(len(data)):
        result[i] = data[i] ^ key[i % keylen]
    return bytes(result)

def infer_key_from_patterns(data, keylen):
    """Inferir clave buscando patrones comunes en el texto descifrado"""
    key = [None] * keylen
    
    # Múltiples hipótesis de plaintext
    hypotheses = [
        (0, b'<!DOCTYPE html>\n<html'),
        (25, b' lang="en" dir="ltr">\n<head>\n<meta charset="UTF-8"/>\n<title>'),
        (100, b'</title>\n<script>'),
        (200, b'className'),
        (300, b'wgAction'),
        (400, b'wgArticle'),
        (500, b'wgCanonical'),
    ]
    
    votes = [{}] * keylen  # Votos para cada posición de la clave
    for i in range(keylen):
        votes[i] = {}
    
    for start_pos, plaintext in hypotheses:
        if start_pos + len(plaintext) <= len(data):
            for i, pt_byte in enumerate(plaintext):
                key_idx = (start_pos + i) % keylen
                inferred_byte = data[start_pos + i] ^ pt_byte
                
                if inferred_byte not in votes[key_idx]:
                    votes[key_idx][inferred_byte] = 0
                votes[key_idx][inferred_byte] += 1
    
    # Escoger el byte con más votos para cada posición
    for i in range(keylen):
        if votes[i]:
            key[i] = max(votes[i].items(), key=lambda x: x[1])[0]
        else:
            key[i] = 0
    
    return bytes(key)

# Leer archivo
with open('/workspace/exclusive_key', 'rb') as f:
    data = f.read()

# Probar diferentes longitudes de clave
for keylen in [20, 19, 21]:
    print(f"\n{'='*60}")
    print(f"Probando keylen={keylen}")
    
    key = infer_key_from_patterns(data, keylen)
    print(f"Clave (hex): {key.hex()}")
    print(f"Clave (ascii): {key}")
    
    decrypted = xor_decrypt(data, key)
    
    # Verificar qué tan bien se ve
    printable_count = sum(1 for b in decrypted[:500] if 32 <= b <= 126 or b in [9, 10, 13])
    print(f"Caracteres imprimibles en primeros 500: {printable_count}/500")
    
    print(f"\nPrimeros 300 bytes:")
    print(decrypted[:300])
    
    # Guardar
    with open(f'/workspace/result_keylen_{keylen}.html', 'wb') as f:
        f.write(decrypted)
    
    # Buscar flag
    if b'247CTF{' in decrypted:
        idx = decrypted.index(b'247CTF{')
        print(f"\n¡FLAG ENCONTRADA en el contenido!")
        print(decrypted[idx:idx+50])

print("\n" + "="*60)
print("ANÁLISIS DE LA CLAVE COMO PASSWORD:")
print("="*60)
print("La clave XOR es la contraseña que olvidaron!")
print(f"\nMejor clave encontrada (keylen=20):")
key20 = infer_key_from_patterns(data, 20)
print(f"ASCII: {key20}")
print(f"Hex: {key20.hex()}")
