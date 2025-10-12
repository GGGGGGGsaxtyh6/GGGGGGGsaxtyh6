# SOLUCIÓN LOCAL

El reto Interstellar está configurado para requerir que motherland.com resuelva a 127.0.0.1 en el servidor.

El Dockerfile incluye:
```
RUN echo "127.0.0.1 motherland.com" >> /etc/hosts
```

Esto permite que el SSRF funcione:
1. Usuario se registra y loguea
2. Usa communicate.php con URL http://motherland.com/
3. El servidor resuelve motherland.com a 127.0.0.1
4. curl hace POST a localhost con la cookie de sesión
5. Esto llega a index.php con action=edit desde 127.0.0.1
6. editName cambia el nombre sin sanitización
7. El nuevo nombre (con payload SSTI) se almacena en la BD
8. Al acceder a index.php, searchUser devuelve el nombre
9. Smarty renderiza {$name} sin escapar
10. El payload SSTI se ejecuta: {system('cat /*flag*')}
11. Flag obtenida

PROBLEMA ACTUAL:
El servidor remoto (94.237.49.23:45329) NO tiene motherland.com configurado en /etc/hosts.
Por eso todas las requests a motherland.com dan DNS timeout.

Esto hace que el reto sea IMPOSIBLE de resolver en el servidor actual.

SOLUCIÓN:
Correr el Docker localmente con la configuración correcta.
