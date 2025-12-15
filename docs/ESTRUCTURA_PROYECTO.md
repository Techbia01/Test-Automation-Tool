# 📁 Estructura del Proyecto

## Organización Actual

```
test_automation_tool/
│
├── 📄 Archivos Principales (Raíz)
│   ├── README.md                    # Documentación principal
│   ├── main.py                      # Punto de entrada de la aplicación
│   ├── app.py                       # Aplicación Flask principal
│   ├── finanzas_app.py              # Aplicación Flask para módulo de finanzas
│   ├── requirements.txt             # Dependencias de Python
│   ├── package.json                 # Configuración de Node.js (si aplica)
│   ├── pyrightconfig.json           # Configuración de Pyright
│   ├── tsconfig.json                # Configuración de TypeScript
│   └── qa_projects.json             # Base de datos de proyectos (JSON)
│
├── 📚 docs/                         # Documentación completa
│   ├── README.md                    # Documentación interna
│   ├── INSTALACION.md               # Guía de instalación
│   ├── GUIA_*.md                    # Varias guías de uso
│   ├── MEJORAS_*.md                 # Documentación de mejoras
│   ├── SOLUCION_*.md                # Documentación de soluciones
│   └── [otros archivos .md]
│
├── 🧪 tests/                        # Casos de prueba
│   ├── test_*.py                    # Todos los archivos de prueba
│   └── [tests unitarios e integración]
│
├── 🔧 scripts/                      # Scripts y utilidades
│   ├── *.sh                         # Scripts de shell (Linux/Mac)
│   ├── *.bat                        # Scripts de Windows
│   ├── *.ps1                        # Scripts de PowerShell
│   ├── diagnostico*.py              # Scripts de diagnóstico
│   ├── verificar*.py                # Scripts de verificación
│   └── [otros scripts de utilidad]
│
├── 💾 data/                         # Datos y archivos de ejemplo
│   ├── casos_login.*                # Datos de ejemplo
│   ├── demo_*.py                    # Demos y ejemplos
│   ├── ejemplo_*.txt                # Archivos de ejemplo
│   └── qa_projects.json             # Backup de proyectos
│
├── 📤 output/                       # Archivos generados
│   └── *.csv                        # Archivos CSV exportados
│
├── 💻 src/                          # Código fuente principal
│   ├── app.py                       # Versión alternativa de app (legacy?)
│   ├── professional_qa_generator.py # Generador principal de casos
│   ├── test_case_automation.py      # Automatización de casos
│   ├── linear_api_client.py         # Cliente de API de Linear
│   └── [otros módulos del sistema]
│
├── 🎨 static/                       # Archivos estáticos
│   ├── css/                         # Hojas de estilo
│   ├── js/                          # Scripts JavaScript
│   └── images/                      # Imágenes
│
├── 📄 templates/                    # Plantillas HTML
│   ├── base.html                    # Plantilla base
│   ├── index.html                   # Página principal
│   ├── new_project.html             # Crear proyecto
│   ├── project_detail.html          # Detalle de proyecto
│   └── finanzas/                    # Templates del módulo finanzas
│
├── ⚙️ generators/                   # Generadores de casos
│   ├── gherkin_generator.py         # Generador Gherkin
│   ├── enhanced_gherkin_generator.py # Generador mejorado
│   └── [otros generadores]
│
├── 📊 exporters/                    # Exportadores
│   ├── linear_simple_exporter.py    # Exportador a Linear
│   ├── linear_integration.py        # Integración con Linear
│   └── [otros exportadores]
│
├── ⚙️ config/                       # Configuración
│   ├── paths.py                     # Rutas del sistema
│   └── setup.py                     # Configuración inicial
│
└── 📁 uploads/                      # Archivos subidos por usuarios
```

## Archivos Importantes

### Punto de Entrada
- **`main.py`**: Ejecuta la aplicación Flask principal
- **`app.py`**: Contiene la aplicación Flask (importada por main.py)

### Configuración
- **`requirements.txt`**: Dependencias de Python
- **`qa_projects.json`**: Base de datos de proyectos (JSON local)

### Scripts Principales
- **`scripts/start_app.sh`**: Iniciar aplicación (Linux/Mac)
- **`scripts/start_app.bat`**: Iniciar aplicación (Windows)
- **`scripts/iniciar_finanzas.sh`**: Iniciar módulo finanzas

## Convenciones

### Nombres de Archivos
- **Tests**: `test_*.py` → `tests/`
- **Scripts**: `*.sh`, `*.bat`, `*.ps1` → `scripts/`
- **Documentación**: `*.md` (excepto README.md) → `docs/`
- **Datos**: Archivos de ejemplo y datos → `data/`

### Estructura de Carpetas
- **Raíz**: Solo archivos esenciales y punto de entrada
- **docs/**: Toda la documentación
- **tests/**: Todos los casos de prueba
- **scripts/**: Todos los scripts y utilidades
- **src/**: Código fuente principal del sistema
- **data/**: Archivos de datos y ejemplos

## Notas

- El archivo `app.py` en `src/` parece ser una versión legacy o alternativa
- El `app.py` en la raíz es el que se usa actualmente (importado por `main.py`)
- `finanzas_app.py` se mantiene en la raíz porque se ejecuta directamente
- Los archivos de configuración JSON se mantienen en la raíz para fácil acceso

