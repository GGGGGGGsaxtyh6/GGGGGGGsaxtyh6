from Crypto.Util.number import *
import gmpy2
from sympy.ntheory.residue_ntheory import discrete_log

m = 9792986822963146992114161946549377254001156012300083076259452975070903436656675903033418798369811004678022807932064872669773556983318074157606463933686225452143852071767552582367819932516654167400507310054793760473098421162463267
A = 246920531455433048826966670968977027196902794022573095007307132382393013927558904839982249967656424317118051446771969623490992917094197975459553923550187
B = 3120090466259654766880909097573553950487818021670727992039931232537173262599219376624291488340607228938989670215080876932583555412966984946786628621917436142053528648425399877486481618672307477414787846984446437445450282569184963
e = 4180488827

output = [263928838896714332657762314348602240455087661491500131260179929152321790693260683004004767933801216877412896467528419672112455669506824987777448696213888416333755744665868795853306879814179767910033263080874331851322593343273834, 7500716958005582985508201577146205078774368134456220390802616323312171951781595852608949532619393759348663684985174625019004577610546554994801687569942118260000292201829011312249563036393035204990811392856155820408283216493092108, 2577794401090299805723177598637436117371525412262771825236813936115237585602114357696686099541164980249580094089526387369627399445447896464668107355247993148990034255262021717192029828447047736912032562575292618672346226630177737, 9097092753543027532933159793556144814276134227405286080166556624316657274280165256861623248902541076900039285592392074751617153907616670295765377162951858063712964557527212039482031296350052367350738141716598584719951567052177519, 8174235910244322855637254130843352735528509191186418212056519911128301630950848710182451421471531481098828227735010211554839205099309290314993113489826162548089590990963249899714956197889959999884447438378454452096405595048394416, 2823506900640363315693941780283568096117331722098156706833610340919194199647098542170689133810904702849664199290565773405646243449194786656181872671323095023235608799444864036190997987871160063941897196360905342203429250068859314, 4625135637721297092934166648990860031642126233341589454312760229225192256970211899532356300747405146834048765116081788846632527090729839758895834854075755594692611781829177188955301784020596520269704429107749955107365380494152652]

factors = [
    10124460123717732577,
    12017858281002457601,
    15013023439701145679,
    17297082179958074003,
    309938271107370186286857659422407283771865851657937731111744300310040346308690205006641245318085354895438500308814135783504803596134094206083383195557983
]

# Calcular phi(m)
phi_m = 1
for f in factors:
    phi_m *= (f - 1)

d = gmpy2.invert(e, phi_m)

# Known plaintext
known_start = b"good luck lmao ictf{"
known_chunks = [bytes_to_long(known_start[i:i+10]) for i in range(0, len(known_start), 10)]
keystreams = [output[i] ^ known_chunks[i] for i in range(len(known_chunks))]

print("=== Estrategia alternativa ===")
print("En lugar de resolver el logaritmo discreto directamente,")
print("intentemos recuperar el estado usando la estructura del cifrado.")
print()

# La ecuación es: new_state = (A^state XOR B)^e mod m
# Si tenemos d tal que e*d = 1 mod phi(m), entonces:
# state_i = log_A((new_state_i^d XOR B)) mod phi(m)

# Pero el problema es que no conocemos new_state directamente...

# Enfoque diferente: bruteforce sobre los últimos 16 bits del estado inicial
# Ya que sabemos que el keystream solo usa state & ~0xffff

print("=== Bruteforce sobre los últimos 16 bits del estado ===")
print("Probando diferentes valores de los últimos 16 bits...")
print()

# Para el primer keystream, sabemos:
# keystream[0] = B^(state0 & ~0xffff) mod m
# Si state0 = high_bits | low_bits, donde low_bits son los últimos 16 bits,
# entonces keystream[0] = B^(state0 - low_bits) mod m
# O sea: B^state0 / B^low_bits = keystream[0] mod m
# Entonces: B^state0 = keystream[0] * B^low_bits mod m

# Para cada valor de low_bits (0 a 65535), calculo B^low_bits
# y luego necesito resolver B^x = keystream[0] * B^low_bits mod m
# para x = state0

# Esto todavía requiere logaritmo discreto...

# Mejor enfoque: ver si el estado inicial es pequeño por el backdoor
print("Probando si el estado inicial es pequeño...")
print("(El backdoor podría ser que el estado no es realmente aleatorio)")
print()

# Probar estados pequeños
max_state_to_try = 2**24  # Probar hasta 2^24
batch_size = 100000

print(f"Probando estados desde 0 hasta {max_state_to_try}...")
for state_guess in range(0, min(max_state_to_try, 10000000), batch_size):
    if state_guess % 1000000 == 0:
        print(f"  Probando alrededor de {state_guess}...")
    
    for offset in range(batch_size):
        s = state_guess + offset
        # Calcular el keystream que produciría este estado
        expected_keystream = pow(B, s - (s & 0xffff), m)
        if expected_keystream == keystreams[0]:
            print(f"\n¡¡¡ESTADO INICIAL ENCONTRADO!!!")
            print(f"state0 = {s}")
            
            # Verificar con el segundo keystream
            # Calcular new_state
            new_s = pow(pow(A, s, m) ^ B, e, m)
            expected_keystream_1 = pow(B, new_s - (new_s & 0xffff), m)
            if expected_keystream_1 == keystreams[1]:
                print(f"¡Verificado con keystream[1]!")
                print(f"state1 = {new_s}")
                
                # Ahora podemos descifrar toda la flag
                print("\nDescifrando la flag completa...")
                state = s
                plaintext = b""
                
                for i in range(len(output)):
                    ks = pow(B, state - (state & 0xffff), m)
                    chunk = output[i] ^ ks
                    chunk_bytes = long_to_bytes(chunk).rjust(10, b'\x00')
                    plaintext += chunk_bytes
                    
                    # Actualizar estado
                    state = pow(pow(A, state, m) ^ B, e, m)
                
                print(f"Plaintext: {plaintext}")
                print(f"Flag: {plaintext.strip()}")
                exit(0)
            else:
                print(f"No verificado con keystream[1], false positive")

print("\nNo se encontró el estado en el rango probado.")
print("El estado inicial debe ser más grande o necesitamos otro enfoque.")
