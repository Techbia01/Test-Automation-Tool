#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuración de Rutas del Sistema
Define las rutas principales del sistema de automatización
"""

import os
from pathlib import Path

# Directorio raíz del proyecto
PROJECT_ROOT = Path(__file__).parent.parent
# Rutas principales
SRC_DIR = PROJECT_ROOT / "src"
GENERATORS_DIR = PROJECT_ROOT / "generators"
EXPORTERS_DIR = PROJECT_ROOT / "exporters"
TESTS_DIR = PROJECT_ROOT / "tests"
DOCS_DIR = PROJECT_ROOT / "docs"
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
CONFIG_DIR = PROJECT_ROOT / "config"
DATA_DIR = PROJECT_ROOT / "data"
TEMPLATES_DIR = PROJECT_ROOT / "templates"
STATIC_DIR = PROJECT_ROOT / "static"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
UPLOADS_DIR = PROJECT_ROOT / "uploads"

# Configuración de Flask
FLASK_CONFIG = {
    'UPLOAD_FOLDER': str(UPLOADS_DIR),
    'OUTPUT_FOLDER': str(OUTPUTS_DIR),
    'TEMPLATES_FOLDER': str(TEMPLATES_DIR),
    'STATIC_FOLDER': str(STATIC_DIR)
}

# Asegurar que los directorios existan
def ensure_directories():
    """Crea los directorios necesarios si no existen"""
    directories = [
        SRC_DIR, GENERATORS_DIR, EXPORTERS_DIR, TESTS_DIR,
        DOCS_DIR, SCRIPTS_DIR, CONFIG_DIR, DATA_DIR,
        TEMPLATES_DIR, STATIC_DIR, OUTPUTS_DIR, UPLOADS_DIR
    ]
    
    for directory in directories:
        directory.mkdir(exist_ok=True)
        print(f"✅ Directorio verificado: {directory}")

if __name__ == "__main__":
    ensure_directories()
