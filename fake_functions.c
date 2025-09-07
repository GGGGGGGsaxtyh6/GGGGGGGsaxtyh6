#include <stdio.h>
#include <string.h>

void fake_validation() { printf("Fake validation passed"); }

int fake_check(char* input) { return strcmp(input, "fake"); }

void fake_decrypt() { printf("Fake decryption"); }

int fake_hash(char* data) { return strlen(data) * 42; }

void fake_anti_debug() { printf("Fake anti-debug"); }

