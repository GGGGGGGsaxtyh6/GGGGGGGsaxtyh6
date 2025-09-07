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

// Constantes ofuscadas con múltiples capas
#define LAYER1_KEY 0xDEADBEEF
#define LAYER2_KEY 0xCAFEBABE
#define LAYER3_KEY 0xFEEDFACE
#define LAYER4_KEY 0x1337C0DE
#define LAYER5_KEY 0xBAADF00D
#define MAGIC_SEED 0x12345678

// Estructura para datos ultra-ofuscados
typedef struct {
    unsigned int layer1;
    unsigned int layer2;
    unsigned int layer3;
    unsigned int checksum;
    unsigned int magic;
    char data[512];
    unsigned int obfuscation_key;
    unsigned int anti_tamper;
} ultra_obfuscated_t;

// Variables globales ultra-ofuscadas
static volatile int debug_detected = 0;
static volatile int vm_detected = 0;
static volatile int sandbox_detected = 0;
static volatile int analysis_detected = 0;
static volatile int tamper_detected = 0;
static char* hidden_buffer = NULL;
static ultra_obfuscated_t* secret_data = NULL;
static unsigned int global_checksum = 0;

// Funciones de ofuscación multi-capa
unsigned int obfuscate_layer1(unsigned int value) {
    return value ^ LAYER1_KEY ^ (value << 3) ^ (value >> 5);
}

unsigned int obfuscate_layer2(unsigned int value) {
    return value ^ LAYER2_KEY ^ (value << 7) ^ (value >> 11);
}

unsigned int obfuscate_layer3(unsigned int value) {
    return value ^ LAYER3_KEY ^ (value << 13) ^ (value >> 17);
}

unsigned int obfuscate_layer4(unsigned int value) {
    return value ^ LAYER4_KEY ^ (value << 19) ^ (value >> 23);
}

unsigned int obfuscate_layer5(unsigned int value) {
    return value ^ LAYER5_KEY ^ (value << 29) ^ (value >> 3);
}

void ultra_deobfuscate_string(char* str, int len, unsigned int key) {
    unsigned int key1 = obfuscate_layer1(key);
    unsigned int key2 = obfuscate_layer2(key);
    unsigned int key3 = obfuscate_layer3(key);
    unsigned int key4 = obfuscate_layer4(key);
    unsigned int key5 = obfuscate_layer5(key);
    
    for (int i = 0; i < len; i++) {
        unsigned int layer_key = (key1 >> (i % 4) * 8) & 0xFF;
        layer_key ^= (key2 >> ((i + 1) % 4) * 8) & 0xFF;
        layer_key ^= (key3 >> ((i + 2) % 4) * 8) & 0xFF;
        layer_key ^= (key4 >> ((i + 3) % 4) * 8) & 0xFF;
        layer_key ^= (key5 >> (i % 4) * 8) & 0xFF;
        str[i] ^= layer_key;
    }
}

// Detección ultra-avanzada de debugging
int detect_debugger_ultra() {
    // Método 1: ptrace múltiple
    if (ptrace(PTRACE_TRACEME, 0, 1, 0) == -1) return 1;
    if (ptrace(PTRACE_TRACEME, 0, 1, 0) == -1) return 1;
    
    // Método 2: Verificar /proc/self/status
    FILE* status = fopen("/proc/self/status", "r");
    if (status) {
        char line[256];
        while (fgets(line, sizeof(line), status)) {
            if (strncmp(line, "TracerPid:", 10) == 0) {
                int pid = atoi(line + 10);
                fclose(status);
                if (pid != 0) return 1;
            }
            if (strncmp(line, "State:", 6) == 0) {
                if (strstr(line, "t") != NULL) {
                    fclose(status);
                    return 1;
                }
            }
        }
        fclose(status);
    }
    
    // Método 3: Timing attack avanzado
    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);
    for (volatile int i = 0; i < 10000000; i++) {
        volatile int dummy = i * 3 + i / 2;
        dummy ^= 0x12345678;
    }
    clock_gettime(CLOCK_MONOTONIC, &end);
    
    long elapsed = (end.tv_sec - start.tv_sec) * 1000000000L + (end.tv_nsec - start.tv_nsec);
    if (elapsed > 100000000) return 1; // Muy lento = debugger
    
    // Método 4: Verificar breakpoints
    unsigned char* code = (unsigned char*)detect_debugger_ultra;
    if (code[0] == 0xCC) return 1; // INT3 breakpoint
    
    // Método 5: Verificar /proc/self/maps
    FILE* maps = fopen("/proc/self/maps", "r");
    if (maps) {
        char line[512];
        while (fgets(line, sizeof(line), maps)) {
            if (strstr(line, "gdb") || strstr(line, "lldb") || strstr(line, "radare2")) {
                fclose(maps);
                return 1;
            }
        }
        fclose(maps);
    }
    
    return 0;
}

