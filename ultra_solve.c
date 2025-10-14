#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <time.h>

int main() {
    uint64_t a = 0x902da3ff53640001ULL;
    uint64_t c = 0x8867e2d15b050000ULL;
    uint64_t target = 0x771b59929b050000ULL;
    
    uint64_t var = 0;
    uint64_t iterations = 0;
    
    time_t start_time = time(NULL);
    time_t last_print = start_time;
    
    printf("Iniciando búsqueda ultra-optimizada...\n");
    printf("Target: 0x%016llx\n", (unsigned long long)target);
    printf("\n");
    
    while (var != target) {
        // Loop unrolling para mejor rendimiento
        for (int i = 0; i < 100000000; i++) {
            var = var * a + c;
            iterations++;
            
            if (var == target) {
                goto found;
            }
        }
        
        time_t now = time(NULL);
        if (now - last_print >= 5) {
            double elapsed = difftime(now, start_time);
            double rate = iterations / elapsed;
            printf("Iteraciones: %llu (%.2f M/s) - var = 0x%016llx\n", 
                   (unsigned long long)iterations, rate / 1000000.0, (unsigned long long)var);
            fflush(stdout);
            last_print = now;
        }
    }
    
found:
    printf("\n¡ENCONTRADO!\n");
    printf("N = %llu (0x%llx)\n", (unsigned long long)iterations, (unsigned long long)iterations);
    printf("var = 0x%016llx\n", (unsigned long long)var);
    
    // Descifrar la flag
    uint64_t flag_enc[4] = {
        0x15849e50ca8a604aULL,
        0x3e40bfe7abfbf126ULL,
        0x9857311b18c5398bULL,
        0x1d3843a27da2c230ULL
    };
    
    uint64_t mul1 = 0x6d4b9fc354323ULL;
    uint64_t mul2 = 0x1ba604d7bc3496dULL;
    uint64_t inc2 = 0x124a1bbd17d5c55ULL;
    uint64_t mul3 = 0x2f7d64b6bb2ae0dULL;
    
    uint64_t N = iterations;
    uint64_t index2 = N * inc2;
    
    uint64_t idx1_1 = N * mul1;
    uint64_t dec1 = flag_enc[0] ^ idx1_1;
    
    uint64_t idx2_1 = index2;
    uint64_t dec2 = flag_enc[1] ^ idx2_1;
    
    uint64_t idx1_2 = idx1_1 * mul2;
    uint64_t dec3 = flag_enc[2] ^ idx1_2;
    
    uint64_t idx2_2 = idx2_1 * mul3;
    uint64_t dec4 = flag_enc[3] ^ idx2_2;
    
    printf("\nFlag descifrada:\n");
    printf("%s\n", (char*)&dec1);
    
    // Imprimir como bytes
    unsigned char* flag_bytes = (unsigned char*)malloc(32);
    *(uint64_t*)(flag_bytes + 0) = dec1;
    *(uint64_t*)(flag_bytes + 8) = dec2;
    *(uint64_t*)(flag_bytes + 16) = dec3;
    *(uint64_t*)(flag_bytes + 24) = dec4;
    
    printf("Flag: ");
    for (int i = 0; i < 32; i++) {
        if (flag_bytes[i] >= 32 && flag_bytes[i] < 127) {
            printf("%c", flag_bytes[i]);
        } else if (flag_bytes[i] == 0) {
            break;
        } else {
            printf("\\x%02x", flag_bytes[i]);
        }
    }
    printf("\n");
    
    free(flag_bytes);
    
    return 0;
}
