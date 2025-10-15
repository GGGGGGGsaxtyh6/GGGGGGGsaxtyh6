from Crypto.Util.number import long_to_bytes, bytes_to_long
from sympy.ntheory.modular import crt

# Valores del desafío
m = 9792986822963146992114161946549377254001156012300083076259452975070903436656675903033418798369811004678022807932064872669773556983318074157606463933686225452143852071767552582367819932516654167400507310054793760473098421162463267
A = 246920531455433048826966670968977027196902794022573095007307132382393013927558904839982249967656424317118051446771969623490992917094197975459553923550187 
B = 3120090466259654766880909097573553950487818021670727992039931232537173262599219376624291488340607228938989670215080876932583555412966984946786628621917436142053528648425399877486481618672307477414787846984446437445450282569184963
e = 4180488827

output = [263928838896714332657762314348602240455087661491500131260179929152321790693260683004004767933801216877412896467528419672112455669506824987777448696213888416333755744665868795853306879814179767910033263080874331851322593343273834, 7500716958005582985508201577146205078774368134456220390802616323312171951781595852608949532619393759348663684985174625019004577610546554994801687569942118260000292201829011312249563036393035204990811392856155820408283216493092108, 2577794401090299805723177598637436117371525412262771825236813936115237585602114357696686099541164980249580094089526387369627399445447896464668107355247993148990034255262021717192029828447047736912032562575292618672346226630177737, 9097092753543027532933159793556144814276134227405286080166556624316657274280165256861623248902541076900039285592392074751617153907616670295765377162951858063712964557527212039482031296350052367350738141716598584719951567052177519, 8174235910244322855637254130843352735528509191186418212056519911128301630950848710182451421471531481098828227735010211554839205099309290314993113489826162548089590990963249899714956197889959999884447438378454452096405595048394416, 2823506900640363315693941780283568096117331722098156706833610340919194199647098542170689133810904702849664199290565773405646243449194786656181872671323095023235608799444864036190997987871160063941897196360905342203429250068859314, 4625135637721297092934166648990860031642126233341589454312760229225192256970211899532356300747405146834048765116081788846632527090729839758895834854075755594692611781829177188955301784020596520269704429107749955107365380494152652]

# Plaintext conocido
known_prefix = b"good luck lmao ictf{"

# Calcular keystreams
chunk0_bytes = known_prefix[0:10]
plaintext0 = bytes_to_long(chunk0_bytes)
keystream0 = output[0] ^ plaintext0

chunk1_bytes = known_prefix[10:20]
plaintext1 = bytes_to_long(chunk1_bytes)
keystream1 = output[1] ^ plaintext1

print(f"Keystream0 = {keystream0}")
print(f"Keystream1 = {keystream1}")

# De los cálculos anteriores:
# Para p3: x ≡ 79822636 (mod 109205942)
# Combinado: x ≡ 371598437320 (mod 513595545226)

state_high_partial, combined_mod = crt([2, 54602971, 4703], [0, 25219665, 2031])

print(f"\n(state & ~0xffff) ≡ {state_high_partial} (mod {combined_mod})")
print(f"Módulo: {combined_mod} ({combined_mod.bit_length()} bits)")

# Ahora buscar el valor completo
# state & ~0xffff = state_high_partial + k * combined_mod
# El estado debe tener alrededor de 700 bits

print("\nBuscando estado completo...")

# El rango de k que debemos buscar es grande
# (state & ~0xffff) tiene alrededor de 700 bits
# combined_mod tiene 39 bits
# Entonces k puede ser hasta ~2^(700-39) = 2^661, que es demasiado

# Pero podemos usar el hecho de que conocemos dos chunks consecutivos
# para verificar rápidamente

# Una estrategia diferente: hacer búsqueda con incrementos más grandes
# y verificar cuando encontremos un candidato prometedor

# Probemos primero con valores de k alrededor de ciertos rangos

import random

# Intentar búsqueda aleatoria primero
print("\nProbando búsqueda aleatoria...")

trials = 1000000

for trial in range(trials):
    # Generar k aleatorio que resulte en un estado de ~700 bits
    target_bits = 684  # 700 - 16 (los bits bajos que probaremos después)
    k_bits = target_bits - combined_mod.bit_length()
    k = random.getrandbits(k_bits)
    
    state_high_bits = state_high_partial + k * combined_mod
    
    # Verificar que tenga el número correcto de bits (aproximadamente)
    if state_high_bits.bit_length() < 680 or state_high_bits.bit_length() > 690:
        continue
    
    # Probar los 16 bits bajos
    for low_bits in range(65536):
        state0 = state_high_bits | low_bits
        
        # Verificar con el primer keystream
        test_keystream0 = pow(B, state0 & ~0xffff, m)
        
        if test_keystream0 == keystream0:
            # ¡Posible candidato! Verificar con el segundo chunk
            state1 = pow(pow(A, state0, m) ^ B, e, m)
            test_keystream1 = pow(B, state1 & ~0xffff, m)
            
            if test_keystream1 == keystream1:
                print(f"\n✓✓✓ ESTADO ENCONTRADO ✓✓✓")
                print(f"k = {k}")
                print(f"state0 = {state0}")
                
                # Descifrar todo
                state = state0
                plaintext = b""
                
                for out in output:
                    keystream = pow(B, state & ~0xffff, m)
                    chunk = out ^ keystream
                    plaintext += long_to_bytes(chunk)
                    state = pow(pow(A, state, m) ^ B, e, m)
                
                print(f"\n{plaintext.decode('utf-8', errors='ignore')}")
                exit(0)
    
    if trial % 10000 == 0 and trial > 0:
        print(f"  Probado {trial} valores de k...")

print("\nNo encontrado con búsqueda aleatoria")

# Intentar búsqueda secuencial más sistemática
print("\nProbando búsqueda secuencial...")

# Como el estado inicial se genera con random.getrandbits(700)
# debería ser un número de aproximadamente 700 bits
# Vamos a buscar sistemáticamente alrededor de 2^699

target_value = 2 ** 699
k_start = (target_value - state_high_partial) // combined_mod

print(f"Comenzando búsqueda desde k ≈ {k_start}")

for k_offset in range(-100000, 100000):
    k = k_start + k_offset
    if k < 0:
        continue
    
    state_high_bits = state_high_partial + k * combined_mod
    
    # Probar solo si tiene el número correcto de bits
    if state_high_bits.bit_length() < 650 or state_high_bits.bit_length() > 705:
        continue
    
    for low_bits in range(65536):
        state0 = state_high_bits | low_bits
        
        test_keystream0 = pow(B, state0 & ~0xffff, m)
        
        if test_keystream0 == keystream0:
            state1 = pow(pow(A, state0, m) ^ B, e, m)
            test_keystream1 = pow(B, state1 & ~0xffff, m)
            
            if test_keystream1 == keystream1:
                print(f"\n✓✓✓ ESTADO ENCONTRADO ✓✓✓")
                print(f"k = {k}")
                print(f"state0 = {state0}")
                
                state = state0
                plaintext = b""
                
                for out in output:
                    keystream = pow(B, state & ~0xffff, m)
                    chunk = out ^ keystream
                    plaintext += long_to_bytes(chunk)
                    state = pow(pow(A, state, m) ^ B, e, m)
                
                print(f"\n{plaintext.decode('utf-8', errors='ignore')}")
                exit(0)
    
    if k_offset % 10000 == 0:
        print(f"  k_offset = {k_offset}, bits = {state_high_bits.bit_length()}")

print("\nNo encontrado")
