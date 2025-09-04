import re
import sys
import hashlib
import os
from typing import List, Tuple


MOD = 10 ** 10000


def load_module_constants(module_path: str) -> Tuple[int, str, bytes]:
    with open(module_path, "r") as f:
        src = f.read()
    iters_m = re.search(r"^ITERS\s*=\s*int\(([^)]+)\)\s*$", src, re.M)
    if not iters_m:
        iters_m = re.search(r"^ITERS\s*=\s*(\d+)\s*$", src, re.M)
    if not iters_m:
        raise ValueError("ITERS not found")
    iters_expr = iters_m.group(1)
    ITERS = int(eval(iters_expr, {}))

    verif_m = re.search(r'^VERIF_KEY\s*=\s*"([0-9a-fA-F]+)"\s*$', src, re.M)
    if not verif_m:
        raise ValueError("VERIF_KEY not found")
    VERIF_KEY = verif_m.group(1)

    enc_m = re.search(r'ENCRYPTED_FLAG\s*=\s*bytes\.fromhex\("([0-9a-fA-F\n\r\t ]+)"\)\s*', src, re.S)
    if not enc_m:
        raise ValueError("ENCRYPTED_FLAG not found")
    hex_str = enc_m.group(1)
    hex_str = re.sub(r"\s+", "", hex_str)
    ENCRYPTED_FLAG = bytes.fromhex(hex_str)
    return ITERS, VERIF_KEY, ENCRYPTED_FLAG


def mat_mul(a: List[List[int]], b: List[List[int]]) -> List[List[int]]:
    n = len(a)
    m = len(b[0])
    k = len(b)
    res = [[0] * m for _ in range(n)]
    for i in range(n):
        ai = a[i]
        for t in range(k):
            ait = ai[t]
            if ait == 0:
                continue
            bt = b[t]
            for j in range(m):
                res[i][j] = (res[i][j] + ait * bt[j]) % MOD
    return res


def mat_pow(mat: List[List[int]], exp: int) -> List[List[int]]:
    n = len(mat)
    # Identity
    res = [[0] * n for _ in range(n)]
    for i in range(n):
        res[i][i] = 1
    base = [row[:] for row in mat]
    e = exp
    while e > 0:
        if e & 1:
            res = mat_mul(res, base)
        base = mat_mul(base, base)
        e >>= 1
    return res


def mat_vec_mul(mat: List[List[int]], vec: List[int]) -> List[int]:
    n = len(mat)
    m = len(vec)
    out = [0] * n
    for i in range(n):
        s = 0
        row = mat[i]
        for j in range(m):
            if row[j] != 0:
                s = (s + row[j] * vec[j]) % MOD
        out[i] = s
    return out


def compute_term_n(n: int) -> int:
    # Base cases
    if n == 0:
        return 1
    if n == 1:
        return 2
    if n == 2:
        return 3
    if n == 3:
        return 4
    # Companion matrix for:
    # m(k+1) = 21*m(k) + 301*m(k-1) - 9549*m(k-2) + 55692*m(k-3)
    M = [
        [21 % MOD, 301 % MOD, (-9549) % MOD, 55692 % MOD],
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
    ]
    # State S(3) = [m3, m2, m1, m0]
    S3 = [4 % MOD, 3 % MOD, 2 % MOD, 1 % MOD]
    P = mat_pow(M, n - 3)
    Sn = mat_vec_mul(P, S3)
    return Sn[0] % MOD


def decrypt_flag(sol: int, verif_key: str, enc_flag: bytes) -> str:
    sol_mod = sol % MOD
    sol_str = str(sol_mod)
    sol_md5 = hashlib.md5(sol_str.encode()).hexdigest()
    if sol_md5 != verif_key:
        raise SystemExit("Incorrect solution")
    key = hashlib.sha256(sol_str.encode()).digest()
    flag = bytearray([b ^ key[i] for i, b in enumerate(enc_flag)]).decode()
    return flag


def main():
    here = os.path.dirname(__file__)
    seq_path = os.path.join(here, "sequences.py")
    ITERS, VERIF_KEY, ENCRYPTED_FLAG = load_module_constants(seq_path)
    try:
        # Python 3.11+ safety for big int to string conversions
        if hasattr(sys, "set_int_max_str_digits"):
            sys.set_int_max_str_digits(20000)
    except Exception:
        pass
    sol = compute_term_n(ITERS)
    flag = decrypt_flag(sol, VERIF_KEY, ENCRYPTED_FLAG)
    print(flag)


if __name__ == "__main__":
    main()

