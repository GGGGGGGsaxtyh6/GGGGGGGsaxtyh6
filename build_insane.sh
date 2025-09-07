#!/bin/bash

# Script de compilación para challenge INSANE de reverse engineering
# Añade múltiples capas de protección y ofuscación

echo "🔥 Construyendo challenge INSANE de reverse engineering..."
echo "⚠️  Este challenge está diseñado para tomar 2+ horas"
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

# Compilar con múltiples flags de protección
echo "🔨 Compilando con protecciones avanzadas..."

gcc -o smurf_treasure smurf_treasure.c \
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
    -fno-merge-all-constants

if [ $? -ne 0 ]; then
    echo "❌ Error en la compilación"
    exit 1
fi

echo "✅ Compilación exitosa"
echo ""

# Añadir strings confusos
echo "🔧 Añadiendo strings confusos..."

# Crear strings adicionales para confundir
cat > add_confusing_strings.py << 'EOF'
import sys
import random
import string

# Generar strings confusos
confusing_strings = [
    "HTB{this_is_definitely_fake}",
    "HTB{not_the_real_flag_at_all}",
    "HTB{decoy_flag_here}",
    "HTB{fake_solution_script}",
    "HTB{try_harder_next_time}",
    "HTB{keep_looking_deeper}",
    "HTB{almost_there_but_not_quite}",
    "HTB{close_but_no_cigar}",
    "HTB{reverse_me_harder_please}",
    "HTB{static_analysis_is_required}",
    "HTB{dynamic_analysis_is_needed}",
    "HTB{debugging_skills_required}",
    "HTB{assembly_knowledge_needed}",
    "HTB{hex_editor_will_help}",
    "HTB{strings_command_is_useful}",
    "HTB{objdump_analysis_required}",
    "HTB{gdb_debugging_skills}",
    "HTB{radare2_analysis_needed}",
    "HTB{ghidra_reverse_engineering}",
    "HTB{ida_pro_analysis_required}",
    "HTB{smurf_was_here_but_flag_is_different}",
    "HTB{smurf_left_clues_but_not_this}",
    "HTB{smurf_treasure_is_hidden_deeper}",
    "HTB{smurf_used_advanced_obfuscation}",
    "HTB{smurf_protected_his_treasure_well}",
    "HTB{smurf_w4s_h3r3_but_this_is_fake}",
    "HTB{smurf_w4s_h3r3_and_s0_w4s_y0ur_fl4g_fake}",
    "HTB{smurf_w4s_h3r3_and_s0_w4s_y0ur_fl4g_wrong}",
    "HTB{smurf_w4s_h3r3_and_s0_w4s_y0ur_fl4g_false}",
    "HTB{smurf_w4s_h3r3_and_s0_w4s_y0ur_fl4g_decoy}"
]

# Strings adicionales para confundir
additional_strings = [
    "This is not the flag you are looking for",
    "Keep searching, the real flag is hidden",
    "Smurf was here but left no trace",
    "The treasure is well hidden",
    "Advanced reverse engineering required",
    "Multiple analysis techniques needed",
    "Static and dynamic analysis required",
    "Anti-debugging protections active",
    "VM and sandbox detection enabled",
    "Integrity checks in place",
    "Multi-stage validation implemented",
    "String obfuscation active",
    "Control flow obfuscation enabled",
    "Dead code injection complete",
    "False positive flags generated",
    "Progressive hint system active",
    "Challenge difficulty: INSANE",
    "Estimated time: 2+ hours",
    "HackTheBox level challenge",
    "Professional reverse engineering required"
]

# Escribir strings a archivos
with open('confusing_strings.txt', 'w') as f:
    for s in confusing_strings:
        f.write(s + '\n')

with open('additional_strings.txt', 'w') as f:
    for s in additional_strings:
        f.write(s + '\n')

print("Strings confusos generados")
EOF

python3 add_confusing_strings.py

# Añadir strings al binario
cat confusing_strings.txt >> smurf_treasure
cat additional_strings.txt >> smurf_treasure

# Limpiar archivos temporales
rm confusing_strings.txt additional_strings.txt add_confusing_strings.py

echo "✅ Strings confusos añadidos"
echo ""

# Crear archivos auxiliares
echo "📁 Creando archivos auxiliares..."

# Crear archivo de pistas
cat > hints.txt << 'EOF'
# PISTAS PARA EL CHALLENGE INSANE
# ================================

