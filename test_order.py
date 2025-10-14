from Crypto.Util.number import *
import gmpy2

m = 9792986822963146992114161946549377254001156012300083076259452975070903436656675903033418798369811004678022807932064872669773556983318074157606463933686225452143852071767552582367819932516654167400507310054793760473098421162463267
B = 3120090466259654766880909097573553950487818021670727992039931232537173262599219376624291488340607228938989670215080876932583555412966984946786628621917436142053528648425399877486481618672307477414787846984446437445450282569184963

# ¡Esta podría ser la clave del backdoor!
# Si B^(2^16) = 1 mod m, entonces el output solo depende de los últimos 16 bits efectivamente
# Porque B^(state & ~0xffff) = B^(k * 2^16) para algún k
# Y si B^(2^16) = 1, entonces B^(k * 2^16) = (B^(2^16))^k = 1^k = 1

print("Verificando si B^(2^16) = 1 mod m...")
result = pow(B, 65536, m)
print(f"B^65536 mod m = {result}")
if result == 1:
    print("¡¡¡BACKDOOR ENCONTRADO!!! B^65536 = 1 mod m")
    print("Esto significa que el output solo depende de los últimos 16 bits del estado!")
else:
    print(f"B^65536 ≠ 1 mod m")
    
    # Probar otros órdenes relacionados con 16 bits
    for exp in [2**16, 2**17, 2**15, 2**14, 2**18, 2**20]:
        r = pow(B, exp, m)
        if r == 1:
            print(f"¡B^{exp} = 1 mod m!")

# También verificar divisores de 2^16
print("\nVerificando divisores de 65536...")
for exp in [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768]:
    r = pow(B, exp, m)
    if r == 1:
        print(f"¡B^{exp} = 1 mod m!")
        print(f"El orden de B divide a {exp}")
        break
