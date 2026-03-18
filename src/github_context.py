#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo para obtener contexto de repositorios GitHub (README, estructura)
y extraer URL de repo desde la descripción de un issue de Linear.
"""

import os
import re
import base64
import requests
from typing import Optional

GITHUB_API_BASE = "https://api.github.com"


def extract_github_repo_from_text(text: str) -> Optional[str]:
    """
    Extrae la primera URL de repositorio GitHub encontrada en el texto.
    Acepta: https://github.com/owner/repo, http://github.com/owner/repo,
    github.com/owner/repo. Devuelve 'owner/repo' o None.
    """
    if not text or not text.strip():
        return None
    # URL completa o solo dominio + path (sin / al final, sin # o ?)
    pattern = r"(?:https?://)?(?:www\.)?github\.com/([a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+)(?:/)?(?:\s|$|[#?)])"
    m = re.search(pattern, text, re.IGNORECASE)
    if m:
        return m.group(1).rstrip("/")
    return None


def _parse_repo_spec(repo_url_or_slug: str) -> Optional[tuple]:
    """Convierte 'owner/repo' o URL a (owner, repo)."""
    if not repo_url_or_slug or not repo_url_or_slug.strip():
        return None
    s = repo_url_or_slug.strip()
    m = re.search(r"github\.com/([a-zA-Z0-9_.-]+)/([a-zA-Z0-9_.-]+)", s, re.IGNORECASE)
    if m:
        return (m.group(1), m.group(2))
    if "/" in s and " " not in s:
        parts = s.split("/", 1)
        if len(parts) == 2 and parts[0] and parts[1]:
            return (parts[0], parts[1])
    return None


def fetch_repo_context(
    repo_url_or_slug: str,
    token: Optional[str] = None,
    include_structure: bool = True,
    max_structure_depth: int = 1,
) -> str:
    """
    Obtiene contexto del repositorio: contenido del README y opcionalmente
    resumen de estructura de directorios.
    repo_url_or_slug: 'owner/repo' o URL completa de GitHub.
    token: GITHUB_TOKEN para repos privados y mayor rate limit.
    include_structure: si True, añade lista de archivos/carpetas en la raíz.
    max_structure_depth: profundidad para listar (1 = solo raíz).
    Devuelve un string listo para inyectar como project_context.
    """
    parsed = _parse_repo_spec(repo_url_or_slug)
    if not parsed:
        return ""
    owner, repo = parsed

    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"token {token}"

    parts = []

    # README
    try:
        r = requests.get(
            f"{GITHUB_API_BASE}/repos/{owner}/{repo}/readme",
            headers=headers,
            timeout=15,
        )
        if r.status_code == 200:
            data = r.json()
            content_b64 = data.get("content")
            if content_b64:
                try:
                    content = base64.b64decode(content_b64).decode("utf-8", errors="replace")
                    parts.append(f"## README\n\n{content}")
                except Exception:
                    pass
    except requests.RequestException:
        pass

    if include_structure and max_structure_depth >= 1:
        try:
            r = requests.get(
                f"{GITHUB_API_BASE}/repos/{owner}/{repo}/contents",
                headers=headers,
                timeout=15,
            )
            if r.status_code == 200:
                items = r.json()
                if isinstance(items, list):
                    names = [x.get("name", "") for x in items if x.get("name")]
                    if names:
                        parts.append("## Estructura (raíz)\n\n" + ", ".join(sorted(names)))
        except requests.RequestException:
            pass

    if not parts:
        return ""
    return "\n\n---\n\n".join(parts)


def get_project_context_for_issue(
    issue_description: str,
    default_repo: Optional[str] = None,
    token: Optional[str] = None,
) -> str:
    """
    Determina el repo a usar (override desde issue o default) y devuelve
    el contexto de proyecto desde GitHub.
    """
    repo = extract_github_repo_from_text(issue_description or "") if issue_description else None
    if not repo:
        repo = default_repo
    if not repo:
        return ""
    parsed = _parse_repo_spec(repo)
    if not parsed:
        return ""
    return fetch_repo_context(repo, token=token, include_structure=True)