// Detección ultra-avanzada de VM/Sandbox
int detect_vm_ultra() {
    // Verificar archivos típicos de VM
    const char* vm_files[] = {
        "/proc/vmware/version", "/proc/xen/version", "/proc/vz/version",
        "/sys/class/dmi/id/product_name", "/sys/class/dmi/id/sys_vendor",
        "/sys/class/dmi/id/board_vendor", "/sys/class/dmi/id/chassis_vendor",
        "/proc/scsi/scsi", "/sys/class/block/sda/device/vendor",
        "/sys/class/block/sda/device/model", "/proc/cpuinfo"
    };
    
    for (int i = 0; i < 11; i++) {
        if (access(vm_files[i], F_OK) == 0) {
            FILE* f = fopen(vm_files[i], "r");
            if (f) {
                char line[256];
                while (fgets(line, sizeof(line), f)) {
                    if (strstr(line, "VMware") || strstr(line, "VirtualBox") || 
                        strstr(line, "QEMU") || strstr(line, "Xen") || 
                        strstr(line, "KVM") || strstr(line, "Bochs")) {
                        fclose(f);
                        return 1;
                    }
                }
                fclose(f);
            }
        }
    }
    
    // Verificar CPU cores y características
    FILE* cpuinfo = fopen("/proc/cpuinfo", "r");
    if (cpuinfo) {
        int cores = 0;
        char line[256];
        while (fgets(line, sizeof(line), cpuinfo)) {
            if (strncmp(line, "processor", 9) == 0) cores++;
            if (strstr(line, "hypervisor") != NULL) {
                fclose(cpuinfo);
                return 1;
            }
        }
        fclose(cpuinfo);
        if (cores < 2) return 1;
    }
    
    // Verificar memoria
    FILE* meminfo = fopen("/proc/meminfo", "r");
    if (meminfo) {
        char line[256];
        while (fgets(line, sizeof(line), meminfo)) {
            if (strncmp(line, "MemTotal:", 9) == 0) {
                int mem_kb = atoi(line + 9);
                if (mem_kb < 2000000) { // Menos de 2GB
                    fclose(meminfo);
                    return 1;
                }
            }
        }
        fclose(meminfo);
    }
    
    return 0;
}

// Detección ultra-avanzada de sandbox
int detect_sandbox_ultra() {
    // Verificar si estamos en un entorno restringido
    if (getuid() == 0) return 1; // Root = sospechoso
    
    // Verificar tiempo de ejecución
    time_t start_time = time(NULL);
    usleep(100000); // 100ms
    time_t end_time = time(NULL);
    if (end_time - start_time < 1) return 1; // Time acelerado
    
    // Verificar recursos del sistema
    struct rlimit rlim;
    if (getrlimit(RLIMIT_AS, &rlim) == 0) {
        if (rlim.rlim_cur < 1000000000) return 1; // Menos de 1GB
    }
    
    // Verificar número de procesos
    FILE* proc = popen("ps aux | wc -l", "r");
    if (proc) {
        char line[32];
        if (fgets(line, sizeof(line), proc)) {
            int proc_count = atoi(line);
            if (proc_count < 50) { // Muy pocos procesos
                pclose(proc);
                return 1;
            }
        }
        pclose(proc);
    }
    
    // Verificar variables de entorno sospechosas
    if (getenv("SANDBOX") || getenv("CUCKOO") || getenv("ANALYSIS")) {
        return 1;
    }
    
    return 0;
}

