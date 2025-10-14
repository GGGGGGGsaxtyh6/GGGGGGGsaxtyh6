from Crypto.Util.number import *
import gmpy2

# Factorización
p1 = 10124460123717732577
p2 = 12017858281002457601
p3 = 15013023439701145679
p4 = 17297082179958074003
p5 = 309938271107370186286857659422407283771865851657937731111744300310040346308690205006641245318085354895438500308814135783504803596134094206083383195557983

m = p1 * p2 * p3 * p4 * p5

A = 246920531455433048826966670968977027196902794022573095007307132382393013927558904839982249967656424317118051446771969623490992917094197975459553923550187
B = 3120090466259654766880909097573553950487818021670727992039931232537173262599219376624291488340607228938989670215080876932583555412966984946786628621917436142053528648425399877486481618672307477414787846984446437445450282569184963

print("Comprobando el orden de A módulo m...")
print(f"A tiene {A.bit_length()} bits")

# Verificar potencias pequeñas de A
for k in [2, 3, 4, 5, 10, 16, 32, 64, 100, 128, 256, 512, 1000, 1024, 2048, 4096, 8192, 10000, 16384, 32768, 65536]:
    val = pow(A, k, m)
    if val == 1:
        print(f"¡A^{k} ≡ 1 (mod m)!")
        print(f"A tiene orden {k}")
        break
    if val == A:
        print(f"A^{k} ≡ A (mod m) - ciclo detectado")
    
    # Verificar si es cercano a B
    if abs(val - B) < 1000:
        print(f"A^{k} ≡ {val} es cercano a B = {B}")
else:
    print("A no tiene orden pequeño")

print("\nComprobando el orden de B módulo m...")
for k in [2, 3, 4, 5, 10, 16, 32, 64, 100, 128, 256, 512, 1000, 1024, 2048, 4096, 8192, 10000, 16384, 32768, 65536, 100000, 262144, 524288, 1000000]:
    val = pow(B, k, m)
    if val == 1:
        print(f"¡B^{k} ≡ 1 (mod m)!")
        print(f"B tiene orden {k}")
        break
else:
    print("B no tiene orden pequeño (probado hasta 2^20)")

print("\nBuscando relaciones entre A y B...")
# ¿Es B una potencia de A?
for k in range(2, 10000):
    if pow(A, k, m) == B:
        print(f"¡B = A^{k} (mod m)!")
        break
    if k % 1000 == 0:
        print(f"  Probado hasta k={k}...")
else:
    print("B no es una potencia pequeña de A")

# ¿Es A una potencia de B?
print("\n¿Es A una potencia de B?")
for k in range(2, 10000):
    if pow(B, k, m) == A:
        print(f"¡A = B^{k} (mod m)!")
        break
    if k % 1000 == 0:
        print(f"  Probado hasta k={k}...")
else:
    print("A no es una potencia pequeña de B")

# Verificar módulo cada primo pequeño
print("\nVerificando órdenes módulo cada primo:")
for p in [p1, p2, p3, p4]:
    print(f"\nMódulo {p}:")
    A_p = A % p
    B_p = B % p
    
    # Orden de A mod p
    for k in [2, 3, 4, 5, 10, 16, 32, 64, 100, 128, 256, 512, 1024, 2048, 4096]:
        if pow(A_p, k, p) == 1:
            print(f"  ord_p(A) | {k}")
            break
    
    # Orden de B mod p
    for k in [2, 3, 4, 5, 10, 16, 32, 64, 100, 128, 256, 512, 1024, 2048, 4096]:
        if pow(B_p, k, p) == 1:
            print(f"  ord_p(B) | {k}")
            break
