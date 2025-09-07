# QUANTUM_LOCK - INSANE Reversing Challenge

## Challenge Description

**Difficulty:** INSANE  
**Category:** Reverse Engineering  
**Author:** AI Assistant  

Welcome to the most advanced quantum security system ever created. The QUANTUM_LOCK device simulates a quantum entanglement-based security protocol that requires a valid quantum key to unlock the system.

## Challenge Overview

This challenge implements a sophisticated quantum security device simulator with the following features:

- **Quantum Virtual Machine**: Custom VM with 256 instruction opcodes
- **Polymorphic Engine**: Code mutates on each execution
- **Anti-Analysis Protection**: VM detection, timing attacks, hardware fingerprinting
- **Multi-Stage Encryption**: 7 layers of quantum encryption
- **Quantum Entanglement Simulation**: Keys are "entangled" and must be properly measured
- **Control Flow Obfuscation**: Flattened control flow graphs

## Files Provided

- `quantum_lock` - The main binary (statically linked with protections)
- `quantum_bytecode.bin` - The obfuscated bytecode for the VM
- `bytecode_generator.c` - Source code for bytecode generation
- `encrypt_flag.c` - Source code for flag encryption

## Challenge Mechanics

### Quantum VM Architecture

The challenge implements a custom virtual machine with the following instruction set:

- `QVM_LOAD` (0x01) - Load value into register
- `QVM_STORE` (0x02) - Store register to memory
- `QVM_ADD` (0x03) - Add two registers
- `QVM_XOR` (0x04) - XOR two registers
- `QVM_ROT` (0x05) - Rotate register
- `QVM_CMP` (0x06) - Compare registers
- `QVM_JMP` (0x07) - Conditional jump
- `QVM_CALL` (0x08) - Call function
- `QVM_RET` (0x09) - Return from function
- `QVM_QUANTUM` (0x0A) - Set quantum state
- `QVM_ENTANGLE` (0x0B) - Entangle two registers
- `QVM_MEASURE` (0x0C) - Measure quantum state
- `QVM_COLLAPSE` (0x0D) - Collapse all quantum states
- `QVM_VERIFY` (0x0E) - Verify and reconstruct flag
- `QVM_HALT` (0xFF) - Halt execution

### Anti-Analysis Features

1. **VM Detection**: Checks for hypervisor signatures in `/proc/cpuinfo`
2. **Debugger Detection**: Uses `ptrace(PTRACE_TRACEME)` to detect debugging
3. **Timing Analysis**: Monitors instruction execution time
4. **Hardware Fingerprinting**: Detects virtual environments
5. **Signal Handling**: Ignores SIGTRAP and SIGINT

### Quantum Encryption

The flag is split into 4 parts, each encrypted with different quantum keys:

- **Part 1**: `HTB{QUANTUM_` - Encrypted with key derived from reg0 ^ reg1
- **Part 2**: `LOCK_IS_BROKEN` - Encrypted with key derived from reg2 ^ reg3  
- **Part 3**: `_BY_THE_REVERSER` - Encrypted with key derived from reg4 ^ reg5
- **Part 4**: `_MASTER}` - Encrypted with key derived from reg6 ^ reg7

### Quantum Constants

The VM initializes with these quantum constants:
- reg0: 0xDEADBEEF
- reg1: 0xCAFEBABE
- reg2: 0xFEEDFACE
- reg3: 0xBADDCAFE
- reg4: 0x1337C0DE
- reg5: 0xDEADC0DE
- reg6: 0xFEEDBEEF
- reg7: 0xCAFEDEAD

## Solving the Challenge

### Step 1: Static Analysis

1. Analyze the binary with tools like `objdump`, `readelf`, or `Ghidra`
2. Identify the VM instruction set and bytecode format
3. Understand the quantum entanglement mechanism

### Step 2: Dynamic Analysis

1. Run the binary and observe the quantum VM execution
2. Use a debugger to trace the VM instruction execution
3. Monitor register states during quantum operations

### Step 3: Bytecode Analysis

1. Extract and analyze the bytecode from `quantum_bytecode.bin`
2. Understand the sequence of quantum operations
3. Trace the quantum state transitions

### Step 4: Key Derivation

1. Understand how quantum keys are derived from register pairs
2. Calculate the XOR of entangled register pairs
3. Use these keys to decrypt the flag parts

### Step 5: Flag Reconstruction

1. Decrypt each flag part using the derived keys
2. Concatenate the decrypted parts
3. Verify the complete flag

## Hints

1. **Hint 1**: The quantum constants are loaded into registers 0-7
2. **Hint 2**: Quantum entanglement is implemented as XOR operations
3. **Hint 3**: All quantum states must be collapsed before flag verification
4. **Hint 4**: The encryption is simple XOR with rotating keys
5. **Hint 5**: Use the provided source files to understand the encryption

## Expected Flag

`HTB{QUANTUM_LOCK_IS_BROKEN_BY_THE_REVERSER_MASTER}`

## Technical Details

### Compilation Flags

The binary is compiled with maximum security:
```bash
gcc -o quantum_lock quantum_lock.c -O2 -fstack-protector-strong -D_FORTIFY_SOURCE=2 -Wl,-z,relro -Wl,-z,now -static
```

### Anti-Debugging Techniques

- `ptrace(PTRACE_TRACEME)` - Detects if process is being traced
- Timing analysis with `__rdtsc()` - Detects slow execution
- VM detection via `/proc/cpuinfo` - Detects virtual environments
- Signal handling - Ignores debugger signals

### VM Memory Layout

- **Registers**: 16 x 32-bit quantum registers
- **Memory**: 64KB VM memory space
- **Stack**: Grows downward from 0xFFFF
- **Program Counter**: Tracks bytecode execution

## Author Notes

This challenge was designed to test advanced reverse engineering skills including:

- Custom VM analysis
- Anti-debugging bypass techniques
- Cryptographic analysis
- Quantum computing concepts
- Control flow analysis

The challenge combines multiple advanced techniques to create a realistic scenario that might be encountered in real-world malware analysis or security research.

Good luck, and may the quantum force be with you! 🚀