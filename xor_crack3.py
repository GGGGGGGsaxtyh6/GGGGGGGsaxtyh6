#!/usr/bin/env python3
from collections import Counter

def xor_decrypt(data, key):
    if isinstance(key, str):
        key = key.encode()
    result = bytearray(len(data))
    keylen = len(key)
    for i in range(len(data)):
        result[i] = data[i] ^ key[i % keylen]
    return bytes(result)

def score_text(data):
    score = 0
    for b in data[:min(len(data), 2000)]:
        if b == 32 or (97 <= b <= 122) or (65 <= b <= 90):  # espacio y letras
            score += 2
        elif 48 <= b <= 57:  # números
            score += 1
        elif 32 <= b <= 126 or b in [9, 10, 13]:
            score += 0.5
        else:
            score -= 3
    return score

def find_key_for_position(data, keylen, pos):
    block = bytearray()
    for j in range(pos, len(data), keylen):
        block.append(data[j])
    
    best_score = -999999
    best_key = 0
    for key in range(256):
        decrypted = bytes([b ^ key for b in block])
        s = score_text(decrypted)
        if s > best_score:
            best_score = s
            best_key = key
    return best_key

# Leer archivo
with open('/workspace/exclusive_key', 'rb') as f:
    data = f.read()

print(f"Tamaño: {len(data)} bytes\n")

# Probar longitudes específicas más probables
test_keylens = [1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 14, 16, 20, 24, 32]

results = []

for keylen in test_keylens:
    print(f"Probando keylen={keylen}...", end=' ')
    key = bytearray()
    for i in range(keylen):
        key.append(find_key_for_position(data, keylen, i))
    
    decrypted = xor_decrypt(data, bytes(key))
    score = score_text(decrypted)
    results.append((score, keylen, bytes(key), decrypted))
    print(f"score={score:.0f}")

# Ordenar por score
results.sort(reverse=True)

# Mostrar los mejores 3
for i, (score, keylen, key, decrypted) in enumerate(results[:3]):
    print(f"\n{'='*60}")
    print(f"#{i+1} - Keylen={keylen}, Score={score:.0f}")
    print(f"Key (hex): {key.hex()}")
    print(f"Key (ascii): {key}")
    print(f"\nPrimeros 300 bytes:")
    print(decrypted[:300])
    
    with open(f'/workspace/result_{i}.txt', 'wb') as f:
        f.write(decrypted)

print(f"\nResultados guardados en result_0.txt, result_1.txt, result_2.txt")
