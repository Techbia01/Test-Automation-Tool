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

Si ya tienes Python 3.8+ y Git instalados, ejecuta estos comandos:

**Windows (PowerShell o CMD):**
```bash
git clone https://github.com/Techbia01/Test-Automation-Tool.git
cd Test-Automation-Tool
python -m pip install -r requirements.txt
python main.py
```

**Mac/Linux:**
```bash
git clone https://github.com/Techbia01/Test-Automation-Tool.git
cd Test-Automation-Tool
pip3 install -r requirements.txt
python3 main.py
```

Luego abre en tu navegador: **http://localhost:5000**

**¿No tienes Python o Git?** → Sigue la guía completa abajo 👇

---

## 🚀 Instalación Completa (Paso a Paso)

### ⚠️ IMPORTANTE: Requisitos del Sistema

**Antes de comenzar, necesitas:**

1. **Python 3.8 o superior** (recomendado: Python 3.10+)
2. **pip** (viene con Python, pero a veces hay que instalarlo)
3. **Git** (para clonar el repositorio)
4. **Navegador web moderno** (Chrome, Firefox, Edge, Safari)
5. **Conexión a Internet** (para clonar y descargar dependencias)

**Tiempo estimado de instalación:** 10-15 minutos

---

### 📋 Paso 1: Verificar que Python está Instalado

**Windows (PowerShell o CMD):**
```bash
python --version
```

**Mac/Linux:**
```bash
python3 --version
```

**✅ Debe mostrar:** `Python 3.8.0` o superior (ej: `Python 3.10.5`)

**❌ Si dice "no se reconoce como comando" o "command not found":**

**Windows:**
1. Descarga Python desde: https://www.python.org/downloads/
2. ⚠️ **MUY IMPORTANTE:** Durante la instalación, marca la casilla **"Add Python to PATH"**
3. Selecciona "Install Now" (incluye pip automáticamente)
4. **Cierra y vuelve a abrir** la terminal después de instalar
5. Verifica: `python --version`

**Mac:**
```bash
# Opción 1: Con Homebrew (recomendado)
brew install python3

# Opción 2: Descarga desde python.org
# Ve a https://www.python.org/downloads/macos/
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

**Linux (Fedora/RHEL):**
```bash
sudo dnf install python3 python3-pip
```

---

### 📋 Paso 2: Verificar que pip está Instalado

**Windows:**
```bash
python -m pip --version
```

**Mac/Linux:**
```bash
python3 -m pip --version
```

**✅ Debe mostrar:** `pip 21.0.0` o superior (ej: `pip 23.0.1`)

**❌ Si dice "no se reconoce como comando":**

**Windows:**
```bash
python -m ensurepip --upgrade
```

**Mac/Linux:**
```bash
python3 -m ensurepip --upgrade
```

**Si aún no funciona, instala pip manualmente:**
```bash
# Descarga get-pip.py
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py

# Ejecuta (Windows)
python get-pip.py

# Ejecuta (Mac/Linux)
python3 get-pip.py
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

**⚠️ IMPORTANTE:** Este paso instala Flask y todas las dependencias necesarias. Puede tardar 2-5 minutos.

**Windows:**
```bash
# Asegúrate de estar en la carpeta del proyecto
cd Test-Automation-Tool

# Instala dependencias
python -m pip install -r requirements.txt
```

**Mac/Linux:**
```bash
# Asegúrate de estar en la carpeta del proyecto
cd Test-Automation-Tool

# Instala dependencias
python3 -m pip install -r requirements.txt
```

**Si tienes problemas de permisos, usa entorno virtual (Recomendado):**
```bash
# Windows
python -m venv venv
venv\Scripts\activate
python -m pip install -r requirements.txt

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
```

**✅ Verifica que Flask se instaló correctamente:**
```bash
# Windows
python -c "import flask; print('✅ Flask instalado:', flask.__version__)"

# Mac/Linux
python3 -c "import flask; print('✅ Flask instalado:', flask.__version__)"
```

**Debe mostrar:** `✅ Flask instalado: 3.1.2` o superior (sin errores)

