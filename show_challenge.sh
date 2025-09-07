#!/bin/bash

# Script para mostrar información completa del challenge INSANE

echo "🔥 CHALLENGE INSANE: SMURF'S HIDDEN TREASURE"
echo "=============================================="
echo ""

echo "📋 Información del Challenge:"
echo "  - Nombre: Smurf's Hidden Treasure"
echo "  - Categoría: Reverse Engineering"
echo "  - Dificultad: INSANE 🔥"
echo "  - Tiempo estimado: 2+ horas"
echo "  - Flag real: HTB{smurf_w4s_h3r3_and_s0_w4s_y0ur_fl4g}"
echo "  - Flag comienza con: HTB{smurf_"
echo ""

echo "📁 Archivos del Challenge:"
ls -la | grep -E "\.(c|sh|txt|md)$|smurf_treasure" | awk '{print "  - " $9 " (" $5 " bytes)"}'
echo ""

echo "🛡️ Protecciones Implementadas:"
echo "  - Anti-debugging (múltiples métodos)"
echo "  - Detección de VM/Sandbox"
echo "  - Verificación de integridad"
echo "  - Validación multi-etapa"
echo "  - Ofuscación de strings y datos"
echo "  - Flags falsas con pistas progresivas"
echo ""

echo "🔧 Herramientas Recomendadas:"
echo "  - Análisis estático: strings, objdump, hexdump, file, readelf"
echo "  - Análisis dinámico: gdb, strace, ltrace"
echo "  - Herramientas avanzadas: radare2, ghidra, ida pro"
echo ""

echo "🚀 Cómo Empezar:"
echo "  1. Lee README_INSANE.md para información completa"
echo "  2. Usa analyze.sh para análisis inicial"
echo "  3. Lee hints.txt para pistas básicas"
echo "  4. Lee advanced_hints.txt para pistas técnicas"
echo "  5. Usa bypass_guide.txt para bypass de protecciones"
echo "  6. Combina análisis estático y dinámico"
echo ""

echo "🔍 Análisis Rápido:"
echo "  - Tamaño del binario: $(ls -lh smurf_treasure | awk '{print $5}')"
echo "  - Strings HTB encontrados: $(strings smurf_treasure | grep -E 'HTB\{.*\}' | wc -l)"
echo "  - Funciones principales: $(objdump -t smurf_treasure | grep -E '(main|validate|detect)' | wc -l)"
echo ""

echo "🎯 Para Resolver el Challenge:"
echo "  1. Identifica que es un challenge de reverse engineering"
echo "  2. Usa herramientas apropiadas de análisis"
echo "  3. Bypasea las protecciones anti-debugging"
echo "  4. Distingue entre flags falsas y la real"
echo "  5. Entiende el sistema de validación multi-etapa"
echo "  6. Encuentra la flag correcta usando reverse engineering"
echo ""

echo "⚠️ Notas Importantes:"
echo "  - Todas las flags en el binario son FALSAS excepto la real"
echo "  - La flag real comienza con HTB{smurf_"
echo "  - Se requiere conocimiento avanzado de assembly y debugging"
echo "  - Este es un challenge de nivel INSANE"
echo "  - Tiempo estimado: 2+ horas para hackers experimentados"
echo ""

echo "🏆 Criterios de Éxito:"
echo "  ✅ Bypass de protecciones anti-debugging"
echo "  ✅ Análisis estático y dinámico"
echo "  ✅ Identificación de flags falsas"
echo "  ✅ Comprensión del sistema de validación"
echo "  ✅ Encontrar la flag correcta"
echo ""

echo "🎓 Habilidades Desarrolladas:"
echo "  - Análisis estático avanzado de binarios"
echo "  - Análisis dinámico con debuggers"
echo "  - Bypass de protecciones anti-debugging"
echo "  - Detección y bypass de VM/Sandbox"
echo "  - Ingeniería inversa de algoritmos complejos"
echo "  - Uso de herramientas profesionales de reverse engineering"
echo ""

echo "🔥 ¡Este challenge está diseñado para hackers de nivel profesional!"
echo "💡 ¡Buena suerte con el reverse engineering!"
echo ""

# Mostrar algunas strings HTB como ejemplo
echo "🔍 Ejemplo de strings HTB encontrados:"
strings smurf_treasure | grep -E "HTB\{.*\}" | head -10
echo ""

echo "📚 Archivos de ayuda disponibles:"
echo "  - README_INSANE.md (documentación completa)"
echo "  - hints.txt (pistas básicas)"
echo "  - advanced_hints.txt (pistas técnicas avanzadas)"
echo "  - bypass_guide.txt (guía de bypass de protecciones)"
echo "  - analyze.sh (script de análisis inicial)"
echo "  - advanced_analysis.sh (script de análisis avanzado)"
echo ""

echo "🎯 ¡El challenge está listo para usar!"
echo "💡 Ejecuta: ./smurf_treasure HTB{tu_flag_aqui}"
echo "🔥 ¡Disfruta este challenge INSANE de reverse engineering!"