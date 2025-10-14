from math import gcd, isqrt
from typing import Dict, List, Tuple

m = 9792986822963146992114161946549377254001156012300083076259452975070903436656675903033418798369811004678022807932064872669773556983318074157606463933686225452143852071767552582367819932516654167400507310054793760473098421162463267
A = 246920531455433048826966670968977027196902794022573095007307132382393013927558904839982249967656424317118051446771969623490992917094197975459553923550187
B = 3120090466259654766880909097573553950487818021670727992039931232537173262599219376624291488340607228938989670215080876932583555412966984946786628621917436142053528648425399877486481618672307477414787846984446437445450282569184963

CT = [
    263928838896714332657762314348602240455087661491500131260179929152321790693260683004004767933801216877412896467528419672112455669506824987777448696213888416333755744665868795853306879814179767910033263080874331851322593343273834,
    7500716958005582985508201577146205078774368134456220390802616323312171951781595852608949532619393759348663684985174625019004577610546554994801687569942118260000292201829011312249563036393035204990811392856155820408283216493092108,
    2577794401090299805723177598637436117371525412262771825236813936115237585602114357696686099541164980249580094089526387369627399445447896464668107355247993148990034255262021717192029828447047736912032562575292618672346226630177737,
    9097092753543027532933159793556144814276134227405286080166556624316657274280165256861623248902541076900039285592392074751617153907616670295765377162951858063712964557527212039482031296350052367350738141716598584719951567052177519,
    8174235910244322855637254130843352735528509191186418212056519911128301630950848710182451421471531481098828227735010211554839205099309290314993113489826162548089590990963249899714956197889959999884447438378454452096405595048394416,
    2823506900640363315693941780283568096117331722098156706833610340919194199647098542170689133810904702849664199290565773405646243449194786656181872671323095023235608799444864036190997987871160063941897196360905342203429250068859314,
    4625135637721297092934166648990860031642126233341589454312760229225192256970211899532356300747405146834048765116081788846632527090729839758895834854075755594692611781829177188955301784020596520269704429107749955107365380494152652,
]

p_list = [
  10124460123717732577,
  12017858281002457601,
  15013023439701145679,
  17297082179958074003,
  309938271107370186286857659422407283771865851657937731111744300310040346308690205006641245318085354895438500308814135783504803596134094206083383195557983,
]

pt0 = int.from_bytes(b'good luck ', 'big')
pt1 = int.from_bytes(b'lmao ictf{', 'big')
ks0 = CT[0] ^ pt0
ks1 = CT[1] ^ pt1

# Utility: Pollard Rho integer factorization + Miller-Rabin

def is_probable_prime(n: int) -> bool:
    if n < 2:
        return False
    small_primes = [2,3,5,7,11,13,17,19,23,29,31,37]
    for p in small_primes:
        if n % p == 0:
            return n == p
    # Miller-Rabin deterministic style for 64-bit; for larger ok approximate
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    # bases (first few primes)
    for a in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]:
        if a >= n:
            continue
        x = pow(a, d, n)
        if x in (1, n-1):
            continue
        skip = False
        for _ in range(s-1):
            x = (x * x) % n
            if x == n - 1:
                skip = True
                break
        if skip:
            continue
        return False
    return True


def pollards_rho(n: int) -> int:
    import random
    if n % 2 == 0:
        return 2
    if n % 3 == 0:
        return 3
    while True:
        x = random.randrange(2, n-1)
        y = x
        c = random.randrange(1, n-1)
        d = 1
        while d == 1:
            x = (x * x + c) % n
            y = (y * y + c) % n
            y = (y * y + c) % n
            d = gcd(abs(x - y), n)
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
    # small trial division
    for p in [2,3,5]:
        while n % p == 0:
            res[p] = res.get(p, 0) + 1
            n //= p
    # wheel trial up to some bound
    i = 7
    wheel = [4,2,4,2,4,6,2,6]
    wi = 0
    bound = 50000
    while i * i <= n and i <= bound:
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

# Discrete log helpers

def bsgs(g: int, h: int, p: int, order: int) -> int:
    # Solve g^x = h mod p with x in [0, order-1]
    m = isqrt(order) + 1
    table = {}
    cur = 1
    for j in range(m):
        # store only first occurrence
        if cur not in table:
            table[cur] = j
        cur = (cur * g) % p
    factor = pow(g, -m, p)
    gamma = h % p
    for i in range(m + 1):
        if gamma in table:
            return (i * m + table[gamma]) % order
        gamma = (gamma * factor) % p
    return None


def compute_order(g: int, p: int, p_minus_1_factors: Dict[int, int]) -> int:
    order = p - 1
    for q, a in p_minus_1_factors.items():
        for _ in range(a):
            cand = order // q
            if pow(g, cand, p) == 1:
                order = cand
            else:
                break
    return order


def factor_power(n: int) -> Dict[int, int]:
    d: Dict[int,int] = {}
    factor(n, d)
    return d


