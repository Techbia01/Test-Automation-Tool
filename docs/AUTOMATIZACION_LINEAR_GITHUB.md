# Automatización Linear + GitHub (sin intervención manual)

Este documento describe cómo ejecutar la generación de casos de prueba de forma automática: lectura de historias desde Linear (en un estado configurado), contexto opcional desde GitHub, generación de casos y subida como sub-issues en Linear.

## Cómo probar

### 1. Probar que el script arranca (sin API key)

Desde la raíz del proyecto:

```bash
python3 scripts/run_linear_automation.py
```

**Salida por defecto (ejecución real):** solo **repo GitHub**, **código del issue** (ej. `ACQ-368`), **título** y **lista de casos** con **`[MANUAL]`** o **`[AUTO]`** (los casos dudosos cuentan como manual), más resultado esperado truncado y nota breve. Para volcar descripción completa, README GitHub y detalle de cada paso: `python3 scripts/run_linear_automation.py --verbose` o `AUTOMATION_VERBOSE=1`.

### Ejecución sugerida (manual vs automatizable)

Cada caso generado incluye una **clasificación heurística** (no sustituye criterio humano):

| Valor | Significado |
|-------|-------------|
| **Manual** | Incluye casos dudosos: ejecutar a mano (usabilidad, señales mixtas, etc.). |
| **Automatizable** | Flujo verificable por API/UI estable; candidato a E2E o contratos. |

En **Linear**, la descripción del sub-issue empieza con **Ejecución sugerida** y **Nota**. Opcionalmente, si creas en el equipo etiquetas con el **mismo nombre** que configures, se añaden a los sub-issues:

- Por defecto se buscan **`TC_Manual`** y **`TC_Automatizable`** (coinciden con nombres habituales en Linear). Se listan **todas** las etiquetas del equipo con paginación, para no perder etiquetas que quedan fuera de la primera página de la API. Si no existen, el script intenta crearlas. Puedes cambiar los nombres con `LINEAR_LABEL_MANUAL_TEST` / `LINEAR_LABEL_AUTOMATABLE`. También se prueban alias `Manual` / `Automatizable` si el nombre configurado no existe.

Sin configurar nada deberías ver: `[ERROR] LINEAR_API_KEY no configurado`. Eso confirma que el script y la carga de config funcionan.

### 2. Probar que se carga el `.env`

Copia la plantilla y pon una API key de prueba (o la real):

```bash
cp .env.example .env
# Edita .env y pon LINEAR_API_KEY=lin_api_tu_clave_real
```

Vuelve a ejecutar:

```bash
python3 scripts/run_linear_automation.py
```

- Si la clave es **inválida**: verás `[ERROR] No se pudo conectar con Linear`. La carga de `.env` está bien; revisa la clave en Linear (Settings → API).
- Si la clave es **válida** pero no tienes issues en el estado configurado: verás `[INFO] No hay issues en estado 'TC Generator'. Nada que procesar.` Eso es correcto.

### 3. Probar el flujo completo (Linear + generación)

1. **En Linear:** Crea un estado con el nombre que uses en config (por defecto `TC Generator`). Si ya tienes uno, úsalo.
2. **En Linear:** Crea o elige una historia de usuario y **muévela a ese estado**. La descripción debe contener el texto de la HU (criterios de aceptación, etc.).
3. Opcional: en la descripción del issue puedes poner una URL de GitHub, ej. `https://github.com/Techbia01/Test-Automation-Tool`, para que el script use ese repo como contexto.
4. En la raíz del proyecto, con `.env` configurado (o `LINEAR_API_KEY` exportada):

   ```bash
   python3 scripts/run_linear_automation.py
   ```

5. Revisa en Linear: el issue debe tener **sub-issues** creados (los casos de prueba). Si configuraste `LINEAR_STATE_AFTER_SUCCESS`, el issue habrá pasado a ese estado.

### 4. Probar solo la extracción desde Linear (sin generar casos)

Script dedicado: no genera casos de prueba ni sube nada a Linear.

```bash
# Ver rama (branchName), adjuntos y descripción de un issue
python3 scripts/inspect_linear_issue.py FIN-123

# Listar issues del estado configurado en .env (LINEAR_TARGET_STATE)
python3 scripts/inspect_linear_issue.py --list

# Listar otro estado
python3 scripts/inspect_linear_issue.py --list --state "TC Generator"
```

