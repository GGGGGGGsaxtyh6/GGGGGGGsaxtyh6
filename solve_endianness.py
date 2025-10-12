#!/usr/bin/env python3
import itertools
import re
from pathlib import Path

INPUT = Path('/workspace/challengefile')

data = INPUT.read_bytes()

# Process in 4-byte words; leave any trailing bytes unchanged
prefix_len = len(data) - (len(data) % 4)
prefix = data[:prefix_len]
suffix = data[prefix_len:]

flag_re = re.compile(br"picoCTF\{.*?\}")

found = set()

for perm in itertools.permutations(range(4)):
    out = bytearray()
    for i in range(0, len(prefix), 4):
        chunk = prefix[i:i+4]
        out.extend((chunk[perm[0]], chunk[perm[1]], chunk[perm[2]], chunk[perm[3]]))
    out.extend(suffix)
    m = flag_re.search(out)
    if m:
        found.add(m.group(0))
        # Stop early once we have at least one plausible flag
        # But still collect a couple in case there are multiple; limit to 3
        if len(found) >= 3:
            break

# Try some common additional transforms if not found:
if not found:
    # Reverse each 4-byte word
    out = bytearray()
    for i in range(0, len(prefix), 4):
        chunk = prefix[i:i+4]
        out.extend(reversed(chunk))
    out.extend(suffix)
    m = flag_re.search(out)
    if m:
        found.add(m.group(0))

if not found:
    # Reverse the entire file
    out = data[::-1]
    m = flag_re.search(out)
    if m:
        found.add(m.group(0))

# Print one flag per line if found; otherwise nothing
for f in sorted(found):
    try:
        print(f.decode('ascii', errors='ignore'))
    except Exception:
        print(bytes(f))
