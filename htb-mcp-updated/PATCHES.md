# Parches para HTB MCP Server - API v4

## Archivo 1: `/internal/tools/machines.go`

### Buscar (alrededor de la línea 140):
```go
	// Determine the correct endpoint based on machine type
	// For now, we'll use the standard machine endpoint
	endpoint := fmt.Sprintf("/machine/play/%d", int(machineID))

	// Make API request
	data, err := t.client.PostWithParsing(ctx, endpoint, payload, "")
```

### Reemplazar con:
```go
	// Build request payload for the new endpoint
	payload := map[string]interface{}{
		"machine_id": int(machineID),
	}

	// Use the correct endpoint for spawning machines
	endpoint := "/vm/spawn"

	// Make API request
	data, err := t.client.PostWithParsing(ctx, endpoint, payload, "")
```

## Archivo 2: `/internal/tools/challenges.go`

### Paso 1: Agregar import
Buscar:
```go
import (
	"context"
	"fmt"

	"github.com/NoASLR/htb-mcp-server/pkg/htb"
	"github.com/NoASLR/htb-mcp-server/pkg/mcp"
)
```

Reemplazar con:
```go
import (
	"context"
	"fmt"
	"strconv"

	"github.com/NoASLR/htb-mcp-server/pkg/htb"
	"github.com/NoASLR/htb-mcp-server/pkg/mcp"
)
```

### Paso 2: Actualizar función Execute de StartChallenge
Buscar (alrededor de línea 122):
```go
func (t *StartChallenge) Execute(ctx context.Context, args map[string]interface{}) (*mcp.CallToolResponse, error) {
	challengeID, ok := args["challenge_id"].(string)
	if !ok {
		return nil, fmt.Errorf("challenge_id is required")
	}

	// Build endpoint URL
	endpoint := fmt.Sprintf("/challenge/%s/start", challengeID)

	// Make API request
	data, err := t.client.PostWithParsing(ctx, endpoint, nil, "")
```

Reemplazar con:
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

## Compilar después de los cambios:
```bash
go build -o htb-mcp-server main.go
```

## Verificar que funciona:
```bash
# Configurar token en .env
echo "HTB_TOKEN=tu_token_aqui" > .env

# Ejecutar servidor
./htb-mcp-server

# En otra terminal, probar con Python
python3 test_mcp.py
```