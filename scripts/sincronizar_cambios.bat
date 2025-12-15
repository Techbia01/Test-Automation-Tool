@echo off
REM Script para sincronizar cambios con el repositorio
REM Uso: sincronizar_cambios.bat

echo ========================================
echo   SINCRONIZACION CON REPOSITORIO
echo ========================================
echo.

REM Verificar que estamos en la carpeta correcta
if not exist "main.py" (
    echo ERROR: No se encuentra main.py
    echo Asegurate de ejecutar este script desde la raiz del proyecto
    pause
    exit /b 1
)

echo [1/4] Verificando estado actual...
git status
echo.

echo [2/4] Actualizando codigo desde el repositorio...
git pull origin main
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Hubo un problema al actualizar el codigo
    echo Revisa los conflictos manualmente
    pause
    exit /b 1
)
echo.

echo [3/4] Verificando cambios locales...
git status
echo.

echo [4/4] ¿Deseas subir tus cambios locales? (S/N)
set /p respuesta="> "
if /i "%respuesta%"=="S" (
    echo.
    echo Agregando cambios...
    git add .
    echo.
    set /p mensaje="Ingresa el mensaje del commit: "
    git commit -m "%mensaje%"
    echo.
    echo Subiendo cambios...
    git push origin main
    if %errorlevel% neq 0 (
        echo.
        echo ERROR: Hubo un problema al subir los cambios
        pause
        exit /b 1
    )
    echo.
    echo ✅ Cambios subidos exitosamente
) else (
    echo.
    echo ℹ️  No se subieron cambios. Tus cambios locales se mantienen.
)

echo.
echo ========================================
echo   SINCRONIZACION COMPLETA
echo ========================================
echo.
pause

