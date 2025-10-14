import random
import math
from typing import Dict, List, Tuple

# Challenge constants
m = 9792986822963146992114161946549377254001156012300083076259452975070903436656675903033418798369811004678022807932064872669773556983318074157606463933686225452143852071767552582367819932516654167400507310054793760473098421162463267
A = 246920531455433048826966670968977027196902794022573095007307132382393013927558904839982249967656424317118051446771969623490992917094197975459553923550187
B = 3120090466259654766880909097573553950487818021670727992039931232537173262599219376624291488340607228938989670215080876932583555412966984946786628621917436142053528648425399877486481618672307477414787846984446437445450282569184963
e = 4180488827

CT = [
    263928838896714332657762314348602240455087661491500131260179929152321790693260683004004767933801216877412896467528419672112455669506824987777448696213888416333755744665868795853306879814179767910033263080874331851322593343273834,
    7500716958005582985508201577146205078774368134456220390802616323312171951781595852608949532619393759348663684985174625019004577610546554994801687569942118260000292201829011312249563036393035204990811392856155820408283216493092108,
    2577794401090299805723177598637436117371525412262771825236813936115237585602114357696686099541164980249580094089526387369627399445447896464668107355247993148990034255262021717192029828447047736912032562575292618672346226630177737,
    9097092753543027532933159793556144814276134227405286080166556624316657274280165256861623248902541076900039285592392074751617153907616670295765377162951858063712964557527212039482031296350052367350738141716598584719951567052177519,
    8174235910244322855637254130843352735528509191186418212056519911128301630950848710182451421471531481098828227735010211554839205099309290314993113489826162548089590990963249899714956197889959999884447438378454452096405595048394416,
    2823506900640363315693941780283568096117331722098156706833610340919194199647098542170689133810904702849664199290565773405646243449194786656181872671323095023235608799444864036190997987871160063941897196360905342203429250068859314,
    4625135637721297092934166648990860031642126233341589454312760229225192256970211899532356300747405146834048765116081788846632527090729839758895834854075755594692611781829177188955301784020596520269704429107749955107365380494152652,
]

KNOWN_PREFIX = b"good luck lmao ictf{"

# Utilities: Miller-Rabin, Pollard Rho, factorization

def is_probable_prime(n: int) -> bool:
    if n < 2:
        return False
    small_primes = [2,3,5,7,11,13,17,19,23,29,31,37]
    for p in small_primes:
        if n % p == 0:
            return n == p
    # write n-1 as d * 2^s
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    # Deterministic bases for 64-bit are known, for 761-bit we'll use several random bases
    bases = [2, 3, 5, 7, 11, 13, 17, 19, 23]
    # Add some random bases
    rand = random.Random(1337)
    for _ in range(4):
        a = rand.randrange(2, min(n - 2, (1 << 32)))
        bases.append(a)
    for a in bases:
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        skip = False
        for _ in range(s - 1):
            x = (x * x) % n
            if x == n - 1:
                skip = True
                break
        if skip:
            continue
        return False
    return True


def pollards_rho(n: int) -> int:
    if n % 2 == 0:
        return 2
    if n % 3 == 0:
        return 3
    # random polynomial f(x) = x^2 + c
    rand = random.Random()
    while True:
        c = rand.randrange(1, n - 1)
        x = rand.randrange(2, n - 1)
        y = x
        d = 1
        while d == 1:
            x = (x * x + c) % n
            y = (y * y + c) % n
            y = (y * y + c) % n
            d = math.gcd(abs(x - y), n)
            if d == n:
                break
        if 1 < d < n:
            return d


