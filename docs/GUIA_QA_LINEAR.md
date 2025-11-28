# 🧪 Guía de Uso: Sistema de Automatización de Casos de Prueba + Linear

## 🎯 **Para tu Equipo QA**

### **Flujo de Trabajo Recomendado**

1. **📝 Crear Historia de Usuario** → 2. **🤖 Generar Casos** → 3. **📤 Exportar a Linear** → 4. **👥 Asignar al Equipo**

---

## 🚀 **Paso 1: Crear Historia de Usuario**

### **Formato Estándar:**
```
Historia de Usuario: [Nombre de la funcionalidad]

Como [tipo de usuario]
Quiero [funcionalidad específica]
Para [beneficio/objetivo]

Descripción:
[Descripción detallada de la funcionalidad]

Criterios de Aceptación:

1. Dado que [condición inicial]
   Cuando [acción del usuario]
   Entonces [resultado esperado]

2. Dado que [condición inicial]
   Cuando [acción del usuario]
   Entonces [resultado esperado]
```

### **Ejemplo Real:**
```
Historia de Usuario: Sistema de Registro de Usuarios

Como visitante del sitio web
Quiero poder registrarme con mi información personal
Para acceder a las funcionalidades exclusivas de la plataforma

Descripción:
El sistema debe permitir a nuevos usuarios crear una cuenta utilizando su email, 
contraseña y datos personales básicos. Debe incluir validaciones de seguridad 
y confirmación por email.

Criterios de Aceptación:

1. Dado que soy un visitante nuevo
   Cuando ingreso email, contraseña y datos válidos
   Entonces debo recibir un email de confirmación

2. Dado que soy un visitante
   Cuando intento registrarme con un email ya existente
   Entonces debo ver el mensaje "Este email ya está registrado"

3. Dado que soy un visitante
   Cuando ingreso una contraseña débil
   Entonces debo ver indicadores de fortaleza de contraseña
```

---

## 🤖 **Paso 2: Generar Casos de Prueba**

### **Comando Básico:**
```bash
python test_case_automation.py mi_historia.txt --output casos_mi_feature --format all
```

### **Con Plantilla Específica:**
```bash
# Para aplicaciones web
python interactive_generator.py
# Selecciona opción 2 (cargar archivo)
# Selecciona plantilla "Aplicación Web"

# Para APIs
python interactive_generator.py
# Selecciona plantilla "API"

# Para aplicaciones móviles
python interactive_generator.py
# Selecciona plantilla "Aplicación Móvil"
```

### **Archivos Generados:**
- `casos_mi_feature.xlsx` - Para revisión en Excel
- `casos_mi_feature.csv` - Para importar a otras herramientas
- `casos_mi_feature.json` - Para integración con Linear

---

## 📤 **Paso 3: Exportar a Linear**

### **Comando de Integración:**
```bash
python linear_integration.py
```

### **Archivos para Linear:**
- `linear_import.csv` - **Importar directamente a Linear**
- `linear_issues.json` - Para importación programática

---

## 👥 **Paso 4: Importar a Linear**

### **Método 1: Importación CSV (Recomendado)**

1. **Abrir Linear** → Tu equipo QA
2. **Ir a Settings** → Import
3. **Seleccionar CSV** → Subir `linear_import.csv`
4. **Mapear campos:**
   - Title → Título del issue
   - Description → Descripción
   - Labels → Etiquetas
   - Priority → Prioridad
   - State → Estado (Todo)

### **Método 2: Creación Manual**

1. **Copiar desde** `linear_issues.json`
2. **Crear issues** uno por uno en Linear
3. **Asignar** a miembros del equipo
4. **Organizar** en sprints

---

## 🎨 **Plantillas Disponibles**

### **🌐 Aplicación Web**
- Compatibilidad de navegadores
- Diseño responsivo
- Accesibilidad
- Rendimiento web

### **📱 Aplicación Móvil**
- Compatibilidad de dispositivos
- Gestos táctiles
- Conectividad de red
- Rendimiento móvil

### **🔌 API**
- Contratos de API
- Seguridad
- Rendimiento
- Integración

---

## 📊 **Estructura de Casos en Linear**

### **Título:**
```
[TC-001] Verificar login con credenciales válidas - Funcional
```

