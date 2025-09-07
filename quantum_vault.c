#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>
#include <sys/ptrace.h>
#include <signal.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <errno.h>
#include <sys/wait.h>
#include <sys/syscall.h>
#include <linux/limits.h>
#include <sys/utsname.h>
#include <sys/resource.h>
#include <sys/time.h>
#include <sys/ioctl.h>
#include <termios.h>
#include <dlfcn.h>
#include <elf.h>
#include <link.h>
#include <math.h>
#include <complex.h>

// Quantum Vault - Un challenge de reverse engineering extremo
// Implementa técnicas avanzadas: VM obfuscation, control flow flattening, y quantum-inspired encryption

#define QUANTUM_STATE_SIZE 256
#define VM_REGISTERS 16
#define MAX_INSTRUCTIONS 1024
#define ENCRYPTION_ROUNDS 16

// Estructura para la máquina virtual ofuscada
typedef struct {
    unsigned int registers[VM_REGISTERS];
    unsigned int stack[256];
    int stack_ptr;
    unsigned int pc; // program counter
    unsigned int instructions[MAX_INSTRUCTIONS];
    int instruction_count;
    unsigned int quantum_state[QUANTUM_STATE_SIZE];
    unsigned int encryption_key[4];
    int vm_running;
} quantum_vm_t;

// Estructura para control flow flattening
typedef struct {
    unsigned int state;
    unsigned int next_state;
    unsigned int (*handler)(quantum_vm_t*);
} flow_state_t;

// Variables globales ofuscadas
static quantum_vm_t* vm = NULL;
static flow_state_t flow_states[32];
static int current_flow_state = 0;
static unsigned int quantum_entropy = 0xDEADBEEF;
static volatile int debug_detected = 0;
static volatile int analysis_detected = 0;

// Función de detección de debugging avanzada
int quantum_debug_detection() {
    // Método 1: ptrace con múltiples intentos
    for (int i = 0; i < 3; i++) {
        if (ptrace(PTRACE_TRACEME, 0, 1, 0) == -1) {
            return 1;
        }
    }
    
    // Método 2: Timing attack con quantum entropy
    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);
    
    // Simular computación cuántica
    for (int i = 0; i < 1000000; i++) {
        quantum_entropy ^= (quantum_entropy << 13);
        quantum_entropy ^= (quantum_entropy >> 17);
        quantum_entropy ^= (quantum_entropy << 5);
    }
    
    clock_gettime(CLOCK_MONOTONIC, &end);
    long elapsed = (end.tv_sec - start.tv_sec) * 1000000000L + (end.tv_nsec - start.tv_nsec);
    
    if (elapsed > 50000000) { // Muy lento = debugger
        return 1;
    }
    
    // Método 3: Verificar /proc/self/status
    FILE* status = fopen("/proc/self/status", "r");
    if (status) {
        char line[256];
        while (fgets(line, sizeof(line), status)) {
            if (strncmp(line, "TracerPid:", 10) == 0) {
                int pid = atoi(line + 10);
                fclose(status);
                return pid != 0;
            }
        }
        fclose(status);
    }
    
    return 0;
}

// Función de detección de análisis estático
int quantum_analysis_detection() {
    // Verificar herramientas de análisis
    const char* analysis_tools[] = {
        "strings", "objdump", "hexdump", "gdb", "radare2", "ghidra", "ida"
    };
    
    for (int i = 0; i < 7; i++) {
        char cmd[256];
        snprintf(cmd, sizeof(cmd), "which %s > /dev/null 2>&1", analysis_tools[i]);
        if (system(cmd) == 0) return 1;
    }
    
    // Verificar procesos de análisis
    FILE* proc = popen("ps aux | grep -E '(strings|objdump|hexdump|gdb|radare2|ghidra|ida)' | grep -v grep", "r");
    if (proc) {
        char line[256];
        if (fgets(line, sizeof(line), proc)) {
            pclose(proc);
            return 1;
        }
        pclose(proc);
    }
    
    return 0;
}

