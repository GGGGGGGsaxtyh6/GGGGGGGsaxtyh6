import gmpy2
from math import gcd

m = 9792986822963146992114161946549377254001156012300083076259452975070903436656675903033418798369811004678022807932064872669773556983318074157606463933686225452143852071767552582367819932516654167400507310054793760473098421162463267
A = 246920531455433048826966670968977027196902794022573095007307132382393013927558904839982249967656424317118051446771969623490992917094197975459553923550187
B = 3120090466259654766880909097573553950487818021670727992039931232537173262599219376624291488340607228938989670215080876932583555412966984946786628621917436142053528648425399877486481618672307477414787846984446437445450282569184963
e = 4180488827

print(f"Bits de m: {m.bit_length()}")
print(f"Bits de A: {A.bit_length()}")
print(f"Bits de B: {B.bit_length()}")

# Verificar si A o B tienen alguna relación especial con m
print(f"\ngcd(A, m) = {gcd(A, m)}")
print(f"gcd(B, m) = {gcd(B, m)}")

# Verificar si e tiene propiedades especiales
print(f"\ne = {e}")
print(f"Bits de e: {e.bit_length()}")

# El backdoor podría estar en que m = p*q donde conocemos la factorización
# Intentemos factorización de Fermat (útil cuando p y q están cerca)
print("\nIntentando factorización de Fermat...")
import math
a = gmpy2.isqrt(m) + 1
max_iter = 10000000
for i in range(max_iter):
    b_sq = a*a - m
    if gmpy2.is_square(b_sq):
        b = gmpy2.isqrt(b_sq)
        p = a - b
        q = a + b
        print(f"¡Factores encontrados!")
        print(f"p = {p}")
        print(f"q = {q}")
        print(f"p * q = {p * q}")
        print(f"p * q == m: {p * q == m}")
        break
    a += 1
    if i % 1000000 == 0 and i > 0:
        print(f"Iteración {i}...")
else:
    print(f"No se encontraron factores en {max_iter} iteraciones")
