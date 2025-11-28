#!/bin/bash

# Script de inicio para Sistema de Finanzas Personales

clear
echo "========================================"
echo "  💰 Sistema de Finanzas Personales"
echo "========================================"
echo ""
echo "Iniciando aplicación..."
echo ""

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null
then
    echo "❌ [ERROR] Python no está instalado en tu sistema."
    echo "Por favor, instala Python 3 primero."
    exit 1
fi

# Verificar/instalar Flask
echo "Verificando dependencias..."
if ! python3 -c "import flask" &> /dev/null
then
    echo "Instalando Flask..."
    pip3 install flask
fi

echo ""
echo "========================================"
echo "  ✅ Iniciando servidor..."
echo "========================================"
echo ""
echo "🌐 La aplicación estará disponible en:"
echo "   http://localhost:5001"
echo ""
echo "💡 Presiona Ctrl+C para detener el servidor"
echo ""

# Ejecutar la aplicación
python3 finanzas_app.py

