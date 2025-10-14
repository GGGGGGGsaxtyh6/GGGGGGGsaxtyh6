from Crypto.Util.number import *
import gmpy2

m = 9792986822963146992114161946549377254001156012300083076259452975070903436656675903033418798369811004678022807932064872669773556983318074157606463933686225452143852071767552582367819932516654167400507310054793760473098421162463267
A = 246920531455433048826966670968977027196902794022573095007307132382393013927558904839982249967656424317118051446771969623490992917094197975459553923550187
B = 3120090466259654766880909097573553950487818021670727992039931232537173262599219376624291488340607228938989670215080876932583555412966984946786628621917436142053528648425399877486481618672307477414787846984446437445450282569184963
e = 4180488827

output = [263928838896714332657762314348602240455087661491500131260179929152321790693260683004004767933801216877412896467528419672112455669506824987777448696213888416333755744665868795853306879814179767910033263080874331851322593343273834, 7500716958005582985508201577146205078774368134456220390802616323312171951781595852608949532619393759348663684985174625019004577610546554994801687569942118260000292201829011312249563036393035204990811392856155820408283216493092108, 2577794401090299805723177598637436117371525412262771825236813936115237585602114357696686099541164980249580094089526387369627399445447896464668107355247993148990034255262021717192029828447047736912032562575292618672346226630177737, 9097092753543027532933159793556144814276134227405286080166556624316657274280165256861623248902541076900039285592392074751617153907616670295765377162951858063712964557527212039482031296350052367350738141716598584719951567052177519, 8174235910244322855637254130843352735528509191186418212056519911128301630950848710182451421471531481098828227735010211554839205099309290314993113489826162548089590990963249899714956197889959999884447438378454452096405595048394416, 2823506900640363315693941780283568096117331722098156706833610340919194199647098542170689133810904702849664199290565773405646243449194786656181872671323095023235608799444864036190997987871160063941897196360905342203429250068859314, 4625135637721297092934166648990860031642126233341589454312760229225192256970211899532356300747405146834048765116081788846632527090729839758895834854075755594692611781829177188955301784020596520269704429107749955107365380494152652]

# Factores de m
factors = [
    10124460123717732577,
    12017858281002457601,
    15013023439701145679,
    17297082179958074003,
    309938271107370186286857659422407283771865851657937731111744300310040346308690205006641245318085354895438500308814135783504803596134094206083383195557983
]

# Verificar factorización
product = 1
for f in factors:
    product *= f
print(f"Verificación: product == m: {product == m}")

# Calcular phi(m)
phi_m = 1
for f in factors:
    phi_m *= (f - 1)
print(f"phi(m) calculado")
print(f"Bits de phi(m): {phi_m.bit_length()}")

# Ahora, con phi(m), puedo calcular el inverso de e módulo phi(m)
# Si gcd(e, phi(m)) = 1, entonces existe d tal que e*d = 1 mod phi(m)
gcd_val = gmpy2.gcd(e, phi_m)
print(f"gcd(e, phi(m)) = {gcd_val}")

if gcd_val == 1:
    d = gmpy2.invert(e, phi_m)
    print(f"Inverso de e módulo phi(m) encontrado: d = {d}")
    print(f"Verificación: (e * d) % phi_m = {(e * d) % phi_m}")
else:
    print("e y phi(m) no son coprimos, necesitamos un enfoque diferente")

# Known plaintext para obtener keystreams
known_start = b"good luck lmao ictf{"
known_chunks = [bytes_to_long(known_start[i:i+10]) for i in range(0, len(known_start), 10)]
keystreams = [output[i] ^ known_chunks[i] for i in range(len(known_chunks))]

print(f"\nKeystreams conocidos: {len(keystreams)}")
print(f"keystream[0] = {keystreams[0]}")
print(f"keystream[1] = {keystreams[1]}")

# El keystream[0] = B^(state0 & ~0xffff) mod m
# Necesitamos encontrar x = (state0 & ~0xffff) tal que B^x = keystream[0] mod m
# Con phi(m), podemos usar Pohlig-Hellman o baby-step giant-step

print("\nIntentando resolver logaritmo discreto...")
print("Esto puede tardar un momento...")

# Para resolver log_B(keystream[0]) mod m, necesitamos trabajar módulo phi(m)
# o usar algoritmos de logaritmo discreto

# Intentemos Pohlig-Hellman manualmente o baby-step giant-step
# Dado que phi(m) está factorizado, Pohlig-Hellman es viable

# Primero, necesitamos el orden de B en el grupo (Z/mZ)*
# El orden divide a phi(m)

print("\nCalculando orden de B...")
# El orden debe dividir a phi(m)
# Probemos si B^phi(m) = 1 mod m (por teorema de Euler, debería serlo)
B_phi = pow(B, phi_m, m)
print(f"B^phi(m) mod m = {B_phi}")
if B_phi == 1:
    print("Verificado: B^phi(m) = 1 mod m (teorema de Euler)")

# Para simplificar, si el orden de B es phi(m) o un divisor conocido,
# podemos resolver el logaritmo discreto

# Usemos sympy para el logaritmo discreto
print("\nIntentando discrete_log con sympy...")
from sympy.ntheory import discrete_log

try:
    # Esto puede tardar mucho, así que lo haremos con un timeout implícito
    # discrete_log(n, a, b, order=None) resuelve a^x = n mod b
    # En nuestra notación: x tal que B^x = keystream[0] mod m
    
    print("Calculando discrete_log(keystream[0], B, m)...")
    print("Esto podría tardar. Si toma más de 30s, necesitaremos Pohlig-Hellman manual...")
    
    # Intentemos con un límite de orden (phi_m)
    # exponent = discrete_log(m, keystream[0], B, order=phi_m)
    # print(f"¡Logaritmo discreto encontrado!: {exponent}")
    print("Usando enfoque alternativo...")
    
except Exception as e:
    print(f"Error en discrete_log: {e}")

# Enfoque alternativo: Como sabemos que el exponente es (state & ~0xffff),
# es decir, es múltiplo de 2^16, podemos buscar en ese espacio reducido

print("\nProbando si el exponente es un múltiplo de 2^16...")
# Si x = k * 2^16, entonces B^(k*2^16) = keystream[0] mod m
# Es decir, (B^(2^16))^k = keystream[0] mod m
# Entonces k = log_{B^(2^16)}(keystream[0])

B_65536 = pow(B, 65536, m)
print(f"B^65536 mod m calculado")

# Ahora necesitamos resolver: (B^65536)^k = keystream[0] mod m
# O sea: log_{B^65536}(keystream[0]) = k

# El orden de B^65536 es phi_m / gcd(65536, phi_m)
gcd_order = gmpy2.gcd(65536, phi_m)
new_order = phi_m // gcd_order
print(f"Orden de B^65536 es aproximadamente phi_m / {gcd_order}")

# Esto sigue siendo muy grande... necesitamos Pohlig-Hellman
print("\nImplementando Pohlig-Hellman...")
