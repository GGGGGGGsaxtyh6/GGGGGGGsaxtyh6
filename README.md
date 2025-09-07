# Challenge de Reverse Engineering: "Smurf's Hidden Treasure"

## 📋 Información del Challenge

- **Nombre**: Smurf's Hidden Treasure
- **Categoría**: Reverse Engineering
- **Dificultad**: Extremo
- **Flag Real**: `HTB{smurf_w4s_h3r3_and_s0_w4s_y0ur_fl4g}`
- **Flag Comienza con**: `HTB{smurf_`

## 🎯 Descripción

Smurf ha escondido su tesoro en este binario. Tu misión es encontrar la flag correcta usando técnicas de ingeniería inversa. El binario contiene múltiples capas de protección y flags falsas para confundir a los analistas.

## 🔧 Herramientas Recomendadas

- **Análisis Estático**:
  - `strings` - Para encontrar strings en el binario
  - `objdump` - Para desensamblar el código
  - `hexdump` - Para análisis hexadecimal
  - `file` - Para información del binario
  - `readelf` - Para información de ELF

- **Análisis Dinámico**:
  - `gdb` - Debugger de GNU
  - `strace` - Para rastrear llamadas al sistema
  - `ltrace` - Para rastrear llamadas a librerías

- **Herramientas Avanzadas**:
  - `radare2` - Framework de reverse engineering
  - `Ghidra` - Herramienta de NSA
  - `IDA Pro` - Desensamblador comercial
  - `x64dbg` - Debugger para Windows

## 🚀 Cómo Empezar

1. **Analiza el binario**:
   ```bash
   file challenge
   strings challenge | grep HTB
   objdump -d challenge
   ```

2. **Ejecuta el binario**:
   ```bash
   ./challenge HTB{test}
   ```

3. **Analiza el comportamiento**:
   - ¿Qué hace el programa?
   - ¿Qué protecciones tiene?
   - ¿Dónde está la validación?

## 🛡️ Protecciones Implementadas

- **Anti-debugging**: Detección de debugger usando `ptrace`
- **Ofuscación**: Strings y datos ofuscados
- **Flags Falsas**: Múltiples flags falsas para confundir
- **Validación Compleja**: Algoritmo de validación no trivial
- **Integridad**: Verificaciones de integridad del programa

## 🔍 Pistas

### Pista 1: Análisis Estático
- Usa `strings challenge | grep HTB` para ver todas las flags
- La flag real comienza con `HTB{smurf_`
- Hay muchas flags falsas, no te confundas

### Pista 2: Análisis Dinámico
- El binario detecta debuggers
- Puedes bypasear la detección modificando el comportamiento
- Usa `gdb` para analizar el flujo de ejecución

### Pista 3: Algoritmo de Validación
- La función `validate_input()` es clave
- Verifica longitud exacta de 32 caracteres
- Comienza con `HTB{` y termina con `}`
- El contenido específico está hardcodeado

## 🎯 Solución

### Método 1: Análisis Estático
1. Usa `strings challenge | grep HTB` para ver todas las flags
2. Identifica la flag real entre las falsas
3. La flag real es: `HTB{smurf_w4s_h3r3_and_s0_w4s_y0ur_fl4g}`

### Método 2: Análisis Dinámico
1. Usa `gdb ./challenge`
2. Bypasea la detección de debugger
3. Analiza la función `validate_input()`
4. Encuentra el string esperado en el código

### Método 3: Ingeniería Inversa Completa
1. Desensambla el binario con `objdump -d challenge`
2. Encuentra la función `main()` y `validate_input()`
3. Analiza el algoritmo de validación
4. Reconstruye la flag esperada

## 📁 Archivos del Challenge

- `challenge` - Binario principal
- `challenge.c` - Código fuente (para referencia)
- `compile.sh` - Script de compilación
- `obfuscate.py` - Script de ofuscación
- `flags.txt` - Flags falsas
- `hint1.txt`, `hint2.txt`, `hint3.txt` - Pistas
- `obfuscated_data.txt` - Datos ofuscados
- `fake_functions.c` - Funciones falsas

## ⚠️ Notas Importantes

- **Todas las flags en el binario son FALSAS excepto la real**
- **La flag real comienza con `HTB{smurf_`**
- **El binario tiene protecciones anti-debugging**
- **Se requiere conocimiento de assembly y debugging**
- **Este es un challenge de nivel extremo**

## 🏆 Criterios de Éxito

Para resolver este challenge, debes:

1. ✅ Identificar que es un challenge de reverse engineering
2. ✅ Usar herramientas apropiadas de análisis
3. ✅ Bypasear las protecciones anti-debugging
4. ✅ Distinguir entre flags falsas y la real
5. ✅ Encontrar la flag correcta: `HTB{smurf_w4s_h3r3_and_s0_w4s_y0ur_fl4g}`

## 🎓 Habilidades Desarrolladas

- Análisis estático de binarios
- Análisis dinámico con debuggers
- Bypass de protecciones anti-debugging
- Identificación de strings y datos
- Ingeniería inversa de algoritmos
- Uso de herramientas de reverse engineering

---

**¡Buena suerte y que disfrutes el challenge!** 🚀