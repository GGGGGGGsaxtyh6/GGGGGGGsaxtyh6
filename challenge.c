#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>
#include <sys/ptrace.h>
#include <signal.h>

// Anti-debugging y ofuscación
#define OBFUSCATE(x) ((x) ^ 0x42)
#define UNOBFUSCATE(x) ((x) ^ 0x42)

// Flags falsas para confundir
char fake_flag1[] = "HTB{fake_flag_1_here}";
char fake_flag2[] = "HTB{not_the_real_flag}";
char fake_flag3[] = "HTB{decoy_flag_123}";

// Función para detectar debugging
int is_debugger_present() {
    if (ptrace(PTRACE_TRACEME, 0, 1, 0) == -1) {
        return 1; // Debugger detectado
    }
    return 0;
}

// Función para verificar integridad
void integrity_check() {
    // Simular verificación de integridad
    volatile int dummy = 0;
    for (int i = 0; i < 1000; i++) {
        dummy += i * 3;
    }
}

// Función de decodificación XOR
void xor_decode(char* data, int len, char key) {
    for (int i = 0; i < len; i++) {
        data[i] ^= key;
    }
}

// Función principal de validación
int validate_input(char* input) {
    // Verificar longitud
    if (strlen(input) != 41) {
        return 0;
    }
    
    // Verificar formato
    if (input[0] != 'H' || input[1] != 'T' || input[2] != 'B' || input[3] != '{') {
        return 0;
    }
    
    if (input[40] != '}') {
        return 0;
    }
    
    // Verificar contenido específico
    char expected[] = "smurf_w4s_h3r3_and_s0_w4s_y0ur_fl4g";
    for (int i = 4; i < 40; i++) {
        if (input[i] != expected[i-4]) {
            return 0;
        }
    }
    
    return 1;
}

// Función de hash personalizada
unsigned long custom_hash(char* str) {
    unsigned long hash = 5381;
    int c;
    while ((c = *str++)) {
        hash = ((hash << 5) + hash) + c;
    }
    return hash;
}

// Función para mostrar mensaje de éxito
void show_success() {
    printf("\n");
    printf("╔══════════════════════════════════════════════════════════════╗\n");
    printf("║                    ¡FELICIDADES!                            ║\n");
    printf("║                                                              ║\n");
    printf("║  Has encontrado la flag correcta:                           ║\n");
    printf("║  HTB{smurf_w4s_h3r3_and_s0_w4s_y0ur_fl4g}                  ║\n");
    printf("║                                                              ║\n");
    printf("║  Este challenge requería:                                    ║\n");
    printf("║  - Análisis estático del binario                            ║\n");
    printf("║  - Bypass de protecciones anti-debugging                    ║\n");
    printf("║  - Ingeniería inversa de algoritmos                         ║\n");
    printf("║  - Identificación de flags falsas                           ║\n");
    printf("║                                                              ║\n");
    printf("║  ¡Excelente trabajo!                                         ║\n");
    printf("╚══════════════════════════════════════════════════════════════╝\n");
}

// Función para mostrar pistas
void show_hints() {
    printf("\n");
    printf("╔══════════════════════════════════════════════════════════════╗\n");
    printf("║                        PISTAS                               ║\n");
    printf("║                                                              ║\n");
    printf("║  1. La flag real comienza con: HTB{smurf_                   ║\n");
    printf("║  2. Usa herramientas como: objdump, strings, gdb            ║\n");
    printf("║  3. Las flags falsas están ahí para confundir               ║\n");
    printf("║  4. El algoritmo de validación está en la función main      ║\n");
    printf("║  5. Hay protecciones anti-debugging que debes bypasear      ║\n");
    printf("║                                                              ║\n");
    printf("╚══════════════════════════════════════════════════════════════╝\n");
}

int main(int argc, char* argv[]) {
    // Verificar argumentos
    if (argc != 2) {
        printf("Uso: %s <flag>\n", argv[0]);
        printf("Ejemplo: %s HTB{tu_flag_aqui}\n", argv[0]);
        return 1;
    }
    
    // Verificar si hay debugger
    if (is_debugger_present()) {
        printf("Error: Debugger detectado. El programa se cerrará.\n");
        return 1;
    }
    
    // Verificación de integridad
    integrity_check();
    
    char* input = argv[1];
    
    // Mostrar información del challenge
    printf("╔══════════════════════════════════════════════════════════════╗\n");
    printf("║                CHALLENGE DE REVERSE ENGINEERING             ║\n");
    printf("║                                                              ║\n");
    printf("║  Nombre: Smurf's Hidden Treasure                            ║\n");
    printf("║  Dificultad: Extremo                                         ║\n");
    printf("║  Categoría: Reverse Engineering                              ║\n");
    printf("║                                                              ║\n");
    printf("║  Descripción:                                                ║\n");
    printf("║  Smurf ha escondido su tesoro en este binario.              ║\n");
    printf("║  Encuentra la flag correcta usando ingeniería inversa.      ║\n");
    printf("║                                                              ║\n");
    printf("║  Pistas:                                                     ║\n");
    printf("║  - La flag tiene 41 caracteres                               ║\n");
    printf("║  - Comienza con HTB{                                        ║\n");
    printf("║  - Termina con }                                             ║\n");
    printf("║  - Contiene información sobre Smurf                          ║\n");
    printf("╚══════════════════════════════════════════════════════════════╝\n");
    
    // Procesar entrada
    printf("\nProcesando entrada: %s\n", input);
    
    // Verificar si es una flag falsa
    if (strcmp(input, fake_flag1) == 0 || 
        strcmp(input, fake_flag2) == 0 || 
        strcmp(input, fake_flag3) == 0) {
        printf("❌ Flag falsa detectada. Esta no es la flag real.\n");
        printf("💡 Pista: La flag real comienza con HTB{smurf_\n");
        return 1;
    }
    
    // Validar la entrada
    if (validate_input(input)) {
        show_success();
        return 0;
    } else {
        printf("❌ Flag incorrecta.\n");
        printf("💡 Pista: La flag real comienza con HTB{smurf_\n");
        
        // Mostrar pistas adicionales si se solicita
        if (strcmp(input, "hints") == 0 || strcmp(input, "help") == 0) {
            show_hints();
        }
        
        return 1;
    }
}