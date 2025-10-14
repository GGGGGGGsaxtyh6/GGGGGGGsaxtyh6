from Crypto.Util.number import *
import gmpy2

m = 9792986822963146992114161946549377254001156012300083076259452975070903436656675903033418798369811004678022807932064872669773556983318074157606463933686225452143852071767552582367819932516654167400507310054793760473098421162463267
A = 246920531455433048826966670968977027196902794022573095007307132382393013927558904839982249967656424317118051446771969623490992917094197975459553923550187
B = 3120090466259654766880909097573553950487818021670727992039931232537173262599219376624291488340607228938989670215080876932583555412966984946786628621917436142053528648425399877486481618672307477414787846984446437445450282569184963
e = 4180488827

output = [263928838896714332657762314348602240455087661491500131260179929152321790693260683004004767933801216877412896467528419672112455669506824987777448696213888416333755744665868795853306879814179767910033263080874331851322593343273834, 7500716958005582985508201577146205078774368134456220390802616323312171951781595852608949532619393759348663684985174625019004577610546554994801687569942118260000292201829011312249563036393035204990811392856155820408283216493092108, 2577794401090299805723177598637436117371525412262771825236813936115237585602114357696686099541164980249580094089526387369627399445447896464668107355247993148990034255262021717192029828447047736912032562575292618672346226630177737, 9097092753543027532933159793556144814276134227405286080166556624316657274280165256861623248902541076900039285592392074751617153907616670295765377162951858063712964557527212039482031296350052367350738141716598584719951567052177519, 8174235910244322855637254130843352735528509191186418212056519911128301630950848710182451421471531481098828227735010211554839205099309290314993113489826162548089590990963249899714956197889959999884447438378454452096405595048394416, 2823506900640363315693941780283568096117331722098156706833610340919194199647098542170689133810904702849664199290565773405646243449194786656181872671323095023235608799444864036190997987871160063941897196360905342203429250068859314, 4625135637721297092934166648990860031642126233341589454312760229225192256970211899532356300747405146834048765116081788846632527090729839758895834854075755594692611781829177188955301784020596520269704429107749955107365380494152652]

known_start = b"good luck lmao ictf{"
known_chunks = [bytes_to_long(known_start[i:i+10]) for i in range(0, len(known_start), 10)]
keystreams = [output[i] ^ known_chunks[i] for i in range(len(known_chunks))]

solutions = [3223629359291819296, 1228725530983745536, 6290194781419687575, 10304742720644704896]
moduli = [10124460123717732576, 12017858281002457600, 15013023439701145678, 17297082179958074002]

print("=== CRT Manual ===\n")

# Implementación manual de CRT
def crt_manual(moduli, remainders):
    """Teorema Chino del Resto"""
    if len(moduli) != len(remainders):
        return None
    
    # Producto de todos los módulos
    M = 1
    for m in moduli:
        M *= m
    
    result = 0
    for i in range(len(moduli)):
        Mi = M // moduli[i]
        # Encontrar inverso de Mi mod moduli[i]
        inv = gmpy2.invert(Mi, moduli[i])
        result += remainders[i] * Mi * inv
    
    return result % M, M

x_combined, mod_combined = crt_manual(moduli, solutions)

print(f"CRT: x ≡ {x_combined} (mod {mod_combined})")
print()

# Verificar con m completo
print("Verificando...")
test_ks = pow(B, x_combined, m)
if test_ks == keystreams[0]:
    print("¡Verificación exitosa!")
    print(f"x_combined (state & ~0xffff) = {x_combined}")
else:
    print(f"Verificación falló directamente")
    print(f"B^x mod m = {test_ks}")
    print(f"keystream_0 = {keystreams[0]}")
    print()
    print("Probando múltiplos...")
    
    for k in range(1000):
        x_test = (x_combined + k * mod_combined) % m
        if pow(B, x_test, m) == keystreams[0]:
            print(f"¡Encontrado con k={k}!")
            x_combined = x_test
            break
    else:
        print("No se encontró solución con múltiplos")
        print("Probando con diferentes combinaciones...")
        # El problema podría ser que los módulos no son coprimos
        import math
        for i in range(len(moduli)):
            for j in range(i+1, len(moduli)):
                g = math.gcd(moduli[i], moduli[j])
                if g > 1:
                    print(f"  gcd(moduli[{i}], moduli[{j}]) = {g}")

print("\nBruteforceando los últimos 16 bits...")
for low_bits in range(65536):
    if low_bits % 10000 == 0:
        print(f"  Probando low_bits = {low_bits}...")
    
    state_0 = x_combined | low_bits
    
    # Verificar que genera el primer keystream
    ks0 = pow(B, state_0 & ~0xffff, m)
    if ks0 != keystreams[0]:
        continue
    
    # Calcular siguiente estado
    new_state = pow(pow(A, state_0, m) ^ B, e, m)
    ks1 = pow(B, new_state & ~0xffff, m)
    
    if ks1 == keystreams[1]:
        print(f"\n¡Estado inicial encontrado!")
        print(f"state_0 = {state_0}")
        print(f"low_bits = {low_bits}")
        
        # Descifrar
        state = state_0
        plaintext = b""
        for j in range(len(output)):
            ks = pow(B, state & ~0xffff, m)
            chunk = output[j] ^ ks
            chunk_bytes = long_to_bytes(chunk)
            if len(chunk_bytes) < 10:
                chunk_bytes = b'\x00' * (10 - len(chunk_bytes)) + chunk_bytes
            plaintext += chunk_bytes
            state = pow(pow(A, state, m) ^ B, e, m)
        
        plaintext = plaintext.rstrip(b'\x00')
        print(f"\nFlag: {plaintext.decode('latin1', errors='ignore')}")
        exit(0)

print("\nNo se encontró coincidencia en los últimos 16 bits :(")
