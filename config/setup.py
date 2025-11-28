#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de configuración para el Sistema de Automatización de Casos de Prueba
"""

import os
import sys
import json
from pathlib import Path

def check_python_version():
    """Verifica que la versión de Python sea compatible"""
    if sys.version_info < (3, 7):
        print("❌ Se requiere Python 3.7 o superior")
        print(f"   Versión actual: {sys.version}")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detectado")
    return True

def install_dependencies():
    """Instala las dependencias necesarias"""
    try:
        import subprocess
        print("📦 Instalando dependencias...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencias instaladas correctamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al instalar dependencias: {e}")
        return False
    except FileNotFoundError:
        print("❌ pip no encontrado. Asegúrate de que Python esté instalado correctamente")
        return False

def create_config_file():
    """Crea archivo de configuración si no existe"""
    config_file = "qa_config.json"
    example_file = "qa_config_example.json"
    
    if not os.path.exists(config_file):
        if os.path.exists(example_file):
            try:
                with open(example_file, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
                
                with open(config_file, 'w', encoding='utf-8') as f:
                    json.dump(config_data, f, indent=2, ensure_ascii=False)
                
                print(f"✅ Archivo de configuración creado: {config_file}")
            except Exception as e:
                print(f"⚠️  No se pudo crear el archivo de configuración: {e}")
        else:
            print("⚠️  Archivo de ejemplo de configuración no encontrado")
    else:
        print(f"✅ Archivo de configuración ya existe: {config_file}")

def test_installation():
    """Prueba que la instalación fue exitosa"""
    try:
        from test_case_automation import UserStoryParser, TestCaseGenerator, QAValidator
        from test_templates import TemplateManager
        print("✅ Instalación verificada correctamente")
        return True
    except ImportError as e:
        print(f"❌ Error en la verificación: {e}")
        return False

def show_usage_instructions():
    """Muestra instrucciones de uso"""
    print("\n" + "=" * 60)
    print("🎉 ¡INSTALACIÓN COMPLETADA!")
    print("=" * 60)
    print("\n📖 INSTRUCCIONES DE USO:")
    print("\n1. Modo Interactivo (Recomendado):")
    print("   python interactive_generator.py")
    print("\n2. Modo Línea de Comandos:")
    print("   python test_case_automation.py example_user_story.txt --output mis_casos")
    print("\n3. Ejecutar Pruebas:")
    print("   python test_system.py")
    print("\n4. Personalizar Configuración:")
    print("   Edita el archivo qa_config.json")
    print("\n📚 Para más información, consulta README.md")

def main():
    """Función principal de configuración"""
    print("🚀 CONFIGURANDO SISTEMA DE AUTOMATIZACIÓN DE CASOS DE PRUEBA")
    print("=" * 70)
    
    # Verificar Python
    if not check_python_version():
        return False
    
    # Instalar dependencias
    if not install_dependencies():
        return False
    
    # Crear archivo de configuración
    create_config_file()
    
    # Probar instalación
    if not test_installation():
        print("❌ La instalación no se completó correctamente")
        return False
    
    # Mostrar instrucciones
    show_usage_instructions()
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
