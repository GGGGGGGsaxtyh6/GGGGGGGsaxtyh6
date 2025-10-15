from Crypto.Util.number import long_to_bytes, GCD
import random

# Valores del desafío
m = 9792986822963146992114161946549377254001156012300083076259452975070903436656675903033418798369811004678022807932064872669773556983318074157606463933686225452143852071767552582367819932516654167400507310054793760473098421162463267
A = 246920531455433048826966670968977027196902794022573095007307132382393013927558904839982249967656424317118051446771969623490992917094197975459553923550187 
B = 3120090466259654766880909097573553950487818021670727992039931232537173262599219376624291488340607228938989670215080876932583555412966984946786628621917436142053528648425399877486481618672307477414787846984446437445450282569184963
e = 4180488827

output = [263928838896714332657762314348602240455087661491500131260179929152321790693260683004004767933801216877412896467528419672112455669506824987777448696213888416333755744665868795853306879814179767910033263080874331851322593343273834, 7500716958005582985508201577146205078774368134456220390802616323312171951781595852608949532619393759348663684985174625019004577610546554994801687569942118260000292201829011312249563036393035204990811392856155820408283216493092108, 2577794401090299805723177598637436117371525412262771825236813936115237585602114357696686099541164980249580094089526387369627399445447896464668107355247993148990034255262021717192029828447047736912032562575292618672346226630177737, 9097092753543027532933159793556144814276134227405286080166556624316657274280165256861623248902541076900039285592392074751617153907616670295765377162951858063712964557527212039482031296350052367350738141716598584719951567052177519, 8174235910244322855637254130843352735528509191186418212056519911128301630950848710182451421471531481098828227735010211554839205099309290314993113489826162548089590990963249899714956197889959999884447438378454452096405595048394416, 2823506900640363315693941780283568096117331722098156706833610340919194199647098542170689133810904702849664199290565773405646243449194786656181872671323095023235608799444864036190997987871160063941897196360905342203429250068859314, 4625135637721297092934166648990860031642126233341589454312760229225192256970211899532356300747405146834048765116081788846632527090729839758895834854075755594692611781829177188955301784020596520269704429107749955107365380494152652]

# Factores de m  
small_factors = [
    10124460123717732577,
    12017858281002457601,
    15013023439701145679,
    17297082179958074003
]

def pollard_rho_dlog(y, g, p, order=None):
    """
    Pollard's rho para discrete log
    Resuelve g^x = y (mod p)
    """
    if order is None:
        order = p - 1
    
    # Función para dividir el espacio en 3 partes
    def f(x_val, a_val, b_val):
        partition = x_val % 3
        if partition == 0:
            # Multiplicar por y
            return (x_val * y) % p, a_val, (b_val + 1) % order
        elif partition == 1:
            # Duplicar
            return (x_val * x_val) % p, (2 * a_val) % order, (2 * b_val) % order
        else:
            # Multiplicar por g
            return (x_val * g) % p, (a_val + 1) % order, b_val
    
    # Tortuga y liebre
    x_t, a_t, b_t = 1, 0, 0
    x_h, a_h, b_h = 1, 0, 0
    
    for i in range(order):
        # Tortuga da un paso
        x_t, a_t, b_t = f(x_t, a_t, b_t)
        
        # Liebre da dos pasos
        x_h, a_h, b_h = f(x_h, a_h, b_h)
        x_h, a_h, b_h = f(x_h, a_h, b_h)
        
        if x_t == x_h:
            # Colisión encontrada
            # g^a_t * y^b_t = g^a_h * y^b_h
            # g^(a_t - a_h) = y^(b_h - b_t)
            # Si y = g^x, entonces: g^(a_t - a_h) = g^(x*(b_h - b_t))
            # Por tanto: x*(b_h - b_t) = a_t - a_h (mod order)
            
            da = (a_t - a_h) % order
            db = (b_h - b_t) % order
            
            if db == 0:
                continue
            
            # Resolver x * db = da (mod order)
            g_db = GCD(db, order)
            
            if da % g_db != 0:
                continue
            
            # x * (db/g) = da/g (mod order/g)
            db_reduced = db // g_db
            da_reduced = da // g_db
            order_reduced = order // g_db
            
            # Calcular inverso
            try:
                db_inv = pow(db_reduced, -1, order_reduced)
                x = (da_reduced * db_inv) % order_reduced
                
                # Verificar
                if pow(g, x, p) == y:
                    return x
                
                # Probar múltiples soluciones
                for k in range(g_db):
                    x_candidate = x + k * order_reduced
                    if pow(g, x_candidate, p) == y:
                        return x_candidate
            except:
                continue
        
        if i % 100000 == 0 and i > 0:
            print(f"  Pollard rho: {i} iteraciones...")
    
    return None

print("Calculando discrete logs con Pollard's rho...")

# Intentar con el primer factor (el más pequeño)
p = small_factors[0]
print(f"\nUsando factor p = {p}")

B_p = B % p
y_p = output[0] % p

print(f"Calculando log de {y_p} base {B_p} módulo {p}")
print(f"Orden del grupo: {p-1}")

# Como el factor es relativamente pequeño (~64 bits), podría ser factible
# Primero veamos si podemos factorizar p-1

import sympy
print(f"\nFactorizando p-1...")
p_minus_1_factors = sympy.factorint(p-1)
print(f"Factores de p-1: {p_minus_1_factors}")

# Si p-1 tiene factores pequeños, Pohlig-Hellman será eficiente
print(f"\nUsando Pohlig-Hellman...")

# Intentar con sympy primero (solo para el factor más pequeño)
try:
    x = sympy.ntheory.discrete_log(p, y_p, B_p, order=p-1)
    print(f"✓ Discrete log encontrado: {x}")
    print(f"Verificando: B^x mod p = {pow(B_p, x, p)}, esperado = {y_p}")
except Exception as ex:
    print(f"Error con sympy: {ex}")
    print("\nIntentando Pollard's rho...")
    x = pollard_rho_dlog(y_p, B_p, p, p-1)
    if x:
        print(f"✓ Discrete log encontrado: {x}")
