#!/bin/bash
# Interceptor de /dev/null

# Crear un archivo temporal para capturar la salida
OUTPUT=/tmp/flag_capture.txt
> $OUTPUT

# Ejecutar el programa y capturar las escrituras a fd 3
echo | qemu-aarch64-static -strace ./poly 2>&1 | while read line; do
    if echo "$line" | grep -q "write(3"; then
        # Extraer lo que se está escribiendo
        echo "$line" >> $OUTPUT
    fi
done

echo "Escrituras a /dev/null capturadas:"
cat $OUTPUT
