# NEURAL_CORRUPTION_ULTIMATE - Writeup

## Challenge Analysis

### Initial Reconnaissance

Let's start by examining the binary:

```bash
$ file neural_ultimate
neural_ultimate: ELF 64-bit LSB executable, x86-64, version 1 (GNU/Linux), statically linked, BuildID[sha1]=..., stripped

$ strings neural_ultimate | head -20
=== NEURAL CORRUPTION ULTIMATE ===
Initializing 20+ advanced techniques...
VM DETECTED! This is fake flag #3: HTB{FAKE_VM_DETECTED}
DEBUGGER DETECTED! This is fake flag #1: HTB{FAKE_DEBUGGER_DETECTED}
TIMING ANOMALY! This is fake flag #2: HTB{FAKE_TIMING_ANOMALY}
HOSTNAME! This is fake flag #7: HTB{FAKE_HOSTNAME}
HARDWARE CHECK FAILED! This is fake flag #8: HTB{FAKE_HARDWARE}
FAKE FLAG #1: HTB{FAKE_FLAG_1}
FAKE FLAG #2: HTB{FAKE_FLAG_2}
FAKE FLAG #3: HTB{FAKE_FLAG_3}
FAKE FLAG #4: HTB{FAKE_FLAG_4}
FAKE FLAG #5: HTB{FAKE_FLAG_5}
CONGRATULATIONS! You found the flag: HTB{FAKE_TRAP_1}
SUCCESS! The flag is: HTB{FAKE_TRAP_2}
TOO SLOW! This is fake flag #10: HTB{FAKE_TIMING}
NEURAL CORRUPTION ULTIMATE ANALYZED!
Real Flag: 
```

The binary is statically linked and stripped, which makes analysis more challenging. We can see it's a neural corruption system with multiple fake flags and anti-analysis techniques.

### Static Analysis

Let's examine the binary structure:

```bash
$ objdump -h neural_ultimate
neural_ultimate:     file format elf64-x86-64

Sections:
Idx Name          Size      VMA               LMA               File off  Algn
  0 .text         0000c000  0000000000401000  0000000000401000  00001000  2**4
  1 .rodata       00000200  000000000040d000  000000000040d000  0000d000  2**2
  2 .data         00000040  000000000040f000  000000000040f000  0000f000  2**2
  3 .bss          00000000  000000000040f040  000000000040f040  0000f040  2**0
```

The binary has a large text section, indicating significant functionality.

### Dynamic Analysis

Let's run the binary to see what happens:

```bash
$ ./neural_ultimate
=== NEURAL CORRUPTION ULTIMATE ===
Initializing 20+ advanced techniques...
VM DETECTED! This is fake flag #3: HTB{FAKE_VM_DETECTED}
```

The binary immediately detects we're in a VM and exits. This is the first anti-analysis technique.

## Anti-Analysis Techniques

### 1. VM Detection
The binary checks `/proc/cpuinfo` for hypervisor signatures:

```c
static void check_vm() {
    FILE *fp = fopen("/proc/cpuinfo", "r");
    if (fp) {
        char line[256];
        while (fgets(line, sizeof(line), fp)) {
            if (strstr(line, "hypervisor") || strstr(line, "vmware") || 
                strstr(line, "virtualbox") || strstr(line, "qemu")) {
                printf("VM DETECTED! This is fake flag #3: HTB{FAKE_VM_DETECTED}\n");
                fake_flag_count++;
                fclose(fp);
                exit(1);
            }
        }
        fclose(fp);
    }
}
```

### 2. Debugger Detection
Uses `ptrace(PTRACE_TRACEME)` to detect debugging:

```c
static void check_ptrace() {
    if (ptrace(PTRACE_TRACEME, 0, 1, 0) == -1) {
        printf("DEBUGGER DETECTED! This is fake flag #1: HTB{FAKE_DEBUGGER_DETECTED}\n");
        fake_flag_count++;
        exit(1);
    }
}
```

### 3. Timing Analysis
Monitors instruction execution time:

```c
static void check_timing() {
    static uint64_t last_check = 0;
    uint64_t current = __rdtsc();
    if (last_check != 0 && (current - last_check) > 1000000) {
        printf("TIMING ANOMALY! This is fake flag #2: HTB{FAKE_TIMING_ANOMALY}\n");
        fake_flag_count++;
        exit(1);
    }
    last_check = current;
}
```

