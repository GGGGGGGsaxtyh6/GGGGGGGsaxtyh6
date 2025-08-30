# 🚀 HackTheBox MCP Server - Versión Mejorada

Servidor MCP (Model Context Protocol) para interactuar con HackTheBox de forma programática. Permite iniciar challenges, obtener IPs de instancias, enviar flags y mucho más.

## 📋 Requisitos Previos

- Python 3.8+
- Una cuenta en HackTheBox con token de API válido
- Conexión a Internet
- Sistema Linux/Unix (probado en Ubuntu)

## 🔧 Instalación

### 1. Configurar el Token

```bash
# Copiar el archivo de configuración de ejemplo
cp .env.example .env

# Editar .env y reemplazar TU_TOKEN_AQUI con tu token real de HTB
nano .env
```

**IMPORTANTE**: Tu token de HTB debe tener el formato:
```
eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9...
```

### 2. Instalar Dependencias de Python

```bash
# Instalar paquetes necesarios
sudo apt-get update
sudo apt-get install -y python3-requests python3-pycryptodome python3-gmpy2

# O con pip:
pip3 install requests pycryptodome gmpy2
```

### 3. Dar Permisos de Ejecución

```bash
chmod +x htb-mcp-server
chmod +x *.py
```

## 🎯 Uso Básico

### Obtener la IP de un Challenge

**IMPORTANTE**: El endpoint correcto para obtener la IP es:
```
https://labs.hackthebox.com/api/v4/challenge/info/{challenge_id}
```

Este endpoint devuelve `docker_ip` y `docker_ports` en el objeto `challenge`.

```bash
# Obtener IP del challenge Baby Time Capsule (ID: 365)
python3 get_challenge_ip.py 365

# Output esperado:
# [+] Challenge: Baby Time Capsule
# [+] Dificultad: Very Easy
# [+] IP: 94.237.55.43
# [+] Puerto: 37928
```

### Iniciar un Challenge y Obtener su IP

```bash
# Inicia el challenge y automáticamente obtiene la IP
python3 start_challenge.py 365
```

### Enviar una Flag

```bash
# Enviar flag al challenge 365
python3 submit_flag.py 365 "HTB{tu_flag_aqui}"
```

## 🛠️ Herramientas Incluidas

### Scripts Python

1. **`get_challenge_ip.py`** - Obtiene la IP y puerto de un challenge activo
2. **`start_challenge.py`** - Inicia un challenge usando el servidor MCP
3. **`submit_flag.py`** - Envía flags a HackTheBox con manejo automático de dificultad

### Servidor MCP

El archivo `htb-mcp-server` es el servidor principal que se comunica con la API de HTB.

**Herramientas disponibles en el servidor MCP:**
- `start_challenge` - Inicia un challenge por ID
- `submit_challenge_flag` - Envía una flag de challenge
- `list_challenges` - Lista challenges disponibles
- `search_content` - Busca contenido en HTB
- `get_user_profile` - Obtiene perfil del usuario
- `get_user_progress` - Obtiene progreso del usuario

## 📚 Ejemplo de Uso Completo

```bash
# 1. Configurar token (solo la primera vez)
cp .env.example .env
# Editar .env y poner tu token

# 2. Iniciar un challenge (ejemplo con ID 365)
python3 start_challenge.py 365

# 3. Obtener la IP del challenge
python3 get_challenge_ip.py 365
# Output: IP: 94.237.55.43, Puerto: 37928

# 4. Resolver el challenge con tu exploit
python3 tu_exploit.py 94.237.55.43 37928

# 5. Enviar la flag obtenida
python3 submit_flag.py 365 "HTB{flag_obtenida}"
```

## 🔍 Solución de Problemas

### Error: "The route could not be found"

- **Causa**: Estás usando un endpoint incorrecto de la API
- **Solución**: Usa `https://labs.hackthebox.com/api/v4/challenge/info/{id}` para challenges

### Error: "Token inválido o expirado"

- **Causa**: Tu token ha expirado o es incorrecto
- **Solución**: Genera un nuevo token desde tu perfil de HTB

### Error: "El challenge no tiene una instancia activa"

- **Causa**: El challenge no está iniciado
- **Solución**: Usa `python3 start_challenge.py <id>` primero

### Error: "difficulty is required"

- **Causa**: La API requiere el parámetro de dificultad al enviar flags
- **Solución**: El script `submit_flag.py` ya maneja esto automáticamente

## 🏗️ Estructura del Proyecto

```
HTB-MCP-MEJORADO/
├── htb-mcp-server              # Servidor MCP principal (binario Go)
├── .env.example                # Plantilla de configuración
├── .env                        # Tu configuración (no compartir)
├── get_challenge_ip.py         # Obtener IP de challenges
├── start_challenge.py          # Iniciar challenges
├── submit_flag.py              # Enviar flags
├── README.md                   # Esta documentación
├── internal/                   # Código fuente Go del servidor
├── pkg/                        # Librerías Go
├── go.mod                      # Dependencias Go
└── main.go                     # Punto de entrada del servidor
```

## 🔐 Notas de Seguridad

1. **NUNCA** compartas tu archivo `.env` con el token
2. **NUNCA** subas tu token a repositorios públicos
3. El token tiene acceso a tu cuenta de HTB, mantenlo seguro
4. Regenera tu token si sospechas que ha sido comprometido

## 💡 Tips Avanzados

### Usar el Servidor MCP Directamente

```python
import subprocess
import json
import os

# Configurar entorno
env = os.environ.copy()
env['HTB_TOKEN'] = 'tu_token_aqui'

# Iniciar servidor
p = subprocess.Popen(['./htb-mcp-server'], 
                    stdin=subprocess.PIPE, 
                    stdout=subprocess.PIPE,
                    env=env, text=True)

# Inicializar
p.stdin.write('{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"0.1.0"}}\n')
p.stdin.flush()

# Llamar herramienta
p.stdin.write('{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"list_challenges","arguments":{"page":1}}}\n')
p.stdin.flush()

# Leer respuesta
response = p.stdout.readline()
print(json.loads(response))
```

### Automatización Completa

Puedes crear scripts que:
1. Inicien múltiples challenges
2. Resuelvan challenges automáticamente
3. Envíen flags en batch
4. Monitoreen tu progreso

## 📝 Notas Importantes

1. **La IP del challenge NO se obtiene del servidor MCP directamente**, sino de la API de HTB usando el endpoint correcto
2. Los challenges deben estar iniciados para tener una IP asignada
3. Algunos challenges pueden tardar unos segundos en inicializarse completamente
4. La dificultad debe enviarse como número (10, 20, 30, 40, 50) no como string

## 🤝 Contribuciones

Este proyecto ha sido mejorado para funcionar correctamente con la API actual de HackTheBox. Los principales cambios incluyen:

- Identificación del endpoint correcto para obtener IPs de challenges
- Scripts auxiliares para operaciones comunes
- Manejo automático de dificultades al enviar flags
- Documentación completa con ejemplos funcionales

## ⚠️ Disclaimer

Este servidor es para uso educativo y debe usarse solo con tu propia cuenta de HackTheBox. No uses este software para actividades no autorizadas.

---

**Versión**: 2.0 - Mejorada y Funcional
**Última actualización**: Enero 2025