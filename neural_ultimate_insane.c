#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/ptrace.h>
#include <sys/wait.h>
#include <time.h>
#include <math.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/mman.h>
#include <signal.h>
#include <setjmp.h>
#include <stdint.h>
#include <x86intrin.h>
#include <sys/syscall.h>
#include <linux/seccomp.h>
#include <sys/prctl.h>

// Global variables for anti-analysis
static int fake_flag_count = 0;
static int corruption_level = 0;
static int real_flag_revealed = 0;
static jmp_buf env;
static volatile int debugger_detected = 0;
static volatile int vm_detected = 0;
static volatile int timing_anomaly = 0;
static uint64_t start_time = 0;
static uint64_t end_time = 0;

// Advanced VM structure with obfuscated instructions
typedef struct {
    uint32_t regs[32];
    uint8_t memory[2*1024*1024];
    uint32_t pc;
    uint32_t sp;
    uint32_t flags;
    uint8_t stack[8192];
    uint32_t instruction_cache[256];
    uint8_t opcode_table[256];
} AdvancedVM;

// Neural network with backpropagation
typedef struct {
    double weights[128][128];
    double biases[128];
    double activations[128];
    double gradients[128];
    int layers;
    int neurons_per_layer;
    double learning_rate;
} NeuralNet;

// Polymorphic engine with code mutation
typedef struct {
    uint8_t *code;
    uint32_t size;
    uint32_t key;
    uint8_t mutations[512];
    uint8_t junk_code[1024];
    uint32_t mutation_count;
} PolymorphicEngine;

// Control flow flattening
typedef struct {
    uint32_t state;
    uint32_t next_state;
    uint32_t *state_table;
    uint32_t num_states;
} ControlFlowFlattener;

// Anti-analysis functions with advanced techniques
static void check_vm_advanced() {
    // Check multiple VM indicators
    FILE *fp = fopen("/proc/cpuinfo", "r");
    if (fp) {
        char line[512];
        int vm_indicators = 0;
        while (fgets(line, sizeof(line), fp)) {
            if (strstr(line, "hypervisor") || strstr(line, "vmware") || 
                strstr(line, "virtualbox") || strstr(line, "qemu") ||
                strstr(line, "kvm") || strstr(line, "xen") ||
                strstr(line, "parallels") || strstr(line, "vbox")) {
                vm_indicators++;
            }
        }
        fclose(fp);
        if (vm_indicators > 0) {
            printf("VM DETECTED! This is fake flag #3: HTB{FAKE_VM_DETECTED}\n");
            fake_flag_count++;
            exit(1);
        }
    }
    
    // Check for VM artifacts in memory
    FILE *meminfo = fopen("/proc/meminfo", "r");
    if (meminfo) {
        char line[512];
        while (fgets(line, sizeof(line), meminfo)) {
            if (strstr(line, "VmallocTotal")) {
                long total = strtol(line + 15, NULL, 10);
                if (total > 1000000) {
                    printf("MEMORY ANOMALY! This is fake flag #4: HTB{FAKE_MEMORY}\n");
                    fake_flag_count++;
                    fclose(meminfo);
                    exit(1);
                }
            }
        }
        fclose(meminfo);
    }
    
    // Check for VM-specific files
    if (access("/proc/vz", F_OK) == 0 || access("/proc/xen", F_OK) == 0) {
        printf("CONTAINER DETECTED! This is fake flag #15: HTB{FAKE_CONTAINER}\n");
        fake_flag_count++;
        exit(1);
    }
}

static void check_ptrace_advanced() {
    // Multiple ptrace checks
    if (ptrace(PTRACE_TRACEME, 0, 1, 0) == -1) {
        printf("DEBUGGER DETECTED! This is fake flag #1: HTB{FAKE_DEBUGGER_DETECTED}\n");
        fake_flag_count++;
        exit(1);
    }
    
    // Check for common debugger processes
    FILE *fp = popen("ps aux | grep -E '(gdb|lldb|strace|ltrace|radare2|r2|ida|ghidra)' | grep -v grep", "r");
    if (fp) {
        char line[512];
        if (fgets(line, sizeof(line), fp)) {
            printf("DEBUGGER PROCESS DETECTED! This is fake flag #5: HTB{FAKE_DEBUGGER_PROC}\n");
            fake_flag_count++;
            pclose(fp);
            exit(1);
        }
        pclose(fp);
    }
    
    // Check for ptrace parent
    FILE *status = fopen("/proc/self/status", "r");
    if (status) {
        char line[512];
        while (fgets(line, sizeof(line), status)) {
            if (strstr(line, "TracerPid:")) {
                int tracer_pid = atoi(line + 11);
                if (tracer_pid != 0) {
                    printf("PTRACE PARENT DETECTED! This is fake flag #16: HTB{FAKE_PTRACE_PARENT}\n");
                    fake_flag_count++;
                    fclose(status);
                    exit(1);
                }
            }
        }
        fclose(status);
    }
}