// Detección de análisis estático
int detect_analysis() {
    // Verificar si hay herramientas de análisis
    const char* analysis_tools[] = {
        "strings", "objdump", "hexdump", "gdb", "radare2", "ghidra", "ida"
    };
    
    for (int i = 0; i < 7; i++) {
        char cmd[256];
        snprintf(cmd, sizeof(cmd), "which %s > /dev/null 2>&1", analysis_tools[i]);
        if (system(cmd) == 0) return 1;
    }
    
    // Verificar si estamos siendo analizados
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

// Verificación de integridad ultra-avanzada
int integrity_check_ultra() {
    // Verificar que el binario no ha sido modificado
    FILE* self = fopen("/proc/self/exe", "r");
    if (!self) return 0;
    
    // Leer primeros bytes y verificar magic number
    unsigned int magic;
    if (fread(&magic, sizeof(magic), 1, self) != 1) {
        fclose(self);
        return 0;
    }
    fclose(self);
    
    // Verificar que no es ELF modificado
    if (magic != 0x464C457F) return 0; // ELF magic
    
    // Verificar checksum del binario
    FILE* binary = fopen("/proc/self/exe", "rb");
    if (!binary) return 0;
    
    unsigned int checksum = 0;
    int c;
    while ((c = fgetc(binary)) != EOF) {
        checksum += c * 31;
        checksum ^= 0x12345678;
    }
    fclose(binary);
    
    // Verificar que el checksum es válido (simplificado)
    if (checksum == 0) return 0;
    
    return 1;
}

// Función de hash ultra-avanzada
unsigned long ultra_hash(const char* str) {
    unsigned long hash1 = 5381;
    unsigned long hash2 = 0;
    unsigned long hash3 = 0x811c9dc5;
    int c;
    
    while ((c = *str++)) {
        hash1 = ((hash1 << 5) + hash1) + c;
        hash2 = hash2 * 31 + c;
        hash3 = hash3 * 0x01000193 ^ c;
    }
    
    return hash1 ^ hash2 ^ hash3;
}

// Función para generar checksum ultra-avanzado
unsigned int generate_ultra_checksum(const char* data, int len) {
    unsigned int checksum1 = 0;
    unsigned int checksum2 = 0;
    unsigned int checksum3 = 0;
    
    for (int i = 0; i < len; i++) {
        checksum1 += data[i] * (i + 1);
        checksum2 ^= data[i] << (i % 32);
        checksum3 = checksum3 * 31 + data[i];
    }
    
    return checksum1 ^ checksum2 ^ checksum3;
}

// Validación ultra-multi-etapa
int validate_stage1_ultra(const char* input) {
    // Etapa 1: Verificar longitud básica
    if (strlen(input) < 10) return 0;
    
    // Etapa 1: Verificar formato HTB{
    if (strncmp(input, "HTB{", 4) != 0) return 0;
    
    // Etapa 1: Verificar que termina con }
    if (input[strlen(input) - 1] != '}') return 0;
    
    return 1;
}

int validate_stage2_ultra(const char* input) {
    // Etapa 2: Verificar longitud específica
    if (strlen(input) != 41) return 0;
    
    // Etapa 2: Verificar que contiene "smurf"
    if (strstr(input, "smurf") == NULL) return 0;
    
    return 1;
}

int validate_stage3_ultra(const char* input) {
    // Etapa 3: Verificación ultra-compleja
    // Flag ultra-ofuscada: HTB{smurf_w4s_h3r3_and_s0_w4s_y0ur_fl4g}
    unsigned char ultra_obfuscated[] = {
        0x0a^0x42, 0x16^0x42, 0x00^0x42, 0x39^0x42, 0x31^0x42, 0x2f^0x42, 0x37^0x42, 0x30^0x42, 0x24^0x42, 0x0d^0x42,
        0x35^0x42, 0x76^0x42, 0x31^0x42, 0x0d^0x42, 0x2a^0x42, 0x71^0x42, 0x30^0x42, 0x71^0x42, 0x0d^0x42, 0x03^0x42,
        0x2c^0x42, 0x06^0x42, 0x0d^0x42, 0x31^0x42, 0x72^0x42, 0x0d^0x42, 0x35^0x42, 0x76^0x42, 0x31^0x42, 0x0d^0x42,
        0x1b^0x42, 0x72^0x42, 0x37^0x42, 0x30^0x42, 0x0d^0x42, 0x24^0x42, 0x2e^0x42, 0x76^0x42, 0x25^0x42, 0x3f^0x42, 0x00
    };
    
    // Deofuscar la flag con múltiples capas
    char expected[42];
    for (int i = 0; i < 41; i++) {
        expected[i] = ultra_obfuscated[i] ^ 0x42;
    }
    expected[41] = '\0';
    
    // Verificar hash ultra-avanzado
    if (ultra_hash(input) != ultra_hash(expected)) return 0;
    
    // Verificar checksum ultra-avanzado
    if (generate_ultra_checksum(input, strlen(input)) != generate_ultra_checksum(expected, strlen(expected))) return 0;
    
    // Verificación carácter por carácter con validación adicional
    for (int i = 0; i < strlen(expected); i++) {
        if (input[i] != expected[i]) return 0;
    }
    
    return 1;
}

// Función para mostrar flags falsas con pistas ultra-progresivas
void show_ultra_fake_flag_response(const char* input) {
    printf("\n");
    printf("╔══════════════════════════════════════════════════════════════╗\n");
    printf("║                    FLAG FALSA DETECTADA                     ║\n");
    printf("║                                                              ║\n");
    printf("║  ❌ Esta no es la flag real                                 ║\n");
    printf("║                                                              ║\n");
    
    // Pistas ultra-progresivas basadas en la entrada
    if (strstr(input, "fake") || strstr(input, "test") || strstr(input, "demo")) {
        printf("║  💡 Pista: La flag real comienza con HTB{smurf_            ║\n");
    } else if (strstr(input, "smurf")) {
        printf("║  💡 Pista: Estás en el camino correcto...                  ║\n");
        printf("║  💡 Pista: La flag tiene exactamente 41 caracteres        ║\n");
        printf("║  💡 Pista: Usa análisis dinámico para encontrar la flag   ║\n");
    } else if (strlen(input) == 41) {
        printf("║  💡 Pista: La longitud es correcta, pero el contenido no  ║\n");
        printf("║  💡 Pista: La flag está ofuscada en el binario            ║\n");
        printf("║  💡 Pista: Necesitas bypasear las protecciones            ║\n");
    } else {
        printf("║  💡 Pista: Analiza el binario con herramientas avanzadas  ║\n");
        printf("║  💡 Pista: La flag real está ultra-ofuscada               ║\n");
        printf("║  💡 Pista: Requiere ingeniería inversa profesional        ║\n");
    }
    
    printf("║                                                              ║\n");
    printf("║  🔍 Herramientas recomendadas:                               ║\n");
    printf("║     - Análisis estático: objdump, hexdump, radare2          ║\n");
    printf("║     - Análisis dinámico: gdb con bypass de protecciones     ║\n");
    printf("║     - Herramientas avanzadas: ghidra, ida pro               ║\n");
    printf("║     - Bypass de protecciones anti-debugging                 ║\n");
    printf("╚══════════════════════════════════════════════════════════════╝\n");
}

// Función para mostrar éxito ultra
void show_ultra_success() {
    printf("\n");
    printf("╔══════════════════════════════════════════════════════════════╗\n");
    printf("║                    ¡FELICIDADES!                            ║\n");
    printf("║                                                              ║\n");
    printf("║  🎉 Has encontrado el tesoro ultra-protegido de Smurf!      ║\n");
    printf("║                                                              ║\n");
    printf("║  🏆 Flag correcta: HTB{smurf_w4s_h3r3_and_s0_w4s_y0ur_fl4g} ║\n");
    printf("║                                                              ║\n");
    printf("║  Este challenge ultra-avanzado requería:                     ║\n");
    printf("║  ✅ Bypass de protecciones anti-debugging ultra-avanzadas    ║\n");
    printf("║  ✅ Detección y bypass de VM/Sandbox ultra-avanzada         ║\n");
    printf("║  ✅ Análisis estático ultra-avanzado                        ║\n");
    printf("║  ✅ Ingeniería inversa de algoritmos ultra-complejos        ║\n");
    printf("║  ✅ Identificación de flags falsas ultra-progresivas        ║\n");
    printf("║  ✅ Análisis de validación ultra-multi-etapa                ║\n");
    printf("║  ✅ Bypass de detección de análisis estático                ║\n");
    printf("║  ✅ Verificación de integridad ultra-avanzada               ║\n");
    printf("║                                                              ║\n");
    printf("║  🎯 ¡Excelente trabajo de reverse engineering ultra!        ║\n");
    printf("╚══════════════════════════════════════════════════════════════╝\n");
}

// Función para mostrar información del challenge ultra
void show_ultra_challenge_info() {
    printf("╔══════════════════════════════════════════════════════════════╗\n");
    printf("║                CHALLENGE ULTRA-INSANE DE REVERSE ENGINEERING ║\n");
    printf("║                                                              ║\n");
    printf("║  🎯 Nombre: Smurf's Ultra-Protected Treasure                ║\n");
    printf("║  🔥 Dificultad: ULTRA-INSANE                                ║\n");
    printf("║  📚 Categoría: Reverse Engineering                           ║\n");
    printf("║  ⏱️  Tiempo estimado: 4+ horas                             ║\n");
    printf("║                                                              ║\n");
    printf("║  📖 Descripción:                                             ║\n");
    printf("║  Smurf ha escondido su tesoro en este binario ultra-        ║\n");
    printf("║  protegido. El binario tiene múltiples capas de protección  ║\n");
    printf("║  ultra-avanzadas y validación ultra-compleja. Encuentra     ║\n");
    printf("║  la flag correcta usando técnicas ultra-avanzadas de        ║\n");
    printf("║  ingeniería inversa.                                        ║\n");
    printf("║                                                              ║\n");
    printf("║  🛡️  Protecciones ultra-implementadas:                      ║\n");
    printf("║     - Anti-debugging ultra-avanzado (5 métodos)             ║\n");
    printf("║     - Detección de VM/Sandbox ultra-avanzada                ║\n");
    printf("║     - Verificación de integridad ultra-avanzada             ║\n");
    printf("║     - Validación ultra-multi-etapa                          ║\n");
    printf("║     - Ofuscación ultra-avanzada de strings y datos          ║\n");
    printf("║     - Flags falsas ultra-progresivas                        ║\n");
    printf("║     - Detección de análisis estático                        ║\n");
    printf("║     - Verificación anti-tampering                           ║\n");
    printf("║                                                              ║\n");
    printf("║  🔍 Pistas iniciales:                                       ║\n");
    printf("║     - La flag comienza con HTB{smurf_                       ║\n");
    printf("║     - Tiene exactamente 41 caracteres                       ║\n");
    printf("║     - Contiene información sobre Smurf                       ║\n");
    printf("║     - Usa análisis estático Y dinámico ultra-avanzado       ║\n");
    printf("║     - Requiere bypass de múltiples protecciones             ║\n");
    printf("╚══════════════════════════════════════════════════════════════╝\n");
}

// Función principal ultra
int main(int argc, char* argv[]) {
    // Verificar argumentos
    if (argc != 2) {
        printf("Uso: %s <flag>\n", argv[0]);
        printf("Ejemplo: %s HTB{tu_flag_aqui}\n", argv[0]);
        return 1;
    }
    
    // Mostrar información del challenge ultra
    show_ultra_challenge_info();
    
    // Verificaciones de seguridad ultra-avanzadas
    printf("\n🔍 Verificando entorno de ejecución ultra-avanzado...\n");
    
    if (detect_debugger_ultra()) {
        printf("❌ Debugger ultra-detectado. El programa se cerrará.\n");
        printf("💡 Pista: Bypasea las protecciones anti-debugging ultra-avanzadas\n");
        return 1;
    }
    
    if (detect_vm_ultra()) {
        printf("⚠️  VM ultra-detectada. Continuando con precaución...\n");
        vm_detected = 1;
    }
    
    if (detect_sandbox_ultra()) {
        printf("⚠️  Sandbox ultra-detectado. Continuando con precaución...\n");
        sandbox_detected = 1;
    }
    
    if (detect_analysis()) {
        printf("⚠️  Análisis estático detectado. Continuando con precaución...\n");
        analysis_detected = 1;
    }
    
    if (!integrity_check_ultra()) {
        printf("❌ Integridad del binario ultra-comprometida.\n");
        return 1;
    }
    
    printf("✅ Verificaciones de seguridad ultra-avanzadas completadas\n");
    
    char* input = argv[1];
    
    // Procesar entrada
    printf("\n🔍 Procesando entrada ultra-avanzada: %s\n", input);
    
    // Verificar si es una flag falsa conocida ultra
    const char* ultra_fake_flags[] = {
        "HTB{fake_flag_1_here}", "HTB{not_the_real_flag}", "HTB{decoy_flag_123}",
        "HTB{this_is_not_the_flag}", "HTB{try_harder}", "HTB{keep_looking}",
        "HTB{almost_there}", "HTB{close_but_no}", "HTB{reverse_me_harder}",
        "HTB{static_analysis_needed}", "HTB{dynamic_analysis_required}",
        "HTB{debugging_skills_needed}", "HTB{assembly_required}",
        "HTB{hex_editor_helpful}", "HTB{strings_command_useful}",
        "HTB{objdump_analysis}", "HTB{gdb_debugging}", "HTB{radare2_analysis}",
        "HTB{ghidra_reverse}", "HTB{ida_pro_analysis}", "HTB{ultra_fake_1}",
        "HTB{ultra_fake_2}", "HTB{ultra_fake_3}", "HTB{ultra_fake_4}",
        "HTB{ultra_fake_5}", "HTB{ultra_fake_6}", "HTB{ultra_fake_7}",
        "HTB{ultra_fake_8}", "HTB{ultra_fake_9}", "HTB{ultra_fake_10}"
    };
    
    for (int i = 0; i < 30; i++) {
        if (strcmp(input, ultra_fake_flags[i]) == 0) {
            show_ultra_fake_flag_response(input);
            return 1;
        }
    }
    
    // Validación ultra-multi-etapa
    printf("🔍 Etapa 1: Validación básica ultra...\n");
    if (!validate_stage1_ultra(input)) {
        printf("❌ Falló validación básica ultra\n");
        printf("💡 Pista: La flag debe comenzar con HTB{ y terminar con }\n");
        return 1;
    }
    printf("✅ Etapa 1 ultra completada\n");
    
    printf("🔍 Etapa 2: Validación de contenido ultra...\n");
    if (!validate_stage2_ultra(input)) {
        printf("❌ Falló validación de contenido ultra\n");
        printf("💡 Pista: La flag debe contener 'smurf' y tener 41 caracteres\n");
        return 1;
    }
    printf("✅ Etapa 2 ultra completada\n");
    
    printf("🔍 Etapa 3: Validación final ultra...\n");
    if (!validate_stage3_ultra(input)) {
        printf("❌ Falló validación final ultra\n");
        printf("💡 Pista: Usa análisis ultra-avanzado para encontrar la flag exacta\n");
        return 1;
    }
    printf("✅ Etapa 3 ultra completada\n");
    
    // Éxito ultra
    show_ultra_success();
    return 0;
}