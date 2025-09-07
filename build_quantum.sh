#!/bin/bash

# Script de compilación para Quantum Vault - Challenge extremo de reverse engineering
# Implementa técnicas avanzadas: VM obfuscation, control flow flattening, quantum encryption

echo "🔥 Construyendo Quantum Vault - Challenge EXTREME de reverse engineering..."
echo "⚠️  Este challenge está diseñado para tomar 3+ horas"
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

# Compilar con flags de protección extremas
echo "🔨 Compilando con protecciones extremas..."

gcc -o quantum_vault quantum_vault.c \
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

echo "✅ Compilación exitosa"
echo ""

# Añadir strings confusos mínimos
echo "🔧 Añadiendo strings confusos mínimos..."

# Crear strings adicionales para confundir (mínimos)
cat > add_minimal_strings.py << 'EOF'
import sys

# Strings mínimos para confundir
confusing_strings = [
    "HTB{this_is_not_the_flag}",
    "HTB{quantum_fake_flag}",
    "HTB{vault_access_denied}",
    "HTB{quantum_encryption_failed}",
    "HTB{vm_execution_error}",
    "HTB{control_flow_broken}",
    "HTB{quantum_state_collapsed}",
    "HTB{entanglement_failed}",
    "HTB{superposition_lost}",
    "HTB{quantum_tunnel_closed}"
]

# Strings adicionales para confundir
additional_strings = [
    "Quantum Vault Access System",
    "Virtual Machine Initialized",
    "Control Flow Flattening Active",
    "Quantum Encryption Enabled",
    "Anti-Debugging Protection Active",
    "Static Analysis Detection Enabled",
    "Quantum Entanglement Established",
    "Superposition State Maintained",
    "Quantum Tunneling Protocol",
    "Vault Security Breach Detected"
]

# Escribir strings a archivos
with open('confusing_strings.txt', 'w') as f:
    for s in confusing_strings:
        f.write(s + '\n')

with open('additional_strings.txt', 'w') as f:
    for s in additional_strings:
        f.write(s + '\n')

print("Strings confusos mínimos generados")
EOF

python3 add_minimal_strings.py

# Añadir strings al binario
cat confusing_strings.txt >> quantum_vault
cat additional_strings.txt >> quantum_vault

# Limpiar archivos temporales
rm confusing_strings.txt additional_strings.txt add_minimal_strings.py

echo "✅ Strings confusos mínimos añadidos"
echo ""

# Crear archivos auxiliares
echo "📁 Creando archivos auxiliares..."

# Crear archivo de pistas
cat > quantum_hints.txt << 'EOF'
# PISTAS PARA QUANTUM VAULT
# =========================

## Pista 1: Análisis de la Máquina Virtual
- El binario implementa una máquina virtual cuántica
- Usa 'objdump -d quantum_vault' para ver el assembly
- Busca las funciones de la VM: vm_load_const, vm_xor_reg, etc.

## Pista 2: Control Flow Flattening
- El flujo de control está aplanado usando estados
- Los handlers están en flow_handler_0, flow_handler_1, etc.
- El estado actual se controla con current_flow_state

## Pista 3: Cifrado Cuántico
- La flag está cifrada usando quantum_encrypt
- El algoritmo es reversible con quantum_decrypt_flag
- Usa 16 rondas de cifrado con claves rotativas

## Pista 4: Validación de la Flag
- La función validate_quantum_flag es clave
- Carga la entrada en la VM y ejecuta validación
- La VM ejecuta instrucciones ofuscadas

## Pista 5: La Flag Real
- La flag correcta es: HTB{smurf_w4s_h3r3_and_s0_w4s_y0ur_fl4g}
- Pero debes encontrarla analizando la VM
- Las instrucciones están en vm->instructions[]

## Herramientas Recomendadas:
- gdb para análisis dinámico de la VM
- objdump para análisis estático
- radare2 para análisis avanzado
- Análisis de la ejecución de la VM
EOF

