#!/bin/bash

# Script de prueba para el challenge INSANE
# Verifica que todas las funcionalidades trabajen correctamente

echo "🧪 Probando el challenge INSANE de reverse engineering..."
echo "⚠️  Este challenge está diseñado para tomar 2+ horas"
echo ""

# Verificar que el binario existe
if [ ! -f "./smurf_treasure" ]; then
    echo "❌ Error: El binario 'smurf_treasure' no existe"
    echo "💡 Ejecuta './build_insane.sh' primero"
    exit 1
fi

echo "✅ Binario encontrado"
echo ""

# Mostrar información del binario
echo "📊 Información del binario:"
echo "Tamaño: $(ls -lh smurf_treasure | awk '{print $5}')"
echo "Tipo: $(file smurf_treasure | cut -d: -f2-)"
echo ""

# Probar con flags falsas
echo "🔍 Probando flags falsas..."
echo ""

fake_flags=(
    "HTB{fake_flag_1_here}"
    "HTB{not_the_real_flag}"
    "HTB{decoy_flag_123}"
    "HTB{this_is_not_the_flag}"
    "HTB{try_harder}"
    "HTB{smurf_was_here_but_flag_is_different}"
    "HTB{smurf_w4s_h3r3_but_this_is_fake}"
)

for flag in "${fake_flags[@]}"; do
    echo "Probando: $flag"
    timeout 5 ./smurf_treasure "$flag" 2>&1 | head -5
    echo ""
done

# Probar con la flag real
echo "🎯 Probando la flag real..."
echo ""

real_flag="HTB{smurf_w4s_h3r3_and_s0_w4s_y0ur_fl4g}"
echo "Probando: $real_flag"
timeout 10 ./smurf_treasure "$real_flag"
echo ""

# Probar con entrada inválida
echo "❌ Probando entrada inválida..."
echo ""

echo "Probando sin argumentos:"
./smurf_treasure 2>&1 | head -2
echo ""

echo "Probando flag muy corta:"
timeout 5 ./smurf_treasure "HTB{short}" 2>&1 | head -3
echo ""

echo "Probando flag muy larga:"
timeout 5 ./smurf_treasure "HTB{this_flag_is_way_too_long_to_be_valid}" 2>&1 | head -3
echo ""

echo "Probando flag sin formato HTB:"
timeout 5 ./smurf_treasure "FLAG{test}" 2>&1 | head -3
echo ""

# Mostrar strings HTB
echo "🔍 Strings HTB encontrados:"
strings smurf_treasure | grep -E "HTB\{.*\}" | head -15
echo ""

# Mostrar funciones principales
echo "🔍 Funciones principales:"
objdump -t smurf_treasure | grep -E "(main|validate|detect)" | head -10
echo ""

# Mostrar protecciones
echo "🔍 Protecciones detectadas:"
strings smurf_treasure | grep -E "(debug|vm|sandbox|integrity)" | head -10
echo ""

# Mostrar archivos auxiliares
echo "📁 Archivos auxiliares:"
ls -la *.txt *.sh 2>/dev/null | grep -v test_insane.sh
echo ""

echo "✅ Pruebas completadas"
echo ""
echo "🎯 El challenge INSANE está listo para usar!"
echo "💡 La flag correcta es: $real_flag"
echo "⚠️  Recuerda: Todas las demás flags son falsas"
echo ""
echo "🔥 Este challenge requiere:"
echo "   - Análisis estático avanzado"
echo "   - Bypass de protecciones anti-debugging"
echo "   - Análisis dinámico con gdb"
echo "   - Identificación de flags falsas"
echo "   - Ingeniería inversa de algoritmos"
echo "   - Tiempo estimado: 2+ horas"
echo ""
echo "📚 Lee hints.txt para pistas detalladas"
echo "🔍 Usa analyze.sh para análisis inicial"