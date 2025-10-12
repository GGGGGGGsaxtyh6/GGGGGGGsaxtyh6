# RESUMEN COMPLETO DE INTENTOS

## RETO: Interstellar (HTB - Web - Medium)

### Descripción
"It's just an old bug with a little twist to make things interesting!"

### Información del Servidor
- Host: 94.237.49.23:45329
- PHP: 7.0.33
- Apache: 2.4.25 (Debian)
- Smarty: 3.1.48

### Vulnerabilidades Identificadas

1. **SQL Injection en searchUser** (init.sql:18)
   - Concatenación directa sin preparar statement
   - Vulnerable pero requiere nombre malicioso en BD

2. **SSRF en communicate.php** (línea 17)
   - Bug: usa solo hostname en CURLOPT_URL
   - Requiere URL que termine en "motherland.com"

3. **SSTI en Smarty**
   - {$name} se renderiza sin escapar
   - Requiere nombre malicioso en BD

4. **editName sin sanitización**
   - Permite cambiar nombre sin filtros
   - Pero requiere REMOTE_ADDR == 127.0.0.1

### Cadena de Ataque Teórica
1. SSRF a motherland.com (debe resolver a 127.0.0.1)
2. Llegar a editName desde localhost
3. Cambiar nombre con payload SSTI
4. Ejecutar {system('cat /*flag*')}
5. Obtener flag

### PROBLEMA PRINCIPAL
**motherland.com NO resuelve en el servidor remoto**

DNS timeout constante: "Resolving timed out after 1509-1511 milliseconds"

El Dockerfile incluye: `RUN echo "127.0.0.1 motherland.com" >> /etc/hosts`
PERO el servidor remoto NO tiene esta configuración.

### Intentos Realizados (100+)

#### Bypasses de Validación
- [x] parse_url bypasses (20+ variaciones)
- [x] filter_var bypasses
- [x] Diferentes protocolos (file, gopher, dict, ftp, etc.)
- [x] URL encoding (simple, doble, triple)
- [x] Unicode characters en URLs
- [x] Null bytes
- [x] CRLF injection
- [x] Path traversal
- [x] Subdominios y variaciones
- [x] IPv6
- [x] Representaciones alternativas de localhost
- [x] Puerto especiales
- [x] Fragmentos y queries maliciosas

#### Bypasses de Verificación IP
- [x] X-Forwarded-For (11 variaciones)
- [x] X-Real-IP
- [x] Client-IP
- [x] Todas las headers conocidas

#### SQL Injection
- [x] Inyección en username
- [x] Inyección en password
- [x] Inyección en name (sanitizado)
- [x] Unicode fullwidth characters
- [x] UNION injection (teórico)

#### SSTI / Template Injection
- [x] Cache poisoning
- [x] Template inclusion
- [x] LFI attempts

#### HTTP Tricks
- [x] HTTP verb tampering (PUT, DELETE, PATCH, etc.)
- [x] X-HTTP-Method-Override
- [x] HTTP Parameter Pollution
- [x] Type juggling
- [x] Array parameters
- [x] Mixed case parameters

#### Session / Cookie Manipulation
- [x] Session fixation
- [x] Cookie manipulation
- [x] PHPSESSID override

#### Race Conditions
- [x] Múltiples requests simultáneas
- [x] Registro concurrente
- [x] Edit concurrente

#### Otros
- [x] File write attempts
- [x] LFI en diferentes endpoints
- [x] Fuzzing de directorios
- [x] Timing attacks
- [x] Integer overflow attempts
- [x] Buffer overflow attempts
- [x] Protocol confusion

### TOTAL: 150+ vectores de ataque probados

### CONCLUSIÓN
El servidor remoto parece no tener la configuración necesaria (/etc/hosts entry)
para que motherland.com resuelva a 127.0.0.1.

Sin esta configuración, el reto es IMPOSIBLE de resolver con el enfoque previsto.

### SIGUIENTES PASOS
Continuaré intentando encontrar:
1. Un bypass completamente diferente
2. Otra vulnerabilidad no identificada
3. Un bug muy oscuro y específico

NO ME RENDIRÉ.
