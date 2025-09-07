#!/bin/bash

# Script de prueba para el challenge de reverse engineering
# Verifica que el challenge funcione correctamente

echo "🧪 Probando el challenge de reverse engineering..."
echo ""

# Verificar que el binario existe
if [ ! -f "./challenge" ]; then
    echo "❌ Error: El binario 'challenge' no existe"
    echo "💡 Ejecuta './compile.sh' primero"
    exit 1
fi

echo "✅ Binario encontrado"
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
)

for flag in "${fake_flags[@]}"; do
    echo "Probando: $flag"
    ./challenge "$flag" 2>&1 | head -3
    echo ""
done

# Probar con la flag real
echo "🎯 Probando la flag real..."
echo ""

real_flag="HTB{smurf_w4s_h3r3_and_s0_w4s_y0ur_fl4g}"
echo "Probando: $real_flag"
./challenge "$real_flag"
echo ""

# Probar con entrada inválida
echo "❌ Probando entrada inválida..."
echo ""

echo "Probando sin argumentos:"
./challenge 2>&1 | head -2
echo ""

echo "Probando flag muy corta:"
./challenge "HTB{short}" 2>&1 | head -2
echo ""

echo "Probando flag muy larga:"
./challenge "HTB{this_flag_is_way_too_long_to_be_valid}" 2>&1 | head -2
echo ""

# Mostrar información del binario
echo "📊 Información del binario:"
echo "Tamaño: $(ls -lh challenge | awk '{print $5}')"
echo "Tipo: $(file challenge | cut -d: -f2-)"
echo ""

# Mostrar strings HTB
echo "🔍 Strings HTB encontrados:"
strings challenge | grep -E "HTB\{.*\}" | head -10
echo ""

echo "✅ Pruebas completadas"
echo ""
echo "🎯 El challenge está listo para usar!"
echo "💡 La flag correcta es: $real_flag"
echo "⚠️  Recuerda: Todas las demás flags son falsas"