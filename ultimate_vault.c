#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/ptrace.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <time.h>
#include <sys/mman.h>
#include <errno.h>
#include <signal.h>
#include <sys/wait.h>
#include <sys/prctl.h>
#include <linux/seccomp.h>
#include <sys/syscall.h>

// Estructura para el estado de la máquina virtual
typedef struct {
    unsigned char* code;
    size_t size;
    unsigned char* data;
    size_t data_size;
    int pc;
    int sp;
    int flags;
    unsigned char registers[16];
    unsigned char stack[256];
} vm_state_t;

// Predicados opacos para confundir análisis estático
static inline int opaque_predicate_1(int x) {
    return ((x * 0x9E3779B9) ^ 0x12345678) & 1;
}

static inline int opaque_predicate_2(int x) {
    return ((x + 0x7FFFFFFF) ^ 0x87654321) & 1;
}

static inline int opaque_predicate_3(int x) {
    return ((x * 0x41C64E6D) + 0x3039) & 1;
}

// Función para cifrar/descifrar usando múltiples capas
void multi_layer_encrypt(unsigned char* data, size_t len, unsigned char key) {
    for (size_t i = 0; i < len; i++) {
        data[i] ^= key;
        data[i] = ((data[i] << 3) | (data[i] >> 5)) & 0xFF;
        data[i] ^= (key + i) & 0xFF;
        data[i] = ((data[i] << 2) | (data[i] >> 6)) & 0xFF;
    }
}

// Función para generar código polimórfico
void generate_polymorphic_code(unsigned char* buffer, size_t size, int seed) {
    srand(seed);
    for (size_t i = 0; i < size; i++) {
        buffer[i] = (rand() ^ (i * 0x9E3779B9)) & 0xFF;
    }
}

// Detección avanzada de análisis
int detect_analysis_environment() {
    // Verificar TracerPid
    FILE* status = fopen("/proc/self/status", "r");
    if (status) {
        char line[256];
        while (fgets(line, sizeof(line), status)) {
            if (strncmp(line, "TracerPid:", 10) == 0) {
                int tracer_pid = atoi(line + 10);
                fclose(status);
                if (tracer_pid != 0) return 1;
                break;
            }
        }
        fclose(status);
    }
    
    // Verificar breakpoints
    if (ptrace(PTRACE_TRACEME, 0, NULL, NULL) == -1) {
        return 1;
    }
    
    // Verificar timing
    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);
    usleep(1000);
    clock_gettime(CLOCK_MONOTONIC, &end);
    long diff = (end.tv_sec - start.tv_sec) * 1000000000L + (end.tv_nsec - start.tv_nsec);
    if (diff > 2000000) return 1; // Más de 2ms indica debugger
    
    // Verificar archivos de VM
    const char* vm_files[] = {
        "/proc/vz/version", "/proc/xen", "/proc/vmware/version",
        "/sys/class/dmi/id/product_name", "/sys/class/dmi/id/sys_vendor"
    };
    
    for (int i = 0; i < 5; i++) {
        if (access(vm_files[i], F_OK) == 0) return 1;
    }
    
    return 0;
}

// Verificación de integridad del binario
int verify_binary_integrity() {
    FILE* self = fopen("/proc/self/exe", "rb");
    if (!self) return 0;
    
    unsigned char buffer[4096];
    size_t bytes_read;
    unsigned long checksum = 0;
    
    while ((bytes_read = fread(buffer, 1, sizeof(buffer), self)) > 0) {
        for (size_t i = 0; i < bytes_read; i++) {
            checksum = (checksum * 31 + buffer[i]) & 0xFFFFFFFF;
        }
    }
    
    fclose(self);
    
    // Checksum esperado (se calcula dinámicamente)
    unsigned long expected = 0x12345678; // Placeholder
    return (checksum == expected);
}

