# HTB MCP Server - Listo para Usar

## 🚀 INICIO RÁPIDO

### 1. Ejecutar el servidor
```bash
./htb-mcp-server
```

### 2. Usar los comandos
```bash
# Listar contenido
python3 examples/list_content.py

# Iniciar máquina
python3 examples/start_machine.py 701

# Iniciar challenge
python3 examples/start_challenge.py 500

# Enviar flag
python3 examples/submit_flag.py challenge 500 "HTB{flag}"
python3 examples/submit_flag.py user 701 "HTB{user_flag}"
python3 examples/submit_flag.py root 701 "HTB{root_flag}"
```

## 📋 COMANDOS DISPONIBLES

### Máquinas
- `list_machines` - Listar máquinas
- `start_machine` - Iniciar máquina (ID requerido)
- `get_machine_ip` - Obtener IP de máquina activa
- `submit_user_flag` - Enviar flag de usuario
- `submit_root_flag` - Enviar flag de root

### Challenges
- `list_challenges` - Listar challenges por categoría
- `start_challenge` - Iniciar challenge (ID requerido)
- `submit_challenge_flag` - Enviar flag de challenge

### Usuario
- `get_user_profile` - Ver tu perfil
- `get_user_progress` - Ver tu progreso
- `search_content` - Buscar contenido

## 💻 EJEMPLOS DE USO

### Ejemplo completo con Python
```python
#!/usr/bin/env python3
import json
import subprocess
import os

class HTBMCPClient:
    def __init__(self):
        self.token = None
        if os.path.exists('.env'):
            with open('.env', 'r') as f:
                for line in f:
                    if line.startswith('HTB_TOKEN='):
                        self.token = line.strip().split('=', 1)[1]
                        break
        
        env = os.environ.copy()
        env['HTB_TOKEN'] = self.token
        
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
        try:
            return json.loads(response_line)
        except:
            return {"error": "Failed to parse"}
    
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

# Usar
client = HTBMCPClient()
client.initialize()

# Iniciar máquina
result = client.call_tool("start_machine", {"machine_id": 701})

# Obtener IP
result = client.call_tool("get_machine_ip", {})

# Enviar flag
result = client.call_tool("submit_user_flag", {
    "machine_id": 701,
    "flag": "HTB{flag}"
})

client.close()
```

## 🔗 OBTENER INFO DE CONEXIÓN

### Para Challenges (IP y Puerto)
```python
import requests
import json

token = "tu_token"  # Ya está en .env
challenge_id = 500

response = requests.get(
    f"https://labs.hackthebox.com/api/v4/challenge/info/{challenge_id}",
    headers={"Authorization": f"Bearer {token}"}
)

data = response.json()
challenge = data['challenge']
ip = challenge['docker_ip']
port = challenge['docker_ports'][0]

print(f"Conectar a: http://{ip}:{port}")
```

### Para Máquinas
```python
response = requests.get(
    "https://labs.hackthebox.com/api/v4/machine/active",
    headers={"Authorization": f"Bearer {token}"}
)

data = response.json()
ip = data['info']['ip']
print(f"IP de la máquina: {ip}")
```

## 📝 NOTAS

- **Token**: Ya está configurado en `.env`
- **Contraseña ZIPs HTB**: `hackthebox`
- **Límites cuenta free**: 1 máquina y 1 challenge activo
- **Challenges Blockchain**: RPC en `http://ip:puerto/rpc`

## 🛠️ SI NECESITAS COMPILAR

```bash
go build -o htb-mcp-server main.go
```

---

**Todo está listo para usar. El token ya está configurado.**