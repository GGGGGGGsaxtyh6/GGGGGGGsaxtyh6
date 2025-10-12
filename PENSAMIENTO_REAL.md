# PENSAMIENTO INTENSO - DESDE CERO

## REALIDAD
motherland.com NO RESUELVE a 127.0.0.1 en el servidor remoto.
Esto significa que el SSRF tradicional NO ES EL CAMINO.

## PREGUNTA CRÍTICA
Si motherland.com no resuelve a localhost, ¿POR QUÉ existe esa restricción?
¿Cuál es el "old bug with a twist"?

## REEVALUACIÓN COMPLETA

### Vulnerabilidades REALES disponibles:

1. **SQL Injection en searchUser** (init.sql:18)
   - Concatenación directa sin escapar
   - Se llama con $_SESSION['name']
   - Pero register.php sanitiza el nombre (línea 8)
   - ¿CÓMO PUEDO INYECTAR UN NOMBRE MALICIOSO?

2. **editName sin sanitización** (init.sql:44)
   - Acepta cualquier new_name
   - PERO requiere REMOTE_ADDR == 127.0.0.1

3. **SSTI en Smarty**
   - $name se renderiza sin escapar
   - Necesito un nombre malicioso en la BD

4. **SSRF en communicate.php**
   - Pero motherland.com no resuelve

## MOMENTO. DÉJAME VER SI HAY OTRA FORMA DE METER SQL INJECTION

¿Qué pasa si...?
- ¿Puedo manipular mi cookie de sesión para cambiar el nombre?
- ¿Hay otra ruta que llame a searchUser con input controlable?
- ¿Puedo explotar el procedimiento registerUser directamente?

## WAIT - EL PROCEDIMIENTO registerUser

```sql
CREATE PROCEDURE registerUser(IN reg_name VARCHAR(255), IN reg_username VARCHAR(255), 
                               IN reg_password VARCHAR(255), IN reg_planet VARCHAR(255))
BEGIN
    INSERT INTO users (name, username, password, planet) 
    VALUES (reg_name, reg_username, reg_password, reg_planet);
END
```

register.php sanitiza el nombre ANTES de llamar al procedimiento.
Pero... ¿qué pasa con username, password, planet?

- username: no veo sanitización
- password: no veo sanitización  
- planet: se elige aleatoriamente del array, NO controlable

PERO estos se insertan con prepared statements en register.php (línea 39).

## LOGINUSER

```sql
CREATE PROCEDURE loginUser(IN login_username VARCHAR(255), IN login_password VARCHAR(255))
BEGIN
    SELECT name, planet, id 
    FROM users 
    WHERE username = login_username AND password = login_password;
END
```

login.php usa prepared statements también (línea 13).

## MOMENTO - ¿Y SI EL BUG ESTÁ EN PHP, NO EN SQL?

PHP 7.0.33 es de 2017. Hay CVEs conocidas.

Smarty 3.1.48 - lanzado en 2023. Relativamente nuevo.

¿Qué "old bug" podría ser?

## CURL BUG

El código hace:
```php
curl_setopt($ch, CURLOPT_URL, $parsedUrl['host']);
```

Esto es INCORRECTO. curl_setopt con CURLOPT_URL espera una URL completa, no solo un hostname.

¿Qué hace curl cuando le das solo un hostname sin protocolo?

Probablemente asume http:// por defecto.

ENTONCES si le paso "motherland.com", curl hace request a http://motherland.com/

PERO... si motherland.com no existe o timeout, ¿qué?

## IDEA LOCA

¿Y si puedo hacer que motherland.com resuelva usando otros métodos?

¿Qué pasa si uso IPv6?
¿Qué pasa si uso diferentes encodings?

WAIT. Parse_url puede tener bugs conocidos en PHP 7.0!

PHP 7.0 parse_url puede ser bypasseado de ciertas formas.
