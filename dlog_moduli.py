from Crypto.Util.number import *
import gmpy2

# Factorización
primes = [
    10124460123717732577,
    12017858281002457601,
    15013023439701145679,
    17297082179958074003,
]
# Omitiendo el quinto primo por ser demasiado grande

m = 1
for p in primes:
    m *= p

m_full = 9792986822963146992114161946549377254001156012300083076259452975070903436656675903033418798369811004678022807932064872669773556983318074157606463933686225452143852071767552582367819932516654167400507310054793760473098421162463267

B = 3120090466259654766880909097573553950487818021670727992039931232537173262599219376624291488340607228938989670215080876932583555412966984946786628621917436142053528648425399877486481618672307477414787846984446437445450282569184963

output = [263928838896714332657762314348602240455087661491500131260179929152321790693260683004004767933801216877412896467528419672112455669506824987777448696213888416333755744665868795853306879814179767910033263080874331851322593343273834, 7500716958005582985508201577146205078774368134456220390802616323312171951781595852608949532619393759348663684985174625019004577610546554994801687569942118260000292201829011312249563036393035204990811392856155820408283216493092108]

known_prefix = b"good luck lmao ictf{"
chunks = [bytes_to_long(known_prefix[i:i+10]) for i in range(0, len(known_prefix), 10)]

target0 = output[0] ^ chunks[0]
target1 = output[1] ^ chunks[1]

print(f"Calculando logaritmo discreto módulo cada primo...")
print(f"target0 = {hex(target0)[:50]}...")

# Baby-step giant-step pero solo para exponentes múltiplos de 2^16
def bsgs_multiple(g, h, p, multiple):
    """Encuentra x tal que g^x = h mod p, donde x es múltiplo de 'multiple'"""
    # Reformular: (g^multiple)^k = h mod p
    g_base = pow(g, multiple, p)
    
    # Ahora buscar k tal que g_base^k = h mod p
    # Pero h debe ser una potencia de g_base
    
    # Verificar que h está en el subgrupo
    order = p - 1
    subgroup_order = order // gmpy2.gcd(order, multiple)
    
    # BSGS estándar
    m_step = min(int(gmpy2.isqrt(subgroup_order)) + 1, 1000000)
    
    table = {}
    val = 1
    for j in range(m_step):
        if val == h:
            return j * multiple
        table[val] = j
        val = (val * g_base) % p
    
    factor = pow(g_base, -m_step, p)
    gamma = h
    for i in range(m_step):
        if gamma in table:
            return (i * m_step + table[gamma]) * multiple
        gamma = (gamma * factor) % p
    
    return None

# Intentar con cada primo
for i, p in enumerate(primes[:2]):  # Solo los dos primeros primos más pequeños
    print(f"\n=== Primo {i+1}: {p} ===")
    g = B % p
    h = target0 % p
    
    print(f"Calculando log_{g}({h}) mod {p}")
    print(f"Tamaño del primo: {p.bit_length()} bits")
    
    # Probar BSGS normal primero para el primo más pequeño
    if i == 0:
        print("Probando BSGS estándar...")
        m_step = min(int(gmpy2.isqrt(p-1)) + 1, 10000000)
        print(f"Pasos BSGS: {m_step}")
        
        table = {}
        val = 1
        found = False
        
        for j in range(min(m_step, 50000000)):
            if val == h:
                print(f"¡Encontrado en baby step! log = {j}")
                found = True
                break
            if j < 1000000:  # Limitar la tabla
                table[val] = j
            val = (val * g) % p
            
            if j % 1000000 == 0 and j > 0:
                print(f"  Baby steps: {j} / {m_step}")
        
        if not found and len(table) > 0:
            print(f"Baby steps completados: {len(table)} entradas")
            print("Iniciando giant steps...")
            factor = pow(g, -len(table), p)
            gamma = h
            for i in range(min(m_step, 1000000)):
                if gamma in table:
                    log_val = i * len(table) + table[gamma]
                    print(f"¡Encontrado en giant step! log = {log_val}")
                    found = True
                    break
                gamma = (gamma * factor) % p
                
                if i % 100000 == 0 and i > 0:
                    print(f"  Giant steps: {i} / {m_step}")
        
        if not found:
            print("No se encontró en el tiempo permitido")
