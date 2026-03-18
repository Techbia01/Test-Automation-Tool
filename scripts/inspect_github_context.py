#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Muestra en consola el contexto que se obtendría de GitHub (README + estructura),
igual que usa la automatización para generar casos.

Uso (desde la raíz del proyecto):

  python3 scripts/inspect_github_context.py org/repo

  python3 scripts/inspect_github_context.py org/repo --ref mi-rama

  python3 scripts/inspect_github_context.py --from-env

  python3 scripts/inspect_github_context.py org/repo --linear-branch mi-feature

  # Repo según equipo Linear (github_team_repos en automation_config.json)
  python3 scripts/inspect_github_context.py --team-key FIN --linear-branch feature/acq-3

  python3 scripts/inspect_github_context.py --max-chars 1500 org/repo
"""

import argparse
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, os.path.join(PROJECT_ROOT, "src"))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "config"))

import automation as automation_config
from github_context import fetch_repo_context, get_project_context_for_issue


def main():
    parser = argparse.ArgumentParser(
        description="Ver el texto de contexto que trae GitHub para el generador."
    )
    parser.add_argument(
        "repo",
        nargs="?",
        help="owner/repo o URL de GitHub",
    )
    parser.add_argument(
        "--from-env",
        action="store_true",
        help="Usar GITHUB_DEFAULT_REPO (y token) del .env",
    )
    parser.add_argument(
        "--team-key",
        default=None,
        metavar="FIN",
        help="Clave equipo Linear (ej. FIN); repo desde github_team_repos en JSON",
    )
    parser.add_argument(
        "--ref",
        default=None,
        help="Rama o tag (README/contents con ?ref=)",
    )
    parser.add_argument(
        "--linear-branch",
        default=None,
        metavar="RAMA",
        help="Incluir bloque como si Linear tuviera esa branchName",
    )
    parser.add_argument(
        "--max-chars",
        type=int,
        default=None,
        help="Truncar salida a N caracteres",
    )
    args = parser.parse_args()

    token = automation_config.GITHUB_TOKEN
    team_repos = automation_config.GITHUB_TEAM_REPOS or {}
    team_key = (args.team_key or "").strip().upper() if args.team_key else None
    text = ""

    if team_key:
        if team_key not in team_repos:
            print(
                "[ERROR] La clave '%s' no está en github_team_repos.\n"
                "        Edita automation_config.json, por ejemplo:\n"
                '        "github_team_repos": { "FIN": "mi-org/app-finanzas" }\n'
                % team_key,
                file=sys.stderr,
            )
            sys.exit(1)
        if args.linear_branch:
            text = get_project_context_for_issue(
                "",
                default_repo=automation_config.GITHUB_DEFAULT_REPO,
                token=token,
                attachment_urls=[],
                linear_branch_name=args.linear_branch,
                linear_team_key=team_key,
                team_key_to_repo=team_repos,
            )
        else:
            text = fetch_repo_context(
                team_repos[team_key],
                token=token,
                include_structure=True,
                git_ref=args.ref,
            )
    elif args.from_env:
        repo = automation_config.GITHUB_DEFAULT_REPO
        if not repo or not str(repo).strip():
            print(
                "[ERROR] GITHUB_DEFAULT_REPO vacío en .env. "
                "Añade owner/repo o pásalo como argumento."
            )
            sys.exit(1)
        repo = str(repo).strip()
        if args.linear_branch:
            text = get_project_context_for_issue(
                "",
                default_repo=repo,
                token=token,
                attachment_urls=[],
                linear_branch_name=args.linear_branch,
            )
        else:
            text = fetch_repo_context(
                repo,
                token=token,
                include_structure=True,
                git_ref=args.ref,
            )
    elif args.repo:
        repo = args.repo.strip()
        placeholder = repo.lower() in ("owner/repo", "org/repo", "mi-org/mi-repo")
        if placeholder:
            print(
                "[AVISO] '%s' es un ejemplo; usa un repo real.\n" % repo,
                file=sys.stderr,
            )
        if args.linear_branch:
            text = get_project_context_for_issue(
                "",
                default_repo=repo,
                token=token,
                attachment_urls=[],
                linear_branch_name=args.linear_branch,
                linear_team_key=None,
                team_key_to_repo=team_repos if team_repos else None,
            )
        else:
            text = fetch_repo_context(
                repo,
                token=token,
                include_structure=True,
                git_ref=args.ref,
            )
    else:
        parser.print_help()
        print(
            "\nEjemplos:\n"
            "  python3 scripts/inspect_github_context.py octocat/Hello-World\n"
            "  python3 scripts/inspect_github_context.py --team-key FIN "
            "--linear-branch mi-rama\n"
        )
        sys.exit(1)

    if not text.strip():
        print(
            "[AVISO] No se obtuvo contenido. Posibles causas:\n"
            "  - Repo privado sin GITHUB_TOKEN en .env\n"
            "  - Rama inexistente\n"
            "  - Repo incorrecto\n",
            file=sys.stderr,
        )
        sys.exit(1)

    if args.linear_branch and "## README" not in text and "## Estructura" not in text:
        print(
            "\n[AVISO] Solo aparece la rama: GitHub no devolvió README/estructura "
            "(repo privado sin token o rama sin README).",
            file=sys.stderr,
        )

    out = text
    if args.max_chars and len(out) > args.max_chars:
        out = out[: args.max_chars] + "\n\n... [truncado, total %d caracteres]" % len(
            text
        )

    print(out)


if __name__ == "__main__":
    main()
