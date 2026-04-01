#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AWS Lambda handler — Linear QA Automation
Puede dispararse desde:
  - API Gateway (webhook de Linear): procesa el issue específico del evento.
  - EventBridge (schedule): procesa todos los issues en estado TARGET_STATE.
"""

import hashlib
import hmac
import json
import os
import sys

# Asegurar que src/ y config/ estén en el path dentro del paquete Lambda
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "config"))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from run_linear_automation import run, run_single_issue


def _verify_linear_signature(body: str, signature: str, secret: str) -> bool:
    """Verifica la firma HMAC-SHA256 que Linear incluye en cada webhook."""
    expected = hmac.new(
        secret.encode("utf-8"),
        body.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    return hmac.compare_digest(expected, signature)


def _handle_webhook(event: dict, engine: str, verbose: bool) -> dict:
    """Procesa un evento de webhook de Linear (enviado por API Gateway)."""
    webhook_secret = os.environ.get("LINEAR_WEBHOOK_SECRET", "")
    raw_body = event.get("body") or ""

    # Verificar firma si se configuró un secreto
    if webhook_secret:
        signature = (event.get("headers") or {}).get("linear-signature", "")
        if not signature:
            print("[WARN] Webhook recibido sin cabecera linear-signature.")
            return {"statusCode": 400, "body": "Missing signature"}
        if not _verify_linear_signature(raw_body, signature, webhook_secret):
            print("[WARN] Firma del webhook inválida.")
            return {"statusCode": 401, "body": "Invalid signature"}

    try:
        payload = json.loads(raw_body)
    except json.JSONDecodeError as e:
        print("[ERROR] Payload no es JSON válido: %s" % e)
        return {"statusCode": 400, "body": "Invalid JSON"}

    action = payload.get("action", "")       # "create" | "update" | "remove"
    event_type = payload.get("type", "")     # "Issue" | "Comment" | …
    data = payload.get("data") or {}

    # Solo nos interesa: issue actualizado cuyo estado sea el objetivo
    if event_type != "Issue" or action not in ("create", "update"):
        print("[INFO] Evento ignorado: type=%s action=%s" % (event_type, action))
        return {"statusCode": 200, "body": "ignored"}

    issue_id = data.get("id")
    if not issue_id:
        return {"statusCode": 400, "body": "Missing issue id"}

    # Verificar que el nuevo estado sea el estado objetivo ("TC Generator")
    target_state = os.environ.get("LINEAR_TARGET_STATE", "TC Generator")
    new_state = (data.get("state") or {}).get("name", "")
    if new_state != target_state:
        print("[INFO] Estado '%s' no es '%s'; se ignora." % (new_state, target_state))
        return {"statusCode": 200, "body": "ignored"}

    print("[INFO] Webhook: issue %s movido a '%s'. Procesando…" % (issue_id, target_state))
    result = run_single_issue(issue_id=issue_id, verbose=verbose, engine=engine)
    print("[INFO] Resultado: %s" % result)
    return {"statusCode": 200, "body": result}


def lambda_handler(event, context):
    """
    Entrypoint Lambda.

    Variables de entorno esperadas (configurar en la consola AWS):
        LINEAR_API_KEY              Requerida
        LINEAR_TARGET_STATE         Default: "TC Generator"
        LINEAR_STATE_AFTER_SUCCESS  Default: vacío (no mover)
        LINEAR_WEBHOOK_SECRET       Recomendado: secreto para verificar firma
        ANTHROPIC_API_KEY           Requerida para engine=auto|claude
        GITHUB_TOKEN                Opcional (repos privados)
        QA_ENGINE                   auto | rules | claude | compare (default: auto)
        AUTOMATION_VERBOSE          0 | 1 (default: 0)
    """
    engine = os.environ.get("QA_ENGINE", "auto")
    verbose = os.environ.get("AUTOMATION_VERBOSE", "0").strip() == "1"

    try:
        # Si viene de API Gateway tendrá la clave "httpMethod" o "requestContext"
        is_webhook = bool(
            event.get("httpMethod") or event.get("requestContext")
        )

        if is_webhook:
            return _handle_webhook(event, engine, verbose)

        # EventBridge (schedule): procesar todos los issues en estado objetivo
        run(verbose=verbose, engine=engine)
        return {"statusCode": 200, "body": "OK"}

    except SystemExit as e:
        return {"statusCode": 500, "body": "Error de configuración: %s" % e}
    except Exception as e:
        print("[ERROR] Excepción no controlada: %s" % e)
        return {"statusCode": 500, "body": str(e)}
