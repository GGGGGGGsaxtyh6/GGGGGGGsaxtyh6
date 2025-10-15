from Crypto.Util.number import GCD
import sympy

# Valores del desafío
m = 9792986822963146992114161946549377254001156012300083076259452975070903436656675903033418798369811004678022807932064872669773556983318074157606463933686225452143852071767552582367819932516654167400507310054793760473098421162463267
A = 246920531455433048826966670968977027196902794022573095007307132382393013927558904839982249967656424317118051446771969623490992917094197975459553923550187 
B = 3120090466259654766880909097573553950487818021670727992039931232537173262599219376624291488340607228938989670215080876932583555412966984946786628621917436142053528648425399877486481618672307477414787846984446437445450282569184963
e = 4180488827

print("Buscando relaciones especiales...")

# Comprobar GCD
print(f"GCD(A, m) = {GCD(A, m)}")
print(f"GCD(B, m) = {GCD(B, m)}")
print(f"GCD(e, m) = {GCD(e, m)}")

# Comprobar si alguno divide a m
print(f"\nm % A = {m % A}")
print(f"m % B = {m % B}")
print(f"m % e = {m % e}")

# Comprobar relaciones entre A y B
print(f"\nA + B mod m = {(A + B) % m}")
print(f"A * B mod m = {(A * B) % m}")
print(f"A ^ B (primeros bits) = {A ^ B}")

# Veamos si B está relacionado con A de alguna forma
print(f"\nA^2 mod m = {pow(A, 2, m)}")
print(f"B == A^2 mod m? {B == pow(A, 2, m)}")

# Veamos otras potencias
for i in range(2, 20):
    if pow(A, i, m) == B:
        print(f"B == A^{i} mod m !")
        break

# Veamos si e divide a algo importante
print(f"\n(m-1) % e = {(m-1) % e}")
print(f"(m+1) % e = {(m+1) % e}")

# Intentemos factorizar e
print(f"\ne = {e}")
print(f"Factores de e: {sympy.factorint(e)}")

# Veamos el tamaño de m en diferentes bases
print(f"\nlog2(m) ≈ {m.bit_length()}")

# Intentemos ver si m tiene una forma especial
# Comprobar si m es de la forma p^k
for k in range(2, 10):
    root = int(m ** (1/k))
    for delta in range(-5, 6):
        candidate = root + delta
        if candidate ** k == m:
            print(f"m = {candidate}^{k}")
            if sympy.isprime(candidate):
                print(f"  y {candidate} es primo!")
