#!/usr/bin/env python3

def enc(val, key):
    for i in range(32):
        val = (key + (val ^ key)) % 256
    return val

# Output dado
output = b'\xe9c\xb4&{t\xa4\x84\xb1.g+\xedp2\xe5_o\xb032\xe1\x94\xc9o.\xb5>\xb1s\x0e\x94_\xe1\xacw\xc1\xf9S_s\xb4\x12p.g\xc52\xfd'

# Crear mapas inversos para todas las claves posibles
print("Creando mapas inversos...")
inv_maps = {}
for key in range(256):
    inv_map = {}
    for val in range(256):
        encrypted = enc(val, key)
        inv_map[encrypted] = val
    inv_maps[key] = inv_map

print("Mapas inversos creados.")
print()

# Ahora intentemos descifrar usando texto plano conocido
# Sabemos que la flag comienza con "ictf{"
known_prefix = b"ictf{"

print(f"Intentando descifrar con prefijo conocido: {known_prefix}")
print(f"Longitud del output: {len(output)}")
print()

# Para el primer byte, necesitamos encontrar qué clave se usó en key[0]
# tal que enc(ord('i'), key[0]) resulte en algo que después de aplicar
# todas las otras claves, llegue a output[0]

# Esto es complejo, así que voy a intentar algo diferente
# Voy a asumir que muchas de las claves son claves de identidad

# Veamos qué claves son de identidad
identity_keys = set()
for key in range(256):
    is_identity = True
    for val in range(256):
        if enc(val, key) != val:
            is_identity = False
            break
    if is_identity:
        identity_keys.add(key)

print(f"Claves de identidad: {len(identity_keys)} de 256")
print()

# Si la mayoría de las claves son de identidad, entonces el cifrado
# es más simple de lo que parece. Intentemos descifrar asumiendo
# que todas las claves excepto algunas son de identidad.

# Probemos descifrar directamente con diferentes claves
print("Probando descifrado con una sola clave no-identidad...")
for possible_key in range(256):
    if possible_key in identity_keys:
        continue
    
    decrypted = bytes([inv_maps[possible_key][b] for b in output])
    
    # Verificar si tiene sentido (ASCII imprimible)
    if all(32 <= b < 127 for b in decrypted[:10]):
        print(f"Clave {possible_key}: {decrypted[:20]}")
        if b"ictf{" in decrypted:
            print(f"POSIBLE FLAG: {decrypted}")
            print()
