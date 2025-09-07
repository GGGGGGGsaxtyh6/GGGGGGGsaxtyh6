#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/ptrace.h>
#include <time.h>
#include <math.h>

// Anti-debugging
void check_debug() {
    if (ptrace(PTRACE_TRACEME, 0, 1, 0) == -1) {
        printf("Debugger detected!\n");
        exit(1);
    }
}

// Complex mathematical function that leads nowhere
double quantum_function(double x, double y) {
    double result = 0;
    for (int i = 0; i < 1000; i++) {
        result += sin(x * i) * cos(y * i) * exp(-i * 0.001);
    }
    return result;
}

// Fake validation function
int validate_input(char* input) {
    if (strlen(input) != 32) return 0;
    
    // This is a red herring - not the real validation
    char pattern[] = "quantum_paradox_2024";
    char encoded[64];
    for (int i = 0; pattern[i]; i++) {
        encoded[i] = pattern[i] ^ 0x33;
    }
    encoded[strlen(pattern)] = '\0';
    
    return strstr(input, encoded) != NULL;
}

// Another fake validation
int validate_quantum_key(char* key) {
    int sum = 0;
    for (int i = 0; key[i]; i++) {
        sum += (int)key[i];
    }
    
    // Check if sum is prime (red herring)
    int primes[] = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47};
    for (int i = 0; i < 15; i++) {
        if (sum == primes[i]) return 1;
    }
    return 0;
}

// Function that contains the real flag (never called)
void get_real_flag() {
    // This function is never called directly
    // The flag is hidden in the binary and must be extracted through memory analysis
    char real_flag[] = "HTB{qu4ntum_paradox_s0lv3d_2024_real_flag}";
    
    // Obfuscate the flag in memory
    for (int i = 0; real_flag[i]; i++) {
        real_flag[i] ^= 0xAA;
    }
    
    // This is just to make the function look like it does something
    double result = quantum_function(1.0, 2.0);
    printf("Quantum result: %f\n", result);
}

// Main function with multiple paths
int main() {
    check_debug();
    
    printf("=== Quantum Paradox Challenge ===\n");
    printf("Enter your quantum key: ");
    
    char input[100];
    fgets(input, sizeof(input), stdin);
    
    // Remove newline
    input[strcspn(input, "\n")] = 0;
    
    // Multiple validation paths - all lead to fake flags
    if (validate_input(input)) {
        printf("Input validated! Processing...\n");
        printf("Quantum analysis complete. FAKE FLAG: HTB{f4k3_fl4g_1_qu4ntum_3rr0r}\n");
        printf("This is a FAKE flag - keep looking deeper!\n");
    } else if (validate_quantum_key(input)) {
        printf("Quantum key accepted! Analyzing...\n");
        printf("Paradox analysis complete. FAKE FLAG: HTB{f4k3_fl4g_2_paradox}\n");
        printf("This is a FAKE flag - keep looking deeper!\n");
    } else {
        printf("Invalid input. Running quantum simulation...\n");
        
        // Simulate quantum operations
        for (int i = 0; i < 5; i++) {
            printf("Quantum state %d: ", i);
            double result = quantum_function(i * 0.1, i * 0.2);
            printf("%.6f\n", result);
            usleep(500000);
        }
        
        printf("Simulation complete. FAKE FLAG: HTB{qu4ntum_3nt4ngl3m3nt_s0lv3d}\n");
        printf("This is a FAKE flag - keep looking deeper!\n");
    }
    
    // The real flag is never displayed - it must be found through reversing
    // It's hidden in the get_real_flag() function and obfuscated in memory
    
    return 0;
}