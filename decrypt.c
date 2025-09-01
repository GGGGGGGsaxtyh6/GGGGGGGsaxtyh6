#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/mman.h>
#include <unistd.h>

#define KEY_LEN 32

void decrypt_block(uint8_t *ret_char, uint8_t char_to_xor, int counter, const uint8_t *key, size_t len_key) {
    uint8_t key_char = key[counter % len_key];
    *ret_char = char_to_xor ^ key_char;  // XOR es simétrico!
}

void decrypt_file(const char *encrypted_filepath, const uint8_t *key, size_t len_key) {
    char *orig_filepath;
    int encfile_fd, origfile_fd;
    struct stat st;
    int i;
    uint8_t *mem, *newmem;
    
    // Remover la extensión .osiris
    orig_filepath = strdup(encrypted_filepath);
    char *ext = strstr(orig_filepath, ".osiris");
    if (ext) {
        *ext = '\0';  // Cortar la extensión
    }
    
    printf("Desencriptando: %s -> %s\n", encrypted_filepath, orig_filepath);
    
    if ((encfile_fd = open(encrypted_filepath, O_RDONLY)) < 0) {
        fprintf(stderr, "[!] No pude abrir archivo cifrado %s\n", encrypted_filepath);
        return;
    }
    
    if (fstat(encfile_fd, &st) < 0) {
        fprintf(stderr, "[!] fstat falló %s\n", encrypted_filepath);
        return;
    }
    
    if (st.st_size == 0) {
        printf("Archivo vacío, saltando: %s\n", encrypted_filepath);
        close(encfile_fd);
        return;
    }
    
    // Crear archivo original
    if ((origfile_fd = open(orig_filepath, O_WRONLY | O_CREAT | O_TRUNC, 0644)) < 0) {
        fprintf(stderr, "[!] No pude crear archivo original %s\n", orig_filepath);
        return;
    }
    
    // Mapear archivo cifrado
    mem = (uint8_t *)mmap(NULL, st.st_size, PROT_READ, MAP_PRIVATE, encfile_fd, 0);
    if (mem == MAP_FAILED) {
        fprintf(stderr, "[!] mmap falló\n");
        return;
    }
    
    newmem = (uint8_t *)malloc(st.st_size);
    
    // ¡DESENCRIPTAR!
    for (i = 0; i < st.st_size; i++) {
        decrypt_block(&newmem[i], mem[i], i, key, len_key);
    }
    
    // Escribir archivo desencriptado
    if ((write(origfile_fd, newmem, st.st_size)) <= 0) {
        fprintf(stderr, "[!] write falló %s\n", orig_filepath);
        return;
    }
    
    printf("✅ RECUPERADO: %s\n", orig_filepath);
    
    // Limpiar
    free(newmem);
    munmap(mem, st.st_size);
    close(origfile_fd);
    close(encfile_fd);
    
    // Eliminar archivo cifrado
    remove(encrypted_filepath);
}

int main() {
    // LA CLAVE CAPTURADA DEL RANSOMWARE
    const char *key = "FA37jNCchRYdSBZAYY4CbwdXs22jJZHm";
    
    printf("🔓 INICIANDO DESENCRIPTACIÓN CON CLAVE: %s\n", key);
    
    // Desencriptar todos los archivos .osiris
    decrypt_file("asdsdsad.osiris", (const uint8_t *)key, KEY_LEN);
    decrypt_file(".git.osiris", (const uint8_t *)key, KEY_LEN);
    
    printf("🎉 ¡DESENCRIPTACIÓN COMPLETADA!\n");
    return 0;
}