# 📚 Guía Completa: Subir Proyecto a Git

Esta guía te ayudará a subir el proyecto a Git (GitHub, GitLab, etc.) para que tus compañeros puedan descargarlo y usarlo localmente.

---

## 🚀 Paso 1: Verificar si Git está instalado

Abre una terminal (PowerShell en Windows, Terminal en Mac/Linux) y verifica:

```bash
git --version
```

Si no está instalado, descárgalo desde: https://git-scm.com/downloads

---

## 📦 Paso 2: Inicializar Git en tu proyecto

Navega a la carpeta del proyecto y ejecuta:

```bash
cd C:\test_automation_tool
git init
```

Esto creará un repositorio Git local en tu proyecto.

---

## ✅ Paso 3: Verificar qué archivos se van a subir

Antes de agregar todo, verifica qué archivos Git va a rastrear:

```bash
git status
```

Deberías ver:
- ✅ Archivos que SÍ se subirán (código fuente, templates, etc.)
- ❌ Archivos que NO se subirán (qa_projects.json, __pycache__, etc.) - estos están en .gitignore

---

## 📝 Paso 4: Agregar todos los archivos al staging

```bash
git add .
```

Esto agrega todos los archivos que NO están en .gitignore.

---

## 💾 Paso 5: Hacer el primer commit

```bash
git commit -m "Initial commit: Sistema de automatización de casos de prueba QA"
```

---

## 🌐 Paso 6: Crear repositorio en GitHub/GitLab

### Opción A: GitHub

1. Ve a https://github.com
2. Inicia sesión (o crea una cuenta)
3. Click en el botón **"+"** (arriba derecha) → **"New repository"**
4. Completa:
   - **Repository name**: `test_automation_tool` (o el nombre que prefieras)
   - **Description**: "Sistema de automatización de casos de prueba para QA"
   - **Visibility**: 
     - ✅ **Private** (solo tú y tus compañeros pueden verlo)
     - O **Public** (cualquiera puede verlo)
   - ❌ **NO marques** "Add a README file" (ya tienes uno)
   - ❌ **NO marques** "Add .gitignore" (ya tienes uno)
5. Click en **"Create repository"**

### Opción B: GitLab

1. Ve a https://gitlab.com
2. Inicia sesión (o crea una cuenta)
3. Click en **"New project"** → **"Create blank project"**
4. Completa el formulario similar a GitHub
5. Click en **"Create project"**

### Opción C: Bitbucket

1. Ve a https://bitbucket.org
2. Similar proceso a GitHub/GitLab

---

## 🔗 Paso 7: Conectar tu repositorio local con el remoto

Después de crear el repositorio en GitHub/GitLab, te mostrará una URL. Cópiala y ejecuta:

**Para HTTPS (recomendado para principiantes):**
```bash
git remote add origin https://github.com/TU-USUARIO/test_automation_tool.git
```

**Para SSH (si tienes configurado):**
```bash
git remote add origin git@github.com:TU-USUARIO/test_automation_tool.git
```

**⚠️ IMPORTANTE:** Reemplaza `TU-USUARIO` con tu usuario de GitHub/GitLab.

---

## 📤 Paso 8: Subir el código al repositorio

```bash
git branch -M main
git push -u origin main
```

Si es la primera vez, te pedirá autenticarte:
- **GitHub**: Te pedirá usuario y contraseña (o token personal)
- **GitLab**: Similar

---

## ✅ Paso 9: Verificar que se subió correctamente

Ve a tu repositorio en GitHub/GitLab y verifica que todos los archivos estén ahí.

---

## 👥 Paso 10: Compartir con tus compañeros

### Opción A: Invitar colaboradores (GitHub)

1. Ve a tu repositorio en GitHub
2. Click en **"Settings"** → **"Collaborators"**
3. Click en **"Add people"**
4. Ingresa el usuario de GitHub de tu compañero
5. Click en **"Add [usuario] to this repository"**

### Opción B: Compartir URL (si es público o ya los invitaste)

Comparte esta URL con tus compañeros:
```
https://github.com/TU-USUARIO/test_automation_tool.git
```

---

## 📥 Para tus compañeros: Cómo descargar y usar

Tus compañeros solo necesitan ejecutar:

```bash
# 1. Clonar el repositorio
git clone https://github.com/TU-USUARIO/test_automation_tool.git

# 2. Entrar al directorio
cd test_automation_tool

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Iniciar el servidor
python main.py
```

O usar los scripts:
- **Windows**: `scripts\iniciar_app.bat`
- **Linux/Mac**: `./scripts/iniciar_app.sh`

---

## 🔄 Actualizar el proyecto (cuando hagas cambios)

Cuando hagas cambios y quieras subirlos:

```bash
# 1. Ver qué cambió
git status

# 2. Agregar los cambios
git add .

# 3. Hacer commit
git commit -m "Descripción de los cambios"

# 4. Subir los cambios
git push
```

---

## 📥 Tus compañeros: Actualizar su copia

Cuando hagas cambios, tus compañeros pueden actualizar su copia:

```bash
# 1. Ir al directorio del proyecto
cd test_automation_tool

# 2. Descargar los cambios
git pull
```

---

## 🐛 Solución de Problemas

### Error: "remote origin already exists"

```bash
git remote remove origin
git remote add origin https://github.com/TU-USUARIO/test_automation_tool.git
```

### Error: "Authentication failed"

- **GitHub**: Necesitas un Personal Access Token en lugar de contraseña
  1. Ve a GitHub → Settings → Developer settings → Personal access tokens
  2. Genera un nuevo token
  3. Úsalo como contraseña al hacer `git push`

### Error: "Permission denied"

- Asegúrate de que tus compañeros estén invitados como colaboradores
- O que el repositorio sea público

### Error: "Port 5000 already in use"

Cada usuario ejecuta el servidor en su PC, así que no hay conflicto. Si un usuario tiene el puerto ocupado:

```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <numero_pid> /F

# Linux/Mac
lsof -ti:5000 | xargs kill -9
```

---

## ✅ Checklist Final

Antes de compartir, verifica:

- [ ] ✅ Git está inicializado (`git init`)
- [ ] ✅ Todos los archivos están agregados (`git add .`)
- [ ] ✅ Se hizo el commit inicial (`git commit`)
- [ ] ✅ El repositorio remoto está creado (GitHub/GitLab)
- [ ] ✅ El remoto está conectado (`git remote add origin`)
- [ ] ✅ El código está subido (`git push`)
- [ ] ✅ Los compañeros están invitados (si es privado)
- [ ] ✅ El README.md está actualizado

---

## 🎉 ¡Listo!

Tu proyecto está en Git y tus compañeros pueden clonarlo y usarlo localmente.

**Cada uno tendrá:**
- ✅ Su propia copia del código
- ✅ Sus propios proyectos (qa_projects.json no se comparte)
- ✅ Su propio servidor local (localhost:5000)
- ✅ Independencia total

---

## 📞 ¿Necesitas ayuda?

Si tienes problemas, revisa:
1. Los logs de Git (`git status`, `git log`)
2. La documentación de GitHub/GitLab
3. Los mensajes de error específicos



