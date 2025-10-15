from Crypto.Util.number import long_to_bytes, bytes_to_long
from sympy.ntheory.modular import crt

m = 9792986822963146992114161946549377254001156012300083076259452975070903436656675903033418798369811004678022807932064872669773556983318074157606463933686225452143852071767552582367819932516654167400507310054793760473098421162463267
A = 246920531455433048826966670968977027196902794022573095007307132382393013927558904839982249967656424317118051446771969623490992917094197975459553923550187 
B = 3120090466259654766880909097573553950487818021670727992039931232537173262599219376624291488340607228938989670215080876932583555412966984946786628621917436142053528648425399877486481618672307477414787846984446437445450282569184963
e = 4180488827

output = [263928838896714332657762314348602240455087661491500131260179929152321790693260683004004767933801216877412896467528419672112455669506824987777448696213888416333755744665868795853306879814179767910033263080874331851322593343273834, 7500716958005582985508201577146205078774368134456220390802616323312171951781595852608949532619393759348663684985174625019004577610546554994801687569942118260000292201829011312249563036393035204990811392856155820408283216493092108, 2577794401090299805723177598637436117371525412262771825236813936115237585602114357696686099541164980249580094089526387369627399445447896464668107355247993148990034255262021717192029828447047736912032562575292618672346226630177737, 9097092753543027532933159793556144814276134227405286080166556624316657274280165256861623248902541076900039285592392074751617153907616670295765377162951858063712964557527212039482031296350052367350738141716598584719951567052177519, 8174235910244322855637254130843352735528509191186418212056519911128301630950848710182451421471531481098828227735010211554839205099309290314993113489826162548089590990963249899714956197889959999884447438378454452096405595048394416, 2823506900640363315693941780283568096117331722098156706833610340919194199647098542170689133810904702849664199290565773405646243449194786656181872671323095023235608799444864036190997987871160063941897196360905342203429250068859314, 4625135637721297092934166648990860031642126233341589454312760229225192256970211899532356300747405146834048765116081788846632527090729839758895834854075755594692611781829177188955301784020596520269704429107749955107365380494152652]

known_prefix = b"good luck lmao ictf{"
chunk0_bytes = known_prefix[0:10]
plaintext0 = bytes_to_long(chunk0_bytes)
keystream0 = output[0] ^ plaintext0
chunk1_bytes = known_prefix[10:20]
plaintext1 = bytes_to_long(chunk1_bytes)
keystream1 = output[1] ^ plaintext1

# Factor grande y sus factores de p-1
large_p = 309938271107370186286857659422407283771865851657937731111744300310040346308690205006641245318085354895438500308814135783504803596134094206083383195557983
p_minus_1_factors = [2, 4037763841, 2397855853, 3620826301, 2910483473, 2916502123, 3313236013, 3686460431, 2689451797, 2329072073, 2334352403, 3842612131, 4241347379, 3978903371, 4078375243, 4271283073, 2581259777]

print("=== Calculando discrete log para el factor grande ===")
print(f"Factor: {large_p} ({large_p.bit_length()} bits)")

B_p = B % large_p
k_p = keystream0 % large_p

def bsgs_small(y, g, p, order):
    m = int(order ** 0.5) + 1
    table = {}
    g_power = 1
    for j in range(m):
        table[g_power] = j
        g_power = (g_power * g) % p
    factor = pow(g, -m, p)
    gamma = y
    for i in range(m):
        if gamma in table:
            return i * m + table[gamma]
        gamma = (gamma * factor) % p
    return None

print(f"\nAplicando Pohlig-Hellman...")

dlogs = []
mods = []

for prime in p_minus_1_factors:
    print(f"  Subgrupo {prime}...", end=" ")
    cofactor = (large_p - 1) // prime
    g_sub = pow(B_p, cofactor, large_p)
    y_sub = pow(k_p, cofactor, large_p)
    x_sub = bsgs_small(y_sub, g_sub, large_p, prime)
    if x_sub is not None:
        print(f"✓ x ≡ {x_sub} (mod {prime})")
        dlogs.append(x_sub)
        mods.append(prime)
    else:
        print(f"✗")

print(f"\n✓ Calculados {len(dlogs)}/{len(p_minus_1_factors)} discrete logs")

if len(dlogs) == len(p_minus_1_factors):
    x_large, _ = crt(mods, dlogs)
    print(f"\nDiscrete log completo para factor grande:")
    print(f"  x = {x_large}")
    
    # Combinar con los resultados anteriores
    print(f"\n=== Combinando todos los factores ===")
    
    # De antes tenemos:
    # Para p=15013023439701145679: x = 13796706501270260414
    # Para p=12017858281002457601: x ≡ 650637893806900 (mod 938895178203317)
    
    p2 = 12017858281002457601
    p3 = 15013023439701145679
    
    x2_partial = 650637893806900
    mod2_partial = 938895178203317
    x3 = 13796706501270260414
    
    # Combinar los tres
    final_result, final_mod = crt(
        [large_p - 1, p3 - 1, mod2_partial],
        [x_large, x3, x2_partial]
    )
    
    print(f"\n(state & ~0xffff) ≡ {final_result} (mod {final_mod})")
    print(f"Módulo final: {final_mod.bit_length()} bits")
    
    # Ahora el módulo es mucho más grande, así que la búsqueda será mucho más pequeña
    print(f"\n=== Buscando estado completo ===")
    
    # Para un estado de ~700 bits
    for target_bits in range(695, 705):
        target_value = 2 ** target_bits
        k = (target_value - final_result) // final_mod
        
        for k_offset in range(-10, 11):
            k_test = k + k_offset
            if k_test < 0:
                continue
            
            state_high = final_result + k_test * final_mod
            
            if state_high.bit_length() != target_bits:
                continue
            
            for low_bits in range(65536):
                state0 = state_high | low_bits
                
                test_ks0 = pow(B, state0 & ~0xffff, m)
                
                if test_ks0 == keystream0:
                    state1 = pow(pow(A, state0, m) ^ B, e, m)
                    test_ks1 = pow(B, state1 & ~0xffff, m)
                    
                    if test_ks1 == keystream1:
                        print(f"\n✓✓✓ ENCONTRADO ✓✓✓")
                        
                        state = state0
                        plaintext = b""
                        
                        for out in output:
                            ks = pow(B, state & ~0xffff, m)
                            chunk = out ^ ks
                            plaintext += long_to_bytes(chunk)
                            state = pow(pow(A, state, m) ^ B, e, m)
                        
                        print(plaintext.decode('utf-8', errors='ignore'))
                        exit(0)
        
        print(f"  Probado {target_bits} bits")
    
    print("\nNo encontrado en rango básico")
else:
    print("\nError calculando discrete logs")
