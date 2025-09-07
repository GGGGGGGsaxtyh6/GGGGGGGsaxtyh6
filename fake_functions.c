/*
 * Fake functions and red herrings to confuse reverse engineers
 * These functions look important but are actually useless
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

// Fake flag decryption functions
void fake_flag_decrypt_v1(uint8_t *data, uint32_t len) {
    // This looks like it decrypts the flag but it's fake
    for (uint32_t i = 0; i < len; i++) {
        data[i] ^= 0x42;
    }
}

void fake_flag_decrypt_v2(uint8_t *data, uint32_t len) {
    // Another fake decryption function
    for (uint32_t i = 0; i < len; i++) {
        data[i] = ((data[i] + 0x13) % 256);
    }
}

void fake_flag_decrypt_v3(uint8_t *data, uint32_t len) {
    // Yet another fake decryption function
    for (uint32_t i = 0; i < len; i++) {
        data[i] ^= (i * 0x37) & 0xFF;
    }
}

// Fake neural network functions
void fake_neural_forward_pass() {
    // This looks like neural network forward pass but it's fake
    printf("Fake neural forward pass executed\n");
}

void fake_neural_backward_pass() {
    // This looks like neural network backward pass but it's fake
    printf("Fake neural backward pass executed\n");
}

void fake_neural_training() {
    // This looks like neural network training but it's fake
    printf("Fake neural training executed\n");
}

// Fake VM functions
void fake_vm_execute_instruction(uint8_t opcode) {
    // This looks like VM instruction execution but it's fake
    printf("Fake VM instruction %02X executed\n", opcode);
}

void fake_vm_load_bytecode() {
    // This looks like VM bytecode loading but it's fake
    printf("Fake VM bytecode loaded\n");
}

// Fake anti-analysis functions
void fake_anti_debug_check() {
    // This looks like anti-debugging but it's fake
    printf("Fake anti-debug check executed\n");
}

void fake_vm_detection() {
    // This looks like VM detection but it's fake
    printf("Fake VM detection executed\n");
}

// Fake flag parts (these are NOT the real flag)
static const uint8_t fake_flag_part1[] = "HTB{FAKE_FLAG_PART_1}";
static const uint8_t fake_flag_part2[] = "HTB{FAKE_FLAG_PART_2}";
static const uint8_t fake_flag_part3[] = "HTB{FAKE_FLAG_PART_3}";
static const uint8_t fake_flag_part4[] = "HTB{FAKE_FLAG_PART_4}";

// Fake flag reconstruction
void fake_reconstruct_flag() {
    printf("Fake flag: %s%s%s%s\n", fake_flag_part1, fake_flag_part2, fake_flag_part3, fake_flag_part4);
}

// Fake encryption keys
static const uint32_t fake_keys[] = {
    0x12345678, 0x87654321, 0xABCDEF00, 0x00FEDCBA,
    0x11111111, 0x22222222, 0x33333333, 0x44444444
};

// Fake decryption with fake keys
void fake_decrypt_with_keys(uint8_t *data, uint32_t len) {
    for (uint32_t i = 0; i < len; i++) {
        data[i] ^= fake_keys[i % 8] >> ((i % 4) * 8);
    }
}

// Fake neural constants
static const double fake_neural_constants[] = {
    1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0
};

// Fake neural network initialization
void fake_init_neural_network() {
    printf("Fake neural network initialized with constants: ");
    for (int i = 0; i < 8; i++) {
        printf("%.1f ", fake_neural_constants[i]);
    }
    printf("\n");
}

// Fake VM initialization
void fake_init_vm() {
    printf("Fake VM initialized\n");
}

// Fake bytecode generation
void fake_generate_bytecode() {
    printf("Fake bytecode generated\n");
}

// Fake corruption detection
void fake_detect_corruption() {
    printf("Fake corruption detected\n");
}

// Fake flag verification
int fake_verify_flag() {
    printf("Fake flag verification failed\n");
    return 0;
}

// Fake main function that looks important
void fake_main_analysis() {
    printf("=== FAKE NEURAL ANALYSIS ===\n");
    fake_init_neural_network();
    fake_init_vm();
    fake_generate_bytecode();
    fake_neural_forward_pass();
    fake_neural_backward_pass();
    fake_neural_training();
    fake_detect_corruption();
    fake_reconstruct_flag();
    fake_verify_flag();
    printf("=== FAKE ANALYSIS COMPLETE ===\n");
}