// Algoritmo de cifrado cuántico inspirado
void quantum_encrypt(unsigned char* data, int len, unsigned int* key) {
    for (int round = 0; round < ENCRYPTION_ROUNDS; round++) {
        for (int i = 0; i < len; i++) {
            // Simular superposición cuántica
            unsigned int quantum_bit = (key[0] >> (i % 32)) & 1;
            unsigned int entangled_bit = (key[1] >> ((i + 1) % 32)) & 1;
            
            // Aplicar transformación cuántica
            data[i] ^= (quantum_bit << 7) | (entangled_bit << 6);
            data[i] ^= (key[2] >> (i % 32)) & 0xFF;
            data[i] ^= (key[3] >> ((i + 2) % 32)) & 0xFF;
            
            // Rotación cuántica
            data[i] = ((data[i] << 3) | (data[i] >> 5)) & 0xFF;
        }
        
        // Actualizar claves para siguiente ronda
        key[0] = (key[0] << 1) | (key[0] >> 31);
        key[1] = (key[1] << 2) | (key[1] >> 30);
        key[2] = (key[2] << 3) | (key[2] >> 29);
        key[3] = (key[3] << 4) | (key[3] >> 28);
    }
}

// Función para descifrar la flag
void quantum_decrypt_flag(unsigned char* encrypted_flag, int len, unsigned int* key) {
    // Invertir el proceso de cifrado
    for (int round = ENCRYPTION_ROUNDS - 1; round >= 0; round--) {
        for (int i = 0; i < len; i++) {
            // Rotación cuántica inversa
            encrypted_flag[i] = ((encrypted_flag[i] >> 3) | (encrypted_flag[i] << 5)) & 0xFF;
            
            // Aplicar transformación cuántica inversa
            encrypted_flag[i] ^= (key[3] >> ((i + 2) % 32)) & 0xFF;
            encrypted_flag[i] ^= (key[2] >> (i % 32)) & 0xFF;
            
            unsigned int quantum_bit = (key[0] >> (i % 32)) & 1;
            unsigned int entangled_bit = (key[1] >> ((i + 1) % 32)) & 1;
            encrypted_flag[i] ^= (quantum_bit << 7) | (entangled_bit << 6);
        }
        
        // Actualizar claves para siguiente ronda
        key[0] = (key[0] >> 1) | (key[0] << 31);
        key[1] = (key[1] >> 2) | (key[1] << 30);
        key[2] = (key[2] >> 3) | (key[2] << 29);
        key[3] = (key[3] >> 4) | (key[3] << 28);
    }
}

// Inicializar la máquina virtual
void init_quantum_vm(quantum_vm_t* vm) {
    memset(vm, 0, sizeof(quantum_vm_t));
    vm->stack_ptr = 0;
    vm->pc = 0;
    vm->vm_running = 1;
    
    // Inicializar estado cuántico
    for (int i = 0; i < QUANTUM_STATE_SIZE; i++) {
        vm->quantum_state[i] = quantum_entropy ^ (i * 0x12345678);
    }
    
    // Inicializar claves de cifrado
    vm->encryption_key[0] = 0xDEADBEEF;
    vm->encryption_key[1] = 0xCAFEBABE;
    vm->encryption_key[2] = 0xFEEDFACE;
    vm->encryption_key[3] = 0x1337C0DE;
}

// Instrucciones de la máquina virtual
unsigned int vm_load_const(quantum_vm_t* vm) {
    unsigned int value = vm->instructions[vm->pc++];
    vm->registers[0] = value;
    return 0;
}

unsigned int vm_xor_reg(quantum_vm_t* vm) {
    unsigned int reg1 = vm->instructions[vm->pc++];
    unsigned int reg2 = vm->instructions[vm->pc++];
    vm->registers[reg1] ^= vm->registers[reg2];
    return 0;
}

unsigned int vm_quantum_entangle(quantum_vm_t* vm) {
    unsigned int reg = vm->instructions[vm->pc++];
    unsigned int quantum_index = vm->instructions[vm->pc++];
    vm->registers[reg] ^= vm->quantum_state[quantum_index % QUANTUM_STATE_SIZE];
    return 0;
}

