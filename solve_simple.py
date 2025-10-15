from Crypto.Util.number import long_to_bytes, bytes_to_long, inverse
import sympy
from sympy.ntheory.modular import crt

# Valores del desafío
m = 9792986822963146992114161946549377254001156012300083076259452975070903436656675903033418798369811004678022807932064872669773556983318074157606463933686225452143852071767552582367819932516654167400507310054793760473098421162463267
A = 246920531455433048826966670968977027196902794022573095007307132382393013927558904839982249967656424317118051446771969623490992917094197975459553923550187 
B = 3120090466259654766880909097573553950487818021670727992039931232537173262599219376624291488340607228938989670215080876932583555412966984946786628621917436142053528648425399877486481618672307477414787846984446437445450282569184963
e = 4180488827

output = [263928838896714332657762314348602240455087661491500131260179929152321790693260683004004767933801216877412896467528419672112455669506824987777448696213888416333755744665868795853306879814179767910033263080874331851322593343273834, 7500716958005582985508201577146205078774368134456220390802616323312171951781595852608949532619393759348663684985174625019004577610546554994801687569942118260000292201829011312249563036393035204990811392856155820408283216493092108, 2577794401090299805723177598637436117371525412262771825236813936115237585602114357696686099541164980249580094089526387369627399445447896464668107355247993148990034255262021717192029828447047736912032562575292618672346226630177737, 9097092753543027532933159793556144814276134227405286080166556624316657274280165256861623248902541076900039285592392074751617153907616670295765377162951858063712964557527212039482031296350052367350738141716598584719951567052177519, 8174235910244322855637254130843352735528509191186418212056519911128301630950848710182451421471531481098828227735010211554839205099309290314993113489826162548089590990963249899714956197889959999884447438378454452096405595048394416, 2823506900640363315693941780283568096117331722098156706833610340919194199647098542170689133810904702849664199290565773405646243449194786656181872671323095023235608799444864036190997987871160063941897196360905342203429250068859314, 4625135637721297092934166648990860031642126233341589454312760229225192256970211899532356300747405146834048765116081788846632527090729839758895834854075755594692611781829177188955301784020596520269704429107749955107365380494152652]

# Factores de m obtenidos de factordb (los 4 primeros son pequeños)
small_factors = [
    10124460123717732577,
    12017858281002457601,
    15013023439701145679,
    17297082179958074003
]

print("Calculando logaritmos discretos para factores pequeños...")

remainders = []
moduli = []

for i, p in enumerate(small_factors):
    print(f"\nFactor {i+1}/{len(small_factors)}: {p}")
    
    # Reducir módulo p
    B_p = B % p
    y_p = output[0] % p
    
    print(f"  Calculando discrete_log({y_p}, {B_p}) mod {p}")
    
    # Usar sympy para calcular discrete log
    try:
        x_p = sympy.ntheory.discrete_log(p, y_p, B_p)
        print(f"  Resultado: {x_p}")
        remainders.append(x_p)
        moduli.append(p - 1)
    except Exception as ex:
        print(f"  Error: {ex}")

print(f"\n\nSe calcularon {len(remainders)}/{len(small_factors)} logs")

if len(remainders) == len(small_factors):
    print("\nUsando CRT para combinar...")
    
    # El resultado será módulo lcm de los moduli
    result, mod = crt(moduli, remainders)
    
    print(f"Estado (módulo {mod}): {result}")
    print(f"Número de bits: {mod.bit_length()}")
    
    # Ahora necesitamos extender esto al valor completo
    # El estado tiene ~700 bits según el código
    # result es el valor módulo el producto de (p_i - 1)
    
    # Para cada posible valor de k, probamos state = result + k * mod
    # Pero también necesitamos probar los 16 bits bajos
    
    print("\nProbando diferentes valores del estado...")
    
    # Primero vamos a probar sin el factor grande, solo con combinaciones
    # de los factores pequeños
    
    max_k = 100  # Probaremos algunos valores de k
    
    for k in range(max_k):
        state_base = result + k * mod
        
        # Probar los 16 bits bajos
        for low_bits in range(min(65536, 1000)):  # Limitamos para no tardar mucho
            state_candidate = state_base + (low_bits << (state_base.bit_length() - 16))
            
            # Verificar
            test_output = pow(B, state_candidate - (state_candidate & 0xffff), m)
            
            if test_output == output[0]:
                print(f"\n✓ ENCONTRADO! Estado: {state_candidate}")
                
                # Descifrar
                state = state_candidate
                plaintext_chunks = []
                
                for out in output:
                    keystream = pow(B, state - (state & 0xffff), m)
                    chunk = out ^ keystream
                    plaintext_chunks.append(chunk)
                    
                    # Actualizar estado
                    new_state = pow(pow(A, state, m) ^ B, e, m)
                    state = new_state
                
                plaintext = b""
                for chunk in plaintext_chunks:
                    try:
                        chunk_bytes = long_to_bytes(chunk)
                        plaintext += chunk_bytes
                    except:
                        pass
                
                print(f"Plaintext: {plaintext}")
                exit(0)
        
        if k % 10 == 0:
            print(f"  Probado k={k}...")
    
    print("\nNo encontrado con este método. Necesitamos el factor grande también...")
else:
    print("\nNo se pudieron calcular suficientes discrete logs")
