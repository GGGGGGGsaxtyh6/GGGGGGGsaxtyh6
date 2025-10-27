# HTB MCP Server - Versión Actualizada y Funcional

## 📦 Descripción
Servidor MCP (Model Context Protocol) para interactuar con HackTheBox de forma autónoma. Esta versión ha sido actualizada para funcionar con la API v4 actual de HTB.

## ✅ Características Funcionando
- ✅ Iniciar y gestionar máquinas
- ✅ Iniciar y gestionar challenges
- ✅ Enviar flags automáticamente
- ✅ Obtener información de conexión completa
- ✅ Listar contenido disponible
- ✅ Ver perfil y progreso

## 🚀 Instalación Rápida

### Requisitos Previos
- Go 1.21 o superior
- Git
- Cuenta de HackTheBox con token API

### Paso 1: Clonar el Repositorio
```bash
git clone https://github.com/noaslr/htb-mcp-server.git
cd htb-mcp-server
```

### Paso 2: Aplicar las Actualizaciones

#### Actualizar `/internal/tools/machines.go`
En la línea ~142, cambiar:
```go
// ANTES:
endpoint := fmt.Sprintf("/machine/play/%d", int(machineID))

// DESPUÉS:
endpoint := "/vm/spawn"
payload := map[string]interface{}{
    "machine_id": int(machineID),
}
```

#### Actualizar `/internal/tools/challenges.go`
1. Agregar import de `strconv` al inicio
2. En la función `Execute` de `StartChallenge` (línea ~122), reemplazar con:
```go
func (t *StartChallenge) Execute(ctx context.Context, args map[string]interface{}) (*mcp.CallToolResponse, error) {
    var challengeID int
    
    // Try to get challenge_id as float64 first (JSON numbers)
    if id, ok := args["challenge_id"].(float64); ok {
        challengeID = int(id)
    } else if idStr, ok := args["challenge_id"].(string); ok {
        // Try to parse as string
        if idInt, err := strconv.Atoi(idStr); err == nil {
            challengeID = idInt
        } else {
            return nil, fmt.Errorf("invalid challenge_id format")
        }
    } else {
        return nil, fmt.Errorf("challenge_id is required")
    }

    // Use the new endpoint format
    endpoint := "/challenge/start"
    payload := map[string]interface{}{
        "challenge_id": challengeID,
    }

    // Make API request
    data, err := t.client.PostWithParsing(ctx, endpoint, payload, "")
```

### Paso 3: Compilar
```bash
go build -o htb-mcp-server main.go
```

### Paso 4: Configurar Token HTB
Crear archivo `.env`:
```bash
HTB_TOKEN=tu_token_aqui
SERVER_PORT=3000
LOG_LEVEL=INFO
RATE_LIMIT_PER_MINUTE=100
CACHE_TTL_SECONDS=300
REQUEST_TIMEOUT_SECONDS=30
```

Para obtener tu token:
1. Ve a https://app.hackthebox.com/profile/settings
2. Genera un App Token
3. Copia el token JWT (formato: xxx.yyy.zzz)

### Paso 5: Ejecutar
```bash
./htb-mcp-server
```

## 📝 Uso

### Iniciar una Máquina
```python
import json
import subprocess

# Configurar cliente MCP
# ... (ver ejemplo completo abajo)

# Iniciar máquina
client.call_tool("start_machine", {"machine_id": 701})
```

### Iniciar un Challenge
```python
# Iniciar challenge
client.call_tool("start_challenge", {"challenge_id": 500})

# Obtener información de conexión
# La IP y puerto estarán en /challenge/info/{id}
```

### Enviar una Flag
```python
# Para máquinas
client.call_tool("submit_user_flag", {
    "machine_id": 701,
    "flag": "HTB{...}"
})

# Para challenges
client.call_tool("submit_challenge_flag", {
    "challenge_id": 500,
    "flag": "HTB{...}"
})
```

## 🔧 Cliente Python Completo

