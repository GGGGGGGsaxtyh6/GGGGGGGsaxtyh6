from Crypto.Util.number import long_to_bytes, bytes_to_long, inverse, GCD
import sympy

# Valores del desafío
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

# Calcular phi(m)
phi_m = 1
for f in factors:
    phi_m *= (f - 1)

e_inv = inverse(e, phi_m)

print("=== Análisis del backdoor ===\n")

# El backdoor está en:
# 1. Solo se usan los bits altos del estado (se ignoran los últimos 16 bits)
# 2. new_state = ((A^state XOR B)^e) mod m

# Si conocemos dos estados consecutivos, podemos verificar
# Pero el problema es que solo conocemos B^(state & ~0xffff)

# Idea: ¿Qué pasa si hay una relación entre A^state XOR B y algo conocido?

# Veamos si podemos encontrar una relación entre el plaintext y el estado
# El plaintext comienza con "good luck lmao ictf{"

known_prefix = b"good luck lmao ictf{"
print(f"Prefix conocido: {known_prefix}")
print(f"Longitud: {len(known_prefix)} bytes")

# El cifrado divide en chunks de 10 bytes
chunk_size = 10
num_chunks = (len(known_prefix) + chunk_size - 1) // chunk_size
print(f"Número de chunks en el prefix: {num_chunks}")

# Para cada chunk, tenemos:
# encrypted_chunk = plaintext_chunk XOR B^(state & ~0xffff)

# Si conocemos el plaintext, podemos calcular B^(state & ~0xffff)!
print("\n=== Recuperando valores de B^(state & ~0xffff) ===\n")

for i in range(min(num_chunks, len(output))):
    chunk_start = i * chunk_size
    chunk_end = min(chunk_start + chunk_size, len(known_prefix))
    chunk_bytes = known_prefix[chunk_start:chunk_end]
    
    # Rellenar con ceros si es necesario (aunque probablemente no)
    if len(chunk_bytes) < chunk_size:
        chunk_bytes = chunk_bytes + b'\x00' * (chunk_size - len(chunk_bytes))
    
    plaintext_chunk = bytes_to_long(chunk_bytes)
    encrypted_chunk = output[i]
    
    # encrypted = plaintext XOR keystream
    # keystream = encrypted XOR plaintext
    keystream = encrypted_chunk ^ plaintext_chunk
    
    print(f"Chunk {i}:")
    print(f"  Plaintext: {chunk_bytes}")
    print(f"  Plaintext (long): {plaintext_chunk}")
    print(f"  Encrypted: {encrypted_chunk}")
    print(f"  Keystream (B^(state & ~0xffff)): {keystream}")
    
    # Ahora keystream = B^x mod m, donde x = state & ~0xffff
    # Necesitamos calcular x usando discrete log
    # Pero sabemos que x es múltiplo de 2^16
    
    # Una vez que tenemos x, necesitamos probar los 16 bits bajos

print("\n=== Estrategia ===")
print("1. Para el primer chunk, sabemos que keystream = B^(state & ~0xffff) mod m")
print("2. Necesitamos calcular log_B(keystream) mod m para obtener (state & ~0xffff)")
print("3. Luego probar fuerza bruta sobre los 16 bits bajos")
print("4. Verificar calculando el siguiente estado y comparando con el segundo chunk")

# El problema es que calcular discrete log es difícil
# Pero... ¿y si hay una forma de evitarlo?

# Espera! Veamos si e tiene alguna relación especial con 2^16

print(f"\n=== Relación con 2^16 ===")
print(f"2^16 = {2**16}")
print(f"e mod 2^16 = {e % (2**16)}")
print(f"GCD(e, 2^16) = {GCD(e, 2**16)}")

# ¿Qué pasa si intentamos un enfoque diferente?
# Sabemos que el estado inicial tiene ~700 bits
# Y se generan con random.getrandbits(700)

# Pero el output solo revela (state & ~0xffff) a través de discrete log

# Otra idea: ¿Podemos usar el hecho de que tenemos múltiples outputs?
# Si conociéramos state_0, podríamos calcular state_1, state_2, etc.
# Y verificar contra los outputs

print("\n=== Probando approach de búsqueda con el prefix conocido ===")

