#!/bin/bash

# Advanced Quantum Paradox Challenge Builder
# This script creates an extremely difficult reversing challenge

set -e

echo "=== Advanced Quantum Paradox Challenge Builder ==="
echo "Building INSANE reversing challenge with maximum obfuscation..."

# Create build directory
mkdir -p build

# Compile with maximum obfuscation and protection
echo "Compiling with maximum obfuscation and protection..."
g++ -std=c++17 -O3 -Wall -Wextra \
    -fno-stack-protector -fno-pie -no-pie \
    -fno-omit-frame-pointer -fno-inline-functions \
    -fno-inline-small-functions -D_FORTIFY_SOURCE=0 \
    -static -s -Wl,--strip-all \
    -DINSANE_MODE=1 \
    -DQUANTUM_PARADOX=1 \
    -DANTI_DEBUG=1 \
    src/main.cpp -o build/quantum_paradox

# Apply additional obfuscation layers
echo "Applying additional obfuscation layers..."

# Add random padding to make analysis harder
dd if=/dev/urandom bs=2048 count=1 >> build/quantum_paradox 2>/dev/null || true

# Strip all symbols and debug info
strip --strip-all build/quantum_paradox

# Create multiple versions with different obfuscation
echo "Creating multiple obfuscated versions..."

# Version 1: Standard obfuscation
cp build/quantum_paradox build/quantum_paradox_v1

# Version 2: Additional padding
cp build/quantum_paradox build/quantum_paradox_v2
dd if=/dev/urandom bs=1024 count=2 >> build/quantum_paradox_v2 2>/dev/null || true

# Version 3: Different padding
cp build/quantum_paradox build/quantum_paradox_v3
dd if=/dev/urandom bs=512 count=4 >> build/quantum_paradox_v3 2>/dev/null || true

# Generate all fake data and puzzles
echo "Generating fake flags and puzzles..."
python3 src/flag_generator.py > build/fake_flags.txt
python3 src/advanced_obfuscator.py

# Move generated files to build directory
mv *.json build/ 2>/dev/null || true

# Create fake memory dumps
echo "Creating fake memory dumps..."
for i in {1..5}; do
    python3 -c "
import random
import string

with open('build/fake_memory_$i.dump', 'w') as f:
    f.write('=== Fake Memory Dump $i ===\n')
    f.write('This looks like it contains flags, but it\'s all fake!\n\n')
    
    for j in range(200):
        addr = random.randint(0x400000, 0x7fffffff)
        data = ''.join(random.choices('0123456789abcdef', k=32))
        f.write(f'{addr:08x}: {data}\n')
    
    f.write('\n=== End of Fake Memory Dump $i ===\n')
"
done

# Create fake assembly dumps
echo "Creating fake assembly dumps..."
for i in {1..3}; do
    objdump -d build/quantum_paradox > build/assembly_dump_$i.txt 2>/dev/null || true
done

# Create fake strings dumps
echo "Creating fake strings dumps..."
strings build/quantum_paradox > build/strings_dump.txt 2>/dev/null || true

# Create fake hex dumps
echo "Creating fake hex dumps..."
for i in {1..3}; do
    hexdump -C build/quantum_paradox | head -200 > build/hex_dump_$i.txt
done

# Create fake disassembly
echo "Creating fake disassembly..."
objdump -d build/quantum_paradox > build/disassembly.txt 2>/dev/null || true

# Create fake section headers
echo "Creating fake section headers..."
objdump -h build/quantum_paradox > build/sections.txt 2>/dev/null || true

# Create fake symbol table
echo "Creating fake symbol table..."
nm build/quantum_paradox > build/symbols.txt 2>/dev/null || true

# Create fake ELF header
echo "Creating fake ELF header..."
readelf -h build/quantum_paradox > build/elf_header.txt 2>/dev/null || true

# Create fake program headers
echo "Creating fake program headers..."
readelf -l build/quantum_paradox > build/program_headers.txt 2>/dev/null || true

# Create fake section headers
echo "Creating fake section headers..."
readelf -S build/quantum_paradox > build/section_headers.txt 2>/dev/null || true

# Create challenge documentation
echo "Creating comprehensive challenge documentation..."
cat > build/README.md << 'EOF'
# Quantum Paradox Challenge - INSANE DIFFICULTY

## Description
This is an extremely difficult reversing challenge that will test your skills in:
- Binary analysis and reverse engineering
- Anti-debugging bypass techniques
- Memory analysis and forensics
- Code obfuscation and deobfuscation
- Assembly language understanding
- Quantum computing concepts (fake)

