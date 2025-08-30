# 📦 Cómo Obtener el HTB MCP Server Actualizado

## Opción 1: Aplicar los Parches Manualmente (RECOMENDADO)

1. **Clonar el repositorio original:**
```bash
git clone https://github.com/noaslr/htb-mcp-server.git
cd htb-mcp-server
```

2. **Aplicar los cambios descritos en PATCHES.md**
   - Solo necesitas modificar 2 archivos
   - Los cambios son pequeños y están bien documentados

3. **Compilar:**
```bash
go build -o htb-mcp-server main.go
```

## Opción 2: Fork del Repositorio

Podrías hacer un fork del repositorio original y aplicar los cambios:

1. Hacer fork de https://github.com/noaslr/htb-mcp-server
2. Aplicar los cambios en tu fork
3. Compartir tu fork actualizado

## Opción 3: Crear un Gist con los Parches

Crear un GitHub Gist con:
- El contenido de PATCHES.md
- El README_UPDATED.md
- Un script de instalación automática

## Opción 4: Subir a un Servicio de Archivos Temporal

Servicios donde podrías subir el archivo tar.gz (19KB):
- GitHub Releases (si haces un fork)
- Gist (los archivos de texto)
- Pastebin (para los parches)
- Google Drive / Dropbox (compartir link público)

## 📝 Archivos Importantes Creados

### Para la instalación necesitas:

1. **README_UPDATED.md** - Instrucciones completas de instalación y uso
2. **PATCHES.md** - Los cambios exactos que hacer en el código
3. **htb-mcp-server-updated.tar.gz** - Todo el código ya parcheado (19KB)

### Archivos de ejemplo creados durante la sesión:

- `test_updated_mcp.py` - Script para probar el servidor
- `htb_mcp_client.py` - Cliente Python de ejemplo
- `start_previous.py` - Ejemplo de iniciar máquina
- `survival_challenge.py` - Ejemplo de resolver challenge

## 🚀 Instalación Rápida desde Cero

```bash
# 1. Clonar
git clone https://github.com/noaslr/htb-mcp-server.git
cd htb-mcp-server

# 2. Aplicar parches (copiar los cambios de PATCHES.md)
# Editar: internal/tools/machines.go (línea ~142)
# Editar: internal/tools/challenges.go (agregar import y cambiar función)

# 3. Compilar
go build -o htb-mcp-server main.go

# 4. Configurar
cat > .env << EOF
HTB_TOKEN=tu_token_de_hackthebox
SERVER_PORT=3000
LOG_LEVEL=INFO
EOF

# 5. Ejecutar
./htb-mcp-server
```

## ✅ Verificación

Para verificar que funciona:

```python
# test.py
import json
import subprocess
import os

# ... (código del cliente HTBMCPClient del README)

client = HTBMCPClient()
client.initialize()

# Debe funcionar:
print(client.call_tool("list_machines", {"status": "active"}))
print(client.call_tool("list_challenges", {"category": "Web"}))

client.close()
```

## 📌 Resumen de Cambios

Los cambios principales fueron:
1. **Endpoint de máquinas**: `/machine/play/{id}` → `/vm/spawn`
2. **Endpoint de challenges**: `/challenge/{id}/start` → `/challenge/start`
3. **Formato de payloads**: Actualizado para la API v4
4. **Manejo de IDs**: Mejorado para aceptar números y strings

## 🔗 Endpoints Descubiertos

Durante la sesión descubrimos estos endpoints funcionales:
- `/api/v4/vm/spawn` - Iniciar máquina
- `/api/v4/vm/terminate` - Terminar máquina
- `/api/v4/challenge/start` - Iniciar challenge
- `/api/v4/challenge/info/{id}` - Info completa del challenge con IP y puerto
- `/api/v4/challenge/own` - Enviar flag
- `/api/v4/machine/active` - Máquina activa
- `/api/v4/user/info` - Información del usuario

## 💡 Tips

1. La contraseña de los ZIPs de HTB es siempre: `hackthebox`
2. Los challenges de blockchain tienen el RPC en: `http://{ip}:{puerto}/rpc`
3. La info de conexión está en: `http://{ip}:{puerto}/connection_info`
4. Solo puedes tener 1 máquina y 1 challenge activo en cuenta free

---

**El servidor MCP actualizado te permite interactuar con HTB de forma completamente autónoma.**