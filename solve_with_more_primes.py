from sympy.ntheory import discrete_log
from Crypto.Util.number import bytes_to_long, long_to_bytes
import gmpy2

B = 3120090466259654766880909097573553950487818021670727992039931232537173262599219376624291488340607228938989670215080876932583555412966984946786628621917436142053528648425399877486481618672307477414787846984446437445450282569184963
A = 246920531455433048826966670968977027196902794022573095007307132382393013927558904839982249967656424317118051446771969623490992917094197975459553923550187
e = 4180488827

primes = [10124460123717732577, 12017858281002457601, 15013023439701145679, 17297082179958074003]
p5 = 309938271107370186286857659422407283771865851657937731111744300310040346308690205006641245318085354895438500308814135783504803596134094206083383195557983
m = primes[0] * primes[1] * primes[2] * primes[3] * p5

output_list = [263928838896714332657762314348602240455087661491500131260179929152321790693260683004004767933801216877412896467528419672112455669506824987777448696213888416333755744665868795853306879814179767910033263080874331851322593343273834, 7500716958005582985508201577146205078774368134456220390802616323312171951781595852608949532619393759348663684985174625019004577610546554994801687569942118260000292201829011312249563036393035204990811392856155820408283216493092108, 2577794401090299805723177598637436117371525412262771825236813936115237585602114357696686099541164980249580094089526387369627399445447896464668107355247993148990034255262021717192029828447047736912032562575292618672346226630177737, 9097092753543027532933159793556144814276134227405286080166556624316657274280165256861623248902541076900039285592392074751617153907616670295765377162951858063712964557527212039482031296350052367350738141716598584719951567052177519, 8174235910244322855637254130843352735528509191186418212056519911128301630950848710182451421471531481098828227735010211554839205099309290314993113489826162548089590990963249899714956197889959999884447438378454452096405595048394416, 2823506900640363315693941780283568096117331722098156706833610340919194199647098542170689133810904702849664199290565773405646243449194786656181872671323095023235608799444864036190997987871160063941897196360905342203429250068859314, 4625135637721297092934166648990860031642126233341589454312760229225192256970211899532356300747405146834048765116081788846632527090729839758895834854075755594692611781829177188955301784020596520269704429107749955107365380494152652]

known_full = b"good luck lmao ictf{"
chunks_known = [bytes_to_long(known_full[i:i+10]) for i in range(0, len(known_full), 10)]
target = output_list[0] ^ chunks_known[0]

print("Calculando logaritmos discretos módulo todos los primos pequeños...\n")

logs = []
for i, p in enumerate(primes):
    print(f"Primo {i+1}/4: {p} ({p.bit_length()} bits)")
    try:
        result = discrete_log(p, target % p, B % p)
        print(f"  x ≡ {result} (mod {p-1})")
        logs.append((result, p-1))
    except Exception as e:
        print(f"  Error: {e}")
        break
    print()

if len(logs) == 4:
    print(f"¡{len(logs)} logaritmos calculados exitosamente!")
    print("\nCombinando con CRT generalizado...")
    
    # CRT generalizado para módulos que pueden no ser coprimos
    # Comenzar con el primer valor
    x = logs[0][0]
    modulo = logs[0][1]
    
    for i in range(1, len(logs)):
        r, n = logs[i]
        
        # Necesitamos encontrar y tal que:
        # y ≡ x (mod modulo)
        # y ≡ r (mod n)
        
        g = int(gmpy2.gcd(modulo, n))
        
        if (r - x) % g != 0:
            print(f"¡ERROR! Resultados inconsistentes entre log {i} y previos")
            break
        
        # Resolver: x + k*modulo ≡ r (mod n)
        # k*modulo ≡ r - x (mod n)
        # k ≡ (r - x) / modulo (mod n/g)
        
        modulo_red = modulo // g
        n_red = n // g
        diff = (r - x) // g
        
        inv = int(gmpy2.invert(modulo_red, n_red))
        k = (diff * inv) % n_red
        
        x = x + k * modulo
        modulo = (modulo * n) // g  # LCM
        
        print(f"  Después de incluir log {i+1}: x ≡ {x} (mod lcm(...))")
        print(f"  Módulo actual tiene {modulo.bit_length()} bits")
    
    print(f"\nResultado final CRT:")
    print(f"x ≡ {x} (mod {modulo})")
    print(f"x tiene {x.bit_length()} bits")
    print(f"Módulo tiene {modulo.bit_length()} bits")
    
    # Verificar
    print(f"\nVerificando...")
    test = pow(B, x, m)
    if test == target:
        print("¡VERIFICADO!")
    else:
        print("No verifica, probando múltiplos del módulo...")
        found = False
        for k in range(1000):
            test_x = x + k * modulo
            test = pow(B, test_x, m)
            if test == target:
                print(f"¡Encontrado con k={k}!")
                x = test_x
                found = True
                break
            if k % 100 == 0 and k > 0:
                print(f"  Probado hasta k={k}...")
        
        if not found:
            print("No encontrado en el rango")
    
    # Buscar últimos 16 bits
    if pow(B, x, m) == target:
        print(f"\nExponente encontrado: {x}")
        print(f"Buscando últimos 16 bits...")
        
        for low_bits in range(65536):
            full_state = x | low_bits
            temp_state = full_state
            match = True
            
            for i in range(min(2, len(chunks_known))):
                keystream = pow(B, temp_state - (temp_state & 0xffff), m)
                expected = output_list[i] ^ chunks_known[i]
                if keystream != expected:
                    match = False
                    break
                temp_state = pow(pow(A, temp_state, m) ^ B, e, m)
            
            if match:
                print(f"¡LOW BITS = {low_bits}!")
                
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
    print(f"Solo se calcularon {len(logs)} logaritmos")
