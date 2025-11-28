# Script de PowerShell para iniciar la aplicación web QA
Write-Host "🌐 INICIANDO SISTEMA WEB QA" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan

# Buscar Python en ubicaciones comunes
$pythonPaths = @(
    "python",  # En PATH
    "$env:USERPROFILE\AppData\Local\Programs\Python\Python311\python.exe",
    "$env:USERPROFILE\AppData\Local\Programs\Python\Python312\python.exe",
    "C:\Python311\python.exe",
    "C:\Python312\python.exe"
)

# Buscar en Program Files
$programFilesPaths = Get-ChildItem "C:\Program Files\Python*" -ErrorAction SilentlyContinue | ForEach-Object { "$($_.FullName)\python.exe" }
$programFilesX86Paths = Get-ChildItem "C:\Program Files (x86)\Python*" -ErrorAction SilentlyContinue | ForEach-Object { "$($_.FullName)\python.exe" }

$pythonPaths += $programFilesPaths
$pythonPaths += $programFilesX86Paths

$pythonExe = $null

foreach ($path in $pythonPaths) {
    if ($path -eq "python") {
        # Verificar si python está en PATH
        try {
            $null = & python --version 2>$null
            if ($LASTEXITCODE -eq 0) {
                $pythonExe = "python"
                break
            }
        } catch {
            continue
        }
    } else {
        if (Test-Path $path) {
            $pythonExe = $path
            break
        }
    }
}

if (-not $pythonExe) {
    Write-Host "❌ Python no encontrado" -ForegroundColor Red
    Write-Host "💡 Por favor instala Python desde https://python.org" -ForegroundColor Yellow
    Write-Host "   Asegúrate de marcar 'Add Python to PATH' durante la instalación" -ForegroundColor Yellow
    Read-Host "Presiona Enter para salir"
    exit 1
}

Write-Host "✅ Python encontrado: $pythonExe" -ForegroundColor Green

# Verificar Flask
Write-Host "🔍 Verificando Flask..." -ForegroundColor Yellow
try {
    & $pythonExe -c "import flask" 2>$null
    if ($LASTEXITCODE -ne 0) {
        throw "Flask no encontrado"
    }
    Write-Host "✅ Flask disponible" -ForegroundColor Green
} catch {
    Write-Host "📦 Instalando Flask..." -ForegroundColor Yellow
    & $pythonExe -m pip install flask requests
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Error instalando Flask" -ForegroundColor Red
        Read-Host "Presiona Enter para salir"
        exit 1
    }
    Write-Host "✅ Flask instalado" -ForegroundColor Green
}

# Crear directorios necesarios
if (-not (Test-Path "uploads")) { New-Item -ItemType Directory -Name "uploads" | Out-Null }
if (-not (Test-Path "outputs")) { New-Item -ItemType Directory -Name "outputs" | Out-Null }

Write-Host "🚀 Iniciando aplicación web..." -ForegroundColor Green
Write-Host "📱 La aplicación se abrirá en: http://localhost:5000" -ForegroundColor Cyan
Write-Host "💡 Para detener, presiona Ctrl+C" -ForegroundColor Yellow
Write-Host "================================" -ForegroundColor Cyan

# Cambiar al directorio del proyecto
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectDir = Split-Path -Parent $scriptDir
Set-Location $projectDir

# Iniciar aplicación
try {
    & $pythonExe main.py
} catch {
    Write-Host "❌ Error iniciando aplicación: $_" -ForegroundColor Red
    Read-Host "Presiona Enter para salir"
}
