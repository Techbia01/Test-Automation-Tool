# 🚀 Guía de Instalación Rápida

## Para Windows

### Paso 1: Verificar Python

Abre PowerShell o CMD y ejecuta:

```bash
python --version
```

Debe mostrar `Python 3.8` o superior. Si no, descarga Python desde:
👉 https://www.python.org/downloads/

**IMPORTANTE**: Durante la instalación, marca ☑️ **"Add Python to PATH"**

---

### Paso 2: Descargar el proyecto

#### Opción A: Con Git

```bash
git clone https://github.com/tu-usuario/test_automation_tool.git
cd test_automation_tool
```

#### Opción B: Sin Git (descarga ZIP)

1. Ve al repositorio en GitHub
2. Click en **"Code"** → **"Download ZIP"**
3. Descomprime el archivo
4. Abre CMD/PowerShell en esa carpeta

---

### Paso 3: Instalar dependencias

```bash
pip install -r data/requirements.txt
```

Verás algo como:

```
Collecting flask...
Successfully installed flask-3.0.0 pandas-2.1.0 ...
```

---

### Paso 4: Ejecutar el sistema

```bash
python main.py
```

Verás:

```
============================================================
Iniciando Sistema de Automatizacion de Casos de Prueba para QA
Accede a: http://localhost:5000
============================================================
```

---

### Paso 5: Abrir en el navegador

Abre tu navegador y ve a:

```
http://localhost:5000
```

---

## Para Mac/Linux

```bash
# 1. Verificar Python
python3 --version

# 2. Clonar repositorio
git clone https://github.com/tu-usuario/test_automation_tool.git
cd test_automation_tool

# 3. Instalar dependencias
pip3 install -r data/requirements.txt

# 4. Ejecutar
python3 main.py

# 5. Abrir navegador en http://localhost:5000
```

---

## ⚠️ Solución de problemas comunes

### "python no se reconoce como comando"

**Solución**: Agrega Python a PATH manualmente

1. Busca donde está instalado Python (ej: `C:\Python311\`)
2. Ve a **Panel de Control → Sistema → Variables de entorno**
3. Agrega la ruta de Python a la variable `PATH`
4. Reinicia CMD/PowerShell

---

### "pip no se reconoce como comando"

**Solución**: Usa `python -m pip` en lugar de `pip`

```bash
python -m pip install -r data/requirements.txt
```

---

### "Port 5000 already in use"

**Solución**: Cambia el puerto en `main.py`

```python
# Línea 6 en main.py
app.run(debug=True, host='0.0.0.0', port=5001)  # Cambia a 5001 u otro
```

---

### Error de permisos en Windows

**Solución**: Ejecuta CMD como Administrador

1. Busca "CMD" en el menú inicio
2. Click derecho → **"Ejecutar como administrador"**
3. Navega a la carpeta y ejecuta los comandos

---

## ✅ Verificar instalación

Si todo funciona correctamente, verás:

1. ✅ Servidor corriendo en http://localhost:5000
2. ✅ Página de inicio cargando
3. ✅ Botón "Crear Nuevo Proyecto" visible

---

## 🎯 Próximos pasos

1. **Lee el README.md** para uso completo
2. **Crea tu primer proyecto**: http://localhost:5000/new_project
3. **Obtén tu API Key de Linear** (si quieres subir casos automáticamente)

---

## 💡 Consejos

- **Mantén CMD/PowerShell abierto** mientras uses el sistema
- Para detener el servidor: `Ctrl + C`
- Tus datos se guardan en `qa_projects.json` (no se borran al cerrar)
- Cada vez que actualices desde Git: `pip install -r data/requirements.txt --upgrade`

---

¡Listo! 🎉 Ya puedes empezar a generar casos de prueba.