Necesitas `LINEAR_API_KEY` en `.env`.

### 5. Ver qué información trae GitHub (README + estructura)

Script que imprime **el mismo texto** que se inyecta en el generador de casos:

```bash
# Repo concreto (público; sin token hace falta si es privado)
python3 scripts/inspect_github_context.py owner/repo

# Rama concreta (equivalente a branchName de Linear + GITHUB_DEFAULT_REPO)
python3 scripts/inspect_github_context.py owner/repo --ref mi-rama

# Usar GITHUB_DEFAULT_REPO y GITHUB_TOKEN del .env
python3 scripts/inspect_github_context.py --from-env

# Simular issue con rama en Linear + repo por defecto
python3 scripts/inspect_github_context.py owner/repo --linear-branch mi-rama

# Vista corta
python3 scripts/inspect_github_context.py owner/repo --max-chars 1500
```

Si sale vacío: repo privado sin `GITHUB_TOKEN`, rama inexistente o repo mal escrito.

**Probar repo por equipo (sin escribir owner/repo a mano):**

```bash
python3 scripts/inspect_github_context.py --team-key FIN --linear-branch feature/acq-3
```

(Requiere `github_team_repos` con la clave `FIN` en `automation_config.json`.)

**Solo el README (texto plano en consola):**

```bash
python3 scripts/show_github_readme.py org/repo
python3 scripts/show_github_readme.py org/repo --ref nombre-rama
python3 scripts/show_github_readme.py --from-env
python3 scripts/show_github_readme.py --team-key ACQ

# Si falla: ver motivo (token, 404, SSO de la organización)
python3 scripts/show_github_readme.py biaenergy/bianetwork-web-app --ref feature/factura-gamification -v
```

Si ves **403** y mensaje de **SSO**: en GitHub → Settings → Developer settings → el token → **Configure SSO** → **Authorize** junto a la organización `biaenergy`.

**Alternativa rápida** (una línea):

```bash
python3 -c "
import sys; sys.path.insert(0,'src')
from github_context import fetch_repo_context
print(fetch_repo_context('octocat/Hello-World')[:800])
"
```

Deberías ver un trozo del README del repo y `Repo extraído: owner/repo`.

---

## Requisitos

- Python 3.8+
- Dependencias instaladas (`pip install -r requirements.txt`)
- **LINEAR_API_KEY**: API Key de Linear (obligatorio para el flujo automático)

## Variables de entorno y configuración

Todas las opciones pueden definirse por **variable de entorno**, por un archivo **`.env`** (recomendado por seguridad) o en **`automation_config.json`**. Orden de prioridad: variables de entorno (incluidas las cargadas desde `.env`) > `automation_config.json`.

**Seguridad:** Copia `.env.example` a `.env` y rellena ahí las claves (LINEAR_API_KEY, GITHUB_TOKEN). El archivo `.env` no se sube a Git.

| Variable / clave JSON        | Descripción |
|-----------------------------|-------------|
| `LINEAR_API_KEY` / `linear_api_key` | API Key de Linear (requerido) |
| `LINEAR_TARGET_STATE` / `linear_target_state` | Estado en el que deben estar las historias para generar casos (por defecto: `TC Generator`) |
| `LINEAR_STATE_AFTER_SUCCESS` / `linear_state_after_success` | Estado al que mover el issue tras generar (ej: `Ready for QA`). Opcional; si no se define, el issue no cambia de estado |
| `LINEAR_TEAM_IDS` / `linear_team_ids` | IDs de equipos separados por coma (o lista en JSON). Vacío = todos los equipos |
| `GITHUB_DEFAULT_REPO` / `github_default_repo` | Repo por defecto si no hay URL en el issue ni mapeo por equipo |
| `github_team_repos` (JSON) | Varios equipos: `{"FIN":"org/repo-a","ACQ":"org/repo-b"}`. La clave = prefijo del issue (`FIN-123` → `FIN`). **No se puede deducir el repo solo con el nombre de rama** |
| `GITHUB_TEAM_REPOS` | Mismo mapa en JSON vía variable de entorno (opcional) |
| `GITHUB_TOKEN` / `github_token` | Token para repos privados (opcional) |

### Ejemplo `automation_config.json`

