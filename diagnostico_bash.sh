#!/bin/bash
# Diagnóstico completo del proyecto con Bash

echo "🔍 DIAGNÓSTICO COMPLETO DEL PROYECTO"
echo "======================================"
echo ""

# Información del sistema
echo "📊 INFORMACIÓN DEL SISTEMA:"
echo "OS: $(uname -a)"
echo "Python: $(python --version 2>&1)"
echo "Pip: $(pip --version 2>&1)"
echo ""

# Directorio actual
echo "📁 INFORMACIÓN DEL PROYECTO:"
echo "Directorio actual: $(pwd)"
echo "Archivos Python: $(find . -name "*.py" | wc -l)"
echo ""

# Verificar estructura de carpetas
echo "📂 ESTRUCTURA DE CARPETAS:"
echo "src/: $(ls -la src/ 2>/dev/null | wc -l) archivos"
echo "generators/: $(ls -la generators/ 2>/dev/null | wc -l) archivos"
echo "exporters/: $(ls -la exporters/ 2>/dev/null | wc -l) archivos"
echo "templates/: $(ls -la templates/ 2>/dev/null | wc -l) archivos"
echo ""

# Verificar dependencias
echo "📦 DEPENDENCIAS:"
python -c "
import sys
print('Python path:')
for p in sys.path:
    print('  -', p)
print()

# Verificar Flask
try:
    import flask
    print('✅ Flask:', flask.__version__)
except ImportError as e:
    print('❌ Flask no encontrado:', e)

# Verificar pandas
try:
    import pandas
    print('✅ Pandas:', pandas.__version__)
except ImportError as e:
    print('❌ Pandas no encontrado:', e)

# Verificar otros módulos
modules = ['json', 'os', 'datetime']
for module in modules:
    try:
        __import__(module)
        print('✅', module.capitalize())
    except ImportError as e:
        print('❌', module.capitalize(), 'no encontrado:', e)
"

echo ""
echo "🔧 VERIFICANDO IMPORTACIONES DEL PROYECTO:"

# Verificar módulos del proyecto
python -c "
import sys
import os

# Agregar directorios al path
current_dir = os.path.dirname(os.path.abspath('.'))
sys.path.insert(0, os.path.join(current_dir, 'src'))
sys.path.insert(0, os.path.join(current_dir, 'exporters'))
sys.path.insert(0, os.path.join(current_dir, 'generators'))

print('Path actualizado:')
for p in sys.path[:5]:
    print('  -', p)
print()

# Verificar módulos del proyecto
project_modules = [
    'test_case_automation',
    'test_templates', 
    'linear_simple_exporter',
    'gherkin_generator',
    'enhanced_gherkin_generator'
]

for module in project_modules:
    try:
        __import__(module)
        print('✅', module)
    except ImportError as e:
        print('❌', module, ':', e)
"

echo ""
echo "🧪 PROBANDO APLICACIÓN FLASK:"
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
    template_path = os.path.join(current_dir, 'templates', 'index.html')
    if os.path.exists(template_path):
        print('✅ Plantilla index.html encontrada')
    else:
        print('❌ Plantilla index.html NO encontrada')
        
except Exception as e:
    print('❌ Error al importar app:', e)
    import traceback
    traceback.print_exc()
"

echo ""
echo "🔍 BUSCANDO ERRORES ESPECÍFICOS:"
echo "Buscando errores de importación..."
grep -r "ImportError\|ModuleNotFoundError" . --include="*.py" 2>/dev/null || echo "No se encontraron errores de importación en archivos"

echo ""
echo "Buscando archivos con problemas de importación..."
find . -name "*.py" -exec grep -l "import.*could not be resolved" {} \; 2>/dev/null || echo "No se encontraron archivos con problemas de importación"

echo ""
echo "======================================"
echo "🔍 DIAGNÓSTICO COMPLETADO"
echo "======================================"
