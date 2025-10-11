# 🔒 Demostración CVE-2024-27307: Expression Injection en JSONata

Proyecto educativo que demuestra la vulnerabilidad crítica de inyección de expresiones en JSONata (CVE-2024-27307) y presenta una implementación reforzada con múltiples capas de seguridad.

---

## 📋 Contenido del Proyecto

```
.
├── vulnerable-service.js      # ⚠️  Servicio VULNERABLE (puerto 3000)
├── hardened-service.js        # ✅ Servicio REFORZADO (puerto 3001)
├── exploit-demo.js            # 💀 Demostraciones de ataques
├── test-security.js           # 🧪 Suite de pruebas de seguridad
├── ANALISIS-VULNERABILIDAD.md # 📚 Análisis técnico completo
├── package.json               # 📦 Dependencias
└── README.md                  # 📖 Este archivo
```

---

## 🚀 Inicio Rápido

### 1. Instalación

```bash
npm install
```

### 2. Ejecutar Demostración de Vulnerabilidad

**Terminal 1** - Servicio vulnerable:
```bash
npm run vulnerable
```

**Terminal 2** - Exploits:
```bash
npm run exploit
```

Verás cómo los ataques comprometen exitosamente el servicio vulnerable.

### 3. Ejecutar Servicio Reforzado

**Terminal 1** - Servicio seguro:
```bash
npm run secure
```

**Terminal 2** - Pruebas de seguridad:
```bash
npm test
```

Verás cómo todas las amenazas son bloqueadas efectivamente.

---

## 💀 Ataques Demostrados

### 1. Prototype Pollution
Contamina `Object.prototype` afectando todos los objetos de la aplicación.

### 2. Remote Code Execution (RCE)
Utiliza el Function constructor para ejecutar código arbitrario en el servidor.

### 3. Denial of Service (DoS)
Agota recursos mediante recursión infinita o operaciones costosas.

### 4. Context Exfiltration
Intenta acceder a variables y contextos internos del servidor.

### 5. Constructor Access
Obtiene acceso a constructores de JavaScript para escalación de privilegios.

---

## 🛡️ Capas de Defensa Implementadas

El servicio reforzado implementa **5 capas de seguridad**:

### Capa 1: Validación de Expresión
- ✅ Blacklist de patrones peligrosos (`constructor`, `__proto__`, `process`, etc.)
- ✅ Límite de longitud de expresión
- ✅ Detección de sintaxis maliciosa

### Capa 2: Validación de Entrada
- ✅ Sanitización recursiva de datos de entrada
- ✅ Bloqueo de propiedades peligrosas
- ✅ Validación de tipos permitidos

### Capa 3: Evaluación Controlada
- ✅ Timeout de 5 segundos
- ✅ Límite de profundidad de recursión
- ✅ Manejo robusto de errores

### Capa 4: Sanitización de Salida
- ✅ Serialización JSON segura
- ✅ Eliminación de referencias a objetos internos
- ✅ Solo tipos primitivos y objetos simples

### Capa 5: Monitoreo y Rate Limiting
- ✅ Logging de seguridad
- ✅ Rate limiting (10 req/min por IP)
- ✅ Alertas de expresiones sospechosas

---

## 📊 Comparación

| Característica | Vulnerable | Reforzado |
|----------------|-----------|-----------|
| Validación | ❌ | ✅ |
| Timeout | ❌ | ✅ |
| Rate Limiting | ❌ | ✅ |
| Sanitización | ❌ | ✅ |
| Logging | ❌ | ✅ |
| **SEGURIDAD** | **🔴 CRÍTICO** | **🟢 SEGURO** |

---

## 🧪 Pruebas Incluidas

La suite de pruebas (`test-security.js`) verifica:

### Ataques que DEBEN ser bloqueados:
- ✓ Prototype pollution
- ✓ Acceso a constructor
- ✓ Acceso a process
- ✓ Contexto global
- ✓ Function constructor
- ✓ Expresiones muy largas
- ✓ Entrada con __proto__

### Expresiones legítimas que DEBEN ser permitidas:
- ✓ Mapeo simple
- ✓ Filtrado
- ✓ Agregaciones ($sum, $count)
- ✓ Transformaciones de objetos