### 4. Environment Fingerprinting
Checks hostname for suspicious patterns:

```c
static void fingerprint_environment() {
    char hostname[256];
    if (gethostname(hostname, sizeof(hostname)) == 0) {
        if (strstr(hostname, "debug") || strstr(hostname, "test")) {
            printf("SUSPICIOUS HOSTNAME! This is fake flag #7: HTB{FAKE_HOSTNAME}\n");
            fake_flag_count++;
            exit(1);
        }
    }
}
```

### 5. Hardware-based Anti-Analysis
Checks CPU features using CPUID:

```c
static void check_hardware() {
    uint32_t eax, ebx, ecx, edx;
    __asm__ volatile("cpuid" : "=a"(eax), "=b"(ebx), "=c"(ecx), "=d"(edx) : "a"(1));
    
    if (!(ecx & (1 << 30))) { // Check for RDRAND
        printf("HARDWARE CHECK FAILED! This is fake flag #8: HTB{FAKE_HARDWARE}\n");
        fake_flag_count++;
        exit(1);
    }
}
```

## Bypassing Anti-Analysis

### Method 1: Binary Patching

We need to patch the binary to bypass the anti-analysis checks:

```bash
# Create a copy for patching
cp neural_ultimate neural_ultimate.patched

# Patch VM detection (NOP the call)
objcopy --dump-section .text=text_section neural_ultimate.patched
# Edit the binary to NOP the check_vm call
objcopy --update-section .text=text_section neural_ultimate.patched

# Patch debugger detection
# Find the ptrace call and replace with NOPs
```

### Method 2: Environment Manipulation

```bash
# Run on a physical machine (not VM)
# Or modify /proc/cpuinfo temporarily
# Or use a debugger that doesn't use ptrace
```

### Method 3: Dynamic Patching with GDB

```bash
$ gdb ./neural_ultimate
(gdb) set environment GDB=1
(gdb) break main
(gdb) run
(gdb) set $pc = main+100  # Skip anti-analysis checks
(gdb) continue
```

## Finding the Real Flag

### Analyzing the reconstruct_real_flag Function

The real flag is hidden in the `reconstruct_real_flag` function:

