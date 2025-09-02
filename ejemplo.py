#!/usr/bin/env python3
"""
Ejemplo de script Python para el repositorio de prueba
"""

import datetime
import random

def saludar(nombre="Usuario"):
    """Función que saluda al usuario"""
    hora_actual = datetime.datetime.now()
    
    if hora_actual.hour < 12:
        momento = "Buenos días"
    elif hora_actual.hour < 18:
        momento = "Buenas tardes"
    else:
        momento = "Buenas noches"
    
    return f"{momento}, {nombre}!"

def generar_numero_aleatorio(min_val=1, max_val=100):
    """Genera un número aleatorio entre min_val y max_val"""
    return random.randint(min_val, max_val)

def calcular_factorial(n):
    """Calcula el factorial de un número"""
    if n < 0:
        return "Error: No se puede calcular el factorial de un número negativo"
    elif n == 0 or n == 1:
        return 1
    else:
        resultado = 1
        for i in range(2, n + 1):
            resultado *= i
        return resultado

def main():
    """Función principal del programa"""
    print("=" * 50)
    print("PROGRAMA DE EJEMPLO - REPOSITORIO DE PRUEBA")
    print("=" * 50)
    
    # Saludar
    print(saludar("Desarrollador"))
    
    # Generar número aleatorio
    numero = generar_numero_aleatorio(1, 10)
    print(f"\nNúmero aleatorio generado: {numero}")
    
    # Calcular factorial
    factorial = calcular_factorial(numero)
    print(f"El factorial de {numero} es: {factorial}")
    
    # Información del sistema
    print(f"\nFecha y hora actual: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    print("\n" + "=" * 50)
    print("Programa ejecutado exitosamente!")

if __name__ == "__main__":
    main()