from Crypto.Util.number import long_to_bytes, bytes_to_long, inverse, GCD
import sympy
from sympy.ntheory.modular import crt

# Valores del desafío
m = 9792986822963146992114161946549377254001156012300083076259452975070903436656675903033418798369811004678022807932064872669773556983318074157606463933686225452143852071767552582367819932516654167400507310054793760473098421162463267
A = 246920531455433048826966670968977027196902794022573095007307132382393013927558904839982249967656424317118051446771969623490992917094197975459553923550187 
B = 3120090466259654766880909097573553950487818021670727992039931232537173262599219376624291488340607228938989670215080876932583555412966984946786628621917436142053528648425399877486481618672307477414787846984446437445450282569184963
e = 4180488827

output = [263928838896714332657762314348602240455087661491500131260179929152321790693260683004004767933801216877412896467528419672112455669506824987777448696213888416333755744665868795853306879814179767910033263080874331851322593343273834, 7500716958005582985508201577146205078774368134456220390802616323312171951781595852608949532619393759348663684985174625019004577610546554994801687569942118260000292201829011312249563036393035204990811392856155820408283216493092108, 2577794401090299805723177598637436117371525412262771825236813936115237585602114357696686099541164980249580094089526387369627399445447896464668107355247993148990034255262021717192029828447047736912032562575292618672346226630177737, 9097092753543027532933159793556144814276134227405286080166556624316657274280165256861623248902541076900039285592392074751617153907616670295765377162951858063712964557527212039482031296350052367350738141716598584719951567052177519, 8174235910244322855637254130843352735528509191186418212056519911128301630950848710182451421471531481098828227735010211554839205099309290314993113489826162548089590990963249899714956197889959999884447438378454452096405595048394416, 2823506900640363315693941780283568096117331722098156706833610340919194199647098542170689133810904702849664199290565773405646243449194786656181872671323095023235608799444864036190997987871160063941897196360905342203429250068859314, 4625135637721297092934166648990860031642126233341589454312760229225192256970211899532356300747405146834048765116081788846632527090729839758895834854075755594692611781829177188955301784020596520269704429107749955107365380494152652]

# Factores de m
small_factors = [
    10124460123717732577,
    12017858281002457601,
    15013023439701145679,
    17297082179958074003
]

# Plaintext conocido
known_prefix = b"good luck lmao ictf{"

# Calcular keystre am para el primer chunk
chunk0_bytes = known_prefix[0:10]
plaintext0 = bytes_to_long(chunk0_bytes)
keystream0 = output[0] ^ plaintext0

print(f"Keystream0 = {keystream0}")

# Calcular keystream para el segundo chunk (para verificación)
chunk1_bytes = known_prefix[10:20]
plaintext1 = bytes_to_long(chunk1_bytes)
keystream1 = output[1] ^ plaintext1

print(f"Keystream1 = {keystream1}")

print("\n=== Calculando discrete logs ===")

def baby_step_giant_step(y, g, p, order):
    """
    Baby-step giant-step para discrete log
    """
    m = int(order ** 0.5) + 1
    
    # Baby steps: construir tabla
    table = {}
    g_power = 1
    for j in range(m):
        if g_power not in table:
            table[g_power] = j
        g_power = (g_power * g) % p
        
        if j % 1000000 == 0 and j > 0:
            print(f"    Baby step: {j}/{m}")
    
    # Giant steps
    factor = pow(g, -m, p)
    gamma = y
    
    for i in range(m):
        if gamma in table:
            result = i * m + table[gamma]
            return result
        gamma = (gamma * factor) % p
        
        if i % 1000000 == 0 and i > 0:
            print(f"    Giant step: {i}/{m}")
    
    return None

remainders = []
moduli = []

