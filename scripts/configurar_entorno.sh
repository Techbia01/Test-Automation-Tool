#!/bin/bash
# Script seguro para configurar el entorno local
# Este script NO borra nada, solo actualiza y configura

echo "========================================"
echo "  CONFIGURACION SEGURA DEL ENTORNO"
echo "========================================"
echo ""
echo "Este script va a:"
echo "- Actualizar el codigo desde el repositorio"
echo "- Instalar/actualizar dependencias"
echo "- Verificar que todo funciona"
echo ""
echo "NO va a borrar tus archivos locales (qa_projects.json, etc.)"
echo ""
read -p "Presiona Enter para continuar..."

# Verificar que estamos en la carpeta correcta
if [ ! -f "main.py" ]; then
    echo ""
    echo "ERROR: No se encuentra main.py"
    echo "Asegurate de ejecutar este script desde la raiz del proyecto"
    echo ""
    exit 1
fi

echo ""
echo "[1/5] Guardando estado actual de Git..."
if ! git status > /dev/null 2>&1; then
    echo "ERROR: Esta carpeta no es un repositorio Git"
    echo "Por favor, clona el repositorio primero:"
    echo "  git clone https://github.com/Techbia01/Test-Automation-Tool.git"
    exit 1
fi
echo "✅ Git configurado correctamente"

echo ""
echo "[2/5] Guardando cambios locales (si los hay)..."
git stash push -m "Cambios locales guardados automaticamente - $(date)"
echo "✅ Cambios locales guardados (puedes recuperarlos con: git stash pop)"

echo ""
echo "[3/5] Actualizando codigo desde el repositorio..."
git fetch origin
if [ $? -ne 0 ]; then
    echo "ERROR: No se pudo conectar con el repositorio"
    echo "Verifica tu conexion a internet"
    exit 1
fi

git pull origin main
if [ $? -ne 0 ]; then
    echo ""
    echo "⚠️  ADVERTENCIA: Hubo conflictos al actualizar"
    echo "Tus cambios locales estan guardados en stash"
    echo ""
    echo "Para resolver conflictos:"
    echo "1. Revisa los archivos con conflictos"
    echo "2. Resuelvelos manualmente"
    echo "3. Ejecuta: git add ."
    echo "4. Ejecuta: git commit -m 'Resuelto conflicto'"
    echo ""
    exit 1
fi
echo "✅ Codigo actualizado"

echo ""
echo "[4/5] Instalando/actualizando dependencias..."
pip install -r requirements.txt --quiet
if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: No se pudieron instalar las dependencias"
    echo "Intenta manualmente: pip install -r requirements.txt"
    exit 1
fi
echo "✅ Dependencias instaladas"

echo ""
echo "[5/5] Verificando que todo funciona..."
python3 -c "import flask; import pandas; print('✅ Todas las dependencias OK')" 2>/dev/null
if [ $? -ne 0 ]; then
    echo ""
    echo "⚠️  ADVERTENCIA: Algunas dependencias pueden no estar instaladas"
    echo "Intenta: pip install -r requirements.txt"
else
    echo "✅ Verificacion completada"
fi

echo ""
echo "========================================"
echo "  CONFIGURACION COMPLETA"
echo "========================================"
echo ""
echo "✅ Tu entorno esta listo para trabajar"
echo ""
echo "Para iniciar el servidor:"
echo "  python main.py"
echo ""
echo "Para recuperar tus cambios guardados (si los tenias):"
echo "  git stash pop"
echo ""
echo "Para ver la guia de trabajo en equipo:"
echo "  Abre: docs/GUIA_TRABAJO_EQUIPO.md"
echo ""

