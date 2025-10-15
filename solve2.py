#!/usr/bin/env python3

def enc(val, key):
    for i in range(32):
        val = (key + (val ^ key)) % 256
    return val

# Output dado
output = b'\xe9c\xb4&{t\xa4\x84\xb1.g+\xedp2\xe5_o\xb032\xe1\x94\xc9o.\xb5>\xb1s\x0e\x94_\xe1\xacw\xc1\xf9S_s\xb4\x12p.g\xc52\xfd'

# Crear mapas inversos para todas las claves posibles
inv_maps = {}
for key in range(256):
    inv_map = {}
    for val in range(256):
        encrypted = enc(val, key)
        inv_map[encrypted] = val
    inv_maps[key] = inv_map

# Claves de identidad
identity_keys = set()
for key in range(256):
    is_identity = True
    for val in range(256):
        if enc(val, key) != val:
            is_identity = False
            break
    if is_identity:
        identity_keys.add(key)

print(f"Claves de identidad: {len(identity_keys)} de 256\n")

# Intentar descifrar asumiendo que hay solo 1 o 2 claves no-identidad
# y que se aplicaron en cualquier orden

non_identity_keys = [k for k in range(256) if k not in identity_keys]

print("Probando con una sola clave no-identidad aplicada múltiples veces...")
for key1 in non_identity_keys:
    decrypted = [inv_maps[key1][b] for b in output]
    decrypted_bytes = bytes(decrypted)
    
    if b"ictf{" in decrypted_bytes or b"ICTF{" in decrypted_bytes:
        print(f"Clave {key1}: {decrypted_bytes}")
    
    # También probar aplicar la inversa múltiples veces
    for iterations in [2, 3, 4, 5, 10, 50, 100, 255, 256]:
        temp = list(output)
        for _ in range(iterations):
            temp = [inv_maps[key1][b] for b in temp]
        decrypted_bytes = bytes(temp)
        
        if b"ictf{" in decrypted_bytes or b"ICTF{" in decrypted_bytes:
            print(f"Clave {key1} ({iterations} iteraciones): {decrypted_bytes}")

print("\nProbando con dos claves no-identidad...")
for i, key1 in enumerate(non_identity_keys[:10]):  # Limitar para no tardar demasiado
    for key2 in non_identity_keys[:10]:
        # Descifrar primero con key2, luego con key1
        temp = [inv_maps[key2][b] for b in output]
        decrypted = [inv_maps[key1][b] for b in temp]
        decrypted_bytes = bytes(decrypted)
        
        if b"ictf{" in decrypted_bytes or b"ICTF{" in decrypted_bytes:
            print(f"Claves {key1}, {key2}: {decrypted_bytes}")