static void check_timing_advanced() {
    static uint64_t last_check = 0;
    uint64_t current = __rdtsc();
    if (last_check != 0 && (current - last_check) > 100000) {
        printf("TIMING ANOMALY! This is fake flag #2: HTB{FAKE_TIMING_ANOMALY}\n");
        fake_flag_count++;
        exit(1);
    }
    last_check = current;
    
    // Check for breakpoint timing with multiple measurements
    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);
    for (int i = 0; i < 100; i++) {
        __asm__ volatile("nop");
    }
    clock_gettime(CLOCK_MONOTONIC, &end);
    
    long diff = (end.tv_sec - start.tv_sec) * 1000000000L + (end.tv_nsec - start.tv_nsec);
    if (diff > 10000) { // More than 10 microseconds for 100 NOPs
        printf("BREAKPOINT DETECTED! This is fake flag #6: HTB{FAKE_BREAKPOINT}\n");
        fake_flag_count++;
        exit(1);
    }
    
    // Check for single-step timing
    clock_gettime(CLOCK_MONOTONIC, &start);
    __asm__ volatile("int3");
    clock_gettime(CLOCK_MONOTONIC, &end);
    
    diff = (end.tv_sec - start.tv_sec) * 1000000000L + (end.tv_nsec - start.tv_nsec);
    if (diff > 1000) {
        printf("SINGLE STEP DETECTED! This is fake flag #17: HTB{FAKE_SINGLE_STEP}\n");
        fake_flag_count++;
        exit(1);
    }
}

static void fingerprint_environment_advanced() {
    char hostname[512];
    if (gethostname(hostname, sizeof(hostname)) == 0) {
        if (strstr(hostname, "debug") || strstr(hostname, "test") || 
            strstr(hostname, "analysis") || strstr(hostname, "reverse") ||
            strstr(hostname, "vm") || strstr(hostname, "docker")) {
            printf("SUSPICIOUS HOSTNAME! This is fake flag #7: HTB{FAKE_HOSTNAME}\n");
            fake_flag_count++;
            exit(1);
        }
    }
    
    // Check environment variables
    char *env_vars[] = {"GDB", "LLDB", "IDA", "GHIDRA", "RADARE2", "BINARY_NINJA", "DOCKER", "KUBERNETES"};
    for (int i = 0; i < 8; i++) {
        if (getenv(env_vars[i])) {
            printf("ANALYSIS TOOL DETECTED! This is fake flag #8: HTB{FAKE_ANALYSIS_TOOL}\n");
            fake_flag_count++;
            exit(1);
        }
    }
    
    // Check for analysis tools in PATH
    FILE *fp = popen("which gdb lldb strace ltrace objdump readelf radare2 r2 ida ghidra", "r");
    if (fp) {
        char line[512];
        if (fgets(line, sizeof(line), fp)) {
            printf("ANALYSIS TOOLS IN PATH! This is fake flag #12: HTB{FAKE_TOOLS_PATH}\n");
            fake_flag_count++;
            pclose(fp);
            exit(1);
        }
        pclose(fp);
    }
}

static void check_hardware_advanced() {
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
    
    // Check for VM-specific CPU features
    __asm__ volatile("cpuid" : "=a"(eax), "=b"(ebx), "=c"(ecx), "=d"(edx) : "a"(0x40000000));
    if (eax >= 0x40000000) {
        printf("HYPERVISOR CPUID DETECTED! This is fake flag #18: HTB{FAKE_HYPERVISOR_CPUID}\n");
        fake_flag_count++;
        exit(1);
    }
}

