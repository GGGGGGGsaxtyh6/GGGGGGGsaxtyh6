import math
from typing import Dict, List, Tuple


def parse_hex_multiline(value_line: str) -> int:
    parts = value_line.split("=", 1)[1].strip().replace("\n", "").replace(" ", "")
    return int(parts, 16)


def read_nc(path: str) -> Tuple[int, int]:
    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    n_hex_lines = []
    c_hex_lines = []
    reading_n = False
    reading_c = False
    for line in lines:
        if line.startswith("n ="):
            reading_n = True
            reading_c = False
            n_hex_lines = [line.split("=", 1)[1].strip()]
            continue
        if line.startswith("c ="):
            reading_c = True
            reading_n = False
            c_hex_lines = [line.split("=", 1)[1].strip()]
            continue
        if reading_n:
            n_hex_lines.append(line)
        if reading_c:
            c_hex_lines.append(line)
    n_hex = "".join([s.replace(" ", "") for s in n_hex_lines])
    c_hex = "".join([s.replace(" ", "") for s in c_hex_lines])
    return int(n_hex, 16), int(c_hex, 16)


def sieve_primes(limit: int) -> List[int]:
    if limit < 2:
        return []
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:2] = b"\x00\x00"
    for p in range(2, int(limit**0.5) + 1):
        if sieve[p]:
            step = p
            start = p * p
            sieve[start: limit + 1: step] = b"\x00" * (((limit - start) // step) + 1)
    return [i for i, is_p in enumerate(sieve) if is_p]


def pollards_p_minus_one(n: int, B: int = 200000, base_candidates: Tuple[int, ...] = (2, 3, 5, 7, 11, 13)) -> int:
    primes = sieve_primes(B)
    for base in base_candidates:
        a = base % n
        for p in primes:
            # compute a = a^(p^k) mod n, where p^k <= B
            pk = p
            while pk * p <= B:
                pk *= p
            a = pow(a, pk, n)
            g = math.gcd(a - 1, n)
            if 1 < g < n:
                return g
            if g == n:
                # Degenerate: try next base
                break
    return 1


def factor_smooth(m: int, primes: List[int]) -> Dict[int, int]:
    factors: Dict[int, int] = {}
    for p in primes:
        if p * p > m:
            break
        if m % p == 0:
            e = 0
            while m % p == 0:
                m //= p
                e += 1
            factors[p] = e
    if m > 1:
        # Remaining factor should be 1 (if fully smooth) or a prime just above limit
        factors[m] = factors.get(m, 0) + 1
    return factors


def bsgs(g: int, h: int, p: int, order: int) -> int:
    m = int(math.isqrt(order)) + 1
    table = {}
    x = 1
    for j in range(m):
        if x not in table:
            table[x] = j
        x = (x * g) % p
    g_inv_m = pow(pow(g, m, p), -1, p)
    gamma = h % p
    for i in range(m + 1):
        if gamma in table:
            return (i * m + table[gamma]) % order
        gamma = (gamma * g_inv_m) % p
    raise ValueError("log not found")


def pohlig_hellman_prime_power(g: int, h: int, p: int, r: int, e: int, N: int) -> int:
    # General lifting, but here e is expected to be 1 for this challenge
    x = 0
    g0 = pow(g, N // (r ** e), p)
    h0 = pow(h, N // (r ** e), p)
    if e == 1:
        return bsgs(g0, h0, p, r)
    # Fallback general case
    for i in range(e):
        c = pow(h0 * pow(g0, -x, p) % p, r ** (e - 1 - i), p)
        d = pow(g0, r ** (e - 1 - i), p)
        a_i = bsgs(d, c, p, r)
        x = x + a_i * (r ** i)
    return x


def discrete_log_pohlig_hellman(g: int, h: int, p: int, factors: Dict[int, int]) -> Tuple[int, int]:
    # Solve x modulo N = p-1
    N = p - 1
    congruences: List[Tuple[int, int]] = []  # (x_i mod r^e, r^e)
    for r, e in factors.items():
        x_re = pohlig_hellman_prime_power(g, h, p, r, e, N)
        congruences.append((x_re, r ** e))
    # Combine via CRT
    x = 0
    m = 1
    for a_i, m_i in congruences:
        x, m = crt_pair(x, m, a_i, m_i)
    return x, m  # x mod m (should equal N if fully factored)


def egcd(a: int, b: int) -> Tuple[int, int, int]:
    if b == 0:
        return (a, 1, 0)
    g, x1, y1 = egcd(b, a % b)
    return (g, y1, x1 - (a // b) * y1)


def crt_pair(a1: int, m1: int, a2: int, m2: int) -> Tuple[int, int]:
    g, x, y = egcd(m1, m2)
    if (a2 - a1) % g != 0:
        raise ValueError("Incompatible congruences")
    lcm = m1 // g * m2
    t = ((a2 - a1) // g) * x % (m2 // g)
    res = (a1 + m1 * t) % lcm
    return res, lcm


def int_to_ascii(m: int) -> str:
    hex_str = format(m, "x")
    if len(hex_str) % 2 == 1:
        hex_str = "0" + hex_str
    try:
        return bytes.fromhex(hex_str).decode("utf-8", errors="strict")
    except Exception:
        return ""


def compute_multiplicative_order(g: int, p: int, factors: Dict[int, int]) -> int:
    # Start with p-1 and divide out factors when possible
    order = p - 1
    for r, e in factors.items():
        for _ in range(e):
            if order % r == 0 and pow(g, order // r, p) == 1:
                order //= r
            else:
                break
    return order


def main():
    n, c = read_nc("output.txt")
    # Factor n via Pollard p-1
    # Try multiple bases/B if needed
    p = 1
    for B in (200000, 400000, 800000, 1200000, 2000000):
        g = pollards_p_minus_one(n, B=B)
        if 1 < g < n:
            p = g
            break
    if not (1 < p < n):
        raise RuntimeError("Failed to factor n")
    q = n // p
    print(f"[+] factored n: p bits={p.bit_length()} q bits={q.bit_length()}")

    # Factor p-1 and q-1 using trial division with a safe prime bound
    max_prime_bound = 300000
    primes = sieve_primes(max_prime_bound)
    factors_p = factor_smooth(p - 1, primes)
    factors_q = factor_smooth(q - 1, primes)
    print(f"[+] #(factors) p-1={len(factors_p)} q-1={len(factors_q)}")

    # Discrete logs modulo p and q using Pohlig–Hellman
    g = 3
    order_p = compute_multiplicative_order(g % p, p, factors_p)
    order_q = compute_multiplicative_order(g % q, q, factors_q)
    print(f"[+] ord_p={order_p}\n[+] ord_q={order_q}")
    # Restrict factors to those dividing the order
    def restrict_factors(factors: Dict[int, int], order: int) -> Dict[int, int]:
        res: Dict[int, int] = {}
        for r, e in factors.items():
            cnt = 0
            t = order
            while t % r == 0 and cnt < e:
                t //= r
                cnt += 1
            if cnt > 0:
                res[r] = cnt
        return res
    factors_p_eff = restrict_factors(factors_p, order_p)
    factors_q_eff = restrict_factors(factors_q, order_q)
    x_p, mod_p = discrete_log_pohlig_hellman(g % p, c % p, p, factors_p_eff)
    x_q, mod_q = discrete_log_pohlig_hellman(g % q, c % q, q, factors_q_eff)
    # verify local solutions
    assert pow(g, x_p, p) == c % p
    assert pow(g, x_q, q) == c % q
    print(f"[+] moduli: mod_p={mod_p} mod_q={mod_q}")

    # Combine with CRT to get x modulo l = lcm(mod_p, mod_q)
    x, l = crt_pair(x_p, mod_p, x_q, mod_q)
    assert pow(g, x, n) == c % n
    print(f"[+] l = {l}")

    # Recover ASCII; since FLAG < l, x should equal FLAG
    candidate = int_to_ascii(x)
    if candidate:
        print(f"[?] candidate0: {candidate}")
    if candidate.startswith("picoCTF{") and candidate.endswith("}"):
        print(candidate)
        return
    # Otherwise, try adding multiples of l (unlikely needed)
    for k in range(1, 1000):
        m = x + k * l
        s = int_to_ascii(m)
        if s.startswith("picoCTF{") and s.endswith("}"):
            print(s)
            return
    raise RuntimeError("FLAG not recovered. Try increasing bounds.")


if __name__ == "__main__":
    main()

