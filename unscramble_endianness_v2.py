#!/usr/bin/env python3
import itertools
import re
import io
import zipfile
from pathlib import Path

INPUT = Path('/workspace/challengefile')
OUTDIR = Path('/workspace/out_all')
OUTDIR.mkdir(exist_ok=True)

data = INPUT.read_bytes()
L = len(data)

flag_re = re.compile(br"picoCTF\{.*?\}")

magics = {
    b"\x89PNG\r\n\x1a\n": "png",
    b"\xff\xd8\xff": "jpg",
    b"GIF8": "gif",
    b"PK\x03\x04": "zip",
    b"%PDF-": "pdf",
    b"\x7fELF": "elf",
    b"RIFF": "riff",
}

candidates = []

# Scoring heuristic

def score(buf: bytes):
    s = 0
    for magic, _label in magics.items():
        if buf.startswith(magic):
            s += 100
    if flag_re.search(buf):
        s += 500
    # ASCII ratio heuristic (first 1KB)
    ascii_bytes = sum(32 <= b <= 126 or b in (9, 10, 13) for b in buf[:1024])
    s += int(100 * ascii_bytes / max(1, min(1024, len(buf))))
    return s

# Strategy 1: permutations within 4-byte words
prefix_len = L - (L % 4)
prefix = data[:prefix_len]
suffix = data[prefix_len:]
for perm in itertools.permutations(range(4)):
    out = bytearray()
    for i in range(0, prefix_len, 4):
        c = prefix[i:i+4]
        out.extend((c[perm[0]], c[perm[1]], c[perm[2]], c[perm[3]]))
    out.extend(suffix)
    candidates.append((score(out), f"wordperm_{perm}", bytes(out)))

# Strategy 2: reverse each 4-byte word
out = bytearray()
for i in range(0, prefix_len, 4):
    out.extend(prefix[i:i+4][::-1])
out.extend(suffix)
candidates.append((score(out), "word_reverse", bytes(out)))

# Strategy 3: deinterleave by byte planes of 4 (quarters -> interleave bytes)
if L >= 8:
    nwords = L // 4
    planes = [data[i*nwords:(i+1)*nwords] for i in range(4)]
    for perm in itertools.permutations(range(4)):
        out = bytearray()
        for k in range(nwords):
            out.extend((planes[perm[0]][k], planes[perm[1]][k], planes[perm[2]][k], planes[perm[3]][k]))
        out.extend(data[4*nwords:])
        candidates.append((score(out), f"deinterleave4_{perm}", bytes(out)))

# Strategy 4: deinterleave by 2-byte halves (two halves -> interleave 2-byte units)
if L >= 4:
    half = L // 2
    halves = [data[0:half], data[half:2*half]]
    for perm in itertools.permutations(range(2)):
        out = bytearray()
        # Interleave 2-byte units
        for k in range(0, min(len(halves[0]), len(halves[1])), 2):
            out.extend(halves[perm[0]][k:k+2])
            out.extend(halves[perm[1]][k:k+2])
        out.extend(data[2*half:])
        candidates.append((score(out), f"deinterleave2_{perm}", bytes(out)))

# Strategy 5: reverse full file
candidates.append((score(data[::-1]), "full_reverse", data[::-1]))

# Sort by score (best first)
ranked = sorted(candidates, key=lambda x: -x[0])

found_flags = set()

# Helper to scan buffers and optionally try to extract from ZIP if detected

def scan_and_maybe_zip(name: str, buf: bytes):
    m = flag_re.search(buf)
    if m:
        found_flags.add(m.group(0))
        return True
    # Try ZIP inspection
    if buf.startswith(b"PK\x03\x04"):
        with zipfile.ZipFile(io.BytesIO(buf)) as zf:
            for zi in zf.infolist():
                try:
                    content = zf.read(zi)
                except Exception:
                    continue
                m2 = flag_re.search(content)
                if m2:
                    found_flags.add(m2.group(0))
                    return True
    return False

# Write top candidates and scan all
TOP_WRITE = 50
for idx, (sc, name, buf) in enumerate(ranked, 1):
    if idx <= TOP_WRITE:
        (OUTDIR / f"{idx:02d}_{name}.bin").write_bytes(buf)
    scan_and_maybe_zip(name, buf)

for f in sorted(found_flags):
    print(f.decode('ascii', errors='ignore'))

print(f"Checked {len(ranked)} candidates; wrote {min(TOP_WRITE, len(ranked))} to {OUTDIR}")
