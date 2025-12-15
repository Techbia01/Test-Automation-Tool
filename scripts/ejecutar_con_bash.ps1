# Script de PowerShell para ejecutar comandos Bash
# Este script ejecuta los comandos Bash en Git Bash

Write-Host "🚀 Ejecutando diagnóstico con Git Bash..." -ForegroundColor Green
Write-Host ""

# Verificar si Git Bash está disponible
$gitBashPath = "C:\Program Files\Git\bin\bash.exe"
if (Test-Path $gitBashPath) {
    Write-Host "✅ Git Bash encontrado en: $gitBashPath" -ForegroundColor Green
} else {
    $gitBashPath = "C:\Program Files (x86)\Git\bin\bash.exe"
    if (Test-Path $gitBashPath) {
        Write-Host "✅ Git Bash encontrado en: $gitBashPath" -ForegroundColor Green
    } else {
        Write-Host "❌ Git Bash no encontrado. Instalando Git..." -ForegroundColor Red
        Write-Host "Por favor, instala Git desde: https://git-scm.com/download/win"
        exit 1
    }
}

# Ejecutar diagnóstico con Git Bash
Write-Host "🔍 Ejecutando diagnóstico completo..." -ForegroundColor Yellow
& $gitBashPath -c "
cd '$(Get-Location)'
echo '🔍 DIAGNÓSTICO CON GIT BASH'
echo '=========================='
echo ''
echo '📊 INFORMACIÓN DEL SISTEMA:'
echo 'OS: $(uname -a)'
echo 'Python: $(python --version 2>&1)'
echo 'Pip: $(pip --version 2>&1)'
echo ''
echo '📁 ESTRUCTURA DEL PROYECTO:'
echo 'Directorio actual: $(pwd)'
echo 'Archivos Python: $(find . -name \"*.py\" | wc -l)'
echo ''
echo '📦 VERIFICANDO DEPENDENCIAS:'
python -c \"
import sys
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
\"
echo ''
echo '🔧 VERIFICANDO MÓDULOS DEL PROYECTO:'
python -c \"
import sys
import os

# Agregar directorios al path
current_dir = os.path.dirname(os.path.abspath('.'))
sys.path.insert(0, current_dir)
sys.path.insert(0, os.path.join(current_dir, 'src'))
sys.path.insert(0, os.path.join(current_dir, 'exporters'))
sys.path.insert(0, os.path.join(current_dir, 'generators'))

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
        print('❌', module, ':', str(e))
\"
echo ''
echo '🌐 VERIFICANDO APLICACIÓN FLASK:'
python -c \"
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
            
except Exception as e:
    print('❌ Error al importar app:', str(e))
    import traceback
    traceback.print_exc()
\"
echo ''
echo '🎉 DIAGNÓSTICO COMPLETADO'
"

Write-Host ""
Write-Host "🎉 Diagnóstico completado con Git Bash" -ForegroundColor Green
Write-Host "Para más información, ejecuta: .\ejecutar_con_bash.ps1" -ForegroundColor Yellow
