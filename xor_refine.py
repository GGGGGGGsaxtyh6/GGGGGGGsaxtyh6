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

# Basándonos en el análisis anterior, sabemos que es HTML
# Los primeros bytes deberían ser algo como "<!DOCTYPE" o "<html"
# Vamos a refinar la clave asumiendo patrones HTML comunes

# Probar con keylen=20 que fue el mejor
keylen = 20

# Empezar con la clave anterior como base
current_key = bytearray.fromhex('3534651b7e1f7b3663616563323162623e343436')

# Intentar refinar posición por posición buscando patrones comunes
# Sabemos que los documentos HTML suelen empezar con "<!DOCTYPE html>" o "<html"

# Intentemos con diferentes hipótesis de plaintext
plaintexts = [
    b'<!DOCTYPE html>',
    b'<html lang="en">',
    b'<!doctype html>',
]

for pt in plaintexts:
    print(f"\nProbando plaintext: {pt}")
    test_key = bytearray(current_key)
    
    # Refinar clave basándonos en este plaintext
    for i in range(min(len(pt), len(data))):
        test_key[i % keylen] = data[i] ^ pt[i]
    
    decrypted = xor_decrypt(data, bytes(test_key))
    print(f"Clave: {bytes(test_key)}")
    print(f"Primeros 200 bytes: {decrypted[:200]}")
    
    # Verificar si se ve bien
    if decrypted[:10].decode('ascii', errors='ignore').isprintable():
        with open(f'/workspace/refined_{pt[:5].hex()}.txt', 'wb') as f:
            f.write(decrypted)

# También probar asumiendo que hay texto común en diferentes posiciones
# Por ejemplo, buscar donde aparece "Wikipedia" en el archivo cifrado
common_words = [b'Wikipedia', b'article', b'<!DOCTYPE', b'<html>', b'<title>', b'<script>']

print("\n" + "="*60)
print("Buscando palabras comunes en diferentes posiciones...")

# Intentar keylen diferente basándose en el patrón
# Si vemos "tml c" probablemente sea "html " 
# Posición 11-15: "tml c" debería ser "html>"

test_positions = [
    (11, b'html>'),  # basado en lo que vimos
    (40, b'<title>'),
    (0, b'<!DOCTYPE'),
]

best_key = bytearray(current_key)

for pos, expected in test_positions:
    if pos + len(expected) <= len(data):
        for i, byte in enumerate(expected):
            key_pos = (pos + i) % keylen
            best_key[key_pos] = data[pos + i] ^ byte

print(f"\nClave refinada: {bytes(best_key)}")
print(f"Clave refinada (hex): {best_key.hex()}")

decrypted = xor_decrypt(data, bytes(best_key))
print(f"\nPrimeros 500 bytes:")
print(decrypted[:500])

with open('/workspace/refined_result.txt', 'wb') as f:
    f.write(decrypted)

print("\nGuardado en refined_result.txt")

# Buscar la flag
if b'picoCTF{' in decrypted:
    idx = decrypted.index(b'picoCTF{')
    flag_section = decrypted[idx:idx+100]
    print(f"\n{'='*60}")
    print("FLAG ENCONTRADA:")
    print(flag_section.decode('ascii', errors='ignore'))
