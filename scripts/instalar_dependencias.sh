#!/bin/bash
# Script para instalar todas las dependencias del proyecto

echo "📦 INSTALANDO DEPENDENCIAS DEL PROYECTO"
echo "======================================="
echo ""

# Verificar si pip está disponible
if ! command -v pip &> /dev/null; then
    echo "❌ pip no encontrado. Instalando pip..."
    python -m ensurepip --upgrade
fi

echo "🔧 Instalando dependencias principales..."

# Instalar Flask
echo "Instalando Flask..."
pip install flask

# Instalar pandas
echo "Instalando pandas..."
pip install pandas

# Instalar openpyxl
echo "Instalando openpyxl..."
pip install openpyxl

# Instalar otras dependencias
echo "Instalando dependencias adicionales..."
pip install colorama rich requests python-docx

echo ""
echo "📋 Verificando instalación..."

python -c "
import sys
print('Python version:', sys.version)
print()

# Verificar todas las dependencias
dependencies = [
    'flask',
    'pandas', 
    'openpyxl',
    'colorama',
    'rich',
    'requests',
    'docx'
]

for dep in dependencies:
    try:
        module = __import__(dep)
        version = getattr(module, '__version__', 'Unknown')
        print('✅', dep, ':', version)
    except ImportError:
        print('❌', dep, 'no encontrado')
"

echo ""
echo "🔧 Configurando entorno Python..."

# Crear archivo de configuración para el IDE
cat > .python-version << EOF
# Configuración de Python para el proyecto
PYTHONPATH=.:src:exporters:generators
EOF

echo "✅ Archivo .python-version creado"

# Crear archivo de configuración para pyright
cat > pyrightconfig.json << EOF
{
    "include": [
        "."
    ],
    "exclude": [
        "**/__pycache__",
        "**/node_modules"
    ],
    "pythonPath": "python",
    "pythonVersion": "3.8",
    "extraPaths": [
        "src",
        "exporters", 
        "generators"
    ],
    "typeCheckingMode": "basic"
}
EOF

echo "✅ Archivo pyrightconfig.json creado"

echo ""
echo "🎉 INSTALACIÓN COMPLETADA"
echo "Ahora puedes ejecutar: ./start_app.sh"