### **Descripción:**
```markdown
**Descripción:** Verificar que un usuario puede iniciar sesión correctamente

**Precondiciones:**
• Usuario registrado en el sistema
• Credenciales válidas disponibles

**Pasos:**
1. Navegar a la página de login
2. Ingresar email válido
3. Ingresar contraseña válida
4. Hacer clic en "Iniciar Sesión"

**Resultado Esperado:** El usuario es redirigido al dashboard principal

**Historia de Usuario:** Sistema de Login
```

### **Etiquetas:**
- `qa` - Identifica casos de QA
- `funcional` - Tipo de prueba
- `happy-path` - Flujo principal
- `login` - Módulo específico

---

## ⚙️ **Configuración Personalizada**

### **Archivo: `qa_config.json`**
```json
{
  "validation": {
    "min_steps": 3,
    "max_steps": 8,
    "min_description_length": 30
  },
  "generation": {
    "include_performance_tests": true,
    "include_security_tests": true,
    "max_cases_per_criteria": 5
  },
  "export": {
    "default_format": "excel",
    "include_validation_results": true
  }
}
```

---

## 🔄 **Flujo de Trabajo del Equipo**

### **1. Product Owner/BA:**
- Crea historias de usuario
- Define criterios de aceptación
- Entrega archivo `.txt` al equipo QA

### **2. QA Lead:**
- Ejecuta generación de casos
- Revisa calidad y cobertura
- Exporta a Linear
- Asigna casos al equipo

### **3. QA Tester:**
- Recibe casos asignados en Linear
- Ejecuta pruebas
- Reporta resultados
- Actualiza estado en Linear

### **4. QA Manager:**
- Monitorea progreso
- Revisa métricas de calidad
- Ajusta configuración según necesidades

---

## 📈 **Métricas y Calidad**

### **Validación Automática:**
- **Puntaje de Calidad:** 0-100
- **Cobertura:** Porcentaje de tipos de prueba
- **Completitud:** Campos requeridos presentes
- **Claridad:** Descripciones detalladas

### **Niveles de Calidad:**
- **Excelente:** 90-100 puntos
- **Bueno:** 80-89 puntos
- **Aceptable:** 70-79 puntos
- **Necesita Mejoras:** 60-69 puntos
- **Crítico:** <60 puntos

---

## 🛠️ **Comandos Útiles**

### **Generación Rápida:**
```bash
# Casos básicos
python test_case_automation.py historia.txt --output casos

# Con plantilla web
python interactive_generator.py

# Solo Excel
python test_case_automation.py historia.txt --format excel

# Solo JSON para Linear
python test_case_automation.py historia.txt --format json
```

### **Validación:**
```bash
# Probar sistema
python test_system.py

# Verificar instalación
python setup.py
```

---

## 💡 **Tips y Mejores Prácticas**

### **Para Historias de Usuario:**
- ✅ Usa formato Given-When-Then
- ✅ Sé específico en criterios
- ✅ Incluye casos edge y negativos
- ✅ Define precondiciones claras

### **Para Casos de Prueba:**
- ✅ Revisa la validación de calidad
- ✅ Ajusta configuración según proyecto
- ✅ Usa plantillas apropiadas
- ✅ Organiza por módulos/funcionalidades

### **Para Linear:**
- ✅ Asigna casos a testers específicos
- ✅ Usa etiquetas consistentes
- ✅ Organiza en sprints
- ✅ Actualiza estados regularmente

---

## 🆘 **Solución de Problemas**

### **Error: "Python not found"**
```bash
# Verificar instalación
python --version

# Si no funciona, reinstalar Python
# Descargar desde python.org
# Marcar "Add Python to PATH"
```

### **Error: "Module not found"**
```bash
# Instalar dependencias
pip install -r requirements.txt
```

### **Error: "File not found"**
```bash
# Verificar que estás en el directorio correcto
cd C:\test_automation_tool

# Verificar archivos
ls *.txt
```

---

## 📞 **Soporte**

- **Documentación:** README.md
- **Ejemplos:** ejemplo_login.txt
- **Configuración:** qa_config_example.json
- **Pruebas:** python test_system.py

---

**¡Desarrollado con ❤️ para equipos QA eficientes!**
