#!/usr/bin/env python3

# Leer la matriz del output
with open('output.txt', 'r') as f:
    content = f.read()

# Parsear la matriz
import ast
matrix = ast.literal_eval(content)

n = len(matrix)
m = len(matrix[0])
print(f"Matriz: {n}x{m}")

# La primera fila contiene información sobre los bits de la flag
# En la matriz original:
# - Primera fila: [0, bit1, bit2, ..., bitn] donde bit es 1 o -1
# - Diagonal: 0
# - Resto: valores aleatorios 1 o 2

# Después de elevar a la potencia n-1, tenemos distancias min-plus
# La flag tiene (m-1) bits

# Analizar la primera fila de la salida
first_row = matrix[0]
print(f"Primera fila (primeros 20): {first_row[:20]}")
print(f"Valores únicos en primera fila: {sorted(set(first_row))}")

# La idea es que en la matriz original M, la primera fila es:
# [0, flag_bit_0, flag_bit_1, ..., flag_bit_{n-1}]
# donde flag_bit_i es 1 si el bit de la flag es 1, -1 si es 0

# Cuando elevamos M a la potencia (n-1), obtenemos información sobre
# los caminos más cortos de longitud (n-1)

# Necesitamos reconstruir la primera fila original
# Si observamos M^n[0][j], esto nos da el camino más corto de longitud n
# desde el nodo 0 al nodo j

# Vamos a analizar patrones
# Los valores en la salida son 1 o 2 mayormente
# Esto sugiere que los caminos más cortos tienen longitudes específicas

# Intentemos recuperar los bits de la flag
# La matriz original tiene estructura especial:
# - Fila 0: [0, b1, b2, ..., bn] donde bi es 1 o -1
# - Filas i>0: [valor, ..., 0, ...] con diagonal 0
# - Los demás valores son 1 o 2

# En álgebra tropical min-plus, el camino más corto de longitud k
# desde i hasta j usando la matriz M se calcula como M^k

# Para k = n-1 (donde n es el tamaño de la matriz),
# M^(n-1)[0][j] debe depender de la primera fila original

# Analicemos la segunda fila también para entender el patrón
second_row = matrix[1]
print(f"Segunda fila (primeros 20): {second_row[:20]}")
print(f"Valores únicos en segunda fila: {sorted(set(second_row))}")

# Dado que todos los valores en la salida son pequeños (1, 2),
# y la operación tropical es min(a+b, c+d, ...), 
# parece que los caminos óptimos tienen longitudes cortas

# Vamos a intentar una estrategia diferente:
# Simular el proceso inverso

# Primero, necesitamos entender qué valores en la primera fila
# corresponden a bits 1 vs bits -1 en la flag original

# Si observamos cuidadosamente, en la matriz de salida M^n,
# los valores en la primera fila deberían revelar información sobre
# la estructura original

# Analicemos todos los valores de la primera fila
from collections import Counter
counter = Counter(first_row)
print(f"Distribución de valores en primera fila: {counter}")

# El valor en posición 0 debe ser 0 (distancia de 0 a 0)
assert first_row[0] == 0

# Los demás valores podrían indicar diferentes caminos
# Valores de 1 vs 2 podrían corresponder a diferentes bits

# Intentemos una hipótesis:
# - Si first_row[i] == 1, entonces el bit de la flag en posición i-1 es 1
# - Si first_row[i] == 2, entonces el bit de la flag en posición i-1 es -1

# Reconstruir la flag basándose en esta hipótesis
flag_bits = []
for i in range(1, m):
    if first_row[i] == 1:
        flag_bits.append('1')
    elif first_row[i] == 2:
        flag_bits.append('0')
    else:
        # Valor inesperado
        flag_bits.append('?')

print(f"Bits de la flag (hipótesis 1): {''.join(flag_bits[:50])}...")
print(f"Total de bits: {len(flag_bits)}")
print(f"Valores inesperados: {flag_bits.count('?')}")

# Convertir bits a bytes
flag_str = ''.join(flag_bits)
if '?' not in flag_str:
    # Convertir binario a bytes
    flag_int = int(flag_str, 2)
    flag_bytes = flag_int.to_bytes((len(flag_str) + 7) // 8, byteorder='big')
    try:
        flag_text = flag_bytes.decode('ascii')
        print(f"Flag (hipótesis 1): {flag_text}")
    except:
        print(f"No se pudo decodificar como ASCII")
        print(f"Bytes: {flag_bytes[:50]}")

# Intentar hipótesis inversa
flag_bits2 = []
for i in range(1, m):
    if first_row[i] == 2:
        flag_bits2.append('1')
    elif first_row[i] == 1:
        flag_bits2.append('0')
    else:
        flag_bits2.append('?')

print(f"\nBits de la flag (hipótesis 2): {''.join(flag_bits2[:50])}...")

flag_str2 = ''.join(flag_bits2)
if '?' not in flag_str2:
    flag_int2 = int(flag_str2, 2)
    flag_bytes2 = flag_int2.to_bytes((len(flag_str2) + 7) // 8, byteorder='big')
    try:
        flag_text2 = flag_bytes2.decode('ascii')
        print(f"Flag (hipótesis 2): {flag_text2}")
    except:
        print(f"No se pudo decodificar como ASCII")
        print(f"Bytes: {flag_bytes2[:50]}")