for idx, p in enumerate(small_factors):
    print(f"\nFactor {idx+1}/{len(small_factors)}: {p} ({p.bit_length()} bits)")
    
    B_p = B % p
    k_p = keystream0 % p
    
    # Orden del grupo es p-1
    order = p - 1
    
    print(f"  Calculando discrete log...")
    print(f"  Orden del grupo: {order} ({order.bit_length()} bits)")
    
    # Factorizar el orden para usar Pohlig-Hellman
    print(f"  Factorizando el orden...")
    order_factors = sympy.factorint(order)
    print(f"  Factores del orden: {order_factors}")
    
    # Si todos los factores son pequeños, Pohlig-Hellman será rápido
    max_factor = max(order_factors.keys())
    print(f"  Mayor factor primo: {max_factor} ({max_factor.bit_length()} bits)")
    
    if max_factor < 10**12:  # Si el factor más grande es < 2^40
        print(f"  Usando Pohlig-Hellman (factores pequeños)")
        
        try:
            # Implementación manual de Pohlig-Hellman
            dlogs = []
            mods = []
            
            for prime, power in order_factors.items():
                subgroup_order = prime ** power
                cofactor = order // subgroup_order
                
                # Reducir al subgrupo
                g_sub = pow(B_p, cofactor, p)
                y_sub = pow(k_p, cofactor, p)
                
                # Calcular discrete log en este subgrupo
                # Para potencias de primos, usar algoritmo específico
                if power == 1:
                    # Subgrupo de orden primo - usar BSGS
                    print(f"    Subgrupo primo {prime}")
                    if prime < 10**9:
                        x_sub = baby_step_giant_step(y_sub, g_sub, p, prime)
                        if x_sub is not None:
                            dlogs.append(x_sub)
                            mods.append(prime)
                            print(f"    ✓ x ≡ {x_sub} (mod {prime})")
                    else:
                        print(f"    ✗ Primo demasiado grande, saltando")
                else:
                    # Potencia de primo - más complejo
                    print(f"    Subgrupo {prime}^{power}, saltando por ahora")
            
            if dlogs:
                # Combinar usando CRT
                x_p, _ = crt(mods, dlogs)
                print(f"  ✓ Discrete log módulo p: {x_p}")
                remainders.append(x_p)
                moduli.append(order)
            else:
                print(f"  ✗ No se pudo calcular")
        except Exception as ex:
            print(f"  ✗ Error: {ex}")
            import traceback
            traceback.print_exc()
    else:
        print(f"  ✗ Factor primo demasiado grande ({max_factor}), saltando")

print(f"\n=== Resultados ===")
print(f"Calculados {len(remainders)}/{len(small_factors)} discrete logs")

if len(remainders) > 0:
    print(f"\nCombinando con CRT...")
    state_high_mod_small, combined_mod = crt(moduli, remainders)
    
    print(f"(state & ~0xffff) ≡ {state_high_mod_small} (mod {combined_mod})")
    print(f"Módulo combinado: {combined_mod.bit_length()} bits")
    
    # Ahora buscar el valor real
    print(f"\nBuscando valor completo del estado...")
    
    # state & ~0xffff = state_high_mod_small + k * combined_mod
    
    max_k = 1000000
    
    for k in range(max_k):
        state_high_bits = state_high_mod_small + k * combined_mod
        
        # Solo probar si el número de bits es razonable (alrededor de 700)
        if state_high_bits.bit_length() > 710:
            break
        
        # Probar los 16 bits bajos
        for low_bits in range(65536):
            state0 = state_high_bits | low_bits
            
            # Verificar
            test_keystream0 = pow(B, state0 & ~0xffff, m)
            
            if test_keystream0 == keystream0:
                # Verificar con el segundo chunk
                state1 = pow(pow(A, state0, m) ^ B, e, m)
                test_keystream1 = pow(B, state1 & ~0xffff, m)
                
                if test_keystream1 == keystream1:
                    print(f"\n✓✓✓ ESTADO INICIAL ENCONTRADO ✓✓✓")
                    print(f"state0 = {state0}")
                    
                    # Descifrar
                    state = state0
                    plaintext = b""
                    
                    for out in output:
                        keystream = pow(B, state & ~0xffff, m)
                        chunk = out ^ keystream
                        plaintext += long_to_bytes(chunk)
                        state = pow(pow(A, state, m) ^ B, e, m)
                    
                    print(f"\n{plaintext.decode('utf-8', errors='ignore')}")
                    exit(0)
        
        if k % 10000 == 0 and k > 0:
            print(f"  Probado k={k}, bits={state_high_bits.bit_length()}")
    
    print("\nNo encontrado")
else:
    print("\nNo se calcularon discrete logs")
