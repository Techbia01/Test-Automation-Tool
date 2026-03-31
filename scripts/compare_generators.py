#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comparación entre el motor de reglas (ProfessionalQAGenerator)
y el agente IA (ClaudeQAGenerator) para la generación de casos de prueba.

Uso:
  python3 scripts/compare_generators.py --issue ACQ-42
  python3 scripts/compare_generators.py --file mi_hu.txt
  python3 scripts/compare_generators.py --issue ACQ-42 --verbose

No sube nada a Linear; solo muestra los resultados en consola.
"""

import argparse
import os
import sys
from typing import List, Optional

# Raíz del proyecto
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, os.path.join(PROJECT_ROOT, "src"))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "config"))

import automation as automation_config
from linear_api_client import LinearAPIClient
from github_context import get_project_context_for_issue, get_pr_description_from_urls, resolve_github_repo_slug
from professional_qa_generator import ProfessionalQAGenerator, TestCase


# ---------------------------------------------------------------------------
# Helpers de presentación
# ---------------------------------------------------------------------------

def _exec_tag(tc: TestCase) -> str:
    return "[AUTO]" if tc.execution_suitability.value == "Automatizable" else "[MAN] "


def _type_counts(cases: List[TestCase]) -> str:
    from collections import Counter
    c = Counter(tc.test_type.value for tc in cases)
    return " | ".join(f"{k}: {v}" for k, v in sorted(c.items()))


def _exec_counts(cases: List[TestCase]) -> str:
    auto = sum(1 for tc in cases if tc.execution_suitability.value == "Automatizable")
    manual = len(cases) - auto
    return f"Auto: {auto} | Manual: {manual}"


def _truncate(text: str, max_len: int = 75) -> str:
    text = (text or "").replace("\n", " ").strip()
    return text[:max_len] + "…" if len(text) > max_len else text


def _print_cases_block(cases: List[TestCase], label: str, width: int = 72) -> None:
    print(f"\n{'=' * width}")
    print(f" {label} ({len(cases)} caso{'s' if len(cases) != 1 else ''})")
    print("=" * width)
    if not cases:
        print("  (sin casos generados)")
        return
    for tc in cases:
        print(f"\n  {_exec_tag(tc)} {tc.id} — {tc.title[:65]}")
        print(f"    Tipo: {tc.test_type.value} | Prioridad: {tc.priority.value}")
        exp = _truncate(tc.expected_result, 90)
        if exp:
            print(f"    → {exp}")
        hint = _truncate(tc.automation_hint, 80)
        if hint:
            print(f"    ({hint})")


def _print_comparison_summary(
    rules_cases: List[TestCase],
    claude_cases: List[TestCase],
) -> None:
    w = 72
    print(f"\n{'=' * w}")
    print(" RESUMEN COMPARATIVO")
    print(f"{'=' * w}")

    col_w = (w - 3) // 2
    header_r = f"{'MOTOR DE REGLAS':^{col_w}}"
    header_c = f"{'CLAUDE AI':^{col_w}}"
    print(f"|{header_r}|{header_c}|")
    print(f"|{'-' * col_w}|{'-' * col_w}|")

    rows = [
        ("Total casos", str(len(rules_cases)), str(len(claude_cases))),
        ("Tipos", _type_counts(rules_cases) or "-", _type_counts(claude_cases) or "-"),
        ("Ejecución", _exec_counts(rules_cases), _exec_counts(claude_cases)),
    ]
    for label, val_r, val_c in rows:
        cell_r = f"{label}: {val_r}"
        cell_c = f"{label}: {val_c}"
        print(f"| {cell_r:<{col_w - 2}} | {cell_c:<{col_w - 2}} |")

    print(f"{'=' * w}\n")


# ---------------------------------------------------------------------------
# Lógica de carga de HU
# ---------------------------------------------------------------------------

def _load_hu_from_file(path: str):
    """Carga texto HU desde un archivo .txt/.md."""
    with open(path, "r", encoding="utf-8") as f:
        text = f.read().strip()
    return text, os.path.splitext(os.path.basename(path))[0]


def _load_hu_from_linear(
    issue_identifier: str,
    verbose: bool = False,
):
    """Obtiene la HU y contexto GitHub desde Linear."""
    api_key = automation_config.LINEAR_API_KEY
    if not api_key:
        print("[ERROR] LINEAR_API_KEY no configurada.")
        sys.exit(1)

    client = LinearAPIClient(api_key)
    if not client.test_connection():
        print("[ERROR] No se pudo conectar con Linear.")
        sys.exit(1)

    # Obtener UUID por identificador público (ej: ACQ-42)
    uuid = client.get_issue_by_identifier(issue_identifier)
    if not uuid:
        print(f"[ERROR] Issue {issue_identifier} no encontrado en Linear.")
        sys.exit(1)

    issue = client.get_issue_summary_by_uuid(uuid)
    if issue is None:
        print(f"[ERROR] No se pudo cargar el issue {issue_identifier}.")
        sys.exit(1)

    user_story_text = (issue.description or "").strip()

    # Fallback: si la descripción está vacía, intentar usar el body del PR adjunto
    if not user_story_text and git_ctx.attachment_urls:
        pr_text = get_pr_description_from_urls(
            git_ctx.attachment_urls, token=automation_config.GITHUB_TOKEN
        )
        if pr_text:
            print(f"[INFO] Descripción vacía; usando body del PR adjunto como HU.")
            user_story_text = pr_text

    if not user_story_text:
        print(f"[ERROR] El issue {issue_identifier} no tiene descripción ni PR con contenido.")
        sys.exit(1)

    # Contexto GitHub
    git_ctx = client.get_issue_git_context(issue.id)
    team_key = issue.identifier.split("-", 1)[0].upper() if "-" in issue.identifier else None
    project_context = get_project_context_for_issue(
        issue.description,
        default_repo=automation_config.GITHUB_DEFAULT_REPO,
        token=automation_config.GITHUB_TOKEN,
        attachment_urls=git_ctx.attachment_urls,
        linear_branch_name=(git_ctx.branch_name or "").strip() or None,
        linear_team_key=team_key,
        team_key_to_repo=automation_config.GITHUB_TEAM_REPOS or None,
    )

    if verbose:
        print(f"[INFO] Issue cargado: {issue.identifier} — {issue.title}")
        resolved = resolve_github_repo_slug(
            git_ctx.attachment_urls,
            issue.description or "",
            automation_config.GITHUB_DEFAULT_REPO,
            linear_team_key=team_key,
            team_key_to_repo=automation_config.GITHUB_TEAM_REPOS or None,
        )
        print(f"[INFO] Repo resuelto: {resolved or '(ninguno)'}")

    return user_story_text, issue.title, project_context


# ---------------------------------------------------------------------------
# Runner principal
# ---------------------------------------------------------------------------

def run(
    issue: Optional[str] = None,
    file: Optional[str] = None,
    verbose: bool = False,
) -> None:
    # ── 1. Cargar HU ────────────────────────────────────────────────────────
    project_context: Optional[str] = None

    if file:
        user_story_text, project_name = _load_hu_from_file(file)
        print(f"[INFO] HU cargada desde archivo: {file}")
    elif issue:
        user_story_text, project_name, project_context = _load_hu_from_linear(
            issue, verbose
        )
    else:
        print("[ERROR] Debes especificar --issue o --file.")
        sys.exit(1)

    print(f"\n[INFO] Proyecto: {project_name}")
    print(f"[INFO] HU ({len(user_story_text)} chars) | Contexto GitHub: {'sí' if project_context else 'no'}")

    # ── 2. Motor de reglas ──────────────────────────────────────────────────
    print("\n[1/2] Ejecutando MOTOR DE REGLAS...")
    rules_gen = ProfessionalQAGenerator()
    rules_gen._qa_generation_verbose = verbose
    try:
        rules_cases = rules_gen.generate_test_cases(
            user_story_text=user_story_text,
            project_name=project_name,
            project_context=project_context,
            verbose_log=verbose,
        )
    except Exception as e:
        print(f"[ERROR] Motor de reglas falló: {e}")
        rules_cases = []

    # ── 3. Claude AI ────────────────────────────────────────────────────────
    print("\n[2/2] Ejecutando CLAUDE AI...")
    try:
        from claude_qa_generator import ClaudeQAGenerator
        claude_gen = ClaudeQAGenerator(
            api_key=automation_config.ANTHROPIC_API_KEY
        )
        claude_cases = claude_gen.generate_test_cases(
            user_story_text=user_story_text,
            project_name=project_name,
            project_context=project_context,
            verbose_log=verbose,
        )
    except ImportError as e:
        print(f"[ERROR] No se pudo importar ClaudeQAGenerator: {e}")
        claude_cases = []
    except ValueError as e:
        print(f"[ERROR] {e}")
        claude_cases = []
    except Exception as e:
        print(f"[ERROR] Claude AI falló: {e}")
        claude_cases = []

    # ── 4. Mostrar resultados ───────────────────────────────────────────────
    _print_cases_block(rules_cases, "MOTOR DE REGLAS")
    _print_cases_block(claude_cases, "CLAUDE AI")
    _print_comparison_summary(rules_cases, claude_cases)


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Comparar motor de reglas vs Claude AI para generación de casos de prueba"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--issue",
        metavar="ID",
        help="Identificador de issue en Linear (ej: ACQ-42)",
    )
    group.add_argument(
        "--file",
        metavar="PATH",
        help="Ruta a un archivo .txt o .md con el texto de la HU",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Mostrar contexto detallado y logs de extracción",
    )
    args = parser.parse_args()
    run(issue=args.issue, file=args.file, verbose=args.verbose)
