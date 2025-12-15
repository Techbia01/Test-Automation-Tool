# 👥 Guía de Trabajo en Equipo - Sin Conflictos

Esta guía te ayudará a trabajar con tu compañero sin generar conflictos en Git.

---

## 🚨 **REGLAS DE ORO**

### ✅ **ANTES de empezar a trabajar:**

1. **SIEMPRE actualiza tu código local primero:**
   ```bash
   git pull origin main
   ```

2. **Verifica que no tengas cambios sin guardar:**
   ```bash
   git status
   ```
   Si hay cambios, decide:
   - **Guardarlos:** `git add .` y `git commit -m "mensaje"`
   - **Descartarlos:** `git stash` (los puedes recuperar después con `git stash pop`)

3. **Asegúrate de estar en la rama main:**
   ```bash
   git branch
   ```
   Debe mostrar `* main`

---

## 🔄 **FLUJO DE TRABAJO DIARIO**

### **Al INICIAR el día:**

```bash
# 1. Actualizar código
git pull origin main

# 2. Verificar que el servidor funciona
python main.py
```

### **Al TERMINAR tu trabajo:**

```bash
# 1. Ver qué cambios hiciste
git status

# 2. Agregar tus cambios
git add .

# 3. Hacer commit con mensaje claro
git commit -m "Descripción clara de lo que cambiaste"

# 4. Subir cambios
git push origin main
```

### **Si hay conflictos al hacer pull:**

```bash
# 1. Hacer pull
git pull origin main

# 2. Si hay conflictos, Git te dirá qué archivos
# 3. Abre los archivos con conflictos (busca <<<<<<< HEAD)
# 4. Resuelve los conflictos manualmente
# 5. Agrega los archivos resueltos
git add archivo_con_conflicto.py

# 6. Completa el merge
git commit -m "Resuelto conflicto en archivo_con_conflicto.py"

# 7. Sube los cambios
git push origin main
```

---

## 🛡️ **ARCHIVOS QUE NO DEBEN GENERAR CONFLICTOS**

Estos archivos están en `.gitignore` y **NO se suben a Git**:

- ✅ `qa_projects.json` - Tus proyectos locales
- ✅ `uploads/` - Archivos que subes
- ✅ `outputs/` - Archivos generados
- ✅ `__pycache__/` - Caché de Python
- ✅ `*.log` - Logs locales

**Cada uno tiene su propia copia local** - No hay conflictos.

---

## ⚠️ **SI HAY CONFLICTOS**

### **Opción 1: Resolver manualmente (Recomendado)**

1. Abre el archivo con conflicto
2. Busca las marcas:
   ```
   <<<<<<< HEAD
   Tu código
   =======
   Código del compañero
   >>>>>>> origin/main
   ```
3. Decide qué código mantener (o combina ambos)
4. Elimina las marcas `<<<<<<<`, `=======`, `>>>>>>>`
5. Guarda el archivo
6. Ejecuta:
   ```bash
   git add archivo.py
   git commit -m "Resuelto conflicto"
   git push origin main
   ```

### **Opción 2: Usar tu versión (CUIDADO - Solo si estás seguro)**

```bash
git checkout --ours archivo.py
git add archivo.py
git commit -m "Manteniendo mi versión de archivo.py"
git push origin main
```

### **Opción 3: Usar la versión del repositorio (CUIDADO - Pierdes tus cambios)**

```bash
git checkout --theirs archivo.py
git add archivo.py
git commit -m "Aceptando versión del repositorio"
git push origin main
```

---

## 📋 **CHECKLIST ANTES DE SUBIR CAMBIOS**

- [ ] ¿Hice `git pull` antes de empezar?
- [ ] ¿El servidor funciona localmente? (`python main.py`)
- [ ] ¿No hay errores de sintaxis?
- [ ] ¿El mensaje del commit es claro?
- [ ] ¿Solo subo archivos de código (no `qa_projects.json`, `uploads/`, etc.)?

---

## 🚀 **COMANDOS RÁPIDOS**

### **Ver estado actual:**
```bash
git status
```

### **Actualizar código:**
```bash
git pull origin main
```

### **Subir cambios:**
```bash
git add .
git commit -m "Tu mensaje aquí"
git push origin main
```

### **Ver historial:**
```bash
git log --oneline -10
```

### **Deshacer cambios locales (CUIDADO):**
```bash
git reset --hard origin/main
```
⚠️ **Esto elimina TODOS tus cambios locales no guardados**

---

## 💡 **MEJORES PRÁCTICAS**

1. **Trabaja en archivos diferentes cuando sea posible**
   - Si tu compañero está en `app.py`, trabaja en `src/professional_qa_generator.py`

2. **Haz commits pequeños y frecuentes**
   - Mejor: 5 commits pequeños que 1 grande
   - Facilita resolver conflictos

3. **Comunícate antes de hacer cambios grandes**
   - "Voy a modificar `app.py`" → Tu compañero sabe que no debe tocarlo

4. **Usa mensajes de commit claros:**
   - ❌ `git commit -m "fix"`
   - ✅ `git commit -m "Fix: Corregir error TestType.FUNCTIONAL en app.py"`

5. **Prueba localmente antes de subir:**
   - Siempre ejecuta `python main.py` y verifica que funciona

---

## 🔧 **SI EL SERVIDOR NO INICIA**

### **Error: "ModuleNotFoundError"**
```bash
pip install -r requirements.txt
```

### **Error: "Port already in use"**
```bash
# Windows
taskkill /F /IM python.exe

# Mac/Linux
pkill -f python
```

### **Error: "Git conflict"**
Sigue la sección "SI HAY CONFLICTOS" arriba.

---

## 📞 **SI NADA FUNCIONA**

1. **Guarda tu trabajo:**
   ```bash
   git stash
   ```

2. **Obtén la versión más reciente:**
   ```bash
   git fetch origin
   git reset --hard origin/main
   ```

3. **Recupera tu trabajo:**
   ```bash
   git stash pop
   ```

4. **Resuelve conflictos manualmente si aparecen**

---

## ✅ **VERIFICACIÓN FINAL**

Antes de cerrar, verifica:

```bash
# 1. Estado limpio
git status
# Debe decir: "nothing to commit, working tree clean"

# 2. Estás actualizado
git log --oneline -1
# Debe mostrar el último commit que subiste

# 3. El servidor funciona
python main.py
# Debe iniciar sin errores
```

---

**Última actualización:** 2024
**Versión:** 1.0

