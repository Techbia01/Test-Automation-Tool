#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Servidor HTTP para webhooks de Linear: al pasar un issue al estado configurado
(LINEAR_TARGET_STATE, ej. TC_Generator o TC Generator), genera casos y sub-issues.

Requisitos:
  - URL HTTPS pública (ngrok, Cloudflare Tunnel, PaaS, etc.); Linear no llama a localhost.
  - LINEAR_WEBHOOK_SECRET: mismo valor que en Linear → Settings → API → tu webhook.
  - LINEAR_API_KEY y resto de config como en run_linear_automation.py.

Linear exige respuesta < ~5 s; el trabajo pesado va en un hilo en segundo plano.

Ejemplo:
  export LINEAR_WEBHOOK_SECRET=...
  python3 scripts/linear_webhook_server.py --port 8765

En Linear: New webhook → URL https://tu-dominio/webhook → resource Issues.
"""

from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import os
import re
import sys
import threading
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, os.path.join(PROJECT_ROOT, "src"))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "config"))
sys.path.insert(0, SCRIPT_DIR)

import automation as automation_config
from flask import Flask, request
from linear_api_client import LinearAPIClient

import run_linear_automation as rla


def _normalize_state(name: str) -> str:
    s = (name or "").replace("_", " ")
    return re.sub(r"\s+", " ", s.strip().lower())


def _state_matches(current: str, target: str) -> bool:
    return _normalize_state(current) == _normalize_state(target)


def _should_run_qa(payload: dict, target_state: str) -> bool:
    if payload.get("type") != "Issue":
        return False
    action = payload.get("action")
    data = payload.get("data") or {}
    state = data.get("state") or {}
    name = state.get("name") or ""
    if not _state_matches(name, target_state):
        return False
    if action == "create":
        return True
    if action == "update":
        uf = payload.get("updatedFrom") or {}
        if "stateId" not in uf:
            return False
        new_id = state.get("id")
        if uf.get("stateId") == new_id:
            return False
        return True
    return False


def _verify_signature(raw_body: bytes, sig_header: str, secret: str) -> bool:
    if not secret or not sig_header or not isinstance(sig_header, str):
        return False
    try:
        sig_header = sig_header.strip()
        expected = hmac.new(
            secret.encode("utf-8"), raw_body, hashlib.sha256
        ).digest()
        got = bytes.fromhex(sig_header)
        return hmac.compare_digest(expected, got)
    except (ValueError, TypeError):
        return False


def _run_qa_background(issue_uuid: str) -> None:
    """Hilo: generar casos para el issue."""
    try:
        api_key = automation_config.LINEAR_API_KEY
        if not api_key:
            print("[webhook] LINEAR_API_KEY no configurado", flush=True)
            return
        client = LinearAPIClient(api_key)
        issue = client.get_issue_summary_by_uuid(issue_uuid)
        if not issue:
            print("[webhook] Issue %s no encontrado" % issue_uuid[:8], flush=True)
            return
        if automation_config.WEBHOOK_SKIP_IF_CHILDREN:
            n = client.count_sub_issues(issue_uuid)
            if n > 0:
                print(
                    "[webhook] Omitido %s: ya tiene %d sub-issue(s)"
                    % (issue.identifier, n),
                    flush=True,
                )
                return
        print(
            "[webhook] Procesando %s (%s)" % (issue.identifier, issue.title[:50]),
            flush=True,
        )
        rla.process_linear_issue_for_qa(client, issue, verbose=False)
    except Exception as e:
        print("[webhook] Error: %s" % e, flush=True)
        import traceback

        traceback.print_exc()


def create_app() -> Flask:
    app = Flask(__name__)

    @app.route("/webhook", methods=["GET", "POST"])
    @app.route("/", methods=["GET", "POST"])
    def linear_webhook():
        if request.method == "GET":
            return {"status": "linear-qa-webhook", "ok": True}, 200

        raw = request.get_data()
        if not raw:
            return "", 400

        bypass = os.environ.get("LINEAR_WEBHOOK_SKIP_VERIFY", "").strip().lower() in (
            "1",
            "true",
            "yes",
        )
        secret = automation_config.LINEAR_WEBHOOK_SECRET
        if not bypass:
            if not secret:
                print("[webhook] Falta LINEAR_WEBHOOK_SECRET", flush=True)
                return "", 503
            sig = request.headers.get("Linear-Signature") or request.headers.get(
                "linear-signature"
            )
            if not _verify_signature(raw, sig or "", secret):
                return "", 401
            try:
                payload = json.loads(raw.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError):
                return "", 400
            ts = payload.get("webhookTimestamp")
            if ts is not None:
                if abs(time.time() * 1000 - float(ts)) > 120000:
                    return "", 401
        else:
            try:
                payload = json.loads(raw.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError):
                return "", 400

        target = automation_config.LINEAR_TARGET_STATE
        if not _should_run_qa(payload, target):
            return "", 200

        data = payload.get("data") or {}
        iid = data.get("id")
        if not iid:
            return "", 200

        threading.Thread(
            target=_run_qa_background, args=(str(iid),), daemon=True
        ).start()
        return "", 200

    return app


def main() -> None:
    parser = argparse.ArgumentParser(description="Webhook Linear → generación QA")
    parser.add_argument("--host", default=os.environ.get("LINEAR_WEBHOOK_HOST", "0.0.0.0"))
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.environ.get("LINEAR_WEBHOOK_PORT", "8765")),
    )
    args = parser.parse_args()
    print(
        "[INFO] Webhook QA | estado disparador: %r | http://%s:%s/webhook"
        % (automation_config.LINEAR_TARGET_STATE, args.host, args.port),
        flush=True,
    )
    if not automation_config.LINEAR_WEBHOOK_SECRET:
        print(
            "[WARN] LINEAR_WEBHOOK_SECRET vacío: define el secreto o "
            "LINEAR_WEBHOOK_SKIP_VERIFY=1 solo en desarrollo.",
            flush=True,
        )
    app = create_app()
    app.run(host=args.host, port=args.port, threaded=True)


if __name__ == "__main__":
    main()