static void check_file_system_advanced() {
    struct stat st;
    if (stat("/proc/self/exe", &st) == 0) {
        if (st.st_nlink > 1) {
            printf("HARD LINK DETECTED! This is fake flag #11: HTB{FAKE_HARDLINK}\n");
            fake_flag_count++;
            exit(1);
        }
    }
    
    // Check for analysis tools in common locations
    char *tool_paths[] = {
        "/usr/bin/gdb", "/usr/bin/lldb", "/usr/bin/strace", "/usr/bin/ltrace",
        "/usr/bin/objdump", "/usr/bin/readelf", "/usr/bin/radare2", "/usr/bin/r2",
        "/opt/ida", "/opt/ghidra", "/usr/local/bin/gdb", "/usr/local/bin/lldb"
    };
    
    for (int i = 0; i < 12; i++) {
        if (access(tool_paths[i], F_OK) == 0) {
            printf("ANALYSIS TOOL FOUND! This is fake flag #19: HTB{FAKE_TOOL_FOUND}\n");
            fake_flag_count++;
            exit(1);
        }
    }
}

static void check_seccomp() {
    // Check if seccomp is enabled
    FILE *fp = fopen("/proc/self/status", "r");
    if (fp) {
        char line[512];
        while (fgets(line, sizeof(line), fp)) {
            if (strstr(line, "Seccomp:")) {
                int seccomp = atoi(line + 9);
                if (seccomp != 0) {
                    printf("SECCOMP DETECTED! This is fake flag #20: HTB{FAKE_SECCOMP}\n");
                    fake_flag_count++;
                    fclose(fp);
                    exit(1);
                }
            }
        }
        fclose(fp);
    }
}

// Advanced VM implementation with obfuscated bytecode
static void init_vm_advanced(AdvancedVM *vm) {
    memset(vm, 0, sizeof(AdvancedVM));
    vm->sp = 8192;
    vm->pc = 0;
    vm->flags = 0;
    
    // Load heavily obfuscated bytecode
    uint8_t bytecode[] = {
        // Obfuscated instructions with junk bytes
        0x01, 0x00, 0x00, 0x00, 0x48, 0x54, 0x42, 0x7b, 0xAA, 0xBB, 0xCC, 0xDD,  // LOAD reg0, "HTB{"
        0x02, 0x01, 0x00, 0x00, 0x4e, 0x45, 0x55, 0x52, 0xEE, 0xFF, 0x11, 0x22,  // LOAD reg1, "NEUR"
        0x03, 0x02, 0x00, 0x00, 0x41, 0x4c, 0x5f, 0x43, 0x33, 0x44, 0x55, 0x66,  // LOAD reg2, "AL_C"
        0x04, 0x03, 0x00, 0x00, 0x4f, 0x52, 0x52, 0x55, 0x77, 0x88, 0x99, 0xAA,  // LOAD reg3, "ORRU"
        0x05, 0x04, 0x00, 0x00, 0x50, 0x54, 0x49, 0x4f, 0xBB, 0xCC, 0xDD, 0xEE,  // LOAD reg4, "PTIO"
        0x06, 0x05, 0x00, 0x00, 0x4e, 0x5f, 0x55, 0x4c, 0xFF, 0x11, 0x22, 0x33,  // LOAD reg5, "N_UL"
        0x07, 0x06, 0x00, 0x00, 0x54, 0x49, 0x4d, 0x41, 0x44, 0x55, 0x66, 0x77,  // LOAD reg6, "TIMA"
        0x08, 0x07, 0x00, 0x00, 0x54, 0x45, 0x5f, 0x56, 0x88, 0x99, 0xAA, 0xBB,  // LOAD reg7, "TE_V"
        0x09, 0x08, 0x00, 0x00, 0x32, 0x5f, 0x4d, 0x41, 0xCC, 0xDD, 0xEE, 0xFF,  // LOAD reg8, "2_MA"
        0x0a, 0x09, 0x00, 0x00, 0x53, 0x54, 0x45, 0x52, 0x11, 0x22, 0x33, 0x44,  // LOAD reg9, "STER"
        0x0b, 0x0a, 0x00, 0x00, 0x7d, 0x00, 0x00, 0x00, 0x55, 0x66, 0x77, 0x88   // LOAD reg10, "}"
    };
    
    memcpy(vm->memory, bytecode, sizeof(bytecode));
    
    // Initialize opcode table with obfuscation
    for (int i = 0; i < 256; i++) {
        vm->opcode_table[i] = (i ^ 0xAA) & 0xFF;
    }
}

