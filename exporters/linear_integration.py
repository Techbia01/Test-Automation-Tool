#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Integración con Linear para Equipos QA
Convierte casos de prueba generados a formato compatible con Linear
"""

import json
import csv
import pandas as pd
from typing import List, Dict, Any
from test_case_automation import TestCase, TestType, Priority

class LinearExporter:
    """Exportador especializado para Linear"""
    
    def __init__(self):
        self.linear_template = {
            "title": "",
            "description": "",
            "labels": [],
            "priority": 0,
            "assignee": "",
            "state": "Todo",
            "team": "QA"
        }
    
    def export_to_linear_format(self, test_cases: List[TestCase], output_file: str = "linear_import.json"):
        """Exporta casos de prueba en formato compatible con Linear"""
        linear_issues = []
        
        for tc in test_cases:
            # Convertir caso de prueba a formato Linear
            linear_issue = self._convert_to_linear_issue(tc)
            linear_issues.append(linear_issue)
        
        # Guardar en formato JSON para importar a Linear
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(linear_issues, f, indent=2, ensure_ascii=False)
        
        print(f"✅ {len(linear_issues)} casos exportados para Linear en {output_file}")
        return linear_issues
    
    def _convert_to_linear_issue(self, test_case: TestCase) -> Dict[str, Any]:
        """Convierte un caso de prueba a formato de issue de Linear"""
        
        # Mapear prioridad
        priority_map = {
            Priority.HIGH: 1,
            Priority.MEDIUM: 2,
            Priority.LOW: 3
        }
        
        # Mapear tipo de prueba a labels
        type_labels = {
            TestType.FUNCTIONAL: "funcional",
            TestType.INTEGRATION: "integración",
            TestType.EDGE_CASE: "caso-límite",
            TestType.NEGATIVE: "negativo",
            TestType.PERFORMANCE: "rendimiento",
            TestType.SECURITY: "seguridad"
        }
        
        # Crear descripción detallada
        description = f"""## Descripción
{test_case.description}

## Precondiciones
{chr(10).join(f"- {pre}" for pre in test_case.preconditions)}

## Pasos de Prueba
{chr(10).join(f"{i+1}. {step}" for i, step in enumerate(test_case.steps))}

## Resultado Esperado
{test_case.expected_result}

## Información Adicional
- **Historia de Usuario**: {test_case.user_story}
- **Tags**: {', '.join(test_case.tags)}
"""
        
        return {
            "title": f"[TC-{test_case.id}] {test_case.title}",
            "description": description,
            "labels": [type_labels.get(test_case.test_type, "general")] + test_case.tags,
            "priority": priority_map.get(test_case.priority, 2),
            "assignee": "",  # Se puede asignar después
            "state": "Todo",
            "team": "QA",
            "metadata": {
                "test_case_id": test_case.id,
                "test_type": test_case.test_type.value,
                "priority": test_case.priority.value,
                "user_story": test_case.user_story
            }
        }
    
    def create_linear_import_template(self, test_cases: List[TestCase], output_file: str = "linear_import_template.csv"):
        """Crea template CSV para importar a Linear manualmente"""
        
        data = []
        for test_case in test_cases:
            data.append({
                "Title": f"[TC-{test_case.id}] {test_case.title}",
                "Description": self._create_linear_description(test_case),
                "Labels": f"qa,{test_case.test_type.value.lower()},{','.join(test_case.tags)}",
                "Priority": test_case.priority.value,
                "State": "Todo",
                "Team": "QA",
                "Test Case ID": test_case.id,
                "Test Type": test_case.test_type.value,
                "User Story": test_case.user_story
            })
        
        df = pd.DataFrame(data)
        df.to_csv(output_file, index=False, encoding='utf-8')
        print(f"✅ Template CSV creado: {output_file}")
        return output_file
    
    def _create_linear_description(self, test_case: TestCase) -> str:
        """Crea descripción optimizada para Linear"""
        return f"""**Descripción:** {test_case.description}

**Precondiciones:**
{chr(10).join(f"• {pre}" for pre in test_case.preconditions)}

**Pasos:**
{chr(10).join(f"{i+1}. {step}" for i, step in enumerate(test_case.steps))}

**Resultado Esperado:** {test_case.expected_result}

**Historia de Usuario:** {test_case.user_story}"""

def main():
    """Función principal para integración con Linear"""
    print("🔗 INTEGRACIÓN CON LINEAR PARA QA")
    print("=" * 50)
    
    # Cargar casos de prueba desde archivo JSON
    try:
        with open('casos_login.json', 'r', encoding='utf-8') as f:
            test_cases_data = json.load(f)
        
        # Convertir datos JSON a objetos TestCase
        test_cases = []
        for data in test_cases_data:
            tc = TestCase(
                id=data['id'],
                title=data['title'],
                description=data['description'],
                preconditions=data['preconditions'],
                steps=data['steps'],
                expected_result=data['expected_result'],
                test_type=TestType(data['test_type']),
                priority=Priority(data['priority']),
                user_story=data['user_story'],
                tags=data['tags']
            )
            test_cases.append(tc)
        
        print(f"📋 {len(test_cases)} casos de prueba cargados")
        
        # Crear exportador Linear
        exporter = LinearExporter()
        
        # Exportar en formato JSON para Linear
        linear_issues = exporter.export_to_linear_format(test_cases, "linear_issues.json")
        
        # Crear template CSV
        exporter.create_linear_import_template(test_cases, "linear_import.csv")
        
        # Mostrar resumen
        print("\n📊 RESUMEN PARA LINEAR:")
        print(f"  • Total de issues: {len(linear_issues)}")
        
        # Contar por tipo
        type_counts = {}
        for test_case in test_cases:
            type_name = test_case.test_type.value
            type_counts[type_name] = type_counts.get(type_name, 0) + 1
        
        print("  • Por tipo de prueba:")
        for test_type, count in type_counts.items():
            print(f"    - {test_type}: {count} casos")
        
        print("\n💡 INSTRUCCIONES PARA LINEAR:")
        print("1. Abre Linear y ve a tu equipo QA")
        print("2. Usa 'linear_import.csv' para importar casos masivamente")
        print("3. O copia manualmente desde 'linear_issues.json'")
        print("4. Asigna casos a miembros del equipo")
        print("5. Organiza por sprints o milestones")
        
    except FileNotFoundError:
        print("❌ No se encontró el archivo 'casos_login.json'")
        print("   Ejecuta primero: python test_case_automation.py ejemplo_login.txt --output casos_login")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