// Máquina virtual polimórfica
int execute_vm_instruction(vm_state_t* vm) {
    if (vm->pc >= vm->size) return 0;
    
    unsigned char opcode = vm->code[vm->pc];
    
    // Decodificar instrucción usando predicados opacos
    if (opaque_predicate_1(vm->pc)) {
        opcode ^= 0x42;
    }
    
    if (opaque_predicate_2(vm->pc)) {
        opcode = ((opcode << 2) | (opcode >> 6)) & 0xFF;
    }
    
    switch (opcode & 0x0F) {
        case 0x01: // LOAD
            if (vm->pc + 1 < vm->size) {
                unsigned char reg = vm->code[vm->pc + 1] & 0x0F;
                unsigned char val = vm->code[vm->pc + 2];
                vm->registers[reg] = val;
                vm->pc += 3;
            }
            break;
            
        case 0x02: // STORE
            if (vm->pc + 1 < vm->size) {
                unsigned char reg = vm->code[vm->pc + 1] & 0x0F;
                vm->stack[vm->sp++] = vm->registers[reg];
                vm->pc += 2;
            }
            break;
            
        case 0x03: // XOR
            if (vm->pc + 2 < vm->size) {
                unsigned char reg1 = vm->code[vm->pc + 1] & 0x0F;
                unsigned char reg2 = vm->code[vm->pc + 2] & 0x0F;
                vm->registers[reg1] ^= vm->registers[reg2];
                vm->pc += 3;
            }
            break;
            
        case 0x04: // ADD
            if (vm->pc + 2 < vm->size) {
                unsigned char reg1 = vm->code[vm->pc + 1] & 0x0F;
                unsigned char reg2 = vm->code[vm->pc + 2] & 0x0F;
                vm->registers[reg1] = (vm->registers[reg1] + vm->registers[reg2]) & 0xFF;
                vm->pc += 3;
            }
            break;
            
        case 0x05: // CMP
            if (vm->pc + 2 < vm->size) {
                unsigned char reg1 = vm->code[vm->pc + 1] & 0x0F;
                unsigned char reg2 = vm->code[vm->pc + 2] & 0x0F;
                vm->flags = (vm->registers[reg1] == vm->registers[reg2]) ? 1 : 0;
                vm->pc += 3;
            }
            break;
            
        case 0x06: // JMP
            if (vm->pc + 1 < vm->size) {
                vm->pc = vm->code[vm->pc + 1];
            }
            break;
            
        case 0x07: // JZ
            if (vm->flags && vm->pc + 1 < vm->size) {
                vm->pc = vm->code[vm->pc + 1];
            } else {
                vm->pc += 2;
            }
            break;
            
        default:
            vm->pc++;
            break;
    }
    
    return 1;
}

// Función para descifrar mensajes
void decrypt_message(unsigned char* encrypted, size_t len, unsigned char key) {
    multi_layer_encrypt(encrypted, len, key);
}

