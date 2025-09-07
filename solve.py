#!/usr/bin/env python3

from Crypto.Util.number import long_to_bytes, bytes_to_long
from sympy import integer_nthroot

# Given values from the challenge
e = 5
N = 24778450034785355796150191255487074823099958164427517612668815658468206009158475774203229828058652831641389747402272728790787685762568229069520469756247804941312947307153713830371750706901868389560472732254665749033734649996443767231968425511092244591774647092925931126950380935008196052393893271837275626174525444417778170526468251066473481105512939105882134615031671691748551289394109269703632798650982887859648332846094423809290782207835604174269463315884480062803289020119565250762542625596177768616201281918850432872639983965071018579891448754659608103400036049016809640134053891855019010729470727777892901808607
enc1 = 25889043021335548821260878832004378483521260681242675042883194031946048423533693101234288009087668042920762024679407711250775447692855635834947612028253548739678779
enc2 = 332075826660041992234163956636404156206918624

def vigenere_decrypt(ciphertext, key):
    """Decrypt Vigenère cipher"""
    decrypted = b""
    for i in range(len(ciphertext)):
        decrypted += bytes([(ciphertext[i] - key[i % len(key)]) % 256])
    return decrypted

def find_rsa_key():
    """Find the RSA key by taking the 5th root of enc2"""
    print(f"Trying to find 5th root of enc2: {enc2}")
    
    # Try to find the 5th root
    root, is_exact = integer_nthroot(enc2, 5)
    if is_exact:
        print(f"Found exact 5th root: {root}")
        return long_to_bytes(root)
    else:
        print(f"5th root not exact: {root}")
        # Try the exact root and root+1
        for candidate in [root, root + 1]:
            if pow(candidate, 5) == enc2:
                print(f"Found key with candidate {candidate}")
                return long_to_bytes(candidate)
    
    # If that doesn't work, try brute force for small values
    print("Trying brute force for small 4-byte keys...")
    for i in range(2**32):  # 4 bytes = 32 bits
        key_bytes = i.to_bytes(4, 'big')
        if pow(bytes_to_long(key_bytes), 5, N) == enc2:
            print(f"Found key via brute force: {key_bytes}")
            return key_bytes
    
    return None

def main():
    print("=== Amo and Boko's Secret Message Decoder ===")
    print(f"RSA Public Key: e={e}, N={N}")
    print(f"enc1 (Vigenère encrypted flag): {enc1}")
    print(f"enc2 (RSA encrypted key): {enc2}")
    print()
    
    # Step 1: Find the Vigenère key by decrypting enc2
    print("Step 1: Finding the Vigenère key...")
    key = find_rsa_key()
    
    if key is None:
        print("Failed to find the key!")
        return
    
    print(f"Found Vigenère key: {key}")
    print()
    
    # Step 2: Decrypt the flag using the Vigenère key
    print("Step 2: Decrypting the flag...")
    flag_encrypted = long_to_bytes(enc1)
    print(f"Encrypted flag as bytes: {flag_encrypted}")
    
    flag = vigenere_decrypt(flag_encrypted, key)
    print(f"Decrypted flag: {flag}")
    
    # Try to decode as string
    try:
        flag_str = flag.decode('utf-8')
        print(f"Flag as string: {flag_str}")
    except:
        print("Could not decode as UTF-8, trying other encodings...")
        try:
            flag_str = flag.decode('latin-1')
            print(f"Flag as latin-1: {flag_str}")
        except:
            print("Could not decode flag as text")

if __name__ == "__main__":
    main()