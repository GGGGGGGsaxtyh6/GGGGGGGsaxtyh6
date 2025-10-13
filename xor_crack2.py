#!/usr/bin/env python3
import sys
from collections import Counter

def xor_decrypt(data, key):
    """Descifrar data con clave XOR"""
    if isinstance(key, str):
        key = key.encode()
    result = []
    for i, byte in enumerate(data):
        result.append(byte ^ key[i % len(key)])
    return bytes(result)

def score_text(data):
    """Score basado en caracteres ASCII imprimibles y comunes en inglés"""
    if len(data) == 0:
        return 0
    
    # Frecuencias comunes en inglés
    english_freq = {
        ord('e'): 12.70, ord('t'): 9.06, ord('a'): 8.17, ord('o'): 7.51,
        ord('i'): 6.97, ord('n'): 6.75, ord('s'): 6.33, ord('h'): 6.09,
        ord('r'): 5.99, ord(' '): 20.0, ord('E'): 12.70, ord('T'): 9.06,
        ord('A'): 8.17, ord('O'): 7.51, ord('I'): 6.97, ord('N'): 6.75
    }
    
    score = 0
    for b in data:
        if b in english_freq:
            score += english_freq[b]
        elif 32 <= b <= 126:
            score += 0.5
        elif b in [9, 10, 13]:  # tab, newline, carriage return
            score += 0.5
        else:
            score -= 2  # penalizar caracteres no imprimibles
    
    return score / len(data)

def find_single_byte_xor(data):
    """Encontrar la mejor clave de un byte para XOR"""
    best_score = -999999
    best_key = 0
    best_result = None
    
    for key in range(256):
        decrypted = bytes([b ^ key for b in data])
        score = score_text(decrypted)
        
        if score > best_score:
            best_score = score
            best_key = key
            best_result = decrypted
    
    return best_key, best_score, best_result

def break_repeating_key_xor_improved(data, keylen):
    """Romper XOR con clave repetida, versión mejorada"""
    key = []
    
    for i in range(keylen):
        # Extraer bytes en posición i, i+keylen, i+2*keylen, ...
        block = bytes([data[j] for j in range(i, len(data), keylen)])
        key_byte, score, _ = find_single_byte_xor(block)
        key.append(key_byte)
    
    return bytes(key)

# Leer archivo
with open('/workspace/exclusive_key', 'rb') as f:
    data = f.read()

print(f"Tamaño del archivo: {len(data)} bytes")

# Buscar magic bytes comunes XOReados
magic_bytes = [
    (b'\x89PNG', 'PNG'),
    (b'GIF8', 'GIF'),
    (b'\xFF\xD8\xFF', 'JPEG'),
    (b'PK\x03\x04', 'ZIP'),
    (b'%PDF', 'PDF'),
    (b'\x1f\x8b', 'GZIP'),
    (b'BM', 'BMP'),
    (b'<!DOCTYPE', 'HTML'),
    (b'<html', 'HTML'),
    (b'<?xml', 'XML'),
]

print("\nBuscando magic bytes XOReados en los primeros bytes...")
first_bytes = data[:10]
for magic, file_type in magic_bytes:
    for i in range(min(len(first_bytes), len(magic))):
        possible_key_byte = first_bytes[i] ^ magic[i]
        print(f"{file_type}: byte {i} sugiere clave[{i}] = 0x{possible_key_byte:02x} ({chr(possible_key_byte) if 32 <= possible_key_byte < 127 else '?'})")

# Probar longitudes de clave comunes con score mejorado
print("\n" + "="*60)
print("Probando longitudes de clave comunes con scoring mejorado...")

best_overall = None
best_overall_score = -999999

for keylen in range(1, 51):
    key = break_repeating_key_xor_improved(data, keylen)
    decrypted = xor_decrypt(data, key)
    score = score_text(decrypted[:1000])  # Score de los primeros 1000 bytes
    
    if score > best_overall_score:
        best_overall_score = score
        best_overall = (keylen, key, decrypted)
    
    if score > 0:  # Solo mostrar resultados prometedores
        print(f"\nLongitud: {keylen}, Score: {score:.2f}")
        print(f"Clave (hex): {key.hex()}")
        print(f"Clave (ascii): {key}")
        print(f"Primeros 150 bytes: {decrypted[:150]}")

if best_overall:
    keylen, key, decrypted = best_overall
    print("\n" + "="*60)
    print(f"MEJOR RESULTADO: Longitud {keylen}, Score: {best_overall_score:.2f}")
    print(f"Clave: {key}")
    print(f"Primeros 500 bytes:\n{decrypted[:500]}")
    
    with open('/workspace/best_decrypted.txt', 'wb') as f:
        f.write(decrypted)
    print("\nGuardado en best_decrypted.txt")
