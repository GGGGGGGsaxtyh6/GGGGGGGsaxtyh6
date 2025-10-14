from sympy.ntheory import discrete_log
from Crypto.Util.number import bytes_to_long, long_to_bytes
import gmpy2

# Parámetros
B = 3120090466259654766880909097573553950487818021670727992039931232537173262599219376624291488340607228938989670215080876932583555412966984946786628621917436142053528648425399877486481618672307477414787846984446437445450282569184963
A = 246920531455433048826966670968977027196902794022573095007307132382393013927558904839982249967656424317118051446771969623490992917094197975459553923550187
e = 4180488827

p1, p2, p3, p4 = 10124460123717732577, 12017858281002457601, 15013023439701145679, 17297082179958074003
p5 = 309938271107370186286857659422407283771865851657937731111744300310040346308690205006641245318085354895438500308814135783504803596134094206083383195557983
m = p1 * p2 * p3 * p4 * p5

output_list = [263928838896714332657762314348602240455087661491500131260179929152321790693260683004004767933801216877412896467528419672112455669506824987777448696213888416333755744665868795853306879814179767910033263080874331851322593343273834, 7500716958005582985508201577146205078774368134456220390802616323312171951781595852608949532619393759348663684985174625019004577610546554994801687569942118260000292201829011312249563036393035204990811392856155820408283216493092108, 2577794401090299805723177598637436117371525412262771825236813936115237585602114357696686099541164980249580094089526387369627399445447896464668107355247993148990034255262021717192029828447047736912032562575292618672346226630177737, 9097092753543027532933159793556144814276134227405286080166556624316657274280165256861623248902541076900039285592392074751617153907616670295765377162951858063712964557527212039482031296350052367350738141716598584719951567052177519, 8174235910244322855637254130843352735528509191186418212056519911128301630950848710182451421471531481098828227735010211554839205099309290314993113489826162548089590990963249899714956197889959999884447438378454452096405595048394416, 2823506900640363315693941780283568096117331722098156706833610340919194199647098542170689133810904702849664199290565773405646243449194786656181872671323095023235608799444864036190997987871160063941897196360905342203429250068859314, 4625135637721297092934166648990860031642126233341589454312760229225192256970211899532356300747405146834048765116081788846632527090729839758895834854075755594692611781829177188955301784020596520269704429107749955107365380494152652]

known_full = b"good luck lmao ictf{"
chunks_known = [bytes_to_long(known_full[i:i+10]) for i in range(0, len(known_full), 10)]
target = output_list[0] ^ chunks_known[0]

print("Calculando log discreto módulo p1...")
result1 = discrete_log(p1, target % p1, B % p1)
print(f"x ≡ {result1} (mod {p1-1})")

print("\nCalculando log discreto módulo p2...")
result2 = discrete_log(p2, target % p2, B % p2)
print(f"x ≡ {result2} (mod {p2-1})")

# Como gcd(p1-1, p2-1) = 32, uso el módulo reducido
# El exponente debe ser result1 mod (p1-1) y result2 mod (p2-1)
# Puedo buscar x = result1 + k*(p1-1) tal que x ≡ result2 (mod p2-1)

n1 = p1 - 1
n2 = p2 - 1

print(f"\nBuscando k tal que result1 + k*n1 ≡ result2 (mod n2)...")
# result1 + k*n1 ≡ result2 (mod n2)
# k*n1 ≡ result2 - result1 (mod n2)
# k ≡ (result2 - result1) / n1 (mod n2)

# Pero n1 y n2 no son coprimos. Necesito trabajar con n1/gcd y n2/gcd
g = int(gmpy2.gcd(n1, n2))
n1_reduced = n1 // g
n2_reduced = n2 // g

diff = result2 - result1
# Verificar que diff es divisible por g
if diff % g != 0:
    print("ERROR: resultados inconsistentes")
else:
    diff_reduced = diff // g
    inv = int(gmpy2.invert(n1_reduced, n2_reduced))
    k = (diff_reduced * inv) % n2_reduced
    
    x_candidate = result1 + k * n1
    print(f"k = {k}")
    print(f"x_candidate = {x_candidate}")
    print(f"Bits: {x_candidate.bit_length()}")
    
    # Verificar
    test = pow(B, x_candidate, m)
    if test == target:
        print("\n¡VERIFICADO! Exponente encontrado.")
        x = x_candidate
    else:
        print("\nNo verifica exactamente, puede que necesite agregar múltiplos del LCM")
        lcm = (n1 * n2) // g
        found = False
        for add_k in range(100):
            test_x = x_candidate + add_k * lcm
            test = pow(B, test_x, m)
            if test == target:
                print(f"¡Encontrado con add_k={add_k}!")
                x = test_x
                found = True
                break
        if not found:
            print("No encontrado. Usando x_candidate de todos modos...")
            x = x_candidate
    
    print(f"\nExponente final (state >> 16 << 16): {x}")
    print(f"Bits: {x.bit_length()}")
    
    # Buscar los últimos 16 bits
    print("\nBuscando últimos 16 bits del estado...")
    for low_bits in range(65536):
        full_state = x | low_bits
        temp_state = full_state
        
        # Verificar con los dos primeros outputs
        match = True
        for i in range(min(2, len(chunks_known))):
            keystream = pow(B, temp_state - (temp_state & 0xffff), m)
            expected = output_list[i] ^ chunks_known[i]
            if keystream != expected:
                match = False
                break
            temp_state = pow(pow(A, temp_state, m) ^ B, e, m)
        
        if match:
            print(f"¡Encontrado! low_bits = {low_bits}")
            print(f"Estado inicial completo: {full_state}")
            
            # Descifrar
            plaintext = b""
            temp_state = full_state
            for out in output_list:
                keystream = pow(B, temp_state - (temp_state & 0xffff), m)
                chunk_val = out ^ keystream
                chunk_bytes = long_to_bytes(chunk_val)
                plaintext += chunk_bytes
                temp_state = pow(pow(A, temp_state, m) ^ B, e, m)
            
            print("\n" + "="*60)
            print(plaintext.decode('utf-8', errors='ignore'))
            print("="*60)
            break
    else:
        print("No se encontraron los últimos 16 bits")
