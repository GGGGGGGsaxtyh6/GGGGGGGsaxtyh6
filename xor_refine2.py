#!/usr/bin/env python3

def xor_decrypt(data, key):
    if isinstance(key, str):
        key = key.encode()
    result = bytearray(len(data))
    keylen = len(key)
    for i in range(len(data)):
        result[i] = data[i] ^ key[i % keylen]
    return bytes(result)

# Leer archivo
with open('/workspace/exclusive_key', 'rb') as f:
    data = f.read()

# Vamos a asumir HTML bien formado y refinar la clave posición por posición
keylen = 20

# Patrones HTML conocidos en posiciones específicas
# Basándonos en el output anterior, vamos a refinar

known_patterns = [
    (0, b'<!DOCTYPE html>'),
    (16, b'\n<html lang="en" dir="ltr">'),
    (44, b'\n<head>'),
    (51, b'\n<meta charset="UTF-8"/>'),
]

# Inicializar clave
key = bytearray([0] * keylen)
key_confidence = [0] * keylen  # cuántas veces hemos visto cada byte de la clave

for pos, pattern in known_patterns:
    for i, expected_byte in enumerate(pattern):
        if pos + i < len(data):
            key_idx = (pos + i) % keylen
            inferred_key_byte = data[pos + i] ^ expected_byte
            
            # Si ya tenemos un valor para esta posición de la clave, verificamos consistencia
            if key_confidence[key_idx] == 0:
                key[key_idx] = inferred_key_byte
                key_confidence[key_idx] = 1
            elif key[key_idx] != inferred_key_byte:
                # Conflicto - mantener el que tengamos más confianza
                pass

print("Clave inferida de patrones conocidos:")
print(f"Hex: {key.hex()}")
print(f"ASCII: {bytes(key)}")
print(f"Confianza por posición: {key_confidence}")

decrypted = xor_decrypt(data, bytes(key))
print(f"\nPrimeros 300 bytes descifrados:")
print(decrypted[:300])

# Ahora vamos a refinar más mirando el resultado
# y buscando palabras comunes que estén casi correctas

# Miremos más patrones en el resultado
sample = decrypted[:500].decode('ascii', errors='ignore')
print(f"\nSample (primeros 500 chars):")
print(sample)

# Guardar
with open('/workspace/refined2_result.txt', 'wb') as f:
    f.write(decrypted)

# Buscar si la clave contiene la flag
print(f"\n{'='*60}")
print("Analizando la clave como posible flag...")
print(f"Clave: {bytes(key)}")

# La clave parece contener "247CTF{" basándome en el análisis anterior
# Vamos a probar diferentes refinamientos

# Probar asumiendo diferentes longitudes de clave también
for test_keylen in [20, 21, 19]:
    print(f"\n--- Probando keylen={test_keylen} ---")
    test_key = bytearray([0] * test_keylen)
    
    for pos, pattern in known_patterns:
        for i, expected_byte in enumerate(pattern):
            if pos + i < len(data):
                key_idx = (pos + i) % test_keylen
                test_key[key_idx] = data[pos + i] ^ expected_byte
    
    print(f"Clave: {bytes(test_key)}")
    
    test_decrypted = xor_decrypt(data, bytes(test_key))
    print(f"Primeros 150 bytes: {test_decrypted[:150]}")
