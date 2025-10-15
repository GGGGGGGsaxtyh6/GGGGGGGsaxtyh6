from Crypto.Util.number import long_to_bytes, bytes_to_long

# Valores del desafío
m = 9792986822963146992114161946549377254001156012300083076259452975070903436656675903033418798369811004678022807932064872669773556983318074157606463933686225452143852071767552582367819932516654167400507310054793760473098421162463267
A = 246920531455433048826966670968977027196902794022573095007307132382393013927558904839982249967656424317118051446771969623490992917094197975459553923550187 
B = 3120090466259654766880909097573553950487818021670727992039931232537173262599219376624291488340607228938989670215080876932583555412966984946786628621917436142053528648425399877486481618672307477414787846984446437445450282569184963
e = 4180488827

output = [263928838896714332657762314348602240455087661491500131260179929152321790693260683004004767933801216877412896467528419672112455669506824987777448696213888416333755744665868795853306879814179767910033263080874331851322593343273834, 7500716958005582985508201577146205078774368134456220390802616323312171951781595852608949532619393759348663684985174625019004577610546554994801687569942118260000292201829011312249563036393035204990811392856155820408283216493092108, 2577794401090299805723177598637436117371525412262771825236813936115237585602114357696686099541164980249580094089526387369627399445447896464668107355247993148990034255262021717192029828447047736912032562575292618672346226630177737, 9097092753543027532933159793556144814276134227405286080166556624316657274280165256861623248902541076900039285592392074751617153907616670295765377162951858063712964557527212039482031296350052367350738141716598584719951567052177519, 8174235910244322855637254130843352735528509191186418212056519911128301630950848710182451421471531481098828227735010211554839205099309290314993113489826162548089590990963249899714956197889959999884447438378454452096405595048394416, 2823506900640363315693941780283568096117331722098156706833610340919194199647098542170689133810904702849664199290565773405646243449194786656181872671323095023235608799444864036190997987871160063941897196360905342203429250068859314, 4625135637721297092934166648990860031642126233341589454312760229225192256970211899532356300747405146834048765116081788846632527090729839758895834854075755594692611781829177188955301784020596520269704429107749955107365380494152652]

# Plaintext conocido
known_prefix = b"good luck lmao ictf{"

chunk0_bytes = known_prefix[0:10]
plaintext0 = bytes_to_long(chunk0_bytes)
keystream0 = output[0] ^ plaintext0

chunk1_bytes = known_prefix[10:20]
plaintext1 = bytes_to_long(chunk1_bytes)
keystream1 = output[1] ^ plaintext1

# Resultados del discrete log
combined_result = 13604982860189876437154905325726720
combined_mod = 14095655317788782324839458519813926

print(f"(state & ~0xffff) ≡ {combined_result} (mod {combined_mod})")
print(f"Módulo: {combined_mod.bit_length()} bits")

# Calcular k para estado de ~700 bits
# state & ~0xffff = combined_result + k * combined_mod
# Queremos que esto sea aproximadamente 2^700

target_bits = 700
target_value = 2 ** target_bits

k_center = (target_value - combined_result) // combined_mod

print(f"\nPara ~{target_bits} bits, k ≈ {k_center}")
print(f"k tiene {k_center.bit_length()} bits")

# Buscar alrededor de k_center
print(f"\n=== Buscando alrededor de k = {k_center} ===\n")

search_range = 10000000  # Buscar +/- 10 millones

for k_offset in range(-search_range, search_range):
    k = k_center + k_offset
    
    if k < 0:
        continue
    
    state_high = combined_result + k * combined_mod
    
    # Verificar que tenga aproximadamente el número correcto de bits
    bits = state_high.bit_length()
    if bits < 684 or bits > 704:
        continue
    
    # Probar los 16 bits bajos
    for low_bits in range(65536):
        state0 = state_high | low_bits
        
        # Verificar con el primer keystream
        test_ks0 = pow(B, state0 & ~0xffff, m)
        
        if test_ks0 == keystream0:
            # Verificar con el segundo keystream
            state1 = pow(pow(A, state0, m) ^ B, e, m)
            test_ks1 = pow(B, state1 & ~0xffff, m)
            
            if test_ks1 == keystream1:
                print(f"\n✓✓✓ ESTADO ENCONTRADO ✓✓✓")
                print(f"k = {k}")
                print(f"state0 = {state0}")
                print(f"Bits: {state0.bit_length()}")
                
                # Descifrar
                state = state0
                plaintext = b""
                
                for out in output:
                    ks = pow(B, state & ~0xffff, m)
                    chunk = out ^ ks
                    plaintext += long_to_bytes(chunk)
                    state = pow(pow(A, state, m) ^ B, e, m)
                
                flag = plaintext.decode('utf-8', errors='ignore')
                print(f"\nFlag: {flag}")
                
                # Guardar la flag
                with open('/workspace/flag.txt', 'w') as f:
                    f.write(flag)
                
                exit(0)
    
    if k_offset % 100000 == 0:
        test_state = combined_result + k * combined_mod
        print(f"  k_offset = {k_offset:,}, k = {k}, bits = {test_state.bit_length()}")

print("\nNo encontrado en el rango de búsqueda")

# Intentar con otros rangos de bits
print("\n=== Probando con otros rangos de bits ===\n")

for target_bits in [695, 698, 699, 701, 702, 705]:
    print(f"\nProbando con {target_bits} bits...")
    
    target_value = 2 ** target_bits
    k_center = (target_value - combined_result) // combined_mod
    
    search_range = 1000000
    
    for k_offset in range(-search_range, search_range):
        k = k_center + k_offset
        
        if k < 0:
            continue
        
        state_high = combined_result + k * combined_mod
        bits = state_high.bit_length()
        
        if bits != target_bits:
            continue
        
        for low_bits in range(65536):
            state0 = state_high | low_bits
            
            test_ks0 = pow(B, state0 & ~0xffff, m)
            
            if test_ks0 == keystream0:
                state1 = pow(pow(A, state0, m) ^ B, e, m)
                test_ks1 = pow(B, state1 & ~0xffff, m)
                
                if test_ks1 == keystream1:
                    print(f"\n✓✓✓ ESTADO ENCONTRADO ✓✓✓")
                    
                    state = state0
                    plaintext = b""
                    
                    for out in output:
                        ks = pow(B, state & ~0xffff, m)
                        chunk = out ^ ks
                        plaintext += long_to_bytes(chunk)
                        state = pow(pow(A, state, m) ^ B, e, m)
                    
                    flag = plaintext.decode('utf-8', errors='ignore')
                    print(f"\nFlag: {flag}")
                    
                    with open('/workspace/flag.txt', 'w') as f:
                        f.write(flag)
                    
                    exit(0)
        
        if k_offset % 100000 == 0:
            print(f"  k_offset = {k_offset:,}")

print("\nNo encontrado")
