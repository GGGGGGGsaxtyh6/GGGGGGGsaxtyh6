from Crypto.Util.number import *
import gmpy2

m = 9792986822963146992114161946549377254001156012300083076259452975070903436656675903033418798369811004678022807932064872669773556983318074157606463933686225452143852071767552582367819932516654167400507310054793760473098421162463267
A = 246920531455433048826966670968977027196902794022573095007307132382393013927558904839982249967656424317118051446771969623490992917094197975459553923550187
B = 3120090466259654766880909097573553950487818021670727992039931232537173262599219376624291488340607228938989670215080876932583555412966984946786628621917436142053528648425399877486481618672307477414787846984446437445450282569184963
e = 4180488827

# Una idea: ¿y si m es de la forma p^k para algún primo p?
print("Verificando si m es una potencia prima...")
for k in range(2, 20):
    root = gmpy2.iroot(m, k)
    if root[1]:  # Si es una raíz exacta
        print(f"m = {root[0]}^{k}")
        if gmpy2.is_prime(root[0]):
            print(f"¡Y {root[0]} es primo!")
        break

# Otra idea: ¿y si m = 2^k - 1 o 2^k + 1?
print("\nVerificando formas especiales de m...")
k = m.bit_length()
mersenne_candidate = (1 << k) - 1
fermat_candidate = (1 << k) + 1

if m == mersenne_candidate:
    print(f"m = 2^{k} - 1 (número de Mersenne)")
elif m == fermat_candidate:
    print(f"m = 2^{k} + 1 (número de Fermat)")
else:
    # Ver qué tan cerca está
    diff_mersenne = abs(m - mersenne_candidate)
    diff_fermat = abs(m - fermat_candidate)
    print(f"Diferencia con 2^{k}-1: {diff_mersenne}")
    print(f"Diferencia con 2^{k}+1: {diff_fermat}")

# ¿Y si A o B son generadores especiales?
print("\nVerificando si A^2 = -1 mod m o algo similar...")
A_sq = pow(A, 2, m)
print(f"A^2 mod m = ... (termina en {str(A_sq)[-50:]})")
if A_sq == m - 1:
    print("A^2 = -1 mod m!")
if A_sq == 1:
    print("A^2 = 1 mod m!")

# Verificar B también
B_sq = pow(B, 2, m)
if B_sq == m - 1:
    print("B^2 = -1 mod m!")
if B_sq == 1:
    print("B^2 = 1 mod m!")

# Verificar si A*B o A+B tienen propiedades especiales
print("\nVerificando relaciones entre A y B...")
A_times_B = (A * B) % m
A_plus_B = (A + B) % m
A_xor_B = A ^ B

print(f"A*B mod m bits: {A_times_B.bit_length()}")
print(f"A+B mod m bits: {A_plus_B.bit_length()}")
print(f"A XOR B bits: {A_xor_B.bit_length()}")

# ¿Y si A^e o B^e tienen propiedades especiales?
print("\nVerificando A^e y B^e...")
A_pow_e = pow(A, e, m)
B_pow_e = pow(B, e, m)
print(f"A^e mod m bits: {A_pow_e.bit_length()}")
print(f"B^e mod m bits: {B_pow_e.bit_length()}")

# El backdoor podría ser en la inversa de e
# ¿Hay un d tal que e*d = 1 mod algo?
# Sin phi(m) esto es difícil...

# Pero espera, ¿y si podemos calcular phi(m) de alguna manera?
# ¿O si m - 1 tiene una estructura especial?
print("\nAnalizando m-1...")
m_minus_1 = m - 1
print(f"m-1 = {m_minus_1}")
print(f"Factores pequeños de m-1:")
temp = m_minus_1
for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71]:
    count = 0
    while temp % p == 0:
        count += 1
        temp //= p
    if count > 0:
        print(f"  {p}^{count}")
