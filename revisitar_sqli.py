#!/usr/bin/env python3
"""
Revisitar SQLi desde OTRO ángulo

searchUser hace:
SET @sql = CONCAT('SELECT * FROM users WHERE name = \'', name, '\'');
PREPARE stmt FROM @sql;
EXECUTE stmt;

Si name = test' OR '1'='1
Resulta en: SELECT * FROM users WHERE name = 'test' OR '1'='1'

Esto devolvería MÚLTIPLES filas.

¿Qué pasa si searchUser devuelve múltiples usuarios?

index.php línea 26: $user = $result->fetch_object();

Solo obtiene la PRIMERA fila.

Pero... ¿qué pasa si inyecto algo que modifique CUÁL fila se devuelve?

O mejor... ¿puedo hacer un UNION injection para controlar QUÉ se devuelve?

name = ' UNION SELECT 'MALICIOUS', 'x', 'y', 'z', 'a' -- 

Pero necesito saber cuántas columnas tiene la tabla users.

Según init.sql:
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    username VARCHAR(20) NOT NULL UNIQUE,
    password VARCHAR(20) NOT NULL,
    planet VARCHAR(20) NOT NULL
);

5 columnas: id, name, username, password, planet

Entonces: ' UNION SELECT 1, 'PAYLOAD_SSTI', 'x', 'y', 'z' --

Esto haría que $user->name sea 'PAYLOAD_SSTI'

¡Y ESO se renderizaría en Smarty con SSTI!

PERO... ¿cómo meto ese nombre en la sesión?

$_SESSION['name'] se establece durante el LOGIN desde la BD.

A menos que... ¿pueda inyectar durante el LOGIN también?

loginUser hace:
SELECT name, planet, id FROM users WHERE username = ? AND password = ?

Usa prepared statements, así que NO hay SQLi allí.

PERO... searchUser se llama en index.php con $_SESSION['name'].

Si pudiera hacer que $_SESSION['name'] contenga un payload SQLi...

Espera. ¿Qué pasa si registro un usuario con nombre normal, pero luego de alguna forma modifico $_SESSION directamente?

No puedo modificar $_SESSION desde el cliente.

PERO... ¿hay algún endpoint que ESTABLEZCA variables de sesión basadas en input?

No he visto ninguno.

Estoy en un callejón sin salida otra vez.
"""
print("[*] Análisis de SQLi:")
print()
print("1. searchUser es vulnerable a SQLi")
print("2. Pero se llama con $_SESSION['name']")
print("3. $_SESSION['name'] viene de la BD después del login")
print("4. register.php sanitiza el nombre antes de insertarlo")
print("5. No hay forma obvia de inyectar un nombre malicioso en la BD")
print()
print("CONCLUSIÓN: Necesito encontrar OTRA forma de poner un nombre malicioso en la BD")
print()
print("Opciones:")
print("a) Usar editName via SSRF (requiere motherland.com)")
print("b) Encontrar otro vector de SQLi que permita UPDATE")
print("c) Explotar alguna race condition")
print("d) Manipular la sesión directamente (poco probable)")
print("e) HAY OTRO BUG QUE NO ESTOY VIENDO")
