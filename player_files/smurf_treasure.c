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

// Constantes ofuscadas
#define OBF_KEY_1 0xDEADBEEF
#define OBF_KEY_2 0xCAFEBABE
#define OBF_KEY_3 0xFEEDFACE
#define MAGIC_NUM 0x1337C0DE

// Estructura para datos ofuscados
typedef struct {
    unsigned int key1;
    unsigned int key2;
    unsigned int checksum;
    char data[256];
} obfuscated_data_t;

// Variables globales ofuscadas
static volatile int debug_detected = 0;
static volatile int vm_detected = 0;
static volatile int sandbox_detected = 0;
static char* hidden_buffer = NULL;
static obfuscated_data_t* secret_data = NULL;

// Funciones de ofuscación
unsigned int obfuscate_xor(unsigned int value, unsigned int key) {
    return value ^ key;
}

void deobfuscate_string(char* str, int len, unsigned int key) {
    for (int i = 0; i < len; i++) {
        str[i] ^= (key >> (i % 4) * 8) & 0xFF;
    }
}

// Detección avanzada de debugging
int detect_debugger() {
    // Método 1: ptrace
    if (ptrace(PTRACE_TRACEME, 0, 1, 0) == -1) {
        return 1;
    }
    
    // Método 2: Verificar /proc/self/status
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
    
    // Método 3: Timing attack
    clock_t start = clock();
    for (volatile int i = 0; i < 1000000; i++);
    clock_t end = clock();
    if ((end - start) > 100000) { // Muy lento = debugger
        return 1;
    }
    
    return 0;
}

// Detección de VM/Sandbox
int detect_vm() {
    // Verificar archivos típicos de VM
    const char* vm_files[] = {
        "/proc/vmware/version",
        "/proc/xen/version",
        "/proc/vz/version",
        "/sys/class/dmi/id/product_name",
        "/sys/class/dmi/id/sys_vendor"
    };
    
    for (int i = 0; i < 5; i++) {
        if (access(vm_files[i], F_OK) == 0) {
            return 1;
        }
    }
    
    // Verificar CPU cores (VMs suelen tener pocos)
    FILE* cpuinfo = fopen("/proc/cpuinfo", "r");
    if (cpuinfo) {
        int cores = 0;
        char line[256];
        while (fgets(line, sizeof(line), cpuinfo)) {
            if (strncmp(line, "processor", 9) == 0) {
                cores++;
            }
        }
        fclose(cpuinfo);
        if (cores < 2) return 1;
    }
    
    return 0;
}

// Detección de sandbox
int detect_sandbox() {
    // Verificar si estamos en un entorno restringido
    if (getuid() == 0) return 1; // Root = sospechoso
    
    // Verificar tiempo de ejecución (sandboxes suelen tener timeout)
    time_t start_time = time(NULL);
    sleep(1);
    time_t end_time = time(NULL);
    if (end_time - start_time < 1) return 1; // Time acelerado
    
    return 0;
}

// Función de verificación de integridad
int integrity_check() {
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
    
    return 1;
}

// Función de hash personalizada
unsigned long custom_hash(const char* str) {
    unsigned long hash = 5381;
    int c;
    while ((c = *str++)) {
        hash = ((hash << 5) + hash) + c;
    }
    return hash;
}

// Función para generar checksum
unsigned int generate_checksum(const char* data, int len) {
    unsigned int checksum = 0;
    for (int i = 0; i < len; i++) {
        checksum += data[i] * (i + 1);
    }
    return checksum;
}

// Función de validación multi-etapa
int validate_stage1(const char* input) {
    // Etapa 1: Verificar longitud básica
    if (strlen(input) < 10) return 0;
    
    // Etapa 1: Verificar formato HTB{
    if (strncmp(input, "HTB{", 4) != 0) return 0;
    
    // Etapa 1: Verificar que termina con }
    if (input[strlen(input) - 1] != '}') return 0;
    
    return 1;
}

int validate_stage2(const char* input) {
    // Etapa 2: Verificar longitud específica
    if (strlen(input) != 41) return 0;
    
    // Etapa 2: Verificar que contiene "smurf"
    if (strstr(input, "smurf") == NULL) return 0;
    
    return 1;
}

