#include <stdio.h>
#include <stdint.h>
#include <string.h>

// Simple XOR encryption
static void simple_encrypt(uint8_t *data, uint32_t len, uint32_t key) {
    for (uint32_t i = 0; i < len; i++) {
        data[i] ^= (key >> ((i % 4) * 8)) & 0xFF;
    }
}

int main() {
    // The flag parts
    uint8_t flag_part1[] = "HTB{QUANTUM_";
    uint8_t flag_part2[] = "LOCK_IS_BROKEN";
    uint8_t flag_part3[] = "_BY_THE_REVERSER";
    uint8_t flag_part4[] = "_MASTER}";
    
    printf("Debug - Before encryption:\n");
    printf("Part 1: %s (len: %zu)\n", flag_part1, strlen((char*)flag_part1));
    for (int i = 0; i < strlen((char*)flag_part1); i++) {
        printf("  [%d] = 0x%02X ('%c')\n", i, flag_part1[i], flag_part1[i]);
    }
    
    // Quantum keys (these will be derived from the VM registers)
    uint32_t key1 = 0xDEADBEEF ^ 0xCAFEBABE;  // reg0 ^ reg1
    uint32_t key2 = 0xFEEDFACE ^ 0xBADDCAFE;  // reg2 ^ reg3
    uint32_t key3 = 0x1337C0DE ^ 0xDEADC0DE;  // reg4 ^ reg5
    uint32_t key4 = 0xFEEDBEEF ^ 0xCAFEDEAD;  // reg6 ^ reg7
    
    printf("Original flag parts:\n");
    printf("Part 1: %s (len: %zu)\n", flag_part1, strlen((char*)flag_part1));
    printf("Part 2: %s (len: %zu)\n", flag_part2, strlen((char*)flag_part2));
    printf("Part 3: %s (len: %zu)\n", flag_part3, strlen((char*)flag_part3));
    printf("Part 4: %s (len: %zu)\n", flag_part4, strlen((char*)flag_part4));
    
    printf("\nKeys:\n");
    printf("Key 1: 0x%08X\n", key1);
    printf("Key 2: 0x%08X\n", key2);
    printf("Key 3: 0x%08X\n", key3);
    printf("Key 4: 0x%08X\n", key4);
    
    // Encrypt each part
    simple_encrypt(flag_part1, strlen((char*)flag_part1), key1);
    simple_encrypt(flag_part2, strlen((char*)flag_part2), key2);
    simple_encrypt(flag_part3, strlen((char*)flag_part3), key3);
    simple_encrypt(flag_part4, strlen((char*)flag_part4), key4);
    
    printf("\nDebug - After encryption:\n");
    printf("Part 1: %s (len: %zu)\n", flag_part1, strlen((char*)flag_part1));
    for (int i = 0; i < 12; i++) {
        printf("  [%d] = 0x%02X\n", i, flag_part1[i]);
    }
    
    printf("\nEncrypted flag parts (hex):\n");
    printf("Part 1: ");
    for (int i = 0; i < 12; i++) {
        printf("0x%02X, ", flag_part1[i]);
    }
    printf("0x00\n");
    
    printf("Part 2: ");
    for (int i = 0; i < strlen((char*)flag_part2); i++) {
        printf("0x%02X, ", flag_part2[i]);
    }
    printf("0x00\n");
    
    printf("Part 3: ");
    for (int i = 0; i < strlen((char*)flag_part3); i++) {
        printf("0x%02X, ", flag_part3[i]);
    }
    printf("0x00\n");
    
    printf("Part 4: ");
    for (int i = 0; i < strlen((char*)flag_part4); i++) {
        printf("0x%02X, ", flag_part4[i]);
    }
    printf("0x00\n");
    
    return 0;
}