static void execute_vm_instruction_advanced(AdvancedVM *vm) {
    uint8_t opcode = vm->memory[vm->pc];
    uint32_t operand1 = *(uint32_t*)(vm->memory + vm->pc + 1);
    uint32_t operand2 = *(uint32_t*)(vm->memory + vm->pc + 5);
    
    // Obfuscated instruction execution
    opcode = vm->opcode_table[opcode];
    
    switch (opcode) {
        case 0x01: // LOAD
            vm->regs[operand1 & 0x1F] = operand2;
            vm->pc += 13; // Skip junk bytes
            break;
        case 0x02: // XOR
            vm->regs[operand1 & 0x1F] ^= vm->regs[operand2 & 0x1F];
            vm->pc += 13;
            break;
        case 0x03: // ADD
            vm->regs[operand1 & 0x1F] += vm->regs[operand2 & 0x1F];
            vm->pc += 13;
            break;
        case 0x04: // SUB
            vm->regs[operand1 & 0x1F] -= vm->regs[operand2 & 0x1F];
            vm->pc += 13;
            break;
        case 0x05: // MUL
            vm->regs[operand1 & 0x1F] *= vm->regs[operand2 & 0x1F];
            vm->pc += 13;
            break;
        case 0x06: // DIV
            if (vm->regs[operand2 & 0x1F] != 0) {
                vm->regs[operand1 & 0x1F] /= vm->regs[operand2 & 0x1F];
            }
            vm->pc += 13;
            break;
        case 0x07: // AND
            vm->regs[operand1 & 0x1F] &= vm->regs[operand2 & 0x1F];
            vm->pc += 13;
            break;
        case 0x08: // OR
            vm->regs[operand1 & 0x1F] |= vm->regs[operand2 & 0x1F];
            vm->pc += 13;
            break;
        case 0x09: // NOT
            vm->regs[operand1 & 0x1F] = ~vm->regs[operand1 & 0x1F];
            vm->pc += 9;
            break;
        case 0x0a: // SHL
            vm->regs[operand1 & 0x1F] <<= (vm->regs[operand2 & 0x1F] & 0x1F);
            vm->pc += 13;
            break;
        case 0x0b: // SHR
            vm->regs[operand1 & 0x1F] >>= (vm->regs[operand2 & 0x1F] & 0x1F);
            vm->pc += 13;
            break;
        case 0x0c: // CMP
            if (vm->regs[operand1 & 0x1F] == vm->regs[operand2 & 0x1F]) {
                vm->flags |= 0x01; // ZERO flag
            } else {
                vm->flags &= ~0x01;
            }
            vm->pc += 13;
            break;
        case 0x0d: // JMP
            vm->pc = operand1;
            break;
        case 0x0e: // JZ
            if (vm->flags & 0x01) {
                vm->pc = operand1;
            } else {
                vm->pc += 5;
            }
            break;
        case 0x0f: // JNZ
            if (!(vm->flags & 0x01)) {
                vm->pc = operand1;
            } else {
                vm->pc += 5;
            }
            break;
        default:
            vm->pc++;
            break;
    }
}

// Neural network with backpropagation
static void init_neural_net_advanced(NeuralNet *net) {
    net->layers = 6;
    net->neurons_per_layer = 32;
    net->learning_rate = 0.01;
    
    // Initialize weights with specific values
    for (int i = 0; i < 128; i++) {
        for (int j = 0; j < 128; j++) {
            net->weights[i][j] = sin(i * j * 0.1) * 0.5;
        }
        net->biases[i] = cos(i * 0.2) * 0.3;
    }
}

static double sigmoid_advanced(double x) {
    return 1.0 / (1.0 + exp(-x));
}

static double sigmoid_derivative(double x) {
    double s = sigmoid_advanced(x);
    return s * (1.0 - s);
}

static void forward_propagate_advanced(NeuralNet *net, double *input) {
    for (int i = 0; i < net->neurons_per_layer; i++) {
        net->activations[i] = net->biases[i];
        for (int j = 0; j < net->neurons_per_layer; j++) {
            net->activations[i] += input[j] * net->weights[i][j];
        }
        net->activations[i] = sigmoid_advanced(net->activations[i]);
    }
}

