#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Inicio para la Aplicación Web QA
Inicia el servidor web para el sistema de generación de casos de prueba
"""

import os
import sys
import webbrowser
import time
from threading import Timer

def open_browser():
    """Abre el navegador después de 2 segundos"""
    time.sleep(2)
    webbrowser.open('http://localhost:5000')

def main():
    """Función principal"""
    print("🌐 INICIANDO APLICACIÓN WEB QA")
    print("=" * 50)
    
    # Verificar que Flask esté instalado
    try:
        import flask
        print(f"✅ Flask {flask.__version__} detectado")
    except ImportError:
        print("❌ Flask no está instalado")
        print("💡 Ejecuta: pip install flask")
        return
    
    # Verificar que todos los módulos estén disponibles
    try:
        from test_case_automation import UserStoryParser, TestCaseGenerator, QAValidator
        from test_templates import TemplateManager
        print("✅ Módulos de generación de casos disponibles")
    except ImportError as e:
        print(f"❌ Error importando módulos: {e}")
        return
    
    # Crear directorios necesarios
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('outputs', exist_ok=True)
    print("✅ Directorios creados")
    
    # Abrir navegador automáticamente
    Timer(1.0, open_browser).start()
    
    print("\n🚀 Iniciando servidor web...")
    print("📱 La aplicación se abrirá automáticamente en tu navegador")
    print("🌐 URL: http://localhost:5000")
    print("\n💡 Para detener el servidor, presiona Ctrl+C")
    print("=" * 50)
    
    # Iniciar aplicación Flask
    try:
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
    except KeyboardInterrupt:
        print("\n\n👋 Servidor detenido. ¡Hasta luego!")
    except Exception as e:
        print(f"\n❌ Error iniciando servidor: {e}")

if __name__ == "__main__":
    main()
