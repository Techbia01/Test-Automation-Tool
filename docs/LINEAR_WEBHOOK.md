# Webhook Linear → generación de casos QA

Cuando un issue **pasa al estado** configurado en `LINEAR_TARGET_STATE` (ej. `TC_Generator` o `TC Generator`), Linear puede llamar a tu servidor y disparar la misma lógica que `run_linear_automation.py` **para ese issue**.

## Requisitos

1. **URL HTTPS pública**  
   Linear [no envía webhooks a localhost](https://linear.app/developers/webhooks). Opciones:
   - [ngrok](https://ngrok.com/), [Cloudflare Tunnel](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/), un VPS, Railway, etc.
2. **`LINEAR_WEBHOOK_SECRET`**  
   Mismo valor que el **signing secret** del webhook en Linear (Settings → API → Webhooks → detalle del webhook).
3. **`LINEAR_API_KEY`** y el resto de variables (GitHub, estados, etiquetas) como en la automatización por script.

## Pasos en Linear

1. Settings → **API** → **New webhook**.
2. **URL:** `https://tu-dominio/webhook` (debe coincidir con tu túnel/servidor).
3. **Resource types:** al menos **Issue** (o el alcance que permita tu plan).
4. Guarda y copia el **secret** a `LINEAR_WEBHOOK_SECRET` en `.env` o `automation_config.json` (`linear_webhook_secret`).

El nombre del estado disparador debe coincidir con **`LINEAR_TARGET_STATE`** (se ignoran mayúsculas y `_` vs espacio: `TC_Generator` = `TC Generator`).

## Arrancar el servidor

Desde la raíz del proyecto:

```bash
export LINEAR_WEBHOOK_SECRET='el_secreto_del_webhook'
python3 scripts/linear_webhook_server.py --port 8765
```

Con túnel (ejemplo ngrok):

```bash
ngrok http 8765
```

Usa la URL `https://xxxx.ngrok.io/webhook` en Linear.

## Comportamiento

- Solo reacciona cuando el issue **entra** en el estado objetivo:
  - **create:** issue creado ya en ese estado.
  - **update:** cambio de **estado** hacia ese estado (si solo editas descripción, no dispara).
- Responde **200** enseguida y ejecuta la generación en **segundo plano** (Linear corta si tardas > ~5 s).
- Si **`WEBHOOK_SKIP_IF_CHILDREN=1`** (por defecto) y el issue **ya tiene sub-issues**, no vuelve a generar (evita duplicados al reabrir o re-disparar).

## Desarrollo local

`LINEAR_WEBHOOK_SKIP_VERIFY=1` desactiva la firma HMAC **solo para pruebas**; no uses en producción.

## Variables relacionadas

| Variable | Descripción |
|----------|-------------|
| `LINEAR_WEBHOOK_SECRET` | Firma del webhook |
| `LINEAR_TARGET_STATE` | Estado que dispara (mismo que el script) |
| `LINEAR_WEBHOOK_PORT` / `--port` | Puerto del servidor |
| `WEBHOOK_SKIP_IF_CHILDREN` | Omitir si ya hay sub-issues (`1` / `true`) |
