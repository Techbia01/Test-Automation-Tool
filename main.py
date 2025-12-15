#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Automatización de Casos de Prueba para QA
Punto de entrada principal del sistema
"""

import sys
import os
import io

# Configurar encoding UTF-8 para Windows (soluciona error 'charmap' codec)
if sys.platform == 'win32':
    try:
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
            sys.stderr.reconfigure(encoding='utf-8', errors='replace')
        else:
            # Para versiones anteriores de Python
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    except (AttributeError, ValueError, TypeError):
        # Si falla, intentar método alternativo
        try:
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
        except:
            pass  # Si todo falla, continuar sin modificar

# Agregar los directorios necesarios al path
current_dir = os.path.dirname(__file__)
sys.path.insert(0, current_dir)

from app import app

if __name__ == '__main__':
    print("Iniciando Sistema de Automatizacion de Casos de Prueba para QA")
    print("Accede a: http://localhost:5000")
    print("Crear proyecto: http://localhost:5000/new_project")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
