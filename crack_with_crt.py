from Crypto.Util.number import *
import gmpy2
from functools import reduce

# Factorización de m
primes = [
    10124460123717732577,
    12017858281002457601,
    15013023439701145679,
    17297082179958074003,
]

B = 3120090466259654766880909097573553950487818021670727992039931232537173262599219376624291488340607228938989670215080876932583555412966984946786628621917436142053528648425399877486481618672307477414787846984446437445450282569184963
output = 263928838896714332657762314348602240455087661491500131260179929152321790693260683004004767933801216877412896467528419672112455669506824987777448696213888416333755744665868795853306879814179767910033263080874331851322593343273834
known_prefix = b'good luck '
chunk = bytes_to_long(known_prefix)
target = output ^ chunk

print("Intentando resolver el logaritmo discreto usando la factorización")
print("Trabajando módulo cada primo y luego usando CRT")
print()

# Para cada primo, necesito resolver: B^x ≡ target (mod p)
# donde x es de la forma k * 2^16 (un múltiplo de 2^16)

def baby_step_giant_step_small(g, h, p, limit=10000000):
    """BSGS para primos, con límite de iteraciones"""
    print(f"  BSGS en primo de {p.bit_length()} bits, límite={limit}")
    
    # Tamaño del paso
    m = min(int(gmpy2.isqrt(p-1)) + 1, limit)
    
    # Baby steps
    table = {}
    val = 1
    for j in range(m):
        if val == h:
            return j
        table[val] = j
        val = (val * g) % p
        if j % 1000000 == 0 and j > 0:
            print(f"    Baby step {j}/{m}")
    
    # Giant steps
    factor = pow(g, -m, p)
    gamma = h
    for i in range(m):
        if gamma in table:
            return i * m + table[gamma]
        gamma = (gamma * factor) % p
        if i % 100000 == 0 and i > 0:
            print(f"    Giant step {i}/{m}")
    
    return None

# Intentar con los primos más pequeños
logs_mod_primes = []

for i, p in enumerate(primes):
    print(f"\n=== Primo {i+1}: {p} ({p.bit_length()} bits) ===")
    
    g_p = B % p
    h_p = target % p
    
    print(f"Resolviendo: {g_p} ^ x ≡ {h_p} (mod {p})")
    
    # Verificar que h_p esté en el grupo generado por g_p
    # Si p es primo, el grupo multiplicativo tiene orden p-1
    
    # Para primos de 64 bits, BSGS podría funcionar si limito las iteraciones
    if i < 2:  # Solo los dos primeros (más pequeños)
        log_p = baby_step_giant_step_small(g_p, h_p, p, limit=5000000)
        if log_p is not None:
            print(f"  ¡Logaritmo encontrado! x ≡ {log_p} (mod {p-1})")
            logs_mod_primes.append((log_p, p-1))  # (valor, módulo)
        else:
            print(f"  No encontrado en el límite de iteraciones")
    else:
        print(f"  Saltando (primo demasiado grande para BSGS simple)")

if len(logs_mod_primes) >= 2:
    print(f"\n¡Tengo {len(logs_mod_primes)} logaritmos! Usando CRT...")
    
    # Usar CRT para combinar
    def chinese_remainder(remainders, moduli):
        """Teorema chino del resto"""
        total = 0
        prod = reduce(lambda a, b: a*b, moduli)
        for r, m in zip(remainders, moduli):
            p = prod // m
            total += r * pow(p, -1, m) * p
        return total % prod
    
    remainders = [log for log, mod in logs_mod_primes]
    moduli = [mod for log, mod in logs_mod_primes]
    
    combined = chinese_remainder(remainders, moduli)
    combined_mod = reduce(lambda a, b: a*b, moduli)
    
    print(f"x ≡ {combined} (mod {combined_mod})")
    print(f"Bits del módulo combinado: {combined_mod.bit_length()}")
    
    # Esto me da x módulo el producto de los (p_i - 1)
    # El verdadero x podría ser combined + k * combined_mod para algún k
    
    # Verificar si este valor funciona
    m_full = 9792986822963146992114161946549377254001156012300083076259452975070903436656675903033418798369811004678022807932064872669773556983318074157606463933686225452143852071767552582367819932516654167400507310054793760473098421162463267
    test = pow(B, combined, m_full)
    if test == target:
        print(f"\n¡VERIFICADO! x = {combined}")
    else:
        print(f"\nNo verifica directamente, probando x = combined + k * combined_mod...")
        for k in range(100):
            test_x = combined + k * combined_mod
            test = pow(B, test_x, m_full)
            if test == target:
                print(f"¡ENCONTRADO! x = {test_x} (k={k})")
                break
else:
    print("\nNo se encontraron suficientes logaritmos")
