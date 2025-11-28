@echo off
title Sistema de Finanzas Personales
color 0A

echo ========================================
echo   Sistema de Finanzas Personales
echo ========================================
echo.
echo Iniciando aplicacion...
echo.

REM Verificar si Python esta instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no esta instalado en tu sistema.
    echo Por favor, instala Python desde https://www.python.org/
    pause
    exit /b
)

REM Verificar/instalar Flask
echo Verificando dependencias...
pip show flask >nul 2>&1
if errorlevel 1 (
    echo Instalando Flask...
    pip install flask
)

echo.
echo ========================================
echo   Iniciando servidor...
echo ========================================
echo.
echo La aplicacion se abrira en:
echo http://localhost:5001
echo.
echo Presiona Ctrl+C para detener el servidor
echo.

REM Ejecutar la aplicacion
python finanzas_app.py

pause

