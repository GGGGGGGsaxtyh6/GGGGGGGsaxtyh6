from Crypto.Util.number import *
import gmpy2

m = 9792986822963146992114161946549377254001156012300083076259452975070903436656675903033418798369811004678022807932064872669773556983318074157606463933686225452143852071767552582367819932516654167400507310054793760473098421162463267
A = 246920531455433048826966670968977027196902794022573095007307132382393013927558904839982249967656424317118051446771969623490992917094197975459553923550187
B = 3120090466259654766880909097573553950487818021670727992039931232537173262599219376624291488340607228938989670215080876932583555412966984946786628621917436142053528648425399877486481618672307477414787846984446437445450282569184963
e = 4180488827

# El backdoor podría estar en que e es el inverso de algo
# O que e*d = 1 mod phi(m)

# Verifiquemos si podemos encontrar alguna estructura
print("Buscando estructura en e...")
print(f"e = {e}")

# Ver si e es pequeño y podría ser un exponente público de RSA
# Si m = p*q y conocemos e, necesitaríamos phi(m) = (p-1)(q-1)

# Déjame intentar otra cosa: el backdoor podría estar en que 
# el estado inicial o la forma en que se actualiza tiene una debilidad

# Probar si A^B = algo interesante
print("\nProbando relaciones entre A y B...")
print(f"A^2 mod m tiene {pow(A, 2, m).bit_length()} bits")
print(f"B^2 mod m tiene {pow(B, 2, m).bit_length()} bits")

# Probar si (A^state XOR B) tiene alguna propiedad especial
# Si XOR B crea un patrón...

# Otra idea: tal vez m tenga factores especiales que no hemos probado
# Intentemos factorización por curvas elípticas o Pollard rho más agresivo
print("\nIntentando Pollard rho...")

def pollard_rho(n, max_iter=1000000):
    if n % 2 == 0:
        return 2
    
    x = 2
    y = 2
    d = 1
    
    def f(x):
        return (x*x + 1) % n
    
    iteration = 0
    while d == 1 and iteration < max_iter:
        x = f(x)
        y = f(f(y))
        d = gmpy2.gcd(abs(x - y), n)
        iteration += 1
        if iteration % 100000 == 0:
            print(f"  Iteración {iteration}...")
    
    if d != 1 and d != n:
        return d
    return None

factor = pollard_rho(m, 2000000)
if factor:
    print(f"¡Factor encontrado con Pollard rho!: {factor}")
    print(f"Otro factor: {m // factor}")
else:
    print("No se encontró factor con Pollard rho")

# Tal vez el backdoor está en el valor específico de e
# Verificar factores de e
print(f"\nFactores de e:")
temp_e = e
for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]:
    while temp_e % p == 0:
        print(f"  {p}")
        temp_e //= p
if temp_e > 1:
    print(f"  {temp_e}")
