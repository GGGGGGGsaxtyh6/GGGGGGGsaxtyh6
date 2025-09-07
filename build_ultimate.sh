#!/bin/bash

# Script de compilación para challenge ULTRA-INSANE de reverse engineering
# Añade múltiples capas de protección ultra-avanzadas y ofuscación

echo "🔥 Construyendo challenge ULTRA-INSANE de reverse engineering..."
echo "⚠️  Este challenge está diseñado para tomar 4+ horas"
echo ""

# Verificar dependencias
echo "🔍 Verificando dependencias..."
if ! command -v gcc &> /dev/null; then
    echo "❌ gcc no encontrado"
    exit 1
fi

if ! command -v objcopy &> /dev/null; then
    echo "❌ objcopy no encontrado"
    exit 1
fi

if ! command -v strip &> /dev/null; then
    echo "❌ strip no encontrado"
    exit 1
fi

echo "✅ Dependencias verificadas"
echo ""

# Compilar con múltiples flags de protección ultra-avanzadas
echo "🔨 Compilando con protecciones ultra-avanzadas..."

gcc -o ultimate_challenge ultimate_challenge.c \
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

if [ $? -ne 0 ]; then
    echo "❌ Error en la compilación"
    exit 1
fi

echo "✅ Compilación ultra-exitosa"
echo ""

# Añadir strings confusos ultra
echo "🔧 Añadiendo strings confusos ultra..."

# Crear strings adicionales ultra para confundir
cat > add_ultra_confusing_strings.py << 'EOF'
import sys
import random
import string

# Generar strings confusos ultra
ultra_confusing_strings = [
    "HTB{this_is_definitely_fake_ultra}",
    "HTB{not_the_real_flag_at_all_ultra}",
    "HTB{decoy_flag_here_ultra}",
    "HTB{fake_solution_script_ultra}",
    "HTB{try_harder_next_time_ultra}",
    "HTB{keep_looking_deeper_ultra}",
    "HTB{almost_there_but_not_quite_ultra}",
    "HTB{close_but_no_cigar_ultra}",
    "HTB{reverse_me_harder_please_ultra}",
    "HTB{static_analysis_is_required_ultra}",
    "HTB{dynamic_analysis_is_needed_ultra}",
    "HTB{debugging_skills_required_ultra}",
    "HTB{assembly_knowledge_needed_ultra}",
    "HTB{hex_editor_will_help_ultra}",
    "HTB{strings_command_is_useful_ultra}",
    "HTB{objdump_analysis_required_ultra}",
    "HTB{gdb_debugging_skills_ultra}",
    "HTB{radare2_analysis_needed_ultra}",
    "HTB{ghidra_reverse_engineering_ultra}",
    "HTB{ida_pro_analysis_required_ultra}",
    "HTB{smurf_was_here_but_flag_is_different_ultra}",
    "HTB{smurf_left_clues_but_not_this_ultra}",
    "HTB{smurf_treasure_is_hidden_deeper_ultra}",
    "HTB{smurf_used_advanced_obfuscation_ultra}",
    "HTB{smurf_protected_his_treasure_well_ultra}",
    "HTB{smurf_w4s_h3r3_but_this_is_fake_ultra}",
    "HTB{smurf_w4s_h3r3_and_s0_w4s_y0ur_fl4g_fake_ultra}",
    "HTB{smurf_w4s_h3r3_and_s0_w4s_y0ur_fl4g_wrong_ultra}",
    "HTB{smurf_w4s_h3r3_and_s0_w4s_y0ur_fl4g_false_ultra}",
    "HTB{smurf_w4s_h3r3_and_s0_w4s_y0ur_fl4g_decoy_ultra}",
    "HTB{ultra_fake_flag_1}",
    "HTB{ultra_fake_flag_2}",
    "HTB{ultra_fake_flag_3}",
    "HTB{ultra_fake_flag_4}",
    "HTB{ultra_fake_flag_5}",
    "HTB{ultra_fake_flag_6}",
    "HTB{ultra_fake_flag_7}",
    "HTB{ultra_fake_flag_8}",
    "HTB{ultra_fake_flag_9}",
    "HTB{ultra_fake_flag_10}",
    "HTB{ultra_fake_flag_11}",
    "HTB{ultra_fake_flag_12}",
    "HTB{ultra_fake_flag_13}",
    "HTB{ultra_fake_flag_14}",
    "HTB{ultra_fake_flag_15}",
    "HTB{ultra_fake_flag_16}",
    "HTB{ultra_fake_flag_17}",
    "HTB{ultra_fake_flag_18}",
    "HTB{ultra_fake_flag_19}",
    "HTB{ultra_fake_flag_20}"
]

