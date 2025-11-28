#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exportador Simplificado para Linear
Genera un solo archivo CSV optimizado para importación directa en Linear
"""

import os
import csv
import json
from datetime import datetime
from typing import List, Dict, Any
import re

class LinearSimpleExporter:
    """Exportador simplificado para Linear con un solo archivo CSV"""
    
    def __init__(self, output_folder: str = "outputs"):
        self.output_folder = output_folder
        os.makedirs(output_folder, exist_ok=True)
    
    def _sanitize_filename(self, filename: str) -> str:
        """Limpia el nombre de archivo de caracteres especiales"""
        # Reemplazar caracteres problemáticos
        replacements = {
            'ó': 'o', 'á': 'a', 'é': 'e', 'í': 'i', 'ú': 'u',
            'ñ': 'n', 'ü': 'u', 'ç': 'c',
            '<': '', '>': '', ':': '', '"': '', '/': '', '\\': '',
            '|': '', '?': '', '*': '', ' ': '_'
        }
        
        for old, new in replacements.items():
            filename = filename.replace(old, new)
        
        # Remover caracteres no ASCII
        filename = re.sub(r'[^\w\-_\.]', '', filename)
        
        # Limitar longitud
        if len(filename) > 50:
            filename = filename[:50]
        
        return filename
    
    def export_to_linear_csv(self, test_cases: List[Dict], project_name: str, user_story: str = "", parent_issue_id: str = "") -> str:
        """
        Exporta casos de prueba a un solo archivo CSV optimizado para Linear
        Puede exportar como issues independientes o como sub-issues de una HU
        """
        # Limpiar nombre del proyecto
        clean_project_name = self._sanitize_filename(project_name)
        
        # Crear nombre de archivo
        timestamp = datetime.now().strftime('%Y%m%d_%H%M')
        if parent_issue_id:
            filename = f"linear_subissues_{clean_project_name}_{timestamp}.csv"
        else:
            filename = f"linear_test_cases_{clean_project_name}_{timestamp}.csv"
        filepath = os.path.join(self.output_folder, filename)
        
        # Preparar datos para CSV
        csv_data = []
        
        for i, test_case in enumerate(test_cases, 1):
            # Crear descripción estructurada para Linear
            description = self._create_linear_description(test_case, user_story)
            
            # Mapear prioridad a formato Linear
            priority = self._map_priority_to_linear(test_case.get('priority', 'medium'))
            
            # Crear etiquetas
            labels = self._create_linear_labels(test_case)
            
            # Crear fila para CSV
            row = {
                'Title': f"TC-{i:03d}: {test_case.get('title', 'Sin título')}",
                'Description': description,
                'Labels': labels,
                'Priority': priority,
                'Type': 'Test Case',
                'State': 'Todo',
                'Assignee': '',  # Se puede asignar manualmente en Linear
                'Project': project_name,
                'Created': datetime.now().strftime('%Y-%m-%d'),
                'Test_ID': test_case.get('id', f'TC-{i:03d}'),
                'Test_Type': test_case.get('test_type', 'Funcional'),
                'Original_Priority': test_case.get('priority', 'Media'),
                'Tags': ', '.join(test_case.get('tags', [])),
                'User_Story': user_story[:100] + '...' if len(user_story) > 100 else user_story,
                'Parent': parent_issue_id if parent_issue_id else ''  # Para sub-issues
            }
            
            csv_data.append(row)
        
        # Escribir CSV con encoding UTF-8 y BOM para Excel (corrige tildes)
        with open(filepath, 'w', newline='', encoding='utf-8-sig') as csvfile:
            if csv_data:
                fieldnames = csv_data[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(csv_data)
        
        return filepath
    
    def export_as_subissues(self, test_cases: List[Dict], project_name: str, parent_issue_id: str, user_story: str = "") -> str:
        """
        Exporta casos de prueba como sub-issues de una Historia de Usuario específica
        """
        return self.export_to_linear_csv(test_cases, project_name, user_story, parent_issue_id)
    
    def _create_linear_description(self, test_case: Dict, user_story: str = "") -> str:
        """Crea descripción optimizada para Linear con estructura exacta"""
        description = f"**Objetivo:** {test_case.get('title', 'Sin título')}\n\n"
        
        # Curl si aplica (para casos de API)
        if test_case.get('test_type', '').lower() in ['api', 'integración']:
            description += "**Curl (Si aplica):**\n```\n# Agregar comando curl aquí si es necesario\n```\n\n"
        
        if test_case.get('preconditions'):
            description += "**Precondiciones:**\n"
            preconditions = test_case['preconditions']
            if isinstance(preconditions, list):
                for i, precond in enumerate(preconditions, 1):
                    description += f"{i}. {precond}\n"
            else:
                description += f"• {preconditions}\n"
            description += "\n"
        
        if test_case.get('steps'):
            description += "**Descripción (formato Gherkin):**\n"
            steps = test_case['steps']
            if isinstance(steps, list):
                for i, step in enumerate(steps, 1):
                    description += f"{i}. {step}\n"
            else:
                description += f"• {steps}\n"
            description += "\n"
        
        if test_case.get('expected_result'):
            description += f"**Resultado Esperado:** {test_case['expected_result']}\n\n"
        
        # Agregar información técnica
        description += "---\n"
        description += f"**Tipo:** {test_case.get('test_type', 'N/A')}\n"
        description += f"**Prioridad:** {test_case.get('priority', 'N/A')}\n"
        if test_case.get('tags'):
            description += f"**Tags:** {', '.join(test_case['tags'])}\n"
        
        # Agregar contexto de la historia de usuario si es relevante
        if user_story and len(user_story) > 0:
            description += f"\n**Contexto HU:** {user_story[:200]}{'...' if len(user_story) > 200 else ''}\n"
        
        return description
    
    def _create_linear_labels(self, test_case: Dict) -> str:
        """Crea etiquetas para Linear separadas por comas"""
        labels = ['Test_Case']
        
        # Agregar tipo como etiqueta
        test_type = test_case.get('test_type', '').lower()
        if test_type:
            # Limpiar tipo para etiqueta
            clean_type = test_type.replace(' ', '_').replace('ó', 'o').replace('ñ', 'n')
            labels.append(f"Type_{clean_type}")
        
        # Agregar prioridad como etiqueta
        priority = test_case.get('priority', '').lower()
        if priority:
            clean_priority = priority.replace(' ', '_').replace('ó', 'o')
            labels.append(f"Priority_{clean_priority}")
        
        # Agregar tags personalizados
        if test_case.get('tags'):
            for tag in test_case['tags']:
                clean_tag = tag.replace(' ', '_').replace('ó', 'o').replace('ñ', 'n')
                labels.append(clean_tag)
        
        return ', '.join(labels)
    
    def _map_priority_to_linear(self, priority: str) -> str:
        """Mapea prioridad a formato Linear"""
        priority_map = {
            'alta': 'Urgent',
            'high': 'Urgent',
            'media': 'High', 
            'medium': 'High',
            'baja': 'Normal',
            'low': 'Normal'
        }
        return priority_map.get(priority.lower(), 'Normal')

def main():
    """Función principal para pruebas"""
    # Ejemplo de uso
    test_cases = [
        {
            'id': 'TC-001',
            'title': 'Verificar login con credenciales válidas',
            'description': 'Verificar que el usuario puede iniciar sesión con credenciales correctas',
            'test_type': 'Funcional',
            'priority': 'Alta',
            'preconditions': ['Usuario registrado en el sistema', 'Credenciales válidas disponibles'],
            'steps': ['Navegar a la página de login', 'Ingresar email válido', 'Ingresar contraseña válida', 'Hacer clic en "Iniciar Sesión"'],
            'expected_result': 'El usuario es redirigido al dashboard principal',
            'tags': ['login', 'autenticación', 'happy-path'],
            'user_story': 'Como usuario del sistema, quiero poder iniciar sesión'
        }
    ]
    
    exporter = LinearSimpleExporter()
    csv_file = exporter.export_to_linear_csv(test_cases, "Sistema de Login", "Historia de usuario de login")
    print(f"✅ Exportado a Linear CSV: {csv_file}")

if __name__ == "__main__":
    main()