// Función principal de validación usando la VM
int validate_with_vm(const char* input) {
    if (!input || strlen(input) != 41) return 0;
    
    // Verificación básica de formato
    if (input[0] != 'H' || input[1] != 'T' || input[2] != 'B' || input[3] != '{' || input[40] != '}') {
        return 0;
    }
    
    // Crear estado de la VM
    vm_state_t vm = {0};
    vm.code = malloc(1024);
    vm.data = malloc(256);
    vm.size = 1024;
    vm.data_size = 256;
    
    if (!vm.code || !vm.data) {
        if (vm.code) free(vm.code);
        if (vm.data) free(vm.data);
        return 0;
    }
    
    // Generar código polimórfico
    generate_polymorphic_code(vm.code, vm.size, 0x12345678);
    
    // Cifrar la entrada
    unsigned char encrypted_input[42];
    strncpy((char*)encrypted_input, input, 41);
    encrypted_input[41] = '\0';
    
    // Aplicar múltiples capas de cifrado
    multi_layer_encrypt(encrypted_input, 41, 0x42);
    multi_layer_encrypt(encrypted_input, 41, 0x13);
    multi_layer_encrypt(encrypted_input, 41, 0x37);
    
    // Cargar datos en la VM
    memcpy(vm.data, encrypted_input, 41);
    
    // Configurar registros para validación
    vm.registers[0] = 0x48; // 'H'
    vm.registers[1] = 0x54; // 'T'
    vm.registers[2] = 0x42; // 'B'
    vm.registers[3] = 0x7B; // '{'
    
    // Ejecutar algunas instrucciones de la VM
    int instructions_executed = 0;
    while (execute_vm_instruction(&vm) && instructions_executed < 100) {
        instructions_executed++;
    }
    
    // Verificación final usando predicados opacos
    int result = 1;
    if (opaque_predicate_1(instructions_executed)) {
        result = (vm.registers[0] == 0x48 && vm.registers[1] == 0x54 && 
                 vm.registers[2] == 0x42 && vm.registers[3] == 0x7B);
    }
    
    // Verificar el contenido de la flag usando operaciones matemáticas
    unsigned char expected_bytes[] = {
        0x73, 0x6D, 0x75, 0x72, 0x66, 0x5F, 0x77, 0x34, 0x73, 0x5F,
        0x68, 0x33, 0x72, 0x33, 0x5F, 0x61, 0x6E, 0x64, 0x5F, 0x73,
        0x30, 0x5F, 0x77, 0x34, 0x73, 0x5F, 0x79, 0x30, 0x75, 0x72,
        0x5F, 0x66, 0x6C, 0x34, 0x67
    };
    
    for (int i = 4; i < 40; i++) {
        if ((unsigned char)input[i] != expected_bytes[i-4]) {
            result = 0;
            break;
        }
    }
    
    free(vm.code);
    free(vm.data);
    
    return result;
}

// Función para mostrar mensajes cifrados
void show_encrypted_message(const char* message, unsigned char key) {
    size_t len = strlen(message);
    unsigned char* encrypted = malloc(len + 1);
    
    strcpy((char*)encrypted, message);
    multi_layer_encrypt(encrypted, len, key);
    
    printf("Mensaje cifrado: ");
    for (size_t i = 0; i < len; i++) {
        printf("%02X ", encrypted[i]);
    }
    printf("\n");
    
    free(encrypted);
}

int main() {
    // Verificaciones de seguridad
    if (detect_analysis_environment()) {
        show_encrypted_message("Entorno de análisis detectado", 0x42);
        exit(1);
    }
    
    if (!verify_binary_integrity()) {
        show_encrypted_message("Integridad del binario comprometida", 0x13);
        exit(1);
    }
    
    // Configurar seccomp para limitar syscalls
    prctl(PR_SET_SECCOMP, SECCOMP_MODE_STRICT);
    
    printf("=== ULTIMATE VAULT ===\n");
    printf("Sistema de seguridad polimórfico activado\n");
    printf("Ingresa la clave de acceso: ");
    
    char input[256];
    if (!fgets(input, sizeof(input), stdin)) {
        show_encrypted_message("Error de entrada", 0x37);
        exit(1);
    }
    
    // Eliminar newline
    input[strcspn(input, "\n")] = '\0';
    
    // Validación usando la VM polimórfica
    if (validate_with_vm(input)) {
        // Descifrar y mostrar la flag
        unsigned char flag[] = {
            0x0A, 0x16, 0x00, 0x39, 0x31, 0x37, 0x1E, 0x30, 0x1D, 0x1E,
            0x1C, 0x1F, 0x1E, 0x1D, 0x1C, 0x1B, 0x1A, 0x19, 0x18, 0x17,
            0x16, 0x15, 0x14, 0x13, 0x12, 0x11, 0x10, 0x0F, 0x0E, 0x0D,
            0x0C, 0x0B, 0x0A, 0x09, 0x08, 0x07, 0x06, 0x05, 0x04, 0x03, 0x02
        };
        
        multi_layer_encrypt(flag, 41, 0x42);
        multi_layer_encrypt(flag, 41, 0x13);
        multi_layer_encrypt(flag, 41, 0x37);
        
        printf("Acceso concedido: %s\n", flag);
    } else {
        show_encrypted_message("Acceso denegado", 0x42);
    }
    
    return 0;
}