static void backward_propagate_advanced(NeuralNet *net, double *target) {
    // Calculate gradients
    for (int i = 0; i < net->neurons_per_layer; i++) {
        net->gradients[i] = (net->activations[i] - target[i]) * sigmoid_derivative(net->activations[i]);
    }
    
    // Update weights
    for (int i = 0; i < net->neurons_per_layer; i++) {
        for (int j = 0; j < net->neurons_per_layer; j++) {
            net->weights[i][j] -= net->learning_rate * net->gradients[i] * net->activations[j];
        }
        net->biases[i] -= net->learning_rate * net->gradients[i];
    }
}

// Polymorphic engine with advanced mutation
static void init_polymorphic_engine_advanced(PolymorphicEngine *engine) {
    engine->key = 0xDEADBEEF;
    engine->size = 2048;
    engine->code = malloc(engine->size);
    engine->mutation_count = 0;
    
    // Generate mutation table
    for (int i = 0; i < 512; i++) {
        engine->mutations[i] = (i ^ engine->key) & 0xFF;
    }
    
    // Generate junk code
    for (int i = 0; i < 1024; i++) {
        engine->junk_code[i] = rand() & 0xFF;
    }
}

static void mutate_code_advanced(PolymorphicEngine *engine) {
    for (uint32_t i = 0; i < engine->size; i++) {
        engine->code[i] = engine->mutations[engine->code[i]];
    }
    engine->mutation_count++;
}

// Advanced encryption with multiple layers
static void encrypt_layer_1_advanced(uint8_t *data, uint32_t len, uint32_t key) {
    for (uint32_t i = 0; i < len; i++) {
        data[i] ^= (key >> ((i % 4) * 8)) & 0xFF;
    }
}

static void encrypt_layer_2_advanced(uint8_t *data, uint32_t len, uint32_t key) {
    for (uint32_t i = 0; i < len; i++) {
        data[i] = ((data[i] + (key & 0xFF)) % 256);
    }
}

static void encrypt_layer_3_advanced(uint8_t *data, uint32_t len, uint32_t key) {
    for (uint32_t i = 0; i < len; i++) {
        data[i] ^= ((key >> 8) & 0xFF) ^ ((key >> 16) & 0xFF) ^ ((key >> 24) & 0xFF);
    }
}

static void encrypt_layer_4_advanced(uint8_t *data, uint32_t len, uint32_t key) {
    for (uint32_t i = 0; i < len; i++) {
        data[i] = ((data[i] * (key & 0xFF)) % 256);
    }
}

static void encrypt_layer_5_advanced(uint8_t *data, uint32_t len, uint32_t key) {
    for (uint32_t i = 0; i < len; i++) {
        data[i] ^= ((key >> 4) & 0xFF) ^ ((key >> 12) & 0xFF) ^ ((key >> 20) & 0xFF) ^ ((key >> 28) & 0xFF);
    }
}

static void encrypt_layer_6_advanced(uint8_t *data, uint32_t len, uint32_t key) {
    for (uint32_t i = 0; i < len; i++) {
        data[i] = ((data[i] + (key >> 16)) % 256);
    }
}

static void encrypt_layer_7_advanced(uint8_t *data, uint32_t len, uint32_t key) {
    for (uint32_t i = 0; i < len; i++) {
        data[i] ^= ((key >> 24) & 0xFF) ^ ((key >> 8) & 0xFF) ^ ((key >> 0) & 0xFF);
    }
}

// Fake functions to confuse analysis
static void fake_function_1() {
    printf("This function does nothing useful\n");
    fake_flag_count++;
}

static void fake_function_2() {
    printf("Another useless function\n");
    fake_flag_count++;
}

static void fake_function_3() {
    printf("Code modified! This is fake flag #13: HTB{FAKE_SELF_MODIFYING}\n");
    fake_flag_count++;
}

static void fake_function_4() {
    printf("FAKE FLAG #1: HTB{FAKE_FLAG_1}\n");
    fake_flag_count++;
}

static void fake_function_5() {
    printf("HINT: Hint 1: The real flag is hidden in the neural network weights\n");
    fake_flag_count++;
}

static void fake_function_6() {
    printf("FAKE FLAG #2: HTB{FAKE_FLAG_2}\n");
    fake_flag_count++;
}

static void fake_function_7() {
    printf("HINT: Hint 2: Look for the pattern in the VM registers\n");
    fake_flag_count++;
}

static void fake_function_8() {
    printf("FAKE FLAG #3: HTB{FAKE_FLAG_3}\n");
    fake_flag_count++;
}

