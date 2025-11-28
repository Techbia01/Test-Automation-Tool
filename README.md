# 🧪 Sistema de Automatización de Casos de Prueba para QA

Sistema web completo para generar y gestionar casos de prueba funcionales con integración directa a Linear.

---

## ✨ Características Principales

- ✅ **Generación automática inteligente** de casos de prueba desde Historias de Usuario
- ✅ **Descompone criterios** en múltiples casos específicos (happy path, errores, usabilidad, etc.)
- ✅ **Formato profesional** con Gherkin (Given/When/Then)
- ✅ **Integración directa con Linear** (subida automática de casos)
- ✅ **Exportación a CSV** para importación manual
- ✅ **Parser robusto** que entiende diferentes formatos de HU
- ✅ **API Key persistente** (se guarda en el navegador)
- ✅ **100% local** - Cada usuario tiene sus propios datos
- ✅ **UI moderna y responsive** con diseño profesional

---

## 🚀 Instalación Rápida

### Prerrequisitos

- **Python 3.8 o superior**
- **pip** (gestor de paquetes Python)
- Navegador web moderno (Chrome, Firefox, Edge)

### Pasos de Instalación

1. **Clonar el repositorio**
   ```bash
   git clone <url-del-repositorio>
   cd test_automation_tool
   ```

2. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

3. **Iniciar el servidor**
   ```bash
   python main.py
   ```

4. **Abrir en el navegador**
   ```
   http://localhost:5000
   ```

### Scripts de Inicio (Opcional)

**Windows:**
```bash
scripts\iniciar_app.bat
```

**Linux/Mac:**
```bash
chmod +x scripts/iniciar_app.sh
./scripts/iniciar_app.sh
```

---

## 📋 Uso del Sistema

### 1. Crear un Proyecto

1. Abre `http://localhost:5000/new_project`
2. Ingresa:
   - **Nombre del proyecto**
   - **Historia de Usuario** (texto completo con criterios de aceptación)
   - **ID de Linear** (opcional, ej: FIN-1264)
3. Click en "Crear Proyecto"

### 2. Generar Casos de Prueba

1. En la página del proyecto, click en **"Generar Casos de Prueba"**
2. El sistema:
   - Extrae automáticamente los criterios de aceptación
   - **Descompone cada criterio** en múltiples casos específicos:
     - Caso feliz (happy path)
     - Estado vacío
     - Manejo de errores (500, 404, recursos no disponibles)
     - Usabilidad (tooltips, botones, modales)
     - Validaciones negativas
     - Persistencia de datos
     - Y más casos según el tipo de criterio
3. Genera casos profesionales con formato Gherkin estructurado

### 3. Subir a Linear

1. Click en **"Subir Directo a Linear"**
2. Ingresa tu **API Key de Linear** (solo la primera vez, se guarda en el navegador)
3. Los casos se suben como sub-issues de la HU
4. Se asocian automáticamente al equipo correcto (FIN, TEC, etc.)
5. Estado inicial: **"Todo"** (listo para trabajar)

---

## 🔑 Obtener API Key de Linear

1. Ve a **Linear → Settings → API**
2. Copia tu API Key (empieza con `lin_api_`)
3. Pégala en el sistema (se guarda automáticamente en tu navegador)

---

## 📁 Estructura del Proyecto

```
test_automation_tool/
├── main.py                          # Punto de entrada del servidor
├── app.py                           # Aplicación Flask principal
├── requirements.txt                 # Dependencias Python
├── README.md                        # Este archivo
├── .gitignore                       # Archivos a ignorar en Git
│
├── src/                             # Código fuente principal
│   ├── professional_qa_generator.py # Generador inteligente mejorado
│   ├── linear_api_client.py         # Cliente API de Linear
│   ├── test_case_automation.py      # Lógica core del sistema
│   └── ...
│
├── templates/                       # Plantillas HTML
│   ├── index.html                   # Página principal
│   ├── new_project.html             # Crear proyectos
│   └── project_detail.html          # Ver y gestionar casos
│
├── static/                          # Archivos estáticos
│   ├── css/                         # Estilos CSS
│   ├── js/                          # JavaScript
│   └── images/                      # Imágenes
│
├── exporters/                       # Exportadores
│   └── linear_simple_exporter.py   # Exportador CSV
│
├── generators/                      # Generadores adicionales
│   └── ...
│
├── scripts/                         # Scripts de utilidad
│   ├── iniciar_app.bat             # Inicio Windows
│   └── iniciar_app.sh              # Inicio Linux/Mac
│
└── data/                            # Datos (local, no se sube a Git)
    └── qa_projects.json             # Tus proyectos (local)
```

