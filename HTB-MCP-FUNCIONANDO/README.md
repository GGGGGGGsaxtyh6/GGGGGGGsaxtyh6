# HTB MCP Server

## Cómo Usar

### 1. Ejecutar servidor
```bash
./htb-mcp-server
```

### 2. Comandos

#### Iniciar máquina
```bash
python3 ejemplos/iniciar_maquina.py 701
```

#### Iniciar challenge
```bash
python3 ejemplos/iniciar_challenge.py 500
```

#### Enviar flag
```bash
python3 ejemplos/enviar_flag.py 500 "HTB{flag_aqui}"
```

## Obtener IP y Puerto de Challenges

```python
import requests
token = open('.env').read().split('HTB_TOKEN=')[1].split('\n')[0]
r = requests.get(f"https://labs.hackthebox.com/api/v4/challenge/info/500", 
                 headers={"Authorization": f"Bearer {token}"})
data = r.json()['challenge']
print(f"IP: {data['docker_ip']}")
print(f"Puerto: {data['docker_ports'][0]}")
```

## Comandos Disponibles

- `list_machines` - Listar máquinas
- `start_machine` - Iniciar máquina
- `get_machine_ip` - Obtener IP
- `submit_user_flag` - Flag usuario
- `submit_root_flag` - Flag root
- `list_challenges` - Listar challenges
- `start_challenge` - Iniciar challenge
- `submit_challenge_flag` - Flag challenge
- `get_user_profile` - Ver perfil

## Notas

- Token ya configurado en `.env`
- Contraseña ZIPs: `hackthebox`
- Solo 1 máquina y 1 challenge activo en free