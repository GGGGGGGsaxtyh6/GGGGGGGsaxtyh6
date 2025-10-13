# Brute-force decryption for the SPN with 2-byte repeating key [a,b]*4

sa = {
    0: 15, 1: 2, 2: 14, 3: 0, 4: 1, 5: 3, 6: 10, 7: 6,
    8: 4, 9: 11, 10: 9, 11: 7, 12: 13, 13: 12, 14: 8, 15: 5
}
sb = {
    0: 12, 1: 8, 2: 13, 3: 6, 4: 9, 5: 1, 6: 11, 7: 14,
    8: 5, 9: 10, 10: 3, 11: 4, 12: 0, 13: 15, 14: 7, 15: 2
}

rsa = {v: k for k, v in sa.items()}
rsb = {v: k for k, v in sb.items()}

p_idx = [5, 2, 3, 1, 6, 0, 7, 4]
inv_idx = [0]*8
for i in range(8):
    inv_idx[p_idx[i]] = i


def to_bits8(x: int) -> str:
    return format(x & 0xFF, '08b')


def from_bits8(b: str) -> int:
    return int(b, 2)


def en_byte(x: int) -> int:
    b = to_bits8(x)
    a, c = b[:4], b[4:]
    s0 = sa[int(a, 2)]
    s1 = sb[int(c, 2)]
    bs = f"{s0:04b}{s1:04b}"
    out_bits = ''.join(bs[i] for i in p_idx)
    return from_bits8(out_bits)


def inv_en_byte(y: int) -> int:
    b = to_bits8(y)
    pre_bits = ''.join(b[i] for i in inv_idx)
    a, c = pre_bits[:4], pre_bits[4:]
    r0 = rsa[int(a, 2)]
    r1 = rsb[int(c, 2)]
    return (r0 << 4) | r1


# Ciphertext extracted from chall.py
ct = [
    190, 245, 36, 15, 132, 103, 116, 14, 59, 38, 28, 203,
    158, 245, 222, 157, 36, 100, 240, 206, 36, 205, 51, 206,
    90, 212, 222, 245, 83, 14, 222, 206, 163, 38, 59, 157, 83, 203, 28, 27
]

rounds = 5
block_len = 8


def decrypt_with_keys(ka: int, kb: int) -> bytes:
    out = []
    # process in 8-byte blocks
    for blk_start in range(0, len(ct), block_len):
        block = ct[blk_start:blk_start + block_len]
        for j in range(len(block)):
            x = block[j]
            for i in range(rounds - 1, -1, -1):
                x = inv_en_byte(x)
                use_a = ((i + j) % 2 == 0)
                x ^= (ka if use_a else kb)
            out.append(x)
    return bytes(out)


def is_printable_ascii(data: bytes) -> bool:
    for ch in data:
        if ch in (9, 10, 13):
            continue
        if ch < 32 or ch > 126:
            return False
    return True


best = None
# Search space: values in range(0, 255) inclusive of 254; safer include 255
for ka in range(0, 255):
    for kb in range(0, 255):
        pt = decrypt_with_keys(ka, kb)
        if is_printable_ascii(pt) and b'{' in pt and b'}' in pt:
            # additional light heuristic: likely flag-like
            best = (ka, kb, pt)
            print(pt.decode(errors='ignore'))
            # Stop at first plausible
            raise SystemExit(0)

# If we did not early-exit, try a weaker condition: just printable
for ka in range(0, 255):
    for kb in range(0, 255):
        pt = decrypt_with_keys(ka, kb)
        if is_printable_ascii(pt):
            best = (ka, kb, pt)
            print(pt.decode(errors='ignore'))
            raise SystemExit(0)

print("No candidate found")