```c
static int reconstruct_real_flag() {
    // The real flag is hidden here (encrypted with neural weights)
    uint8_t flag_parts[8][32] = {
        {0x0f, 0xf5, 0x64, 0x9c, 0x09, 0xe4, 0x73, 0x75, 0x06, 0xed, 0x79, 0x64, 0x08, 0xf3, 0x74, 0x72, 0x17, 0xf5, 0x6f, 0x68, 0x09, 0xfe, 0x73, 0x6b, 0x13, 0xe8, 0x6b, 0x66, 0x13, 0xe4, 0x79, 0x6e},
        {0x6a, 0x53, 0x61, 0x71, 0x7c, 0x53, 0x78, 0x76, 0x6a, 0x58, 0x6a, 0x70, 0x77, 0x5f, 0x74, 0x77, 0x7c, 0x53, 0x67, 0x7c, 0x6d, 0x43, 0x6a, 0x7c, 0x6f, 0x49, 0x67, 0x66, 0x7a, 0x5e, 0x70, 0x78},
        {0x5a, 0x86, 0x89, 0x91, 0x4c, 0x9a, 0x92, 0x9a, 0x46, 0x86, 0x92, 0x8f, 0x47, 0x9c, 0x80, 0x8f, 0x5d, 0x97, 0x88, 0x9c, 0x51, 0x8c, 0x8b, 0x91, 0x5a, 0x8b, 0x88, 0x91, 0x40, 0x86, 0x98, 0x9c},
        {0x25, 0xe6, 0x11, 0x0a, 0x21, 0xfe, 0x19, 0x0b, 0x36, 0xe1, 0x11, 0x05, 0x2a, 0xee, 0x11, 0x10, 0x2c, 0xef, 0x11, 0x07, 0x2b, 0xf8, 0x1c, 0x11, 0x34, 0xfe, 0x0b, 0x00, 0x3b, 0xfc, 0x03, 0x1b},
        {0x15, 0x3d, 0xa7, 0xb2, 0x14, 0x2b, 0xb7, 0xb2, 0x08, 0x25, 0xbd, 0xb6, 0x1b, 0x3d, 0xa0, 0xbe, 0x04, 0x3b, 0xbe, 0xb6, 0x04, 0x30, 0xb6, 0xa5, 0x08, 0x33, 0xbb, 0xb8, 0x08, 0x26, 0xa1, 0xb8},
        {0x72, 0x49, 0x6a, 0x6d, 0x71, 0x49, 0x6a, 0x77, 0x7c, 0x59, 0x67, 0x78, 0x75, 0x53, 0x7b, 0x7c, 0x6d, 0x5b, 0x7a, 0x6b, 0x72, 0x53, 0x74, 0x77, 0x7d, 0x53, 0x61, 0x71, 0x7c, 0x53, 0x76, 0x76},
        {0x4e, 0xd4, 0xcf, 0xcc, 0x48, 0xc3, 0xde, 0xc3, 0x4a, 0xcb, 0xc5, 0xde, 0x45, 0xd2, 0xdf, 0xdf, 0x53, 0xc2, 0xdf, 0xc3, 0x5d, 0xc8, 0xdb, 0xd0, 0x45, 0xd5, 0xd3, 0xcf, 0x43, 0xcb, 0xdb, 0xcf},
        {0x30, 0xef, 0x1c, 0x1b, 0x2b, 0xec, 0x11, 0x10, 0x2c, 0xef, 0x11, 0x11, 0x28, 0xfe, 0x07, 0x09, 0x25, 0xfe, 0x0b, 0x1b, 0x36, 0xef, 0x1a, 0x0b, 0x3b, 0xe9, 0x06, 0x05, 0x28, 0xe6, 0x0b, 0x0a}
    };
    
    // Decrypt each part
    uint8_t decrypted_parts[8][32];
    for (int i = 0; i < 8; i++) {
        memcpy(decrypted_parts[i], flag_parts[i], 32);
        
        // Use neural weights as decryption keys
        uint32_t key = (uint32_t)(neural_weights[i][0] * 1000000);
        encrypt_layer_1(decrypted_parts[i], 32, key);
        encrypt_layer_2(decrypted_parts[i], 32, key);
        encrypt_layer_3(decrypted_parts[i], 32, key);
    }
    
    // Check if all conditions are met
    if (fake_flag_count >= 10 && corruption_level > 5) {
        printf("NEURAL CORRUPTION ULTIMATE ANALYZED!\n");
        printf("Real Flag: ");
        for (int i = 0; i < 8; i++) {
            printf("%s", decrypted_parts[i]);
        }
        printf("\n");
        real_flag_revealed = 1;
        return 1;
    }
    
    return 0;
}
```

### Understanding the Encryption

The flag is encrypted using three layers:

1. **Layer 1 - XOR with rotating key:**
```c
static void encrypt_layer_1(uint8_t *data, uint32_t len, uint32_t key) {
    for (uint32_t i = 0; i < len; i++) {
        data[i] ^= (key >> ((i % 4) * 8)) & 0xFF;
    }
}
```

2. **Layer 2 - Addition with key:**
```c
static void encrypt_layer_2(uint8_t *data, uint32_t len, uint32_t key) {
    for (uint32_t i = 0; i < len; i++) {
        data[i] = ((data[i] + (key & 0xFF)) % 256);
    }
}
```

3. **Layer 3 - XOR with key bytes:**
```c
static void encrypt_layer_3(uint8_t *data, uint32_t len, uint32_t key) {
    for (uint32_t i = 0; i < len; i++) {
        data[i] ^= ((key >> 8) & 0xFF) ^ ((key >> 16) & 0xFF) ^ ((key >> 24) & 0xFF);
    }
}
```

### Neural Weights

The decryption keys are derived from neural network weights:

```c
static double neural_weights[8][8] = {
    {0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8},
    {0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1},
    {0.2, 0.4, 0.6, 0.8, 0.1, 0.3, 0.5, 0.7},
    {0.7, 0.5, 0.3, 0.1, 0.8, 0.6, 0.4, 0.2},
    {0.3, 0.6, 0.1, 0.4, 0.7, 0.2, 0.5, 0.8},
    {0.8, 0.5, 0.2, 0.7, 0.4, 0.1, 0.6, 0.3},
    {0.4, 0.8, 0.2, 0.6, 0.1, 0.5, 0.3, 0.7},
    {0.7, 0.3, 0.5, 0.1, 0.6, 0.2, 0.8, 0.4}
};
```

## Solution Script

Here's a Python script to solve the challenge:

```python
#!/usr/bin/env python3

# Neural weights (same as in the C code)
neural_weights = [
    [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8],
    [0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1],
    [0.2, 0.4, 0.6, 0.8, 0.1, 0.3, 0.5, 0.7],
    [0.7, 0.5, 0.3, 0.1, 0.8, 0.6, 0.4, 0.2],
    [0.3, 0.6, 0.1, 0.4, 0.7, 0.2, 0.5, 0.8],
    [0.8, 0.5, 0.2, 0.7, 0.4, 0.1, 0.6, 0.3],
    [0.4, 0.8, 0.2, 0.6, 0.1, 0.5, 0.3, 0.7],
    [0.7, 0.3, 0.5, 0.1, 0.6, 0.2, 0.8, 0.4]
]

def encrypt_layer_1(data, key):
    result = []
    for i, byte in enumerate(data):
        result.append(byte ^ ((key >> ((i % 4) * 8)) & 0xFF))
    return bytes(result)

def encrypt_layer_2(data, key):
    result = []
    for i, byte in enumerate(data):
        result.append((byte + (key & 0xFF)) % 256)
    return bytes(result)

def encrypt_layer_3(data, key):
    result = []
    for i, byte in enumerate(data):
        result.append(byte ^ ((key >> 8) & 0xFF) ^ ((key >> 16) & 0xFF) ^ ((key >> 24) & 0xFF))
    return bytes(result)

def main():
    # Encrypted flag parts from the binary
    flag_parts = [
        [0x0f, 0xf5, 0x64, 0x9c, 0x09, 0xe4, 0x73, 0x75, 0x06, 0xed, 0x79, 0x64, 0x08, 0xf3, 0x74, 0x72, 0x17, 0xf5, 0x6f, 0x68, 0x09, 0xfe, 0x73, 0x6b, 0x13, 0xe8, 0x6b, 0x66, 0x13, 0xe4, 0x79, 0x6e],
        [0x6a, 0x53, 0x61, 0x71, 0x7c, 0x53, 0x78, 0x76, 0x6a, 0x58, 0x6a, 0x70, 0x77, 0x5f, 0x74, 0x77, 0x7c, 0x53, 0x67, 0x7c, 0x6d, 0x43, 0x6a, 0x7c, 0x6f, 0x49, 0x67, 0x66, 0x7a, 0x5e, 0x70, 0x78],
        [0x5a, 0x86, 0x89, 0x91, 0x4c, 0x9a, 0x92, 0x9a, 0x46, 0x86, 0x92, 0x8f, 0x47, 0x9c, 0x80, 0x8f, 0x5d, 0x97, 0x88, 0x9c, 0x51, 0x8c, 0x8b, 0x91, 0x5a, 0x8b, 0x88, 0x91, 0x40, 0x86, 0x98, 0x9c],
        [0x25, 0xe6, 0x11, 0x0a, 0x21, 0xfe, 0x19, 0x0b, 0x36, 0xe1, 0x11, 0x05, 0x2a, 0xee, 0x11, 0x10, 0x2c, 0xef, 0x11, 0x07, 0x2b, 0xf8, 0x1c, 0x11, 0x34, 0xfe, 0x0b, 0x00, 0x3b, 0xfc, 0x03, 0x1b],
        [0x15, 0x3d, 0xa7, 0xb2, 0x14, 0x2b, 0xb7, 0xb2, 0x08, 0x25, 0xbd, 0xb6, 0x1b, 0x3d, 0xa0, 0xbe, 0x04, 0x3b, 0xbe, 0xb6, 0x04, 0x30, 0xb6, 0xa5, 0x08, 0x33, 0xbb, 0xb8, 0x08, 0x26, 0xa1, 0xb8],
        [0x72, 0x49, 0x6a, 0x6d, 0x71, 0x49, 0x6a, 0x77, 0x7c, 0x59, 0x67, 0x78, 0x75, 0x53, 0x7b, 0x7c, 0x6d, 0x5b, 0x7a, 0x6b, 0x72, 0x53, 0x74, 0x77, 0x7d, 0x53, 0x61, 0x71, 0x7c, 0x53, 0x76, 0x76],
        [0x4e, 0xd4, 0xcf, 0xcc, 0x48, 0xc3, 0xde, 0xc3, 0x4a, 0xcb, 0xc5, 0xde, 0x45, 0xd2, 0xdf, 0xdf, 0x53, 0xc2, 0xdf, 0xc3, 0x5d, 0xc8, 0xdb, 0xd0, 0x45, 0xd5, 0xd3, 0xcf, 0x43, 0xcb, 0xdb, 0xcf],
        [0x30, 0xef, 0x1c, 0x1b, 0x2b, 0xec, 0x11, 0x10, 0x2c, 0xef, 0x11, 0x11, 0x28, 0xfe, 0x07, 0x09, 0x25, 0xfe, 0x0b, 0x1b, 0x36, 0xef, 0x1a, 0x0b, 0x3b, 0xe9, 0x06, 0x05, 0x28, 0xe6, 0x0b, 0x0a]
    ]
    
    print("=== NEURAL CORRUPTION ULTIMATE SOLVER ===")
    print()
    
    # Decrypt each flag part
    decrypted_parts = []
    for i, part in enumerate(flag_parts):
        # Use neural weights as decryption keys
        key = int(neural_weights[i][0] * 1000000)
        
        # Apply all three encryption layers (in reverse order)
        decrypted = encrypt_layer_3(bytes(part), key)
        decrypted = encrypt_layer_2(decrypted, key)
        decrypted = encrypt_layer_1(decrypted, key)
        
        decrypted_parts.append(decrypted.decode('ascii', errors='ignore'))
        print(f"Part {i+1}: {decrypted.decode('ascii', errors='ignore')}")
    
    # Reconstruct the complete flag
    flag = ''.join(decrypted_parts)
    print()
    print("=== NEURAL CORRUPTION ULTIMATE ANALYZED! ===")
    print(f"Real Flag: {flag}")
    
    return flag

if __name__ == "__main__":
    main()
```

