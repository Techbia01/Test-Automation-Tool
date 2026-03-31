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
    get_pr_description_from_urls,
    resolve_github_repo_slug,
)

# Límite por bloque para no saturar la terminal (ajustable)
_MAX_CONTEXT_CHARS = 30000
from professional_qa_generator import ProfessionalQAGenerator
from test_case_automation import TestCase as LegacyTestCase, TestType, Priority

# ClaudeQAGenerator: importación diferida para no fallar si anthropic no está instalado
def _load_claude_generator():
    try:
        from claude_qa_generator import ClaudeQAGenerator
        return ClaudeQAGenerator(api_key=automation_config.ANTHROPIC_API_KEY)
    except ImportError as e:
        print("[ERROR] ClaudeQAGenerator no disponible: %s" % e)
        sys.exit(1)
    except ValueError as e:
        print("[ERROR] %s" % e)
        sys.exit(1)


def _convert_professional_to_serializable(professional_cases, project_name: str):
    """Convierte casos del generador profesional al formato dict para Linear."""
    type_map = {
        "Funcional": TestType.FUNCTIONAL,
        "Negativo": TestType.NEGATIVE,
        "Integración": TestType.INTEGRATION,
        "Regresión": TestType.FUNCTIONAL,
        "UI": TestType.FUNCTIONAL,
    }
    priority_map = {
        "Alta": Priority.HIGH,
        "Media": Priority.MEDIUM,
        "Baja": Priority.LOW,
    }
    result = []
    for prof_case in professional_cases:
        full_description = prof_case._format_description()
        tc = LegacyTestCase(
            id=prof_case.id,
            title=prof_case.title,
            description=full_description,
            preconditions=prof_case.preconditions,
            steps=prof_case.steps,
            expected_result=prof_case.expected_result,
            test_type=type_map.get(prof_case.test_type.value, TestType.FUNCTIONAL),
            priority=priority_map.get(prof_case.priority.value, Priority.HIGH),
            user_story=project_name,
            tags=["@qa", "@automated"],
        )
        result.append({
            "test_case_id": tc.id,
            "title": tc.title,
            "description": tc.description,
            "linear_description_is_complete": True,
            "preconditions": tc.preconditions,
            "steps": tc.steps,
            "expected_result": tc.expected_result,
            "priority": tc.priority.value if hasattr(tc.priority, "value") else str(tc.priority),
            "type": tc.test_type.value if hasattr(tc.test_type, "value") else str(tc.test_type),
            "execution_suitability": prof_case.execution_suitability.value,
            "automation_hint": prof_case.automation_hint,
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


def _exec_tag(pc) -> str:
    if pc.execution_suitability.value == "Automatizable":
        return "[AUTO]"
    return "[MANUAL]"


def process_linear_issue_for_qa(
    client: LinearAPIClient,
    issue: LinearIssueSummary,
    verbose: bool = False,
    engine: str = "rules",
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

    git_ctx = client.get_issue_git_context(issue.id)
    attachment_urls = git_ctx.attachment_urls
    branch_name = (git_ctx.branch_name or "").strip()

    team_key = None
    if issue.identifier and "-" in issue.identifier:
        team_key = issue.identifier.split("-", 1)[0].strip().upper()

    # Si la descripción está vacía, intentar usar el body del PR adjunto
    if not user_story_text and attachment_urls:
        pr_text = get_pr_description_from_urls(attachment_urls, token=gh_token)
        if pr_text:
            print("[INFO] Descripción vacía; usando body del PR adjunto como HU.")
            user_story_text = pr_text

    if not user_story_text:
        print("[WARN] Issue sin descripción ni PR con contenido; se omite.")
        return "skipped_no_description"

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

    # ── Selección de motor ───────────────────────────────────────────────────
    professional_cases = []

    if engine == "rules":
        rules_gen = ProfessionalQAGenerator()
        rules_gen._qa_generation_verbose = verbose
        professional_cases = _run_generator("Motor de reglas", rules_gen, issue, user_story_text, project_context, verbose)

    elif engine == "claude":
        professional_cases = _run_generator("Claude AI", _load_claude_generator(), issue, user_story_text, project_context, verbose)

    elif engine == "compare":
        rules_gen = ProfessionalQAGenerator()
        rules_gen._qa_generation_verbose = verbose
        for label, gen in [("Motor de reglas", rules_gen), ("Claude AI", _load_claude_generator())]:
            print("[%s] Generando..." % label)
            cases = _run_generator(label, gen, issue, user_story_text, project_context, verbose)
            seen = {tc.title.strip().lower() for tc in professional_cases}
            for tc in cases:
                if tc.title.strip().lower() not in seen:
                    professional_cases.append(tc)
                    seen.add(tc.title.strip().lower())
            print("  → %d caso(s) generados por %s" % (len(cases), label))

    else:  # "auto" (default): Claude con fallback al motor de reglas
        print("[INFO] Motor: Claude AI (con fallback a motor de reglas)")
        try:
            professional_cases = _run_generator("Claude AI", _load_claude_generator(), issue, user_story_text, project_context, verbose)
        except SystemExit:
            # _load_claude_generator hace sys.exit si no hay API key
            professional_cases = []
        if not professional_cases:
            print("[WARN] Claude AI no generó casos; usando motor de reglas como fallback.")
            rules_gen = ProfessionalQAGenerator()
            rules_gen._qa_generation_verbose = verbose
            professional_cases = _run_generator("Motor de reglas (fallback)", rules_gen, issue, user_story_text, project_context, verbose)

    if not professional_cases:
        print("[WARN] No se generaron casos para este issue.")
        return "skipped_no_cases"

    if not verbose:
        print("")
        print("Repo: %s" % (resolved_repo or "(sin repo)"))
        print("Código: %s" % issue.identifier)
        print("Issue: %s" % issue.title)
        _print_cases_compact(professional_cases)
        print("")
    else:
        print("=" * 72)
        print(
            " CASOS GENERADOS — %d — %s"
            % (len(professional_cases), issue.identifier)
        )
        print("=" * 72)
        for i, pc in enumerate(professional_cases, 1):
            print(
                "\n--- Caso %d / %d — %s ---"
                % (i, len(professional_cases), pc.id)
            )
            print("Título: %s" % pc.title)
            print(
                "Tipo: %s | Prioridad: %s"
                % (pc.test_type.value, pc.priority.value)
            )
            print("Criterio: %s" % _trunc_block(pc.criterion or "", 2000))
            print("Precondiciones:")
            for p in pc.preconditions or []:
                print("  • %s" % p)
            print("Pasos:")
            for s in pc.steps or []:
                print("  %s" % s)
            print("Resultado esperado:\n  %s" % (pc.expected_result or ""))
            print(
                "Ejecución sugerida: %s — %s"
                % (
                    pc.execution_suitability.value,
                    pc.automation_hint or "—",
                )
            )
        print("\n" + "=" * 72 + "\n")

    formatted = _convert_professional_to_serializable(professional_cases, issue.title)
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


def _run_generator(label, gen, issue, user_story_text, project_context, verbose):
    """Ejecuta un generador y retorna los casos. Lista vacía si falla."""
    try:
        return gen.generate_test_cases(
            user_story_text=user_story_text,
            project_name=issue.title,
            project_context=project_context or None,
            verbose_log=verbose,
        )
    except Exception as e:
        print("[ERROR][%s] Fallo generando casos: %s" % (label, e))
        return []


def _print_cases_compact(professional_cases) -> None:
    """Lista casos: id, título, ejecución sugerida, resultado (truncado)."""
    print("Casos generados (%d):" % len(professional_cases))
    for pc in professional_cases:
        print(
            "  • %s %s — %s"
            % (_exec_tag(pc), pc.id, pc.title)
        )
        exp = (pc.expected_result or "").replace("\n", " ").strip()
        if len(exp) > 280:
            exp = exp[:280] + "…"
        if exp:
            print("    → %s" % exp)
        hint = (pc.automation_hint or "").strip()
        if hint:
            print("    (%s)" % hint[:120] + ("…" if len(hint) > 120 else ""))


def run(verbose: bool = False, engine: str = "rules") -> None:
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
        print("       Motor: %s" % engine)
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
        engine_label = {
            "auto": "Claude AI + fallback reglas",
            "claude": "Claude AI",
            "rules": "Motor de reglas",
            "compare": "Ambos (unión)",
        }.get(engine, engine)
        print(
            "[INFO] Linear → QA | motor: %s | estado: %s | issues (máx. 50)"
            % (engine_label, target_state)
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
        out = process_linear_issue_for_qa(client, issue, verbose=verbose, engine=engine)
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
    parser.add_argument(
        "--engine",
        choices=["auto", "rules", "claude", "compare"],
        default="auto",
        help=(
            "Motor de generación: "
            "'auto' = Claude AI con fallback a motor de reglas (por defecto), "
            "'rules' = solo motor de reglas, "
            "'claude' = solo Claude AI, "
            "'compare' = ambos (sube la unión de casos)"
        ),
    )
    args = parser.parse_args()
    env_v = os.environ.get("AUTOMATION_VERBOSE", "").strip().lower()
    verbose = args.verbose or env_v in ("1", "true", "yes")
    run(verbose=verbose, engine=args.engine)
