from Crypto.Util.number import long_to_bytes, bytes_to_long
from sympy.ntheory.modular import crt
import sympy

# Valores del desafío
m = 9792986822963146992114161946549377254001156012300083076259452975070903436656675903033418798369811004678022807932064872669773556983318074157606463933686225452143852071767552582367819932516654167400507310054793760473098421162463267
A = 246920531455433048826966670968977027196902794022573095007307132382393013927558904839982249967656424317118051446771969623490992917094197975459553923550187 
B = 3120090466259654766880909097573553950487818021670727992039931232537173262599219376624291488340607228938989670215080876932583555412966984946786628621917436142053528648425399877486481618672307477414787846984446437445450282569184963
e = 4180488827

output = [263928838896714332657762314348602240455087661491500131260179929152321790693260683004004767933801216877412896467528419672112455669506824987777448696213888416333755744665868795853306879814179767910033263080874331851322593343273834, 7500716958005582985508201577146205078774368134456220390802616323312171951781595852608949532619393759348663684985174625019004577610546554994801687569942118260000292201829011312249563036393035204990811392856155820408283216493092108, 2577794401090299805723177598637436117371525412262771825236813936115237585602114357696686099541164980249580094089526387369627399445447896464668107355247993148990034255262021717192029828447047736912032562575292618672346226630177737, 9097092753543027532933159793556144814276134227405286080166556624316657274280165256861623248902541076900039285592392074751617153907616670295765377162951858063712964557527212039482031296350052367350738141716598584719951567052177519, 8174235910244322855637254130843352735528509191186418212056519911128301630950848710182451421471531481098828227735010211554839205099309290314993113489826162548089590990963249899714956197889959999884447438378454452096405595048394416, 2823506900640363315693941780283568096117331722098156706833610340919194199647098542170689133810904702849664199290565773405646243449194786656181872671323095023235608799444864036190997987871160063941897196360905342203429250068859314, 4625135637721297092934166648990860031642126233341589454312760229225192256970211899532356300747405146834048765116081788846632527090729839758895834854075755594692611781829177188955301784020596520269704429107749955107365380494152652]

# Factores pequeños de m
small_factors = [
    12017858281002457601,  # Tiene un factor de 199637503339 (38 bits) - factible con BSGS
    15013023439701145679   # Tiene un factor de 137474419109 (38 bits) - factible con BSGS
]

# Plaintext conocido
known_prefix = b"good luck lmao ictf{"

chunk0_bytes = known_prefix[0:10]
plaintext0 = bytes_to_long(chunk0_bytes)
keystream0 = output[0] ^ plaintext0

chunk1_bytes = known_prefix[10:20]
plaintext1 = bytes_to_long(chunk1_bytes)
keystream1 = output[1] ^ plaintext1

print("=== Calculando discrete logs con BSGS para factores medianos ===\n")

def bsgs(y, g, p, order):
    """Baby-step giant-step mejorado"""
    m = int(order ** 0.5) + 1
    
    print(f"    BSGS: m = {m:,}")
    
    # Baby steps
    table = {}
    g_power = 1
    for j in range(m):
        table[g_power] = j
        g_power = (g_power * g) % p
        
        if j > 0 and j % 5000000 == 0:
            print(f"    Baby steps: {j:,}/{m:,}")
    
    print(f"    Tabla construida con {len(table):,} entradas")
    
    # Giant steps
    factor = pow(g, -m, p)
    gamma = y
    
    for i in range(m):
        if gamma in table:
            return i * m + table[gamma]
        gamma = (gamma * factor) % p
        
        if i > 0 and i % 5000000 == 0:
            print(f"    Giant steps: {i:,}/{m:,}")
    
    return None

# Procesar solo el segundo factor que tiene factores manejables
p = small_factors[1]  # 15013023439701145679

print(f"Usando factor: {p}")

B_p = B % p
k_p = keystream0 % p

order = p - 1
print(f"Orden: {order}")

# Factorizar el orden
print(f"Factorizando orden...")
order_factors = sympy.factorint(order)
print(f"Factores: {order_factors}")

# Factores: {2: 1, 54602971: 1, 137474419109: 1}

print("\n=== Aplicando Poh lig-Hellman ===\n")

dlogs_partial = []
mods_partial = []

# Subgrupo de orden 2
print("Subgrupo de orden 2:")
cofactor = order // 2
g_sub = pow(B_p, cofactor, p)
y_sub = pow(k_p, cofactor, p)

if y_sub == 1:
    x_sub = 0
elif y_sub == g_sub:
    x_sub = 1
else:
    x_sub = None

if x_sub is not None:
    print(f"  x ≡ {x_sub} (mod 2)")
    dlogs_partial.append(x_sub)
    mods_partial.append(2)

