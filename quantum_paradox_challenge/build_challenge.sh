#!/bin/bash

# Quantum Paradox Challenge Builder
# This script builds the challenge with maximum obfuscation and protection

set -e

echo "=== Quantum Paradox Challenge Builder ==="
echo "Building insane reversing challenge..."

# Create build directory
mkdir -p build

# Compile with maximum obfuscation
echo "Compiling with maximum obfuscation..."
g++ -std=c++17 -O3 -Wall -Wextra \
    -fno-stack-protector -fno-pie -no-pie \
    -fno-omit-frame-pointer -fno-inline-functions \
    -fno-inline-small-functions -D_FORTIFY_SOURCE=0 \
    -static -s -Wl,--strip-all \
    src/main.cpp -o build/quantum_paradox

# Apply additional obfuscation
echo "Applying additional obfuscation..."

# Add random padding to make analysis harder
dd if=/dev/urandom bs=1024 count=1 >> build/quantum_paradox 2>/dev/null || true

# Strip all symbols
strip --strip-all build/quantum_paradox

# Create a packed version (simulate UPX)
echo "Creating packed version..."
cp build/quantum_paradox build/quantum_paradox.packed

# Generate fake flags and puzzles
echo "Generating fake flags and puzzles..."
python3 src/flag_generator.py > build/fake_flags.txt

# Create a fake memory dump
echo "Creating fake memory dump..."
python3 -c "
import random
import string

# Generate fake memory dump
with open('build/fake_memory.dump', 'w') as f:
    f.write('=== Fake Memory Dump ===\n')
    f.write('This looks like it contains flags, but it\'s all fake!\n\n')
    
    for i in range(100):
        addr = random.randint(0x400000, 0x7fffffff)
        data = ''.join(random.choices('0123456789abcdef', k=32))
        f.write(f'{addr:08x}: {data}\n')
    
    f.write('\n=== End of Fake Memory Dump ===\n')
"

# Create fake assembly dump
echo "Creating fake assembly dump..."
objdump -d build/quantum_paradox > build/assembly_dump.txt 2>/dev/null || true

# Create fake strings dump
echo "Creating fake strings dump..."
strings build/quantum_paradox > build/strings_dump.txt 2>/dev/null || true

# Create a fake hex dump
echo "Creating fake hex dump..."
hexdump -C build/quantum_paradox | head -100 > build/hex_dump.txt

# Create challenge documentation
echo "Creating challenge documentation..."
cat > build/README.md << 'EOF'
# Quantum Paradox Challenge

## Description
This is an extremely difficult reversing challenge that will test your skills in:
- Binary analysis
- Anti-debugging bypass
- Memory analysis
- Code obfuscation
- Assembly understanding

## Files Included
- `quantum_paradox` - The main challenge binary
- `quantum_paradox.packed` - Packed version (same binary)
- `fake_flags.txt` - Contains multiple fake flags (DO NOT SUBMIT THESE!)
- `fake_memory.dump` - Fake memory dump (DO NOT USE THIS!)
- `assembly_dump.txt` - Assembly code dump
- `strings_dump.txt` - Strings found in binary
- `hex_dump.txt` - Hex dump of binary

## Challenge Rules
1. The real flag is hidden deep within the binary
2. Multiple fake flags are present to mislead you
3. Anti-debugging measures are in place
4. The flag format is HTB{...}
5. You must find the REAL flag, not the fake ones

## Hints
- Look for the `getRealFlag()` function
- The real flag is obfuscated in memory
- Anti-debugging must be bypassed
- Memory analysis is crucial
- The flag is never displayed during normal execution

## Difficulty: INSANE
Expected time: 2+ hours

Good luck!
EOF

# Create a fake solution script (to mislead)
echo "Creating fake solution script..."
cat > build/fake_solution.py << 'EOF'
#!/usr/bin/env python3
"""
FAKE SOLUTION - DO NOT USE!
This is designed to mislead you.
"""

import subprocess
import sys

def fake_solve():
    print("This is a FAKE solution!")
    print("The real flag is NOT: HTB{f4k3_fl4g_1_qu4ntum_3rr0r}")
    print("The real flag is NOT: HTB{f4k3_fl4g_2_paradox}")
    print("The real flag is NOT: HTB{qu4ntum_3nt4ngl3m3nt_s0lv3d}")
    print("Keep looking deeper in the binary!")
    print("Hint: Check the getRealFlag() function and memory analysis")

if __name__ == "__main__":
    fake_solve()
EOF

chmod +x build/fake_solution.py

# Create final challenge package
echo "Creating final challenge package..."
cd build
tar -czf ../quantum_paradox_challenge.tar.gz *
cd ..

echo "=== Build Complete ==="
echo "Challenge files created in build/ directory"
echo "Final package: quantum_paradox_challenge.tar.gz"
echo ""
echo "Challenge Summary:"
echo "- Main binary: build/quantum_paradox"
echo "- Multiple fake flags included"
echo "- Anti-debugging protection enabled"
echo "- Maximum obfuscation applied"
echo "- Expected solving time: 2+ hours"
echo ""
echo "The real flag is hidden in the getRealFlag() function"
echo "and must be extracted through memory analysis!"