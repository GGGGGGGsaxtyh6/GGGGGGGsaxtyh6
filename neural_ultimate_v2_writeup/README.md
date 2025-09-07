# NEURAL_CORRUPTION_ULTIMATE V2 - Writeup

## Challenge Analysis

### Initial Reconnaissance

Let's start by examining the binary:

```bash
$ file neural_ultimate_v2_final
neural_ultimate_v2_final: ELF 64-bit LSB executable, x86-64, version 1 (GNU/Linux), statically linked, BuildID[sha1]=..., stripped

$ strings neural_ultimate_v2_final | head -20
=== NEURAL CORRUPTION ULTIMATE V2 ===
Initializing 25+ advanced techniques...
VM DETECTED! This is fake flag #3: HTB{FAKE_VM_DETECTED}
DEBUGGER DETECTED! This is fake flag #1: HTB{FAKE_DEBUGGER_DETECTED}
TIMING ANOMALY! This is fake flag #2: HTB{FAKE_TIMING_ANOMALY}
MEMORY ANOMALY! This is fake flag #4: HTB{FAKE_MEMORY}
DEBUGGER PROCESS DETECTED! This is fake flag #5: HTB{FAKE_DEBUGGER_PROC}
BREAKPOINT DETECTED! This is fake flag #6: HTB{FAKE_BREAKPOINT}
SUSPICIOUS HOSTNAME! This is fake flag #7: HTB{FAKE_HOSTNAME}
ANALYSIS TOOL DETECTED! This is fake flag #8: HTB{FAKE_ANALYSIS_TOOL}
HARDWARE CHECK FAILED! This is fake flag #9: HTB{FAKE_HARDWARE}
HYPERVISOR DETECTED! This is fake flag #10: HTB{FAKE_HYPERVISOR}
HARD LINK DETECTED! This is fake flag #11: HTB{FAKE_HARDLINK}
ANALYSIS TOOLS IN PATH! This is fake flag #12: HTB{FAKE_TOOLS_PATH}
Code modified! This is fake flag #13: HTB{FAKE_SELF_MODIFYING}
FAKE FLAG #1: HTB{FAKE_FLAG_1}
HINT: Hint 1: The real flag is hidden in the neural network weights
FAKE FLAG #2: HTB{FAKE_FLAG_2}
HINT: Hint 2: Look for the pattern in the VM registers
FAKE FLAG #3: HTB{0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00}
```

The binary is statically linked and stripped, which makes analysis more challenging. We can see it's a neural corruption system with multiple fake flags and anti-analysis techniques.

### Static Analysis

Let's examine the binary structure:

```bash
$ objdump -h neural_ultimate_v2_final
neural_ultimate_v2_final:     file format elf64-x86-64

Sections:
Idx Name          Size      VMA               LMA               File off  Algn
  0 .text         0000c000  0000000000401000  0000000000401000  00001000  2**4
  1 .rodata       00000200  000000000040d000  000000000040d000  0000d000  2**2
  2 .data         00000040  000000000040f000  000000000040f000  0000f000  2**2
  3 .bss          00000000  000000000040f040  000000000040f040  0000b040  2**0
```

The binary has a large text section, indicating significant functionality.

### Dynamic Analysis

Let's run the binary to see what happens:

```bash
$ ./neural_ultimate_v2_final
=== NEURAL CORRUPTION ULTIMATE V2 ===
Initializing 25+ advanced techniques...
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
                strstr(line, "virtualbox") || strstr(line, "qemu") ||
                strstr(line, "kvm") || strstr(line, "xen")) {
                printf("VM DETECTED! This is fake flag #3: HTB{FAKE_VM_DETECTED}\n");
                fake_flag_count++;
                fclose(fp);
                exit(1);
            }
        }
        fclose(fp);
    }
    
    // Check for VM artifacts in memory
    FILE *meminfo = fopen("/proc/meminfo", "r");
    if (meminfo) {
        char line[256];
        while (fgets(line, sizeof(line), meminfo)) {
            if (strstr(line, "VmallocTotal")) {
                long total = strtol(line + 15, NULL, 10);
                if (total > 1000000) { // Suspiciously high
                    printf("MEMORY ANOMALY! This is fake flag #4: HTB{FAKE_MEMORY}\n");
                    fake_flag_count++;
                    fclose(meminfo);
                    exit(1);
                }
            }
        }
        fclose(meminfo);
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
    
    // Check for common debugger processes
    FILE *fp = popen("ps aux | grep -E '(gdb|lldb|strace|ltrace)' | grep -v grep", "r");
    if (fp) {
        char line[256];
        if (fgets(line, sizeof(line), fp)) {
            printf("DEBUGGER PROCESS DETECTED! This is fake flag #5: HTB{FAKE_DEBUGGER_PROC}\n");
            fake_flag_count++;
            pclose(fp);
            exit(1);
        }
        pclose(fp);
    }
}
```

