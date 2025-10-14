from Crypto.Util.number import *
import gmpy2

m = 9792986822963146992114161946549377254001156012300083076259452975070903436656675903033418798369811004678022807932064872669773556983318074157606463933686225452143852071767552582367819932516654167400507310054793760473098421162463267
A = 246920531455433048826966670968977027196902794022573095007307132382393013927558904839982249967656424317118051446771969623490992917094197975459553923550187
B = 3120090466259654766880909097573553950487818021670727992039931232537173262599219376624291488340607228938989670215080876932583555412966984946786628621917436142053528648425399877486481618672307477414787846984446437445450282569184963
e = 4180488827

# Keystream del primer bloque (conocemos el plaintext "good luck ")
keystream0 = 263928838896714332657762314348602240455087661491500131260179929152321790693260683004004767933801216877412896467528419672112455669506824987777448696213888416333755744665868795853306879814179767910033263081341240785125410643513418

# El keystream es B^(state0 & ~0xffff) mod m
# Necesitamos encontrar x = (state0 & ~0xffff) tal que B^x = keystream0 mod m

# Intentemos baby-step giant-step con un límite razonable
print("Intentando baby-step giant-step para logaritmo discreto...")
print("Esto podría ser el backdoor si el espacio es limitado...")

# Primero, verificar si hay potencias pequeñas
print("\nBuscando potencias pequeñas de B que den el keystream...")
for exp in range(0, 100000, 1):
    if pow(B, exp, m) == keystream0:
        print(f"¡Encontrado! B^{exp} = keystream0 mod m")
        print(f"state0 & ~0xffff = {exp}")
        break
    if exp % 10000 == 0 and exp > 0:
        print(f"  Probado hasta {exp}...")

# También probar con potencias grandes pero específicas
# El estado tiene 700 bits, y eliminamos 16, así que el exponente está en rango [0, 2^684]
# Pero si state0 es conocido o pequeño por el backdoor...

print("\nProbando si el estado inicial podría ser pequeño...")
# Si el estado es realmente aleatorio de 700 bits pero el backdoor hace que sea predecible...

# Otra idea: tal vez podemos trabajar hacia atrás desde el output conocido
# Si conocemos parte del plaintext final ("}"), podemos obtener más keystreams
