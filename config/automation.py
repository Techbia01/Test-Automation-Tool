#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuración para la automatización Linear + GitHub.
Carga variables desde .env (recomendado para seguridad) y luego automation_config.json.
Las variables de entorno tienen prioridad sobre el JSON.
"""

import os
import json
from typing import Dict, List, Optional

# Cargar .env desde la raíz del proyecto (no subir .env a Git; usar .env.example como plantilla)
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_env_path = os.path.join(_PROJECT_ROOT, ".env")
if os.path.exists(_env_path):
    try:
        from dotenv import load_dotenv
        load_dotenv(_env_path)
    except ImportError:
        pass  # python-dotenv opcional; sin él solo se usan env vars ya definidas

# Ruta al archivo JSON opcional de automatización (en raíz del proyecto)
_AUTOMATION_JSON = os.path.join(_PROJECT_ROOT, "automation_config.json")


def _get_env(key: str, default: Optional[str] = None) -> Optional[str]:
    """Valor de variable de entorno (prioridad)."""
    return os.environ.get(key) or default


def _load_json_config() -> dict:
    """Carga automation_config.json si existe."""
    if os.path.exists(_AUTOMATION_JSON):
        try:
            with open(_AUTOMATION_JSON, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            pass
    return {}


_json = _load_json_config()


# --- Linear ---
LINEAR_API_KEY: Optional[str] = _get_env("LINEAR_API_KEY") or _json.get("linear_api_key")
"""API Key de Linear. Requerido para el flujo automático."""

LINEAR_TARGET_STATE: str = (
    _get_env("LINEAR_TARGET_STATE")
    or _json.get("linear_target_state")
    or "TC Generator"
)
"""Estado en Linear en el que deben estar las historias para generar casos (ej: TC Generator)."""

LINEAR_STATE_AFTER_SUCCESS: Optional[str] = (
    _get_env("LINEAR_STATE_AFTER_SUCCESS")
    or _json.get("linear_state_after_success")
)
"""Estado al que mover el issue tras generar casos (ej: Ready for QA). None = no cambiar."""

def _parse_team_ids() -> List[str]:
    raw = _get_env("LINEAR_TEAM_IDS") or _json.get("linear_team_ids")
    if raw is None:
        return []
    if isinstance(raw, list):
        return [str(x) for x in raw]
    return [x.strip() for x in str(raw).split(",") if x.strip()]


LINEAR_TEAM_IDS: List[str] = _parse_team_ids()
"""Lista de IDs de equipo para filtrar. Vacío = intentar todos los equipos."""


def _parse_github_team_repos() -> Dict[str, str]:
    """
    Prefijo de equipo Linear (clave del equipo, ej. FIN en FIN-123) -> owner/repo.
    No se puede inferir el repo solo con el nombre de rama; varios equipos = varios repos.
    """
    raw = _json.get("github_team_repos")
    if isinstance(raw, dict):
        return {
            str(k).strip().upper(): str(v).strip()
            for k, v in raw.items()
            if k and v
        }
    env = _get_env("GITHUB_TEAM_REPOS")
    if env:
        try:
            d = json.loads(env)
            if isinstance(d, dict):
                return {
                    str(k).strip().upper(): str(v).strip()
                    for k, v in d.items()
                    if k and v
                }
        except json.JSONDecodeError:
            pass
    return {}


GITHUB_TEAM_REPOS: Dict[str, str] = _parse_github_team_repos()
"""Mapa clave de equipo Linear -> repo GitHub (ej. FIN -> mi-org/app-finanzas)."""

GITHUB_DEFAULT_REPO: Optional[str] = (
    _get_env("GITHUB_DEFAULT_REPO") or _json.get("github_default_repo")
)
"""Repo por defecto si no hay URL en el issue ni entrada en github_team_repos."""

GITHUB_TOKEN: Optional[str] = _get_env("GITHUB_TOKEN") or _json.get("github_token")
"""Token de GitHub para repos privados y mayor rate limit. Opcional."""

def _optional_label(env_key: str, json_key: str) -> Optional[str]:
    raw = _get_env(env_key) or _json.get(json_key)
    if raw is None:
        return None
    s = str(raw).strip()
    return s or None


LINEAR_LABEL_MANUAL_TEST: Optional[str] = _optional_label(
    "LINEAR_LABEL_MANUAL_TEST", "linear_label_manual_test"
)
LINEAR_LABEL_AUTOMATABLE: Optional[str] = _optional_label(
    "LINEAR_LABEL_AUTOMATABLE", "linear_label_automatizable"
)
"""
Nombres de etiqueta para ejecución manual / automatizable.
Si no se definen, Linear API usa por defecto «Manual» y «Automatizable»
(creación automática en el equipo si no existen).
"""

LINEAR_WEBHOOK_SECRET: Optional[str] = _get_env("LINEAR_WEBHOOK_SECRET") or _json.get(
    "linear_webhook_secret"
)
"""Secreto de firma del webhook (Linear → Settings → API → webhook)."""

_ws_raw = _get_env("WEBHOOK_SKIP_IF_CHILDREN")
if _ws_raw is not None and str(_ws_raw).strip() != "":
    WEBHOOK_SKIP_IF_CHILDREN = str(_ws_raw).strip().lower() in ("1", "true", "yes")
elif "webhook_skip_if_children" in _json:
    _wv = _json.get("webhook_skip_if_children")
    WEBHOOK_SKIP_IF_CHILDREN = (
        bool(_wv) if isinstance(_wv, bool) else str(_wv).lower() in ("1", "true", "yes")
    )
else:
    WEBHOOK_SKIP_IF_CHILDREN = True
"""Si el padre ya tiene sub-issues, no reprocesar (evita duplicados al re-disparar)."""
