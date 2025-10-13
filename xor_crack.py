#!/usr/bin/env python3
import sys
from collections import Counter
import string

def hamming_distance(b1, b2):
    """Calcular distancia de Hamming entre dos bytes"""
    return bin(b1 ^ b2).count('1')

def find_key_length(data, max_keylen=40):
    """Encontrar la longitud probable de la clave XOR"""
    distances = {}
    
    for keylen in range(2, max_keylen + 1):
        # Tomar varios bloques y calcular distancia promedio
        blocks = []
        for i in range(0, min(keylen * 8, len(data)), keylen):
            if i + keylen <= len(data):
                blocks.append(data[i:i+keylen])
        
        if len(blocks) < 2:
            continue
            
        # Calcular distancia promedio entre bloques consecutivos
        total_dist = 0
        comparisons = 0
        for i in range(len(blocks) - 1):
            dist = sum(hamming_distance(blocks[i][j], blocks[i+1][j]) 
                      for j in range(len(blocks[i])))
            total_dist += dist / keylen  # Normalizar por longitud
            comparisons += 1
        
        if comparisons > 0:
            distances[keylen] = total_dist / comparisons
    
    # Ordenar por menor distancia
    sorted_keylens = sorted(distances.items(), key=lambda x: x[1])
    return [k for k, v in sorted_keylens[:10]]

def frequency_analysis(data):
    """Análisis de frecuencia simple"""
    counter = Counter(data)
    return counter.most_common(10)

def find_xor_key_byte(data_bytes):
    """Encontrar el byte de clave XOR más probable para un conjunto de bytes"""
    # Asumiendo que el texto plano es principalmente ASCII imprimible o tiene espacios
    best_score = -1
    best_key = 0
    
    for key_byte in range(256):
        decrypted = bytes([b ^ key_byte for b in data_bytes])
        # Calcular score basado en caracteres ASCII imprimibles
        score = sum(1 for b in decrypted if 32 <= b <= 126 or b in [9, 10, 13])
        
        if score > best_score:
            best_score = score
            best_key = key_byte
    
    return best_key

def break_repeating_key_xor(data, keylen):
    """Romper XOR con clave repetida de longitud conocida"""
    key = []
    
    for i in range(keylen):
        # Extraer bytes en posición i, i+keylen, i+2*keylen, ...
        block = bytes([data[j] for j in range(i, len(data), keylen)])
        key_byte = find_xor_key_byte(block)
        key.append(key_byte)
    
    return bytes(key)

def xor_decrypt(data, key):
    """Descifrar data con clave XOR"""
    result = []
    for i, byte in enumerate(data):
        result.append(byte ^ key[i % len(key)])
    return bytes(result)

# Leer archivo
with open('/workspace/exclusive_key', 'rb') as f:
    data = f.read()

print(f"Tamaño del archivo: {len(data)} bytes")
print("\nAnalizando frecuencias de bytes...")
freqs = frequency_analysis(data)
print("Bytes más comunes:", freqs[:5])

print("\nBuscando longitud de clave...")
probable_keylens = find_key_length(data, max_keylen=50)
print(f"Longitudes de clave más probables: {probable_keylens[:5]}")

# Probar con las longitudes más probables
for keylen in probable_keylens[:5]:
    print(f"\n{'='*60}")
    print(f"Probando con longitud de clave: {keylen}")
    key = break_repeating_key_xor(data, keylen)
    print(f"Clave encontrada (hex): {key.hex()}")
    print(f"Clave encontrada (ascii): {key}")
    
    decrypted = xor_decrypt(data, key)
    
    # Mostrar primeros 200 bytes
    print(f"\nPrimeros 200 bytes descifrados:")
    print(decrypted[:200])
    print()
    
    # Buscar "flag" o "picoCTF" en el resultado
    if b'flag' in decrypted.lower() or b'pico' in decrypted.lower() or b'CTF' in decrypted:
        print("¡Posible flag encontrada!")
        # Guardar resultado completo
        with open(f'/workspace/decrypted_keylen_{keylen}.txt', 'wb') as f:
            f.write(decrypted)
        print(f"Guardado en decrypted_keylen_{keylen}.txt")
