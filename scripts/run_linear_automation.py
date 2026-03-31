#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de automatización: lee historias de Linear en un estado configurado,
genera casos de prueba (con contexto opcional de GitHub) y los sube como sub-issues.

Por defecto (ejecución real): solo repo, código del issue, título y listado de casos.
Con --verbose o AUTOMATION_VERBOSE=1: vuelca contexto Linear/GitHub completo.

Ejecutar desde la raíz del proyecto: python3 scripts/run_linear_automation.py
"""

import argparse
import os
import re
import sys

# Raíz del proyecto
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, os.path.join(PROJECT_ROOT, "src"))

# Config de automatización (env + automation_config.json)
sys.path.insert(0, os.path.join(PROJECT_ROOT, "config"))
import automation as automation_config

from linear_api_client import LinearAPIClient, LinearIssueSummary
from github_context import (
    extract_github_repo_from_text,
    extract_github_repo_from_urls,
    get_project_context_for_issue,
    resolve_github_repo_slug,
)

# Límite por bloque para no saturar la terminal (ajustable)
_MAX_CONTEXT_CHARS = 30000
from improved_test_generator import ImprovedTestGenerator, ImprovedTestCase


def _format_improved_description(tc: ImprovedTestCase) -> str:
    """Formatea un ImprovedTestCase con la estructura de plantilla acordada."""
    is_auto = "@automatizable" in tc.tags
    exec_label = "Automatizable" if is_auto else "Manual"

    # Criterio original (línea de la historia de usuario)
    criterio_raw = re.sub(r'^(?:Criterio\s+\d+:|Scenario:)\s*', '', tc.scenario or "").strip()
    if not criterio_raw:
        criterio_raw = tc.title

    # Precondiciones fijas + específicas del caso
    base_prec = [
        "El sistema está operativo y accesible",
        "El usuario tiene los permisos necesarios",
        "Los datos de prueba están disponibles",
    ]
    extra_prec = [p for p in (tc.preconditions or []) if p not in base_prec]
    prec_lines = "\n".join(f"- {p}" for p in base_prec + extra_prec)

    # Pasos Gherkin
    given_str = "\nAnd ".join(tc.given_steps) if tc.given_steps else "el usuario accede al módulo correspondiente"
    when_str  = "\nAnd ".join(tc.when_steps)  if tc.when_steps  else "el usuario ejecuta la acción"
    then_str  = "\nAnd ".join(tc.then_steps)  if tc.then_steps  else "el sistema responde correctamente"

    # Resultado esperado como prosa
    resultado = ". ".join(s.rstrip(".") for s in (tc.then_steps or []))
    resultado = f"{resultado}. No se presentan errores en el proceso. La interfaz responde correctamente."

    return (
        f"Ejecución sugerida: {exec_label}\n"
        f"Nota:\n\n"
        f"Objetivo: {tc.title}\n"
        f"Criterio de aceptación: {criterio_raw}\n\n"
        f"Tipo: {tc.test_type.capitalize()}\n"
        f"Prioridad: {tc.priority.capitalize()}\n\n"
        f"Precondiciones:\n{prec_lines}\n\n"
        f"Pasos (lenguaje Gherkin):\n\n"
        f"Given que {given_str}\n"
        f"When {when_str}\n"
        f"Then {then_str}\n\n"
        f"Resultado Esperado:\n{resultado}"
    )


def _convert_improved_to_serializable(cases: list, project_name: str) -> list:
    """Convierte ImprovedTestCase al formato dict esperado por LinearAPIClient."""
    result = []
    for tc in cases:
        is_auto = "@automatizable" in tc.tags
        result.append({
            "test_case_id": tc.id,
            "title": tc.title,
            "description": _format_improved_description(tc),
            "linear_description_is_complete": True,
            "preconditions": tc.given_steps,
            "steps": tc.when_steps,
            "expected_result": "\n".join(tc.then_steps),
            "priority": tc.priority.capitalize(),
            "type": tc.test_type.capitalize(),
            "execution_suitability": "Automatizable" if is_auto else "Manual",
            "automation_hint": "",
        })
    return result


def _trunc_block(text: str, limit: int = _MAX_CONTEXT_CHARS) -> str:
    if not text:
        return "(vacío)"
    if len(text) <= limit:
        return text
    return text[:limit] + "\n\n... [truncado, total %d caracteres]\n" % len(text)


def _repo_origin_label(
    attachment_urls,
    description,
    team_key,
    team_repos,
    default_repo,
    resolved_slug,
) -> str:
    if extract_github_repo_from_urls(attachment_urls or []):
        return "adjuntos Linear (PR/enlace GitHub)"
    if extract_github_repo_from_text(description or ""):
        return "URL en descripción del issue"
    if team_key and (team_repos or {}).get(team_key or ""):
        return "github_team_repos[%s]" % team_key
    if default_repo and str(default_repo).strip():
        return "GITHUB_DEFAULT_REPO"
    if resolved_slug:
        return "resuelto"
    return "no determinado"


def _exec_tag(tc) -> str:
    if "@automatizable" in getattr(tc, "tags", []):
        return "[AUTO]"
    return "[MANUAL]"


def process_linear_issue_for_qa(
    client: LinearAPIClient,
    issue: LinearIssueSummary,
    verbose: bool = False,
) -> str:
    """
    Genera y sube casos de prueba para un issue. Retorno:
    processed | skipped_no_description | skipped_no_cases |
    error_generation | error_upload
    """
    assert isinstance(issue, LinearIssueSummary)
    if verbose:
        print("\n" + "-" * 60)
        print(
            "[INFO] Procesando: %s - %s"
            % (issue.identifier, issue.title[:50])
        )

    default_repo = automation_config.GITHUB_DEFAULT_REPO
    gh_token = automation_config.GITHUB_TOKEN
    team_repos = automation_config.GITHUB_TEAM_REPOS or {}
    state_after = automation_config.LINEAR_STATE_AFTER_SUCCESS

    user_story_text = (issue.description or "").strip()
    if not user_story_text:
        print("[WARN] Issue sin descripción; se omite.")
        return "skipped_no_description"

    git_ctx = client.get_issue_git_context(issue.id)
    attachment_urls = git_ctx.attachment_urls
    branch_name = (git_ctx.branch_name or "").strip()

    team_key = None
    if issue.identifier and "-" in issue.identifier:
        team_key = issue.identifier.split("-", 1)[0].strip().upper()

    project_context = get_project_context_for_issue(
        issue.description,
        default_repo=default_repo,
        token=gh_token,
        attachment_urls=attachment_urls,
        linear_branch_name=branch_name or None,
        linear_team_key=team_key,
        team_key_to_repo=team_repos if team_repos else None,
    )
    resolved_repo = resolve_github_repo_slug(
        attachment_urls,
        issue.description or "",
        default_repo,
        linear_team_key=team_key,
        team_key_to_repo=team_repos if team_repos else None,
    )
    origin = _repo_origin_label(
        attachment_urls,
        issue.description,
        team_key,
        team_repos,
        default_repo,
        resolved_repo,
    )

    if verbose:
        print("\n" + "=" * 72)
        print(" CONTEXTO LINEAR — %s" % issue.identifier)
        print("=" * 72)
        print("Título: %s" % issue.title)
        print("Estado (al listar): %s" % issue.state)
        print("Equipo (team_id): %s" % issue.team_id)
        print("Rama (branchName): %s" % (branch_name or "(sin rama)"))
        print("Origen repo GitHub: %s" % origin)
        print("Repo resuelto: %s" % (resolved_repo or "(ninguno)"))
        print("Rama usada en API GitHub: %s" % (branch_name or "(default)"))
        print("-" * 72)
        print("Adjuntos (%d):" % len(attachment_urls))
        for u in attachment_urls:
            short = u[:120] + ("..." if len(u) > 120 else "")
            print("  • %s" % short)
        if not attachment_urls:
            print("  (ninguno)")
        print("-" * 72)
        print("Descripción / historia de usuario:")
        print(_trunc_block(user_story_text, _MAX_CONTEXT_CHARS))
        print("=" * 72)

        print("\n" + "=" * 72)
        print(" CONTEXTO GITHUB (inyectado al generador)")
        print("=" * 72)
        print(
            "Repo: %s | Rama ref: %s"
            % (
                resolved_repo or "(sin repo — solo texto de rama si aplica)",
                branch_name or "(rama default del repo)",
            )
        )
        if project_context:
            print(_trunc_block(project_context, _MAX_CONTEXT_CHARS))
        else:
            print("(vacío — sin README/estructura o sin repo resuelto)")
            if resolved_repo:
                print(
                    "[WARN] Repo %s resuelto pero sin contenido "
                    "(¿privado sin GITHUB_TOKEN o sin README en la rama?)."
                    % resolved_repo
                )
        print("=" * 72 + "\n")
    else:
        if resolved_repo and not project_context:
            print(
                "[WARN] %s | %s: repo sin README/contexto en rama."
                % (issue.identifier, resolved_repo)
            )

    try:
        gen = ImprovedTestGenerator()
        cases = gen.generate_from_text(user_story_text)
    except Exception as e:
        print("[ERROR] Fallo generando casos: %s" % e)
        
        return "error_generation"

    if not cases:
        print("[WARN] No se generaron casos para este issue.")
        return "skipped_no_cases"

    if not verbose:
        print("")
        print("Repo: %s" % (resolved_repo or "(sin repo)"))
        print("Código: %s" % issue.identifier)
        print("Issue: %s" % issue.title)
        _print_cases_compact(cases)
        print("")
    else:
        print("=" * 72)
        print(" CASOS GENERADOS — %d — %s" % (len(cases), issue.identifier))
        print("=" * 72)
        for i, tc in enumerate(cases, 1):
            print("\n--- Caso %d / %d — %s ---" % (i, len(cases), tc.id))
            print("Título: %s" % tc.title)
            print("Tipo: %s | Prioridad: %s" % (tc.test_type, tc.priority))
            print("Given:")
            for s in tc.given_steps: print("  • %s" % s)
            print("When:")
            for s in tc.when_steps:  print("  • %s" % s)
            print("Then:")
            for s in tc.then_steps:  print("  • %s" % s)
            print("Tags: %s" % " ".join(tc.tags))
        print("\n" + "=" * 72 + "\n")

    formatted = _convert_improved_to_serializable(cases, issue.title)
    created = client.upload_test_cases_as_subissues(
        parent_issue_identifier=issue.identifier,
        test_cases=formatted,
        team_id=issue.team_id,
        label_manual=automation_config.LINEAR_LABEL_MANUAL_TEST,
        label_automatizable=automation_config.LINEAR_LABEL_AUTOMATABLE,
    )

    if created:
        print("[OK] Subidos %d casos como sub-issues de %s" % (len(created), issue.identifier))
        if state_after:
            if client.update_issue_state(issue.id, state_after, issue.team_id):
                print("[OK] Issue movido a estado: %s" % state_after)
            else:
                print("[WARN] No se pudo mover el issue al estado '%s'" % state_after)
        return "processed"
    print("[ERROR] No se crearon sub-issues para %s" % issue.identifier)
    return "error_upload"


def _print_cases_compact(cases) -> None:
    """Lista casos: id, título, tipo, pasos When/Then (truncados)."""
    print("Casos generados (%d):" % len(cases))
    for tc in cases:
        print("  • %s %s — %s  [%s | %s]"
              % (_exec_tag(tc), tc.id, tc.title, tc.test_type, tc.priority))
        when = " / ".join(tc.when_steps)[:120]
        if when:
            print("    When: %s" % when)
        then = " / ".join(tc.then_steps)[:120]
        if then:
            print("    Then: %s" % then)


def run(verbose: bool = False) -> None:
    api_key = automation_config.LINEAR_API_KEY
    if not api_key:
        print("[ERROR] LINEAR_API_KEY no configurado (variable de entorno o automation_config.json)")
        sys.exit(1)

    target_state = automation_config.LINEAR_TARGET_STATE
    state_after = automation_config.LINEAR_STATE_AFTER_SUCCESS
    team_ids = automation_config.LINEAR_TEAM_IDS
    default_repo = automation_config.GITHUB_DEFAULT_REPO
    gh_token = automation_config.GITHUB_TOKEN
    team_repos = automation_config.GITHUB_TEAM_REPOS or {}

    if verbose:
        print("=" * 80)
        print("[INFO] Automatización Linear + GitHub (modo verbose)")
        print("       Estado objetivo: %s" % target_state)
        print("       Estado tras éxito: %s" % (state_after or "(no cambiar)"))
        print("       Repo GitHub por defecto: %s" % (default_repo or "(ninguno)"))
        if team_repos:
            print(
                "       Repos por equipo Linear: %s"
                % ", ".join("%s->%s" % (k, v) for k, v in team_repos.items())
            )
        print("=" * 80)
    else:
        print(
            "[INFO] Linear → QA | estado: %s | issues (máx. 50)"
            % target_state
        )

    client = LinearAPIClient(api_key)
    if not client.test_connection():
        print("[ERROR] No se pudo conectar con Linear. Revisa LINEAR_API_KEY.")
        sys.exit(1)

    team_ids_arg = team_ids if team_ids else None
    issues = client.list_issues_by_state(
        state_name=target_state,
        team_ids=team_ids_arg,
        first=50,
    )

    if not issues:
        print("[INFO] No hay issues en estado '%s'. Nada que procesar." % target_state)
        return

    print("[INFO] Issues a procesar: %d" % len(issues))

    processed = 0
    errors = 0

    for issue in issues:
        out = process_linear_issue_for_qa(client, issue, verbose=verbose)
        if out == "processed":
            processed += 1
        elif out in ("error_generation", "error_upload"):
            errors += 1

    print("\n" + "=" * 80)
    print("[INFO] Resumen: %d issues procesados, %d errores" % (processed, errors))
    print("=" * 80)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Automatización Linear + GitHub → casos QA"
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Volcar contexto Linear/GitHub completo y detalle de cada caso",
    )
    args = parser.parse_args()
    env_v = os.environ.get("AUTOMATION_VERBOSE", "").strip().lower()
    verbose = args.verbose or env_v in ("1", "true", "yes")
    run(verbose=verbose)
