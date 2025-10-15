from Crypto.Util.number import long_to_bytes, bytes_to_long, inverse
import sympy

# Valores del desafío
m = 9792986822963146992114161946549377254001156012300083076259452975070903436656675903033418798369811004678022807932064872669773556983318074157606463933686225452143852071767552582367819932516654167400507310054793760473098421162463267
A = 246920531455433048826966670968977027196902794022573095007307132382393013927558904839982249967656424317118051446771969623490992917094197975459553923550187 
B = 3120090466259654766880909097573553950487818021670727992039931232537173262599219376624291488340607228938989670215080876932583555412966984946786628621917436142053528648425399877486481618672307477414787846984446437445450282569184963
e = 4180488827

output = [263928838896714332657762314348602240455087661491500131260179929152321790693260683004004767933801216877412896467528419672112455669506824987777448696213888416333755744665868795853306879814179767910033263080874331851322593343273834, 7500716958005582985508201577146205078774368134456220390802616323312171951781595852608949532619393759348663684985174625019004577610546554994801687569942118260000292201829011312249563036393035204990811392856155820408283216493092108, 2577794401090299805723177598637436117371525412262771825236813936115237585602114357696686099541164980249580094089526387369627399445447896464668107355247993148990034255262021717192029828447047736912032562575292618672346226630177737, 9097092753543027532933159793556144814276134227405286080166556624316657274280165256861623248902541076900039285592392074751617153907616670295765377162951858063712964557527212039482031296350052367350738141716598584719951567052177519, 8174235910244322855637254130843352735528509191186418212056519911128301630950848710182451421471531481098828227735010211554839205099309290314993113489826162548089590990963249899714956197889959999884447438378454452096405595048394416, 2823506900640363315693941780283568096117331722098156706833610340919194199647098542170689133810904702849664199290565773405646243449194786656181872671323095023235608799444864036190997987871160063941897196360905342203429250068859314, 4625135637721297092934166648990860031642126233341589454312760229225192256970211899532356300747405146834048765116081788846632527090729839758895834854075755594692611781829177188955301784020596520269704429107749955107365380494152652]

# Factores de m obtenidos de factordb
factors = [
    10124460123717732577,
    12017858281002457601,
    15013023439701145679,
    17297082179958074003,
    309938271107370186286857659422407283771865851657937731111744300310040346308690205006641245318085354895438500308814135783504803596134094206083383195557983
]

print("Verificando factorización...")
product = 1
for f in factors:
    product *= f
assert product == m, "Factorización incorrecta"
print("✓ Factorización correcta")

# Calcular phi(m)
phi_m = 1
for f in factors:
    phi_m *= (f - 1)
print(f"phi(m) calculado")

# Calcular inverso de e mod phi(m)
e_inv = inverse(e, phi_m)
print(f"e_inv calculado")

# Ahora necesitamos calcular logaritmos discretos
# output[i] = B^(state_i - (state_i & 0xffff)) mod m
# Usaremos Pohlig-Hellman para calcular el discrete log

def pohlig_hellman_prime(y, g, p):
    """Calcula discrete log de y base g módulo primo p usando baby-step giant-step"""
    # Para un primo p, esto es más simple
    # Usaremos el algoritmo de sympy
    try:
        x = sympy.ntheory.discrete_log(p, y, g)
        return x
    except:
        return None

