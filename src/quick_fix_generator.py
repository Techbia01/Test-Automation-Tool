#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador Rápido de Casos de Prueba - Solución Directa
Arregla títulos repetidos, descripciones gigantes y mejora estructura
"""

import re
from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class QuickTestCase:
    """Caso de prueba con estructura mejorada"""
    id: str
    title: str
    description: str
    preconditions: List[str]
    steps: List[str]
    expected_result: str
    test_type: str
    priority: str
    tags: List[str]

class QuickTestGenerator:
    """Generador rápido que soluciona problemas inmediatos"""
    
    def __init__(self):
        self.test_counter = 1
        
    def generate_improved_cases(self, user_story, qa_comments: str = "") -> List[QuickTestCase]:
        """Genera casos de prueba mejorados con títulos únicos"""
        cases = []
        self.test_counter = 1
        
        # Analizar la historia de usuario
        story_analysis = self._analyze_user_story(user_story)
        
        # Generar casos específicos para cada criterio
        for i, criteria in enumerate(user_story.acceptance_criteria):
            case = self._create_specific_case(user_story, criteria, i + 1, story_analysis)
            cases.append(case)
        
        # Generar caso negativo
        negative_case = self._create_negative_case(user_story, story_analysis)
        cases.append(negative_case)
        
        return cases
    
    def _analyze_user_story(self, user_story) -> Dict[str, Any]:
        """Analiza la historia de usuario para extraer información clave"""
        full_text = f"{user_story.title} {user_story.description}".lower()
        
        # Detectar dominio
        domain = 'general'
        if any(word in full_text for word in ['login', 'sesión', 'autenticación', 'credenciales']):
            domain = 'autenticacion'
        elif any(word in full_text for word in ['factura', 'pago', 'cliente', 'producto']):
            domain = 'facturacion'
        elif any(word in full_text for word in ['inventario', 'stock', 'almacén', 'producto']):
            domain = 'inventario'
        
        # Extraer acción principal
        main_action = 'validar'
        if 'crear' in full_text or 'generar' in full_text:
            main_action = 'crear'
        elif 'editar' in full_text or 'modificar' in full_text:
            main_action = 'editar'
        elif 'eliminar' in full_text or 'borrar' in full_text:
            main_action = 'eliminar'
        elif 'buscar' in full_text or 'consultar' in full_text:
            main_action = 'consultar'
        
        return {
            'domain': domain,
            'main_action': main_action,
            'title_base': user_story.title[:50] if len(user_story.title) > 50 else user_story.title
        }
    
    def _create_specific_case(self, user_story, criteria: str, criteria_index: int, analysis: Dict[str, Any]) -> QuickTestCase:
        """Crea un caso específico para un criterio"""
        
        # Generar título único y descriptivo
        action_map = {
            'validar': 'Validar',
            'crear': 'Crear',
            'editar': 'Modificar',
            'eliminar': 'Eliminar',
            'consultar': 'Consultar'
        }
        
        # Generar título completo y claro SIN cortar palabras
        action_title = action_map.get(analysis['main_action'], 'Verificar')
        domain_context = self._get_domain_context(analysis['domain'])
        
        # Crear título descriptivo y completo
        if elements and len(elements) > 0:
            element = elements[0].replace('_', ' ').title()
            title = f"TC-{self.test_counter:03d}: {action_title} {element} en {domain_context}"
        else:
            title = f"TC-{self.test_counter:03d}: {action_title} {domain_context} - Escenario {criteria_index}"
        
        # Asegurar que el título no sea demasiado largo
        if len(title) > 80:
            title = f"TC-{self.test_counter:03d}: {action_title} funcionalidad - Escenario {criteria_index}"
        
        # Analizar criterio específico
        criteria_analysis = self._analyze_criteria(criteria)
        
        # Generar descripción concisa
        description = self._create_concise_description(criteria_analysis, domain_context)
        
        # Generar pasos estructurados
        preconditions = self._generate_preconditions(analysis['domain'])
        steps = self._generate_steps(criteria_analysis, analysis)
        expected_result = self._generate_expected_result(criteria_analysis)
        
        # Generar tags relevantes
        tags = [f"@{analysis['domain']}", f"@{analysis['main_action']}", "@funcional"]
        
        case = QuickTestCase(
            id=f"TC-{self.test_counter:03d}",
            title=title,
            description=description,
            preconditions=preconditions,
            steps=steps,
            expected_result=expected_result,
            test_type="Funcional",
            priority="Alta",
            tags=tags
        )
        
        self.test_counter += 1
        return case
    
    def _get_domain_context(self, domain: str) -> str:
        """Obtiene contexto específico del dominio"""
        contexts = {
            'autenticacion': 'proceso de autenticación',
            'facturacion': 'sistema de facturación',
            'inventario': 'gestión de inventario',
            'general': 'funcionalidad del sistema'
        }
        return contexts.get(domain, 'funcionalidad del sistema')
    
    def _analyze_criteria(self, criteria: str) -> Dict[str, str]:
        """Analiza un criterio específico"""
        criteria_lower = criteria.lower()
        
        # Extraer componentes Gherkin
        given_match = re.search(r'dado\s+que\s+(.+?)(?=cuando|entonces|$)', criteria_lower)
        when_match = re.search(r'cuando\s+(.+?)(?=entonces|dado|$)', criteria_lower)
        then_match = re.search(r'entonces\s+(.+?)(?=dado|cuando|$)', criteria_lower)
        
        return {
            'given': given_match.group(1).strip() if given_match else '',
            'when': when_match.group(1).strip() if when_match else '',
            'then': then_match.group(1).strip() if then_match else '',
            'full_criteria': criteria[:200] + '...' if len(criteria) > 200 else criteria
        }
    
    def _create_concise_description(self, criteria_analysis: Dict[str, str], context: str) -> str:
        """Crea una descripción CONCISA y bien formateada"""
        # Extraer solo lo esencial del criterio
        criteria_short = criteria_analysis['full_criteria']
        if len(criteria_short) > 150:
            criteria_short = criteria_short[:147] + "..."
        
        # Descripción corta y justificada
        description = f"""**Objetivo:** Verificar {context}

