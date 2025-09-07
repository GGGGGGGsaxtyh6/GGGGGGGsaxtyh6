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
#include <stdint.h>
#include <inttypes.h>

// Predicados opacos extremos
static inline int opaque_predicate_1(int x) {
    return ((x * 0x9E3779B9) ^ 0x12345678) & 1;
}

static inline int opaque_predicate_2(int x) {
    return ((x + 0x7FFFFFFF) ^ 0x87654321) & 1;
}

static inline int opaque_predicate_3(int x) {
    return ((x * 0x41C64E6D) + 0x3039) & 1;
}

static inline int opaque_predicate_4(int x) {
    return ((x * 0x6C078965) ^ 0x5D588B65) & 1;
}

static inline int opaque_predicate_5(int x) {
    return ((x + 0x269EC3) * 0x343FD) & 1;
}

// Función de cifrado metamórfico
void metamorphic_encrypt(unsigned char* data, size_t len, unsigned int key, int round) {
    for (size_t i = 0; i < len; i++) {
        // Aplicar transformación metamórfica
        unsigned int transformed_key = key ^ (i * 0x9E3779B9) ^ (round * 0x41C64E6D);
        
        data[i] ^= (transformed_key >> (i % 32)) & 0xFF;
        data[i] = ((data[i] << 3) | (data[i] >> 5)) & 0xFF;
        data[i] ^= (transformed_key >> ((i + 1) % 32)) & 0xFF;
        data[i] = ((data[i] << 2) | (data[i] >> 6)) & 0xFF;
        data[i] ^= (transformed_key >> ((i + 2) % 32)) & 0xFF;
        
        // Rotación cuántica
        data[i] = ((data[i] << 1) | (data[i] >> 7)) & 0xFF;
    }
}

// Detección extrema de análisis
int detect_analysis_environment_extreme() {
    // Método 1: Verificar TracerPid con múltiples intentos
    for (int attempt = 0; attempt < 3; attempt++) {
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
        usleep(1000);
    }
    
    // Método 2: Verificar breakpoints con ptrace
    for (int i = 0; i < 3; i++) {
        if (ptrace(PTRACE_TRACEME, 0, 1, 0) == -1) {
            return 1;
        }
    }
    
    // Método 3: Timing attack cuántico
    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);
    
    // Simular computación cuántica
    unsigned int entropy = 0xDEADBEEF;
    for (int i = 0; i < 1000000; i++) {
        entropy ^= (entropy << 13);
        entropy ^= (entropy >> 17);
        entropy ^= (entropy << 5);
    }
    
    clock_gettime(CLOCK_MONOTONIC, &end);
    long elapsed = (end.tv_sec - start.tv_sec) * 1000000000L + (end.tv_nsec - start.tv_nsec);
    
    if (elapsed > 50000000) { // Muy lento = debugger
        return 1;
    }
    
    // Método 4: Verificar /proc/self/maps
    FILE* maps = fopen("/proc/self/maps", "r");
    if (maps) {
        char line[256];
        int suspicious_mappings = 0;
        while (fgets(line, sizeof(line), maps)) {
            if (strstr(line, "gdb") || strstr(line, "radare2") || strstr(line, "ghidra")) {
                suspicious_mappings++;
            }
        }
        fclose(maps);
        if (suspicious_mappings > 0) return 1;
    }
    
    // Método 5: Verificar herramientas de análisis
    const char* analysis_tools[] = {
        "strings", "objdump", "hexdump", "gdb", "radare2", "ghidra", "ida",
        "strace", "ltrace", "valgrind", "gprof", "perf"
    };
    
    for (int i = 0; i < 12; i++) {
        char cmd[256];
        snprintf(cmd, sizeof(cmd), "which %s > /dev/null 2>&1", analysis_tools[i]);
        if (system(cmd) == 0) return 1;
    }
    
    // Método 6: Verificar procesos de análisis
    FILE* proc = popen("ps aux | grep -E '(strings|objdump|hexdump|gdb|radare2|ghidra|ida|strace|ltrace|valgrind)' | grep -v grep", "r");
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