---

## 📚 Documentación Completa

Para un análisis técnico exhaustivo, consulta:

📖 **[ANALISIS-VULNERABILIDAD.md](./ANALISIS-VULNERABILIDAD.md)**

Incluye:
- Descripción detallada de CVE-2024-27307
- Vectores de ataque con ejemplos
- Cadenas de explotación
- Estrategias de mitigación
- Referencias y recursos

---

## ⚠️ Advertencias Importantes

### 🔴 NUNCA EN PRODUCCIÓN

```javascript
// ❌ NUNCA HAGAS ESTO
app.post("/api", (req, res) => {
  const result = jsonata(req.body.expression).evaluate(req.body.data)
  res.json(result)
})
```

### 🟢 ALTERNATIVAS SEGURAS

1. **Expresiones pre-definidas**: Solo permite queries específicas
2. **Validación estricta**: Implementa todas las capas de defensa
3. **Sandbox aislado**: Ejecuta en entorno separado con recursos limitados
4. **Evitar evaluación de entrada del usuario**: La opción más segura

---

## 🎯 Casos de Uso Educativos

Este proyecto es ideal para:

- 🎓 **Estudiantes** aprendiendo sobre vulnerabilidades de inyección
- 👨‍💻 **Desarrolladores** implementando APIs de transformación de datos
- 🔐 **Profesionales de seguridad** realizando auditorías
- 🏢 **Equipos de desarrollo** estableciendo estándares de seguridad

---

## 🔬 Experimentos Adicionales

### Modificar Patrones Peligrosos

Edita `hardened-service.js`:
```javascript
const SECURITY_CONFIG = {
  dangerousPatterns: [
    // Agrega tus propios patrones
  ]
}
```

### Ajustar Timeouts

```javascript
const SECURITY_CONFIG = {
  evaluationTimeout: 2000, // Más restrictivo
}
```

### Implementar Whitelist Estricta

```javascript
const ALLOWED_EXPRESSIONS = {
  'query1': 'users.name',
  'query2': '$sum(orders.total)'
}
```

---

## 📊 Estadísticas de Seguridad

### CVE-2024-27307

- **CVSS Score**: 9.8 (Crítico)
- **Vector**: Network, Low Complexity, No Privileges Required
- **Impacto**: Confidentiality HIGH, Integrity HIGH, Availability HIGH

### Prevalencia

- Miles de aplicaciones Node.js usan JSONata
- Microservicios de transformación de datos en riesgo
- APIs públicas particularmente vulnerables

---

## 🤝 Contribuciones

Este es un proyecto educativo. Mejoras sugeridas:

1. Implementar sandbox con `isolated-vm`
2. Agregar más vectores de ataque
3. Implementar dashboard de monitoreo
4. Agregar tests automatizados
5. Documentar más casos de uso

---

## 📜 Licencia

MIT - Uso educativo y de investigación en seguridad.

---

## ⚡ Comandos Rápidos

```bash
# Instalar
npm install

# Servicio vulnerable
npm run vulnerable

# Servicio seguro
npm run secure

# Demostración de exploits
npm run exploit

# Suite de pruebas
npm test
```

---

## 🎓 Recursos de Aprendizaje

- [Documentación JSONata](https://jsonata.org/)
- [OWASP Expression Language Injection](https://owasp.org/www-community/vulnerabilities/Expression_Language_Injection)
- [CWE-917](https://cwe.mitre.org/data/definitions/917.html)
- [Node.js Security Best Practices](https://nodejs.org/en/docs/guides/security/)

---

## 📞 Soporte

Para preguntas sobre seguridad en aplicaciones reales:

- Consulta con tu equipo de seguridad
- Revisa las guías de OWASP
- Considera contratar una auditoría profesional

---

**⚠️ RECUERDA**: Este proyecto es para EDUCACIÓN solamente. No uses el servicio vulnerable en ningún entorno real.

**🔒 PRINCIPIO FUNDAMENTAL**: La mejor defensa contra expression injection es NO EVALUAR expresiones de usuarios no confiables.

---

**Fecha**: Octubre 2025  
**Versión**: 1.0.0  
**Estado**: Demostración Educativa