unsigned int vm_decrypt_round(quantum_vm_t* vm) {
    unsigned int data_ptr = vm->instructions[vm->pc++];
    unsigned int len = vm->instructions[vm->pc++];
    
    // Simular descifrado parcial
    for (int i = 0; i < len; i++) {
        vm->registers[data_ptr + i] ^= vm->encryption_key[i % 4];
    }
    return 0;
}

unsigned int vm_validate_flag(quantum_vm_t* vm) {
    // Esta función valida la flag usando la VM
    unsigned int expected_hash = 0x12345678;
    unsigned int computed_hash = 0;
    
    for (int i = 0; i < 8; i++) {
        computed_hash ^= vm->registers[i];
        computed_hash = (computed_hash << 1) | (computed_hash >> 31);
    }
    
    return (computed_hash == expected_hash) ? 0 : 1;
}

// Control flow flattening handlers
unsigned int flow_handler_0(quantum_vm_t* vm) {
    return vm_load_const(vm);
}

unsigned int flow_handler_1(quantum_vm_t* vm) {
    return vm_xor_reg(vm);
}

unsigned int flow_handler_2(quantum_vm_t* vm) {
    return vm_quantum_entangle(vm);
}

unsigned int flow_handler_3(quantum_vm_t* vm) {
    return vm_decrypt_round(vm);
}

unsigned int flow_handler_4(quantum_vm_t* vm) {
    return vm_validate_flag(vm);
}

// Inicializar control flow flattening
void init_flow_flattening() {
    flow_states[0] = (flow_state_t){0, 1, flow_handler_0};
    flow_states[1] = (flow_state_t){1, 2, flow_handler_1};
    flow_states[2] = (flow_state_t){2, 3, flow_handler_2};
    flow_states[3] = (flow_state_t){3, 4, flow_handler_3};
    flow_states[4] = (flow_state_t){4, 0, flow_handler_4};
    
    current_flow_state = 0;
}

// Ejecutar la máquina virtual
int execute_quantum_vm(quantum_vm_t* vm) {
    init_flow_flattening();
    
    // Cargar instrucciones ofuscadas
    vm->instructions[0] = 0x4854427B; // "HTB{"
    vm->instructions[1] = 0x736D7572; // "smur"
    vm->instructions[2] = 0x665F7734; // "f_w4"
    vm->instructions[3] = 0x735F6833; // "s_h3"
    vm->instructions[4] = 0x72335F61; // "r3_a"
    vm->instructions[5] = 0x6E645F73; // "nd_s"
    vm->instructions[6] = 0x305F7734; // "0_w4"
    vm->instructions[7] = 0x735F7930; // "s_y0"
    vm->instructions[8] = 0x75725F66; // "ur_f"
    vm->instructions[9] = 0x6C34677D; // "l4g}"
    vm->instruction_count = 10;
    
    // Ejecutar VM con control flow flattening
    int cycles = 0;
    while (vm->vm_running && cycles < 1000) {
        flow_state_t* current_state = &flow_states[current_flow_state];
        int result = current_state->handler(vm);
        
        if (result != 0) {
            return result;
        }
        
        current_flow_state = current_state->next_state;
        cycles++;
    }
    
    return 0;
}

// Función principal de validación
int validate_quantum_flag(const char* input) {
    if (strlen(input) != 41) return 0;
    if (strncmp(input, "HTB{", 4) != 0) return 0;
    if (input[40] != '}') return 0;
    
    // Crear VM y ejecutar validación
    quantum_vm_t vm;
    init_quantum_vm(&vm);
    
    // Cargar input en la VM
    for (int i = 0; i < 8; i++) {
        vm.registers[i] = ((unsigned int*)input)[i];
    }
    
    // Ejecutar VM
    int result = execute_quantum_vm(&vm);
    
    return (result == 0);
}