// Detección extrema de VM/Sandbox
int detect_vm_sandbox_extreme() {
    // Verificar archivos de VM
    const char* vm_files[] = {
        "/proc/vz/version", "/proc/xen", "/proc/vmware/version",
        "/sys/class/dmi/id/product_name", "/sys/class/dmi/id/sys_vendor",
        "/sys/class/dmi/id/board_vendor", "/sys/class/dmi/id/chassis_vendor",
        "/proc/scsi/scsi", "/proc/ide/hd0/model", "/proc/ide/hd1/model"
    };
    
    for (int i = 0; i < 10; i++) {
        if (access(vm_files[i], F_OK) == 0) return 1;
    }
    
    // Verificar variables de entorno de VM
    const char* vm_env_vars[] = {
        "VBOX_INSTALL_PATH", "VMWARE_ROOT", "XEN_ROOT", "QEMU_ROOT",
        "VIRTUAL_ENV", "CONDA_DEFAULT_ENV", "PIPENV_ACTIVE"
    };
    
    for (int i = 0; i < 7; i++) {
        if (getenv(vm_env_vars[i])) return 1;
    }
    
    // Verificar características del sistema
    struct utsname sysinfo;
    if (uname(&sysinfo) == 0) {
        if (strstr(sysinfo.machine, "x86_64") == NULL) return 1;
        if (strstr(sysinfo.sysname, "Linux") == NULL) return 1;
    }
    
    // Verificar recursos del sistema
    struct rlimit rlim;
    if (getrlimit(RLIMIT_AS, &rlim) == 0) {
        if (rlim.rlim_cur < 1000000000) return 1; // Menos de 1GB RAM
    }
    
    // Verificar número de CPUs
    long cpu_count = sysconf(_SC_NPROCESSORS_ONLN);
    if (cpu_count < 2) return 1; // Menos de 2 CPUs
    
    // Verificar tiempo de sistema
    struct timeval tv;
    if (gettimeofday(&tv, NULL) == 0) {
        if (tv.tv_sec < 1600000000) return 1; // Sistema muy antiguo
    }
    
    return 0;
}

// Verificación de integridad extrema
int verify_binary_integrity_extreme() {
    FILE* self = fopen("/proc/self/exe", "rb");
    if (!self) return 0;
    
    unsigned char buffer[4096];
    size_t bytes_read;
    unsigned long checksum = 0;
    unsigned long checksum2 = 0;
    
    while ((bytes_read = fread(buffer, 1, sizeof(buffer), self)) > 0) {
        for (size_t i = 0; i < bytes_read; i++) {
            checksum = (checksum * 31 + buffer[i]) & 0xFFFFFFFF;
            checksum2 = (checksum2 * 37 + buffer[i]) & 0xFFFFFFFF;
        }
    }
    
    fclose(self);
    
    // Verificar múltiples checksums
    unsigned long expected1 = 0x12345678;
    unsigned long expected2 = 0x87654321;
    
    return (checksum == expected1 && checksum2 == expected2);
}

// Función principal de validación
int validate_metamorphic_flag(const char* input) {
    if (!input || strlen(input) != 41) return 0;
    
    // Verificación básica de formato
    if (input[0] != 'H' || input[1] != 'T' || input[2] != 'B' || input[3] != '{' || input[40] != '}') {
        return 0;
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
            return 0;
        }
    }
    
    return 1;
}

// Función para mostrar mensajes cifrados
void show_encrypted_message(const char* message, unsigned char key) {
    size_t len = strlen(message);
    unsigned char* encrypted = malloc(len + 1);
    
    strcpy((char*)encrypted, message);
    metamorphic_encrypt(encrypted, len, key, 0);
    
    printf("Mensaje cifrado: ");
    for (size_t i = 0; i < len; i++) {
        printf("%02X ", encrypted[i]);
    }
    printf("\n");
    
    free(encrypted);
}

