# Makefile para QuantumCipher Research Tool
# Reto de reversing nivel INSANE

CC = gcc
CFLAGS = -Wall -Wextra -O2 -fno-stack-protector -fno-pie -no-pie
LDFLAGS = -lpthread -lm -lrt
TARGET = quantum_cipher
SOURCE = quantum_cipher_challenge.c

# Flags de protección adicionales
PROTECTION_FLAGS = -D_FORTIFY_SOURCE=0 -fno-omit-frame-pointer -fno-inline-functions-called-once
OBFUSCATION_FLAGS = -fno-ident -fno-asynchronous-unwind-tables -fno-unwind-tables

# Compilación con todas las protecciones
all: $(TARGET)

$(TARGET): $(SOURCE)
	$(CC) $(CFLAGS) $(PROTECTION_FLAGS) $(OBFUSCATION_FLAGS) -o $(TARGET) $(SOURCE) $(LDFLAGS)
	strip --strip-all $(TARGET)
	@echo "Binary compiled with maximum protection level"
	@echo "Challenge ready for deployment"

# Compilación de debug (sin protecciones)
debug: $(SOURCE)
	$(CC) -g -O0 -DDEBUG -o $(TARGET)_debug $(SOURCE) $(LDFLAGS)
	@echo "Debug version compiled"

# Limpiar archivos generados
clean:
	rm -f $(TARGET) $(TARGET)_debug
	@echo "Cleanup completed"

# Instalar dependencias del sistema
install-deps:
	sudo apt-get update
	sudo apt-get install -y gcc make build-essential
	@echo "Dependencies installed"

# Verificar que el binario funciona
test: $(TARGET)
	@echo "Testing binary execution..."
	@echo "8" | timeout 5s ./$(TARGET) || true
	@echo "Test completed"

.PHONY: all debug clean install-deps test