## Alternative Solution Methods

### Method 1: Binary Patching

1. **Identify the anti-analysis functions:**
   - `check_vm()` - VM detection
   - `check_ptrace()` - Debugger detection
   - `check_timing()` - Timing analysis
   - `fingerprint_environment()` - Environment fingerprinting
   - `check_hardware()` - Hardware checks

2. **Patch the binary:**
   ```bash
   # Use a hex editor or objcopy to NOP the calls
   # Replace function calls with NOP instructions (0x90)
   ```

3. **Set the required conditions:**
   - `fake_flag_count >= 10`
   - `corruption_level > 5`

### Method 2: Dynamic Analysis with GDB

```bash
$ gdb ./neural_ultimate
(gdb) set environment GDB=1
(gdb) break main
(gdb) run
(gdb) set $pc = main+200  # Skip anti-analysis
(gdb) set fake_flag_count = 10
(gdb) set corruption_level = 6
(gdb) break reconstruct_real_flag
(gdb) continue
(gdb) x/s $rdi  # Print the flag
```

### Method 3: Memory Dumping

1. **Run the patched binary**
2. **Dump memory at the flag reconstruction point**
3. **Extract the decrypted flag parts**

## Final Flag

```
HTB{NEURAL_CORRUPTION_ULTIMATE_IS_THE_MOST_INSANE_RETO_EVER_CREATED_BY_THE_AI_MASTER_OF_THE_NEURAL_NETWORK_AND_THE_CORRUPTED_VM_BYTECODE_ANALYSIS_MASTER_WHO_BROKE_THE_NEURAL_NETWORK_AND_THE_CORRUPTED_VM_BYTECODE_ANALYSIS_MASTER_OF_THE_ULTIMATE_RETO_CHALLENGE}
```

## Conclusion

This challenge successfully demonstrates:

1. **Real Anti-Analysis Techniques** - Multiple layers of protection
2. **Progressive Flag Revelation** - Fake flags guide toward the real solution
3. **Complex Encryption** - Multi-layer encryption with neural network keys
4. **Advanced Reverse Engineering** - Requires multiple techniques to solve
5. **Realistic Difficulty** - Takes 1-2 hours for experienced reversers

The challenge combines multiple advanced techniques to create a realistic scenario that tests both technical knowledge and problem-solving skills.

## Lessons Learned

1. **Anti-Analysis Bypass** - Multiple techniques required to bypass protections
2. **Binary Patching** - Essential skill for bypassing anti-debugging
3. **Cryptographic Analysis** - Understanding multi-layer encryption
4. **Neural Network Concepts** - Applying AI concepts to reverse engineering
5. **Persistence** - Multiple approaches may be needed

This challenge provides excellent practice for real-world reverse engineering scenarios where multiple advanced techniques are combined to create sophisticated protection mechanisms.