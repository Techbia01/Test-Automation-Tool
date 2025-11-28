#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Automatización de Casos de Prueba para QA
Punto de entrada principal del sistema
"""

import sys
import os

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