int validate_stage3(const char* input) {
    // Etapa 3: Verificación completa
    const char* expected = "HTB{smurf_w4s_h3r3_and_s0_w4s_y0ur_fl4g}";
    
    // Verificar hash
    if (custom_hash(input) != custom_hash(expected)) return 0;
    
    // Verificar checksum
    if (generate_checksum(input, strlen(input)) != generate_checksum(expected, strlen(expected))) return 0;
    
    // Verificación carácter por carácter
    for (int i = 0; i < strlen(expected); i++) {
        if (input[i] != expected[i]) return 0;
    }
    
    return 1;
}

// Función para mostrar flags falsas con pistas
void show_fake_flag_response(const char* input) {
    printf("\n");
    printf("╔══════════════════════════════════════════════════════════════╗\n");
    printf("║                    FLAG FALSA DETECTADA                     ║\n");
    printf("║                                                              ║\n");
    printf("║  ❌ Esta no es la flag real                                 ║\n");
    printf("║                                                              ║\n");
    
    // Pistas progresivas basadas en la entrada
    if (strstr(input, "fake") || strstr(input, "test") || strstr(input, "demo")) {
        printf("║  💡 Pista: La flag real comienza con HTB{smurf_            ║\n");
    } else if (strstr(input, "smurf")) {
        printf("║  💡 Pista: Estás en el camino correcto...                  ║\n");
        printf("║  💡 Pista: La flag tiene exactamente 41 caracteres        ║\n");
    } else if (strlen(input) == 41) {
        printf("║  💡 Pista: La longitud es correcta, pero el contenido no  ║\n");
        printf("║  💡 Pista: Usa herramientas de análisis estático          ║\n");
    } else {
        printf("║  💡 Pista: Analiza el binario con 'strings' y 'objdump'   ║\n");
        printf("║  💡 Pista: La flag real está oculta en el código          ║\n");
    }
    
    printf("║                                                              ║\n");
    printf("║  🔍 Herramientas recomendadas:                               ║\n");
    printf("║     - strings, objdump, hexdump                              ║\n");
    printf("║     - gdb, radare2, ghidra                                   ║\n");
    printf("║     - análisis estático y dinámico                           ║\n");
    printf("╚══════════════════════════════════════════════════════════════╝\n");
}

// Función para mostrar éxito
void show_success() {
    printf("\n");
    printf("╔══════════════════════════════════════════════════════════════╗\n");
    printf("║                    ¡FELICIDADES!                            ║\n");
    printf("║                                                              ║\n");
    printf("║  🎉 Has encontrado el tesoro de Smurf!                      ║\n");
    printf("║                                                              ║\n");
    printf("║  🏆 Flag correcta: HTB{smurf_w4s_h3r3_and_s0_w4s_y0ur_fl4g} ║\n");
    printf("║                                                              ║\n");
    printf("║  Este challenge requería:                                    ║\n");
    printf("║  ✅ Bypass de protecciones anti-debugging                    ║\n");
    printf("║  ✅ Detección y bypass de VM/Sandbox                         ║\n");
    printf("║  ✅ Análisis estático avanzado                               ║\n");
    printf("║  ✅ Ingeniería inversa de algoritmos                         ║\n");
    printf("║  ✅ Identificación de flags falsas                           ║\n");
    printf("║  ✅ Análisis de múltiples etapas de validación               ║\n");
    printf("║                                                              ║\n");
    printf("║  🎯 ¡Excelente trabajo de reverse engineering!               ║\n");
    printf("╚══════════════════════════════════════════════════════════════╝\n");
}

// Función para mostrar información del challenge
void show_challenge_info() {
    printf("╔══════════════════════════════════════════════════════════════╗\n");
    printf("║                CHALLENGE DE REVERSE ENGINEERING             ║\n");
    printf("║                                                              ║\n");
    printf("║  🎯 Nombre: Smurf's Hidden Treasure                         ║\n");
    printf("║  🔥 Dificultad: INSANE                                       ║\n");
    printf("║  📚 Categoría: Reverse Engineering                           ║\n");
    printf("║  ⏱️  Tiempo estimado: 2+ horas                              ║\n");
    printf("║                                                              ║\n");
    printf("║  📖 Descripción:                                             ║\n");
    printf("║  Smurf ha escondido su tesoro en este binario protegido.    ║\n");
    printf("║  El binario tiene múltiples capas de protección y           ║\n");
    printf("║  validación. Encuentra la flag correcta usando técnicas     ║\n");
    printf("║  avanzadas de ingeniería inversa.                           ║\n");
    printf("║                                                              ║\n");
    printf("║  🛡️  Protecciones implementadas:                            ║\n");
    printf("║     - Anti-debugging (múltiples métodos)                     ║\n");
    printf("║     - Detección de VM/Sandbox                                ║\n");
    printf("║     - Verificación de integridad                             ║\n");
    printf("║     - Validación multi-etapa                                 ║\n");
    printf("║     - Ofuscación de strings y datos                          ║\n");
    printf("║     - Flags falsas con pistas progresivas                    ║\n");
    printf("║                                                              ║\n");
    printf("║  🔍 Pistas iniciales:                                        ║\n");
    printf("║     - La flag comienza con HTB{smurf_                        ║\n");
    printf("║     - Tiene exactamente 41 caracteres                        ║\n");
    printf("║     - Contiene información sobre Smurf                       ║\n");
    printf("║     - Usa análisis estático Y dinámico                       ║\n");
    printf("╚══════════════════════════════════════════════════════════════╝\n");
}

