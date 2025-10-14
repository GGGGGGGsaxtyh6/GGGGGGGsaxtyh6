from Crypto.Util.number import *
import gmpy2

# Idea: MEET IN THE MIDDLE
# Si state = high_bits || low_bits
# donde low_bits son los últimos X bits y high_bits son los primeros (700-X) bits
# 
# Entonces: B^(state & ~0xffff) = B^((high_bits || low_bits) & ~0xffff)
#                                 = B^(high_bits << 16)   (asumiendo low_bits < 2^16)
#
# Si divido state en dos partes:
# state = upper * 2^k + lower
# donde lower < 2^k
#
# Entonces si k > 16:
# state & ~0xffff = (upper * 2^k) + (lower & ~0xffff)
#                 = upper * 2^k + ((lower >> 16) << 16)
#
# B^(state & ~0xffff) = B^(upper * 2^k) * B^((lower >> 16) << 16) mod m

m = 9792986822963146992114161946549377254001156012300083076259452975070903436656675903033418798369811004678022807932064872669773556983318074157606463933686225452143852071767552582367819932516654167400507310054793760473098421162463267
B = 3120090466259654766880909097573553950487818021670727992039931232537173262599219376624291488340607228938989670215080876932583555412966984946786628621917436142053528648425399877486481618672307477414787846984446437445450282569184963

output = 263928838896714332657762314348602240455087661491500131260179929152321790693260683004004767933801216877412896467528419672112455669506824987777448696213888416333755744665868795853306879814179767910033263080874331851322593343273834
known_prefix = b'good luck '
chunk = bytes_to_long(known_prefix)
target = output ^ chunk

print("MEET IN THE MIDDLE Attack")
print(f"Target: {hex(target)[:60]}...")
print()

# Dividir state en dos partes de N bits cada una
# state = upper || middle || lower_16
# donde lower_16 son los 16 bits que se eliminan

# Probar con upper de pocos bits y middle de pocos bits
bits_upper = 18  # bits superiores
bits_middle = 18  # bits medios

print(f"Dividiendo state en: upper({bits_upper} bits) || middle({bits_middle} bits) || lower(16 bits)")
print(f"Total: {bits_upper + bits_middle + 16} bits")
print()

# Pre-computar B^(2^16) mod m
base_16 = pow(B, 2**16, m)
print("Pre-computando tabla de middle values...")

# Baby step: middle values
table = {}
for middle in range(2**bits_middle):
    # middle representa los bits en posiciones 16...(16+bits_middle-1)
    exponent_middle = middle << 16
    val = pow(B, exponent_middle, m)
    table[val] = middle
    
    if middle % 100000 == 0 and middle > 0:
        print(f"  Tabla: {middle} / {2**bits_middle}")

print(f"Tabla creada con {len(table)} entradas")
print()

# Giant step: upper values
print("Buscando en upper values...")
base_upper = pow(B, 2**(16 + bits_middle), m)  # B^(2^(16+bits_middle))

for upper in range(2**bits_upper):
    # upper representa los bits en posiciones (16+bits_middle)...
    exponent_upper = upper * (2**(16 + bits_middle))
    val_upper = pow(B, exponent_upper, m)
    
    # Necesitamos: B^exponent_upper * B^exponent_middle = target
    # Entonces: B^exponent_middle = target / B^exponent_upper
    # = target * B^(-exponent_upper)
    
    needed = (target * pow(val_upper, -1, m)) % m
    
    if needed in table:
        middle = table[needed]
        state_high_bits = (upper << (16 + bits_middle)) | (middle << 16)
        print(f"\n¡POSIBLE MATCH!")
        print(f"upper = {upper}, middle = {middle}")
        print(f"state (sin últimos 16 bits) = {state_high_bits}")
        
        # Verificar
        test = pow(B, state_high_bits, m)
        if test == target:
            print(f"¡VERIFICADO! state (sin low 16 bits) = {state_high_bits}")
            print(f"state completo = {state_high_bits} + [0..65535]")
            break
        else:
            print(f"No verificó, falsa alarma")
    
    if upper % 10000 == 0 and upper > 0:
        print(f"  Upper: {upper} / {2**bits_upper}")

else:
    print(f"\nNo encontrado con {bits_upper}+{bits_middle} bits")
    print("El estado debe tener más bits significativos")