def dlog_pohlig_hellman(g: int, h: int, p: int, order: int, order_factors: Dict[int,int]) -> int:
    congruences: List[Tuple[int, int]] = []
    for q, a in order_factors.items():
        q_pow = q ** a
        n_i = order // q_pow
        g_i = pow(g, n_i, p)
        h_i = pow(h, n_i, p)
        # Solve for x_i mod q^a via lifting
        x_i = 0
        for j in range(a):
            # c_j = h * g^{-x_i}
            c = (h * pow(pow(g, x_i, p), -1, p)) % p
            # reduce to order q
            cj = pow(c, order // (q ** (j + 1)), p)
            gj = pow(g, order // (q ** (j + 1)), p)
            # now solve gj^d = cj for d in [0, q-1]
            d = bsgs(gj, cj, p, q)
            if d is None:
                # failure
                raise ValueError('BSGS failed for subgroup of size %d' % q)
            x_i += d * (q ** j)
        congruences.append((x_i % q_pow, q_pow))
    # CRT combine
    x = 0
    M = 1
    for _, mod in congruences:
        M *= mod
    for a_i, m_i in congruences:
        M_i = M // m_i
        inv = pow(M_i, -1, m_i)
        x = (x + a_i * M_i * inv) % M
    return x % order

# 2-adic discrete log in prime field for g^{2^k}

def v2(n: int) -> int:
    c = 0
    while n % 2 == 0:
        n //= 2
        c += 1
    return c


def dlog_2power_component(g: int, h: int, p: int) -> Tuple[int,int]:
    # compute x mod 2^t where t = v2(order(g))
    # Let s = v2(p-1)
    s = v2(p - 1)
    # Reduce to 2-Sylow by raising by r=(p-1)/2^s
    r = (p - 1) >> s
    g2 = pow(g, r, p)
    h2 = pow(h, r, p)
    # compute t = order_2 of g2
    t = 0
    tmp = g2
    while tmp != 1 and t < s:
        tmp = pow(tmp, 2, p)
        t += 1
    # Now solve for x bits length t
    x = 0
    cur = h2
    G = [g2]
    for i in range(1, t):
        G.append(pow(G[-1], 2, p))
    T2 = G[t-1] if t>0 else 1
    for i in range(t):
        u = pow(cur, 1 << (t - 1 - i), p)
        if u == 1:
            bit = 0
        elif u == T2:
            bit = 1
            inv = pow(G[i], -1, p)
            cur = (cur * inv) % p
        else:
            raise ValueError('Not in 2-subgroup')
        x |= (bit << i)
    return x, (1 << t)


def crt_pair(a1: int, m1: int, a2: int, m2: int) -> Tuple[int,int]:
    g = gcd(m1, m2)
    if (a2 - a1) % g != 0:
        raise ValueError('Incompatible congruences')
    m1_ = m1 // g
    m2_ = m2 // g
    inv = pow(m1_, -1, m2_)
    x = (a1 + (a2 - a1) // g * inv % m2_ * m1) % (m1 * m2_)
    return x, m1 * m2_


def main():
    g = pow(B, 1 << 16, m)
    # Collect congruences x = s_high mod mod_i
    x = 0
    M = 1
    # We'll also verify by testing ks0 equality when possible
    for p in p_list:
        gp = pow(B % p, 1 << 16, p)
        hp = ks0 % p
        # factor p-1 partially/fully
        fac = factor_power(p - 1)
        # compute order of gp
        ord_gp = compute_order(gp, p, fac)
        # factor ord_gp
        fac_ord = factor_power(ord_gp)
        # build x_p modulo ord_gp using PH
        try:
            x_p = dlog_pohlig_hellman(gp, hp, p, ord_gp, fac_ord)
        except Exception:
            # As fallback, use only 2-adic part
            x2, m2 = dlog_2power_component(gp, hp, p)
            x_p = x2
            ord_gp = m2
            fac_ord = {2: ord_gp.bit_length()-1}
        # combine
        try:
            x, M = crt_pair(x, M, x_p, ord_gp)
        except Exception:
            # skip combining if incompatible
            pass
    # Now x ≡ s_high mod M (where M | ord_g)
    # Brute-force low 16 bits and verify ks0, allowing shifts by multiples of M up to small tries
    found = None
    max_k = 512  # try limited number of shifts
    for k in range(max_k):
        s_high = (x + k * M)
        base_exp = s_high << 16
        # verify keystream 0
        if pow(B, base_exp, m) != ks0:
            continue
        # found correct s_high; now brute-force low 16 bits by checking next block consistency
        for low in range(65536):
            s0 = base_exp | low
            # compute next state and ks1 to compare with observed ks1
            aval = pow(A, s0, m)
            y = aval ^ B
            s1 = pow(y, 4180488827, m)
            ks1_calc = pow(B, s1 - (s1 & 0xffff), m)
            if ks1_calc == ks1:
                found = s0
                break
        if found is not None:
            break
    if found is None:
        print('FAIL')
        return
    # decrypt all blocks
    state = found
    out = b''
    for c in CT:
        ks = pow(B, state - (state & 0xffff), m)
        pt_chunk = c ^ ks
        out += pt_chunk.to_bytes(10, 'big')
        # update state
        state = pow((pow(A, state, m) ^ B), 4180488827, m)
    print(out)

if __name__ == '__main__':
    main()
