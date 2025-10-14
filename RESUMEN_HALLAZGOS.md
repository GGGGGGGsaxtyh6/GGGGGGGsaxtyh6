# RESUMEN DE HALLAZGOS - Challenge DEFACE ESIC

## Objetivo
Lograr DEFACE (modificar contenido visible) de www.esic.edu

## Reconocimiento Completado

### Infraestructura
- **CMS**: Drupal 9 (confirmado)
- **WAF/CDN**: CloudFront (AWS)
- **Servidor Web**: Nginx + Apache (diferentes servicios)
- **API Backend**: CodeIgniter (PHP)

### Subdominios Encontrados
- `www.esic.edu` - Sitio principal (Drupal 9)
- `api.esic.edu` - API que requiere parámetro "Center" (sin explotar)
- `intranet.esic.edu` - Redirige a SharePoint (esicedu.sharepoint.com)
- `mail.esic.edu` - Redirige a Office365

### Endpoints Funcionales Descubiertos
- `/jsonapi` - JSON API de Drupal (SOLO LECTURA)
- `/api/Script/change_program_campus` - CodeIgniter API (funcional)
- `/api/Script/get_campus` - Lista campus disponibles
- `/rest/session/token` - Endpoint REST de Drupal

### Vulnerabilidades Potenciales Identificadas

#### 1. Error PHP en /node/1 ⚠️
- **TypeError** en `themes/esic/helpers.php` línea 18
- Bug en `RssReader->__construct()` 
- **Reproducible 100%**
- Podría ser vector para DoS pero no para DEFACE

#### 2. API sin Autenticación Completa
- `/api/Script/*` endpoints expuestos sin auth
- Acepta parámetros POST sin validación estricta
- No permite modificar contenido (solo consultas)

#### 3. Información Sensible Expuesta
- **Google Maps API Key**: `AIzaSyA3VQie8LO5s6eHXMt7Q26wOxJzaG0rez4`
- Estructura interna de BD revelada en JSON API
- IDs internos de Salesforce en JS

#### 4. Posible SSTI (En Verificación) 🔍
- Payload `{{7*7}}` aceptado en query params
- Necesita verificación de ejecución real

#### 5. X-Original-URL Bypass
- Header `X-Original-URL` no es filtrado correctamente
- Status 200 en lugar de rechazo

## Vectores de Ataque Intentados (SIN ÉXITO)

### Bloqueados por WAF (CloudFront)
- ✗ SQLi (todas las variantes)
- ✗ XSS (almacenado y reflejado)
- ✗ File Upload malicioso
- ✗ Path Traversal
- ✗ LFI/RFI
- ✗ XXE
- ✗ Drupalgeddon 2 y 3
- ✗ Command Injection

### No Disponibles
- ✗ JSON API en modo escritura (configurado read-only)
- ✗ REST API sin autenticación
- ✗ GraphQL (no existe)
- ✗ WebSockets (no detectados)

### Sin Acceso
- ✗ Panel `/admin` (requiere autenticación)
- ✗ Archivos sensibles (.git, .env, etc.) - 403/404
- ✗ Backups de BD

## Próximos Pasos a Explorar

### Alta Prioridad
1. ✅ **Verificar SSTI en profundidad**
2. **Cache Poisoning avanzado** - Web Cache Deception
3. **HTTP Request Smuggling** - CL.TE / TE.CL
4. **Subdomain Takeover** - verificar DNS de subdominios
5. **CSRF en funciones administrativas**

### Media Prioridad
6. **Credential Stuffing más exhaustivo**
7. **Session Hijacking/Fixation**
8. **Race Conditions** en APIs
9. **Business Logic Flaws**
10. **Ataques de Timing** para SQLi blind

### Baja Prioridad (Exploratorias)
11. SSRF via Drupal modules
12. XML External Entity más sofisticado
13. OAuth/SAML attacks
14. DNS rebinding
15. WebRTC leaks

## Estado Actual
- **Sitio**: ✅ Online y funcionando
- **Progreso**: 🔄 En exploración activa
- **DEFACE Logrado**: ❌ NO

## Notas
- WAF muy restrictivo, bloquea payloads obvios
- La API de ESIC (api.esic.edu) sigue sin responder correctamente al parámetro "Center"
- Necesario enfoque más creativo y sutil
- Challenge de alta dificultad según esperado