# Strings adicionales ultra para confundir
ultra_additional_strings = [
    "This is not the flag you are looking for ultra",
    "Keep searching, the real flag is hidden ultra",
    "Smurf was here but left no trace ultra",
    "The treasure is well hidden ultra",
    "Advanced reverse engineering required ultra",
    "Multiple analysis techniques needed ultra",
    "Static and dynamic analysis required ultra",
    "Anti-debugging protections active ultra",
    "VM and sandbox detection enabled ultra",
    "Integrity checks in place ultra",
    "Multi-stage validation implemented ultra",
    "String obfuscation active ultra",
    "Control flow obfuscation enabled ultra",
    "Dead code injection complete ultra",
    "False positive flags generated ultra",
    "Progressive hint system active ultra",
    "Challenge difficulty: ULTRA-INSANE ultra",
    "Estimated time: 4+ hours ultra",
    "HackTheBox level challenge ultra",
    "Professional reverse engineering required ultra",
    "Ultra-advanced anti-debugging active ultra",
    "Ultra-advanced VM detection enabled ultra",
    "Ultra-advanced sandbox detection active ultra",
    "Ultra-advanced integrity checks in place ultra",
    "Ultra-advanced multi-stage validation ultra",
    "Ultra-advanced string obfuscation active ultra",
    "Ultra-advanced control flow obfuscation ultra",
    "Ultra-advanced dead code injection ultra",
    "Ultra-advanced false positive flags ultra",
    "Ultra-advanced progressive hint system ultra"
]

# Escribir strings a archivos
with open('ultra_confusing_strings.txt', 'w') as f:
    for s in ultra_confusing_strings:
        f.write(s + '\n')

with open('ultra_additional_strings.txt', 'w') as f:
    for s in ultra_additional_strings:
        f.write(s + '\n')

print("Strings confusos ultra generados")
EOF

python3 add_ultra_confusing_strings.py

# Añadir strings al binario
cat ultra_confusing_strings.txt >> ultimate_challenge
cat ultra_additional_strings.txt >> ultimate_challenge

# Limpiar archivos temporales
rm ultra_confusing_strings.txt ultra_additional_strings.txt add_ultra_confusing_strings.py

echo "✅ Strings confusos ultra añadidos"
echo ""

# Crear archivos auxiliares ultra
echo "📁 Creando archivos auxiliares ultra..."

# Crear archivo de pistas ultra
cat > ultra_hints.txt << 'EOF'
# PISTAS ULTRA PARA EL CHALLENGE ULTRA-INSANE
# ============================================