```json
{
  "linear_api_key": "lin_api_xxxx",
  "linear_target_state": "TC Generator",
  "linear_state_after_success": "Ready for QA",
  "linear_team_ids": [],
  "github_default_repo": "mi-org/repo-por-defecto",
  "github_team_repos": {
    "FIN": "mi-org/app-finanzas",
    "ACQ": "mi-org/app-adquisiciones"
  },
  "github_token": ""
}
```

- **Recomendado:** `cp .env.example .env` y edita `.env` con tus claves (el archivo `.env` está en `.gitignore`).
- Alternativa: copia `automation_config.example.json` a `automation_config.json` y rellena los valores. No subas archivos con claves reales a Git.

## Ejecución del script

Desde la **raíz del proyecto**:

```bash
python3 scripts/run_linear_automation.py
```

En Windows (si `python` apunta a Python 3):

```bash
python scripts/run_linear_automation.py
```

El script:

1. Conecta a Linear y lista issues en el estado configurado (`LINEAR_TARGET_STATE`).
2. Por cada issue: obtiene la descripción (historia de usuario), resuelve el repo de GitHub (URL en la descripción o repo por defecto), obtiene contexto (README y estructura) y genera casos de prueba.
3. Sube los casos como sub-issues del issue en Linear.
4. Si está configurado `LINEAR_STATE_AFTER_SUCCESS`, mueve el issue a ese estado para no reprocesarlo.

## Repositorio GitHub por issue

Orden de resolución del repo:

1. **Adjuntos** (PR / URL GitHub).
2. **Descripción** con URL de GitHub.
3. **`github_team_repos`**: repo según la clave del equipo (`FIN-123` → clave `FIN`).
4. **`GITHUB_DEFAULT_REPO`**.

**Rama (`branchName`):** solo indica en qué rama está el trabajo; **no identifica el repositorio** (muchas apps pueden tener una rama `feature/x`). Para varios equipos en un mismo Linear, define **`github_team_repos`** en `automation_config.json`. El README se pide con `?ref=<rama>` cuando ya se conoce el repo.

## Webhook (disparo al cambiar de estado)

Si quieres ejecutar **en cuanto** un issue pasa al estado configurado (sin esperar al cron), usa un servidor webhook. Guía: [docs/LINEAR_WEBHOOK.md](LINEAR_WEBHOOK.md).

## Ejemplo de cron (Linux/macOS)

Ejecutar cada 15 minutos:

```bash
# Editar crontab
crontab -e

# Añadir línea (ajustar ruta y variables)
*/15 * * * * cd /ruta/a/Test-Automation-Tool && LINEAR_API_KEY=lin_api_xxx LINEAR_TARGET_STATE="TC Generator" LINEAR_STATE_AFTER_SUCCESS="Ready for QA" python3 scripts/run_linear_automation.py >> /tmp/linear_automation.log 2>&1
```

O usando un script wrapper que cargue un `.env`:

```bash
# run_auto_qa.sh
cd /ruta/a/Test-Automation-Tool
set -a
[ -f .env ] && source .env
set +a
python3 scripts/run_linear_automation.py
```

Y en crontab:

```bash
*/15 * * * * /ruta/a/run_auto_qa.sh >> /tmp/linear_automation.log 2>&1
```

## Estados en Linear

- Crea en tu workspace de Linear un estado con el nombre configurado en `LINEAR_TARGET_STATE` (por defecto **TC Generator**).
- Las historias que muevas a ese estado serán las que el script procese.
- Opcionalmente configura `LINEAR_STATE_AFTER_SUCCESS` (ej: **Ready for QA**) para mover el issue después de generar los casos y evitar duplicados en la siguiente ejecución.

## Solución de problemas

- **"LINEAR_API_KEY no configurado"**: Define la variable de entorno o `linear_api_key` en `automation_config.json`.
- **"No se pudo conectar con Linear"**: Comprueba que la API Key sea válida y tenga permisos de lectura/escritura.
- **"No hay issues en estado '...'"**: Verifica que el nombre del estado coincida exactamente con el de la UI de Linear y que existan issues en ese estado.
- **Contexto GitHub vacío**: Comprueba `GITHUB_DEFAULT_REPO` o `github_team_repos` (clave = prefijo del issue). Repos privados: `GITHUB_TOKEN`.
