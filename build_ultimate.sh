#!/bin/bash

echo "Compilando ULTIMATE VAULT con ofuscación extrema..."

gcc -o ultimate_vault ultimate_vault.c \
    -O3 \
    -s \
    -fno-stack-protector \
    -fno-pie \
    -no-pie \
    -static \
    -Wl,--strip-all \
    -D_FORTIFY_SOURCE=0 \
    -fno-builtin \
    -fno-ident \
    -fno-asynchronous-unwind-tables \
    -fno-unwind-tables \
    -fno-plt \
    -fno-pic \
    -Wl,-z,noexecstack \
    -Wl,-z,relro \
    -Wl,-z,now \
    -ffunction-sections \
    -fdata-sections \
    -Wl,--gc-sections \
    -fno-common \
    -fno-merge-constants \
    -fno-merge-all-constants \
    -fno-inline-functions-called-once \
    -fno-early-inlining \
    -fno-unit-at-a-time \
    -fno-toplevel-reorder \
    -fno-reorder-blocks \
    -fno-reorder-blocks-and-partition \
    -fno-reorder-functions \
    -fno-strict-aliasing \
    -fno-strict-overflow \
    -fno-delete-null-pointer-checks \
    -fno-expensive-optimizations \
    -fno-schedule-insns \
    -fno-schedule-insns2 \
    -fno-sched-spec \
    -fno-sched-spec-load \
    -fno-sched-spec-load-dangerous \
    -fno-sched-stalled-insns \
    -fno-sched-stalled-insns-dep \
    -fno-sched2-use-superblocks \
    -fno-sched2-use-traces

echo "Compilación completada. Verificando ofuscación..."

# Verificar que no hay strings visibles
echo "Verificando strings..."
strings ultimate_vault | grep -i "HTB" || echo "✓ Flag no visible con strings"
strings ultimate_vault | grep -i "smurf" || echo "✓ Contenido de flag no visible"

echo "Binario creado: ultimate_vault"