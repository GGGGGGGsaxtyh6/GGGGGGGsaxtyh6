#!/usr/bin/env python3
import string

def xor_decrypt(data, key):
    if isinstance(key, str):
        key = key.encode()
    result = bytearray(len(data))
    keylen = len(key)
    for i in range(len(data)):
        result[i] = data[i] ^ key[i % keylen]
    return bytes(result)

def try_all_printable_for_position(data, keylen, pos):
    """Probar todos los caracteres imprimibles para una posición de la clave"""
    scores = {}
    
    for test_byte in range(32, 127):  # Solo caracteres imprimibles ASCII
        # Descifrar todos los bytes en esa posición
        decrypted_bytes = []
        for i in range(pos, len(data), keylen):
            decrypted_bytes.append(data[i] ^ test_byte)
        
        # Score: contar cuántos son caracteres válidos de texto
        score = 0
        for b in decrypted_bytes:
            if 32 <= b <= 126 or b in [9, 10, 13]:
                score += 1
        
        scores[test_byte] = score
    
    return max(scores.items(), key=lambda x: x[1])

# Leer archivo
with open('/workspace/exclusive_key', 'rb') as f:
    data = f.read()

print("Buscando la clave asumiendo que es completamente ASCII imprimible...")
print("(Es una 'password', así que probablemente sea legible)\n")

# Probar varias longitudes
for keylen in [19, 20, 21, 22]:
    print(f"{'='*60}")
    print(f"Probando keylen = {keylen}")
    
    key = bytearray()
    for pos in range(keylen):
        best_byte, score = try_all_printable_for_position(data, keylen, pos)
        key.append(best_byte)
        print(f"  Pos {pos:2d}: '{chr(best_byte)}' (0x{best_byte:02x}) - score: {score}/{len(data)//keylen}")
    
    print(f"\nClave completa: {bytes(key)}")
    print(f"Clave (hex): {key.hex()}")
    
    # Descifrar y verificar
    decrypted = xor_decrypt(data, bytes(key))
    
    # Contar caracteres imprimibles
    printable = sum(1 for b in decrypted[:1000] if 32 <= b <= 126 or b in [9, 10, 13])
    print(f"Caracteres imprimibles en primeros 1000: {printable}/1000")
    
    # Mostrar primeros bytes
    print(f"\nPrimeros 200 bytes del resultado:")
    print(decrypted[:200])
    
    # Guardar
    filename = f'/workspace/smart_result_keylen_{keylen}.html'
    with open(filename, 'wb') as f:
        f.write(decrypted)
    print(f"\nGuardado en {filename}")
    print()
