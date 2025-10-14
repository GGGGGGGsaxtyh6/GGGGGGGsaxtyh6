from Crypto.Util.number import *
import gmpy2
import random as rand

m = 9792986822963146992114161946549377254001156012300083076259452975070903436656675903033418798369811004678022807932064872669773556983318074157606463933686225452143852071767552582367819932516654167400507310054793760473098421162463267
A = 246920531455433048826966670968977027196902794022573095007307132382393013927558904839982249967656424317118051446771969623490992917094197975459553923550187
B = 3120090466259654766880909097573553950487818021670727992039931232537173262599219376624291488340607228938989670215080876932583555412966984946786628621917436142053528648425399877486481618672307477414787846984446437445450282569184963
e = 4180488827

output = [263928838896714332657762314348602240455087661491500131260179929152321790693260683004004767933801216877412896467528419672112455669506824987777448696213888416333755744665868795853306879814179767910033263080874331851322593343273834, 7500716958005582985508201577146205078774368134456220390802616323312171951781595852608949532619393759348663684985174625019004577610546554994801687569942118260000292201829011312249563036393035204990811392856155820408283216493092108, 2577794401090299805723177598637436117371525412262771825236813936115237585602114357696686099541164980249580094089526387369627399445447896464668107355247993148990034255262021717192029828447047736912032562575292618672346226630177737, 9097092753543027532933159793556144814276134227405286080166556624316657274280165256861623248902541076900039285592392074751617153907616670295765377162951858063712964557527212039482031296350052367350738141716598584719951567052177519, 8174235910244322855637254130843352735528509191186418212056519911128301630950848710182451421471531481098828227735010211554839205099309290314993113489826162548089590990963249899714956197889959999884447438378454452096405595048394416, 2823506900640363315693941780283568096117331722098156706833610340919194199647098542170689133810904702849664199290565773405646243449194786656181872671323095023235608799444864036190997987871160063941897196360905342203429250068859314, 4625135637721297092934166648990860031642126233341589454312760229225192256970211899532356300747405146834048765116081788846632527090729839758895834854075755594692611781829177188955301784020596520269704429107749955107365380494152652]

factors = [
    10124460123717732577,
    12017858281002457601,
    15013023439701145679,
    17297082179958074003,
]

# Known plaintext
known_start = b"good luck lmao ictf{"
known_chunks = [bytes_to_long(known_start[i:i+10]) for i in range(0, len(known_start), 10)]
keystreams = [output[i] ^ known_chunks[i] for i in range(len(known_chunks))]

print("=== Enfoque: Pollard Rho para logaritmo discreto ===\n")

def pollard_rho_dlog(g, h, p, order=None):
    """
    Encuentra x tal que g^x = h (mod p) usando Pollard rho
    """
    if order is None:
        order = p - 1
    
    # Función de partición en 3 conjuntos
    def f(x_val, a_val, b_val):
        partition = x_val % 3
        if partition == 0:
            # Multiplicar por h
            x_new = (x_val * h) % p
            a_new = a_val
            b_new = (b_val + 1) % order
        elif partition == 1:
            # Elevar al cuadrado
            x_new = (x_val * x_val) % p
            a_new = (2 * a_val) % order
            b_new = (2 * b_val) % order
        else:
            # Multiplicar por g
            x_new = (x_val * g) % p
            a_new = (a_val + 1) % order
            b_new = b_val
        return x_new, a_new, b_new
    
    # Inicializar
    x, a, b = 1, 0, 0
    X, A, B = 1, 0, 0
    
    for i in range(order):
        # Tortoise
        x, a, b = f(x, a, b)
        
        # Hare (dos pasos)
        X, A, B = f(X, A, B)
        X, A, B = f(X, A, B)
        
        if x == X:
            # Colisión encontrada
            # g^a * h^b = g^A * h^B (mod p)
            # g^a * (g^x)^b = g^A * (g^x)^B (mod p)
            # g^(a + xb) = g^(A + xB) (mod p)
            # a + xb = A + xB (mod order)
            # x(B - b) = a - A (mod order)
            
            r = (B - b) % order
            s = (a - A) % order
            
            d = gmpy2.gcd(r, order)
            if d == 1:
                # Única solución
                result = (s * gmpy2.invert(r, order)) % order
                return result
            else:
                # Múltiples soluciones posibles
                r_prime = r // d
                s_prime = s // d
                order_prime = order // d
                
                if s % d != 0:
                    return None  # No hay solución
                
                x0 = (s_prime * gmpy2.invert(r_prime, order_prime)) % order_prime
                
                # Probar las d posibles soluciones
                for k in range(d):
                    candidate = x0 + k * order_prime
                    if pow(g, candidate, p) == h:
                        return candidate
                
                return None
        
        if i % 100000 == 0 and i > 0:
            print(f"  Iteración {i}...")
    
    return None

keystream_0 = keystreams[0]

print("Probando Pollard Rho en factores pequeños...\n")

for i, p in enumerate(factors[:2]):  # Solo los dos más pequeños
    print(f"Factor {i+1}: p = {p} ({p.bit_length()} bits)")
    
    B_mod_p = B % p
    ks_mod_p = keystream_0 % p
    
    print(f"  Resolviendo B^x ≡ {ks_mod_p} (mod {p})")
    print(f"  Usando Pollard Rho...")
    
    try:
        x = pollard_rho_dlog(B_mod_p, ks_mod_p, p, order=p-1)
        
        if x is not None:
            # Verificar
            if pow(B_mod_p, x, p) == ks_mod_p:
                print(f"  ¡Solución encontrada y verificada!: x = {x}")
            else:
                print(f"  Solución encontrada pero no verifica: x = {x}")
        else:
            print(f"  No se encontró solución")
    except Exception as ex:
        print(f"  Error: {ex}")
    
    print()

print("\n¿Qué tal si el backdoor es diferente?")
print("Tal vez el exponente (state & ~0xffff) es pequeño...")
print("O tal vez hay una relación específica que no he visto...")
