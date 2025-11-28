#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo Interactivo para Equipos QA
Demuestra el flujo completo de generación de casos de prueba
"""

import os
import json
from test_case_automation import UserStoryParser, TestCaseGenerator, QAValidator, TestCaseExporter
from test_templates import TemplateManager
from linear_integration import LinearExporter

def print_header(title):
    """Imprime un encabezado formateado"""
    print("\n" + "=" * 60)
    print(f"🎯 {title}")
    print("=" * 60)

def demo_basic_generation():
    """Demo de generación básica"""
    print_header("DEMO: Generación Básica de Casos de Prueba")
    
    # Historia de ejemplo
    sample_story = """
    Historia de Usuario: Carrito de Compras
    
    Como cliente de la tienda online
    Quiero poder agregar productos a mi carrito
    Para poder comprar múltiples items de una vez
    
    Descripción:
    El sistema debe permitir a los usuarios agregar productos al carrito,
    ver el resumen de compra y proceder al checkout.
    
    Criterios de Aceptación:
    
    1. Dado que soy un cliente
       Cuando agrego un producto al carrito
       Entonces debo ver el producto en mi carrito
    
    2. Dado que tengo productos en el carrito
       Cuando modifico la cantidad
       Entonces el total debe actualizarse automáticamente
    
    3. Dado que tengo productos en el carrito
       Cuando elimino un producto
       Entonces el producto debe desaparecer del carrito
    """
    
    print("📝 Historia de Usuario de ejemplo:")
    print(sample_story[:200] + "...")
    
    # Parsear historia
    parser = UserStoryParser()
    user_story = parser.parse_from_text(sample_story)
    
    print(f"\n✅ Historia parseada: {user_story.title}")
    print(f"📋 Criterios encontrados: {len(user_story.acceptance_criteria)}")
    
    # Generar casos
    generator = TestCaseGenerator()
    test_cases = generator.generate_test_cases(user_story)
    
    print(f"🧪 Casos generados: {len(test_cases)}")
    
    # Validar calidad
    validator = QAValidator()
    validation_result = validator.validate_test_suite(test_cases)
    
    print(f"📊 Puntaje de calidad: {validation_result['average_score']}/100")
    print(f"🎯 Nivel: {validation_result['overall_quality']}")
    
    return test_cases, user_story

def demo_templates():
    """Demo de plantillas especializadas"""
    print_header("DEMO: Plantillas Especializadas")
    
    # Crear historia simple
    simple_story = """
    Historia de Usuario: API de Usuarios
    
    Como desarrollador
    Quiero consumir la API de usuarios
    Para integrar con mi aplicación
    
    Criterios:
    1. Dado que hago GET /users
       Cuando la API responde
       Entonces debo recibir lista de usuarios
    """
    
    parser = UserStoryParser()
    user_story = parser.parse_from_text(simple_story)
    
    generator = TestCaseGenerator()
    base_cases = generator.generate_test_cases(user_story)
    
    template_manager = TemplateManager()
    
    print("🎨 Plantillas disponibles:")
    for template_name in template_manager.get_available_templates():
        info = template_manager.get_template_info(template_name)
        print(f"  • {info['name']}: {info['description']}")
    
    # Aplicar plantilla API
    print(f"\n🔌 Aplicando plantilla API...")
    api_cases = template_manager.apply_template('api', user_story, base_cases)
    
    print(f"📈 Casos base: {len(base_cases)}")
    print(f"📈 Con plantilla API: {len(api_cases)}")
    print(f"📈 Casos adicionales: {len(api_cases) - len(base_cases)}")
    
    return api_cases

def demo_linear_integration(test_cases):
    """Demo de integración con Linear"""
    print_header("DEMO: Integración con Linear")
    
    # Exportar para Linear
    exporter = LinearExporter()
    
    # Crear archivos para Linear
    linear_issues = exporter.export_to_linear_format(test_cases[:5], "demo_linear.json")
    exporter.create_linear_import_template(test_cases[:5], "demo_linear.csv")
    
    print("📤 Archivos generados para Linear:")
    print("  • demo_linear.json - Para importación programática")
    print("  • demo_linear.csv - Para importación manual")
    
    # Mostrar ejemplo de issue
    if linear_issues:
        example_issue = linear_issues[0]
        print(f"\n📋 Ejemplo de issue para Linear:")
        print(f"  Título: {example_issue['title']}")
        print(f"  Etiquetas: {', '.join(example_issue['labels'])}")
        print(f"  Prioridad: {example_issue['priority']}")
        print(f"  Estado: {example_issue['state']}")
    
    return linear_issues

def demo_validation():
    """Demo de validación de calidad"""
    print_header("DEMO: Validación de Calidad QA")
    
    # Crear casos de ejemplo con diferentes calidades
    from test_case_automation import TestCase, TestType, Priority
    
    good_case = TestCase(
        id="TC-GOOD-001",
        title="Verificar login con credenciales válidas",
        description="Verificar que un usuario puede iniciar sesión correctamente con sus credenciales válidas",
        preconditions=["Usuario registrado", "Credenciales válidas disponibles"],
        steps=["Navegar a login", "Ingresar email", "Ingresar contraseña", "Hacer clic en Iniciar Sesión"],
        expected_result="El usuario es redirigido al dashboard principal",
        test_type=TestType.FUNCTIONAL,
        priority=Priority.HIGH,
        user_story="Sistema de Login",
        tags=["funcional", "happy-path"]
    )
    
    bad_case = TestCase(
        id="TC-BAD-001",
        title="Test",
        description="Test",
        preconditions=[],
        steps=["Test"],
        expected_result="Test",
        test_type=TestType.FUNCTIONAL,
        priority=Priority.HIGH,
        user_story="Test",
        tags=[]
    )
    
    validator = QAValidator()
    
    print("🔍 Validando caso de buena calidad:")
    good_result = validator.validate_test_case(good_case)
    print(f"  Puntaje: {good_result['score']}/100")
    print(f"  Problemas: {len(good_result['issues'])}")
    print(f"  Advertencias: {len(good_result['warnings'])}")
    
    print("\n🔍 Validando caso de mala calidad:")
    bad_result = validator.validate_test_case(bad_case)
    print(f"  Puntaje: {bad_result['score']}/100")
    print(f"  Problemas: {len(bad_result['issues'])}")
    if bad_result['issues']:
        print(f"  Problemas encontrados: {', '.join(bad_result['issues'])}")
    
    return [good_case, bad_case]

def demo_export_formats(test_cases):
    """Demo de formatos de exportación"""
    print_header("DEMO: Formatos de Exportación")
    
    exporter = TestCaseExporter()
    
    # Exportar a diferentes formatos
    print("📤 Exportando a diferentes formatos...")
    
    try:
        exporter.export_to_excel(test_cases[:3], "demo_casos.xlsx")
        print("✅ Excel: demo_casos.xlsx")
    except Exception as e:
        print(f"❌ Error Excel: {e}")
    
    try:
        exporter.export_to_csv(test_cases[:3], "demo_casos.csv")
        print("✅ CSV: demo_casos.csv")
    except Exception as e:
        print(f"❌ Error CSV: {e}")
    
    try:
        exporter.export_to_json(test_cases[:3], "demo_casos.json")
        print("✅ JSON: demo_casos.json")
    except Exception as e:
        print(f"❌ Error JSON: {e}")
    
    # Mostrar estadísticas
    print(f"\n📊 Estadísticas de exportación:")
    print(f"  • Casos exportados: {len(test_cases[:3])}")
    print(f"  • Formatos: Excel, CSV, JSON")

def main():
    """Función principal del demo"""
    print("🎬 DEMO INTERACTIVO: Sistema de Automatización de Casos de Prueba")
    print("🎯 Para Equipos QA + Integración con Linear")
    print("\nEste demo te mostrará todas las funcionalidades del sistema...")
    
    input("\nPresiona Enter para continuar...")
    
    try:
        # Demo 1: Generación básica
        test_cases, user_story = demo_basic_generation()
        input("\nPresiona Enter para continuar al siguiente demo...")
        
        # Demo 2: Plantillas
        api_cases = demo_templates()
        input("\nPresiona Enter para continuar al siguiente demo...")
        
        # Demo 3: Validación
        validation_cases = demo_validation()
        input("\nPresiona Enter para continuar al siguiente demo...")
        
        # Demo 4: Exportación
        demo_export_formats(test_cases)
        input("\nPresiona Enter para continuar al siguiente demo...")
        
        # Demo 5: Integración Linear
        linear_issues = demo_linear_integration(test_cases)
        
        # Resumen final
        print_header("RESUMEN DEL DEMO")
        print("✅ Generación automática de casos de prueba")
        print("✅ Validación de calidad con métricas")
        print("✅ Plantillas especializadas (Web, Móvil, API)")
        print("✅ Exportación a múltiples formatos")
        print("✅ Integración con Linear para equipos QA")
        print("✅ Sistema configurable y extensible")
        
        print(f"\n📁 Archivos generados en este demo:")
        demo_files = ["demo_linear.json", "demo_linear.csv", "demo_casos.xlsx", "demo_casos.csv", "demo_casos.json"]
        for file in demo_files:
            if os.path.exists(file):
                print(f"  • {file}")
        
        print(f"\n🎉 ¡Demo completado exitosamente!")
        print(f"💡 Revisa los archivos generados para ver ejemplos reales")
        print(f"📖 Consulta GUIA_QA_LINEAR.md para instrucciones detalladas")
        
    except Exception as e:
        print(f"❌ Error durante el demo: {e}")
        print("💡 Asegúrate de que todas las dependencias estén instaladas")

if __name__ == "__main__":
    main()