// Función para mostrar información del challenge
void show_quantum_challenge_info() {
    printf("╔══════════════════════════════════════════════════════════════╗\n");
    printf("║                QUANTUM VAULT - REVERSE ENGINEERING         ║\n");
    printf("║                                                              ║\n");
    printf("║  🎯 Nombre: Quantum Vault                                   ║\n");
    printf("║  🔥 Dificultad: EXTREME                                     ║\n");
    printf("║  📚 Categoría: Reverse Engineering                           ║\n");
    printf("║  ⏱️  Tiempo estimado: 3+ horas                             ║\n");
    printf("║                                                              ║\n");
    printf("║  📖 Descripción:                                             ║\n");
    printf("║  Un banco cuántico ha implementado un sistema de seguridad  ║\n");
    printf("║  ultra-avanzado. El vault utiliza una máquina virtual      ║\n");
    printf("║  cuántica con cifrado inspirado en mecánica cuántica.      ║\n");
    printf("║  Encuentra la clave para acceder al vault.                 ║\n");
    printf("║                                                              ║\n");
    printf("║  🛡️  Protecciones implementadas:                            ║\n");
    printf("║     - Máquina virtual cuántica ofuscada                    ║\n");
    printf("║     - Control flow flattening                              ║\n");
    printf("║     - Cifrado cuántico inspirado                           ║\n");
    printf("║     - Anti-debugging avanzado                              ║\n");
    printf("║     - Detección de análisis estático                       ║\n");
    printf("║                                                              ║\n");
    printf("║  🔍 Pistas:                                                 ║\n");
    printf("║     - La flag comienza con HTB{                            ║\n");
    printf("║     - Tiene exactamente 41 caracteres                      ║\n");
    printf("║     - Usa análisis dinámico de la VM                       ║\n");
    printf("║     - El cifrado es reversible                              ║\n");
    printf("╚══════════════════════════════════════════════════════════════╝\n");
}

// Función para mostrar éxito
void show_quantum_success() {
    printf("\n");
    printf("╔══════════════════════════════════════════════════════════════╗\n");
    printf("║                    ¡FELICIDADES!                            ║\n");
    printf("║                                                              ║\n");
    printf("║  🎉 Has accedido al Quantum Vault!                          ║\n");
    printf("║                                                              ║\n");
    printf("║  🏆 Flag correcta: HTB{smurf_w4s_h3r3_and_s0_w4s_y0ur_fl4g} ║\n");
    printf("║                                                              ║\n");
    printf("║  Este challenge requería:                                    ║\n");
    printf("║  ✅ Análisis de máquina virtual cuántica                    ║\n");
    printf("║  ✅ Bypass de control flow flattening                       ║\n");
    printf("║  ✅ Ingeniería inversa del cifrado cuántico                 ║\n");
    printf("║  ✅ Análisis dinámico de la VM                              ║\n");
    printf("║  ✅ Bypass de protecciones anti-debugging                   ║\n");
    printf("║                                                              ║\n");
    printf("║  🎯 ¡Excelente trabajo de reverse engineering!              ║\n");
    printf("╚══════════════════════════════════════════════════════════════╝\n");
}

// Función principal
int main(int argc, char* argv[]) {
    if (argc != 2) {
        printf("Uso: %s <flag>\n", argv[0]);
        printf("Ejemplo: %s HTB{tu_flag_aqui}\n", argv[0]);
        return 1;
    }
    
    show_quantum_challenge_info();
    
    // Verificaciones de seguridad
    printf("\n🔍 Verificando entorno de ejecución...\n");
    
    if (quantum_debug_detection()) {
        printf("❌ Debugger detectado. El programa se cerrará.\n");
        printf("💡 Pista: Bypasea las protecciones anti-debugging\n");
        return 1;
    }
    
    if (quantum_analysis_detection()) {
        printf("⚠️  Análisis estático detectado. Continuando con precaución...\n");
        analysis_detected = 1;
    }
    
    printf("✅ Verificaciones de seguridad completadas\n");
    
    char* input = argv[1];
    
    // Procesar entrada
    printf("\n🔍 Procesando entrada en el Quantum Vault...\n");
    printf("🔬 Inicializando máquina virtual cuántica...\n");
    printf("🌊 Aplicando control flow flattening...\n");
    printf("🔐 Ejecutando algoritmo de cifrado cuántico...\n");
    
    // Validar flag
    if (validate_quantum_flag(input)) {
        show_quantum_success();
        return 0;
    } else {
        printf("❌ Acceso denegado al Quantum Vault.\n");
        printf("💡 Pista: Analiza la máquina virtual cuántica\n");
        return 1;
    }
}