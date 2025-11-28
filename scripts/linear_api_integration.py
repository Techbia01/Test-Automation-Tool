#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Integración Automática con Linear API
Sube casos de prueba directamente sin CSV manual
"""

import os
import json
import requests
from typing import List, Dict, Any
from datetime import datetime

class LinearAPIIntegration:
    """Integración directa con Linear API"""
    
    def __init__(self, api_key: str, team_id: str):
        self.api_key = api_key
        self.team_id = team_id
        self.base_url = "https://api.linear.app/graphql"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def create_test_case_issue(self, test_case: Dict[str, Any]) -> str:
        """Crea un issue en Linear para un caso de prueba"""
        
        # Preparar descripción
        description = self._format_description(test_case)
        
        # Preparar etiquetas
        label_ids = self._get_or_create_labels(test_case)
        
        # Mapear prioridad
        priority = self._map_priority(test_case.get('priority', 'media'))
        
        # Mutation GraphQL para crear issue
        mutation = """
        mutation CreateIssue($input: IssueCreateInput!) {
            issueCreate(input: $input) {
                success
                issue {
                    id
                    identifier
                    title
                    url
                }
            }
        }
        """
        
        variables = {
            "input": {
                "teamId": self.team_id,
                "title": f"TC-{test_case.get('id', '001')}: {test_case.get('title', 'Sin título')}",
                "description": description,
                "priority": priority,
                "labelIds": label_ids,
                "stateId": self._get_todo_state_id()
            }
        }
        
        response = requests.post(
            self.base_url,
            headers=self.headers,
            json={"query": mutation, "variables": variables}
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('data', {}).get('issueCreate', {}).get('success'):
                issue = result['data']['issueCreate']['issue']
                print(f"✅ Creado: {issue['identifier']} - {issue['title']}")
                return issue['id']
            else:
                print(f"❌ Error creando issue: {result}")
                return None
        else:
            print(f"❌ Error HTTP: {response.status_code}")
            return None
    
    def _format_description(self, test_case: Dict[str, Any]) -> str:
        """Formatea la descripción para Linear"""
        description = f"**Objetivo:** {test_case.get('title', 'Sin título')}\n\n"
        
        if test_case.get('preconditions'):
            description += "**Precondiciones:**\n"
            for i, precond in enumerate(test_case['preconditions'], 1):
                description += f"{i}. {precond}\n"
            description += "\n"
        
        if test_case.get('steps'):
            description += "**Pasos de Ejecución:**\n"
            for i, step in enumerate(test_case['steps'], 1):
                description += f"{i}. {step}\n"
            description += "\n"
        
        if test_case.get('expected_result'):
            description += f"**Resultado Esperado:** {test_case['expected_result']}\n\n"
        
        description += "---\n"
        description += f"**Tipo:** {test_case.get('test_type', 'N/A')}\n"
        description += f"**Prioridad:** {test_case.get('priority', 'N/A')}\n"
        
        if test_case.get('tags'):
            description += f"**Tags:** {', '.join(test_case['tags'])}\n"
        
        return description
    
    def _get_or_create_labels(self, test_case: Dict[str, Any]) -> List[str]:
        """Obtiene o crea etiquetas necesarias"""
        # Esta función requeriría implementar la lógica de etiquetas
        # Por simplicidad, retornamos IDs de ejemplo
        return []
    
    def _map_priority(self, priority: str) -> int:
        """Mapea prioridad a valores Linear"""
        priority_map = {
            'alta': 1,    # Urgent
            'high': 1,
            'media': 2,   # High  
            'medium': 2,
            'baja': 3,    # Normal
            'low': 3
        }
        return priority_map.get(priority.lower(), 3)
    
    def _get_todo_state_id(self) -> str:
        """Obtiene el ID del estado 'Todo'"""
        # Esta función requeriría una query para obtener estados
        # Por simplicidad, retornamos un ID de ejemplo
        return "todo-state-id"
    
    def bulk_import_test_cases(self, test_cases: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Importa múltiples casos de prueba"""
        results = {
            'success': 0,
            'failed': 0,
            'issues': []
        }
        
        for test_case in test_cases:
            issue_id = self.create_test_case_issue(test_case)
            if issue_id:
                results['success'] += 1
                results['issues'].append(issue_id)
            else:
                results['failed'] += 1
        
        return results

def setup_linear_integration():
    """Configuración inicial de la integración"""
    print("🔧 CONFIGURACIÓN DE LINEAR API")
    print("=" * 40)
    
    # Solicitar credenciales
    api_key = input("Ingresa tu Linear API Key: ")
    team_id = input("Ingresa tu Team ID: ")
    
    # Guardar configuración
    config = {
        "api_key": api_key,
        "team_id": team_id,
        "created_at": datetime.now().isoformat()
    }
    
    with open('.linear_config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print("✅ Configuración guardada en .linear_config.json")
    print("\n📋 PRÓXIMOS PASOS:")
    print("1. Verifica que tu API Key tenga permisos de escritura")
    print("2. Confirma que el Team ID es correcto")
    print("3. Ejecuta una prueba de importación")

def main():
    """Función principal"""
    # Ejemplo de uso
    test_cases = [
        {
            'id': 'TC-001',
            'title': 'Verificar login con credenciales válidas',
            'test_type': 'Funcional',
            'priority': 'Alta',
            'preconditions': ['Usuario registrado', 'Credenciales válidas'],
            'steps': ['Navegar a login', 'Ingresar datos', 'Hacer clic'],
            'expected_result': 'Usuario logueado correctamente',
            'tags': ['login', 'autenticación']
        }
    ]
    
    # Cargar configuración
    try:
        with open('.linear_config.json', 'r') as f:
            config = json.load(f)
        
        # Crear integración
        linear = LinearAPIIntegration(
            api_key=config['api_key'],
            team_id=config['team_id']
        )
        
        # Importar casos
        results = linear.bulk_import_test_cases(test_cases)
        
        print(f"✅ Importación completada:")
        print(f"  - Exitosos: {results['success']}")
        print(f"  - Fallidos: {results['failed']}")
        
    except FileNotFoundError:
        print("❌ No se encontró configuración. Ejecuta setup_linear_integration() primero.")

if __name__ == "__main__":
    # Descomentar para configurar por primera vez
    # setup_linear_integration()
    
    # Ejecutar importación
    main()
