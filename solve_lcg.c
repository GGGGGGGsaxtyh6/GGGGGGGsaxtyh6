#include <stdio.h>
#include <stdint.h>

int main() {
    uint64_t mul = 0x902da3ff53640001ULL;
    uint64_t inc = 0x8867e2d15b050000ULL;
    uint64_t target = 0x771b59929b050000ULL;
    
    uint64_t var = 0;
    uint64_t iterations = 0;
    
    // Ejecutar el LCG hasta encontrar el target
    while (var != target) {
        var = var * mul + inc;
        iterations++;
        
        if (iterations % 100000000 == 0) {
            printf("Iteración %llu, var = 0x%llx\n", iterations, var);
            fflush(stdout);
        }
        
        // Límite de seguridad
        if (iterations > 100000000000ULL) {
            printf("Excedido límite de iteraciones\n");
            return 1;
        }
    }
    
    printf("¡Encontrado! N = %llu\n", iterations);
    printf("var = 0x%llx\n", var);
    
    return 0;
}
