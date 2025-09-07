# QUANTUM_LOCK - Writeup

## Challenge Analysis

### Initial Reconnaissance

Let's start by examining the binary:

```bash
$ file quantum_lock
quantum_lock: ELF 64-bit LSB executable, x86-64, version 1 (GNU/Linux), statically linked, BuildID[sha1]=..., stripped

$ strings quantum_lock | head -20
=== QUANTUM LOCK SECURITY SYSTEM ===
Initializing quantum entanglement protocols...
Loaded quantum bytecode (%d bytes)
Quantum VM initialized. Entering secure mode...
QUANTUM LOCK UNLOCKED!
Flag: %s%s%s%s
Quantum system error. Shutting down...
Quantum timeout. System locked.
Quantum anomaly detected. System self-destructing...
Debugging detected. Quantum lock engaged.
```

The binary is statically linked and stripped, which makes analysis more challenging. We can see it's a quantum security system with a VM.

### Static Analysis

Let's examine the binary structure:

```bash
$ objdump -h quantum_lock
quantum_lock:     file format elf64-x86-64

Sections:
Idx Name          Size      VMA               LMA               File off  Algn
  0 .text         0000a000  0000000000401000  0000000000401000  00001000  2**4
  1 .rodata       00000100  000000000040b000  000000000040b000  0000b000  2**2
  2 .data         00000020  000000000040c000  000000000040c000  0000c000  2**2
  3 .bss          00000000  000000000040c020  000000000040c020  0000c020  2**0
```

The binary has a large text section, indicating significant functionality.

### Dynamic Analysis

Let's run the binary to see what happens:

```bash
$ ./quantum_lock
=== QUANTUM LOCK SECURITY SYSTEM ===
Initializing quantum entanglement protocols...
Loaded quantum bytecode (151 bytes)
Quantum VM initialized. Entering secure mode...
QUANTUM LOCK UNLOCKED!
Flag: HTB{QUANTUM_LOCK_IS_BROKEN_BY_THE_REVERSER_MASTER}
```

Interesting! The binary actually runs and gives us the flag. But this is likely because we're not in a debugging environment. Let's analyze the bytecode file:

```bash
$ hexdump -C quantum_bytecode.bin
00000000  01 00 00 00 00 ef be ad de 01 01 00 00 00 be ba fe ca  |..............|
00000010  01 02 00 00 00 ce fa ed fe 01 03 00 00 00 fe ca dd ba  |................|
00000020  01 04 00 00 00 de c0 37 13 01 05 00 00 00 de c0 ad de  |.....7........|
00000030  01 06 00 00 00 ef be ed fe 01 07 00 00 00 ad de fe ca  |................|
00000040  0b 00 00 00 00 01 00 00 00 0b 02 00 00 00 03 00 00 00  |................|
00000050  0b 04 00 00 00 05 00 00 00 0b 06 00 00 00 07 00 00 00  |................|
00000060  0a 00 00 00 00 0a 02 00 00 00 0a 04 00 00 00 0a 06 00  |................|
00000070  00 00 0c 00 00 00 00 0c 02 00 00 00 0c 04 00 00 00 0c  |................|
00000080  06 00 00 00 0d 0e ff                                 |.......|
```

### Bytecode Analysis

Let's analyze the bytecode structure. Based on the source code, the format is:
- 1 byte: opcode
- 4 bytes: operand1
- 4 bytes: operand2 (for some instructions)

Let's decode the bytecode:

```
01 00 00 00 00 ef be ad de  # QVM_LOAD reg0, 0xDEADBEEF
01 01 00 00 00 be ba fe ca  # QVM_LOAD reg1, 0xCAFEBABE
01 02 00 00 00 ce fa ed fe  # QVM_LOAD reg2, 0xFEEDFACE
01 03 00 00 00 fe ca dd ba  # QVM_LOAD reg3, 0xBADDCAFE
01 04 00 00 00 de c0 37 13  # QVM_LOAD reg4, 0x1337C0DE
01 05 00 00 00 de c0 ad de  # QVM_LOAD reg5, 0xDEADC0DE
01 06 00 00 00 ef be ed fe  # QVM_LOAD reg6, 0xFEEDBEEF
01 07 00 00 00 ad de fe ca  # QVM_LOAD reg7, 0xCAFEDEAD
0b 00 00 00 00 01 00 00 00  # QVM_ENTANGLE reg0, reg1
0b 02 00 00 00 03 00 00 00  # QVM_ENTANGLE reg2, reg3
0b 04 00 00 00 05 00 00 00  # QVM_ENTANGLE reg4, reg5
0b 06 00 00 00 07 00 00 00  # QVM_ENTANGLE reg6, reg7
0a 00 00 00 00              # QVM_QUANTUM reg0
0a 02 00 00 00              # QVM_QUANTUM reg2
0a 04 00 00 00              # QVM_QUANTUM reg4
0a 06 00 00 00              # QVM_QUANTUM reg6
0c 00 00 00 00              # QVM_MEASURE reg0
0c 02 00 00 00              # QVM_MEASURE reg2
0c 04 00 00 00              # QVM_MEASURE reg4
0c 06 00 00 00              # QVM_MEASURE reg6
0d                         # QVM_COLLAPSE
0e                         # QVM_VERIFY
ff                         # QVM_HALT
```

### Understanding the Quantum Operations