---

### 📋 Paso 6: Verificar Instalación Completa

Ejecuta este comando para verificar que todas las dependencias están instaladas:

**Windows:**
```bash
python -c "import flask, pandas, openpyxl, requests; print('✅ Todas las dependencias están instaladas')"
```

**Mac/Linux:**
```bash
python3 -c "import flask, pandas, openpyxl, requests; print('✅ Todas las dependencias están instaladas')"
```

**✅ Si muestra el mensaje de éxito:** Todo está listo para continuar

**❌ Si muestra errores como "ModuleNotFoundError":**
- Revisa que ejecutaste `pip install -r requirements.txt` correctamente
- Verifica que estás en la carpeta correcta del proyecto
- Revisa la sección "Solución de Problemas" más abajo

---

### 📋 Paso 7: Iniciar el Servidor

**Windows:**
```bash
python main.py
```

**Mac/Linux:**
```bash
python3 main.py
```

**✅ Debe mostrar algo como:**
```
Iniciando Sistema de Automatizacion de Casos de Prueba para QA
Accede a: http://localhost:5000
Crear proyecto: http://localhost:5000/new_project
============================================================
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

**⚠️ IMPORTANTE:** 
- **NO cierres la terminal** mientras uses el sistema (el servidor debe seguir corriendo)
- Para detener el servidor, presiona `CTRL+C` en la terminal
- Si ves errores de encoding en Windows, es normal - el sistema los maneja automáticamente

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

## 👥 Trabajo en Equipo

Si trabajas con otros desarrolladores, **lee primero** la guía completa:

📖 **[Guía de Trabajo en Equipo](docs/GUIA_TRABAJO_EQUIPO.md)** - Evita conflictos Git

### **Comandos rápidos:**

```bash
# Actualizar código antes de trabajar
git pull origin main

# Subir tus cambios
git add .
git commit -m "Descripción de tus cambios"
git push origin main

# O usa el script automático (Windows)
scripts\sincronizar_cambios.bat

# O en Mac/Linux
./scripts/sincronizar_cambios.sh
```

**Importante:** 
- ✅ Siempre haz `git pull` antes de empezar
- ✅ Cada uno tiene su propio `qa_projects.json` (no se sube a Git)
- ✅ Los archivos locales (`uploads/`, `outputs/`) no generan conflictos

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

### ❌ Error: "Port 5000 already in use" o "Address already in use"

**Problema:** Otro programa está usando el puerto 5000 (puede ser otra instancia del servidor).

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

**O cambia el puerto en `main.py` (línea 42):**
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Cambia 5000 por 5001
```

Luego accede a: `http://localhost:5001`

---

### ❌ Error: "Permission denied" o "Access denied" al instalar paquetes

**Problema:** No tienes permisos para instalar paquetes globalmente.

**Solución Recomendada - Usa Entorno Virtual (Más Seguro):**

**Windows:**
```bash
# Crea un entorno virtual
python -m venv venv

# Actívalo
venv\Scripts\activate

# Instala dependencias
python -m pip install -r requirements.txt

# Ejecuta la app
python main.py
```

**Mac/Linux:**
```bash
# Crea un entorno virtual
python3 -m venv venv

# Actívalo
source venv/bin/activate

# Instala dependencias
python3 -m pip install -r requirements.txt

# Ejecuta la app
python3 main.py
```

**Solución Alternativa - Instalar para el Usuario:**
```bash
# Windows
python -m pip install --user -r requirements.txt

# Mac/Linux
python3 -m pip install --user -r requirements.txt
```

**Nota:** Con `--user`, los paquetes se instalan solo para tu usuario, no globalmente.

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

**Solución Windows:**
```bash
# Reinstala todas las dependencias
python -m pip install --upgrade -r requirements.txt

# O instala manualmente la que falta
python -m pip install pandas openpyxl flask requests
```

**Solución Mac/Linux:**
```bash
# Reinstala todas las dependencias
python3 -m pip install --upgrade -r requirements.txt

# O instala manualmente la que falta
python3 -m pip install pandas openpyxl flask requests
```

