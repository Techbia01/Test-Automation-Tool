# Automatización Linear + GitHub (sin intervención manual)

Este documento describe cómo ejecutar la generación de casos de prueba de forma automática: lectura de historias desde Linear (en un estado configurado), contexto opcional desde GitHub, generación de casos y subida como sub-issues en Linear.

## Cómo probar

### 1. Probar que el script arranca (sin API key)

Desde la raíz del proyecto:

```bash
python3 scripts/run_linear_automation.py
```

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

### 4. Probar solo el contexto de GitHub (sin Linear)

Desde la raíz del proyecto, en Python:

```bash
python3 -c "
import sys
sys.path.insert(0, 'src')
from github_context import get_project_context_for_issue, fetch_repo_context

# Repo por defecto
ctx = fetch_repo_context('Techbia01/Test-Automation-Tool', include_structure=True)
print('Contexto (primeros 500 chars):', (ctx or '')[:500])

# Extracción de URL desde texto
from github_context import extract_github_repo_from_text
text = 'Ver repo: https://github.com/owner/repo y mas texto'
print('Repo extraído:', extract_github_repo_from_text(text))
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
| `GITHUB_DEFAULT_REPO` / `github_default_repo` | Repo por defecto (`owner/repo` o URL). Se usa si el issue no contiene URL de GitHub |
| `GITHUB_TOKEN` / `github_token` | Token de GitHub para repos privados y mayor rate limit (opcional) |

### Ejemplo `automation_config.json`

```json
{
  "linear_api_key": "lin_api_xxxx",
  "linear_target_state": "TC Generator",
  "linear_state_after_success": "Ready for QA",
  "linear_team_ids": [],
  "github_default_repo": "mi-org/mi-repo",
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

- Si en la **descripción del issue** de Linear aparece una URL de GitHub (ej: `https://github.com/owner/repo` o `github.com/owner/repo`), se usa ese repo para obtener contexto.
- Si no hay URL, se usa **GITHUB_DEFAULT_REPO**.
- El contexto incluye el README y la lista de archivos/carpetas en la raíz del repo para mejorar la generación de casos.

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
- **Contexto GitHub vacío**: Si usas repo por defecto, comprueba `GITHUB_DEFAULT_REPO`. Para repos privados, define `GITHUB_TOKEN`.
