import gmpy2
from math import gcd

m = 9792986822963146992114161946549377254001156012300083076259452975070903436656675903033418798369811004678022807932064872669773556983318074157606463933686225452143852071767552582367819932516654167400507310054793760473098421162463267
A = 246920531455433048826966670968977027196902794022573095007307132382393013927558904839982249967656424317118051446771969623490992917094197975459553923550187
B = 3120090466259654766880909097573553950487818021670727992039931232537173262599219376624291488340607228938989670215080876932583555412966984946786628621917436142053528648425399877486481618672307477414787846984446437445450282569184963

# Quizás A o B revelen información sobre m
# Si A^algo ≡ algo mod m, podría revelar factores

print("Probando GCD con potencias de A y B...")

# Intentar: gcd(A^k - 1, m) o gcd(B^k - 1, m)
for k in [2, 3, 4, 5, 10, 12, 16, 20, 100, 256, 512, 1024]:
    g1 = gcd(pow(A, k, m) - 1, m)
    g2 = gcd(pow(B, k, m) - 1, m)
    
    if g1 > 1 and g1 < m:
        print(f"¡GCD encontrado con A^{k}-1: {g1}")
        print(f"Factor: {g1}")
        print(f"Cofactor: {m // g1}")
        break
    if g2 > 1 and g2 < m:
        print(f"¡GCD encontrado con B^{k}-1: {g2}")
        print(f"Factor: {g2}")
        print(f"Cofactor: {m // g2}")
        break
else:
    print("No se encontró factor con ese método")

print("\nProbando si m = p*q con p y q cercanos (Fermat)...")
a = gmpy2.isqrt(m) + 1
max_iter = 10000000
for i in range(max_iter):
    b2 = a*a - m
    if gmpy2.is_square(b2):
        b = gmpy2.isqrt(b2)
        p = a - b
        q = a + b
        if p * q == m:
            print(f"¡FACTORES ENCONTRADOS!")
            print(f"p = {p}")
            print(f"q = {q}")
            print(f"Verificación: p * q == m: {p * q == m}")
            break
    a += 1
    if i % 1000000 == 0 and i > 0:
        print(f"Iteración {i}/{max_iter}...")
else:
    print(f"No se encontró con Fermat en {max_iter} iteraciones")
