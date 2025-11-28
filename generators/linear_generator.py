#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de Casos de Prueba desde Linear
Permite generar casos de prueba directamente desde issues de Linear
"""

import json
import requests
import os
from typing import List, Dict, Any, Optional
from test_case_automation import UserStoryParser, TestCaseGenerator, QAValidator, TestCaseExporter
from test_templates import TemplateManager

class LinearAPI:
    """Cliente para la API de Linear"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('LINEAR_API_KEY')
        self.base_url = "https://api.linear.app/graphql"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def get_issues_by_label(self, label: str, team_id: str = None) -> List[Dict[str, Any]]:
        """Obtiene issues de Linear por label"""
        query = """
        query GetIssues($filter: IssueFilter) {
            issues(filter: $filter) {
                nodes {
                    id
                    title
                    description
                    labels {
                        nodes {
                            name
                        }
                    }
                    team {
                        name
                    }
                    state {
                        name
                    }
                    priority
                    assignee {
                        name
                    }
                }
            }
        }
        """
        
        variables = {
            "filter": {
                "labels": {"contains": [label]},
                "team": {"id": {"eq": team_id}} if team_id else None
            }
        }
        
        try:
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json={"query": query, "variables": variables}
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get('data', {}).get('issues', {}).get('nodes', [])
            else:
                print(f"❌ Error API Linear: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"❌ Error conectando con Linear: {e}")
            return []
    
    def get_issues_by_team(self, team_name: str) -> List[Dict[str, Any]]:
        """Obtiene issues de un equipo específico"""
        query = """
        query GetTeamIssues($teamName: String!) {
            team(name: $teamName) {
                issues {
                    nodes {
                        id
                        title
                        description
                        labels {
                            nodes {
                                name
                            }
                        }
                        state {
                            name
                        }
                        priority
                    }
                }
            }
        }
        """
        
        variables = {"teamName": team_name}
        
        try:
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json={"query": query, "variables": variables}
            )
            
            if response.status_code == 200:
                data = response.json()
                team_data = data.get('data', {}).get('team')
                if team_data:
                    return team_data.get('issues', {}).get('nodes', [])
            return []
                
        except Exception as e:
            print(f"❌ Error obteniendo issues del equipo: {e}")
            return []

