#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo para obtener contexto de repositorios GitHub (README, estructura)
y resolver owner/repo desde descripción de Linear, adjuntos (PR/rama) o repo por defecto.
"""

import re
import base64
import requests
from typing import Dict, List, Optional

GITHUB_API_BASE = "https://api.github.com"


def _normalize_github_token(token: Optional[str]) -> Optional[str]:
    """Quita espacios y comillas típicas del .env."""
    if not token:
        return None
    t = str(token).strip()
    if (t.startswith('"') and t.endswith('"')) or (t.startswith("'") and t.endswith("'")):
        t = t[1:-1].strip()
    return t or None


def _github_authorization_header(token: str) -> str:
    """Fine-grained (github_pat_*) exige Bearer; classic (ghp_*) usa token."""
    t = _normalize_github_token(token) or ""
    if t.startswith("github_pat_"):
        return f"Bearer {t}"
    return f"token {t}"


def _readme_ref_candidates(git_ref: Optional[str]) -> List[str]:
    """Ramas con / en el nombre a veces responden mejor con prefijo heads/."""
    r = (git_ref or "").strip()
    if not r:
        return []
    out = [r]
    if "/" in r and not r.startswith("refs/"):
        full = f"heads/{r}"
        if full not in out:
            out.append(full)
    return out


def github_url_to_owner_repo(url: str) -> Optional[str]:
    """
    Extrae 'owner/repo' desde una URL de GitHub (repo, PR, rama, blob, compare, issues).
    """
    if not url or not url.strip():
        return None
    u = url.strip()
    # Normalizar
    m = re.search(
        r"github\.com/([a-zA-Z0-9_.-]+)/([a-zA-Z0-9_.-]+)(?:/|$|\?|#)",
        u,
        re.IGNORECASE,
    )
    if m:
        return f"{m.group(1)}/{m.group(2)}"
    return None


def extract_github_repo_from_urls(urls: List[str]) -> Optional[str]:
    """
    Elige owner/repo a partir de una lista de URLs (adjuntos Linear, etc.).
    Prioridad: PR > rama (tree) > enlace genérico al repo.
    """
    if not urls:
        return None
    pull_pairs: List[str] = []
    tree_pairs: List[str] = []
    other_pairs: List[str] = []
    for u in urls:
        if not u or "github.com" not in u.lower():
            continue
        slug = github_url_to_owner_repo(u)
        if not slug:
            continue
        ul = u.lower()
        if "/pull/" in ul:
            pull_pairs.append(slug)
        elif "/tree/" in ul:
            tree_pairs.append(slug)
        else:
            other_pairs.append(slug)
    if pull_pairs:
        return pull_pairs[0]
    if tree_pairs:
        return tree_pairs[0]
    if other_pairs:
        return other_pairs[0]
    return None


def _collect_github_urls_from_text(text: str) -> List[str]:
    """Encuentra URLs de GitHub en texto libre."""
    if not text or not text.strip():
        return []
    urls = set()
    for m in re.finditer(
        r"https?://(?:www\.)?github\.com/[a-zA-Z0-9_.\-/]+",
        text,
        re.IGNORECASE,
    ):
        urls.add(m.group(0).rstrip(").,;]"))
    return list(urls)


def extract_github_repo_from_text(text: str) -> Optional[str]:
    """
    Extrae owner/repo desde texto (descripción del issue).
    Incluye URLs de PR, tree/branch y repo simple.
    """
    if not text or not text.strip():
        return None
    found = _collect_github_urls_from_text(text)
    if found:
        return extract_github_repo_from_urls(found)
    # Sin esquema: github.com/owner/repo
    pattern = (
        r"(?:https?://)?(?:www\.)?github\.com/"
        r"([a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+)(?:/pull/|/tree/|/blob/|/compare/|/)?"
    )
    m = re.search(pattern, text, re.IGNORECASE)
    if m:
        return m.group(1).rstrip("/")
    return None


def resolve_github_repo_slug(
    attachment_urls: List[str],
    issue_description: str,
    default_repo: Optional[str],
    linear_team_key: Optional[str] = None,
    team_key_to_repo: Optional[Dict[str, str]] = None,
) -> Optional[str]:
    """
    Orden: adjuntos (PR) > descripción > repo por equipo Linear > GITHUB_DEFAULT_REPO.

    linear_team_key: prefijo del identificador (ej. FIN en FIN-123), suele coincidir
    con la clave del equipo en Linear. team_key_to_repo: mapa clave -> owner/repo.
    """
    repo = extract_github_repo_from_urls(attachment_urls or [])
    if repo:
        return repo
    repo = extract_github_repo_from_text(issue_description or "")
    if repo:
        return repo
    if team_key_to_repo and linear_team_key:
        key = str(linear_team_key).strip().upper()
        mapped = team_key_to_repo.get(key)
        if mapped:
            parsed = _parse_repo_spec(mapped)
            if parsed:
                return f"{parsed[0]}/{parsed[1]}"
    if default_repo and str(default_repo).strip():
        dr = str(default_repo).strip()
        parsed = _parse_repo_spec(dr)
        if parsed:
            return f"{parsed[0]}/{parsed[1]}"
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


def fetch_readme_markdown(
    repo_url_or_slug: str,
    token: Optional[str] = None,
    git_ref: Optional[str] = None,
) -> str:
    """
    Devuelve solo el texto del README del repositorio (markdown decodificado).
    git_ref: rama o tag; si la rama no tiene README, intenta la rama por defecto.
    """
    parsed = _parse_repo_spec(repo_url_or_slug)
    if not parsed:
        return ""
    owner, repo = parsed
    tok = _normalize_github_token(token)

    def _decode(resp) -> str:
        if resp.status_code != 200:
            return ""
        data = resp.json()
        b64 = data.get("content")
        if not b64:
            return ""
        try:
            return base64.b64decode(b64).decode("utf-8", errors="replace")
        except Exception:
            return ""

    auth_attempts = []
    if tok:
        auth_attempts.append(_github_authorization_header(tok))
        if tok.startswith("github_pat_"):
            pass
        else:
            alt = f"Bearer {tok}"
            if alt not in auth_attempts:
                auth_attempts.append(alt)

    def _headers(auth: Optional[str]) -> dict:
        h = {"Accept": "application/vnd.github.v3+json"}
        if auth:
            h["Authorization"] = auth
        return h

    ref_list = _readme_ref_candidates(git_ref) if git_ref and git_ref.strip() else [None]

    try:
        for auth in auth_attempts or [None]:
            headers = _headers(auth)
            for ref in ref_list:
                params = {"ref": ref} if ref else None
                r = requests.get(
                    f"{GITHUB_API_BASE}/repos/{owner}/{repo}/readme",
                    headers=headers,
                    params=params,
                    timeout=20,
                )
                text = _decode(r)
                if text:
                    return text
            if git_ref and git_ref.strip():
                r0 = requests.get(
                    f"{GITHUB_API_BASE}/repos/{owner}/{repo}/readme",
                    headers=headers,
                    timeout=20,
                )
                t0 = _decode(r0)
                if t0:
                    return t0
    except requests.RequestException:
        pass
    return ""


def github_repo_and_readme_diagnostic(
    repo_url_or_slug: str,
    token: Optional[str] = None,
    git_ref: Optional[str] = None,
) -> List[str]:
    """
    Líneas de texto para depuración (sin exponer el token).
    """
    lines: List[str] = []
    parsed = _parse_repo_spec(repo_url_or_slug)
    if not parsed:
        lines.append("owner/repo no válido")
        return lines
    owner, repo_name = parsed
    tok = _normalize_github_token(token)
    lines.append(
        "GITHUB_TOKEN: %s (%d caracteres)"
        % ("cargado" if tok else "NO cargado (revisa .env en la raíz del proyecto)", len(tok or ""))
    )
    h = {"Accept": "application/vnd.github.v3+json"}
    if tok:
        h["Authorization"] = _github_authorization_header(tok)
    try:
        r = requests.get(
            f"{GITHUB_API_BASE}/repos/{owner}/{repo_name}",
            headers=h,
            timeout=15,
        )
        try:
            j = r.json()
            msg = (j.get("message") or "")[:200]
        except Exception:
            msg = r.text[:200]
        lines.append("GET /repos/%s/%s -> HTTP %s" % (owner, repo_name, r.status_code))
        if msg and r.status_code != 200:
            lines.append("  GitHub: %s" % msg)
        if r.status_code == 403 and "sso" in (msg or "").lower():
            lines.append(
                "  -> Autoriza el token para la org: GitHub -> Settings -> "
                "Applications -> tu token -> Configure SSO -> Authorize"
            )
    except requests.RequestException as e:
        lines.append("Error red: %s" % e)

    if git_ref and git_ref.strip():
        for cand in _readme_ref_candidates(git_ref):
            try:
                r2 = requests.get(
                    f"{GITHUB_API_BASE}/repos/{owner}/{repo_name}/readme",
                    headers=h,
                    params={"ref": cand},
                    timeout=15,
                )
                ok = r2.status_code == 200 and bool(
                    (r2.json() or {}).get("content")
                )
                lines.append(
                    "README ref=%r -> HTTP %s %s"
                    % (cand, r2.status_code, "OK" if ok else "")
                )
                if r2.status_code != 200:
                    try:
                        lines.append(
                            "  %s"
                            % ((r2.json() or {}).get("message") or "")[:150]
                        )
                    except Exception:
                        pass
            except requests.RequestException as e:
                lines.append("README ref=%r error: %s" % (cand, e))
    return lines


def fetch_repo_context(
    repo_url_or_slug: str,
    token: Optional[str] = None,
    include_structure: bool = True,
    max_structure_depth: int = 1,
    git_ref: Optional[str] = None,
) -> str:
    """
    Obtiene contexto del repositorio: README y opcionalmente estructura en raíz.
    git_ref: rama o tag de GitHub (mismo nombre que en Linear branchName);
             si se indica, README y contents se piden con ?ref=.
    """
    parsed = _parse_repo_spec(repo_url_or_slug)
    if not parsed:
        return ""
    owner, repo = parsed

    headers = {"Accept": "application/vnd.github.v3+json"}
    tok = _normalize_github_token(token)
    if tok:
        headers["Authorization"] = _github_authorization_header(tok)

    ref_opts: List[Optional[str]] = (
        _readme_ref_candidates(git_ref) if git_ref and git_ref.strip() else [None]
    )

    parts: List[str] = []

    def _readme_once(params_req: Optional[dict]) -> Optional[str]:
        try:
            r = requests.get(
                f"{GITHUB_API_BASE}/repos/{owner}/{repo}/readme",
                headers=headers,
                params=params_req,
                timeout=20,
            )
            if r.status_code != 200:
                return None
            data = r.json()
            b64 = data.get("content")
            if not b64:
                return None
            return base64.b64decode(b64).decode("utf-8", errors="replace")
        except (requests.RequestException, ValueError, TypeError, KeyError):
            return None

    try:
        got: Optional[str] = None
        for ref in ref_opts:
            prm = {"ref": ref} if ref else None
            got = _readme_once(prm)
            if got:
                break
        used_default = False
        if not got and git_ref and git_ref.strip():
            got = _readme_once(None)
            used_default = bool(got)
        if got:
            if used_default:
                parts.append(
                    "## README (rama por defecto; la rama vinculada "
                    "no tiene README en la raíz)\n\n" + got
                )
            elif git_ref and git_ref.strip():
                parts.append(f"## README (rama `{git_ref}`)\n\n{got}")
            else:
                parts.append("## README\n\n" + got)
    except requests.RequestException:
        pass

    if include_structure and max_structure_depth >= 1:
        try:
            cparams = None
            if git_ref and git_ref.strip():
                for ref in ref_opts:
                    if ref:
                        cparams = {"ref": ref}
                        break
                if not cparams:
                    cparams = {"ref": git_ref.strip()}
            r = requests.get(
                f"{GITHUB_API_BASE}/repos/{owner}/{repo}/contents",
                headers=headers,
                params=cparams,
                timeout=15,
            )
            if r.status_code == 200:
                items = r.json()
                if isinstance(items, list):
                    names = [x.get("name", "") for x in items if x.get("name")]
                    if names:
                        lbl = f"rama `{git_ref}`" if git_ref else "raíz"
                        parts.append(
                            f"## Estructura ({lbl})\n\n"
                            + ", ".join(sorted(names))
                        )
        except requests.RequestException:
            pass

    if not parts:
        return ""
    return "\n\n---\n\n".join(parts)


def _extract_pr_number_from_url(url: str) -> Optional[int]:
    """Extrae el número de PR de una URL de GitHub (…/pull/123)."""
    m = re.search(r"/pull/(\d+)", url or "", re.IGNORECASE)
    return int(m.group(1)) if m else None


def get_pr_description_from_url(
    pr_url: str,
    token: Optional[str] = None,
) -> Optional[str]:
    """
    Consulta la API de GitHub para obtener título + body de un PR.
    Retorna un texto formateado listo para usarse como user_story_text,
    o None si el PR no tiene body o no se puede acceder.
    """
    slug = github_url_to_owner_repo(pr_url)
    pr_number = _extract_pr_number_from_url(pr_url)
    if not slug or not pr_number:
        return None

    url = f"{GITHUB_API_BASE}/repos/{slug}/pulls/{pr_number}"
    headers = {"Accept": "application/vnd.github+json"}
    clean_token = _normalize_github_token(token)
    if clean_token:
        headers["Authorization"] = _github_authorization_header(clean_token)

    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code != 200:
            return None
        data = resp.json()
        title = (data.get("title") or "").strip()
        body = (data.get("body") or "").strip()
        if not title and not body:
            return None
        parts = []
        if title:
            parts.append(f"**PR:** {title}")
        if body:
            parts.append(body)
        return "\n\n".join(parts)
    except Exception:
        return None


def get_pr_description_from_urls(
    urls: List[str],
    token: Optional[str] = None,
) -> Optional[str]:
    """
    Recorre una lista de URLs y retorna la descripción del primer PR
    de GitHub que tenga contenido.
    """
    for url in (urls or []):
        if "github.com" in (url or "").lower() and "/pull/" in url.lower():
            desc = get_pr_description_from_url(url, token=token)
            if desc:
                return desc
    return None


def get_project_context_for_issue(
    issue_description: str,
    default_repo: Optional[str] = None,
    token: Optional[str] = None,
    attachment_urls: Optional[List[str]] = None,
    linear_branch_name: Optional[str] = None,
    linear_team_key: Optional[str] = None,
    team_key_to_repo: Optional[Dict[str, str]] = None,
) -> str:
    """
    Resuelve el repo (adjuntos > descripción > default) y añade la rama
    que Linear expone en branchName (integración GitHub).
    """
    parts: List[str] = []
    branch = (linear_branch_name or "").strip()

    if branch:
        parts.append(
            "## Rama de Git vinculada al issue en Linear\n\n"
            f"Nombre de rama: `{branch}`\n\n"
            "Los cambios de esta historia se desarrollan en esta rama; "
            "alinea los casos de prueba con lo que exista en ella.\n"
        )

    repo = resolve_github_repo_slug(
        attachment_urls or [],
        issue_description or "",
        default_repo,
        linear_team_key=linear_team_key,
        team_key_to_repo=team_key_to_repo,
    )

    if repo:
        ctx = fetch_repo_context(
            repo,
            token=token,
            include_structure=True,
            git_ref=branch if branch else None,
        )
        if ctx:
            parts.append(ctx)

    if not parts:
        return ""
    return "\n\n---\n\n".join(parts)
