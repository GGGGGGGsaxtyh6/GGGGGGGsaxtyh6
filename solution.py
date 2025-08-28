#!/usr/bin/env python3
# Solución genérica que lee el input y calcula el polinomio

# Leer input
import sys
lines = sys.stdin.read().strip().split('\n')
coefficients = list(map(int, lines[0].split()))
x = int(lines[1])

# Calcular polinomio
result = 0
for i, coef in enumerate(coefficients):
    result += coef * (x ** i)

# Imprimir resultado
print(result)