```python
#!/usr/bin/env python3
import json
import subprocess
import os

class HTBMCPClient:
    def __init__(self):
        env_path = '.env'
        self.token = None
        if os.path.exists(env_path):
            with open(env_path, 'r') as f:
                for line in f:
                    if line.startswith('HTB_TOKEN='):
                        self.token = line.strip().split('=', 1)[1]
                        break
        
        env = os.environ.copy()
        env['HTB_TOKEN'] = self.token
        env['LOG_LEVEL'] = 'INFO'
        
        self.process = subprocess.Popen(
            ['./htb-mcp-server'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
            text=True,
            bufsize=1
        )
        self.request_id = 0
        
    def _send_request(self, method, params=None):
        self.request_id += 1
        request = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": method,
            "params": params or {}
        }
        
        request_str = json.dumps(request) + '\n'
        self.process.stdin.write(request_str)
        self.process.stdin.flush()
        
        response_line = self.process.stdout.readline()
        if not response_line:
            return {"error": "No response from server"}
        
        try:
            return json.loads(response_line)
        except json.JSONDecodeError:
            return {"error": f"Failed to parse response: {response_line}"}
    
    def initialize(self):
        return self._send_request("initialize", {
            "protocolVersion": "0.1.0",
            "capabilities": {},
            "clientInfo": {"name": "htb-client", "version": "1.0.0"}
        })
    
    def call_tool(self, tool_name, arguments):
        return self._send_request("tools/call", {
            "name": tool_name,
            "arguments": arguments
        })
    
    def close(self):
        if self.process:
            self.process.terminate()
            self.process.wait()

# Ejemplo de uso
if __name__ == "__main__":
    client = HTBMCPClient()
    
    # Inicializar
    client.initialize()
    
    # Listar máquinas
    result = client.call_tool("list_machines", {"status": "active"})
    print(result)
    
    # Iniciar máquina
    result = client.call_tool("start_machine", {"machine_id": 701})
    print(result)
    
    client.close()
```

## 📋 Endpoints Actualizados

| Función | Endpoint Antiguo | Endpoint Nuevo | Estado |
|---------|-----------------|----------------|--------|
| Iniciar máquina | `/machine/play/{id}` | `/vm/spawn` | ✅ |
| Terminar máquina | - | `/vm/terminate` | ✅ |
| Iniciar challenge | `/challenge/{id}/start` | `/challenge/start` | ✅ |
| Info challenge | - | `/challenge/info/{id}` | ✅ |
| Enviar flag | - | `/challenge/own` | ✅ |

## 🔍 Obtener Información de Conexión

### Para Challenges
```python
import requests

token = "tu_token_htb"
challenge_id = 500

# Obtener info completa incluyendo IP y puerto
response = requests.get(
    f"https://labs.hackthebox.com/api/v4/challenge/info/{challenge_id}",
    headers={"Authorization": f"Bearer {token}"}
)

data = response.json()
challenge = data.get('challenge', {})

# La información de conexión está en:
docker_ip = challenge.get('docker_ip')  # IP del contenedor
docker_ports = challenge.get('docker_ports')  # Lista de puertos
```

### Para Máquinas
```python
# Obtener máquina activa
response = requests.get(
    "https://labs.hackthebox.com/api/v4/machine/active",
    headers={"Authorization": f"Bearer {token}"}
)

data = response.json()
info = data.get('info', {})
machine_ip = info.get('ip')  # IP de la máquina
```

## 🐛 Solución de Problemas

### "HTB token appears invalid or expired"
- Verifica que tu token sea válido
- Genera un nuevo token en HTB

### "Machine/Challenge not spawning"
- Verifica que no tengas otra máquina/challenge activo
- Las cuentas free solo permiten 1 activo a la vez

### "Cannot connect to IP"
- Asegúrate de estar conectado a la VPN de HTB
- Verifica que la instancia esté activa

## 📝 Notas Importantes

1. **Contraseña de ZIPs**: Los archivos ZIP de HTB usan la contraseña `hackthebox`

2. **Límites de cuenta Free**:
   - Solo 1 máquina activa a la vez
   - Solo 1 challenge activo a la vez
   - Máquinas tienen tiempo límite

3. **Endpoints especiales**:
   - RPC para challenges blockchain: `http://{ip}:{puerto}/rpc`
   - Info de conexión en challenges: `http://{ip}:{puerto}/connection_info`

## 🚀 Ejemplo Completo: Resolver un Challenge

```python
# 1. Iniciar challenge
client.call_tool("start_challenge", {"challenge_id": 500})

# 2. Obtener info de conexión
import requests
resp = requests.get(
    "https://labs.hackthebox.com/api/v4/challenge/info/500",
    headers={"Authorization": f"Bearer {token}"}
)
info = resp.json()['challenge']
ip = info['docker_ip']
port = info['docker_ports'][0]

# 3. Interactuar con el challenge
# ... resolver el challenge ...

# 4. Enviar flag
client.call_tool("submit_challenge_flag", {
    "challenge_id": 500,
    "flag": "HTB{flag_aqui}"
})
```

## 📦 Archivos Modificados

Los únicos archivos que necesitan modificación son:
- `/internal/tools/machines.go` (línea ~142)
- `/internal/tools/challenges.go` (líneas ~122-146)

## ✨ Créditos

- Servidor MCP original por NoASLR
- Actualizaciones para API v4 realizadas el 30/08/2025
- Probado con HTB API v4

## 📄 Licencia

MIT License - Ver archivo LICENSE original

---

**¡El servidor está listo para usar con la API actual de HackTheBox!**