## Pista 1: Análisis Estático
- Usa 'strings smurf_treasure | grep HTB' para ver todas las flags
- La flag real comienza con: HTB{smurf_
- Hay muchas flags falsas, no te confundas
- Usa 'objdump -d smurf_treasure' para ver el assembly

## Pista 2: Análisis Dinámico
- El binario tiene protecciones anti-debugging
- Usa gdb para bypasear las protecciones
- Comando: gdb ./smurf_treasure
- Bypass: set environment LD_PRELOAD=/lib/x86_64-linux-gnu/libc.so.6

## Pista 3: Protecciones
- Anti-debugging: ptrace, /proc/self/status, timing attacks
- VM detection: archivos típicos de VM
- Sandbox detection: verificación de entorno
- Integrity check: verificación del binario

## Pista 4: Validación Multi-etapa
- Etapa 1: Formato básico (HTB{...})
- Etapa 2: Longitud y contenido (41 chars, contiene "smurf")
- Etapa 3: Validación completa (hash, checksum, carácter por carácter)

## Pista 5: La Flag Real
- La flag correcta es: HTB{smurf_w4s_h3r3_and_s0_w4s_y0ur_fl4g}
- Pero debes encontrarla por ti mismo usando reverse engineering
- El algoritmo de validación está en las funciones validate_stage*

## Herramientas Recomendadas:
- strings, objdump, hexdump, file, readelf
- gdb, strace, ltrace
- radare2, ghidra, ida pro
- Análisis estático y dinámico combinados
EOF

# Crear archivo de flags falsas
cat > fake_flags.txt << 'EOF'
# FLAGS FALSAS - NO SON LA FLAG REAL
# ===================================

HTB{this_is_definitely_fake}
HTB{not_the_real_flag_at_all}
HTB{decoy_flag_here}
HTB{fake_solution_script}
HTB{try_harder_next_time}
HTB{keep_looking_deeper}
HTB{almost_there_but_not_quite}
HTB{close_but_no_cigar}
HTB{reverse_me_harder_please}
HTB{static_analysis_is_required}
HTB{dynamic_analysis_is_needed}
HTB{debugging_skills_required}
HTB{assembly_knowledge_needed}
HTB{hex_editor_will_help}
HTB{strings_command_is_useful}
HTB{objdump_analysis_required}
HTB{gdb_debugging_skills}
HTB{radare2_analysis_needed}
HTB{ghidra_reverse_engineering}
HTB{ida_pro_analysis_required}

# La flag real comienza con: HTB{smurf_
# Tiene exactamente 41 caracteres
# Contiene información sobre Smurf
EOF

# Crear script de análisis
cat > analyze.sh << 'EOF'
#!/bin/bash

echo "🔍 Análisis del challenge INSANE"
echo "================================"
echo ""

echo "📊 Información del binario:"
file smurf_treasure
echo "Tamaño: $(ls -lh smurf_treasure | awk '{print $5}')"
echo ""

echo "🔍 Strings HTB encontrados:"
strings smurf_treasure | grep -E "HTB\{.*\}" | head -20
echo ""

echo "🔍 Funciones principales:"
objdump -t smurf_treasure | grep -E "(main|validate|detect)" | head -10
echo ""

echo "🔍 Protecciones detectadas:"
strings smurf_treasure | grep -E "(debug|vm|sandbox|integrity)" | head -10
echo ""

echo "💡 Próximos pasos:"
echo "1. Analiza el assembly con: objdump -d smurf_treasure"
echo "2. Busca la función main y las funciones de validación"
echo "3. Identifica las protecciones anti-debugging"
echo "4. Bypasea las protecciones con gdb"
echo "5. Encuentra la flag real en el código"
EOF

chmod +x analyze.sh

echo "✅ Archivos auxiliares creados"
echo ""

# Mostrar información final
echo "🎯 Challenge INSANE construido exitosamente!"
echo ""
echo "📁 Archivos creados:"
echo "  - smurf_treasure (binario principal)"
echo "  - hints.txt (pistas para resolver)"
echo "  - fake_flags.txt (flags falsas)"
echo "  - analyze.sh (script de análisis)"
echo ""
echo "📊 Información del binario:"
file smurf_treasure
echo "Tamaño: $(ls -lh smurf_treasure | awk '{print $5}')"
echo ""
echo "🔍 Strings HTB encontrados:"
strings smurf_treasure | grep -E "HTB\{.*\}" | head -10
echo ""
echo "⚠️  Nota: Hay muchas más strings ocultas en el binario"
echo ""
echo "🎯 Para resolver este challenge:"
echo "1. Lee hints.txt para pistas"
echo "2. Usa analyze.sh para análisis inicial"
echo "3. Combina análisis estático y dinámico"
echo "4. Bypasea las protecciones anti-debugging"
echo "5. Encuentra la flag real: HTB{smurf_w4s_h3r3_and_s0_w4s_y0ur_fl4g}"
echo ""
echo "🔥 ¡Este challenge está diseñado para tomar 2+ horas!"
echo "💡 ¡Buena suerte con el reverse engineering!"