## Pista 1: Análisis Estático Ultra
- Usa 'strings ultimate_challenge | grep HTB' para ver todas las flags
- La flag real comienza con: HTB{smurf_
- Hay muchas flags falsas ultra, no te confundas
- Usa 'objdump -d ultimate_challenge' para ver el assembly

## Pista 2: Análisis Dinámico Ultra
- El binario tiene protecciones anti-debugging ultra-avanzadas
- Usa gdb para bypasear las protecciones ultra-avanzadas
- Comando: gdb ./ultimate_challenge
- Bypass ultra: set environment LD_PRELOAD=/lib/x86_64-linux-gnu/libc.so.6

## Pista 3: Protecciones Ultra
- Anti-debugging ultra: ptrace, /proc/self/status, timing attacks, breakpoints, /proc/self/maps
- VM detection ultra: archivos típicos de VM, CPU cores, memoria, características
- Sandbox detection ultra: verificación de entorno, recursos, procesos, variables
- Integrity check ultra: verificación del binario, checksum
- Analysis detection: detección de herramientas de análisis

## Pista 4: Validación Ultra-Multi-etapa
- Etapa 1: Formato básico (HTB{...})
- Etapa 2: Longitud y contenido (41 chars, contiene "smurf")
- Etapa 3: Validación ultra-completa (hash ultra, checksum ultra, carácter por carácter)

## Pista 5: La Flag Real Ultra
- La flag correcta es: HTB{smurf_w4s_h3r3_and_s0_w4s_y0ur_fl4g}
- Pero debes encontrarla por ti mismo usando reverse engineering ultra
- El algoritmo de validación está en las funciones validate_stage*_ultra

## Herramientas Ultra Recomendadas:
- strings, objdump, hexdump, file, readelf, nm
- gdb, strace, ltrace, gdb-peda
- radare2, ghidra, ida pro, binary ninja
- Análisis estático y dinámico ultra combinados
EOF

# Crear archivo de flags falsas ultra
cat > ultra_fake_flags.txt << 'EOF'
# FLAGS FALSAS ULTRA - NO SON LA FLAG REAL
# ========================================

HTB{this_is_definitely_fake_ultra}
HTB{not_the_real_flag_at_all_ultra}
HTB{decoy_flag_here_ultra}
HTB{fake_solution_script_ultra}
HTB{try_harder_next_time_ultra}
HTB{keep_looking_deeper_ultra}
HTB{almost_there_but_not_quite_ultra}
HTB{close_but_no_cigar_ultra}
HTB{reverse_me_harder_please_ultra}
HTB{static_analysis_is_required_ultra}
HTB{dynamic_analysis_is_needed_ultra}
HTB{debugging_skills_required_ultra}
HTB{assembly_knowledge_needed_ultra}
HTB{hex_editor_will_help_ultra}
HTB{strings_command_is_useful_ultra}
HTB{objdump_analysis_required_ultra}
HTB{gdb_debugging_skills_ultra}
HTB{radare2_analysis_needed_ultra}
HTB{ghidra_reverse_engineering_ultra}
HTB{ida_pro_analysis_required_ultra}

# La flag real comienza con: HTB{smurf_
# Tiene exactamente 41 caracteres
# Contiene información sobre Smurf
# Está ultra-ofuscada en el binario
EOF

# Crear script de análisis ultra
cat > ultra_analyze.sh << 'EOF'
#!/bin/bash

echo "🔍 Análisis Ultra del Challenge ULTRA-INSANE"
echo "============================================="
echo ""

# Información básica
echo "📊 Información del binario:"
file ultimate_challenge
echo "Tamaño: $(ls -lh ultimate_challenge | awk '{print $5}')"
echo ""

# Análisis de strings
echo "🔍 Strings HTB encontrados:"
strings ultimate_challenge | grep -E "HTB\{.*\}" | head -25
echo ""

# Análisis de funciones
echo "🔍 Funciones principales:"
objdump -t ultimate_challenge | grep -E "(main|validate|detect|obfuscat)" | head -20
echo ""

# Análisis de protecciones
echo "🔍 Protecciones detectadas:"
strings ultimate_challenge | grep -E "(debug|vm|sandbox|integrity|ptrace|analysis)" | head -20
echo ""

# Análisis de llamadas al sistema
echo "🔍 Llamadas al sistema:"
objdump -d ultimate_challenge | grep -E "(syscall|int 0x80)" | head -15
echo ""

# Análisis de strings importantes
echo "🔍 Strings importantes:"
strings ultimate_challenge | grep -E "(smurf|treasure|flag|validate|ultra)" | head -20
echo ""

# Análisis de constantes
echo "🔍 Constantes importantes:"
objdump -s ultimate_challenge | grep -E "(0x[0-9a-f]{8})" | head -15
echo ""

# Análisis de secciones
echo "🔍 Secciones del binario:"
readelf -S ultimate_challenge | head -25
echo ""

# Análisis de símbolos
echo "🔍 Símbolos importantes:"
nm ultimate_challenge | grep -E "(main|validate|detect)" | head -20
echo ""

echo "💡 Próximos pasos ultra:"
echo "1. Usa gdb para análisis dinámico ultra"
echo "2. Bypasea las protecciones anti-debugging ultra-avanzadas"
echo "3. Analiza las funciones de validación ultra"
echo "4. Encuentra la flag real ultra-ofuscada en el código"
echo "5. Verifica con el algoritmo de validación ultra"
echo ""
echo "🔧 Comandos útiles ultra:"
echo "gdb ./ultimate_challenge"
echo "objdump -d ultimate_challenge > ultra_disassembly.txt"
echo "strings ultimate_challenge | grep HTB"
echo "radare2 -d ultimate_challenge"
EOF

chmod +x ultra_analyze.sh

echo "✅ Archivos auxiliares ultra creados"
echo ""

# Mostrar información final
echo "🎯 Challenge ULTRA-INSANE construido exitosamente!"
echo ""
echo "📁 Archivos creados:"
echo "  - ultimate_challenge (binario principal)"
echo "  - ultra_hints.txt (pistas ultra para resolver)"
echo "  - ultra_fake_flags.txt (flags falsas ultra)"
echo "  - ultra_analyze.sh (script de análisis ultra)"
echo ""
echo "📊 Información del binario:"
file ultimate_challenge
echo "Tamaño: $(ls -lh ultimate_challenge | awk '{print $5}')"
echo ""
echo "🔍 Strings HTB encontrados:"
strings ultimate_challenge | grep -E "HTB\{.*\}" | head -15
echo ""
echo "⚠️  Nota: Hay muchas más strings ultra ocultas en el binario"
echo ""
echo "🎯 Para resolver este challenge ultra:"
echo "1. Lee ultra_hints.txt para pistas ultra"
echo "2. Usa ultra_analyze.sh para análisis inicial ultra"
echo "3. Combina análisis estático y dinámico ultra-avanzado"
echo "4. Bypasea las protecciones anti-debugging ultra-avanzadas"
echo "5. Encuentra la flag real ultra-ofuscada: HTB{smurf_w4s_h3r3_and_s0_w4s_y0ur_fl4g}"
echo ""
echo "🔥 ¡Este challenge está diseñado para tomar 4+ horas!"
echo "💡 ¡Buena suerte con el reverse engineering ultra!"