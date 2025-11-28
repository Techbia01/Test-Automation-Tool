tio
# 🌐 Sistema Web QA - Guía de Uso

## 🎯 **Sistema Web Completo para Equipos QA**

¡Ahora tienes una aplicación web completa para generar casos de prueba de forma interactiva!

---

## 🚀 **Cómo Iniciar el Sistema**

### **1. Iniciar la Aplicación Web**
```bash
python start_web_app.py
```

### **2. Acceder a la Aplicación**
- **URL:** http://localhost:5000
- **Se abre automáticamente** en tu navegador
- **Puerto:** 5000 (configurable)

---

## 📋 **Flujo de Trabajo Completo**

### **Paso 1: Crear Nuevo Proyecto**
1. **Hacer clic** en "Nuevo Proyecto"
2. **Completar información:**
   - Nombre del proyecto
   - Descripción (opcional)
   - **Pegar historia de usuario** completa
   - **Agregar comentarios de QA** (opcional)

### **Paso 2: Validar Historia de Usuario**
1. **Hacer clic** en "Validar Historia"
2. **Revisar** el resultado de la validación:
   - Título extraído
   - Criterios de aceptación encontrados
   - Errores o advertencias

### **Paso 3: Crear Proyecto**
1. **Hacer clic** en "Crear Proyecto"
2. **Ser redirigido** a la página de detalles

### **Paso 4: Generar Casos de Prueba**
1. **Seleccionar plantilla:**
   - Sin plantilla (casos básicos)
   - Aplicación Web
   - Aplicación Móvil
   - API
2. **Agregar comentarios adicionales** (opcional)
3. **Hacer clic** en "Generar Casos de Prueba"

### **Paso 5: Revisar y Exportar**
1. **Revisar** los casos generados
2. **Ver validación de calidad**
3. **Exportar** en formato CSV o para Linear

---

## 🎨 **Características del Sistema Web**

### **✅ Interfaz Intuitiva**
- **Diseño moderno** con Bootstrap 5
- **Responsive** para móviles y tablets
- **Navegación fácil** entre secciones

### **✅ Validación en Tiempo Real**
- **Parseo automático** de historias de usuario
- **Validación de criterios** de aceptación
- **Detección de errores** en formato

### **✅ Generación Inteligente**
- **Plantillas especializadas** (Web, Móvil, API)
- **Validación de calidad** automática
- **Métricas de cobertura** y puntaje

### **✅ Gestión de Proyectos**
- **Almacenamiento persistente** de proyectos
- **Historial completo** de generaciones
- **Exportación múltiple** de formatos

### **✅ Integración con Linear**
- **Exportación directa** para Linear
- **Formato CSV** optimizado
- **Metadatos completos** incluidos

---

## 📊 **Panel de Control**

### **Dashboard Principal**
- **Estadísticas** de proyectos
- **Lista de proyectos** recientes
- **Acceso rápido** a funciones

### **Información de Proyectos**
- **Estado** (Borrador/Generado)
- **Plantilla utilizada**
- **Número de casos** generados
- **Fecha de creación**

### **Validación de Calidad**
- **Puntaje** de 0-100
- **Nivel de calidad** (Excelente/Bueno/Aceptable)
- **Cobertura** de tipos de prueba
- **Recomendaciones** automáticas

---

## 🔧 **Funcionalidades Avanzadas**

### **Validación de Historias de Usuario**
- **Extracción automática** de título
- **Detección de criterios** de aceptación
- **Validación de formato** Given-When-Then
- **Sugerencias de mejora**

### **Generación de Casos**
- **Casos funcionales** por criterio
- **Casos de integración** automáticos
- **Casos límite** y negativos
- **Casos específicos** por plantilla

### **Exportación Flexible**
- **CSV estándar** para revisión
- **CSV para Linear** con formato optimizado
- **Metadatos completos** incluidos
- **Descarga directa** desde el navegador

---

## 💡 **Tips y Mejores Prácticas**

### **Para Historias de Usuario:**
- ✅ **Usa formato estándar** Given-When-Then
- ✅ **Incluye descripción detallada**
- ✅ **Especifica criterios claros**
- ✅ **Agrega casos edge** en comentarios

### **Para Comentarios de QA:**
- ✅ **Especifica validaciones adicionales**
- ✅ **Menciona casos límite importantes**
- ✅ **Indica requisitos de seguridad**
- ✅ **Detalla flujos alternativos**

### **Para Plantillas:**
- ✅ **Web:** Para aplicaciones con navegador
- ✅ **Móvil:** Para apps iOS/Android
- ✅ **API:** Para servicios REST/GraphQL
- ✅ **Sin plantilla:** Para casos básicos

---

## 🛠️ **Comandos Útiles**

### **Iniciar Sistema:**
```bash
# Iniciar aplicación web
python start_web_app.py

# Iniciar con puerto específico
python app.py
```

### **Verificar Instalación:**
```bash
# Verificar dependencias
pip list | grep -E "(flask|pandas|openpyxl)"

# Probar módulos
python -c "from app import app; print('✅ App OK')"
```

### **Desarrollo:**
```bash
# Modo debug
export FLASK_DEBUG=1
python app.py

# Ver logs
tail -f app.log
```

---

## 🔄 **Integración con Linear**

### **Exportación para Linear:**
1. **Generar casos** en el sistema web
2. **Hacer clic** en "Exportar para Linear"
3. **Descargar** archivo CSV
4. **Importar** en Linear

### **Formato Linear:**
- **Título:** [TC-001] Descripción del caso
- **Descripción:** Formato markdown completo
- **Labels:** qa, funcional, happy-path
- **Prioridad:** Alta/Media/Baja
- **Estado:** Todo

### **Importación en Linear:**
1. **Linear** → Settings → Import
2. **Seleccionar CSV** descargado
3. **Mapear campos** automáticamente
4. **Importar** casos de prueba

---

## 🆘 **Solución de Problemas**

### **Error: "Puerto 5000 en uso"**
```bash
# Cambiar puerto en app.py
app.run(port=5001)

# O matar proceso en puerto 5000
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### **Error: "Módulo no encontrado"**
```bash
# Instalar dependencias
pip install -r requirements.txt

# Verificar instalación
python -c "import flask, pandas, openpyxl"
```

### **Error: "No se pueden generar casos"**
- Verificar que la historia de usuario tenga criterios
- Revisar formato Given-When-Then
- Comprobar que no haya caracteres especiales

### **Error: "No se puede exportar"**
- Verificar que existan casos generados
- Comprobar permisos de escritura
- Revisar espacio en disco

---

## 📈 **Métricas y Monitoreo**

### **Métricas de Calidad:**
- **Puntaje promedio** por proyecto
- **Cobertura** de tipos de prueba
- **Casos válidos** vs inválidos
- **Tiempo de generación**

### **Estadísticas de Uso:**
- **Proyectos creados** por día/semana
- **Plantillas más utilizadas**
- **Exportaciones** a Linear
- **Errores más comunes**

---

## 🎉 **¡Sistema Completo Listo!**

### **Lo que tienes ahora:**
- ✅ **Aplicación web completa**
- ✅ **Interfaz intuitiva**
- ✅ **Generación automática**
- ✅ **Validación de calidad**
- ✅ **Exportación a Linear**
- ✅ **Gestión de proyectos**

### **Próximos pasos:**
1. **Inicia** la aplicación web
2. **Crea** tu primer proyecto
3. **Pega** una historia de usuario
4. **Genera** casos de prueba
5. **Exporta** para Linear

---

**¡Desarrollado con ❤️ para equipos QA eficientes!**