**Criterio:** {criteria_short}

**Tipo:** Funcional | **Prioridad:** Alta"""
        
        return description
    
    def _generate_preconditions(self, domain: str) -> List[str]:
        """Genera precondiciones específicas del dominio"""
        preconditions_map = {
            'autenticacion': [
                "El sistema está disponible y funcionando",
                "La página de login está accesible",
                "Los datos de prueba están configurados"
            ],
            'facturacion': [
                "El sistema de facturación está operativo",
                "Los datos de clientes están disponibles",
                "Los productos están configurados en el sistema"
            ],
            'inventario': [
                "El sistema de inventario está funcionando",
                "Los almacenes están configurados",
                "Los productos están registrados"
            ],
            'general': [
                "El sistema está operativo",
                "Los datos de prueba están disponibles",
                "El usuario tiene los permisos necesarios"
            ]
        }
        
        return preconditions_map.get(domain, preconditions_map['general'])
    
    def _generate_steps(self, criteria_analysis: Dict[str, str], analysis: Dict[str, Any]) -> List[str]:
        """Genera pasos de ejecución estructurados"""
        steps = []
        
        # Paso 1: Configuración inicial
        if criteria_analysis['given']:
            steps.append(f"Verificar que {criteria_analysis['given']}")
        else:
            steps.append("Acceder al sistema y navegar a la funcionalidad correspondiente")
        
        # Paso 2: Acción principal
        if criteria_analysis['when']:
            steps.append(f"Ejecutar la acción: {criteria_analysis['when']}")
        else:
            action_map = {
                'validar': 'Realizar la validación correspondiente',
                'crear': 'Crear el elemento según los parámetros',
                'editar': 'Modificar los datos necesarios',
                'eliminar': 'Eliminar el elemento seleccionado',
                'consultar': 'Realizar la consulta con los filtros apropiados'
            }
            steps.append(action_map.get(analysis['main_action'], 'Ejecutar la funcionalidad'))
        
        # Paso 3: Verificación
        steps.append("Verificar que el resultado obtenido es el esperado")
        
        return steps
    
    def _generate_expected_result(self, criteria_analysis: Dict[str, str]) -> str:
        """Genera resultado esperado específico"""
        if criteria_analysis['then']:
            return f"El sistema debe: {criteria_analysis['then']}"
        else:
            return "El sistema debe completar la operación exitosamente y mostrar el resultado apropiado"
    
    def _create_negative_case(self, user_story, analysis: Dict[str, Any]) -> QuickTestCase:
        """Crea un caso negativo"""
        domain_context = self._get_domain_context(analysis['domain'])
        
        title = f"TC-{self.test_counter:03d}: Validación de manejo de errores en {domain_context}"
        
        description = f"""**Objetivo:** Verificar manejo de errores en {domain_context}

**Criterio:** El sistema debe manejar errores y mostrar mensajes apropiados

**Tipo:** Negativo | **Prioridad:** Media"""
        
        preconditions = [
            "El sistema está operativo",
            "Se tienen datos inválidos para la prueba"
        ]
        
        steps = [
            "Acceder a la funcionalidad correspondiente",
            "Ingresar datos inválidos o realizar una acción incorrecta",
            "Verificar que el sistema maneja el error apropiadamente"
        ]
        
        expected_result = "El sistema debe mostrar un mensaje de error claro y mantener la estabilidad"
        
        case = QuickTestCase(
            id=f"TC-{self.test_counter:03d}",
            title=title,
            description=description,
            preconditions=preconditions,
            steps=steps,
            expected_result=expected_result,
            test_type="Negativo",
            priority="Media",
            tags=[f"@{analysis['domain']}", "@negativo", "@error-handling"]
        )
        
        self.test_counter += 1
        return case
