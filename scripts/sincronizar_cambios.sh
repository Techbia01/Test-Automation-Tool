#!/bin/bash
# Script para sincronizar cambios con el repositorio
# Uso: ./sincronizar_cambios.sh

echo "========================================"
echo "  SINCRONIZACION CON REPOSITORIO"
echo "========================================"
echo ""

# Verificar que estamos en la carpeta correcta
if [ ! -f "main.py" ]; then
    echo "ERROR: No se encuentra main.py"
    echo "Asegurate de ejecutar este script desde la raiz del proyecto"
    exit 1
fi

echo "[1/4] Verificando estado actual..."
git status
echo ""

echo "[2/4] Actualizando codigo desde el repositorio..."
git pull origin main
if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: Hubo un problema al actualizar el codigo"
    echo "Revisa los conflictos manualmente"
    exit 1
fi
echo ""

echo "[3/4] Verificando cambios locales..."
git status
echo ""

echo "[4/4] ¿Deseas subir tus cambios locales? (s/n)"
read -r respuesta
if [[ "$respuesta" =~ ^[Ss]$ ]]; then
    echo ""
    echo "Agregando cambios..."
    git add .
    echo ""
    read -p "Ingresa el mensaje del commit: " mensaje
    git commit -m "$mensaje"
    echo ""
    echo "Subiendo cambios..."
    git push origin main
    if [ $? -ne 0 ]; then
        echo ""
        echo "ERROR: Hubo un problema al subir los cambios"
        exit 1
    fi
    echo ""
    echo "✅ Cambios subidos exitosamente"
else
    echo ""
    echo "ℹ️  No se subieron cambios. Tus cambios locales se mantienen."
fi

echo ""
echo "========================================"
echo "  SINCRONIZACION COMPLETA"
echo "========================================"
echo ""