## Challenge Files
- `quantum_paradox` - Main challenge binary
- `quantum_paradox_v1` - Version 1 (standard obfuscation)
- `quantum_paradox_v2` - Version 2 (additional padding)
- `quantum_paradox_v3` - Version 3 (different padding)
- `fake_flags.txt` - Contains multiple fake flags (DO NOT SUBMIT THESE!)
- `fake_memory_*.dump` - Fake memory dumps (DO NOT USE THESE!)
- `assembly_dump_*.txt` - Assembly code dumps
- `strings_dump.txt` - Strings found in binary
- `hex_dump_*.txt` - Hex dumps of binary
- `disassembly.txt` - Complete disassembly
- `sections.txt` - Section headers
- `symbols.txt` - Symbol table
- `elf_header.txt` - ELF header information
- `program_headers.txt` - Program headers
- `section_headers.txt` - Section headers
- `*.json` - Various obfuscated data files

## Challenge Rules
1. The real flag is hidden deep within the binary
2. Multiple fake flags are present to mislead you
3. Anti-debugging measures are in place and must be bypassed
4. The flag format is HTB{...}
5. You must find the REAL flag, not the fake ones
6. Memory analysis is crucial for solving this challenge
7. The flag is never displayed during normal execution

## Hints
- Look for the `getRealFlag()` function in the source code
- The real flag is obfuscated in memory using XOR
- Anti-debugging must be bypassed to analyze the binary
- Memory analysis and forensics are essential
- The flag is hidden in a function that's never called
- Check for obfuscated strings and data structures
- Look for XOR operations and deobfuscation routines

## Difficulty: INSANE
Expected solving time: 2+ hours for experienced reversers

## Tools Recommended
- IDA Pro or Ghidra for static analysis
- GDB with anti-debugging bypass
- Hex editor for binary analysis
- Memory analysis tools
- String analysis tools

## Warning
This challenge contains multiple fake flags and misleading information.
Do not submit any of the fake flags - only the real one will be accepted.

Good luck!
EOF

# Create fake solution scripts
echo "Creating fake solution scripts..."
cat > build/fake_solution_1.py << 'EOF'
#!/usr/bin/env python3
"""
FAKE SOLUTION 1 - DO NOT USE!
This is designed to mislead you.
"""

def fake_solve_1():
    print("This is FAKE SOLUTION 1!")
    print("The real flag is NOT: HTB{f4k3_fl4g_1_qu4ntum_3rr0r}")
    print("The real flag is NOT: HTB{f4k3_fl4g_2_paradox}")
    print("The real flag is NOT: HTB{qu4ntum_3nt4ngl3m3nt_s0lv3d}")
    print("Keep looking deeper in the binary!")
    print("Hint: Check the getRealFlag() function and memory analysis")

if __name__ == "__main__":
    fake_solve_1()
EOF

cat > build/fake_solution_2.py << 'EOF'
#!/usr/bin/env python3
"""
FAKE SOLUTION 2 - DO NOT USE!
This is designed to mislead you.
"""

def fake_solve_2():
    print("This is FAKE SOLUTION 2!")
    print("The real flag is NOT: HTB{asm_puzzle_1_solved}")
    print("The real flag is NOT: HTB{crypto_analysis_complete}")
    print("The real flag is NOT: HTB{quantum_algorithm_solved_paradox}")
    print("Keep looking deeper in the binary!")
    print("Hint: The real flag is obfuscated with XOR key 0xAA")

if __name__ == "__main__":
    fake_solve_2()
EOF

chmod +x build/fake_solution_*.py

# Create final challenge package
echo "Creating final challenge package..."
cd build
tar -czf ../quantum_paradox_challenge_insane.tar.gz *
cd ..

echo "=== Advanced Build Complete ==="
echo "Challenge files created in build/ directory"
echo "Final package: quantum_paradox_challenge_insane.tar.gz"
echo ""
echo "Challenge Summary:"
echo "- Main binary: build/quantum_paradox"
echo "- Multiple versions with different obfuscation"
echo "- Extensive fake flags and misleading data"
echo "- Anti-debugging protection enabled"
echo "- Maximum obfuscation applied"
echo "- Expected solving time: 2+ hours"
echo ""
echo "The real flag is hidden in the getRealFlag() function"
echo "and must be extracted through memory analysis!"
echo "Flag format: HTB{qu4ntum_paradox_solved_2024_real_flag}"
echo ""
echo "Remember: All other flags are FAKE!"