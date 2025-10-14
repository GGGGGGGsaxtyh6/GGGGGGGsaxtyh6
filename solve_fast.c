#include <stdio.h>
#include <stdint.h>
#include <pthread.h>

#define NUM_THREADS 4

typedef struct {
    uint64_t start;
    uint64_t end;
    int thread_id;
} thread_data_t;

uint64_t mul = 0x902da3ff53640001ULL;
uint64_t inc = 0x8867e2d15b050000ULL;
uint64_t target = 0x771b59929b050000ULL;
volatile int found = 0;
uint64_t result_n = 0;

void* search_range(void* arg) {
    thread_data_t* data = (thread_data_t*)arg;
    uint64_t var = 0;
    
    // Saltar a la posición inicial
    for (uint64_t i = 0; i < data->start && !found; i++) {
        var = var * mul + inc;
    }
    
    for (uint64_t i = data->start; i < data->end && !found; i++) {
        if (var == target) {
            found = 1;
            result_n = i;
            printf("Thread %d: ¡Encontrado! N = %llu\n", data->thread_id, i);
            return NULL;
        }
        var = var * mul + inc;
        
        if (i % 1000000000 == 0 && i > 0) {
            printf("Thread %d: %llu iteraciones\n", data->thread_id, i);
        }
    }
    
    return NULL;
}

int main() {
    // Basándome en que alcanzó 52 mil millones en 60 segundos,
    // la tasa es aproximadamente 867 millones por segundo
    // Continuar desde donde se quedó
    
    uint64_t start = 52700000000ULL;
    uint64_t chunk_size = 10000000000ULL; // 10 mil millones por thread
    
    pthread_t threads[NUM_THREADS];
    thread_data_t thread_data[NUM_THREADS];
    
    for (int i = 0; i < NUM_THREADS; i++) {
        thread_data[i].start = start + i * chunk_size;
        thread_data[i].end = start + (i + 1) * chunk_size;
        thread_data[i].thread_id = i;
        pthread_create(&threads[i], NULL, search_range, &thread_data[i]);
    }
    
    for (int i = 0; i < NUM_THREADS; i++) {
        pthread_join(threads[i], NULL);
    }
    
    if (found) {
        printf("\n¡Solución encontrada! N = %llu\n", result_n);
    } else {
        printf("\nNo encontrado en el rango buscado\n");
    }
    
    return 0;
}
