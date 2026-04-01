#!/bin/bash
# Genera el paquete ZIP listo para subir a AWS Lambda
# Uso: bash scripts/build_lambda.sh

set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BUILD_DIR="$ROOT/build_lambda"
ZIP_FILE="$ROOT/lambda_package.zip"

echo "[1/4] Limpiando build anterior..."
rm -rf "$BUILD_DIR" "$ZIP_FILE"
mkdir -p "$BUILD_DIR"

echo "[2/4] Instalando dependencias..."
pip install -r "$ROOT/requirements_lambda.txt" -t "$BUILD_DIR" --quiet

echo "[3/4] Copiando código fuente..."
cp "$ROOT/lambda_handler.py" "$BUILD_DIR/"
cp -r "$ROOT/src"     "$BUILD_DIR/src"
cp -r "$ROOT/config"  "$BUILD_DIR/config"
cp -r "$ROOT/scripts" "$BUILD_DIR/scripts"

echo "[4/4] Generando ZIP..."
cd "$BUILD_DIR"
zip -r "$ZIP_FILE" . -x "*.pyc" -x "*/__pycache__/*" -x "*.dist-info/*" > /dev/null

echo ""
echo "✓ Paquete listo: $ZIP_FILE"
echo "  Tamaño: $(du -sh "$ZIP_FILE" | cut -f1)"
echo ""
echo "Sube el ZIP en AWS Lambda → Código → Subir desde archivo .zip"
echo "Handler: lambda_handler.lambda_handler"
echo "Runtime: Python 3.11"
