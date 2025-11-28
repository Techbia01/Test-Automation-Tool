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

## ⚡ Instalación Rápida (Si ya tienes Python y Git)

Si ya tienes Python 3.8+ y Git instalados, ejecuta estos 3 comandos:

```bash
git clone https://github.com/Techbia01/Test-Automation-Tool.git
cd Test-Automation-Tool
pip install -r requirements.txt
python main.py
```

Luego abre: http://localhost:5000

**¿No tienes Python o Git?** → Sigue la guía completa abajo 👇

---

## 🚀 Instalación Completa (Paso a Paso)

### ⚠️ IMPORTANTE: Verifica Requisitos Antes de Continuar

**Antes de clonar el repositorio, asegúrate de tener instalado:**

1. **Python 3.8 o superior**
2. **pip** (viene con Python)
3. **Git** (para clonar el repositorio)
4. Navegador web moderno (Chrome, Firefox, Edge)

---

### 📋 Paso 1: Verificar que Python está Instalado

Abre una terminal (PowerShell en Windows, Terminal en Mac/Linux) y ejecuta:

```bash
python --version
```

**O si no funciona, prueba:**
```bash
python3 --version
```

**✅ Debe mostrar algo como:** `Python 3.8.0` o superior

**❌ Si dice "no se reconoce como comando":**
- **Windows:** Descarga Python desde https://www.python.org/downloads/
  - ⚠️ **IMPORTANTE:** Durante la instalación, marca la casilla **"Add Python to PATH"**
- **Mac:** `brew install python3` o descarga desde python.org
- **Linux:** `sudo apt install python3 python3-pip` (Ubuntu/Debian)

---

### 📋 Paso 2: Verificar que pip está Instalado

```bash
pip --version
```

**O si no funciona:**
```bash
pip3 --version
```

**✅ Debe mostrar algo como:** `pip 21.0.0` o superior

**❌ Si dice "no se reconoce como comando":**
```bash
# Windows
python -m ensurepip --upgrade

# Mac/Linux
python3 -m ensurepip --upgrade
```

---

### 📋 Paso 3: Verificar que Git está Instalado

```bash
git --version
```

**✅ Debe mostrar algo como:** `git version 2.30.0` o superior

**❌ Si dice "no se reconoce como comando":**
- **Windows:** Descarga desde https://git-scm.com/downloads
- **Mac:** `brew install git` o descarga desde git-scm.com
- **Linux:** `sudo apt install git` (Ubuntu/Debian)

---

### 📋 Paso 4: Clonar el Repositorio

```bash
git clone https://github.com/Techbia01/Test-Automation-Tool.git
cd Test-Automation-Tool
```

**✅ Verifica que estás en la carpeta correcta:**
```bash
# Debe mostrar archivos como: main.py, requirements.txt, README.md
dir    # Windows
ls     # Mac/Linux
```

---

### 📋 Paso 5: Instalar Dependencias Python

**⚠️ IMPORTANTE:** Este paso instala Flask y todas las dependencias necesarias.

```bash
pip install -r requirements.txt
```

**O si `pip` no funciona:**
```bash
python -m pip install -r requirements.txt
```

**O en Mac/Linux:**
```bash
pip3 install -r requirements.txt
python3 -m pip install -r requirements.txt
```

**✅ Verifica que Flask se instaló correctamente:**
```bash
python -c "import flask; print(flask.__version__)"
```

**Debe mostrar:** `2.0.0` o superior (sin errores)

---

### 📋 Paso 6: Verificar Instalación Completa

Ejecuta este comando para verificar que todo está listo:

```bash
python -c "import flask, pandas, openpyxl, requests; print('✅ Todas las dependencias están instaladas')"
```

**✅ Si muestra el mensaje de éxito:** Todo está listo para continuar

**❌ Si muestra errores:** Revisa la sección "Solución de Problemas" más abajo

---

### 📋 Paso 7: Iniciar el Servidor

```bash
python main.py
```

**O si no funciona:**
```bash
python3 main.py
```

