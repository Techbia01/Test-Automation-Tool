#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador Interactivo de Casos de Prueba
Interfaz de usuario amigable para crear casos de prueba
"""

from test_case_automation import UserStoryParser, TestCaseGenerator, TestCaseExporter, QAValidator
from test_templates import TemplateManager
import os
import sys

def print_banner():
    """Muestra el banner de bienvenida"""
    print("=" * 60)
    print("🧪 AUTOMATIZADOR DE CASOS DE PRUEBA PARA QA")
    print("=" * 60)
    print("Genera casos de prueba automáticamente desde historias de usuario")
    print()

def get_user_input():
    """Obtiene la entrada del usuario de forma interactiva"""
    print("📝 OPCIONES DE ENTRADA:")
    print("1. Ingresar historia de usuario manualmente")
    print("2. Cargar desde archivo")
    print("3. Usar ejemplo predefinido")
    
    choice = input("\nSelecciona una opción (1-3): ").strip()
    
    if choice == "1":
        return get_manual_input()
    elif choice == "2":
        return get_file_input()
    elif choice == "3":
        return get_example_input()
    else:
        print("❌ Opción inválida")
        return None

def get_manual_input():
    """Obtiene entrada manual del usuario"""
    print("\n📋 INGRESA TU HISTORIA DE USUARIO:")
    print("(Presiona Enter en una línea vacía para terminar)")
    print()
    
    lines = []
    while True:
        line = input()
        if line.strip() == "":
            break
        lines.append(line)
    
    return "\n".join(lines)

def get_file_input():
    """Obtiene entrada desde archivo"""
    filename = input("\n📁 Ingresa la ruta del archivo: ").strip()
    
    if not os.path.exists(filename):
        print(f"❌ El archivo {filename} no existe")
        return None
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"❌ Error al leer el archivo: {e}")
        return None

def get_example_input():
    """Usa el ejemplo predefinido"""
    example_file = "example_user_story.txt"
    
    if not os.path.exists(example_file):
        print(f"❌ El archivo de ejemplo {example_file} no existe")
        return None
    
    try:
        with open(example_file, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"❌ Error al leer el archivo de ejemplo: {e}")
        return None

def get_export_options():
    """Obtiene las opciones de exportación"""
    print("\n📤 OPCIONES DE EXPORTACIÓN:")
    print("1. Excel (.xlsx)")
    print("2. CSV (.csv)")
    print("3. JSON (.json)")
    print("4. Todos los formatos")
    
    choice = input("\nSelecciona formato (1-4): ").strip()
    
    formats = {
        "1": "excel",
        "2": "csv", 
        "3": "json",
        "4": "all"
    }
    
    return formats.get(choice, "all")

def get_template_selection():
    """Obtiene la selección de plantilla"""
    print("\n🎨 PLANTILLAS DISPONIBLES:")
    template_manager = TemplateManager()
    templates = template_manager.get_available_templates()
    
    for i, template_name in enumerate(templates, 1):
        info = template_manager.get_template_info(template_name)
        print(f"{i}. {info['name']} - {info['description']}")
    
    print(f"{len(templates) + 1}. Sin plantilla (casos básicos)")
    
    choice = input(f"\nSelecciona una plantilla (1-{len(templates) + 1}): ").strip()
    
    try:
        choice_num = int(choice)
        if 1 <= choice_num <= len(templates):
            return templates[choice_num - 1]
        elif choice_num == len(templates) + 1:
            return None
        else:
            print("❌ Opción inválida, usando casos básicos")
            return None
    except ValueError:
        print("❌ Opción inválida, usando casos básicos")
        return None

def get_output_filename():
    """Obtiene el nombre del archivo de salida"""
    default = "test_cases"
    filename = input(f"\n📄 Nombre del archivo de salida (default: {default}): ").strip()
    return filename if filename else default

def main():
    """Función principal interactiva"""
    print_banner()
    
    # Obtener entrada del usuario
    user_input = get_user_input()
    if not user_input:
        print("❌ No se pudo obtener la entrada del usuario")
        return
    
    print("\n🔄 Procesando historia de usuario...")
    
    # Parsear historia de usuario
    parser = UserStoryParser()
    user_story = parser.parse_from_text(user_input)
    
    print(f"✅ Historia parseada: {user_story.title}")
    print(f"📝 Criterios encontrados: {len(user_story.acceptance_criteria)}")
    
    # Mostrar criterios encontrados
    if user_story.acceptance_criteria:
        print("\n📋 CRITERIOS DE ACEPTACIÓN ENCONTRADOS:")
        for i, criteria in enumerate(user_story.acceptance_criteria, 1):
            print(f"  {i}. {criteria}")
    
    # Seleccionar plantilla
    selected_template = get_template_selection()
    
    # Generar casos de prueba
    print("\n🧪 Generando casos de prueba...")
    generator = TestCaseGenerator()
    base_test_cases = generator.generate_test_cases(user_story)
    
    # Aplicar plantilla si se seleccionó una
    if selected_template:
        print(f"🎨 Aplicando plantilla: {selected_template}")
        template_manager = TemplateManager()
        test_cases = template_manager.apply_template(selected_template, user_story, base_test_cases)
        print(f"✅ Plantilla aplicada. Casos adicionales generados: {len(test_cases) - len(base_test_cases)}")
    else:
        test_cases = base_test_cases
    
    print(f"✅ Casos generados: {len(test_cases)}")
    
    # Mostrar resumen de casos generados
    print("\n📊 RESUMEN DE CASOS GENERADOS:")
    test_types = {}
    for tc in test_cases:
        test_type = tc.test_type.value
        test_types[test_type] = test_types.get(test_type, 0) + 1
    
    for test_type, count in test_types.items():
        print(f"  • {test_type}: {count} casos")
    
    # Validación de QA
    print("\n🔍 VALIDACIÓN DE CALIDAD QA:")
    validator = QAValidator()
    validation_result = validator.validate_test_suite(test_cases)
    
    print(f"  📈 Puntaje promedio: {validation_result['average_score']}/100")
    print(f"  🎯 Calidad general: {validation_result['overall_quality']}")
    print(f"  ✅ Casos válidos: {validation_result['valid_cases']}/{validation_result['total_cases']}")
    print(f"  📊 Cobertura: {validation_result['coverage_score']}%")
    
    # Mostrar recomendaciones si las hay
    if validation_result['recommendations']:
        print("\n💡 RECOMENDACIONES:")
        for rec in validation_result['recommendations']:
            print(f"  • {rec}")
    
    # Mostrar casos con problemas
    problematic_cases = [r for r in validation_result['individual_results'] if not r['is_valid']]
    if problematic_cases:
        print(f"\n⚠️  CASOS CON PROBLEMAS ({len(problematic_cases)}):")
        for case in problematic_cases[:3]:  # Mostrar solo los primeros 3
            print(f"  • {case['test_case_id']}: {', '.join(case['issues'])}")
        if len(problematic_cases) > 3:
            print(f"  ... y {len(problematic_cases) - 3} casos más")
    
    # Obtener opciones de exportación
    export_format = get_export_options()
    output_filename = get_output_filename()
    
    # Exportar casos de prueba
    print("\n💾 Exportando casos de prueba...")
    exporter = TestCaseExporter()
    
    try:
        if export_format in ["excel", "all"]:
            exporter.export_to_excel(test_cases, f"{output_filename}.xlsx")
        
        if export_format in ["csv", "all"]:
            exporter.export_to_csv(test_cases, f"{output_filename}.csv")
        
        if export_format in ["json", "all"]:
            exporter.export_to_json(test_cases, f"{output_filename}.json")
        
        print("\n🎉 ¡Automatización completada exitosamente!")
        print(f"📁 Archivos generados en el directorio actual")
        
    except Exception as e:
        print(f"❌ Error durante la exportación: {e}")

if __name__ == "__main__":
    main()
