import math

moduli = [10124460123717732576, 12017858281002457600, 15013023439701145678, 17297082179958074002]

print("Verificando si los módulos son coprimos...")
for i in range(len(moduli)):
    for j in range(i+1, len(moduli)):
        g = math.gcd(moduli[i], moduli[j])
        if g > 1:
            print(f"gcd(moduli[{i}], moduli[{j}]) = {g}")
            print(f"  moduli[{i}] = {moduli[i]}")
            print(f"  moduli[{j}] = {moduli[j]}")
            
            # Factorizar el gcd
            print(f"  Factorizando {g}...")
            temp = g
            for p in [2, 3, 5, 7, 11, 13]:
                count = 0
                while temp % p == 0:
                    count += 1
                    temp //= p
                if count > 0:
                    print(f"    {p}^{count}")

print("\nLos módulos deberían ser (pi - 1) para cada factor primo pi de m")
print("Necesito factorizar cada (pi - 1) y usar Pohlig-Hellman adecuadamente")