**✅ Debe mostrar algo como:**
```
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

---

### 📋 Paso 8: Abrir en el Navegador

Abre tu navegador y ve a:
```
http://localhost:5000
```

**✅ Debe mostrar la página principal del sistema**

---

### ✅ Checklist de Verificación Final

Antes de empezar a usar el sistema, verifica que todo esté correcto:

- [ ] ✅ Python está instalado: `python --version` muestra 3.8 o superior
- [ ] ✅ pip está instalado: `pip --version` funciona sin errores
- [ ] ✅ Git está instalado: `git --version` funciona sin errores
- [ ] ✅ Repositorio clonado: Estás en la carpeta `Test-Automation-Tool`
- [ ] ✅ Dependencias instaladas: `python -c "import flask"` no da error
- [ ] ✅ Servidor inicia: `python main.py` muestra "Running on http://127.0.0.1:5000"
- [ ] ✅ Página carga: http://localhost:5000 muestra la interfaz del sistema

**Si todos los checks están ✅, ¡estás listo para usar el sistema!**

---

### 🎯 Scripts de Inicio Automático (Recomendado)

Los scripts verifican todo automáticamente y te guían si falta algo:

**Windows:**
```bash
scripts\iniciar_app.bat
```

**Mac/Linux:**
```bash
chmod +x scripts/iniciar_app.sh
./scripts/iniciar_app.sh
```

**PowerShell (Windows):**
```bash
.\scripts\iniciar_app.ps1
```

Estos scripts:
- ✅ Verifican que Python esté instalado
- ✅ Instalan dependencias automáticamente
- ✅ Inician el servidor
- ✅ Te muestran la URL para abrir en el navegador

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

## 🐛 Solución de Problemas Comunes

### ❌ Error: "Python no se reconoce como comando interno o externo"

**Problema:** Python no está instalado o no está en el PATH.

**Solución Windows:**
1. Descarga Python desde https://www.python.org/downloads/
2. Durante la instalación, **marca la casilla "Add Python to PATH"** (MUY IMPORTANTE)
3. Reinicia la terminal después de instalar
4. Verifica: `python --version`

**Solución Mac:**
```bash
brew install python3
```

**Solución Linux:**
```bash
sudo apt update
sudo apt install python3 python3-pip
```

---

### ❌ Error: "ModuleNotFoundError: No module named 'flask'"

**Problema:** Flask no está instalado o las dependencias no se instalaron correctamente.

**Solución:**
```bash
# Primero, asegúrate de estar en la carpeta del proyecto
cd Test-Automation-Tool

# Instala todas las dependencias
pip install -r requirements.txt

# Si no funciona, prueba:
python -m pip install -r requirements.txt

# O en Mac/Linux:
pip3 install -r requirements.txt
python3 -m pip install -r requirements.txt
```

**Verifica que se instaló:**
```bash
python -c "import flask; print('✅ Flask instalado:', flask.__version__)"
```

---

### ❌ Error: "pip no se reconoce como comando interno o externo"

**Problema:** pip no está instalado o no está en el PATH.

**Solución:**
```bash
# Windows
python -m ensurepip --upgrade

# Mac/Linux
python3 -m ensurepip --upgrade
```

**O instala pip manualmente:**
```bash
# Descarga get-pip.py desde https://bootstrap.pypa.io/get-pip.py
python get-pip.py
```

---

### ❌ Error: "git no se reconoce como comando interno o externo"

**Problema:** Git no está instalado.

**Solución:**
- **Windows:** Descarga desde https://git-scm.com/downloads
- **Mac:** `brew install git`
- **Linux:** `sudo apt install git`

---

### ❌ Error: "Port 5000 already in use"

**Problema:** Otro programa está usando el puerto 5000.

**Solución Windows:**
```bash
# Encuentra qué programa usa el puerto
netstat -ano | findstr :5000

# Mata el proceso (reemplaza <PID> con el número que apareció)
taskkill /PID <PID> /F
```

**Solución Mac/Linux:**
```bash
# Encuentra y mata el proceso
lsof -ti:5000 | xargs kill -9
```

**O cambia el puerto en `main.py`:**
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Cambia 5000 por 5001
```

