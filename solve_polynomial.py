#!/usr/bin/env python3

def evaluate_polynomial(coefficients, x):
    """
    Evalúa un polinomio dados sus coeficientes y el valor de x
    Polinomio: a_0 + a_1*x + a_2*x^2 + ... + a_8*x^8
    """
    result = 0
    for i, coef in enumerate(coefficients):
        result += coef * (x ** i)
    return result

# Verificar con el ejemplo
print("🧪 Verificando con el ejemplo del reto:")
coeffs = [1, -2, 3, -4, 5, -6, 7, -8, 9]
x = 5
expected = 2983941

result = evaluate_polynomial(coeffs, x)
print(f"Coeficientes: {coeffs}")
print(f"x = {x}")
print(f"Resultado calculado: {result}")
print(f"Resultado esperado: {expected}")
print(f"✅ Correcto!" if result == expected else f"❌ Incorrecto")

# Ahora voy a hacer una función que tome el input como string y devuelva el resultado
def solve_from_input(coeffs_line, x_line):
    """
    Resuelve el polinomio desde las líneas de input
    """
    # Parsear coeficientes
    coefficients = list(map(int, coeffs_line.strip().split()))
    # Parsear x
    x = int(x_line.strip())
    
    # Calcular resultado
    result = evaluate_polynomial(coefficients, x)
    
    return result

# Test con el ejemplo como strings
print("\n🧪 Test con formato de input:")
coeffs_str = "1 -2 3 -4 5 -6 7 -8 9"
x_str = "5"
result = solve_from_input(coeffs_str, x_str)
print(f"Input 1: {coeffs_str}")
print(f"Input 2: {x_str}")
print(f"Output: {result}")