def pohlig_hellman(y, g, n, factors):
    """
    Calcula discrete log de y base g módulo n usando Pohlig-Hellman
    n debe estar factorizado en factors (lista de primos)
    """
    # Calculamos el orden del grupo
    order = 1
    for f in factors:
        order *= (f - 1)
    
    # Usar el teorema chino del resto
    # Para cada factor primo, calculamos el discrete log módulo ese factor
    
    remainders = []
    moduli = []
    
    for p in factors:
        # Trabajar en el subgrupo de orden (p-1)
        h = pow(g, order // (p-1), n)
        y_reduced = pow(y, order // (p-1), n)
        
        # Calcular discrete log en este subgrupo
        # Usaremos baby-step giant-step
        x_p = baby_step_giant_step(y_reduced, h, p)
        
        if x_p is not None:
            remainders.append(x_p)
            moduli.append(p - 1)
        else:
            print(f"No se pudo calcular discrete log para factor {p}")
            return None
    
    # Usar CRT para combinar
    from sympy.ntheory.modular import crt
    x = crt(moduli, remainders)[0]
    return x

def baby_step_giant_step(y, g, p, order=None):
    """
    Baby-step giant-step para calcular discrete log
    Resuelve g^x = y (mod p)
    """
    if order is None:
        order = p - 1
    
    m = int(order**0.5) + 1
    
    # Baby step: construir tabla g^j para j = 0, 1, ..., m-1
    table = {}
    g_power = 1
    for j in range(m):
        if g_power not in table:
            table[g_power] = j
        g_power = (g_power * g) % p
    
    # Giant step
    # Calcular g^(-m) mod p
    factor = pow(g, -m, p)
    gamma = y
    
    for i in range(m):
        if gamma in table:
            return i * m + table[gamma]
        gamma = (gamma * factor) % p
    
    return None

print("\nCalculando logaritmos discretos usando Pohlig-Hellman...")
print("Esto puede tomar algo de tiempo...")

# Para cada output, calculamos el discrete log
# Pero hay un problema: el discrete log nos da (state - (state & 0xffff))
# que es state con los últimos 16 bits en cero

# Primero intentemos con el primer output para ver si funciona
print("\nProbando con el primer chunk...")

# El problema es que necesitamos el discrete log módulo m, no módulo cada factor
# Voy a usar un enfoque diferente: el teorema chino del resto

# Para cada factor primo p_i de m, calcularemos:
# output[0] ≡ B^x (mod p_i)
# donde x = state - (state & 0xffff)

print("\nUsando enfoque de CRT...")

# Calcular discrete log módulo cada factor primo
logs_mod_factors = []

for i, p in enumerate(factors):
    print(f"Procesando factor {i+1}/{len(factors)}: {p.bit_length()} bits")
    
    # Reducir módulo p
    B_p = B % p
    output_0_p = output[0] % p
    
    # Calcular discrete log en F_p
    # El orden del grupo multiplicativo es p-1
    
    # Usar baby-step giant-step
    # Pero primero necesitamos verificar que B es generador o al menos tiene orden alto
    
    # Para simplificar, usaremos sympy
    try:
        x_p = sympy.ntheory.discrete_log(p, output_0_p, B_p, order=p-1)
        print(f"  Discrete log módulo p: {x_p}")
        logs_mod_factors.append((x_p, p-1))
    except Exception as ex:
        print(f"  Error: {ex}")
        # Intentar con baby-step giant-step manual
        print(f"  Intentando baby-step giant-step...")
        x_p = baby_step_giant_step(output_0_p, B_p, p, p-1)
        if x_p is not None:
            print(f"  Discrete log módulo p: {x_p}")
            logs_mod_factors.append((x_p, p-1))
        else:
            print(f"  Falló")

print(f"\nCalculados {len(logs_mod_factors)} logaritmos de {len(factors)} factores")

if len(logs_mod_factors) == len(factors):
    # Usar CRT para combinar
    from sympy.ntheory.modular import crt
    
    remainders = [x for x, _ in logs_mod_factors]
    moduli = [m for _, m in logs_mod_factors]
    
    # Calcular phi(m) como producto de (p_i - 1)
    order_B = 1
    for m_i in moduli:
        order_B *= m_i
    
    print(f"\nUsando CRT para combinar...")
    state_high_bits = crt(moduli, remainders)[0]
    
    print(f"Bits altos del estado (sin los últimos 16 bits): {state_high_bits}")
    
    # Ahora necesitamos probar fuerza bruta sobre los 16 bits bajos
    print("\nProbando fuerza bruta sobre los últimos 16 bits...")
    
    for low_bits in range(65536):
        if low_bits % 10000 == 0:
            print(f"  Probando {low_bits}/65536...")
        
        state_candidate = state_high_bits + low_bits
        
        # Verificar si este estado produce el output correcto
        output_test = pow(B, state_candidate - (state_candidate & 0xffff), m)
        
        if output_test == output[0]:
            print(f"\n✓ Encontrado estado inicial: {state_candidate}")
            
            # Ahora podemos descifrar todos los chunks
            state = state_candidate
            plaintext_chunks = []
            
            for i, out in enumerate(output):
                # El chunk cifrado es: out XOR pow(B, state - (state & 0xffff), m)
                keystream = pow(B, state - (state & 0xffff), m)
                chunk = out ^ keystream
                plaintext_chunks.append(chunk)
                
                # Actualizar estado para el próximo chunk
                new_state = pow(pow(A, state, m) ^ B, e, m)
                state = new_state
            
            # Convertir chunks a bytes
            plaintext = b""
            for chunk in plaintext_chunks:
                chunk_bytes = long_to_bytes(chunk)
                plaintext += chunk_bytes
            
            print(f"\nPlaintext descifrado: {plaintext}")
            break
    else:
        print("\nNo se encontró el estado correcto :(")
else:
    print("\nNo se pudieron calcular todos los discrete logs")
