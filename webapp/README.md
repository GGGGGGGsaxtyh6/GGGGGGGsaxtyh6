# 🚀 WebApp Dinámica con Flask

Una aplicación web moderna y completa con sistema de autenticación, gestión de posts y tareas, construida con Flask y SQLite.

## ✨ Características

- 🔐 **Sistema de Autenticación Completo**
  - Registro de usuarios
  - Login/Logout
  - Sesiones persistentes
  - Contraseñas encriptadas

- 📝 **Gestión de Posts**
  - Crear y publicar posts
  - Sistema de likes
  - Feed de la comunidad

- ✅ **Lista de Tareas**
  - Añadir tareas con prioridades
  - Marcar como completadas
  - Eliminar tareas

- 👤 **Perfiles de Usuario**
  - Perfil personalizable
  - Biografía
  - Estadísticas del usuario
  - Avatar con colores únicos

- 📊 **Dashboard Interactivo**
  - Estadísticas en tiempo real
  - Posts recientes
  - Tareas pendientes
  - Acciones rápidas

## 🛠️ Tecnologías Utilizadas

- **Backend:** Flask (Python)
- **Base de Datos:** SQLite con SQLAlchemy
- **Frontend:** HTML5, CSS3, JavaScript
- **Autenticación:** Flask-Login
- **Estilos:** CSS personalizado con diseño responsive
- **Iconos:** RemixIcon

## 📦 Instalación

1. **Clonar el repositorio:**
```bash
git clone https://github.com/GGGGGGGsaxtyh6/GGGGGGGsaxtyh6.git
cd GGGGGGGsaxtyh6/webapp
```

2. **Crear entorno virtual:**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

4. **Ejecutar la aplicación:**
```bash
python app.py
```

5. **Abrir en el navegador:**
```
http://localhost:5000
```

## 🎮 Usuario Demo

Para probar la aplicación rápidamente:
- **Usuario:** demo
- **Contraseña:** demo123

## 📱 Capturas de Pantalla

### Página de Inicio
- Hero section con características
- Botones de registro y login
- Grid de características

### Dashboard
- Estadísticas del usuario
- Posts recientes
- Tareas pendientes
- Acciones rápidas

### Sistema de Posts
- Crear nuevos posts
- Feed de la comunidad
- Sistema de likes

### Gestión de Tareas
- Añadir tareas con prioridades
- Marcar como completadas
- Filtros y organización

## 🔧 Estructura del Proyecto

```
webapp/
├── app.py                 # Aplicación principal Flask
├── requirements.txt       # Dependencias Python
├── database.db           # Base de datos SQLite (se crea automáticamente)
├── templates/            # Plantillas HTML
│   ├── base.html        # Plantilla base
│   ├── index.html       # Página de inicio
│   ├── login.html       # Página de login
│   ├── register.html    # Página de registro
│   ├── dashboard.html   # Dashboard del usuario
│   ├── profile.html     # Perfil del usuario
│   ├── posts.html       # Lista de posts
│   ├── create_post.html # Crear nuevo post
│   └── todos.html       # Gestión de tareas
└── static/              # Archivos estáticos
    ├── css/
    │   └── style.css    # Estilos CSS
    └── js/
        └── main.js      # JavaScript principal
```

## 🚀 Características Destacadas

1. **Diseño Responsive:** Funciona perfectamente en dispositivos móviles y desktop
2. **Animaciones Suaves:** Transiciones y efectos visuales agradables
3. **Validación de Formularios:** Validación en cliente y servidor
4. **Mensajes Flash:** Notificaciones para todas las acciones
5. **Base de Datos Persistente:** Todos los datos se guardan en SQLite

## 🔒 Seguridad

- Contraseñas hasheadas con Werkzeug
- Protección CSRF con Flask
- Validación de entrada de usuario
- Sesiones seguras

## 📝 API Endpoints

- `GET /` - Página de inicio
- `GET/POST /register` - Registro de usuarios
- `GET/POST /login` - Inicio de sesión
- `GET /logout` - Cerrar sesión
- `GET /dashboard` - Dashboard del usuario
- `GET /profile` - Perfil del usuario
- `GET/POST /posts` - Lista de posts
- `GET/POST /posts/create` - Crear nuevo post
- `POST /posts/<id>/like` - Dar like a un post
- `GET/POST /todos` - Gestión de tareas
- `POST /todos/add` - Añadir nueva tarea
- `POST /todos/<id>/toggle` - Marcar tarea como completada
- `POST /todos/<id>/delete` - Eliminar tarea

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una nueva rama
3. Realiza tus cambios
4. Envía un pull request

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la Licencia MIT.

## 👨‍💻 Autor

Creado con ❤️ usando Flask y Cursor AI

---

**Nota:** Esta es una aplicación de demostración con fines educativos. Para uso en producción, se recomienda usar PostgreSQL o MySQL en lugar de SQLite y configurar variables de entorno para las claves secretas.