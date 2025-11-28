@echo off
echo 🌐 INICIANDO SISTEMA WEB QA
echo ================================

REM Buscar Python en ubicaciones comunes
set PYTHON_PATH=

REM Verificar si Python está en el PATH
python --version >nul 2>&1
if %errorlevel% == 0 (
    set PYTHON_PATH=python
    goto :found_python
)

REM Buscar en ubicaciones comunes
if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\python.exe" (
    set PYTHON_PATH="C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\python.exe"
    goto :found_python
)

if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312\python.exe" (
    set PYTHON_PATH="C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312\python.exe"
    goto :found_python
)

if exist "C:\Python311\python.exe" (
    set PYTHON_PATH="C:\Python311\python.exe"
    goto :found_python
)

if exist "C:\Python312\python.exe" (
    set PYTHON_PATH="C:\Python312\python.exe"
    goto :found_python
)

REM Buscar en Program Files
for /d %%i in ("C:\Program Files\Python*") do (
    if exist "%%i\python.exe" (
        set PYTHON_PATH="%%i\python.exe"
        goto :found_python
    )
)

for /d %%i in ("C:\Program Files (x86)\Python*") do (
    if exist "%%i\python.exe" (
        set PYTHON_PATH="%%i\python.exe"
        goto :found_python
    )
)

echo ❌ Python no encontrado
echo 💡 Por favor instala Python desde https://python.org
echo    Asegúrate de marcar "Add Python to PATH" durante la instalación
pause
exit /b 1

:found_python
echo ✅ Python encontrado: %PYTHON_PATH%

REM Verificar Flask
echo 🔍 Verificando Flask...
%PYTHON_PATH% -c "import flask" >nul 2>&1
if %errorlevel% neq 0 (
    echo 📦 Instalando Flask...
    %PYTHON_PATH% -m pip install flask requests
    if %errorlevel% neq 0 (
        echo ❌ Error instalando Flask
        pause
        exit /b 1
    )
)

echo ✅ Flask disponible

REM Crear directorios necesarios
if not exist "uploads" mkdir uploads
if not exist "outputs" mkdir outputs

echo 🚀 Iniciando aplicación web...
echo 📱 La aplicación se abrirá en: http://localhost:5000
echo 💡 Para detener, presiona Ctrl+C
echo ================================

REM Iniciar aplicación
cd /d "%~dp0.."
%PYTHON_PATH% main.py

pause
