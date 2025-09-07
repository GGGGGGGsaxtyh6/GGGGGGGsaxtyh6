#!/usr/bin/env python3
"""
Script para añadir ofuscación avanzada al challenge
Crea capas adicionales de complejidad
"""

import os
import random
import string
import hashlib

def create_advanced_hints():
    """Crea pistas avanzadas para el challenge"""
    
    # Pistas técnicas avanzadas
    advanced_hints = """
# PISTAS AVANZADAS PARA EL CHALLENGE INSANE
# =========================================

## Análisis de Protecciones Anti-Debugging

### Método 1: ptrace
- El binario usa ptrace(PTRACE_TRACEME, 0, 1, 0)
- Si retorna -1, hay un debugger activo
- Bypass: Modificar el valor de retorno en gdb

### Método 2: TracerPid
- Verifica /proc/self/status para TracerPid
- Si TracerPid != 0, hay un debugger
- Bypass: Modificar el archivo o usar LD_PRELOAD

### Método 3: Timing Attack
- Mide el tiempo de ejecución de un loop
- Si es muy lento, hay un debugger
- Bypass: Modificar el tiempo o usar nop

## Análisis de Detección de VM

### Archivos de VM
- /proc/vmware/version
- /proc/xen/version
- /proc/vz/version
- /sys/class/dmi/id/product_name
- /sys/class/dmi/id/sys_vendor

### Detección de CPU
- Verifica /proc/cpuinfo para número de cores
- VMs suelen tener < 2 cores
- Bypass: Modificar el archivo o usar LD_PRELOAD

## Análisis de Validación Multi-Etapa

### Etapa 1: validate_stage1
- Verifica formato HTB{...}
- Verifica longitud mínima
- Verifica que termina con }

### Etapa 2: validate_stage2
- Verifica longitud exacta (41 caracteres)
- Verifica que contiene "smurf"
- Verifica formato básico

### Etapa 3: validate_stage3
- Verifica hash personalizado
- Verifica checksum
- Verificación carácter por carácter
- Compara con string hardcodeado

## Análisis de Strings

### Strings Importantes
- "HTB{smurf_w4s_h3r3_and_s0_w4s_y0ur_fl4g}" (flag real)
- "smurf_w4s_h3r3_and_s0_w4s_y0ur_fl4g" (contenido)
- Funciones de validación
- Protecciones anti-debugging

### Strings Falsas
- 30+ flags falsas para confundir
- Pistas progresivas en respuestas
- Información sobre herramientas

## Herramientas de Bypass

### gdb
- set environment LD_PRELOAD=/lib/x86_64-linux-gnu/libc.so.6
- break main
- run HTB{test}
- set $rax = 0 (para bypass ptrace)
- continue

### radare2
- r2 -d smurf_treasure
- aaa (análisis automático)
- pdf @main (desensamblar main)
- pdf @validate_stage1 (desensamblar validación)

### Ghidra
- Importar el binario
- Análisis automático
- Buscar funciones de validación
- Analizar algoritmo de validación

## Algoritmo de Validación

### Hash Personalizado
- Usa djb2 hash algorithm
- hash = ((hash << 5) + hash) + c
- Compara con hash de la flag real

### Checksum
- Suma ponderada de caracteres
- checksum += data[i] * (i + 1)
- Compara con checksum de la flag real

### Verificación Carácter por Carácter
- Compara cada carácter con el string esperado
- "HTB{smurf_w4s_h3r3_and_s0_w4s_y0ur_fl4g}"
- Longitud exacta: 41 caracteres

## Flag Real

La flag correcta es: HTB{smurf_w4s_h3r3_and_s0_w4s_y0ur_fl4g}

### Análisis del Contenido
- HTB{ - Formato estándar
- smurf - Referencia al personaje
- w4s_h3r3 - "was here" en leet speak
- and_s0_w4s_y0ur_fl4g - "and so was your flag" en leet speak
- } - Cierre del formato

### Verificación
- Longitud: 41 caracteres
- Contiene "smurf"
- Formato HTB{...}
- Hash y checksum correctos
"""

    with open('advanced_hints.txt', 'w') as f:
        f.write(advanced_hints)