# Subgrupo de orden 54602971
print("\nSubgrupo de orden 54602971:")
cofactor = order // 54602971
g_sub = pow(B_p, cofactor, p)
y_sub = pow(k_p, cofactor, p)

print(f"  Calculando BSGS...")
x_sub = bsgs(y_sub, g_sub, p, 54602971)

if x_sub is not None:
    print(f"  ✓ x ≡ {x_sub} (mod 54602971)")
    dlogs_partial.append(x_sub)
    mods_partial.append(54602971)
else:
    print(f"  ✗ No encontrado")

# Subgrupo de orden 137474419109 (el factor grande - 38 bits)
print("\nSubgrupo de orden 137474419109 (puede tardar varios minutos):")
cofactor = order // 137474419109
g_sub = pow(B_p, cofactor, p)
y_sub = pow(k_p, cofactor, p)

print(f"  Calculando BSGS...")
x_sub = bsgs(y_sub, g_sub, p, 137474419109)

if x_sub is not None:
    print(f"  ✓ x ≡ {x_sub} (mod 137474419109)")
    dlogs_partial.append(x_sub)
    mods_partial.append(137474419109)
else:
    print(f"  ✗ No encontrado")

if len(dlogs_partial) == 3:
    print("\n✓✓✓ Discrete log completo calculado! ✓✓✓")
    
    # Combinar con CRT
    x_complete, _ = crt(mods_partial, dlogs_partial)
    print(f"\nDiscrete log para p={p}:")
    print(f"  x = {x_complete}")
    
    # Ahora necesitamos calcular al menos un discrete log más de otro factor
    # para poder usar CRT completo
    
    # Intentemos con el factor 2 (12017858281002457601)
    print(f"\n=== Calculando para segundo factor ===\n")
    
    p2 = small_factors[0]
    print(f"Factor: {p2}")
    
    B_p2 = B % p2
    k_p2 = keystream0 % p2
    
    order2 = p2 - 1
    order2_factors = sympy.factorint(order2)
    print(f"Factores de orden: {order2_factors}")
    # {2: 9, 5: 2, 199637503339: 1, 4703: 1}
    
    dlogs_partial2 = []
    mods_partial2 = []
    
    # Solo haremos el de 4703 que ya sabemos que da 2031
    # y el de 199637503339 (38 bits) con BSGS
    
    print("\nSubgrupo de orden 4703:")
    cofactor = order2 // 4703
    g_sub = pow(B_p2, cofactor, p2)
    y_sub = pow(k_p2, cofactor, p2)
    x_sub = bsgs(y_sub, g_sub, p2, 4703)
    if x_sub is not None:
        print(f"  ✓ x ≡ {x_sub} (mod 4703)")
        dlogs_partial2.append(x_sub)
        mods_partial2.append(4703)
    
    print("\nSubgrupo de orden 199637503339 (puede tardar varios minutos):")
    cofactor = order2 // 199637503339
    g_sub = pow(B_p2, cofactor, p2)
    y_sub = pow(k_p2, cofactor, p2)
    x_sub = bsgs(y_sub, g_sub, p2, 199637503339)
    if x_sub is not None:
        print(f"  ✓ x ≡ {x_sub} (mod 199637503339)")
        dlogs_partial2.append(x_sub)
        mods_partial2.append(199637503339)
    
    if len(dlogs_partial2) == 2:
        x_complete2, _ = crt(mods_partial2, dlogs_partial2)
        print(f"\nDiscrete log parcial para p2={p2}:")
        print(f"  x ≡ {x_complete2} (mod {mods_partial2[0] * mods_partial2[1]})")
        
        # Combinar ambos factores
        print(f"\n=== Combinando ambos factores ===")
        
        combined_result, combined_mod = crt([order, mods_partial2[0] * mods_partial2[1]], 
                                           [x_complete, x_complete2])
        
        print(f"(state & ~0xffff) ≡ {combined_result} (mod {combined_mod})")
        print(f"Módulo combinado: {combined_mod.bit_length()} bits")
        
        # Buscar el estado completo
        print(f"\n=== Buscando estado completo ===")
        
        max_k = 10**10 // combined_mod  # Limitar búsqueda
        
        for k in range(max_k):
            state_high = combined_result + k * combined_mod
            
            # Solo probar si tiene ~700 bits
            if state_high.bit_length() > 705:
                break
            
            if state_high.bit_length() < 650:
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
                        
                        print(f"\n{plaintext.decode('utf-8', errors='ignore')}")
                        exit(0)
            
            if k % 1000000 == 0 and k > 0:
                print(f"  Probado k={k:,}, bits={state_high.bit_length()}")

print("\nScript terminado")
