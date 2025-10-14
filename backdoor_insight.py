from Crypto.Util.number import bytes_to_long, long_to_bytes
import gmpy2

# Parámetros
p1, p2, p3, p4 = 10124460123717732577, 12017858281002457601, 15013023439701145679, 17297082179958074003
p5 = 309938271107370186286857659422407283771865851657937731111744300310040346308690205006641245318085354895438500308814135783504803596134094206083383195557983
m = p1 * p2 * p3 * p4 * p5

A = 246920531455433048826966670968977027196902794022573095007307132382393013927558904839982249967656424317118051446771969623490992917094197975459553923550187
B = 3120090466259654766880909097573553950487818021670727992039931232537173262599219376624291488340607228938989670215080876932583555412966984946786628621917436142053528648425399877486481618672307477414787846984446437445450282569184963
e = 4180488827

# Tengo el inverso de e
phi_m = (p1-1) * (p2-1) * (p3-1) * (p4-1) * (p5-1)
d = int(gmpy2.invert(e, phi_m))

output_list = [263928838896714332657762314348602240455087661491500131260179929152321790693260683004004767933801216877412896467528419672112455669506824987777448696213888416333755744665868795853306879814179767910033263080874331851322593343273834, 7500716958005582985508201577146205078774368134456220390802616323312171951781595852608949532619393759348663684985174625019004577610546554994801687569942118260000292201829011312249563036393035204990811392856155820408283216493092108]

known_full = b"good luck lmao ictf{"
chunks_known = [bytes_to_long(known_full[i:i+10]) for i in range(0, len(known_full), 10)]

print("NUEVA IDEA: Usar el inverso de e para relacionar estados")
print()

# De la actualización:
# state_1 = (A^state_0 XOR B)^e mod m
#
# Entonces:
# state_1^d = A^state_0 XOR B mod m
# A^state_0 = state_1^d XOR B mod m

# output_0 = B^(state_0 >> 16 << 16) mod m
# output_1 = B^(state_1 >> 16 << 16) mod m

# Si supiera state_1, podría calcular A^state_0 = state_1^d XOR B
# Y luego necesitaría resolver log_A(A^state_0) = state_0

# Pero no conozco state_1, solo conozco output_1 XOR chunk_1 = B^(state_1 >> 16 << 16)

print("Idea: Bruteforcear state_1 (sin los últimos 16 bits)")
print("Como state_1 viene de (algo)^e, podría tener estructura")
print()

# Si state_1 tiene pocos bits, puedo probar directamente
print("Probando state_1 pequeño (sin low 16 bits)...")

keystream_1 = output_list[1] ^ chunks_known[1]

max_bits = 64  # Probar hasta 64 bits
for state_1_high in range(2**(max_bits)):
    state_1_partial = state_1_high << 16
    
    # Verificar si B^state_1_partial == keystream_1
    test = pow(B, state_1_partial, m)
    if test == keystream_1:
        print(f"\n¡STATE_1 (sin low 16 bits) ENCONTRADO!")
        print(f"state_1_high = {state_1_high}")
        print(f"state_1_partial = {state_1_partial}")
        print(f"Bits: {state_1_partial.bit_length()}")
        
        # Ahora puedo intentar encontrar state_0
        # state_1 = (A^state_0 XOR B)^e mod m
        # A^state_0 XOR B = state_1^d mod m
        # A^state_0 = (state_1^d mod m) XOR B
        
        # Necesito probar con diferentes low_bits de state_1
        for low_bits_1 in range(65536):
            state_1_full = state_1_partial | low_bits_1
            
            # Calcular A^state_0
            val = pow(state_1_full, d, m)
            A_pow_state_0 = val ^ B
            
            # Ahora necesito state_0 tal que A^state_0 = A_pow_state_0
            # Esto sigue siendo un log discreto, pero puedo probar si state_0 es pequeño
            
            # O... verificar con el primer output
            # Si state_0 es pequeño, puedo probarlo
            
            for state_0_high in range(2**40):  # Probar hasta 40 bits
                state_0_partial = state_0_high << 16
                
                # Verificar: A^state_0_partial == A_pow_state_0?
                test_A = pow(A, state_0_partial, m)
                if test_A == A_pow_state_0:
                    print(f"\n¡STATE_0 (sin low 16 bits) ENCONTRADO!")
                    print(f"state_0_partial = {state_0_partial}")
                    
                    # Verificar con output_0
                    for low_bits_0 in range(65536):
                        state_0_full = state_0_partial | low_bits_0
                        ks0 = pow(B, state_0_full - (state_0_full & 0xffff), m)
                        if ks0 == (output_list[0] ^ chunks_known[0]):
                            print(f"¡LOW BITS DE STATE_0 = {low_bits_0}!")
                            print(f"Estado inicial completo: {state_0_full}")
                            
                            # Descifrar
                            plaintext = b""
                            temp_state = state_0_full
                            for out in output_list:
                                keystream = pow(B, temp_state - (temp_state & 0xffff), m)
                                chunk_val = out ^ keystream
                                chunk_bytes = long_to_bytes(chunk_val)
                                plaintext += chunk_bytes
                                temp_state = pow(pow(A, temp_state, m) ^ B, e, m)
                            
                            print("\n" + "="*60)
                            print(plaintext.decode('utf-8', errors='ignore'))
                            print("="*60)
                            exit(0)
                
                if state_0_high % 100000 == 0 and state_0_high > 0:
                    print(f"    Probando state_0_high = {state_0_high}...")
        
        break
    
    if state_1_high % 10000 == 0 and state_1_high > 0:
        print(f"  state_1_high = {state_1_high}...")

print("\nNo encontrado con este enfoque")