**Si sigue fallando, verifica que estás en la carpeta correcta:**
```bash
# Debe mostrar main.py, requirements.txt, etc.
dir    # Windows
ls     # Mac/Linux
```

---

### ❌ El servidor no inicia o muestra errores

**Solución paso a paso:**

1. **Verifica que estás en la carpeta correcta:**
   ```bash
   # Windows
   dir
   # Debe mostrar: main.py, app.py, requirements.txt, etc.
   
   # Mac/Linux
   ls
   # Debe mostrar: main.py, app.py, requirements.txt, etc.
   ```

2. **Verifica que main.py existe:**
   ```bash
   # Windows
   dir main.py
   
   # Mac/Linux
   ls main.py
   ```

3. **Verifica que Python funciona:**
   ```bash
   # Windows
   python --version
   
   # Mac/Linux
   python3 --version
   ```

4. **Verifica que Flask está instalado:**
   ```bash
   # Windows
   python -c "import flask; print('OK')"
   
   # Mac/Linux
   python3 -c "import flask; print('OK')"
   ```

5. **Lee los mensajes de error en la terminal** - suelen indicar qué falta o qué está mal

6. **Si ves errores de encoding (charmap):** Es normal en Windows, el sistema los maneja automáticamente

7. **Si ves "Errno 22 Invalid argument":** Ya está solucionado en la versión actual, pero si aparece:
   - Verifica que tienes permisos de escritura en la carpeta
   - Asegúrate de que la ruta no tenga caracteres especiales
   - Revisa `docs/SOLUCION_ERROR_ERRNO22.md` para más detalles

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

**Windows:**
```bash
# 1. Asegúrate de estar en la carpeta del proyecto
cd Test-Automation-Tool

# 2. Descarga los cambios
git pull origin main

# 3. Actualiza las dependencias (por si hay nuevas)
python -m pip install -r requirements.txt --upgrade

# 4. Verifica que todo sigue funcionando
python -c "import flask; print('✅ Todo actualizado correctamente')"

# 5. Reinicia el servidor
python main.py
```

**Mac/Linux:**
```bash
# 1. Asegúrate de estar en la carpeta del proyecto
cd Test-Automation-Tool

# 2. Descarga los cambios
git pull origin main

# 3. Actualiza las dependencias (por si hay nuevas)
python3 -m pip install -r requirements.txt --upgrade

# 4. Verifica que todo sigue funcionando
python3 -c "import flask; print('✅ Todo actualizado correctamente')"

# 5. Reinicia el servidor
python3 main.py
```

**⚠️ IMPORTANTE:**
- Tus proyectos locales (`qa_projects.json`) **NO se sobrescriben**
- Si hay conflictos, Git te avisará
- Siempre verifica que el servidor inicia correctamente después de actualizar
- Si hay errores después de actualizar, revisa la sección "Solución de Problemas"

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

**Windows:**
```bash
git clone https://github.com/Techbia01/Test-Automation-Tool.git
cd Test-Automation-Tool
python -m pip install -r requirements.txt
python main.py
```

**Mac/Linux:**
```bash
git clone https://github.com/Techbia01/Test-Automation-Tool.git
cd Test-Automation-Tool
python3 -m pip install -r requirements.txt
python3 main.py
```

Luego abre: **http://localhost:5000**

**¡A generar casos de prueba profesionales! 🚀**

---

## 📚 Documentación Adicional

- **[Contexto Técnico](docs/CONTEXTO_TECNICO_PRESENTACION.md)** - Detalles técnicos del sistema
- **[Guía de Trabajo en Equipo](docs/GUIA_TRABAJO_EQUIPO.md)** - Cómo trabajar con otros desarrolladores
- **[Solución Error Errno 22](docs/SOLUCION_ERROR_ERRNO22.md)** - Solución a problemas de rutas en Windows
- **[Solución Error Charmap](docs/SOLUCION_ERROR_CHARMAP.md)** - Solución a problemas de encoding

---

**Última actualización:** 2024
**Versión:** 1.0