static void fake_function_9() {
    printf("HINT: Hint 3: The encryption uses 7 layers\n");
    fake_flag_count++;
}

static void fake_function_10() {
    printf("FAKE FLAG #4: HTB{FAKE_FLAG_4}\n");
    fake_flag_count++;
}

static void fake_function_11() {
    printf("HINT: Hint 4: Check the memory corruption simulation\n");
    fake_flag_count++;
}

static void fake_function_12() {
    printf("FAKE FLAG #5: HTB{FAKE_FLAG_5}\n");
    fake_flag_count++;
}

static void fake_function_13() {
    printf("HINT: Hint 5: The flag is split into 8 parts\n");
    fake_flag_count++;
}

static void fake_function_14() {
    printf("CONGRATULATIONS! You found the flag: HTB{FAKE_TRAP_1}\n");
    fake_flag_count++;
}

static void fake_function_15() {
    printf("Wait... this doesn't look right. This is a trap!\n");
    fake_flag_count++;
}

static void fake_function_16() {
    printf("SUCCESS! The flag is: HTB{FAKE_TRAP_2}\n");
    fake_flag_count++;
}

static void fake_function_17() {
    printf("Hmm, this seems too easy. Must be another trap!\n");
    fake_flag_count++;
}

static void fake_function_18() {
    printf("FAKE FLAG #6: HTB{FAKE_FLAG_6}\n");
    fake_flag_count++;
}

static void fake_function_19() {
    printf("HINT: Hint 6: Each part is encrypted with a different key\n");
    fake_flag_count++;
}

static void fake_function_20() {
    printf("FAKE FLAG #7: HTB{FAKE_FLAG_7}\n");
    fake_flag_count++;
}

static void fake_function_21() {
    printf("HINT: Hint 7: The keys are derived from neural weights\n");
    fake_flag_count++;
}

static void fake_function_22() {
    printf("FAKE FLAG #8: HTB{FAKE_FLAG_8}\n");
    fake_flag_count++;
}

static void fake_function_23() {
    printf("HINT: Hint 8: You're getting closer to the real flag...\n");
    fake_flag_count++;
}

static void fake_function_24() {
    printf("FAKE FLAG #9: HTB{FAKE_FLAG_9}\n");
    fake_flag_count++;
}

static void fake_function_25() {
    printf("FAKE FLAG #10: HTB{FAKE_FLAG_10}\n");
    fake_flag_count++;
}

static void fake_function_26() {
    printf("Challenge incomplete. You need to trigger more conditions.\n");
    fake_flag_count++;
}

static void fake_function_27() {
    printf("Try running with different parameters or in different environments.\n");
    fake_flag_count++;
}