# Calculemos el keystream para el primer chunk
chunk0_bytes = known_prefix[0:10]
plaintext0 = bytes_to_long(chunk0_bytes)
keystream0 = output[0] ^ plaintext0

print(f"\nKeystream0 = {keystream0}")
print(f"Esto debe ser igual a B^(state0 & ~0xffff) mod m")

# Vamos a intentar calcular el discrete log usando solo los factores pequeños
# y luego extrapolar

print("\nCalculando discrete log módulo factores pequeños...")

from sympy.ntheory.modular import crt

small_factors_list = factors[:4]  # Solo los 4 factores pequeños
print(f"Usando {len(small_factors_list)} factores pequeños")

remainders = []
moduli = []

for idx, p in enumerate(small_factors_list):
    print(f"\nFactor {idx+1}: {p} ({p.bit_length()} bits)")
    
    B_p = B % p
    k_p = keystream0 % p
    
    print(f"  Calculando discrete_log({k_p}, {B_p}) mod {p}")
    
    try:
        # Usar sympy discrete_log
        x_p = sympy.ntheory.discrete_log(p, k_p, B_p, order=p-1)
        print(f"  ✓ Resultado: {x_p}")
        remainders.append(x_p)
        moduli.append(p - 1)
    except Exception as ex:
        print(f"  ✗ Error: {ex}")
        break

if len(remainders) == len(small_factors_list):
    print(f"\n✓ Calculados todos los discrete logs!")
    print(f"\nUsando CRT...")
    
    result_state_high, result_mod = crt(moduli, remainders)
    
    print(f"\nResultado CRT:")
    print(f"  (state & ~0xffff) ≡ {result_state_high} (mod {result_mod})")
    print(f"  Módulo tiene {result_mod.bit_length()} bits")
    
    # Ahora necesitamos encontrar el valor completo
    # state & ~0xffff = result_state_high + k * result_mod para algún k
    
    print(f"\nProbando diferentes valores de k...")
    
    # El estado original tiene ~700 bits
    # result_mod tiene ~64 bits de cada factor, total ~256 bits
    # Así que k puede ser bastante grande
    
    # Pero podemos usar el segundo chunk para verificar!
    
    chunk1_bytes = known_prefix[10:20]
    plaintext1 = bytes_to_long(chunk1_bytes)
    keystream1 = output[1] ^ plaintext1
    
    print(f"\nKeystream1 (para verificación): {keystream1}")
    
    # Limitemos k a un rango razonable
    max_k = 100000
    
    for k in range(max_k):
        state_high_bits = result_state_high + k * result_mod
        
        # Probar los 16 bits bajos
        for low_bits in range(65536):
            state0 = state_high_bits | low_bits
            
            # Verificar que produce el keystream correcto
            test_keystream0 = pow(B, state0 & ~0xffff, m)
            
            if test_keystream0 == keystream0:
                # ¡Verificación adicional con el segundo chunk!
                # Calcular state1
                state1 = pow(pow(A, state0, m) ^ B, e, m)
                test_keystream1 = pow(B, state1 & ~0xffff, m)
                
                if test_keystream1 == keystream1:
                    print(f"\n✓✓✓ ESTADO INICIAL ENCONTRADO! ✓✓✓")
                    print(f"state0 = {state0}")
                    
                    # Descifrar toda la flag
                    state = state0
                    plaintext_chunks = []
                    
                    for out in output:
                        keystream = pow(B, state & ~0xffff, m)
                        chunk = out ^ keystream
                        plaintext_chunks.append(chunk)
                        
                        # Actualizar estado
                        state = pow(pow(A, state, m) ^ B, e, m)
                    
                    plaintext = b""
                    for chunk in plaintext_chunks:
                        try:
                            plaintext += long_to_bytes(chunk)
                        except:
                            pass
                    
                    print(f"\nFLAG: {plaintext.decode('utf-8', errors='ignore')}")
                    exit(0)
        
        if k % 1000 == 0:
            print(f"  Probado k={k}...")
    
    print("\nNo encontrado en el rango de búsqueda")
else:
    print(f"\nSolo se calcularon {len(remainders)}/{len(small_factors_list)} discrete logs")
