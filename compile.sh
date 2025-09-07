#!/bin/bash

# Script de compilación para el challenge de reversing
# Añade múltiples capas de protección y ofuscación

echo "🔨 Compilando challenge de reverse engineering..."

# Compilar con múltiples flags de protección
gcc -o challenge challenge.c \
    -O2 \
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
    -fno-pie \
    -Wl,-z,noexecstack \
    -Wl,-z,relro \
    -Wl,-z,now

# Verificar que se compiló correctamente
if [ $? -eq 0 ]; then
    echo "✅ Compilación exitosa"
    
    # Añadir información adicional al binario
    echo "📝 Añadiendo metadatos..."
    
    # Crear un script que añada strings adicionales para confundir
    cat > add_strings.py << 'EOF'
import sys

# Strings adicionales para confundir a los analistas
confusing_strings = [
    "HTB{this_is_not_the_flag}",
    "HTB{decoy_flag_here}",
    "HTB{fake_flag_123}",
    "HTB{not_the_real_one}",
    "HTB{try_harder}",
    "HTB{keep_looking}",
    "HTB{almost_there}",
    "HTB{close_but_no}",
    "HTB{reverse_me_harder}",
    "HTB{static_analysis_needed}",
    "HTB{dynamic_analysis_required}",
    "HTB{debugging_skills_needed}",
    "HTB{assembly_required}",
    "HTB{hex_editor_helpful}",
    "HTB{strings_command_useful}",
    "HTB{objdump_analysis}",
    "HTB{gdb_debugging}",
    "HTB{radare2_analysis}",
    "HTB{ghidra_reverse}",
    "HTB{ida_pro_analysis}"
]

# Escribir strings a un archivo temporal
with open('confusing_strings.txt', 'w') as f:
    for s in confusing_strings:
        f.write(s + '\n')

print("Strings confusos añadidos")
EOF

    python3 add_strings.py
    
    # Añadir los strings al binario
    cat confusing_strings.txt >> challenge
    
    # Limpiar archivos temporales
    rm confusing_strings.txt add_strings.py
    
    echo "🎯 Challenge compilado exitosamente: ./challenge"
    echo "📊 Tamaño del binario: $(ls -lh challenge | awk '{print $5}')"
    
    # Mostrar información del binario
    echo ""
    echo "📋 Información del binario:"
    file challenge
    echo ""
    echo "🔍 Strings encontrados:"
    strings challenge | grep -E "HTB\{.*\}" | head -10
    echo ""
    echo "⚠️  Nota: Hay más strings ocultos en el binario"
    
else
    echo "❌ Error en la compilación"
    exit 1
fi