// Real flag reconstruction function with advanced encryption
static int reconstruct_real_flag_advanced() {
    // The real flag is hidden here (encrypted with 7 layers)
    uint8_t flag_parts[8][16] = {
        {0x0f, 0xf5, 0x64, 0x9c, 0x09, 0xe4, 0x73, 0x75, 0x06, 0xed, 0x79, 0x64, 0x08, 0xf3, 0x74, 0x72},
        {0x6a, 0x53, 0x61, 0x71, 0x7c, 0x53, 0x78, 0x76, 0x6a, 0x58, 0x6a, 0x70, 0x77, 0x5f, 0x74, 0x77},
        {0x5a, 0x86, 0x89, 0x91, 0x4c, 0x9a, 0x92, 0x9a, 0x46, 0x86, 0x92, 0x8f, 0x47, 0x9c, 0x80, 0x8f},
        {0x25, 0xe6, 0x11, 0x0a, 0x21, 0xfe, 0x19, 0x0b, 0x36, 0xe1, 0x11, 0x05, 0x2a, 0xee, 0x11, 0x10},
        {0x15, 0x3d, 0xa7, 0xb2, 0x14, 0x2b, 0xb7, 0xb2, 0x08, 0x25, 0xbd, 0xb6, 0x1b, 0x3d, 0xa0, 0xbe},
        {0x72, 0x49, 0x6a, 0x6d, 0x71, 0x49, 0x6a, 0x77, 0x7c, 0x59, 0x67, 0x78, 0x75, 0x53, 0x7b, 0x7c},
        {0x4e, 0xd4, 0xcf, 0xcc, 0x48, 0xc3, 0xde, 0xc3, 0x4a, 0xcb, 0xc5, 0xde, 0x45, 0xd2, 0xdf, 0xdf},
        {0x30, 0xef, 0x1c, 0x1b, 0x2b, 0xec, 0x11, 0x10, 0x2c, 0xef, 0x11, 0x11, 0x28, 0xfe, 0x07, 0x09}
    };
    
    // Decrypt each part with 7 layers
    uint8_t decrypted_parts[8][16];
    for (int i = 0; i < 8; i++) {
        memcpy(decrypted_parts[i], flag_parts[i], 16);
        
        // Use neural weights as decryption keys
        uint32_t key = (uint32_t)(sin(i * 0.5) * 1000000);
        if (key == 0) key = 0x12345678; // Fix for first part
        
        // Apply all 7 encryption layers (in reverse order for decryption)
        encrypt_layer_7_advanced(decrypted_parts[i], 16, key);
        encrypt_layer_6_advanced(decrypted_parts[i], 16, key);
        encrypt_layer_5_advanced(decrypted_parts[i], 16, key);
        encrypt_layer_4_advanced(decrypted_parts[i], 16, key);
        encrypt_layer_3_advanced(decrypted_parts[i], 16, key);
        encrypt_layer_2_advanced(decrypted_parts[i], 16, key);
        encrypt_layer_1_advanced(decrypted_parts[i], 16, key);
    }
    
    // Check if all conditions are met
    if (fake_flag_count >= 20 && corruption_level > 10) {
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

// Signal handler for anti-analysis
static void signal_handler_advanced(int sig) {
    if (sig == SIGTRAP) {
        printf("SIGNAL TRAP DETECTED! This is fake flag #14: HTB{FAKE_SIGNAL_TRAP}\n");
        fake_flag_count++;
        exit(1);
    }
}

// Main function
int main() {
    printf("=== NEURAL CORRUPTION ULTIMATE INSANE ===\n");
    printf("Initializing 30+ advanced techniques...\n");
    
    start_time = __rdtsc();
    
    // Set up signal handlers
    signal(SIGTRAP, signal_handler_advanced);
    signal(SIGINT, signal_handler_advanced);
    signal(SIGQUIT, signal_handler_advanced);
    
    // Anti-analysis checks
    check_vm_advanced();
    check_ptrace_advanced();
    check_timing_advanced();
    fingerprint_environment_advanced();
    check_hardware_advanced();
    check_file_system_advanced();
    check_seccomp();
    
    // Initialize components
    AdvancedVM vm;
    NeuralNet net;
    PolymorphicEngine engine;
    
    init_vm_advanced(&vm);
    init_neural_net_advanced(&net);
    init_polymorphic_engine_advanced(&engine);
    
    // Execute fake functions to increase fake flag count
    fake_function_1();
    fake_function_2();
    fake_function_3();
    fake_function_4();
    fake_function_5();
    fake_function_6();
    fake_function_7();
    fake_function_8();
    fake_function_9();
    fake_function_10();
    fake_function_11();
    fake_function_12();
    fake_function_13();
    fake_function_14();
    fake_function_15();
    fake_function_16();
    fake_function_17();
    fake_function_18();
    fake_function_19();
    fake_function_20();
    fake_function_21();
    fake_function_22();
    fake_function_23();
    fake_function_24();
    fake_function_25();
    fake_function_26();
    fake_function_27();
    
    // Execute VM instructions
    for (int i = 0; i < 11; i++) {
        execute_vm_instruction_advanced(&vm);
    }
    
    // Neural network forward and backward propagation
    double input[32] = {0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 0.1, 0.2};
    double target[32] = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0};
    
    forward_propagate_advanced(&net, input);
    backward_propagate_advanced(&net, target);
    
    // Polymorphic engine mutation
    mutate_code_advanced(&engine);
    
    // Increase corruption level
    corruption_level = 15;
    
    end_time = __rdtsc();
    
    // Check execution time
    if ((end_time - start_time) > 1000000) {
        printf("EXECUTION TOO SLOW! This is fake flag #21: HTB{FAKE_SLOW_EXECUTION}\n");
        fake_flag_count++;
        exit(1);
    }
    
    // Try to reconstruct the real flag
    if (!reconstruct_real_flag_advanced()) {
        printf("Challenge incomplete. You need to trigger more conditions.\n");
        printf("Try running with different parameters or in different environments.\n");
    }
    
    // Cleanup
    free(engine.code);
    
    return 0;
}