class LinearTestCaseGenerator:
    """Generador de casos de prueba desde Linear"""
    
    def __init__(self, linear_api: LinearAPI = None):
        self.linear_api = linear_api or LinearAPI()
        self.parser = UserStoryParser()
        self.generator = TestCaseGenerator()
        self.validator = QAValidator()
        self.template_manager = TemplateManager()
    
    def generate_from_linear_issues(self, issues: List[Dict[str, Any]], template: str = None) -> List[Dict[str, Any]]:
        """Genera casos de prueba desde issues de Linear"""
        all_test_cases = []
        
        for issue in issues:
            # Convertir issue a historia de usuario
            user_story = self._convert_issue_to_user_story(issue)
            
            if user_story:
                # Generar casos de prueba
                test_cases = self.generator.generate_test_cases(user_story)
                
                # Aplicar plantilla si se especifica
                if template:
                    test_cases = self.template_manager.apply_template(template, user_story, test_cases)
                
                # Validar calidad
                validation_result = self.validator.validate_test_suite(test_cases)
                
                # Agregar metadatos de Linear
                for tc in test_cases:
                    tc_data = {
                        'test_case': tc,
                        'linear_issue': issue,
                        'validation': validation_result,
                        'template_used': template
                    }
                    all_test_cases.append(tc_data)
        
        return all_test_cases
    
    def _convert_issue_to_user_story(self, issue: Dict[str, Any]) -> Optional[Any]:
        """Convierte un issue de Linear a historia de usuario"""
        title = issue.get('title', '')
        description = issue.get('description', '')
        
        # Extraer labels
        labels = [label['name'] for label in issue.get('labels', {}).get('nodes', [])]
        
        # Crear historia de usuario estructurada
        user_story_text = f"""
        Historia de Usuario: {title}
        
        Como usuario del sistema
        Quiero {self._extract_want_from_title(title)}
        Para {self._extract_benefit_from_description(description)}
        
        Descripción:
        {description}
        
        Criterios de Aceptación:
        {self._extract_criteria_from_description(description)}
        """
        
        try:
            return self.parser.parse_from_text(user_story_text)
        except Exception as e:
            print(f"⚠️  Error parseando issue {title}: {e}")
            return None
    
    def _extract_want_from_title(self, title: str) -> str:
        """Extrae el 'quiero' del título del issue"""
        # Buscar patrones comunes
        if "login" in title.lower():
            return "poder iniciar sesión"
        elif "register" in title.lower() or "signup" in title.lower():
            return "poder registrarme"
        elif "profile" in title.lower():
            return "poder gestionar mi perfil"
        elif "search" in title.lower():
            return "poder buscar contenido"
        elif "payment" in title.lower() or "pago" in title.lower():
            return "poder realizar pagos"
        else:
            return f"poder usar la funcionalidad: {title.lower()}"
    
    def _extract_benefit_from_description(self, description: str) -> str:
        """Extrae el beneficio de la descripción"""
        if not description:
            return "cumplir con los requisitos del sistema"
        
        # Buscar frases que indiquen beneficio
        benefit_phrases = [
            "para poder", "para que", "para acceder", "para gestionar",
            "para realizar", "para ver", "para crear", "para modificar"
        ]
        
        for phrase in benefit_phrases:
            if phrase in description.lower():
                # Extraer la parte después de la frase
                parts = description.lower().split(phrase)
                if len(parts) > 1:
                    benefit = parts[1].split('.')[0].strip()
                    if benefit:
                        return benefit
        
        return "cumplir con los requisitos del sistema"
    
    def _extract_criteria_from_description(self, description: str) -> str:
        """Extrae criterios de aceptación de la descripción"""
        if not description:
            return "1. Dado que soy un usuario\n   Cuando uso la funcionalidad\n   Entonces debo obtener el resultado esperado"
        
        # Buscar criterios existentes
        criteria_indicators = [
            "dado que", "cuando", "entonces", "criterio", "acceptance",
            "debe", "debería", "requisito"
        ]
        
        lines = description.split('\n')
        criteria_lines = []
        
        for line in lines:
            line_lower = line.lower().strip()
            if any(indicator in line_lower for indicator in criteria_indicators):
                criteria_lines.append(line.strip())
        
        if criteria_lines:
            return '\n'.join(criteria_lines)
        else:
            return "1. Dado que soy un usuario\n   Cuando uso la funcionalidad\n   Entonces debo obtener el resultado esperado"

def main():
    """Función principal para generar desde Linear"""
    print("🔗 GENERADOR DE CASOS DE PRUEBA DESDE LINEAR")
    print("=" * 60)
    
    # Verificar API key
    api_key = os.getenv('LINEAR_API_KEY')
    if not api_key:
        print("⚠️  LINEAR_API_KEY no encontrada en variables de entorno")
        print("💡 Configura tu API key de Linear:")
        print("   set LINEAR_API_KEY=tu_api_key_aqui")
        print("\n🔄 Continuando con modo demo (sin API real)...")
        
        # Modo demo con datos simulados
        demo_mode()
        return
    
    # Crear cliente Linear
    linear_api = LinearAPI(api_key)
    generator = LinearTestCaseGenerator(linear_api)
    
    print("📋 Opciones disponibles:")
    print("1. Generar desde label específico")
    print("2. Generar desde equipo QA")
    print("3. Generar desde issues con criterios de aceptación")
    
    choice = input("\nSelecciona una opción (1-3): ").strip()
    
    if choice == "1":
        label = input("Ingresa el label a buscar: ").strip()
        issues = linear_api.get_issues_by_label(label)
        if issues:
            print(f"📋 {len(issues)} issues encontrados con label '{label}'")
            generate_and_export(generator, issues, label)
        else:
            print(f"❌ No se encontraron issues con label '{label}'")
    
    elif choice == "2":
        team_name = input("Ingresa el nombre del equipo: ").strip()
        issues = linear_api.get_issues_by_team(team_name)
        if issues:
            print(f"📋 {len(issues)} issues encontrados en equipo '{team_name}'")
            generate_and_export(generator, issues, team_name)
        else:
            print(f"❌ No se encontraron issues en equipo '{team_name}'")
    
    elif choice == "3":
        # Buscar issues que contengan criterios de aceptación
        print("🔍 Buscando issues con criterios de aceptación...")
        # Implementar búsqueda por contenido
        print("💡 Esta funcionalidad está en desarrollo")
    
    else:
        print("❌ Opción inválida")

