#!/usr/bin/env python3

def enc(val, key):
    for i in range(32):
        val = (key + (val ^ key)) % 256
    return val

# Encontrar claves de identidad
identity_keys = []
for key in range(256):
    is_identity = True
    for val in range(256):
        if enc(val, key) != val:
            is_identity = False
            break
    if is_identity:
        identity_keys.append(key)

print(f"Claves de identidad ({len(identity_keys)}):")
for key in identity_keys:
    print(f"{key:3d} = {key:08b}")

print("\nClaves NO de identidad:")
non_identity_keys = [k for k in range(256) if k not in identity_keys]
for key in non_identity_keys[:20]:
    print(f"{key:3d} = {key:08b}")

# Analizar patrón
print("\nAnalizando patrón de bits en claves de identidad:")
# Ver qué posiciones de bits están siempre en 0 o 1
for bit_pos in range(8):
    bit_values = [((key >> bit_pos) & 1) for key in identity_keys]
    print(f"Bit {bit_pos}: {sum(bit_values)} unos, {len(bit_values) - sum(bit_values)} ceros")