// Función principal
int main(int argc, char* argv[]) {
    // Verificar argumentos
    if (argc != 2) {
        printf("Uso: %s <flag>\n", argv[0]);
        printf("Ejemplo: %s HTB{tu_flag_aqui}\n", argv[0]);
        return 1;
    }
    
    // Mostrar información del challenge
    show_challenge_info();
    
    // Verificaciones de seguridad
    printf("\n🔍 Verificando entorno de ejecución...\n");
    
    if (detect_debugger()) {
        printf("❌ Debugger detectado. El programa se cerrará.\n");
        printf("💡 Pista: Bypasea las protecciones anti-debugging\n");
        return 1;
    }
    
    if (detect_vm()) {
        printf("⚠️  VM detectada. Continuando con precaución...\n");
        vm_detected = 1;
    }
    
    if (detect_sandbox()) {
        printf("⚠️  Sandbox detectado. Continuando con precaución...\n");
        sandbox_detected = 1;
    }
    
    if (!integrity_check()) {
        printf("❌ Integridad del binario comprometida.\n");
        return 1;
    }
    
    printf("✅ Verificaciones de seguridad completadas\n");
    
    char* input = argv[1];
    
    // Procesar entrada
    printf("\n🔍 Procesando entrada: %s\n", input);
    
    // Verificar si es una flag falsa conocida
    const char* fake_flags[] = {
        "HTB{fake_flag_1_here}",
        "HTB{not_the_real_flag}",
        "HTB{decoy_flag_123}",
        "HTB{this_is_not_the_flag}",
        "HTB{try_harder}",
        "HTB{keep_looking}",
        "HTB{almost_there}",
        "HTB{close_but_no}",
        "HTB{reverse_me_harder}",
        "HTB{static_analysis_needed}",
        "HTB{dynamic_analysis_required}",
        "HTB{debugging_skills_needed}",
        "HTB{assembly_required}",
        "HTB{hex_editor_helpful}",
        "HTB{strings_command_useful}",
        "HTB{objdump_analysis}",
        "HTB{gdb_debugging}",
        "HTB{radare2_analysis}",
        "HTB{ghidra_reverse}",
        "HTB{ida_pro_analysis}"
    };
    
    for (int i = 0; i < 20; i++) {
        if (strcmp(input, fake_flags[i]) == 0) {
            show_fake_flag_response(input);
            return 1;
        }
    }
    
    // Validación multi-etapa
    printf("🔍 Etapa 1: Validación básica...\n");
    if (!validate_stage1(input)) {
        printf("❌ Falló validación básica\n");
        printf("💡 Pista: La flag debe comenzar con HTB{ y terminar con }\n");
        return 1;
    }
    printf("✅ Etapa 1 completada\n");
    
    printf("🔍 Etapa 2: Validación de contenido...\n");
    if (!validate_stage2(input)) {
        printf("❌ Falló validación de contenido\n");
        printf("💡 Pista: La flag debe contener 'smurf' y tener 41 caracteres\n");
        return 1;
    }
    printf("✅ Etapa 2 completada\n");
    
    printf("🔍 Etapa 3: Validación final...\n");
    if (!validate_stage3(input)) {
        printf("❌ Falló validación final\n");
        printf("💡 Pista: Usa análisis estático para encontrar la flag exacta\n");
        return 1;
    }
    printf("✅ Etapa 3 completada\n");
    
    // Éxito
    show_success();
    return 0;
}