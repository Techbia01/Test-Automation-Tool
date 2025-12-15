#!/bin/bash
# Script para verificar y corregir todos los errores del proyecto

echo "🔍 VERIFICANDO Y CORRIGIENDO ERRORES DEL PROYECTO"
echo "=================================================="
echo ""

# Función para verificar si un comando existe
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Verificar herramientas necesarias
echo "🔧 Verificando herramientas necesarias..."
if command_exists python; then
    echo "✅ Python encontrado: $(python --version)"
else
    echo "❌ Python no encontrado"
    exit 1
fi

if command_exists pip; then
    echo "✅ pip encontrado: $(pip --version)"
else
    echo "❌ pip no encontrado"
    exit 1
fi

echo ""

# Verificar estructura del proyecto
echo "📂 Verificando estructura del proyecto..."
required_dirs=("src" "generators" "exporters" "templates" "tests")
for dir in "${required_dirs[@]}"; do
    if [ -d "$dir" ]; then
        echo "✅ $dir/ existe"
    else
        echo "❌ $dir/ no existe"
    fi
done

echo ""

# Verificar archivos principales
echo "📄 Verificando archivos principales..."
required_files=("app.py" "main.py" "requirements.txt")
for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file existe"
    else
        echo "❌ $file no existe"
    fi
done

echo ""

# Verificar dependencias Python
echo "📦 Verificando dependencias Python..."
python -c "
import sys
import os

# Agregar directorios al path
current_dir = os.path.dirname(os.path.abspath('.'))
sys.path.insert(0, current_dir)
sys.path.insert(0, os.path.join(current_dir, 'src'))
sys.path.insert(0, os.path.join(current_dir, 'exporters'))
sys.path.insert(0, os.path.join(current_dir, 'generators'))

print('Python version:', sys.version)
print('Python path:')
for p in sys.path[:5]:
    print('  -', p)
print()

# Verificar dependencias externas
external_deps = ['flask', 'pandas', 'openpyxl', 'colorama', 'rich', 'requests']
for dep in external_deps:
    try:
        module = __import__(dep)
        version = getattr(module, '__version__', 'Unknown')
        print('✅', dep, ':', version)
    except ImportError:
        print('❌', dep, 'no encontrado')

print()

# Verificar módulos del proyecto
project_modules = [
    'test_case_automation',
    'test_templates', 
    'linear_simple_exporter',
    'gherkin_generator',
    'enhanced_gherkin_generator'
]

print('Módulos del proyecto:')
for module in project_modules:
    try:
        __import__(module)
        print('✅', module)
    except ImportError as e:
        print('❌', module, ':', str(e))
"

echo ""

# Verificar aplicación Flask
echo "🌐 Verificando aplicación Flask..."
python -c "
import sys
import os

# Configurar path
current_dir = os.path.dirname(os.path.abspath('.'))
sys.path.insert(0, current_dir)
sys.path.insert(0, os.path.join(current_dir, 'src'))
sys.path.insert(0, os.path.join(current_dir, 'exporters'))
sys.path.insert(0, os.path.join(current_dir, 'generators'))

try:
    from app import app
    print('✅ App importada correctamente')
    print('✅ Template folder:', app.template_folder)
    print('✅ Static folder:', app.static_folder)
    
    # Verificar plantillas
    template_files = ['index.html', 'base.html', 'new_project.html', 'project_detail.html']
    for template in template_files:
        template_path = os.path.join(current_dir, 'templates', template)
        if os.path.exists(template_path):
            print('✅ Plantilla', template, 'encontrada')
        else:
            print('❌ Plantilla', template, 'NO encontrada')
            
    # Probar renderizado de plantilla
    try:
        with app.app_context():
            from flask import render_template
            projects = []
            template = render_template('index.html', projects=projects)
            print('✅ Plantilla index.html renderizada correctamente')
    except Exception as e:
        print('❌ Error al renderizar plantilla:', str(e))
        
except Exception as e:
    print('❌ Error al importar app:', str(e))
    import traceback
    traceback.print_exc()
"

echo ""

# Verificar errores específicos
echo "🔍 Buscando errores específicos..."
echo "Buscando errores de importación en archivos Python..."
find . -name "*.py" -exec grep -l "ImportError\|ModuleNotFoundError" {} \; 2>/dev/null | while read file; do
    echo "⚠️  Archivo con errores de importación: $file"
done

echo ""

# Resumen final
echo "📊 RESUMEN DE VERIFICACIÓN:"
echo "============================"

# Contar archivos Python
python_files=$(find . -name "*.py" | wc -l)
echo "📄 Archivos Python: $python_files"

# Contar errores de importación
import_errors=$(find . -name "*.py" -exec grep -l "ImportError\|ModuleNotFoundError" {} \; 2>/dev/null | wc -l)
echo "❌ Archivos con errores de importación: $import_errors"

# Verificar si el servidor puede iniciar
echo ""
echo "🚀 Probando inicio del servidor..."
timeout 5 python main.py > /dev/null 2>&1 &
server_pid=$!
sleep 2
if kill -0 $server_pid 2>/dev/null; then
    echo "✅ Servidor puede iniciar correctamente"
    kill $server_pid 2>/dev/null
else
    echo "❌ Servidor no puede iniciar"
fi

echo ""
echo "🎉 VERIFICACIÓN COMPLETADA"
echo "Para iniciar el servidor, ejecuta: ./start_app.sh"
