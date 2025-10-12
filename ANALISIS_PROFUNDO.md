# ANÁLISIS PROFUNDO DEL RETO INTERSTELLAR

## DESCRIPCIÓN
"It's just an old bug with a little twist to make things interesting!"

## VULNERABILIDADES IDENTIFICADAS

### 1. SQL INJECTION en searchUser (init.sql línea 18)
```sql
SET @sql = CONCAT('SELECT * FROM users WHERE name = \'', name, '\'');
```
**PROBLEMA**: Concatenación directa sin escapar
**LIMITACIÓN**: register.php sanitiza nombre (solo alfanuméricos)
**BYPASS**: editName NO sanitiza new_name!

### 2. SSRF en communicate.php (línea 17)
```php
curl_setopt($ch, CURLOPT_URL, $parsedUrl['host']);
```
**BUG**: Solo pasa hostname, no la URL completa
**VALIDACIÓN**: Host debe terminar en motherland.com
**LIMITACIÓN**: CURLOPT_TIMEOUT = 1 segundo

### 3. SSTI en Smarty
**VECTOR**: $name se renderiza sin escapar en index.tpl línea 135
```
<h2>Yo, {$name}</h2>
```
**PROBLEMA**: editName no sanitiza new_name
**OBJETIVO**: RCE para leer flag con nombre aleatorio

### 4. Función edit solo desde localhost (index.php línea 45)
```php
if ($_SERVER['REMOTE_ADDR'] != '127.0.0.1') {
    $smarty->assign('error', "Only localhost can use this function!");
```

## CADENA DE EXPLOTACIÓN TEÓRICA
1. SSRF para hacer POST desde localhost -> edit
2. Cambiar nombre con payload SSTI o SQLi
3. Ejecutar código o extraer datos
4. Leer flag

## PROBLEMA ACTUAL
motherland.com NO RESUELVE en el servidor -> DNS timeout

## HIPÓTESIS
1. **El reto está mal configurado** - Poco probable para HTB retired
2. **Necesito controlar motherland.com** - Imposible desde aquí
3. **HAY OTRO ENFOQUE QUE NO ESTOY VIENDO**

## LO QUE NO HE INTENTADO SUFICIENTEMENTE

### A. Explotar SQL Injection sin cambiar nombre
¿Puedo inyectar en planet o username de alguna forma?

### B. Bypass de la validación de IP
¿X-Forwarded-For funciona? ¿Otras headers?

### C. Explotar el timeout corto de curl
¿Alguna forma de hacer que llegue antes del timeout?

### D. Revisar versión exacta de Smarty
Composer en PHP 7.0 (2015) instalaría Smarty 3.1.x
¿Hay CVEs específicas?

### E. Otros vectores en communicate.php
El código tiene CURLOPT_HTTPHEADER con la cookie
¿Puedo inyectar headers?
