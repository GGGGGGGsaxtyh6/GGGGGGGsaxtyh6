from sympy.ntheory import discrete_log
from Crypto.Util.number import bytes_to_long

# Parámetros
m = 9792986822963146992114161946549377254001156012300083076259452975070903436656675903033418798369811004678022807932064872669773556983318074157606463933686225452143852071767552582367819932516654167400507310054793760473098421162463267
B = 3120090466259654766880909097573553950487818021670727992039931232537173262599219376624291488340607228938989670215080876932583555412966984946786628621917436142053528648425399877486481618672307477414787846984446437445450282569184963

output = 263928838896714332657762314348602240455087661491500131260179929152321790693260683004004767933801216877412896467528419672112455669506824987777448696213888416333755744665868795853306879814179767910033263080874331851322593343273834

known_prefix = b"good luck "
chunk = bytes_to_long(known_prefix)
target = output ^ chunk

print("Intentando logaritmo discreto con sympy...")
print(f"Buscando x tal que B^x ≡ target (mod m)")
print(f"B = {hex(B)[:50]}...")
print(f"target = {hex(target)[:50]}...")
print(f"m = {hex(m)[:50]}...")
print()

# Intentar con los primos más pequeños primero
primes = [
    10124460123717732577,
    12017858281002457601,
]

print("Probando módulo primos pequeños...")
for i, p in enumerate(primes):
    print(f"\nPrimo {i+1}: {p}")
    g = B % p
    h = target % p
    
    print(f"  Intentando discrete_log({h}, {g}, {p})...")
    print(f"  Esto puede tardar...")
    
    try:
        result = discrete_log(p, h, g)  # sympy usa orden (n, a, b) para b^x ≡ a (mod n)
        print(f"  ¡Encontrado! x = {result}")
    except Exception as e:
        print(f"  Error: {e}")
    
    break  # Solo intentar con el primero por ahora

print("\nSi sympy tarda demasiado, el logaritmo discreto es demasiado grande incluso para sympy")