def factor(n: int, res: Dict[int, int]):
    if n == 1:
        return
    if is_probable_prime(n):
        res[n] = res.get(n, 0) + 1
        return
    # trial division by small primes up to some bound for speed
    # Using a small wheel
    for p in [2,3,5]:
        while n % p == 0:
            res[p] = res.get(p, 0) + 1
            n //= p
    # quick trial division up to 10000
    i = 7
    wheel = [4,2,4,2,4,6,2,6]
    wi = 0
    bound = 10000
    while i <= bound and i * i <= n:
        while n % i == 0:
            res[i] = res.get(i, 0) + 1
            n //= i
        i += wheel[wi]
        wi = (wi + 1) % len(wheel)
    if n == 1:
        return
    if is_probable_prime(n):
        res[n] = res.get(n, 0) + 1
        return
    d = pollards_rho(n)
    factor(d, res)
    factor(n // d, res)

# Compute order of element g modulo m given group order n

def compute_order(g: int, n: int, fac: Dict[int, int], mod: int) -> int:
    order = n
    for p, a in fac.items():
        for _ in range(a):
            if pow(g, order // p, mod) == 1:
                order //= p
            else:
                break
    return order

# CRT combine a list of (x_i, mod_i)

def crt(pairs: List[Tuple[int, int]]) -> Tuple[int, int]:
    x = 0
    M = 1
    for _, m_i in pairs:
        M *= m_i
    for x_i, m_i in pairs:
        M_i = M // m_i
        inv = pow(M_i, -1, m_i)
        x = (x + x_i * M_i * inv) % M
    return x, M

# Discrete log via Pohlig-Hellman for prime powers and CRT

def dlog_pohlig_hellman(g: int, h: int, mod: int, order: int, order_factors: Dict[int, int]) -> int:
    congruences: List[Tuple[int, int]] = []
    for p, a in order_factors.items():
        q = p ** a
        n_i = order // q
        g_i = pow(g, n_i, mod)
        h_i = pow(h, n_i, mod)
        # Solve for x mod q
        x = 0
        g_inv = pow(g, -1, mod)
        for j in range(a):
            # h_j = (h * g^{-x})^{order / p^{j+1}}
            h_j = pow((h * pow(pow(g, x, mod), -1, mod)) % mod, order // (p ** (j + 1)), mod)
            g_j = pow(g, order // (p ** (j + 1)), mod)
            # Find d in 0..p-1 with g_j^d == h_j
            d = None
            cur = 1
            for k in range(p):
                if cur == h_j:
                    d = k
                    break
                cur = (cur * g_j) % mod
            if d is None:
                # Fallback linear search failure; but for small p this should not happen
                raise ValueError("Discrete log digit not found; bad factorization or inputs")
            x += d * (p ** j)
        congruences.append((x % q, q))
    # Combine via CRT
    x, M = crt(congruences)
    # x is modulo 'order'
    return x % order


def main():
    # Build known plaintext blocks
    pt0 = int.from_bytes(KNOWN_PREFIX[:10], 'big')
    pt1 = int.from_bytes(KNOWN_PREFIX[10:20], 'big')
    k0 = CT[0] ^ pt0
    k1 = CT[1] ^ pt1

    # Generator for keystream subgroup
    g = pow(B, 1 << 16, m)

    # Factor group order n = m-1
    n = m - 1
    fac: Dict[int, int] = {}
    factor(n, fac)
    # Compute order of g
    order_g = compute_order(g, n, fac, m)

    # Factor order_g (subset of fac)
    fac_order: Dict[int, int] = {}
    tmp = order_g
    for p, a in fac.items():
        cnt = 0
        while tmp % p == 0:
            tmp //= p
            cnt += 1
        if cnt:
            fac_order[p] = cnt
    if tmp != 1:
        # If leftover, factor it
        factor(tmp, fac_order)
        # Recompute tmp to ensure fully factored
        tmp2 = order_g
        for p, a in fac_order.items():
            for _ in range(a):
                if tmp2 % p == 0:
                    tmp2 //= p
        if tmp2 != 1:
            # As a safeguard, include remaining part as prime factor if prime
            if is_probable_prime(tmp2):
                fac_order[tmp2] = fac_order.get(tmp2, 0) + 1
            else:
                pass

    # Compute discrete logs s_high0 and s_high1
    s_high0 = dlog_pohlig_hellman(g, k0, m, order_g, fac_order)
    s_high1_target = dlog_pohlig_hellman(g, k1, m, order_g, fac_order)

    # Precompute A^{s_high0 << 16}
    A_high = pow(A, s_high0 << 16, m)
    # Precompute A^low for low in 0..65535
    A_low = [1] * 65536
    for i in range(1, 65536):
        A_low[i] = (A_low[i-1] * A) % m

    found_low = None
    s0 = None
    # Bruteforce low 16 bits; for each, compute s1 and compare s1_high modulo order_g to target
    for low in range(65536):
        X = (A_high * A_low[low]) % m
        s1 = pow(X ^ B, e, m)
        s1_high = s1 >> 16
        if s1_high % order_g == s_high1_target:
            found_low = low
            s0 = (s_high0 << 16) | low
            break

    if s0 is None:
        raise SystemExit("Failed to recover state low 16 bits")

    # With full initial state s0, decrypt all blocks
    state = s0
    keystream = []
    for _ in CT:
        ks = pow(B, state - (state & 0xffff), m)
        keystream.append(ks)
        state = pow((pow(A, state, m) ^ B), e, m)

    # Decrypt to bytes
    pt_bytes = b""
    for ct, ks in zip(CT, keystream):
        x = ct ^ ks
        b = x.to_bytes(10, 'big')
        pt_bytes += b

    # Print plaintext; strip potential zero padding at end
    print(pt_bytes)

if __name__ == '__main__':
    main()