def generate_and_export(generator: LinearTestCaseGenerator, issues: List[Dict[str, Any]], source: str):
    """Genera y exporta casos de prueba"""
    print(f"\n🧪 Generando casos de prueba desde {source}...")
    
    # Seleccionar plantilla
    print("\n🎨 Plantillas disponibles:")
    templates = generator.template_manager.get_available_templates()
    for i, template in enumerate(templates, 1):
        info = generator.template_manager.get_template_info(template)
        print(f"{i}. {info['name']}")
    
    template_choice = input(f"\nSelecciona plantilla (1-{len(templates)}) o Enter para ninguna: ").strip()
    selected_template = None
    
    if template_choice.isdigit():
        choice_num = int(template_choice)
        if 1 <= choice_num <= len(templates):
            selected_template = templates[choice_num - 1]
    
    # Generar casos
    test_cases_data = generator.generate_from_linear_issues(issues, selected_template)
    
    if not test_cases_data:
        print("❌ No se pudieron generar casos de prueba")
        return
    
    print(f"✅ {len(test_cases_data)} casos generados")
    
    # Exportar
    exporter = TestCaseExporter()
    test_cases = [data['test_case'] for data in test_cases_data]
    
    output_prefix = f"linear_{source.replace(' ', '_')}"
    
    try:
        exporter.export_to_excel(test_cases, f"{output_prefix}.xlsx")
        exporter.export_to_csv(test_cases, f"{output_prefix}.csv")
        exporter.export_to_json(test_cases, f"{output_prefix}.json")
        
        print(f"\n📤 Archivos exportados:")
        print(f"  • {output_prefix}.xlsx")
        print(f"  • {output_prefix}.csv")
        print(f"  • {output_prefix}.json")
        
        # Mostrar resumen de calidad
        if test_cases_data:
            avg_score = sum(data['validation']['average_score'] for data in test_cases_data) / len(test_cases_data)
            print(f"\n📊 Puntaje promedio de calidad: {avg_score:.1f}/100")
        
    except Exception as e:
        print(f"❌ Error exportando: {e}")

def demo_mode():
    """Modo demo sin API real"""
    print("\n🎬 MODO DEMO - Simulando integración con Linear")
    
    # Datos simulados
    demo_issues = [
        {
            "id": "demo-1",
            "title": "Sistema de Login",
            "description": "Implementar sistema de autenticación seguro\n\nCriterios:\n- Dado que soy usuario registrado\n- Cuando ingreso credenciales válidas\n- Entonces debo acceder al sistema",
            "labels": {"nodes": [{"name": "qa-testing"}]},
            "team": {"name": "QA"},
            "state": {"name": "Todo"},
            "priority": 1
        },
        {
            "id": "demo-2", 
            "title": "Carrito de Compras",
            "description": "Permitir agregar productos al carrito\n\nCriterios:\n- Dado que soy cliente\n- Cuando agrego producto al carrito\n- Entonces debo ver el producto en mi carrito",
            "labels": {"nodes": [{"name": "ecommerce"}]},
            "team": {"name": "QA"},
            "state": {"name": "Todo"},
            "priority": 2
        }
    ]
    
    print(f"📋 {len(demo_issues)} issues demo encontrados")
    
    # Generar casos
    generator = LinearTestCaseGenerator()
    test_cases_data = generator.generate_from_linear_issues(demo_issues, "web")
    
    print(f"✅ {len(test_cases_data)} casos generados desde Linear")
    
    # Exportar
    exporter = TestCaseExporter()
    test_cases = [data['test_case'] for data in test_cases_data]
    
    try:
        exporter.export_to_excel(test_cases, "linear_demo.xlsx")
        exporter.export_to_csv(test_cases, "linear_demo.csv")
        exporter.export_to_json(test_cases, "linear_demo.json")
        
        print(f"\n📤 Archivos demo exportados:")
        print(f"  • linear_demo.xlsx")
        print(f"  • linear_demo.csv") 
        print(f"  • linear_demo.json")
        
    except Exception as e:
        print(f"❌ Error exportando demo: {e}")

if __name__ == "__main__":
    main()
