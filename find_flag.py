#!/usr/bin/env python3
import re
import sys

def xor_decode(data, key):
    """Decodifica datos usando XOR con una clave"""
    result = []
    for i, byte in enumerate(data):
        result.append(byte ^ key[i % len(key)])
    return bytes(result)

def analyze_binary(filename):
    """Analiza el binario buscando patrones de flags"""
    with open(filename, 'rb') as f:
        data = f.read()
    
    print(f"Analizando {filename}...")
    print(f"Tamaño del archivo: {len(data)} bytes")
    
    # Buscar patrones que empiecen con { (0x7b)
    flag_patterns = []
    for i in range(len(data) - 20):  # Buscar al menos 20 bytes
        if data[i] == 0x7b:  # {
            # Buscar el } correspondiente en los próximos 50 bytes
            for j in range(i + 1, min(i + 50, len(data))):
                if data[j] == 0x7d:  # }
                    pattern = data[i:j+1]
                    flag_patterns.append((i, pattern))
                    break
    
    print(f"\nEncontrados {len(flag_patterns)} patrones con {{ }}:")
    
    for offset, pattern in flag_patterns:
        print(f"\nOffset 0x{offset:08x}: {pattern.hex()}")
        print(f"ASCII: {pattern}")
        
        # Intentar decodificación XOR con claves comunes
        common_keys = [b'key', b'flag', b'pico', b'\x42', b'\x13', b'\xaa']
        for key in common_keys:
            try:
                decoded = xor_decode(pattern, key)
                if b'pico' in decoded.lower() or b'flag' in decoded.lower():
                    print(f"XOR con {key}: {decoded}")
            except:
                pass
    
    # Buscar strings que contengan "pico" o "flag" en diferentes encodings
    text_data = data.decode('latin-1', errors='ignore')
    
    # Buscar patrones de flag típicos
    flag_regex = re.compile(r'pico[^}]*}|flag[^}]*}|{[^}]*}', re.IGNORECASE)
    matches = flag_regex.findall(text_data)
    
    if matches:
        print(f"\nPatrones de texto encontrados:")
        for match in matches:
            print(f"  {match}")

if __name__ == "__main__":
    analyze_binary("bininst2.exe")