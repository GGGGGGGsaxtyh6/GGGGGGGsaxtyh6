import sympy

large_factor = 309938271107370186286857659422407283771865851657937731111744300310040346308690205006641245318085354895438500308814135783504803596134094206083383195557983

print(f"Factor grande: {large_factor}")
print(f"Bits: {large_factor.bit_length()}")

# Verificar si es primo
print(f"\n¿Es primo? {sympy.isprime(large_factor)}")

# Si es primo, factorizar p-1
if sympy.isprime(large_factor):
    print(f"\nFactorizando {large_factor}-1...")
    factors = sympy.factorint(large_factor - 1, limit=10**8)
    print(f"Factores: {factors}")
    
    # Ver cuál es el factor más grande
    if factors:
        max_factor = max(factors.keys())
        print(f"Factor primo más grande: {max_factor} ({max_factor.bit_length()} bits)")
