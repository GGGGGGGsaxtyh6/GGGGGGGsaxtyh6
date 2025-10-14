from Crypto.Util.number import *
import gmpy2

# Parámetros
p1 = 10124460123717732577
p2 = 12017858281002457601
p3 = 15013023439701145679
p4 = 17297082179958074003
p5 = 309938271107370186286857659422407283771865851657937731111744300310040346308690205006641245318085354895438500308814135783504803596134094206083383195557983

m = p1 * p2 * p3 * p4 * p5
A = 246920531455433048826966670968977027196902794022573095007307132382393013927558904839982249967656424317118051446771969623490992917094197975459553923550187
B = 3120090466259654766880909097573553950487818021670727992039931232537173262599219376624291488340607228938989670215080876932583555412966984946786628621917436142053528648425399877486481618672307477414787846984446437445450282569184963
e = 4180488827

output = [263928838896714332657762314348602240455087661491500131260179929152321790693260683004004767933801216877412896467528419672112455669506824987777448696213888416333755744665868795853306879814179767910033263080874331851322593343273834, 7500716958005582985508201577146205078774368134456220390802616323312171951781595852608949532619393759348663684985174625019004577610546554994801687569942118260000292201829011312249563036393035204990811392856155820408283216493092108, 2577794401090299805723177598637436117371525412262771825236813936115237585602114357696686099541164980249580094089526387369627399445447896464668107355247993148990034255262021717192029828447047736912032562575292618672346226630177737, 9097092753543027532933159793556144814276134227405286080166556624316657274280165256861623248902541076900039285592392074751617153907616670295765377162951858063712964557527212039482031296350052367350738141716598584719951567052177519, 8174235910244322855637254130843352735528509191186418212056519911128301630950848710182451421471531481098828227735010211554839205099309290314993113489826162548089590990963249899714956197889959999884447438378454452096405595048394416, 2823506900640363315693941780283568096117331722098156706833610340919194199647098542170689133810904702849664199290565773405646243449194786656181872671323095023235608799444864036190997987871160063941897196360905342203429250068859314, 4625135637721297092934166648990860031642126233341589454312760229225192256970211899532356300747405146834048765116081788846632527090729839758895834854075755594692611781829177188955301784020596520269704429107749955107365380494152652]

known_prefix = b"good luck lmao ictf{"
chunks = [bytes_to_long(known_prefix[i:i+10]) for i in range(0, len(known_prefix), 10)]

print("ENFOQUE FINAL: Bruteforce en espacio reducido con verificación de múltiples outputs")
print()

# Calcular targets
targets = []
for i in range(min(len(chunks), len(output))):
    target = output[i] ^ chunks[i]
    targets.append(target)
    print(f"Target {i}: B^(state_{i} >> 16 << 16) ≡ {hex(target)[:50]}... (mod m)")

print()
print("Asumiendo que el estado inicial tiene pocos bits significativos...")
print("Probando con estados de diferentes tamaños...")
print()

# Calcular el inverso de e
phi_m = (p1-1) * (p2-1) * (p3-1) * (p4-1) * (p5-1)
d = int(gmpy2.invert(e, phi_m))

# Función para simular el PRNG
def simulate_prng(initial_state, num_outputs):
    state = initial_state
    outputs = []
    for _ in range(num_outputs):
        keystream = pow(B, state - (state & 0xffff), m)
        outputs.append(keystream)
        # Actualizar estado
        new_state = pow(pow(A, state, m) ^ B, e, m)
        state = new_state
    return outputs

# Bruteforce con estados pequeños, probando con chunks de bits
for nbits_high in [16, 20, 24, 28, 30, 32]:
    print(f"\n=== Probando con (state >> 16) de {nbits_high} bits ===")
    print(f"Esto significa state total de hasta {nbits_high + 16} bits")
    
    max_high = 2**nbits_high
    step = max(1, max_high // 5000000)  # Muestrear para no exceder timeout
    
    for state_high in range(0, max_high, step):
        # state = (state_high << 16) | state_low
        # Pero como output elimina state_low, podemos probar con state_low = 0
        state = state_high << 16
        
        # Verificar contra el primer target
        test0 = pow(B, state, m)
        
        if test0 == targets[0]:
            print(f"\n¡MATCH EN PRIMER OUTPUT!")
            print(f"state_high = {state_high}, state (con low=0) = {state}")
            
            # Verificar con todos los outputs
            simulated = simulate_prng(state, len(targets))
            if simulated == targets:
                print(f"\n¡¡¡TODOS LOS OUTPUTS COINCIDEN!!!")
                print(f"Estado inicial encontrado: {state}")
                
                # Descifrar el mensaje completo
                plaintext = b""
                temp_state = state
                for out in output:
                    keystream = pow(B, temp_state - (temp_state & 0xffff), m)
                    chunk_val = out ^ keystream
                    chunk_bytes = long_to_bytes(chunk_val)
                    if len(chunk_bytes) <= 10:
                        plaintext += chunk_bytes
                    temp_state = pow(pow(A, temp_state, m) ^ B, e, m)
                
                print(f"\n{'='*60}")
                print(f"PLAINTEXT COMPLETO:")
                print(plaintext)
                print(f"{'='*60}")
                exit(0)
            else:
                # Ver cuántos coinciden
                matches = sum(1 for i, j in zip(simulated, targets) if i == j)
                if matches > 1:
                    print(f"  Coinciden {matches}/{len(targets)} outputs")
                    print(f"  Probando con diferentes low_bits...")
                    
                    # Intentar diferentes valores de low bits
                    for low_bits in range(65536):
                        test_state = state | low_bits
                        simulated2 = simulate_prng(test_state, len(targets))
                        if simulated2 == targets:
                            print(f"\n¡ENCONTRADO con low_bits={low_bits}!")
                            print(f"Estado inicial: {test_state}")
                            
                            # Descifrar
                            plaintext = b""
                            temp_state = test_state
                            for out in output:
                                keystream = pow(B, temp_state - (temp_state & 0xffff), m)
                                chunk_val = out ^ keystream
                                chunk_bytes = long_to_bytes(chunk_val)
                                if len(chunk_bytes) <= 10:
                                    plaintext += chunk_bytes
                                temp_state = pow(pow(A, temp_state, m) ^ B, e, m)
                            
                            print(f"\n{'='*60}")
                            print(f"PLAINTEXT COMPLETO:")
                            print(plaintext)
                            print(f"{'='*60}")
                            exit(0)
        
        if state_high % 100000 == 0 and state_high > 0:
            print(f"  Probado {state_high}/{max_high}... (step={step})")

print("\nNo encontrado. El estado debe ser más complejo.")
