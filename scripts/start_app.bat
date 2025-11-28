@echo off
echo ========================================
echo  Sistema de Automatizacion de Casos de Prueba para QA
echo ========================================
echo.
echo Iniciando servidor...
echo.
echo URLs disponibles:
echo - Aplicacion Principal: http://localhost:5000
echo - Crear Proyecto: http://localhost:5000/new_project
echo.
echo Presiona Ctrl+C para detener el servidor
echo ========================================
echo.

cd /d "%~dp0.."
echo Verificando estructura del proyecto...
python -c "from app import app; print('✅ Estructura del proyecto OK')"
echo.
echo Iniciando servidor...
python main.py

pause