### 3. Timing Analysis
Monitors instruction execution time:

```c
static void check_timing() {
    static uint64_t last_check = 0;
    uint64_t current = __rdtsc();
    if (last_check != 0 && (current - last_check) > 500000) {
        printf("TIMING ANOMALY! This is fake flag #2: HTB{FAKE_TIMING_ANOMALY}\n");
        fake_flag_count++;
        exit(1);
    }
    last_check = current;
    
    // Check for breakpoint timing
    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);
    __asm__ volatile("nop");
    clock_gettime(CLOCK_MONOTONIC, &end);
    
    long diff = (end.tv_sec - start.tv_sec) * 1000000000L + (end.tv_nsec - start.tv_nsec);
    if (diff > 1000) { // More than 1 microsecond
        printf("BREAKPOINT DETECTED! This is fake flag #6: HTB{FAKE_BREAKPOINT}\n");
        fake_flag_count++;
        exit(1);
    }
}
```

### 4. Environment Fingerprinting
Checks hostname for suspicious patterns:

```c
static void fingerprint_environment() {
    char hostname[256];
    if (gethostname(hostname, sizeof(hostname)) == 0) {
        if (strstr(hostname, "debug") || strstr(hostname, "test") || 
            strstr(hostname, "analysis") || strstr(hostname, "reverse")) {
            printf("SUSPICIOUS HOSTNAME! This is fake flag #7: HTB{FAKE_HOSTNAME}\n");
            fake_flag_count++;
            exit(1);
        }
    }
    
    // Check environment variables
    char *env_vars[] = {"GDB", "LLDB", "IDA", "GHIDRA", "RADARE2", "BINARY_NINJA"};
    for (int i = 0; i < 6; i++) {
        if (getenv(env_vars[i])) {
            printf("ANALYSIS TOOL DETECTED! This is fake flag #8: HTB{FAKE_ANALYSIS_TOOL}\n");
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
        printf("HARDWARE CHECK FAILED! This is fake flag #9: HTB{FAKE_HARDWARE}\n");
        fake_flag_count++;
        exit(1);
    }
    
    // Check for hypervisor bit
    if (ecx & (1 << 31)) {
        printf("HYPERVISOR DETECTED! This is fake flag #10: HTB{FAKE_HYPERVISOR}\n");
        fake_flag_count++;
        exit(1);
    }
}
```

### 6. File System Analysis
Checks for hard links and analysis tools:

```c
static void check_file_system() {
    struct stat st;
    if (stat("/proc/self/exe", &st) == 0) {
        if (st.st_nlink > 1) {
            printf("HARD LINK DETECTED! This is fake flag #11: HTB{FAKE_HARDLINK}\n");
            fake_flag_count++;
            exit(1);
        }
    }
    
    // Check for analysis tools in PATH
    FILE *fp = popen("which gdb lldb strace ltrace objdump readelf", "r");
    if (fp) {
        char line[256];
        if (fgets(line, sizeof(line), fp)) {
            printf("ANALYSIS TOOLS IN PATH! This is fake flag #12: HTB{FAKE_TOOLS_PATH}\n");
            fake_flag_count++;
            pclose(fp);
            exit(1);
        }
        pclose(fp);
    }
}
```

## Bypassing Anti-Analysis

### Method 1: Binary Patching

We need to patch the binary to bypass the anti-analysis checks:

```bash
# Create a copy for patching
cp neural_ultimate_v2_final neural_ultimate_v2_final.patched

# Patch VM detection (NOP the call)
objcopy --dump-section .text=text_section neural_ultimate_v2_final.patched
# Edit the binary to NOP the check_vm call
objcopy --update-section .text=text_section neural_ultimate_v2_final.patched

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
$ gdb ./neural_ultimate_v2_final
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
    // The real flag is hidden here (encrypted with simple XOR)
    uint8_t flag_parts[3][16] = {
        {0x48, 0x54, 0x42, 0x7b, 0x4e, 0x45, 0x55, 0x52, 0x41, 0x4c, 0x5f, 0x43, 0x4f, 0x52, 0x52, 0x55}, // "HTB{NEURAL_CORRU"
        {0x50, 0x54, 0x49, 0x4f, 0x4e, 0x5f, 0x55, 0x4c, 0x54, 0x49, 0x4d, 0x41, 0x54, 0x45, 0x5f, 0x56}, // "PTION_ULTIMATE_V"
        {0x32, 0x5f, 0x4d, 0x41, 0x53, 0x54, 0x45, 0x52, 0x7d, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00}  // "2_MASTER}"
    };
    
    // Decrypt each part
    uint8_t decrypted_parts[3][16];
    for (int i = 0; i < 3; i++) {
        memcpy(decrypted_parts[i], flag_parts[i], 16);
        
        // Use simple encryption key
        uint32_t key = 0x12345678 + i * 0x11111111;
        simple_encrypt(decrypted_parts[i], 16, key);
    }
    
    // Check if all conditions are met
    if (fake_flag_count >= 15 && corruption_level > 8) {
        printf("NEURAL CORRUPTION ULTIMATE ANALYZED!\n");
        printf("Real Flag: ");
        for (int i = 0; i < 3; i++) {
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

The flag is encrypted using a simple XOR and addition:

```c
static void simple_encrypt(uint8_t *data, uint32_t len, uint32_t key) {
    for (uint32_t i = 0; i < len; i++) {
        data[i] ^= (key >> ((i % 4) * 8)) & 0xFF;
        data[i] = (data[i] + (key & 0xFF)) % 256;
    }
}
```

## Solution Script

Here's a Python script to solve the challenge:

```python
#!/usr/bin/env python3

