#!/usr/bin/env python3
import math
from typing import Dict, List, Tuple
from sympy import factorint, ilcm
from sympy.ntheory.modular import crt

# Problem constants
m = 9792986822963146992114161946549377254001156012300083076259452975070903436656675903033418798369811004678022807932064872669773556983318074157606463933686225452143852071767552582367819932516654167400507310054793760473098421162463267
A = 246920531455433048826966670968977027196902794022573095007307132382393013927558904839982249967656424317118051446771969623490992917094197975459553923550187
B = 3120090466259654766880909097573553950487818021670727992039931232537173262599219376624291488340607228938989670215080876932583555412966984946786628621917436142053528648425399877486481618672307477414787846984446437445450282569184963
e = 4180488827
C = [
  263928838896714332657762314348602240455087661491500131260179929152321790693260683004004767933801216877412896467528419672112455669506824987777448696213888416333755744665868795853306879814179767910033263080874331851322593343273834,
  7500716958005582985508201577146205078774368134456220390802616323312171951781595852608949532619393759348663684985174625019004577610546554994801687569942118260000292201829011312249563036393035204990811392856155820408283216493092108,
  2577794401090299805723177598637436117371525412262771825236813936115237585602114357696686099541164980249580094089526387369627399445447896464668107355247993148990034255262021717192029828447047736912032562575292618672346226630177737,
  9097092753543027532933159793556144814276134227405286080166556624316657274280165256861623248902541076900039285592392074751617153907616670295765377162951858063712964557527212039482031296350052367350738141716598584719951567052177519,
  8174235910244322855637254130843352735528509191186418212056519911128301630950848710182451421471531481098828227735010211554839205099309290314993113489826162548089590990963249899714956197889959999884447438378454452096405595048394416,
  2823506900640363315693941780283568096117331722098156706833610340919194199647098542170689133810904702849664199290565773405646243449194786656181872671323095023235608799444864036190997987871160063941897196360905342203429250068859314,
  4625135637721297092934166648990860031642126233341589454312760229225192256970211899532356300747405146834048765116081788846632527090729839758895834854075755594692611781829177188955301784020596520269704429107749955107365380494152652,
]

P0 = int.from_bytes(b"good luck ", 'big')
P1 = int.from_bytes(b"lmao ictf{", 'big')
K0 = C[0] ^ P0
K1 = C[1] ^ P1

# Prime factors of m (from GP factorint)
PRIMES = [
    10124460123717732577,
    12017858281002457601,
    15013023439701145679,
    17297082179958074003,
    309938271107370186286857659422407283771865851657937731111744300310040346308690205006641245318085354895438500308814135783504803596134094206083383195557983,
]

# Baby-step giant-step discrete log in group of known prime order q

def bsgs_prime_order(p: int, g: int, h: int, q: int) -> int:
    mstep = int(math.isqrt(q)) + 1
    table = {}
    x = 1
    for i in range(mstep):
        # store g^i
        if x not in table:
            table[x] = i
        x = (x * g) % p
    # precompute g^{-m}
    gm = pow(g, mstep, p)
    inv_gm = pow(gm, -1, p)
    y = h % p
    for j in range(mstep+1):
        if y in table:
            i = table[y]
            r = j * mstep + i
            if r % q == 0:
                return 0
            return r % q
        y = (y * inv_gm) % p
    raise ValueError('dlog not found')

# Compute multiplicative order of g modulo prime p

def multiplicative_order_mod_prime(p: int, g: int) -> int:
    if g % p == 0:
        raise ValueError('g divisible by p')
    order = p - 1
    fac = factorint(order)
    for prime, exp in fac.items():
        for _ in range(exp):
            cand = order // prime
            if pow(g, cand, p) == 1:
                order = cand
            else:
                break
    return order

# Pohlig–Hellman for prime field with given order factorization

def discrete_log_ph(p: int, g: int, h: int, order: int, fac: Dict[int, int]) -> Tuple[int, int]:
    # returns (x mod order, order)
    residues: List[int] = []
    moduli: List[int] = []
    for q, e in fac.items():
        # work modulo q^e
        qpow = q ** e
        x_q = 0
        # Precompute inverse of g
        g_inv = pow(g, -1, p)
        for j in range(e):
            exp = order // (q ** (j + 1))
            g_j = pow(g, exp, p)
            # h * g^{-x_q}
            h_adj = (h * pow(g_inv, x_q, p)) % p
            h_j = pow(h_adj, exp, p)
            # Solve y in [0..q-1] s.t. g_j^y == h_j
            y = bsgs_prime_order(p, g_j, h_j, q)
            x_q = x_q + y * (q ** j)
        residues.append(x_q)
        moduli.append(qpow)
    # Combine with CRT modulo 'order'
    x, mod = crt(moduli, residues)
    # crt returns None if inconsistent
    if x is None:
        raise ValueError('CRT failed in PH')
    # Ensure modulo 'order'
    return int(x % order), order

# Compute G and logs modulo each prime factor
G = pow(B, 1 << 16, m)

n0_residues: List[int] = []
mod_orders: List[int] = []

for p in PRIMES:
    Gp = G % p
    K0p = K0 % p
    ord_p = multiplicative_order_mod_prime(p, Gp)
    fac = factorint(ord_p)
    x_p, _ = discrete_log_ph(p, Gp, K0p, ord_p, fac)
    n0_residues.append(x_p)
    mod_orders.append(ord_p)

# Combine across primes (moduli may not be coprime; crt handles as long as consistent)
n0_val, n0_mod = crt(mod_orders, n0_residues)
if n0_val is None:
    raise SystemExit('Failed to CRT combine n0 residues')

n0 = int(n0_val)

# Precompute H = A^(2^16) and T = H^n0
H = pow(A, 1 << 16, m)
T = pow(H, n0, m)

# Precompute A^{2^i} for low 16 bits
A_pows = [A % m]
for _ in range(15):
    A_pows.append(pow(A_pows[-1], 2, m))

def pow_A_low16(exp16: int) -> int:
    r = 1
    e = exp16
    i = 0
    while e:
        if e & 1:
            r = (r * A_pows[i]) % m
        e >>= 1
        i += 1
    return r

# Find r0 via K1 check
S0 = None
for r0 in range(1 << 16):
    val = (T * pow_A_low16(r0)) % m  # A^S0
    base = val ^ B
    S1 = pow(base, e, m)
    if pow(B, S1 - (S1 & 0xFFFF), m) == K1 % m:
        S0 = (n0 << 16) | r0
        break

if S0 is None:
    raise SystemExit('Failed to find r0')

# Decrypt all blocks
state = S0
pt_chunks: List[bytes] = []
for Ci in C:
    K = pow(B, state - (state & 0xFFFF), m)
    P = Ci ^ K
    pt_chunks.append(P.to_bytes(10, 'big'))
    state = pow((pow(A, state, m) ^ B), e, m)

plaintext = b''.join(pt_chunks).rstrip(b'\x00')
print(plaintext.decode('latin-1'))
