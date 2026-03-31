#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Solo extracción de datos desde Linear (sin generar casos ni subir sub-issues).

Uso desde la raíz del proyecto:

  # Un issue por identificador (ej. FIN-123) o UUID interno
  python3 scripts/inspect_linear_issue.py FIN-123

  # Listar issues en el estado configurado (.env LINEAR_TARGET_STATE)
  python3 scripts/inspect_linear_issue.py --list

  # Listar issues en otro estado
  python3 scripts/inspect_linear_issue.py --list --state "En progreso"
"""

import argparse
import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, os.path.join(PROJECT_ROOT, "src"))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "config"))

import automation as automation_config
from linear_api_client import LinearAPIClient


def main():
    parser = argparse.ArgumentParser(
        description="Inspeccionar datos de Linear (rama, adjuntos, descripción)."
    )
    parser.add_argument(
        "issue",
        nargs="?",
        help="Identificador del issue (ej. FIN-123) o UUID",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="Listar issues en LINEAR_TARGET_STATE (o --state)",
    )
    parser.add_argument(
        "--state",
        default=None,
        help="Nombre del estado para --list (por defecto: LINEAR_TARGET_STATE)",
    )
    args = parser.parse_args()

    api_key = automation_config.LINEAR_API_KEY
    if not api_key:
        print("[ERROR] LINEAR_API_KEY no configurada (.env o entorno).")
        sys.exit(1)

    client = LinearAPIClient(api_key)
    if not client.test_connection():
        print("[ERROR] No se pudo conectar con Linear.")
        sys.exit(1)
    print("[OK] Conexión con Linear correcta.\n")

    if args.list:
        state = args.state or automation_config.LINEAR_TARGET_STATE
        team_ids = automation_config.LINEAR_TEAM_IDS or None
        issues = client.list_issues_by_state(
            state_name=state,
            team_ids=team_ids,
            first=30,
        )
        print("Estado: %s | Issues: %d\n" % (state, len(issues)))
        for i in issues:
            git = client.get_issue_git_context(i.id)
            branch = git.branch_name or "(sin branchName)"
            print("  %s | %s" % (i.identifier, i.title[:60]))
            print("      rama Linear: %s" % branch)
            if git.attachment_urls:
                print("      adjuntos: %d URL(s)" % len(git.attachment_urls))
                for u in git.attachment_urls[:3]:
                    print("        - %s" % (u[:80] + ("..." if len(u) > 80 else "")))
                if len(git.attachment_urls) > 3:
                    print("        - ...")
            print()
        return

    if not args.issue:
        parser.print_help()
        print("\nEjemplo: python3 scripts/inspect_linear_issue.py FIN-123")
        sys.exit(1)

    ident = args.issue.strip()
    uuid_re = re.compile(
        r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
        re.I,
    )
    if uuid_re.match(ident):
        issue_uuid = ident
    else:
        resolved = client.get_issue_by_identifier(ident)
        if not resolved:
            print("[ERROR] No se encontró el issue: %s" % ident)
            sys.exit(1)
        issue_uuid = resolved
        print("UUID interno: %s\n" % issue_uuid)

    query = """
    query($issueId: String!) {
        issue(id: $issueId) {
            id
            identifier
            title
            branchName
            description
            state { name }
            team { key name }
            attachments {
                nodes {
                    url
                    title
                    subtitle
                }
            }
        }
    }
    """
    try:
        data = client._make_request(query, {"issueId": issue_uuid})
    except Exception as e:
        print("[ERROR] API: %s" % e)
        sys.exit(1)

    issue = data.get("data", {}).get("issue")
    if not issue:
        print("[ERROR] Issue no encontrado (id: %s)" % issue_uuid)
        if "errors" in data:
            print(data["errors"])
        sys.exit(1)

    print("=" * 60)
    print("Issue: %s — %s" % (issue.get("identifier"), issue.get("title")))
    print("Estado: %s" % (issue.get("state") or {}).get("name"))
    print(
        "Equipo: %s (%s)"
        % (
            (issue.get("team") or {}).get("name"),
            (issue.get("team") or {}).get("key"),
        )
    )
    print("=" * 60)
    print("\n## branchName (rama vinculada en Linear)")
    bn = issue.get("branchName")
    print(repr(bn) if bn is not None else "(vacío o null)")
    print("\n## Adjuntos (%d)" % len(issue.get("attachments", {}).get("nodes", [])))
    for n in issue.get("attachments", {}).get("nodes", []):
        print("  - %s" % (n.get("url") or "(sin url)"))
        if n.get("title"):
            print("    title: %s" % n.get("title"))
    desc = (issue.get("description") or "").strip()
    print("\n## Descripción (primeros 500 caracteres)")
    print(desc[:500] + ("..." if len(desc) > 500 else "") or "(vacía)")
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
