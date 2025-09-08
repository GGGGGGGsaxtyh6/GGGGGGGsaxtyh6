#!/bin/bash

# Script de configuración para el reto QuantumCipher
# Nivel: INSANE
# Tiempo estimado: 3 horas

echo "=== QuantumCipher Research Tool Challenge Setup ==="
echo "Nivel: INSANE"
echo "Tiempo estimado de resolución: 3 horas"
echo ""

# Verificar que estamos en un entorno Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo "ERROR: Este reto está diseñado para sistemas Linux"
    exit 1
fi

# Instalar dependencias necesarias
echo "Instalando dependencias del sistema..."
sudo apt-get update -qq
sudo apt-get install -y gcc make build-essential

# Compilar el binario con todas las protecciones
echo "Compilando binario con protecciones cuánticas..."
make clean
make all

# Verificar que el binario se compiló correctamente
if [ ! -f "quantum_cipher" ]; then
    echo "ERROR: Fallo en la compilación del binario"
    exit 1
fi

# Configurar permisos
chmod +x quantum_cipher

# Crear directorio de trabajo para el jugador
mkdir -p player_workspace
cp quantum_cipher player_workspace/
cp README.md player_workspace/ 2>/dev/null || true

echo ""
echo "=== RETO CONFIGURADO EXITOSAMENTE ==="
echo ""
echo "El binario 'quantum_cipher' está listo para el reto."
echo "Este es un reto de reversing nivel INSANE con las siguientes características:"
echo ""
echo "PROTECCIONES IMPLEMENTADAS:"
echo "1.  Anti-debugging cuántico con detección de ptrace"
echo "2.  Entrelazamiento de memoria con protección de ejecución"
echo "3.  Decoherencia temporal con monitoreo continuo"
echo "4.  Superposición de estados con cambios dinámicos"
echo "5.  Medición cuántica con restricciones de seccomp"
echo "6.  Túnel cuántico en memoria protegida"
echo "7.  Interferencia destructiva con patrones complejos"
echo "8.  Colapso de función de onda con validación de integridad"
echo "9.  Teleportación cuántica con buffers encriptados"
echo "10. Computación adiabática con evolución temporal"
echo "11. Corrección de errores cuánticos con síndromes"
echo "12. Inyección de ruido cuántico con generación aleatoria"
echo "13. Paralelismo cuántico con múltiples hilos"
echo "14. Criptografía post-cuántica con claves avanzadas"
echo "15. Simulación cuántica con ciclos de procesamiento"
echo ""
echo "CARACTERÍSTICAS DEL RETO:"
echo "- Software realista que simula una herramienta de investigación cuántica"
echo "- Múltiples módulos falsos y engañosos"
echo "- Lógica en capas que se desbloquea gradualmente"
echo "- Pistas sutiles distribuidas por todo el código"
echo "- Flag protegido tras superar todas las barreras"
echo ""
echo "OBJETIVO:"
echo "Encontrar el flag oculto: HTB{quantum_entanglement_breaches_reality_boundaries_2025}"
echo ""
echo "PISTAS INICIALES:"
echo "- El flag está protegido por múltiples capas de protección cuántica"
echo "- Cada protección debe ser superada de manera específica"
echo "- Las pistas están ocultas en el comportamiento del programa"
echo "- La resolución requiere comprensión profunda del funcionamiento"
echo ""
echo "¡Buena suerte en tu viaje cuántico!"
echo ""