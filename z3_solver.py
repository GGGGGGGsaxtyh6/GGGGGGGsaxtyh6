#!/usr/bin/env python3
from z3 import *
import struct
import subprocess

print("=== Z3 SOLVER PARA TINY VM ===")

# Cargar expected output
expected_output = [129, 162, 253, 190, 189, 69, 44, 25, 242, 51, 201, 199, 165, 240, 188, 73, 222, 136, 182, 219, 17, 206, 31, 35, 252, 185]

# Crear variables Z3 para cada carácter de la flag
flag_chars = [BitVec(f'flag_{i}', 8) for i in range(26)]

# Crear solver
s = Solver()

# Restricción: formato ictf{...}
s.add(flag_chars[0] == ord('i'))
s.add(flag_chars[1] == ord('c'))
s.add(flag_chars[2] == ord('t'))
s.add(flag_chars[3] == ord('f'))
s.add(flag_chars[4] == ord('{'))
s.add(flag_chars[25] == ord('}'))

# Restricción: caracteres imprimibles (ASCII 32-126)
for i in range(5, 25):
    s.add(And(flag_chars[i] >= 32, flag_chars[i] <= 126))

# Basado en el análisis del bytecode, parece que la operación es:
# output[i] = (flag[i] ^ key[i % len(key)]) para alguna clave

# Probar con la clave "tinyVMkey!" que encontramos
key = b'tinyVMkey!'
extended_key = (key * 3)[:26]

print(f"Clave extendida: {extended_key}")
print(f"Output esperado: {bytes(expected_output)}")

# Agregar restricciones basadas en XOR
for i in range(26):
    s.add(flag_chars[i] ^ extended_key[i] == expected_output[i])

print("\nResolviendo con Z3...")
if s.check() == sat:
    model = s.model()
    flag = ''.join([chr(model[flag_chars[i]].as_long()) for i in range(26)])
    print(f"\n🎉 FLAG ENCONTRADA POR Z3: {flag} 🎉\n")
    
    # Verificar con el binario
    with open('/tmp/test.txt', 'w') as f:
        f.write(flag)
    proc = subprocess.run(['./tiny_vm'], stdin=open('/tmp/test.txt'), 
                        capture_output=True, text=True, timeout=2)
    
    if "Correct" in proc.stdout:
        print(f"✓ VERIFICADO CON EL BINARIO!")
        with open('/workspace/FLAG.txt', 'w') as f:
            f.write(flag)
    else:
        print(f"✗ No verificó con el binario. Output: {proc.stdout}")
        print("Intentando con operaciones diferentes...")
else:
    print("✗ No se encontró solución con XOR simple")
    
# Si no funcionó con XOR, probar otras operaciones
print("\nProbando con ADD...")
s2 = Solver()
flag_chars2 = [BitVec(f'flag2_{i}', 8) for i in range(26)]

s2.add(flag_chars2[0] == ord('i'))
s2.add(flag_chars2[1] == ord('c'))
s2.add(flag_chars2[2] == ord('t'))
s2.add(flag_chars2[3] == ord('f'))
s2.add(flag_chars2[4] == ord('{'))
s2.add(flag_chars2[25] == ord('}'))

for i in range(5, 25):
    s2.add(And(flag_chars2[i] >= 32, flag_chars2[i] <= 126))

for i in range(26):
    s2.add((flag_chars2[i] + extended_key[i]) & 0xFF == expected_output[i])

if s2.check() == sat:
    model = s2.model()
    flag = ''.join([chr(model[flag_chars2[i]].as_long()) for i in range(26)])
    print(f"\n🎉 FLAG ENCONTRADA (ADD): {flag} 🎉\n")
    
    with open('/tmp/test.txt', 'w') as f:
        f.write(flag)
    proc = subprocess.run(['./tiny_vm'], stdin=open('/tmp/test.txt'), 
                        capture_output=True, text=True, timeout=2)
    
    if "Correct" in proc.stdout:
        print(f"✓ VERIFICADO!")
        with open('/workspace/FLAG.txt', 'w') as f:
            f.write(flag)
        exit(0)

print("\n⚠️ Z3 no encontró solución directa. El algoritmo debe ser más complejo.")