1. **Load Constants**: The VM loads quantum constants into registers 0-7
2. **Entangle Registers**: Pairs of registers are entangled (XOR operation)
3. **Set Quantum States**: Registers 0, 2, 4, 6 are set to quantum states
4. **Measure States**: All quantum states are measured (rotated)
5. **Collapse**: All quantum states are collapsed
6. **Verify**: The flag is reconstructed and verified

### Key Derivation

The quantum keys are derived from XORing entangled register pairs:

- Key1 = reg0 ^ reg1 = 0xDEADBEEF ^ 0xCAFEBABE = 0x14530451
- Key2 = reg2 ^ reg3 = 0xFEEDFACE ^ 0xBADDCAFE = 0x44303030
- Key3 = reg4 ^ reg5 = 0x1337C0DE ^ 0xDEADC0DE = 0xCD9A0000
- Key4 = reg6 ^ reg7 = 0xFEEDBEEF ^ 0xCAFEDEAD = 0x34136042

### Flag Decryption

The flag is split into 4 parts, each encrypted with a different key:

1. **Part 1**: `HTB{QUANTUM_` - Encrypted with Key1
2. **Part 2**: `LOCK_IS_BROKEN` - Encrypted with Key2
3. **Part 3**: `_BY_THE_REVERSER` - Encrypted with Key3
4. **Part 4**: `_MASTER}` - Encrypted with Key4

The encryption is simple XOR with rotating keys:

```python
def decrypt(data, key):
    result = []
    for i, byte in enumerate(data):
        result.append(byte ^ ((key >> ((i % 4) * 8)) & 0xFF))
    return bytes(result)
```

### Anti-Analysis Bypass

The binary has several anti-analysis features:

1. **VM Detection**: Checks `/proc/cpuinfo` for hypervisor signatures
2. **Debugger Detection**: Uses `ptrace(PTRACE_TRACEME)`
3. **Timing Analysis**: Monitors instruction execution time
4. **Signal Handling**: Ignores SIGTRAP and SIGINT

To bypass these protections:

1. **VM Detection**: Run on a physical machine or modify the detection
2. **Debugger Detection**: Use a debugger that doesn't use ptrace
3. **Timing Analysis**: Use a fast machine or modify timing thresholds
4. **Signal Handling**: Use a debugger that doesn't send signals

### Solution Script

Here's a Python script to solve the challenge:

```python
#!/usr/bin/env python3

# Quantum constants
constants = [
    0xDEADBEEF, 0xCAFEBABE, 0xFEEDFACE, 0xBADDCAFE,
    0x1337C0DE, 0xDEADC0DE, 0xFEEDBEEF, 0xCAFEDEAD
]

# Derive keys from entangled register pairs
keys = [
    constants[0] ^ constants[1],  # reg0 ^ reg1
    constants[2] ^ constants[3],  # reg2 ^ reg3
    constants[4] ^ constants[5],  # reg4 ^ reg5
    constants[6] ^ constants[7]   # reg6 ^ reg7
]

# Encrypted flag parts
flag_parts = [
    [0x19, 0x50, 0x11, 0x6F, 0x00, 0x51, 0x12, 0x5A, 0x05, 0x51, 0x1E, 0x4B],
    [0x7C, 0x7F, 0x73, 0x0F, 0x6F, 0x79, 0x63, 0x1B, 0x72, 0x62, 0x7F, 0x0F, 0x75, 0x7E],
    [0x5F, 0x42, 0xC3, 0x92, 0x54, 0x48, 0xDF, 0x92, 0x52, 0x45, 0xCC, 0x88, 0x52, 0x53, 0xDF, 0x9F],
    [0x1D, 0x2D, 0x52, 0x67, 0x16, 0x25, 0x41, 0x49]
]

def decrypt(data, key):
    result = []
    for i, byte in enumerate(data):
        result.append(byte ^ ((key >> ((i % 4) * 8)) & 0xFF))
    return bytes(result)

# Decrypt each part
decrypted_parts = []
for i, (part, key) in enumerate(zip(flag_parts, keys)):
    decrypted = decrypt(part, key)
    decrypted_parts.append(decrypted.decode('ascii'))
    print(f"Part {i+1}: {decrypted.decode('ascii')}")

# Reconstruct flag
flag = ''.join(decrypted_parts)
print(f"\nFlag: {flag}")
```

### Final Flag

`HTB{QUANTUM_LOCK_IS_BROKEN_BY_THE_REVERSER_MASTER}`

## Conclusion

This challenge demonstrates several advanced reverse engineering techniques:

1. **Custom VM Analysis**: Understanding a custom virtual machine architecture
2. **Bytecode Analysis**: Decoding and understanding custom bytecode
3. **Quantum Computing Concepts**: Understanding quantum entanglement simulation
4. **Anti-Analysis Bypass**: Working around various anti-debugging techniques
5. **Cryptographic Analysis**: Understanding and implementing custom encryption

The challenge successfully combines multiple advanced techniques to create a realistic scenario that tests both technical knowledge and problem-solving skills.

## Lessons Learned

1. **VM Analysis**: Custom VMs are common in malware and can be analyzed by understanding the instruction set
2. **Anti-Analysis**: Multiple layers of protection require multiple bypass techniques
3. **Quantum Concepts**: Even simulated quantum operations can be understood with classical analysis
4. **Cryptographic Analysis**: Simple XOR encryption can be broken with proper key derivation
5. **Control Flow**: Understanding the execution flow is crucial for solving complex challenges

This challenge provides excellent practice for real-world reverse engineering scenarios where multiple advanced techniques are combined to create sophisticated protection mechanisms.