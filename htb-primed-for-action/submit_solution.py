import requests
import json

# Código de la solución
codigo_solucion = """# Función para verificar si un número es primo
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

# Leer la entrada
entrada = input()

# Convertir la entrada en una lista de números enteros
numeros = list(map(int, entrada.split()))

# Encontrar todos los números primos en la lista
primos = []
for num in numeros:
    if es_primo(num):
        primos.append(num)

# Multiplicar los dos primos para obtener la clave
resultado = primos[0] * primos[1]

# Imprimir el resultado
print(resultado)"""

# URL del servidor
url = "http://94.237.55.43:56845/run"

# Preparar los datos para enviar
data = {
    "code": codigo_solucion,
    "language": "python"
}

# Enviar la solicitud POST
response = requests.post(url, json=data)

# Mostrar la respuesta
if response.status_code == 200:
    result = response.json()
    print("Respuesta del servidor:")
    print(json.dumps(result, indent=2))
    
    if 'flag' in result:
        print(f"\n¡BANDERA ENCONTRADA!: {result['flag']}")
else:
    print(f"Error: {response.status_code}")
    print(response.text)