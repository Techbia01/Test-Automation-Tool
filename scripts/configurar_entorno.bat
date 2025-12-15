@echo off
REM Script seguro para configurar el entorno local
REM Este script NO borra nada, solo actualiza y configura

echo ========================================
echo   CONFIGURACION SEGURA DEL ENTORNO
echo ========================================
echo.
echo Este script va a:
echo - Actualizar el codigo desde el repositorio
echo - Instalar/actualizar dependencias
echo - Verificar que todo funciona
echo.
echo NO va a borrar tus archivos locales (qa_projects.json, etc.)
echo.
pause

REM Verificar que estamos en la carpeta correcta
if not exist "main.py" (
    echo.
    echo ERROR: No se encuentra main.py
    echo Asegurate de ejecutar este script desde la raiz del proyecto
    echo.
    pause
    exit /b 1
)

echo.
echo [1/5] Guardando estado actual de Git...
git status > nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Esta carpeta no es un repositorio Git
    echo Por favor, clona el repositorio primero:
    echo   git clone https://github.com/Techbia01/Test-Automation-Tool.git
    pause
    exit /b 1
)
echo ✅ Git configurado correctamente

echo.
echo [2/5] Guardando cambios locales (si los hay)...
git stash push -m "Cambios locales guardados automaticamente - %date% %time%"
echo ✅ Cambios locales guardados (puedes recuperarlos con: git stash pop)

echo.
echo [3/5] Actualizando codigo desde el repositorio...
git fetch origin
if %errorlevel% neq 0 (
    echo ERROR: No se pudo conectar con el repositorio
    echo Verifica tu conexion a internet
    pause
    exit /b 1
)

git pull origin main
if %errorlevel% neq 0 (
    echo.
    echo ⚠️  ADVERTENCIA: Hubo conflictos al actualizar
    echo Tus cambios locales estan guardados en stash
    echo.
    echo Para resolver conflictos:
    echo 1. Revisa los archivos con conflictos
    echo 2. Resuelvelos manualmente
    echo 3. Ejecuta: git add .
    echo 4. Ejecuta: git commit -m "Resuelto conflicto"
    echo.
    pause
    exit /b 1
)
echo ✅ Codigo actualizado

echo.
echo [4/5] Instalando/actualizando dependencias...
pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo.
    echo ERROR: No se pudieron instalar las dependencias
    echo Intenta manualmente: pip install -r requirements.txt
    pause
    exit /b 1
)
echo ✅ Dependencias instaladas

echo.
echo [5/5] Verificando que todo funciona...
python -c "import flask; import pandas; print('✅ Todas las dependencias OK')" 2>nul
if %errorlevel% neq 0 (
    echo.
    echo ⚠️  ADVERTENCIA: Algunas dependencias pueden no estar instaladas
    echo Intenta: pip install -r requirements.txt
) else (
    echo ✅ Verificacion completada
)

echo.
echo ========================================
echo   CONFIGURACION COMPLETA
echo ========================================
echo.
echo ✅ Tu entorno esta listo para trabajar
echo.
echo Para iniciar el servidor:
echo   python main.py
echo.
echo Para recuperar tus cambios guardados (si los tenias):
echo   git stash pop
echo.
echo Para ver la guia de trabajo en equipo:
echo   Abre: docs\GUIA_TRABAJO_EQUIPO.md
echo.
pause

