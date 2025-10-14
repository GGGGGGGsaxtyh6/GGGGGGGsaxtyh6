import requests
import json

m = 9792986822963146992114161946549377254001156012300083076259452975070903436656675903033418798369811004678022807932064872669773556983318074157606463933686225452143852071767552582367819932516654167400507310054793760473098421162463267

# Intentar con factordb.com API
url = f"http://factordb.com/api?query={m}"

print(f"Consultando FactorDB...")
try:
    response = requests.get(url, timeout=30)
    data = response.json()
    print(f"Respuesta: {json.dumps(data, indent=2)}")
    
    if 'factors' in data:
        print("\n¡Factores encontrados!")
        for factor in data['factors']:
            print(f"  {factor}")
except Exception as e:
    print(f"Error: {e}")

# Si factordb no funciona, intentar factorización local con métodos más avanzados
print("\nSi factordb no funciona, intentando factorización local...")