---

## 🧩 Características Técnicas

### Generación Inteligente de Casos

El sistema **NO copia literalmente** los criterios. En su lugar:

- **Analiza cada criterio** para entender su tipo (visualización, interacción, validación, etc.)
- **Descompone en múltiples casos específicos**:
  - Happy path (caso feliz)
  - Estados vacíos
  - Manejo de errores
  - Usabilidad
  - Validaciones negativas
  - Persistencia
  - Y más según el contexto

- **Genera 10+ casos por criterio** (en lugar de 1 genérico)
- **Formato estructurado**: TC-XXX, Objetivo, Criterio, Precondiciones, Pasos, Resultado Esperado

### Parser Robusto

- Extrae criterios incluso sin emojis o formato especial
- Entiende diferentes formatos: bullets, numeración, Gherkin, texto libre
- Análisis contextual inteligente

### Integración con Linear

- Detección automática de equipo: FIN-1264 → Equipo Finanzas
- Estado inicial configurable: Se suben en estado "Todo"
- Sub-issues automáticas: Los casos se vinculan a la HU padre
- Sin duplicar IDs: Linear genera sus propios identificadores

---

## 💾 Datos Locales

Todo se guarda **localmente en tu PC**:

- **Proyectos**: `qa_projects.json` (en la raíz del proyecto)
- **API Key**: `localStorage` del navegador (solo tu navegador)
- **Cada usuario**: Datos completamente independientes

**No hay base de datos compartida** - Cada uno trabaja con su propia copia.

**Nota**: El archivo `qa_projects.json` está en `.gitignore`, así que NO se sube a Git.

---

## 🛠️ Personalización

### Cambiar el Puerto

Edita `main.py`:

```python
app.run(debug=True, host='0.0.0.0', port=5000)  # Cambia 5000 por otro puerto
```

### Ajustar Estados de Linear

Edita `src/linear_api_client.py`, método `_get_todo_state_id()`:

```python
if state.get('name', '').lower() in ['todo', 'to do', 'backlog']:  # Agrega más estados
```

---

## 🐛 Solución de Problemas

### "ModuleNotFoundError: No module named 'flask'"

```bash
pip install -r requirements.txt
```

### "Port 5000 already in use"

**Windows:**
```bash
netstat -ano | findstr :5000
taskkill /PID <numero_pid> /F
```

**Linux/Mac:**
```bash
lsof -ti:5000 | xargs kill -9
```

O cambia el puerto en `main.py`.

### Los casos no se generan bien

- Asegúrate de que la HU tenga una sección **"Criterios de aceptación"**
- El parser es flexible y acepta diferentes formatos
- Si el formato es muy libre, el parser intentará extraer oraciones relevantes

### Error al subir a Linear

- Verifica que tu **API Key sea correcta**
- El **ID de HU debe existir** en Linear (ej: FIN-1264)
- Asegúrate de tener **permisos de escritura** en el equipo

---

## 🔄 Actualizar desde Git

```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

**Nota**: Tus proyectos locales (`qa_projects.json`) NO se sobrescriben.

---

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama: `git checkout -b feature/nueva-funcionalidad`
3. Commit: `git commit -m 'Agregar nueva funcionalidad'`
4. Push: `git push origin feature/nueva-funcionalidad`
5. Abre un Pull Request

---

## 📝 Licencia

Este proyecto es de uso interno. Si decides compartirlo públicamente, agrega una licencia apropiada (MIT, Apache, etc.).

---

## 💬 Soporte

Si encuentras problemas:

1. Revisa la sección **"Solución de problemas"** arriba
2. Verifica los logs en la terminal donde ejecutaste `python main.py`
3. Abre un issue en GitHub con:
   - Descripción del problema
   - Mensaje de error completo
   - Pasos para reproducir

---

## 🎉 ¡Listo para Usar!

Tu sistema está configurado para que **cada desarrollador lo clone y use independientemente**.

No necesitas configurar bases de datos ni servidores compartidos. Simplemente:

```bash
git clone <repo>
cd test_automation_tool
pip install -r requirements.txt
python main.py
```

**¡A generar casos de prueba profesionales! 🚀**
