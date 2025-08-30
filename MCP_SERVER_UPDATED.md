# HTB MCP Server - ACTUALIZADO Y FUNCIONANDO ✅

## 🎉 Actualización Completada

El servidor MCP de HackTheBox ha sido actualizado exitosamente con los endpoints correctos de la API v4.

## 📋 Cambios Realizados

### 1. **Máquinas** 
- ✅ **Endpoint de spawn actualizado**: `/machine/play/{id}` → `/vm/spawn`
- ✅ **Endpoint de terminate**: `/vm/terminate`
- ✅ **Funciones disponibles**:
  - Listar máquinas (activas y retiradas)
  - Iniciar máquinas
  - Obtener IP de máquina activa
  - Terminar máquinas

### 2. **Challenges**
- ✅ **Endpoint de start actualizado**: `/challenge/{id}/start` → `/challenge/start`
- ✅ **Formato de payload corregido**: Ahora usa `{"challenge_id": id}`
- ✅ **Funciones disponibles**:
  - Listar challenges por categoría
  - Iniciar challenges (especialmente los de tipo "container")
  - Enviar flags de challenges

## 🚀 Cómo Usar

### Iniciar el Servidor MCP

```bash
cd /workspace/htb-mcp-server
./run_htb_server.sh
```

### Ejemplos de Uso

#### Iniciar una Máquina
```python
# Máquina Previous (ID: 701)
client.call_tool("start_machine", {"machine_id": 701})
```

#### Iniciar un Challenge
```python
# Challenge Flag Command (ID: 646)
client.call_tool("start_challenge", {"challenge_id": 646})
```

## ✅ Endpoints Funcionando

| Función | Endpoint | Método | Estado |
|---------|----------|--------|--------|
| Iniciar máquina | `/api/v4/vm/spawn` | POST | ✅ Funcionando |
| Terminar máquina | `/api/v4/vm/terminate` | POST | ✅ Funcionando |
| Máquina activa | `/api/v4/machine/active` | GET | ✅ Funcionando |
| Listar máquinas | `/api/v4/machine/paginated` | GET | ✅ Funcionando |
| Iniciar challenge | `/api/v4/challenge/start` | POST | ✅ Funcionando |
| Listar challenges | `/api/v4/challenge/list` | GET | ✅ Funcionando |
| Info de usuario | `/api/v4/user/info` | GET | ✅ Funcionando |

## 📊 Estado Actual

### Máquina Activa
- **Previous** (ID: 701)
- **IP**: 10.10.11.83
- **Sistema**: Linux
- **Dificultad**: Medium

### Challenge Activo
- **Flag Command** (ID: 646)
- **Categoría**: Web
- **Tipo**: Container
- **Instance ID**: 1658434

## 🔧 Archivos Modificados

1. `/workspace/htb-mcp-server/internal/tools/machines.go`
   - Actualizado endpoint de spawn a `/vm/spawn`
   - Corregido formato de payload

2. `/workspace/htb-mcp-server/internal/tools/challenges.go`
   - Actualizado endpoint de start a `/challenge/start`
   - Agregado manejo de challenge_id como entero
   - Corregido formato de payload

## 📝 Notas

- Los challenges de tipo "container" son los que se pueden iniciar (Web, Pwn, etc.)
- Los challenges de tipo "download" solo requieren descargar archivos
- Las máquinas free tienen un límite de tiempo de ejecución
- Solo puedes tener una máquina y un challenge activo a la vez en cuenta free

## ✨ Todo Listo

El servidor MCP está completamente funcional y puede:
- ✅ Iniciar y gestionar máquinas
- ✅ Iniciar y gestionar challenges
- ✅ Listar contenido disponible
- ✅ Enviar flags
- ✅ Ver perfil y progreso

¡El servidor está listo para usar!