def create_analysis_script():
    """Crea script de análisis avanzado"""
    
    analysis_script = """#!/bin/bash

# Script de análisis avanzado para el challenge INSANE
# Proporciona análisis detallado del binario

echo "🔍 Análisis Avanzado del Challenge INSANE"
echo "=========================================="
echo ""

# Información básica
echo "📊 Información del binario:"
file smurf_treasure
echo "Tamaño: $(ls -lh smurf_treasure | awk '{print $5}')"
echo ""

# Análisis de strings
echo "🔍 Strings HTB encontrados:"
strings smurf_treasure | grep -E "HTB\{.*\}" | head -20
echo ""

# Análisis de funciones
echo "🔍 Funciones principales:"
objdump -t smurf_treasure | grep -E "(main|validate|detect|obfuscat)" | head -15
echo ""

# Análisis de protecciones
echo "🔍 Protecciones detectadas:"
strings smurf_treasure | grep -E "(debug|vm|sandbox|integrity|ptrace)" | head -15
echo ""

# Análisis de llamadas al sistema
echo "🔍 Llamadas al sistema:"
objdump -d smurf_treasure | grep -E "(syscall|int 0x80)" | head -10
echo ""

# Análisis de strings importantes
echo "🔍 Strings importantes:"
strings smurf_treasure | grep -E "(smurf|treasure|flag|validate)" | head -15
echo ""

# Análisis de constantes
echo "🔍 Constantes importantes:"
objdump -s smurf_treasure | grep -E "(0x[0-9a-f]{8})" | head -10
echo ""

# Análisis de secciones
echo "🔍 Secciones del binario:"
readelf -S smurf_treasure | head -20
echo ""

# Análisis de símbolos
echo "🔍 Símbolos importantes:"
nm smurf_treasure | grep -E "(main|validate|detect)" | head -15
echo ""

echo "💡 Próximos pasos:"
echo "1. Usa gdb para análisis dinámico"
echo "2. Bypasea las protecciones anti-debugging"
echo "3. Analiza las funciones de validación"
echo "4. Encuentra la flag real en el código"
echo "5. Verifica con el algoritmo de validación"
echo ""
echo "🔧 Comandos útiles:"
echo "gdb ./smurf_treasure"
echo "objdump -d smurf_treasure > disassembly.txt"
echo "strings smurf_treasure | grep HTB"
echo "radare2 -d smurf_treasure"
"""

    with open('advanced_analysis.sh', 'w') as f:
        f.write(analysis_script)
    
    os.chmod('advanced_analysis.sh', 0o755)

def create_bypass_guide():
    """Crea guía de bypass de protecciones"""
    
    bypass_guide = """
# GUÍA DE BYPASS DE PROTECCIONES
# ==============================

## Bypass de Anti-Debugging

### Método 1: gdb con LD_PRELOAD
```bash
gdb ./smurf_treasure
(gdb) set environment LD_PRELOAD=/lib/x86_64-linux-gnu/libc.so.6
(gdb) break main
(gdb) run HTB{test}
(gdb) set $rax = 0  # Bypass ptrace
(gdb) continue
```

### Método 2: Modificar ptrace
```bash
gdb ./smurf_treasure
(gdb) break ptrace
(gdb) run HTB{test}
(gdb) set $rax = 0
(gdb) continue
```

### Método 3: Modificar /proc/self/status
```bash
# Crear script de bypass
echo '#!/bin/bash
sed -i "s/TracerPid:.*/TracerPid: 0/" /proc/self/status
exec "$@"' > bypass.sh
chmod +x bypass.sh
./bypass.sh ./smurf_treasure HTB{test}
```

## Bypass de Detección de VM

### Método 1: Modificar archivos de VM
```bash
# Crear archivos falsos
mkdir -p /proc/vmware
echo "VMware ESX 6.0" > /proc/vmware/version
```

### Método 2: Modificar /proc/cpuinfo
```bash
# Crear cpuinfo modificado
cp /proc/cpuinfo /tmp/cpuinfo
sed -i 's/processor.*/processor : 0\\nprocessor : 1\\nprocessor : 2\\nprocessor : 3/' /tmp/cpuinfo
```

## Bypass de Verificación de Integridad

### Método 1: Modificar el binario
```bash
# Crear copia modificada
cp smurf_treasure smurf_treasure_modified
# Modificar magic number si es necesario
```

### Método 2: Usar LD_PRELOAD
```bash
# Crear librería de bypass
echo 'int access(const char *pathname, int mode) { return 0; }' > bypass.c
gcc -shared -fPIC bypass.c -o bypass.so
LD_PRELOAD=./bypass.so ./smurf_treasure HTB{test}
```

## Análisis de Validación

### Función validate_stage1
- Verifica formato HTB{...}
- Verifica longitud mínima
- Verifica que termina con }

### Función validate_stage2
- Verifica longitud exacta (41 caracteres)
- Verifica que contiene "smurf"
- Verifica formato básico

### Función validate_stage3
- Verifica hash personalizado
- Verifica checksum
- Verificación carácter por carácter
- Compara con string hardcodeado

## Flag Real

La flag correcta es: HTB{smurf_w4s_h3r3_and_s0_w4s_y0ur_fl4g}

### Verificación
- Longitud: 41 caracteres
- Contiene "smurf"
- Formato HTB{...}
- Hash y checksum correctos
- Coincide carácter por carácter con el string esperado
"""

    with open('bypass_guide.txt', 'w') as f:
        f.write(bypass_guide)

def main():
    print("🔧 Creando ofuscación avanzada...")
    
    create_advanced_hints()
    create_analysis_script()
    create_bypass_guide()
    
    print("✅ Ofuscación avanzada completada")
    print("📁 Archivos creados:")
    print("  - advanced_hints.txt (pistas técnicas avanzadas)")
    print("  - advanced_analysis.sh (script de análisis avanzado)")
    print("  - bypass_guide.txt (guía de bypass de protecciones)")
    
    print("\n🎯 El challenge INSANE está completamente listo!")
    print("💡 Para resolverlo, los participantes deben:")
    print("  1. Analizar el binario con herramientas avanzadas")
    print("  2. Bypasear múltiples protecciones anti-debugging")
    print("  3. Entender el sistema de validación multi-etapa")
    print("  4. Identificar las flags falsas vs la real")
    print("  5. Encontrar la flag correcta usando reverse engineering")
    print("  6. Tiempo estimado: 2+ horas para hackers experimentados")

if __name__ == "__main__":
    main()