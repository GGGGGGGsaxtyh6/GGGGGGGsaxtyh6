#!/usr/bin/env python3
import math
from sympy import factorint, discrete_log

# Constants from randumber.py
m = 9792986822963146992114161946549377254001156012300083076259452975070903436656675903033418798369811004678022807932064872669773556983318074157606463933686225452143852071767552582367819932516654167400507310054793760473098421162463267
A = 246920531455433048826966670968977027196902794022573095007307132382393013927558904839982249967656424317118051446771969623490992917094197975459553923550187
B = 3120090466259654766880909097573553950487818021670727992039931232537173262599219376624291488340607228938989670215080876932583555412966984946786628621917436142053528648425399877486481618672307477414787846984446437445450282569184963
e = 4180488827

# Ciphertext list from comment
C = [
  263928838896714332657762314348602240455087661491500131260179929152321790693260683004004767933801216877412896467528419672112455669506824987777448696213888416333755744665868795853306879814179767910033263080874331851322593343273834,
  7500716958005582985508201577146205078774368134456220390802616323312171951781595852608949532619393759348663684985174625019004577610546554994801687569942118260000292201829011312249563036393035204990811392856155820408283216493092108,
  2577794401090299805723177598637436117371525412262771825236813936115237585602114357696686099541164980249580094089526387369627399445447896464668107355247993148990034255262021717192029828447047736912032562575292618672346226630177737,
  9097092753543027532933159793556144814276134227405286080166556624316657274280165256861623248902541076900039285592392074751617153907616670295765377162951858063712964557527212039482031296350052367350738141716598584719951567052177519,
  8174235910244322855637254130843352735528509191186418212056519911128301630950848710182451421471531481098828227735010211554839205099309290314993113489826162548089590990963249899714956197889959999884447438378454452096405595048394416,
  2823506900640363315693941780283568096117331722098156706833610340919194199647098542170689133810904702849664199290565773405646243449194786656181872671323095023235608799444864036190997987871160063941897196360905342203429250068859314,
  4625135637721297092934166648990860031642126233341589454312760229225192256970211899532356300747405146834048765116081788846632527090729839758895834854075755594692611781829177188955301784020596520269704429107749955107365380494152652,
]

# Helpers

def bytes_to_long_be(b: bytes) -> int:
    return int.from_bytes(b, 'big')

def long_to_bytes_be(n: int, length: int) -> bytes:
    return n.to_bytes(length, 'big')

# Known plaintext prefix split into 10-byte chunks
known_chunks = [
    b"good luck ",
    b"lmao ictf{",
]

# Derive first two keystream blocks (output_i)
O = []
for i, kc in enumerate(known_chunks):
    chunk_int = bytes_to_long_be(kc)
    Oi = C[i] ^ chunk_int
    O.append(Oi)

# Compute generator G = B^(2^16)
G = pow(B, 1 << 16, m)

# Utility: compute order of an element given modulus is prime-ish
# Start from N' = (m-1)/g where g = gcd(m-1, 2^16); then divide by prime factors until G^ord == 1
N = m - 1
g = math.gcd(N, 1 << 16)
ord_candidate = N // g
# Factor ord_candidate
factors = factorint(ord_candidate)
# Reduce to exact order by dividing factors while maintaining G^order == 1
orderG = ord_candidate
for p, exp in factors.items():
    for _ in range(exp):
        q = orderG // p
        if pow(G, q, m) == 1:
            orderG = q
        else:
            break

# Discrete logs to get n0, n1 such that G^n = O
n0 = discrete_log(m, O[0] % m, G % m, order=orderG)
n1 = discrete_log(m, O[1] % m, G % m, order=orderG)

# Recover r0 by brute-force over 16-bit low part
# Precompute H = A^(2^16) and T = H^n0
H = pow(A, 1 << 16, m)
T = pow(H, n0, m)

# Precompute A^{2^i} for i in [0..15] to quickly compute A^r for any r<2^16
A_pows = [A % m]
for i in range(1, 16):
    A_pows.append(pow(A_pows[-1], 2, m))


def pow_A_small(exp16: int) -> int:
    # exp16 in [0, 65535]
    result = 1
    i = 0
    e = exp16
    while e:
        if e & 1:
            result = (result * A_pows[i]) % m
        e >>= 1
        i += 1
    return result

r0_found = None
S0_found = None
S1_found = None

for r0 in range(0, 1 << 16):
    val = (T * pow_A_small(r0)) % m  # A^S0
    base = val ^ B  # bitwise XOR before exponentiation
    S1 = pow(base, e, m)
    if (S1 >> 16) == n1:
        r0_found = r0
        S0_found = (n0 << 16) | r0
        S1_found = S1
        break

if r0_found is None:
    raise SystemExit("Failed to recover r0")

# With full S known, generate keystream and decrypt all blocks

def keystream_from_state(S: int) -> int:
    return pow(B, S - (S & 0xFFFF), m)

def next_state(S: int) -> int:
    return pow((pow(A, S, m) ^ B), e, m)

S = S0_found
plaintext_chunks = []
for i in range(len(C)):
    K = keystream_from_state(S)
    P_int = C[i] ^ K
    # determine chunk length: 10 bytes for all except possibly last; but we don't know last length yet
    # We'll try 10 bytes and strip trailing nulls later
    P_bytes = long_to_bytes_be(P_int, 10)
    plaintext_chunks.append(P_bytes)
    S = next_state(S)

plaintext = b"".join(plaintext_chunks)
# Strip possible trailing null bytes
plaintext = plaintext.rstrip(b"\x00")
print(plaintext.decode(errors='ignore'))
