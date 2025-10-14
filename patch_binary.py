import struct

# Leer el binario
with open('umapyoi', 'rb') as f:
    data = bytearray(f.read())

# Offset de las llamadas a a1() y a2() en main
# 0x00001273: call a1()
# 0x00001278: call a2()
# Vamos a reemplazar estas llamadas con NOPs (0x90)

# Primero encontrar el offset en el archivo
# Las direcciones son relativas, necesito encontrar el offset real en el archivo

# Cambiar call a1() por NOPs
# e8 f1 fe ff ff = call -271 (a1)
offset_call_a1 = 0x1273
offset_call_a2 = 0x1278

# Reemplazar con NOPs (5 bytes cada uno)
for i in range(5):
    data[offset_call_a1 + i] = 0x90
    data[offset_call_a2 + i] = 0x90

# Escribir el binario modificado
with open('umapyoi_noloop', 'wb') as f:
    f.write(data)

print("Binario parcheado creado: umapyoi_noloop")