---

### ❌ Error: "Permission denied" al instalar paquetes

**Problema:** No tienes permisos para instalar paquetes globalmente.

**Solución (Recomendado - Usa entorno virtual):**
```bash
# Crea un entorno virtual
python -m venv venv

# Actívalo
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Instala dependencias
pip install -r requirements.txt

# Ejecuta la app
python main.py
```

**Solución Alternativa (Instalar para el usuario):**
```bash
pip install --user -r requirements.txt
```

---

### ❌ Error: "No se puede clonar el repositorio"

**Problema:** Git no está instalado o la URL es incorrecta.

**Solución:**
1. Verifica que Git esté instalado: `git --version`
2. Usa la URL correcta: `https://github.com/Techbia01/Test-Automation-Tool.git`
3. Si es privado, asegúrate de estar autenticado en GitHub

---

### ❌ Los casos no se generan bien

**Problema:** La Historia de Usuario no tiene formato claro.

**Solución:**
- Asegúrate de que la HU tenga una sección **"Criterios de aceptación"**
- El parser es flexible y acepta diferentes formatos:
  - ✅ Listas con bullets (`-`, `*`, `•`)
  - ✅ Numeración (`1.`, `2.`, etc.)
  - ✅ Emojis (`✅`, `☑️`, `✓`)
  - ✅ Formato Gherkin (Given/When/Then)
  - ✅ Texto libre con palabras clave ("debe", "se debe", "el sistema")
- Si el formato es muy libre, el parser intentará extraer oraciones relevantes
- Revisa `docs/EJEMPLO_HISTORIA_USUARIO.md` para ver ejemplos

---

### ❌ Error al subir a Linear

**Problema:** Problemas con la API de Linear.

**Solución:**
1. Verifica que tu **API Key sea correcta** (debe empezar con `lin_api_`)
2. El **ID de HU debe existir** en Linear (ej: FIN-1264)
3. Asegúrate de tener **permisos de escritura** en el equipo
4. Verifica tu conexión a internet
5. Revisa los logs en la terminal para ver el error específico

---

### ❌ Error: "No module named 'pandas'" o similar

**Problema:** Alguna dependencia no se instaló correctamente.

**Solución:**
```bash
# Reinstala todas las dependencias
pip install --upgrade -r requirements.txt

# O instala manualmente la que falta
pip install pandas openpyxl flask requests colorama rich
```

---

### ❌ El servidor no inicia o muestra errores

**Solución paso a paso:**
1. Verifica que estás en la carpeta correcta: `dir` (Windows) o `ls` (Mac/Linux)
2. Verifica que `main.py` existe: `dir main.py` o `ls main.py`
3. Verifica que Python funciona: `python --version`
4. Verifica que Flask está instalado: `python -c "import flask"`
5. Lee los mensajes de error en la terminal - suelen indicar qué falta

---

### 💡 ¿Aún tienes problemas?

1. **Verifica que seguiste todos los pasos** de la sección "Instalación Completa"
2. **Revisa los logs** en la terminal donde ejecutaste `python main.py`
3. **Abre un issue en GitHub** con:
   - Descripción del problema
   - Mensaje de error completo (copia y pega)
   - Sistema operativo (Windows/Mac/Linux)
   - Versión de Python: `python --version`
   - Pasos que seguiste antes del error

---

## 🔄 Actualizar desde Git

Cuando haya nuevas versiones del proyecto:

```bash
# 1. Asegúrate de estar en la carpeta del proyecto
cd Test-Automation-Tool

# 2. Descarga los cambios
git pull origin main

# 3. Actualiza las dependencias (por si hay nuevas)
pip install -r requirements.txt --upgrade

# 4. Verifica que todo sigue funcionando
python -c "import flask; print('✅ Todo actualizado correctamente')"

# 5. Reinicia el servidor
python main.py
```

**⚠️ IMPORTANTE:**
- Tus proyectos locales (`qa_projects.json`) **NO se sobrescriben**
- Si hay conflictos, Git te avisará
- Siempre verifica que el servidor inicia correctamente después de actualizar

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
