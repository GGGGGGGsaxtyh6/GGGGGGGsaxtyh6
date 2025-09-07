#ifndef QUANTUM_CONFIG_H
#define QUANTUM_CONFIG_H

// Quantum Paradox Challenge Configuration
// This file contains obfuscated configuration data

// Obfuscated string constants
#define OBFUSCATED_STRING_1 "\x48\x65\x6c\x6c\x6f\x20\x57\x6f\x72\x6c\x64"
#define OBFUSCATED_STRING_2 "\x51\x75\x61\x6e\x74\x75\x6d\x20\x50\x61\x72\x61\x64\x6f\x78"
#define OBFUSCATED_STRING_3 "\x46\x6c\x61\x67\x20\x66\x6f\x75\x6e\x64"
#define OBFUSCATED_STRING_4 "\x49\x6e\x76\x61\x6c\x69\x64\x20\x69\x6e\x70\x75\x74"
#define OBFUSCATED_STRING_5 "\x44\x65\x62\x75\x67\x67\x65\x72\x20\x64\x65\x74\x65\x63\x74\x65\x64"

// XOR key for deobfuscation
#define XOR_KEY 0x42

// Fake flag constants (DO NOT SUBMIT THESE!)
#define FAKE_FLAG_1 "HTB{f4k3_fl4g_1_qu4ntum_3rr0r}"
#define FAKE_FLAG_2 "HTB{f4k3_fl4g_2_paradox}"
#define FAKE_FLAG_3 "HTB{qu4ntum_3nt4ngl3m3nt_s0lv3d}"
#define FAKE_FLAG_4 "HTB{asm_puzzle_1_solved}"
#define FAKE_FLAG_5 "HTB{crypto_analysis_complete}"

// Obfuscated fake flags
#define OBFUSCATED_FAKE_FLAG_1 "\x48\x54\x42\x7b\x66\x34\x6b\x33\x5f\x66\x6c\x34\x67\x5f\x31\x5f\x71\x75\x34\x6e\x74\x75\x6d\x5f\x33\x72\x72\x30\x72\x7d"
#define OBFUSCATED_FAKE_FLAG_2 "\x48\x54\x42\x7b\x66\x34\x6b\x33\x5f\x66\x6c\x34\x67\x5f\x32\x5f\x70\x61\x72\x61\x64\x6f\x78\x7d"
#define OBFUSCATED_FAKE_FLAG_3 "\x48\x54\x42\x7b\x71\x75\x34\x6e\x74\x75\x6d\x5f\x33\x6e\x74\x34\x6e\x67\x6c\x33\x6d\x33\x6e\x74\x5f\x73\x30\x6c\x76\x33\x64\x7d"

// Quantum state constants
#define QUANTUM_STATE_0 0x00
#define QUANTUM_STATE_1 0x01
#define QUANTUM_STATE_PLUS 0x02
#define QUANTUM_STATE_MINUS 0x03
#define QUANTUM_STATE_I 0x04
#define QUANTUM_STATE_MINUS_I 0x05

// Anti-debugging constants
#define ANTI_DEBUG_MAGIC_1 0xDEADBEEF
#define ANTI_DEBUG_MAGIC_2 0xCAFEBABE
#define ANTI_DEBUG_MAGIC_3 0xFEEDFACE

// Memory obfuscation constants
#define MEMORY_OBFUSCATION_KEY_1 0xAA
#define MEMORY_OBFUSCATION_KEY_2 0x55
#define MEMORY_OBFUSCATION_KEY_3 0x33

// Function obfuscation constants
#define FUNCTION_OBFUSCATION_OFFSET 0x1000
#define FUNCTION_OBFUSCATION_MULTIPLIER 0x1337

// String obfuscation macros
#define OBFUSCATE_STRING(str) \
    do { \
        for (int i = 0; str[i] != '\0'; i++) { \
            str[i] ^= XOR_KEY; \
        } \
    } while(0)

#define DEOBFUSCATE_STRING(str) \
    do { \
        for (int i = 0; str[i] != '\0'; i++) { \
            str[i] ^= XOR_KEY; \
        } \
    } while(0)

// Memory obfuscation macros
#define OBFUSCATE_MEMORY(ptr, size, key) \
    do { \
        for (int i = 0; i < size; i++) { \
            ((char*)ptr)[i] ^= key; \
        } \
    } while(0)

// Anti-debugging macros
#define CHECK_DEBUGGER() \
    do { \
        if (IsDebuggerPresent()) { \
            exit(1); \
        } \
    } while(0)

#define ANTI_DEBUG_TRAP() \
    __asm__("int3")

// Quantum operation macros
#define QUANTUM_HADAMARD(state) \
    do { \
        state = (state == QUANTUM_STATE_0) ? QUANTUM_STATE_PLUS : QUANTUM_STATE_MINUS; \
    } while(0)

#define QUANTUM_PAULI_X(state) \
    do { \
        state = (state == QUANTUM_STATE_0) ? QUANTUM_STATE_1 : QUANTUM_STATE_0; \
    } while(0)

#define QUANTUM_PAULI_Z(state) \
    do { \
        state = (state == QUANTUM_STATE_PLUS) ? QUANTUM_STATE_MINUS : QUANTUM_STATE_PLUS; \
    } while(0)

// Fake quantum algorithm constants
#define QUANTUM_ALGORITHM_STEPS 7
#define QUANTUM_ALGORITHM_QUBITS 8
#define QUANTUM_ALGORITHM_DEPTH 20

// Obfuscated function pointers
typedef void (*obfuscated_func_t)(void);
extern obfuscated_func_t obfuscated_functions[];

// Obfuscated data structures
typedef struct {
    int magic;
    char obfuscated_data[256];
    int checksum;
} obfuscated_data_t;

typedef struct {
    int quantum_state;
    char fake_flag[64];
    int obfuscation_key;
} quantum_particle_t;

// Global obfuscated data
extern obfuscated_data_t global_obfuscated_data;
extern quantum_particle_t quantum_particles[QUANTUM_ALGORITHM_QUBITS];

// Function declarations for obfuscated functions
void obfuscated_function_1(void);
void obfuscated_function_2(void);
void obfuscated_function_3(void);
void obfuscated_function_4(void);
void obfuscated_function_5(void);

// Quantum algorithm functions
void quantum_algorithm_step_1(void);
void quantum_algorithm_step_2(void);
void quantum_algorithm_step_3(void);
void quantum_algorithm_step_4(void);
void quantum_algorithm_step_5(void);
void quantum_algorithm_step_6(void);
void quantum_algorithm_step_7(void);

// Memory analysis functions
void analyze_memory_patterns(void);
void extract_fake_flags(void);
void obfuscate_memory_region(void* ptr, size_t size);

// Anti-debugging functions
bool check_debugger_presence(void);
void anti_debug_trap(void);
void obfuscate_function_pointers(void);

// String obfuscation functions
void obfuscate_strings(void);
void deobfuscate_strings(void);
char* get_obfuscated_string(int index);

// Quantum state functions
void initialize_quantum_states(void);
void apply_quantum_gates(void);
void measure_quantum_states(void);
void extract_quantum_flag(void);

// Utility functions
int calculate_checksum(void* data, size_t size);
void validate_obfuscated_data(void);
void cleanup_obfuscated_data(void);

#endif // QUANTUM_CONFIG_H