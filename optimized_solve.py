from Crypto.Util.number import *
import gmpy2

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

# Known plaintext
known_start = b"good luck lmao ictf{"
known_chunks = [bytes_to_long(known_start[i:i+10]) for i in range(0, len(known_start), 10)]
keystreams = [output[i] ^ known_chunks[i] for i in range(len(known_chunks))]

print("=== Baby-Step Giant-Step para factores pequeños ===\n")

def baby_step_giant_step(g, h, p, max_n=None):
    """
    Resuelve g^x = h (mod p) usando baby-step giant-step
    Asume que la solución está en [0, max_n) si se proporciona max_n
    """
    if max_n is None:
        max_n = p - 1
    
    m = int(gmpy2.isqrt(max_n)) + 1
    
    # Baby step: construir tabla {g^j : j} para j = 0, 1, ..., m-1
    print(f"    Baby step: construyendo tabla de tamaño {m}...")
    table = {}
    g_power = 1
    for j in range(m):
        if g_power == h:
            return j
        table[g_power] = j
        g_power = (g_power * g) % p
        if j % 100000 == 0 and j > 0:
            print(f"      {j} entradas...")
    
    # Giant step: calcular g^(-m) y buscar
    print(f"    Giant step...")
    g_inv_m = pow(g, -m, p)
    gamma = h
    for i in range(m):
        if gamma in table:
            x = i * m + table[gamma]
            print(f"    ¡Solución encontrada!: x = {x}")
            return x
        gamma = (gamma * g_inv_m) % p
        if i % 10000 == 0 and i > 0:
            print(f"      Iteración {i}...")
    
    return None

keystream_0 = keystreams[0]

solutions = []
moduli = []

for i, p in enumerate(factors[:4]):  # Primero probar con los 4 factores pequeños
    print(f"Factor {i+1}: p = {p} ({p.bit_length()} bits)")
    
    B_mod_p = B % p
    ks_mod_p = keystream_0 % p
    
    print(f"  Resolviendo B^x ≡ {ks_mod_p} (mod {p})")
    
    # Baby-step giant-step
    x = baby_step_giant_step(B_mod_p, ks_mod_p, p, max_n=p-1)
    
    if x is not None:
        # Verificar
        if pow(B_mod_p, x, p) == ks_mod_p:
            print(f"  Verificado: B^{x} ≡ keystream (mod {p})")
            solutions.append(x)
            moduli.append(p - 1)
        else:
            print(f"  Error en verificación")
    else:
        print(f"  No se encontró solución")
    
    print()

if len(solutions) >= 2:
    print(f"Soluciones encontradas para {len(solutions)} factores")
    print("Intentando reconstruir el estado usando las soluciones parciales...")
    
    # Usar CRT chino para combinar
    from sympy.ntheory.modular import crt
    
    x_combined, mod_combined = crt(moduli, solutions)
    print(f"CRT: x ≡ {x_combined} (mod {mod_combined})")
    print()
    
    # El problema es que necesitamos la solución mod phi(m), no mod lcm de los (pi-1)
    # Pero podemos probar diferentes candidatos
    
    print("Probando candidatos...")
    
    # Probar múltiplos de la solución combinada
    for k in range(100):
        x_candidate = x_combined + k * mod_combined
        
        # Ver si este x da el keystream correcto
        test_ks = pow(B, x_candidate, m)
        if test_ks == keystream_0:
            print(f"¡Candidato válido encontrado!: x = {x_candidate}")
            
            # Ahora bruteforcear los últimos 16 bits
            print("Buscando los últimos 16 bits...")
            for low_bits in range(65536):
                state_0 = x_candidate | low_bits
                
                # Calcular siguiente estado
                new_state = pow(pow(A, state_0, m) ^ B, e, m)
                ks1_test = pow(B, new_state & ~0xffff, m)
                
                if ks1_test == keystreams[1]:
                    print(f"¡Estado inicial encontrado!: {state_0}")
                    
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
                    print(f"\nFlag: {plaintext.decode('latin1')}")
                    exit(0)