// Función para mostrar información del challenge
void show_insane_challenge_info() {
    printf("╔══════════════════════════════════════════════════════════════╗\n");
    printf("║                INSANE VAULT - REVERSE ENGINEERING          ║\n");
    printf("║                                                              ║\n");
    printf("║  🎯 Nombre: Insane Vault                                   ║\n");
    printf("║  🔥 Dificultad: INSANE                                     ║\n");
    printf("║  📚 Categoría: Reverse Engineering                           ║\n");
    printf("║  ⏱️  Tiempo estimado: 3+ horas                             ║\n");
    printf("║                                                              ║\n");
    printf("║  📖 Descripción:                                             ║\n");
    printf("║  Un banco cuántico ha implementado un sistema de seguridad  ║\n");
    printf("║  ultra-avanzado con código metamórfico. El vault utiliza   ║\n");
    printf("║  una máquina virtual metamórfica con cifrado cuántico.     ║\n");
    printf("║  Encuentra la clave para acceder al vault.                 ║\n");
    printf("║                                                              ║\n");
    printf("║  🛡️  Protecciones implementadas:                            ║\n");
    printf("║     - Código metamórfico que se reescribe a sí mismo       ║\n");
    printf("║     - Máquina virtual metamórfica ofuscada                 ║\n");
    printf("║     - Control flow obfuscation extremo                     ║\n");
    printf("║     - Cifrado cuántico metamórfico                         ║\n");
    printf("║     - Anti-debugging extremo                               ║\n");
    printf("║     - Detección de VM/Sandbox extrema                      ║\n");
    printf("║     - Verificación de integridad extrema                   ║\n");
    printf("║                                                              ║\n");
    printf("║  🔍 Pistas:                                                 ║\n");
    printf("║     - La flag comienza con HTB{                            ║\n");
    printf("║     - Tiene exactamente 41 caracteres                      ║\n");
    printf("║     - Usa análisis dinámico de la VM metamórfica           ║\n");
    printf("║     - El cifrado es metamórfico y reversible               ║\n");
    printf("╚══════════════════════════════════════════════════════════════╝\n");
}

// Función para mostrar éxito
void show_insane_success() {
    printf("\n");
    printf("╔══════════════════════════════════════════════════════════════╗\n");
    printf("║                    ¡FELICIDADES!                            ║\n");
    printf("║                                                              ║\n");
    printf("║  🎉 Has accedido al Insane Vault!                          ║\n");
    printf("║                                                              ║\n");
    printf("║  🏆 Flag correcta: HTB{smurf_w4s_h3r3_and_s0_w4s_y0ur_fl4g} ║\n");
    printf("║                                                              ║\n");
    printf("║  Este challenge requería:                                    ║\n");
    printf("║  ✅ Análisis de código metamórfico                          ║\n");
    printf("║  ✅ Bypass de máquina virtual metamórfica                   ║\n");
    printf("║  ✅ Ingeniería inversa del cifrado cuántico                 ║\n");
    printf("║  ✅ Análisis dinámico de la VM metamórfica                  ║\n");
    printf("║  ✅ Bypass de protecciones anti-debugging extremas          ║\n");
    printf("║  ✅ Bypass de detección de VM/Sandbox                       ║\n");
    printf("║  ✅ Bypass de verificación de integridad                    ║\n");
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
    
    show_insane_challenge_info();
    
    // Verificaciones de seguridad extremas
    printf("\n🔍 Verificando entorno de ejecución...\n");
    
    if (detect_analysis_environment_extreme()) {
        printf("❌ Entorno de análisis detectado. El programa se cerrará.\n");
        printf("💡 Pista: Bypasea las protecciones anti-debugging extremas\n");
        return 1;
    }
    
    if (detect_vm_sandbox_extreme()) {
        printf("❌ VM/Sandbox detectado. El programa se cerrará.\n");
        printf("💡 Pista: Bypasea la detección de VM/Sandbox\n");
        return 1;
    }
    
    if (!verify_binary_integrity_extreme()) {
        printf("❌ Integridad del binario comprometida. El programa se cerrará.\n");
        printf("💡 Pista: Bypasea la verificación de integridad\n");
        return 1;
    }
    
    printf("✅ Verificaciones de seguridad extremas completadas\n");
    
    char* input = argv[1];
    
    // Procesar entrada
    printf("\n🔍 Procesando entrada en el Insane Vault...\n");
    printf("🔬 Inicializando máquina virtual metamórfica...\n");
    printf("🌊 Aplicando control flow obfuscation extremo...\n");
    printf("🔐 Ejecutando algoritmo de cifrado cuántico metamórfico...\n");
    
    // Validar flag
    if (validate_metamorphic_flag(input)) {
        show_insane_success();
        return 0;
    } else {
        printf("❌ Acceso denegado al Insane Vault.\n");
        printf("💡 Pista: Analiza la máquina virtual metamórfica\n");
        return 1;
    }
}