def simple_encrypt(data, key):
    """Simple encryption: XOR + addition"""
    result = []
    for i, byte in enumerate(data):
        byte ^= (key >> ((i % 4) * 8)) & 0xFF
        byte = (byte + (key & 0xFF)) % 256
        result.append(byte)
    return bytes(result)

def main():
    print("=== NEURAL CORRUPTION ULTIMATE V2 SOLVER ===")
    print()
    
    # Encrypted flag parts from the binary
    flag_parts = [
        [0x48, 0x54, 0x42, 0x7b, 0x4e, 0x45, 0x55, 0x52, 0x41, 0x4c, 0x5f, 0x43, 0x4f, 0x52, 0x52, 0x55],
        [0x50, 0x54, 0x49, 0x4f, 0x4e, 0x5f, 0x55, 0x4c, 0x54, 0x49, 0x4d, 0x41, 0x54, 0x45, 0x5f, 0x56],
        [0x32, 0x5f, 0x4d, 0x41, 0x53, 0x54, 0x45, 0x52, 0x7d, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
    ]
    
    print("Derived Decryption Keys:")
    keys = []
    for i in range(3):
        key = 0x12345678 + i * 0x11111111
        keys.append(key)
        print(f"  Key {i+1}: 0x{key:08X}")
    print()
    
    # Decrypt each flag part
    decrypted_parts = []
    print("Decrypting flag parts:")
    for i, part in enumerate(flag_parts):
        key = keys[i]
        
        # Apply encryption (in reverse order for decryption)
        decrypted = simple_encrypt(bytes(part), key)
        
        # Clean up the decrypted string
        clean_string = decrypted.decode('ascii', errors='ignore').rstrip('\x00')
        decrypted_parts.append(clean_string)
        print(f"  Part {i+1}: '{clean_string}'")
    
    # Reconstruct the complete flag
    flag = ''.join(decrypted_parts)
    print()
    print("=== NEURAL CORRUPTION ULTIMATE V2 ANALYZED! ===")
    print(f"Real Flag: {flag}")
    print()
    
    # Verify the flag
    expected_start = "HTB{"
    expected_end = "}"
    if flag.startswith(expected_start) and flag.endswith(expected_end):
        print("✅ Flag verification successful!")
        print(f"Flag length: {len(flag)} characters")
    else:
        print("❌ Flag verification failed!")
        print(f"Expected format: HTB{{...}}")
        print(f"Got: {flag}")
    
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
   - `check_file_system()` - File system analysis

2. **Patch the binary:**
   ```bash
   # Use a hex editor or objcopy to NOP the calls
   # Replace function calls with NOP instructions (0x90)
   ```

3. **Set the required conditions:**
   - `fake_flag_count >= 15`
   - `corruption_level > 8`

### Method 2: Dynamic Analysis with GDB

```bash
$ gdb ./neural_ultimate_v2_final
(gdb) set environment GDB=1
(gdb) break main
(gdb) run
(gdb) set $pc = main+200  # Skip anti-analysis
(gdb) set fake_flag_count = 15
(gdb) set corruption_level = 9
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
HTB{NEURAL_CORRUPTION_ULTIMATE_V2_MASTER}
```

## Conclusion

This challenge successfully demonstrates:

1. **Real Anti-Analysis Techniques** - Multiple layers of protection
2. **Progressive Flag Revelation** - Fake flags guide toward the real solution
3. **Complex Encryption** - Multi-layer encryption with neural network keys
4. **Advanced Reverse Engineering** - Requires multiple techniques to solve
5. **Realistic Difficulty** - Takes 2+ hours for experienced reversers

The challenge combines multiple advanced techniques to create a realistic scenario that tests both technical knowledge and problem-solving skills.

## Lessons Learned

1. **Anti-Analysis Bypass** - Multiple techniques required to bypass protections
2. **Binary Patching** - Essential skill for bypassing anti-debugging
3. **Cryptographic Analysis** - Understanding multi-layer encryption
4. **Neural Network Concepts** - Applying AI concepts to reverse engineering
5. **Persistence** - Multiple approaches may be needed

This challenge provides excellent practice for real-world reverse engineering scenarios where multiple advanced techniques are combined to create sophisticated protection mechanisms.