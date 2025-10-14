from Crypto.Util.number import *
import gmpy2

m = 9792986822963146992114161946549377254001156012300083076259452975070903436656675903033418798369811004678022807932064872669773556983318074157606463933686225452143852071767552582367819932516654167400507310054793760473098421162463267
A = 246920531455433048826966670968977027196902794022573095007307132382393013927558904839982249967656424317118051446771969623490992917094197975459553923550187
B = 3120090466259654766880909097573553950487818021670727992039931232537173262599219376624291488340607228938989670215080876932583555412966984946786628621917436142053528648425399877486481618672307477414787846984446437445450282569184963
e = 4180488827

print("Verificando estados especiales...")
print()

# ¿Qué pasa si state = 0?
print("state = 0:")
print(f"  A^0 mod m = {pow(A, 0, m)}")
print(f"  Debería ser 1")
print()

# ¿Qué pasa si state = 1?
print("state = 1:")
val = pow(A, 1, m)
print(f"  A^1 mod m = {val}")
print(f"  A^1 XOR B = {val ^ B}")
print()

# ¿Hay algún state pequeño tal que A^state ≡ B (mod m)?
print("¿Existe state pequeño tal que A^state ≡ B (mod m)?")
for state in range(2, 100000):
    if pow(A, state, m) == B:
        print(f"  ¡SÍ! state = {state}")
        break
    if state % 10000 == 0:
        print(f"  Probado hasta state = {state}...")
else:
    print("  No encontrado hasta 100000")
print()

# ¿Qué pasa si A^state ≡ 0 (mod m)?
print("¿A^state puede ser 0 mod m?")
if gmpy2.gcd(A, m) > 1:
    print(f"  gcd(A, m) = {gmpy2.gcd(A, m)} > 1, así que sí es posible")
else:
    print(f"  gcd(A, m) = 1, así que no")
print()

# Verificar si B es especial de alguna manera
print(f"B mod m = {B % m}")
print(f"B == (B % m): {B == (B % m)}")
print(f"B < m: {B < m}")
print()

# ¿Qué pasa si el estado initial está relacionado con e?
print(f"Probando states relacionados con e = {e}...")
for multiplier in [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2**16]:
    state = e * multiplier
    val = pow(A, state, m)
    print(f"  state = e * {multiplier} = {state}:")
    print(f"    A^state mod m = {hex(val)[:50]}...")
    if val == B:
        print(f"    ¡Es igual a B!")
    if val ^ B < 1000:
        print(f"    XOR con B da valor pequeño: {val ^ B}")
print()

# Verificar relaciones con los primos de la factorización
p1 = 10124460123717732577
print(f"Probando states relacionados con p1 = {p1}...")
for multiplier in [1, 2, 4, 8, 16]:
    state = p1 // multiplier
    if state > 0:
        val = pow(A, state, m)
        print(f"  state = p1 // {multiplier} = {state}:")
        print(f"    bits: {state.bit_length()}")
