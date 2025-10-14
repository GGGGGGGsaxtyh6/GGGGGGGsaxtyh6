from sympy.ntheory import discrete_log
from Crypto.Util.number import bytes_to_long, long_to_bytes

# Parámetros básicos
B_str = "3120090466259654766880909097573553950487818021670727992039931232537173262599219376624291488340607228938989670215080876932583555412966984946786628621917436142053528648425399877486481618672307477414787846984446437445450282569184963"
B = int(B_str)

output_str = "263928838896714332657762314348602240455087661491500131260179929152321790693260683004004767933801216877412896467528419672112455669506824987777448696213888416333755744665868795853306879814179767910033263080874331851322593343273834"
output0 = int(output_str)

known_prefix = b"good luck "
chunk = bytes_to_long(known_prefix)
target = output0 ^ chunk

print("Calculando log discreto con primer primo...")
p1 = 10124460123717732577

g = B % p1
h = target % p1

print(f"discrete_log({p1}, {h}, {g})")
result1 = discrete_log(p1, h, g)
print(f"Resultado 1: {result1}")

print("\nCalculando log discreto con segundo primo...")
p2 = 12017858281002457601

g2 = B % p2
h2 = target % p2

result2 = discrete_log(p2, h2, g2)
print(f"Resultado 2: {result2}")

print("\nUsando CRT...")
# CRT
n1 = p1 - 1
n2 = p2 - 1

# x ≡ result1 (mod n1)
# x ≡ result2 (mod n2)

# CRT manual
N = n1 * n2
N1 = N // n1
N2 = N // n2

M1 = pow(N1, -1, n1)
M2 = pow(N2, -1, n2)

x = (result1 * M1 * N1 + result2 * M2 * N2) % N

print(f"\nx ≡ {x} (mod {N})")
print(f"Bits de x: {x.bit_length()}")

print("\nEl exponente encontrado tiene {} bits".format(x.bit_length()))
print("Verificando...")

# Ahora necesito verificar módulo el m completo
# Construir m
m = p1 * p2 * 15013023439701145679 * 17297082179958074003 * int("309938271107370186286857659422407283771865851657937731111744300310040346308690205006641245318085354895438500308814135783504803596134094206083383195557983")

test = pow(B, x, m)
if test == target:
    print("¡VERIF ICADO!")
    print(f"Exponente = {x}")
else:
    print("No verifica, probando x + k*N...")
    for k in range(100):
        test_x = x + k * N
        test = pow(B, test_x, m)
        if test == target:
            print(f"¡Encontrado con k={k}!")
            x = test_x
            break
    else:
        print("No encontrado")
