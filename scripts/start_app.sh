#!/bin/bash
# Script de inicio para el Sistema de Automatización de Casos de Prueba para QA

echo "========================================"
echo " Sistema de Automatizacion de Casos de Prueba para QA"
echo "========================================"
echo ""
echo "Iniciando servidor..."
echo ""
echo "URLs disponibles:"
echo "- Aplicacion Principal: http://localhost:5000"
echo "- Crear Proyecto: http://localhost:5000/new_project"
echo ""
echo "Presiona Ctrl+C para detener el servidor"
echo "========================================"
echo ""

# Cambiar al directorio del script
cd "$(dirname "$0")"

echo "🔍 Verificando estructura del proyecto..."
echo "📁 Directorio actual: $(pwd)"
echo "📁 Archivos Python encontrados:"
find . -name "*.py" -type f | head -10

echo ""
echo "🧪 Probando importaciones..."
python -c "
import sys
import os
print('✅ Python version:', sys.version)
print('✅ Python path:', sys.executable)
print('✅ Current directory:', os.getcwd())
print('✅ Python path entries:')
for p in sys.path[:5]:
    print('  -', p)
"

echo ""
echo "🔧 Verificando dependencias..."
python -c "
try:
    import flask
    print('✅ Flask:', flask.__version__)
except ImportError as e:
    print('❌ Flask no encontrado:', e)

try:
    import pandas
    print('✅ Pandas:', pandas.__version__)
except ImportError as e:
    print('❌ Pandas no encontrado:', e)
"

echo ""
echo "🚀 Iniciando servidor..."
python main.py
