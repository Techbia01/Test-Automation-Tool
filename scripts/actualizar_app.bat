@echo off
echo 🔄 ACTUALIZANDO APLICACIÓN WEB QA
echo ================================

REM Buscar Python
set PYTHON_PATH=

if exist "C:\Program Files\Python311\python.exe" (
    set PYTHON_PATH="C:\Program Files\Python311\python.exe"
    goto :found_python
)

if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\python.exe" (
    set PYTHON_PATH="C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\python.exe"
    goto :found_python
)

echo ❌ Python no encontrado
pause
exit /b 1

:found_python
echo ✅ Python encontrado: %PYTHON_PATH%

REM Instalar dependencias
echo 🛠️ Instalando dependencias...
%PYTHON_PATH% -m pip install python-docx flask requests pandas openpyxl
if %errorlevel% neq 0 (
    echo ❌ Error al instalar dependencias
    pause
    exit /b 1
)

REM Matar procesos en puerto 5000
echo 🔄 Deteniendo procesos en puerto 5000...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :5000') do (
    taskkill /f /pid %%a >nul 2>&1
)

REM Esperar un momento
timeout /t 2 /nobreak >nul

echo 🚀 Iniciando aplicación web con nuevas funcionalidades...
echo 📱 URL: http://localhost:5000
echo 🆕 Nuevas funciones:
echo    - Exportación a Word (.docx)
echo    - Exportación a Excel mejorada
echo    - Exportación optimizada para Linear
echo    - Soporte completo para caracteres especiales
echo ================================

REM Iniciar aplicación
%PYTHON_PATH% app.py

pause
