from Crypto.Util.number import *
import gmpy2
from sympy.ntheory.residue_ntheory import discrete_log
from sympy.ntheory.modular import crt

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
    309938271107370186286857659422407283771865851657937731111744300310040346308690205006641245318085354895438500308814135783504803596134094206083383195557983
]

# Known plaintext
known_start = b"good luck lmao ictf{"
known_chunks = [bytes_to_long(known_start[i:i+10]) for i in range(0, len(known_start), 10)]
keystreams = [output[i] ^ known_chunks[i] for i in range(len(known_chunks))]

print("=== Usando CRT con los factores de m ===")
print(f"Resolviendo B^x = keystream[0] mod m usando CRT")
print()

keystream_0 = keystreams[0]

# Resolver B^x = keystream_0 mod pi para cada factor pi
solutions = []
moduli = []

for i, p in enumerate(factors):
    print(f"Factor {i+1}/{len(factors)}: p = {p} ({p.bit_length()} bits)")
    
    # Reducir los valores mod p
    B_mod_p = B % p
    ks_mod_p = keystream_0 % p
    
    print(f"  Resolviendo B^x ≡ {ks_mod_p} (mod {p})")
    print(f"  Usando discrete_log de sympy...")
    
    try:
        # discrete_log encuentra x tal que B^x = keystream mod p
        x = discrete_log(p, ks_mod_p, B_mod_p)
        print(f"  ¡Solución encontrada!: x ≡ {x} (mod ord(B))")
        solutions.append(x)
        
        # El módulo es el orden de B mod p, que divide a p-1
        # Para simplificar, usamos p-1 (puede haber soluciones modulares más pequeñas)
        moduli.append(p - 1)
        
    except Exception as ex:
        print(f"  Error: {ex}")
        print(f"  Intentando con fuerza bruta...")
        
        # Fuerza bruta para factores pequeños
        if p.bit_length() <= 64:
            found = False
            for x in range(min(p-1, 10**7)):
                if pow(B_mod_p, x, p) == ks_mod_p:
                    print(f"  ¡Solución encontrada por fuerza bruta!: x = {x}")
                    solutions.append(x)
                    moduli.append(p - 1)
                    found = True
                    break
                if x % 1000000 == 0 and x > 0:
                    print(f"    Probando x = {x}...")
            
            if not found:
                print(f"  No se encontró solución en el rango probado")
                break
        else:
            print(f"  Factor demasiado grande para fuerza bruta")
            break
    
    print()

if len(solutions) == len(factors):
    print("¡Todas las soluciones encontradas!")
    print(f"solutions = {solutions}")
    print(f"moduli = {moduli}")
    print()
    print("Aplicando CRT...")
    
    # Usar CRT para combinar las soluciones
    x_combined, mod_combined = crt(moduli, solutions)
    print(f"Solución combinada: x ≡ {x_combined} (mod {mod_combined})")
    print()
    
    # Verificar
    print("Verificando...")
    result = pow(B, x_combined, m)
    if result == keystream_0:
        print("¡Verificación exitosa!")
        print(f"x (estado & ~0xffff) = {x_combined}")
        
        # Ahora necesitamos encontrar los últimos 16 bits
        # Probamos todos los valores posibles de los últimos 16 bits
        print("\nBuscando los últimos 16 bits del estado...")
        for low_bits in range(65536):
            state_candidate = x_combined | low_bits
            
            # Verificar con el primer keystream (siempre debería coincidir por construcción)
            ks0 = pow(B, state_candidate & ~0xffff, m)
            if ks0 != keystream_0:
                continue  # No debería pasar
            
            # Calcular el siguiente estado
            new_state = pow(pow(A, state_candidate, m) ^ B, e, m)
            
            # Calcular el segundo keystream
            ks1 = pow(B, new_state & ~0xffff, m)
            
            if ks1 == keystreams[1]:
                print(f"¡Estado inicial encontrado!")
                print(f"state0 = {state_candidate}")
                print(f"low_bits = {low_bits}")
                print()
                
                # Descifrar toda la flag
                print("Descifrando la flag...")
                state = state_candidate
                plaintext = b""
                
                for j in range(len(output)):
                    ks = pow(B, state & ~0xffff, m)
                    chunk = output[j] ^ ks
                    chunk_bytes = long_to_bytes(chunk)
                    if len(chunk_bytes) < 10:
                        chunk_bytes = b'\x00' * (10 - len(chunk_bytes)) + chunk_bytes
                    plaintext += chunk_bytes
                    
                    # Actualizar estado
                    state = pow(pow(A, state, m) ^ B, e, m)
                
                # Limpiar plaintext
                plaintext = plaintext.rstrip(b'\x00')
                print(f"\nPlaintext: {plaintext}")
                exit(0)
        
        print("No se encontró coincidencia en los últimos 16 bits")
    else:
        print(f"Verificación fallida: pow(B, {x_combined}, m) != keystream_0")
else:
    print("No se pudieron resolver todas las ecuaciones modulares")
