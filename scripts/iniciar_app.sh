#!/bin/bash
# Script para iniciar la aplicación web QA en Linux/Mac

echo "🌐 INICIANDO SISTEMA WEB QA"
echo "================================"

# Buscar Python
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "❌ Python no encontrado"
    echo "💡 Por favor instala Python desde https://python.org"
    exit 1
fi

echo "✅ Python encontrado: $PYTHON_CMD"

# Verificar Flask
echo "🔍 Verificando Flask..."
if ! $PYTHON_CMD -c "import flask" 2>/dev/null; then
    echo "📦 Instalando dependencias..."
    $PYTHON_CMD -m pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ Error instalando dependencias"
        exit 1
    fi
    echo "✅ Dependencias instaladas"
else
    echo "✅ Flask disponible"
fi

# Crear directorios necesarios
mkdir -p uploads outputs

# Cambiar al directorio del proyecto
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$( cd "$SCRIPT_DIR/.." && pwd )"
cd "$PROJECT_DIR"

echo "🚀 Iniciando aplicación web..."
echo "📱 La aplicación se abrirá en: http://localhost:5000"
echo "💡 Para detener, presiona Ctrl+C"
echo "================================"

# Iniciar aplicación
$PYTHON_CMD main.py

