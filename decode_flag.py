#!/usr/bin/env python3
import binascii

def xor_decrypt(data, key):
    """Desencripta usando XOR con una clave"""
    result = []
    for i, byte in enumerate(data):
        result.append(byte ^ key[i % len(key)])
    return bytes(result)

def try_common_keys(encrypted_data):
    """Prueba claves comunes para desencriptar"""
    common_keys = [
        b'key',
        b'pico',
        b'flag',
        b'ctf',
        b'\x42',
        b'\x13', 
        b'\xaa',
        b'\x01',
        b'\xff',
        b'picoCTF',
        b'binary',
        b'inst',
        b'writeFile'
    ]
    
    print("Probando claves comunes:")
    for key in common_keys:
        try:
            decrypted = xor_decrypt(encrypted_data, key)
            # Verificar si el resultado parece una flag válida
            if b'pico' in decrypted.lower() or b'flag' in decrypted.lower() or decrypted.startswith(b'{') or b'CTF' in decrypted:
                print(f"Clave {key}: {decrypted}")
        except:
            pass

def try_single_byte_xor(encrypted_data):
    """Prueba XOR de un solo byte (0-255)"""
    print("\nProbando XOR de un solo byte:")
    for key in range(256):
        try:
            decrypted = xor_decrypt(encrypted_data, bytes([key]))
            # Verificar si parece texto legible
            if all(32 <= b <= 126 for b in decrypted):  # ASCII imprimible
                if b'pico' in decrypted.lower() or b'flag' in decrypted.lower() or b'CTF' in decrypted:
                    print(f"Clave 0x{key:02x}: {decrypted}")
        except:
            pass

def analyze_flag():
    # La flag encriptada encontrada
    hex_flag = "7b661bad1f1a0dab6caca2f71a54fce0ba9be0b5950ab42d162f912156ab5bd9b784b49e0cb5485914967e02a9fc7d"
    
    print(f"Flag encriptada (hex): {hex_flag}")
    
    # Convertir a bytes
    encrypted_data = binascii.unhexlify(hex_flag)
    print(f"Longitud: {len(encrypted_data)} bytes")
    print(f"Datos: {encrypted_data}")
    
    # Intentar diferentes métodos de desencriptación
    try_common_keys(encrypted_data)
    try_single_byte_xor(encrypted_data)
    
    # Análisis adicional
    print(f"\nAnálisis de patrones:")
    print(f"Primer byte: 0x{encrypted_data[0]:02x} ('{chr(encrypted_data[0]) if 32 <= encrypted_data[0] <= 126 else '?'}')")
    print(f"Último byte: 0x{encrypted_data[-1]:02x} ('{chr(encrypted_data[-1]) if 32 <= encrypted_data[-1] <= 126 else '?'}')")
    
    # Verificar si ya empieza con { y termina con }
    if encrypted_data[0] == ord('{') and encrypted_data[-1] == ord('}'):
        print("¡Los datos ya empiezan con { y terminan con }!")
        try:
            # Intentar decodificar el contenido interno
            inner_data = encrypted_data[1:-1]  # Sin las llaves
            print(f"Contenido interno: {inner_data.hex()}")
            
            # Probar XOR en el contenido interno
            for key in range(256):
                try:
                    decrypted_inner = xor_decrypt(inner_data, bytes([key]))
                    if all(32 <= b <= 126 for b in decrypted_inner):
                        full_flag = b'{' + decrypted_inner + b'}'
                        print(f"Posible flag con clave 0x{key:02x}: {full_flag}")
                except:
                    pass
        except:
            pass

if __name__ == "__main__":
    analyze_flag()