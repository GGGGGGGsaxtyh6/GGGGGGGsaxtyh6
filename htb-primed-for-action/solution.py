# Función para verificar si un número es primo
def es_primo(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

# Leer la entrada - será una línea con números separados por espacios
entrada = input()

# Convertir la entrada en una lista de números enteros
numeros = list(map(int, entrada.split()))

# Encontrar todos los números primos en la lista
primos = []
for num in numeros:
    if es_primo(num):
        primos.append(num)

# El desafío dice que hay exactamente 2 números primos
# Multiplicar los dos primos para obtener la clave
if len(primos) >= 2:
    resultado = primos[0] * primos[1]
else:
    # Si por alguna razón no hay suficientes primos, usar el producto de los disponibles
    resultado = primos[0] if len(primos) == 1 else 0

# Imprimir el resultado
print(resultado)