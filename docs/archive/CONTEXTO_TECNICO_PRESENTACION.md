# 🏗️ Contexto Técnico del Sistema - Para Presentación

## 📋 Índice
1. [Arquitectura General](#arquitectura-general)
2. [Stack Tecnológico](#stack-tecnológico)
3. [Componentes Principales](#componentes-principales)
4. [Flujo de Funcionamiento](#flujo-de-funcionamiento)
5. [Detalles Técnicos Clave](#detalles-técnicos-clave)
6. [Integraciones](#integraciones)
7. [Decisiones de Diseño](#decisiones-de-diseño)

---

## 🏛️ Arquitectura General

### **Tipo de Arquitectura**
- **Arquitectura:** Cliente-Servidor (Web Application)
- **Patrón:** MVC (Model-View-Controller) simplificado
- **Comunicación:** HTTP/REST API
- **Almacenamiento:** JSON local (sin base de datos externa)

### **Estructura del Sistema**
```
Cliente (Navegador)
    ↓ HTTP Requests
Servidor Flask (Python)
    ↓ Procesamiento
Generador de Casos de Prueba
    ↓
Parser de Historias de Usuario
    ↓
Exportador/Integrador Linear
    ↓
Respuesta JSON/HTML
```

---

## 💻 Stack Tecnológico

### **Backend**
- **Framework:** Flask 3.1.2 (Python)
- **Lenguaje:** Python 3.8+
- **Procesamiento de Datos:** Pandas 2.3.3
- **HTTP Client:** Requests 2.32.5
- **Parsing:** Regex + NLP básico (análisis de texto)

### **Frontend**
- **Templates:** Jinja2 (incluido en Flask)
- **Estilos:** CSS3 (custom + Bootstrap components)
- **JavaScript:** Vanilla JS (sin frameworks)
- **UI Framework:** Bootstrap 5 (componentes modales, cards)

### **Almacenamiento**
- **Formato:** JSON (archivo local `qa_projects.json`)
- **Ventaja:** No requiere base de datos, cada usuario tiene sus propios datos
- **Persistencia:** LocalStorage del navegador (API Keys)

### **Integraciones Externas**
- **Linear API:** GraphQL (subida de casos de prueba)
- **Exportación:** CSV, Excel (openpyxl)

---

## 🔧 Componentes Principales

### **1. Servidor Flask (`app.py` / `main.py`)**

**Responsabilidades:**
- Manejar rutas HTTP (GET, POST)
- Servir templates HTML
- Procesar requests del frontend
- Gestionar proyectos (CRUD básico)

**Rutas Principales:**
```python
GET  /                          # Página principal (lista proyectos)
GET  /new_project               # Formulario crear proyecto
POST /create_project            # Crear nuevo proyecto
GET  /project/<id>              # Detalle del proyecto
POST /generate_test_cases       # Generar casos de prueba
POST /upload_to_linear/<id>    # Subir casos a Linear
GET  /export_linear_simple/<id> # Exportar CSV para Linear
```

**Características:**
- Encoding UTF-8 configurado para Windows
- Manejo de errores con try/except
- Respuestas JSON para API calls

---

### **2. Generador de Casos de Prueba (`src/professional_qa_generator.py`)**

**Responsabilidades:**
- Parsear historias de usuario
- Extraer criterios de aceptación
- Generar casos de prueba profesionales
- Aplicar reglas de negocio

**Clases Principales:**
```python
class ProfessionalQAGenerator:
    - generate_test_cases()      # Método principal
    - extract_criteria_from_text() # Extrae criterios
    - _decompose_criterion_into_test_cases() # Descompone en casos
    - _generate_professional_title() # Genera títulos profesionales
```

**Algoritmo de Generación:**
1. **Parseo Adaptativo:** Detecta estructura de la HU (tradicional, narrativa, EMS)
2. **Extracción de Criterios:** Múltiples estrategias (Gherkin, listas, bullets, análisis de líneas)
3. **Descomposición:** Cada criterio se descompone en casos específicos
4. **Generación de Títulos:** Patrón "Validar que [acción] [entidad] [condición] [resultado]"
5. **Priorización:** Alta/Media/Baja según tipo de caso
6. **Formato Gherkin:** Given/When/Then automático

**Características Técnicas:**
- **Parser Adaptativo:** Detecta automáticamente el formato de la HU
- **Múltiples Estrategias:** Si una falla, prueba otras
- **Eliminación de Redundancia:** Máximo 1 caso por criterio (excepto creación vs edición)
- **Títulos Completos:** 120-180 caracteres, sin truncar

---

### **3. Parser de Historias de Usuario (`src/adaptive_parser.py`)**

**Responsabilidades:**
- Detectar estructura de la HU
- Extraer contexto, flujos, estados
- Identificar elementos UI

**Tipos de Estructura Detectados:**
- **Tradicional:** "Como... quiero... para..."
- **Narrativa/EMS:** Con contexto, descripción, flujos
- **Mixta:** Combinación de ambos

---

### **4. Integración con Linear (`src/linear_api_client.py`)**

**Responsabilidades:**
- Conectar con Linear API (GraphQL)
- Crear sub-issues automáticamente
- Detectar equipos automáticamente
- Manejar estados y prioridades

**Características:**
- **Detección Automática de Equipo:** Por prefijo del issue (FIN-1264 → Equipo Finanzas)
- **Sub-issues:** Los casos se crean como hijos de la HU
- **Estados:** Configurable (por defecto "Todo")
- **Manejo de Errores:** Reintentos y mensajes claros

**API GraphQL Usada:**
```graphql
mutation {
  issueCreate(
    input: {
      title: "..."
      description: "..."
      teamId: "..."
      parentId: "..."
      stateId: "..."
    }
  ) {
    success
    issue { id, identifier }
  }
}
```

---

### **5. Exportadores (`exporters/`)**

**Tipos de Exportación:**
- **CSV Simple:** Para importación manual en Linear
- **CSV Sub-issues:** Con relación padre-hijo
- **Excel:** Con formato mejorado (openpyxl)

---

## 🔄 Flujo de Funcionamiento

### **Flujo Completo: Generar Casos de Prueba**

```
1. Usuario ingresa Historia de Usuario en el formulario
   ↓
2. Frontend envía POST /create_project con los datos
   ↓
3. Servidor guarda proyecto en qa_projects.json
   ↓
4. Usuario hace click en "Generar Casos de Prueba"
   ↓
5. Frontend envía POST /generate_test_cases
   ↓
6. Servidor llama a ProfessionalQAGenerator.generate_test_cases()
   ↓
7. Parser adaptativo analiza la estructura de la HU
   ↓
8. Se extraen criterios de aceptación (múltiples estrategias)
   ↓
9. Cada criterio se descompone en casos de prueba
   ↓
10. Se generan títulos profesionales (patrón específico)
    ↓
11. Se crean pasos en formato Gherkin (Given/When/Then)
    ↓
12. Se asigna prioridad y tipo a cada caso
    ↓
13. Se retornan casos al frontend en formato JSON
    ↓
14. Frontend renderiza casos en cards modernas
    ↓
15. Usuario puede editar, exportar o subir a Linear
```

---

## 🔑 Detalles Técnicos Clave

### **1. Manejo de Encoding UTF-8**

**Problema:** Windows usa 'charmap' por defecto, causando errores con caracteres especiales.

**Solución:**
```python
if sys.platform == 'win32':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    else:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
```

**Ubicación:** `main.py`, `app.py`, `src/professional_qa_generator.py`

---

### **2. Almacenamiento Local (Sin Base de Datos)**

**Decisión:** Usar JSON en lugar de base de datos SQL.

**Razones:**
- ✅ Simplicidad: No requiere instalación de DB
- ✅ Portabilidad: Cada usuario tiene sus propios datos
- ✅ Sin conflictos: No hay problemas de sincronización
- ✅ Fácil backup: Solo copiar un archivo

**Archivo:** `qa_projects.json` (en `.gitignore`)

**Estructura:**
```json
{
  "proj_1_1234567890": {
    "id": "proj_1_1234567890",
    "name": "Nombre del Proyecto",
    "user_story": "...",
    "test_cases": [...],
    "created_at": "2024-01-01T00:00:00",
    "status": "generated"
  }
}
```

---

### **3. Generación Inteligente de Títulos**

**Patrón Obligatorio:**
```
"Validar que [evento/acción] [entidad] [condición específica] [resultado esperado observable]"
```

**Ejemplo:**
```
"Validar que al cambiar una frontera de tipo Residencial a Industrial 
se reasigne el estrato correctamente"
```

**Características:**
- Longitud: 120-180 caracteres
- Sin truncar: Si es muy largo, se reformula
- Siempre completo: Oración cerrada
- Específico: No genérico

---

### **4. Eliminación de Redundancia**

**Problema:** Generar múltiples casos para el mismo criterio.

**Solución:**
- Máximo 1 caso por criterio de aceptación
- Consolidación de validaciones relacionadas (persistencia, UI, usabilidad)
- Separación explícita solo si aplica creación vs edición

**Lógica:**
```python
def _decompose_criterion_into_test_cases(self, criterion, ...):
    # Genera happy path (incluye persistencia si aplica)
    # Genera casos negativos solo si el criterio los menciona
    # Genera casos de error solo si el criterio los menciona
    # NO genera casos genéricos
```

---

### **5. Parser Adaptativo Multi-Estrategia**

**Estrategias en Orden:**
1. **Parser Adaptativo:** Detecta estructura (tradicional/narrativa)
2. **Gherkin:** Busca Given/When/Then
3. **Emojis:** Busca criterios con emojis (✅, ✔️, etc.)
4. **Listas Numeradas:** 1., 2., 3.
5. **Bullets:** -, *, •
6. **Análisis de Líneas:** Líneas individuales con palabras clave
7. **División por Frases:** Último recurso

**Ventaja:** Funciona con cualquier formato de HU.

---

### **6. Manejo de Conflictos Git**

**Problema:** Conflictos al trabajar en equipo.

**Solución Implementada:**
- Scripts de sincronización automática
- Guía de trabajo en equipo
- `.gitignore` completo para archivos locales
- Configuración de encoding para evitar problemas

---

## 🔌 Integraciones

### **Linear API**

**Tipo:** GraphQL API
**Autenticación:** API Key (Bearer token)
**Endpoint:** https://api.linear.app/graphql

**Características:**
- Detección automática de equipo por prefijo
- Creación de sub-issues automática
- Manejo de estados y prioridades
- Reintentos en caso de error

**Flujo:**
1. Usuario ingresa API Key (se guarda en localStorage)
2. Usuario ingresa ID de HU padre
3. Sistema detecta equipo automáticamente
4. Crea sub-issues para cada caso de prueba
5. Retorna lista de issues creados

---

## 🎨 Decisiones de Diseño

### **1. ¿Por qué Flask y no Django?**
- **Razón:** Simplicidad y flexibilidad
- **Ventaja:** Menos overhead, más control
- **Ideal para:** Aplicaciones medianas como esta

### **2. ¿Por qué JSON y no Base de Datos?**
- **Razón:** Cada usuario trabaja localmente
- **Ventaja:** Sin problemas de sincronización
- **Ideal para:** Herramientas de escritorio/web local

### **3. ¿Por qué Vanilla JS y no React/Vue?**
- **Razón:** Simplicidad y mantenibilidad
- **Ventaja:** Menos dependencias, más rápido
- **Ideal para:** Aplicaciones con lógica principalmente en backend

### **4. ¿Por qué Múltiples Estrategias de Parsing?**
- **Razón:** Las HUs vienen en diferentes formatos
- **Ventaja:** Mayor tasa de éxito en extracción
- **Ideal para:** Entornos donde no hay estándar fijo

### **5. ¿Por qué Generación Automática y no Manual?**
- **Razón:** Ahorro de tiempo (80% del trabajo)
- **Ventaja:** Consistencia y cobertura completa
- **Ideal para:** Equipos QA con muchas HUs

---

## 📊 Métricas y Rendimiento

### **Tiempos Típicos:**
- **Parseo de HU:** 0.5-2 segundos
- **Generación de casos:** 2-5 segundos (depende de cantidad de criterios)
- **Subida a Linear:** 1-2 segundos por caso (depende de API)

### **Capacidad:**
- **Proyectos:** Ilimitados (solo limitado por espacio en disco)
- **Casos por proyecto:** Recomendado hasta 50-100 casos
- **Criterios por HU:** Funciona bien con 5-20 criterios

---

## 🛡️ Seguridad y Privacidad

### **Datos Locales:**
- ✅ `qa_projects.json` NO se sube a Git (`.gitignore`)
- ✅ API Keys se guardan en localStorage del navegador
- ✅ No hay transmisión de datos sensibles

### **Linear API:**
- ✅ API Key se envía solo a Linear (HTTPS)
- ✅ No se almacena en servidor
- ✅ Cada usuario maneja su propia API Key

---

## 🔄 Mantenimiento y Escalabilidad

### **Fácil de Extender:**
- Agregar nuevos tipos de exportación: Crear en `exporters/`
- Agregar nuevos parsers: Crear en `src/` y registrar en generador
- Agregar nuevas rutas: Agregar en `app.py`

### **Escalabilidad:**
- **Actual:** Ideal para equipos pequeños-medianos (5-20 personas)
- **Futuro:** Podría migrarse a base de datos si se necesita compartir datos

---

## 📝 Preguntas Frecuentes Técnicas

### **¿Por qué Python?**
- Librerías excelentes para procesamiento de texto (NLP básico)
- Flask es simple y potente
- Fácil integración con APIs

### **¿Por qué no usar IA/LLM directamente?**
- **Costo:** LLMs tienen costo por request
- **Velocidad:** Procesamiento local es más rápido
- **Control:** Reglas de negocio específicas y predecibles
- **Privacidad:** Datos no salen del servidor local

### **¿Cómo se garantiza la calidad de los casos generados?**
- **Parser robusto:** Múltiples estrategias de extracción
- **Reglas de negocio:** Lógica específica para cada tipo de caso
- **Validación:** Sistema de validación de calidad (QAValidator)
- **Edición manual:** Siempre se puede editar después

### **¿Qué pasa si Linear cambia su API?**
- El código está modularizado (`linear_api_client.py`)
- Solo hay que actualizar ese módulo
- El resto del sistema no se afecta

---

## 🚀 Mejoras Futuras Posibles

1. **Base de Datos:** Migrar a SQLite o PostgreSQL para compartir datos
2. **IA/LLM:** Integrar OpenAI/Claude para casos más complejos
3. **Templates:** Permitir crear plantillas personalizadas
4. **Reportes:** Generar reportes de cobertura de pruebas
5. **Integraciones:** Jira, Azure DevOps, etc.

---

**Última actualización:** 2024
**Versión del Sistema:** 1.0

