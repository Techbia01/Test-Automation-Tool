#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Muestra en consola el README de un repositorio GitHub.

  python3 scripts/show_github_readme.py org/repo
  python3 scripts/show_github_readme.py org/repo --ref mi-rama
  python3 scripts/show_github_readme.py --from-env
  python3 scripts/show_github_readme.py --team-key ACQ
"""

import argparse
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, os.path.join(PROJECT_ROOT, "src"))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "config"))

import automation as automation_config
from github_context import fetch_readme_markdown, github_repo_and_readme_diagnostic


def main():
    p = argparse.ArgumentParser(description="Mostrar README de GitHub en stdout.")
    p.add_argument("repo", nargs="?", help="owner/repo")
    p.add_argument("--ref", help="Rama o tag")
    p.add_argument("--from-env", action="store_true", help="GITHUB_DEFAULT_REPO")
    p.add_argument("--team-key", help="Clave equipo (github_team_repos)")
    p.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Diagnóstico en stderr (token, HTTP, SSO)",
    )
    args = p.parse_args()

    token = automation_config.GITHUB_TOKEN
    repo = None

    if args.team_key:
        tr = automation_config.GITHUB_TEAM_REPOS or {}
        k = args.team_key.strip().upper()
        if k not in tr:
            print("[ERROR] Clave '%s' no está en github_team_repos." % k, file=sys.stderr)
            sys.exit(1)
        repo = tr[k]
    elif args.from_env:
        repo = automation_config.GITHUB_DEFAULT_REPO
        if not repo or not str(repo).strip():
            print("[ERROR] GITHUB_DEFAULT_REPO vacío.", file=sys.stderr)
            sys.exit(1)
        repo = str(repo).strip()
    elif args.repo:
        repo = args.repo.strip()
    else:
        p.print_help()
        sys.exit(1)

    if args.verbose:
        print("Directorio: %s" % os.getcwd(), file=sys.stderr)
        print("Raíz proyecto: %s" % PROJECT_ROOT, file=sys.stderr)
        for line in github_repo_and_readme_diagnostic(
            repo, token=token, git_ref=args.ref
        ):
            print(line, file=sys.stderr)
        print("---", file=sys.stderr)

    text = fetch_readme_markdown(repo, token=token, git_ref=args.ref)
    if not text:
        print(
            "[ERROR] No se pudo obtener el README. Ejecuta con -v para ver el motivo.",
            file=sys.stderr,
        )
        sys.exit(1)
    print(text)


if __name__ == "__main__":
    main()
