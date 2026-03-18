#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de automatización: lee historias de Linear en un estado configurado,
genera casos de prueba (con contexto opcional de GitHub) y los sube como sub-issues.
Ejecutar desde la raíz del proyecto: python scripts/run_linear_automation.py
"""

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
from github_context import get_project_context_for_issue
from professional_qa_generator import ProfessionalQAGenerator
from test_case_automation import TestCase as LegacyTestCase, TestType, Priority


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
        preconditions_text = "\n".join([f"- {p}" for p in prof_case.preconditions])
        steps_text = "\n".join(prof_case.steps)
        structured_description = (
            f"**Objetivo:** Verificar funcionalidad del sistema\n\n"
            f"**Criterio:** {prof_case.criterion}\n\n"
            f"**Preconditions:**\n{preconditions_text}\n\n"
            f"**Pasos:**\n{steps_text}\n\n"
            f"**Resultado Esperado:**\n{prof_case.expected_result}"
        )
        tc = LegacyTestCase(
            id=prof_case.id,
            title=prof_case.title,
            description=structured_description,
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
            "preconditions": tc.preconditions,
            "steps": tc.steps,
            "expected_result": tc.expected_result,
            "priority": tc.priority.value if hasattr(tc.priority, "value") else str(tc.priority),
            "type": tc.test_type.value if hasattr(tc.test_type, "value") else str(tc.test_type),
        })
    return result


def run():
    api_key = automation_config.LINEAR_API_KEY
    if not api_key:
        print("[ERROR] LINEAR_API_KEY no configurado (variable de entorno o automation_config.json)")
        sys.exit(1)

    target_state = automation_config.LINEAR_TARGET_STATE
    state_after = automation_config.LINEAR_STATE_AFTER_SUCCESS
    team_ids = automation_config.LINEAR_TEAM_IDS
    default_repo = automation_config.GITHUB_DEFAULT_REPO
    gh_token = automation_config.GITHUB_TOKEN

    print("=" * 80)
    print("[INFO] Automatización Linear + GitHub")
    print(f"       Estado objetivo: {target_state}")
    print(f"       Estado tras éxito: {state_after or '(no cambiar)'}")
    print(f"       Repo GitHub por defecto: {default_repo or '(ninguno)'}")
    print("=" * 80)

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

    qa_generator = ProfessionalQAGenerator()
    processed = 0
    errors = 0

    for issue in issues:
        assert isinstance(issue, LinearIssueSummary)
        print("\n" + "-" * 60)
        print("[INFO] Procesando: %s - %s" % (issue.identifier, issue.title[:50]))

        user_story_text = (issue.description or "").strip()
        if not user_story_text:
            print("[WARN] Issue sin descripción; se omite.")
            errors += 1
            continue

        project_context = get_project_context_for_issue(
            issue.description,
            default_repo=default_repo,
            token=gh_token,
        )

        try:
            professional_cases = qa_generator.generate_test_cases(
                user_story_text=user_story_text,
                project_name=issue.title,
                project_context=project_context or None,
            )
        except Exception as e:
            print("[ERROR] Fallo generando casos: %s" % e)
            errors += 1
            continue

        if not professional_cases:
            print("[WARN] No se generaron casos para este issue.")
            continue

        formatted = _convert_professional_to_serializable(professional_cases, issue.title)
        created = client.upload_test_cases_as_subissues(
            parent_issue_identifier=issue.identifier,
            test_cases=formatted,
            team_id=issue.team_id,
        )

        if created:
            processed += 1
            print("[OK] Subidos %d casos como sub-issues de %s" % (len(created), issue.identifier))
            if state_after:
                if client.update_issue_state(issue.id, state_after, issue.team_id):
                    print("[OK] Issue movido a estado: %s" % state_after)
                else:
                    print("[WARN] No se pudo mover el issue al estado '%s'" % state_after)
        else:
            print("[ERROR] No se crearon sub-issues para %s" % issue.identifier)
            errors += 1

    print("\n" + "=" * 80)
    print("[INFO] Resumen: %d issues procesados, %d errores" % (processed, errors))
    print("=" * 80)


if __name__ == "__main__":
    run()
