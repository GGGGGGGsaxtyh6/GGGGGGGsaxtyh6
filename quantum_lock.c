/*
 * QUANTUM_LOCK - INSANE Reversing Challenge
 * 
 * This is a quantum security device simulator that requires
 * a valid quantum key to unlock the system.
 * 
 * Difficulty: INSANE
 * Techniques: VM Obfuscation, Polymorphic Code, Anti-Analysis
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <time.h>
#include <sys/time.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <signal.h>
#include <setjmp.h>
#include <stdint.h>
#include <x86intrin.h>
#include <sys/ptrace.h>
#include <sys/wait.h>

// Quantum VM State
typedef struct {
    uint32_t regs[16];        // Quantum registers
    uint8_t *memory;          // VM memory space
    uint32_t pc;              // Program counter
    uint32_t sp;              // Stack pointer
    uint8_t flags;            // Status flags
    uint32_t quantum_state;   // Current quantum state
} quantum_vm_t;

// Anti-analysis structures
typedef struct {
    uint64_t start_time;
    uint64_t last_check;
    uint32_t instruction_count;
    uint8_t debug_detected;
    uint8_t vm_detected;
    uint8_t timing_anomaly;
} anti_analysis_t;

// Global state
static quantum_vm_t vm;
static anti_analysis_t anti_analysis;
static jmp_buf quantum_exit;
static uint8_t *polymorphic_buffer;
static uint32_t poly_size;

// Quantum constants (these are the key fragments)
static const uint32_t QUANTUM_CONSTANTS[] = {
    0xDEADBEEF, 0xCAFEBABE, 0xFEEDFACE, 0xBADDCAFE,
    0x1337C0DE, 0xDEADC0DE, 0xFEEDBEEF, 0xCAFEDEAD
};

// VM Instruction opcodes (obfuscated)
#define QVM_NOP     0x00
#define QVM_LOAD    0x01
#define QVM_STORE   0x02
#define QVM_ADD     0x03
#define QVM_XOR     0x04
#define QVM_ROT     0x05
#define QVM_CMP     0x06
#define QVM_JMP     0x07
#define QVM_CALL    0x08
#define QVM_RET     0x09
#define QVM_QUANTUM 0x0A
#define QVM_ENTANGLE 0x0B
#define QVM_MEASURE 0x0C
#define QVM_COLLAPSE 0x0D
#define QVM_VERIFY  0x0E
#define QVM_HALT    0xFF

// Anti-analysis functions
static void init_anti_analysis() {
    anti_analysis.start_time = __rdtsc();
    anti_analysis.last_check = anti_analysis.start_time;
    anti_analysis.instruction_count = 0;
    anti_analysis.debug_detected = 0;
    anti_analysis.vm_detected = 0;
    anti_analysis.timing_anomaly = 0;
}

static void check_timing() {
    uint64_t current = __rdtsc();
    uint64_t elapsed = current - anti_analysis.last_check;
    
    // If too much time has passed, we're probably being debugged
    if (elapsed > 1000000) {  // Arbitrary threshold
        anti_analysis.timing_anomaly = 1;
        longjmp(quantum_exit, 1);
    }
    anti_analysis.last_check = current;
}

static void check_vm_environment() {
    // Check for VM artifacts
    FILE *fp = fopen("/proc/cpuinfo", "r");
    if (fp) {
        char line[256];
        while (fgets(line, sizeof(line), fp)) {
            if (strstr(line, "hypervisor") || strstr(line, "vmware") || 
                strstr(line, "virtualbox") || strstr(line, "qemu")) {
                anti_analysis.vm_detected = 1;
                fclose(fp);
                longjmp(quantum_exit, 1);
            }
        }
        fclose(fp);
    }
    
    // Check for debugger
    if (ptrace(PTRACE_TRACEME, 0, 1, 0) == -1) {
        anti_analysis.debug_detected = 1;
        longjmp(quantum_exit, 1);
    }
}

// Load the real quantum bytecode
static void load_quantum_bytecode() {
    FILE *fp = fopen("quantum_bytecode.bin", "rb");
    if (!fp) {
        // Generate bytecode if file doesn't exist
        printf("Bytecode not found. Generating...\n");
        (void)system("gcc -o bytecode_gen bytecode_generator.c && ./bytecode_gen");
        fp = fopen("quantum_bytecode.bin", "rb");
    }
    
    if (fp) {
        fseek(fp, 0, SEEK_END);
        poly_size = ftell(fp);
        fseek(fp, 0, SEEK_SET);
        
        polymorphic_buffer = malloc(poly_size);
        (void)fread(polymorphic_buffer, 1, poly_size, fp);
        fclose(fp);
        
        printf("Loaded quantum bytecode (%d bytes)\n", poly_size);
    } else {
        printf("Failed to load bytecode. Using fallback.\n");
        poly_size = 1024;
        polymorphic_buffer = malloc(poly_size);
        memset(polymorphic_buffer, 0, poly_size);
    }
}

// Quantum VM implementation
static void init_quantum_vm() {
    vm.memory = malloc(65536);  // 64KB VM memory
    vm.pc = 0;
    vm.sp = 65535;
    vm.flags = 0;
    vm.quantum_state = 0;
    
    // Initialize registers with quantum constants
    for (int i = 0; i < 8; i++) {
        vm.regs[i] = QUANTUM_CONSTANTS[i];
    }
    
    // Clear remaining registers
    for (int i = 8; i < 16; i++) {
        vm.regs[i] = 0;
    }
}

static void quantum_entangle(uint32_t reg1, uint32_t reg2) {
    // Simulate quantum entanglement
    vm.regs[reg1] ^= vm.regs[reg2];
    vm.regs[reg2] ^= vm.regs[reg1];
    vm.regs[reg1] ^= vm.regs[reg2];
    vm.quantum_state |= (1 << reg1) | (1 << reg2);
}

static void quantum_measure(uint32_t reg) {
    // Quantum measurement collapses the state
    if (vm.quantum_state & (1 << reg)) {
        vm.regs[reg] = (vm.regs[reg] << 1) | (vm.regs[reg] >> 31);
        vm.quantum_state &= ~(1 << reg);
    }
}

// Multi-stage decryption
static void decrypt_stage1(uint8_t *data, uint32_t len, uint32_t key) {
    for (uint32_t i = 0; i < len; i++) {
        data[i] ^= (key >> ((i % 4) * 8)) & 0xFF;
        key = (key << 1) | (key >> 31);
    }
}

static void decrypt_stage2(uint8_t *data, uint32_t len, uint32_t key) {
    for (uint32_t i = 0; i < len; i++) {
        data[i] = ((data[i] - (key & 0xFF)) + 256) % 256;
        key = (key * 1103515245 + 12345) & 0xFFFFFFFF;
    }
}

static void decrypt_stage3(uint8_t *data, uint32_t len, uint32_t key) {
    for (uint32_t i = 0; i < len; i++) {
        data[i] ^= ((key >> 8) & 0xFF) ^ ((key >> 16) & 0xFF) ^ ((key >> 24) & 0xFF);
        key = key ^ (key << 13) ^ (key >> 19);
    }
}

// Simple XOR decryption for testing
static void simple_decrypt(uint8_t *data, uint32_t len, uint32_t key) {
    for (uint32_t i = 0; i < len; i++) {
        data[i] ^= (key >> ((i % 4) * 8)) & 0xFF;
    }
}

// Flag reconstruction
static int reconstruct_flag() {
    // The flag is split into 4 parts, each encrypted with different quantum keys
    uint8_t flag_part1[] = {0x19, 0x50, 0x11, 0x6F, 0x00, 0x51, 0x12, 0x5A, 0x05, 0x51, 0x1E, 0x4B, 0x00};
    uint8_t flag_part2[] = {0x7C, 0x7F, 0x73, 0x0F, 0x6F, 0x79, 0x63, 0x1B, 0x72, 0x62, 0x7F, 0x0F, 0x75, 0x7E, 0x00};
    uint8_t flag_part3[] = {0x5F, 0x42, 0xC3, 0x92, 0x54, 0x48, 0xDF, 0x92, 0x52, 0x45, 0xCC, 0x88, 0x52, 0x53, 0xDF, 0x9F, 0x00};
    uint8_t flag_part4[] = {0x1D, 0x2D, 0x52, 0x67, 0x16, 0x25, 0x41, 0x49, 0x00};
    
    // Decrypt each part with quantum keys derived from registers
    uint32_t key1 = vm.regs[0] ^ vm.regs[1];
    uint32_t key2 = vm.regs[2] ^ vm.regs[3];
    uint32_t key3 = vm.regs[4] ^ vm.regs[5];
    uint32_t key4 = vm.regs[6] ^ vm.regs[7];
    
    // Create copies for decryption
    uint8_t decrypted1[sizeof(flag_part1)];
    uint8_t decrypted2[sizeof(flag_part2)];
    uint8_t decrypted3[sizeof(flag_part3)];
    uint8_t decrypted4[sizeof(flag_part4)];
    
    memcpy(decrypted1, flag_part1, sizeof(flag_part1));
    memcpy(decrypted2, flag_part2, sizeof(flag_part2));
    memcpy(decrypted3, flag_part3, sizeof(flag_part3));
    memcpy(decrypted4, flag_part4, sizeof(flag_part4));
    
    simple_decrypt(decrypted1, sizeof(flag_part1) - 1, key1);
    simple_decrypt(decrypted2, sizeof(flag_part2) - 1, key2);
    simple_decrypt(decrypted3, sizeof(flag_part3) - 1, key3);
    simple_decrypt(decrypted4, sizeof(flag_part4) - 1, key4);
    
    // Final verification - all quantum states must be collapsed
    if (vm.quantum_state == 0) {
        printf("QUANTUM LOCK UNLOCKED!\n");
        printf("Flag: %s%s%s%s\n", decrypted1, decrypted2, decrypted3, decrypted4);
        return 1;
    }
    
    return 0;
}

// VM instruction execution
static int execute_vm_instruction(uint8_t opcode, uint32_t operand1, uint32_t operand2) {
    anti_analysis.instruction_count++;
    
    // Debug output (commented out for release)
    // if (anti_analysis.instruction_count <= 10) {
    //     printf("Executing instruction %d: opcode=0x%02X, op1=0x%08X, op2=0x%08X\n", 
    //            anti_analysis.instruction_count, opcode, operand1, operand2);
    // }
    
    // Anti-analysis checks every 100 instructions
    if (anti_analysis.instruction_count % 100 == 0) {
        check_timing();
        check_vm_environment();
    }
    
    switch (opcode) {
        case QVM_NOP:
            break;
            
        case QVM_LOAD:
            vm.regs[operand1 & 0xF] = operand2;
            break;
            
        case QVM_STORE:
            *(uint32_t*)(vm.memory + (operand1 & 0xFFFF)) = vm.regs[operand2 & 0xF];
            break;
            
        case QVM_ADD:
            vm.regs[operand1 & 0xF] += vm.regs[operand2 & 0xF];
            break;
            
        case QVM_XOR:
            vm.regs[operand1 & 0xF] ^= vm.regs[operand2 & 0xF];
            break;
            
        case QVM_ROT:
            vm.regs[operand1 & 0xF] = (vm.regs[operand1 & 0xF] << (operand2 & 0x1F)) | 
                                     (vm.regs[operand1 & 0xF] >> (32 - (operand2 & 0x1F)));
            break;
            
        case QVM_CMP:
            vm.flags = (vm.regs[operand1 & 0xF] == vm.regs[operand2 & 0xF]) ? 1 : 0;
            break;
            
        case QVM_JMP:
            if (vm.flags) {
                vm.pc = operand1;
            }
            break;
            
        case QVM_CALL:
            vm.memory[vm.sp--] = vm.pc;
            vm.pc = operand1;
            break;
            
        case QVM_RET:
            vm.pc = vm.memory[++vm.sp];
            break;
            
        case QVM_QUANTUM:
            vm.quantum_state ^= (1 << (operand1 & 0xF));
            break;
            
        case QVM_ENTANGLE:
            quantum_entangle(operand1 & 0xF, operand2 & 0xF);
            break;
            
        case QVM_MEASURE:
            quantum_measure(operand1 & 0xF);
            break;
            
        case QVM_COLLAPSE:
            vm.quantum_state = 0;
            break;
            
        case QVM_VERIFY:
            return reconstruct_flag();
            
        case QVM_HALT:
            return -1;
            
        default:
            // Unknown instruction - crash the VM
            return -1;
    }
    
    return 0;
}

// Main quantum lock program
static void quantum_lock_main() {
    printf("=== QUANTUM LOCK SECURITY SYSTEM ===\n");
    printf("Initializing quantum entanglement protocols...\n");
    
    // Initialize everything
    init_anti_analysis();
    init_quantum_vm();
    load_quantum_bytecode();
    
    // Set up signal handler for anti-debugging
    signal(SIGTRAP, SIG_IGN);
    signal(SIGINT, SIG_IGN);
    
    printf("Quantum VM initialized. Entering secure mode...\n");
    
    // Main VM execution loop
    uint8_t *bytecode = (uint8_t*)polymorphic_buffer;
    uint32_t instruction_count = 0;
    
    while (vm.pc < poly_size && instruction_count < 10000) {
        uint8_t opcode = bytecode[vm.pc++];
        uint32_t operand1 = 0, operand2 = 0;
        
        // Read operands based on instruction type
        switch (opcode) {
            case QVM_LOAD:
            case QVM_STORE:
            case QVM_ROT:
            case QVM_CMP:
            case QVM_JMP:
            case QVM_CALL:
            case QVM_QUANTUM:
            case QVM_MEASURE:
                operand1 = *(uint32_t*)(bytecode + vm.pc);
                vm.pc += 4;
                operand2 = *(uint32_t*)(bytecode + vm.pc);
                vm.pc += 4;
                break;
                
            case QVM_ENTANGLE:
            case QVM_ADD:
            case QVM_XOR:
                operand1 = *(uint32_t*)(bytecode + vm.pc);
                vm.pc += 4;
                operand2 = *(uint32_t*)(bytecode + vm.pc);
                vm.pc += 4;
                break;
                
            case QVM_NOP:
            case QVM_RET:
            case QVM_COLLAPSE:
            case QVM_VERIFY:
            case QVM_HALT:
                // No operands
                break;
                
            default:
                // Unknown instruction - skip it
                vm.pc++;
                continue;
        }
        
        int result = execute_vm_instruction(opcode, operand1, operand2);
        if (result == 1) {
            // Flag found!
            break;
        } else if (result == -1) {
            printf("Quantum system error. Shutting down...\n");
            break;
        }
        
        instruction_count++;
    }
    
    if (instruction_count >= 10000) {
        printf("Quantum timeout. System locked.\n");
    }
}

// Entry point with anti-debugging
int main(int argc, char *argv[]) {
    // Anti-debugging: check if we're being traced
    if (ptrace(PTRACE_TRACEME, 0, 1, 0) == -1) {
        printf("Debugging detected. Quantum lock engaged.\n");
        exit(1);
    }
    
    // Set up quantum exit handler
    if (setjmp(quantum_exit)) {
        printf("Quantum anomaly detected. System self-destructing...\n");
        exit(1);
    }
    
    // Seed random number generator
    srand(time(NULL) ^ getpid());
    
    // Run the quantum lock
    quantum_lock_main();
    
    // Cleanup
    if (vm.memory) free(vm.memory);
    if (polymorphic_buffer) free(polymorphic_buffer);
    
    return 0;
}