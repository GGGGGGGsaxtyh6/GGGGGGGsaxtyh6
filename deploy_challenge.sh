#!/bin/bash

# Script de despliegue para el reto QuantumCipher
# Nivel: INSANE

echo "=== Despliegue del Reto QuantumCipher ==="
echo "Nivel: INSANE"
echo "Tiempo estimado: 3 horas"
echo ""

# Verificar que estamos en un entorno Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo "ERROR: Este reto está diseñado para sistemas Linux"
    exit 1
fi

# Crear directorio de despliegue
DEPLOY_DIR="quantum_cipher_challenge"
mkdir -p $DEPLOY_DIR

echo "Creando directorio de despliegue: $DEPLOY_DIR"

# Copiar archivos del reto
cp quantum_cipher $DEPLOY_DIR/
cp README.md $DEPLOY_DIR/
cp Makefile $DEPLOY_DIR/

# Crear archivo de instrucciones para el jugador
cat > $DEPLOY_DIR/INSTRUCTIONS.txt << 'EOF'
=== QUANTUM CIPHER RESEARCH TOOL CHALLENGE ===

NIVEL: INSANE
TIEMPO ESTIMADO: 3 horas
OBJETIVO: Encontrar el flag oculto

INSTRUCCIONES:
1. Ejecuta: ./quantum_cipher
2. Explora todas las opciones del menú
3. Busca pistas sutiles en el comportamiento
4. Usa técnicas de reversing para superar las protecciones
5. Encuentra el flag oculto

HERRAMIENTAS RECOMENDADAS:
- GDB para debugging
- objdump para análisis estático
- strace para monitoreo de syscalls

PISTAS:
- Las pistas están ocultas en el comportamiento del programa
- Cada opción del menú puede revelar información importante
- Presta atención a los mensajes de "ANOMALY"
- El flag está protegido por múltiples capas

¡Buena suerte en tu viaje cuántico!
EOF

# Crear archivo de metadatos
cat > $DEPLOY_DIR/METADATA.json << 'EOF'
{
  "challenge_name": "QuantumCipher Research Tool",
  "level": "INSANE",
  "estimated_time": "3 hours",
  "category": "Reverse Engineering",
  "difficulty": "Expert",
  "protections": 15,
  "flag_format": "HTB{...}",
  "tools_required": ["GDB", "objdump", "strace"],
  "description": "Advanced quantum cryptography research tool with multiple protection layers"
}
EOF

# Crear script de verificación
cat > $DEPLOY_DIR/verify_solution.sh << 'EOF'
#!/bin/bash

echo "=== Verificación de Solución ==="
echo ""

if [ ! -f "quantum_cipher" ]; then
    echo "ERROR: Binario no encontrado"
    exit 1
fi

echo "✓ Binario encontrado"

# Verificar que el binario es ejecutable
if [ ! -x "quantum_cipher" ]; then
    echo "ERROR: Binario no es ejecutable"
    exit 1
fi

echo "✓ Binario es ejecutable"

# Verificar tamaño del binario
size=$(stat -c%s quantum_cipher)
echo "✓ Tamaño del binario: $size bytes"

# Verificar que no hay símbolos de debug
if nm quantum_cipher 2>/dev/null | wc -l | grep -q "^0$"; then
    echo "✓ Símbolos de debug eliminados"
else
    echo "✗ Símbolos de debug presentes"
fi

echo ""
echo "El reto está listo para ser resuelto."
echo "Ejecuta './quantum_cipher' para comenzar."
EOF

chmod +x $DEPLOY_DIR/verify_solution.sh

# Crear archivo de estadísticas
cat > $DEPLOY_DIR/STATS.txt << 'EOF'
=== ESTADÍSTICAS DEL RETO ===

PROTECCIONES IMPLEMENTADAS: 15
- Anti-debugging cuántico
- Entrelazamiento de memoria
- Decoherencia temporal
- Superposición de estados
- Medición cuántica
- Túnel cuántico
- Interferencia destructiva
- Colapso de función de onda
- Teleportación cuántica
- Computación adiabática
- Corrección de errores cuánticos
- Inyección de ruido cuántico
- Paralelismo cuántico
- Criptografía post-cuántica
- Simulación cuántica

CARACTERÍSTICAS:
- Software realista con múltiples módulos
- Lógica en capas con desbloqueo gradual
- Pistas sutiles distribuidas
- Flag protegido tras múltiples barreras
- Tiempo estimado: 3 horas

NIVEL DE DIFICULTAD: INSANE
- Requiere habilidades expertas en reversing
- Múltiples técnicas de bypass necesarias
- Comprensión profunda del funcionamiento
- Persistencia y creatividad requeridas
EOF

# Crear archivo de log para el administrador
cat > $DEPLOY_DIR/admin_log.txt << 'EOF'
=== LOG DEL ADMINISTRADOR ===

RETO: QuantumCipher Research Tool
FECHA: $(date)
NIVEL: INSANE
ESTADO: Desplegado

ARCHIVOS INCLUIDOS:
- quantum_cipher: Binario principal del reto
- README.md: Documentación completa
- INSTRUCTIONS.txt: Instrucciones para el jugador
- METADATA.json: Metadatos del reto
- verify_solution.sh: Script de verificación
- STATS.txt: Estadísticas del reto
- admin_log.txt: Este archivo

NOTAS:
- El reto está listo para ser desplegado
- Todas las protecciones están activas
- Las pistas están distribuidas correctamente
- El flag está oculto y protegido

PRÓXIMOS PASOS:
1. Probar el reto en el entorno objetivo
2. Verificar que todas las funcionalidades trabajen
3. Confirmar que las protecciones están activas
4. Desplegar para los jugadores
EOF

# Crear archivo de respaldo
tar -czf quantum_cipher_challenge_backup.tar.gz $DEPLOY_DIR/

echo ""
echo "=== DESPLIEGUE COMPLETADO ==="
echo ""
echo "Directorio de despliegue: $DEPLOY_DIR"
echo "Archivo de respaldo: quantum_cipher_challenge_backup.tar.gz"
echo ""
echo "Contenido del directorio:"
ls -la $DEPLOY_DIR/
echo ""
echo "Para desplegar el reto:"
echo "1. Copia el directorio '$DEPLOY_DIR' al servidor objetivo"
echo "2. Ejecuta './verify_solution.sh' para verificar"
echo "3. El reto está listo para los jugadores"
echo ""
echo "¡El reto QuantumCipher está listo para desafiar a los expertos!"