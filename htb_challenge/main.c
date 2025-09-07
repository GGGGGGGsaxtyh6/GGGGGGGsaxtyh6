#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/ptrace.h>

// Anti-debugging
void check_debug() {
    if (ptrace(PTRACE_TRACEME, 0, 1, 0) == -1) {
        printf("Debugger detected!\n");
        exit(1);
    }
}

// Obfuscated strings
char* obfuscated_strings[] = {
    "\x48\x65\x6c\x6c\x6f", // "Hello"
    "\x57\x6f\x72\x6c\x64", // "World"
    "\x51\x75\x61\x6e\x74\x75\x6d", // "Quantum"
    "\x50\x61\x72\x61\x64\x6f\x78" // "Paradox"
};

// XOR key
#define XOR_KEY 0x42

// Deobfuscate function
void deobfuscate(char* str) {
    for (int i = 0; str[i] != '\0'; i++) {
        str[i] ^= XOR_KEY;
    }
}

// Fake flags
char* fake_flags[] = {
    "HTB{f4k3_fl4g_1_qu4ntum_3rr0r}",
    "HTB{f4k3_fl4g_2_paradox}",
    "HTB{qu4ntum_3nt4ngl3m3nt_s0lv3d}"
};

// Real flag (obfuscated)
char real_flag[] = "\x48\x54\x42\x7b\x71\x75\x34\x6e\x74\x75\x6d\x5f\x70\x61\x72\x61\x64\x6f\x78\x5f\x73\x30\x6c\x76\x33\x64\x5f\x32\x30\x32\x34\x5f\x72\x65\x61\x6c\x5f\x66\x6c\x61\x67\x7d";

// Main function
int main() {
    check_debug();
    
    printf("=== Quantum Paradox Challenge ===\n");
    printf("Enter your quantum key: ");
    
    char input[100];
    fgets(input, sizeof(input), stdin);
    
    // Remove newline
    input[strcspn(input, "\n")] = 0;
    
    // Check input
    if (strlen(input) == 0) {
        printf("Invalid input!\n");
        return 1;
    }
    
    // Simulate quantum processing
    printf("Processing quantum data...\n");
    sleep(1);
    
    // Show fake flags based on input
    if (strstr(input, "quantum")) {
        printf("Quantum analysis complete. Flag: %s\n", fake_flags[0]);
    } else if (strstr(input, "paradox")) {
        printf("Paradox analysis complete. Flag: %s\n", fake_flags[1]);
    } else if (strstr(input, "entanglement")) {
        printf("Entanglement analysis complete. Flag: %s\n", fake_flags[2]);
    } else {
        printf("Running quantum simulation...\n");
        sleep(2);
        printf("Simulation complete. No flag found.\n");
    }
    
    // The real flag is never displayed - it's hidden in the binary
    // It must be extracted through reverse engineering
    
    return 0;
}