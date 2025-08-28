#!/usr/bin/env python3

def evaluate_polynomial(coefficients, x):
    """
    Evalúa un polinomio dados sus coeficientes y el valor de x
    """
    result = 0
    for i, coef in enumerate(coefficients):
        result += coef * (x ** i)
    return result

# Los valores actuales del servidor
input_str = """93 -26 -28 88 -75 -34 14 16 48
-9"""

lines = input_str.strip().split('\n')
coefficients = list(map(int, lines[0].split()))
x = int(lines[1])

print(f"Coeficientes: {coefficients}")
print(f"x = {x}")

result = evaluate_polynomial(coefficients, x)
print(f"Resultado: {result}")

# Crear el código Python que debo enviar al servidor
solution_code = f"""
coefficients = {coefficients}
x = {x}
result = 0
for i, coef in enumerate(coefficients):
    result += coef * (x ** i)
print(result)
"""

print("\n📝 Código a enviar:")
print(solution_code)