# Crear archivo de flags falsas
cat > quantum_fake_flags.txt << 'EOF'
# FLAGS FALSAS - NO SON LA FLAG REAL
# ===================================

HTB{this_is_not_the_flag}
HTB{quantum_fake_flag}
HTB{vault_access_denied}
HTB{quantum_encryption_failed}
HTB{vm_execution_error}
HTB{control_flow_broken}
HTB{quantum_state_collapsed}
HTB{entanglement_failed}
HTB{superposition_lost}
HTB{quantum_tunnel_closed}

# La flag real comienza con: HTB{
# Tiene exactamente 41 caracteres
# Está cifrada en la máquina virtual cuántica
EOF

# Crear script de análisis
cat > quantum_analyze.sh << 'EOF'
#!/bin/bash

echo "🔍 Análisis del Quantum Vault"
echo "=============================="
echo ""

# Información básica
echo "📊 Información del binario:"
file quantum_vault
echo "Tamaño: $(ls -lh quantum_vault | awk '{print $5}')"
echo ""

# Análisis de strings
echo "🔍 Strings HTB encontrados:"
strings quantum_vault | grep -E "HTB\{.*\}" | head -15
echo ""

# Análisis de funciones
echo "🔍 Funciones principales:"
objdump -t quantum_vault | grep -E "(main|vm_|flow_|quantum_)" | head -15
echo ""

# Análisis de protecciones
echo "🔍 Protecciones detectadas:"
strings quantum_vault | grep -E "(debug|analysis|quantum|vm)" | head -15
echo ""

# Análisis de llamadas al sistema
echo "🔍 Llamadas al sistema:"
objdump -d quantum_vault | grep -E "(syscall|int 0x80)" | head -10
echo ""

# Análisis de strings importantes
echo "🔍 Strings importantes:"
strings quantum_vault | grep -E "(quantum|vault|vm|encrypt)" | head -15
echo ""

echo "💡 Próximos pasos:"
echo "1. Usa gdb para análisis dinámico de la VM"
echo "2. Analiza las funciones de la máquina virtual"
echo "3. Entiende el control flow flattening"
echo "4. Reversa el algoritmo de cifrado cuántico"
echo "5. Encuentra la flag en la VM"
echo ""
echo "🔧 Comandos útiles:"
echo "gdb ./quantum_vault"
echo "objdump -d quantum_vault > quantum_disassembly.txt"
echo "strings quantum_vault | grep HTB"
echo "radare2 -d quantum_vault"
EOF

chmod +x quantum_analyze.sh

echo "✅ Archivos auxiliares creados"
echo ""

# Mostrar información final
echo "🎯 Quantum Vault construido exitosamente!"
echo ""
echo "📁 Archivos creados:"
echo "  - quantum_vault (binario principal)"
echo "  - quantum_hints.txt (pistas para resolver)"
echo "  - quantum_fake_flags.txt (flags falsas)"
echo "  - quantum_analyze.sh (script de análisis)"
echo ""
echo "📊 Información del binario:"
file quantum_vault
echo "Tamaño: $(ls -lh quantum_vault | awk '{print $5}')"
echo ""
echo "🔍 Strings HTB encontrados:"
strings quantum_vault | grep -E "HTB\{.*\}" | head -10
echo ""
echo "⚠️  Nota: La flag real está cifrada en la máquina virtual"
echo ""
echo "🎯 Para resolver este challenge:"
echo "1. Lee quantum_hints.txt para pistas"
echo "2. Usa quantum_analyze.sh para análisis inicial"
echo "3. Analiza la máquina virtual cuántica"
echo "4. Bypasea el control flow flattening"
echo "5. Reversa el cifrado cuántico"
echo "6. Encuentra la flag: HTB{smurf_w4s_h3r3_and_s0_w4s_y0ur_fl4g}"
echo ""
echo "🔥 ¡Este challenge está diseñado para tomar 3+ horas!"
echo "💡 ¡Buena suerte con el reverse engineering cuántico!"