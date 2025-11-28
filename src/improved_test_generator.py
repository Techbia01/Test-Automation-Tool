#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador Mejorado de Casos de Prueba
Soluciona problemas de títulos repetidos, descripciones gigantes y mejor estructura
"""

import re
import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from test_case_automation import UserStory, TestCase, TestType, Priority

@dataclass
class ImprovedTestCase:
    """Caso de prueba mejorado con estructura clara"""
    id: str
    title: str
    feature: str
    scenario: str
    given_steps: List[str]
    when_steps: List[str]
    then_steps: List[str]
    tags: List[str]
    test_type: str
    priority: str
    user_story: str
    preconditions: List[str]
    
    def __post_init__(self):
        if self.given_steps is None:
            self.given_steps = []
        if self.when_steps is None:
            self.when_steps = []
        if self.then_steps is None:
            self.then_steps = []
        if self.tags is None:
            self.tags = []
        if self.preconditions is None:
            self.preconditions = []

class ImprovedTestGenerator:
    """Generador mejorado que soluciona problemas de títulos y descripciones"""
    
    def __init__(self):
        self.test_counter = 1
        self.action_patterns = {
            'validar': ['validar', 'verificar', 'comprobar', 'confirmar'],
            'crear': ['crear', 'generar', 'establecer', 'configurar'],
            'editar': ['editar', 'modificar', 'actualizar', 'cambiar'],
            'eliminar': ['eliminar', 'borrar', 'remover', 'quitar'],
            'buscar': ['buscar', 'consultar', 'encontrar', 'localizar'],
            'mostrar': ['mostrar', 'visualizar', 'presentar', 'exhibir'],
            'navegar': ['navegar', 'acceder', 'ir', 'dirigir'],
            'procesar': ['procesar', 'ejecutar', 'realizar', 'completar']
        }
        
        self.domain_contexts = {
            'autenticacion': {
                'elementos': ['formulario de login', 'campo de email', 'campo de contraseña', 'botón iniciar sesión'],
                'acciones': ['iniciar sesión', 'validar credenciales', 'mostrar error', 'redirigir'],
                'estados': ['autenticado', 'no autenticado', 'credenciales inválidas']
            },
            'facturacion': {
                'elementos': ['factura', 'cliente', 'producto', 'impuesto', 'total'],
                'acciones': ['generar factura', 'calcular impuestos', 'enviar por email', 'guardar'],
                'estados': ['borrador', 'enviada', 'pagada', 'vencida']
            },
            'inventario': {
                'elementos': ['producto', 'stock', 'almacén', 'categoría', 'proveedor'],
                'acciones': ['agregar producto', 'actualizar stock', 'generar reporte', 'alertar'],
                'estados': ['disponible', 'agotado', 'descontinuado', 'en tránsito']
            }
        }
    
    def generate_improved_cases(self, user_story: UserStory, qa_comments: str = "") -> List[ImprovedTestCase]:
        """Genera casos de prueba mejorados con títulos únicos y descripciones concisas"""
        improved_cases = []
        self.test_counter = 1
        
        # Analizar contexto del dominio
        domain_context = self._analyze_domain_context(user_story, qa_comments)
        
        # Generar casos específicos para cada criterio
        for i, criteria in enumerate(user_story.acceptance_criteria):
            cases = self._generate_specific_cases_for_criteria(
                user_story, criteria, i + 1, domain_context
            )
            improved_cases.extend(cases)
        
        # Generar casos adicionales (edge cases, negativos)
        improved_cases.extend(self._generate_additional_cases(user_story, domain_context))
        
        return improved_cases
    
    def _analyze_domain_context(self, user_story: UserStory, qa_comments: str) -> Dict[str, Any]:
        """Analiza el contexto del dominio para generar casos más específicos"""
        full_text = f"{user_story.title} {user_story.description} {qa_comments}".lower()
        
        # Detectar dominio principal
        detected_domain = 'general'
        for domain, context in self.domain_contexts.items():
            if any(keyword in full_text for keyword in context['elementos'] + context['acciones']):
                detected_domain = domain
                break
        
        # Extraer elementos clave
        key_elements = self._extract_key_elements(full_text)
        main_actions = self._extract_main_actions(full_text)
        
        return {
            'domain': detected_domain,
            'key_elements': key_elements,
            'main_actions': main_actions,
            'context': self.domain_contexts.get(detected_domain, {})
        }
    
    def _extract_key_elements(self, text: str) -> List[str]:
        """Extrae elementos clave del texto"""
        elements = []
        
        # Patrones para elementos UI
        ui_patterns = [
            r'botón\s+(\w+)', r'campo\s+(\w+)', r'formulario\s+(\w+)',
            r'tabla\s+(\w+)', r'modal\s+(\w+)', r'página\s+(\w+)'
        ]
        
        for pattern in ui_patterns:
            matches = re.findall(pattern, text)
            elements.extend(matches)
        
        # Elementos de negocio
        business_patterns = [
            r'(\w+)\s+del\s+sistema', r'(\w+)\s+de\s+la\s+aplicación',
            r'(\w+)\s+embebida', r'(\w+)\s+condicional'
        ]
        
        for pattern in business_patterns:
            matches = re.findall(pattern, text)
            elements.extend(matches)
        
        return list(set(elements))[:5]  # Máximo 5 elementos
    
    def _extract_main_actions(self, text: str) -> List[str]:
        """Extrae las acciones principales del texto"""
        actions = []
        
        for action_type, keywords in self.action_patterns.items():
            if any(keyword in text for keyword in keywords):
                actions.append(action_type)
        
        return actions[:3]  # Máximo 3 acciones principales
    
    def _generate_specific_cases_for_criteria(self, user_story: UserStory, criteria: str, 
                                            criteria_index: int, context: Dict[str, Any]) -> List[ImprovedTestCase]:
        """Genera casos específicos para un criterio de aceptación"""
        cases = []
        
        # Analizar el criterio específico
        criteria_analysis = self._analyze_criteria(criteria, context)
        
        # Generar caso principal (happy path)
        main_case = self._create_main_case(
            user_story, criteria, criteria_index, criteria_analysis, context
        )
        cases.append(main_case)
        
        # Generar caso alternativo si aplica
        if criteria_analysis['has_alternatives']:
            alt_case = self._create_alternative_case(
                user_story, criteria, criteria_index, criteria_analysis, context
            )
            cases.append(alt_case)
        
        return cases
    
    def _analyze_criteria(self, criteria: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analiza un criterio específico para extraer información relevante"""
        criteria_lower = criteria.lower()
        
        # Extraer componentes Gherkin
        given_match = re.search(r'dado\s+que\s+(.+?)(?=cuando|entonces|$)', criteria_lower)
        when_match = re.search(r'cuando\s+(.+?)(?=entonces|dado|$)', criteria_lower)
        then_match = re.search(r'entonces\s+(.+?)(?=dado|cuando|$)', criteria_lower)
        
        # Detectar si hay alternativas
        has_alternatives = any(word in criteria_lower for word in ['o', 'alternativamente', 'también'])
        
        # Extraer acción principal
        main_action = self._extract_action_from_criteria(criteria_lower)
        
        # Detectar elementos específicos
        specific_elements = self._extract_specific_elements(criteria_lower, context)
        
        return {
            'given': given_match.group(1).strip() if given_match else '',
            'when': when_match.group(1).strip() if when_match else '',
            'then': then_match.group(1).strip() if then_match else '',
            'has_alternatives': has_alternatives,
            'main_action': main_action,
            'specific_elements': specific_elements
        }
    
    def _extract_action_from_criteria(self, criteria: str) -> str:
        """Extrae la acción principal del criterio"""
        for action_type, keywords in self.action_patterns.items():
            if any(keyword in criteria for keyword in keywords):
                return action_type
        return 'procesar'
    
    def _extract_specific_elements(self, criteria: str, context: Dict[str, Any]) -> List[str]:
        """Extrae elementos específicos del criterio"""
        elements = []
        
        # Buscar elementos del contexto del dominio
        domain_context = context.get('context', {})
        for element in domain_context.get('elementos', []):
            if element.lower() in criteria:
                elements.append(element)
        
        # Buscar patrones específicos
        patterns = [
            r'(\w+)\s+embebida', r'(\w+)\s+condicional', r'(\w+)\s+del\s+sistema',
            r'campo\s+(\w+)', r'botón\s+(\w+)', r'página\s+(\w+)'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, criteria)
            elements.extend(matches)
        
        return list(set(elements))[:3]
    
    def _create_main_case(self, user_story: UserStory, criteria: str, criteria_index: int,
                         analysis: Dict[str, Any], context: Dict[str, Any]) -> ImprovedTestCase:
        """Crea el caso de prueba principal"""
        
        # Generar título específico y único
        title = self._generate_unique_title(analysis, context, criteria_index)
        
        # Generar feature concisa
        feature = self._generate_concise_feature(user_story, analysis)
        
        # Generar scenario específico
        scenario = self._generate_specific_scenario(analysis, context)
        
        # Generar pasos Gherkin estructurados
        given_steps = self._generate_given_steps(analysis, context)
        when_steps = self._generate_when_steps(analysis, context)
        then_steps = self._generate_then_steps(analysis, context)
        
        # Generar tags relevantes
        tags = self._generate_relevant_tags(analysis, context)
        
        return ImprovedTestCase(
            id=f"TC-{self.test_counter:03d}",
            title=title,
            feature=feature,
            scenario=scenario,
            given_steps=given_steps,
            when_steps=when_steps,
            then_steps=then_steps,
            tags=tags,
            test_type="funcional",
            priority="alta",
            user_story=user_story.title[:100],
            preconditions=[]
        )
    
    def _generate_unique_title(self, analysis: Dict[str, Any], context: Dict[str, Any], 
                              criteria_index: int) -> str:
        """Genera un título único y descriptivo"""
        action = analysis['main_action']
        elements = analysis['specific_elements']
        
        # Mapear acciones a títulos en español
        action_titles = {
            'validar': 'Validar',
            'crear': 'Crear',
            'editar': 'Modificar',
            'eliminar': 'Eliminar',
            'buscar': 'Consultar',
            'mostrar': 'Visualizar',
            'navegar': 'Acceder',
            'procesar': 'Procesar'
        }
        
        base_title = action_titles.get(action, 'Verificar')
        
        # Agregar elemento específico si existe
        if elements:
            element = elements[0].replace('_', ' ').title()
            title = f"{base_title} {element}"
        else:
            title = f"{base_title} funcionalidad"
        
        # Agregar contexto específico
        if 'error' in analysis.get('then', '').lower():
            title += " - Caso de error"
        elif 'exitoso' in analysis.get('then', '').lower():
            title += " - Caso exitoso"
        else:
            title += f" - Escenario {criteria_index}"
        
        # Incrementar contador para unicidad
        final_title = f"{title} (TC-{self.test_counter:03d})"
        self.test_counter += 1
        
        return final_title
    
    def _generate_concise_feature(self, user_story: UserStory, analysis: Dict[str, Any]) -> str:
        """Genera una descripción concisa de la feature"""
        # Extraer las primeras 10 palabras del título
        title_words = user_story.title.split()[:10]
        base_feature = ' '.join(title_words)
        
        # Limpiar y estructurar
        if len(base_feature) > 80:
            base_feature = base_feature[:77] + "..."
        
        return f"Feature: {base_feature}"
    
    def _generate_specific_scenario(self, analysis: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Genera un escenario específico"""
        action = analysis['main_action']
        elements = analysis['specific_elements']
        
        if elements:
            element = elements[0].replace('_', ' ')
            return f"Scenario: {action.title()} {element} correctamente"
        else:
            return f"Scenario: {action.title()} funcionalidad del sistema"
    
    def _generate_given_steps(self, analysis: Dict[str, Any], context: Dict[str, Any]) -> List[str]:
        """Genera pasos Given estructurados"""
        steps = []
        
        if analysis['given']:
            # Usar el given del análisis si existe
            steps.append(f"Given {analysis['given']}")
        else:
            # Generar given basado en contexto
            domain = context.get('domain', 'general')
            if domain == 'autenticacion':
                steps.append("Given el usuario está en la página de login")
            elif domain == 'facturacion':
                steps.append("Given el sistema de facturación está disponible")
            else:
                steps.append("Given el sistema está operativo")
        
        return steps
    
    def _generate_when_steps(self, analysis: Dict[str, Any], context: Dict[str, Any]) -> List[str]:
        """Genera pasos When estructurados"""
        steps = []
        
        if analysis['when']:
            steps.append(f"When {analysis['when']}")
        else:
            action = analysis['main_action']
            elements = analysis['specific_elements']
            
            if elements:
                element = elements[0].replace('_', ' ')
                steps.append(f"When el usuario {action} {element}")
            else:
                steps.append(f"When el usuario ejecuta la acción de {action}")
        
        return steps
    
    def _generate_then_steps(self, analysis: Dict[str, Any], context: Dict[str, Any]) -> List[str]:
        """Genera pasos Then estructurados"""
        steps = []
        
        if analysis['then']:
            steps.append(f"Then {analysis['then']}")
        else:
            # Generar then basado en la acción
            action = analysis['main_action']
            if action == 'validar':
                steps.append("Then la validación se completa exitosamente")
            elif action == 'crear':
                steps.append("Then el elemento se crea correctamente")
            elif action == 'mostrar':
                steps.append("Then la información se muestra correctamente")
            else:
                steps.append("Then la operación se ejecuta exitosamente")
        
        return steps
    
    def _generate_relevant_tags(self, analysis: Dict[str, Any], context: Dict[str, Any]) -> List[str]:
        """Genera tags relevantes para el caso"""
        tags = []
        
        # Tag por acción
        action = analysis['main_action']
        tags.append(f"@{action}")
        
        # Tag por dominio
        domain = context.get('domain', 'general')
        tags.append(f"@{domain}")
        
        # Tag por tipo de caso
        if 'error' in analysis.get('then', '').lower():
            tags.append("@negativo")
        else:
            tags.append("@positivo")
        
        return tags
    
    def _create_alternative_case(self, user_story: UserStory, criteria: str, criteria_index: int,
                                analysis: Dict[str, Any], context: Dict[str, Any]) -> ImprovedTestCase:
        """Crea un caso alternativo si aplica"""
        # Similar al caso principal pero con variaciones
        title = self._generate_unique_title(analysis, context, criteria_index) + " - Alternativo"
        
        # Modificar pasos para el caso alternativo
        given_steps = self._generate_given_steps(analysis, context)
        when_steps = [step.replace("ejecuta", "intenta ejecutar") for step in self._generate_when_steps(analysis, context)]
        then_steps = ["Then se muestra el comportamiento alternativo esperado"]
        
        tags = self._generate_relevant_tags(analysis, context)
        tags.append("@alternativo")
        
        return ImprovedTestCase(
            id=f"TC-{self.test_counter:03d}",
            title=title,
            feature=self._generate_concise_feature(user_story, analysis),
            scenario=f"Scenario: Caso alternativo - {analysis['main_action']}",
            given_steps=given_steps,
            when_steps=when_steps,
            then_steps=then_steps,
            tags=tags,
            test_type="funcional",
            priority="media",
            user_story=user_story.title[:100],
            preconditions=[]
        )
    
    def _generate_additional_cases(self, user_story: UserStory, context: Dict[str, Any]) -> List[ImprovedTestCase]:
        """Genera casos adicionales (edge cases, negativos)"""
        additional_cases = []
        
        # Caso negativo general
        negative_case = ImprovedTestCase(
            id=f"TC-{self.test_counter:03d}",
            title=f"Validar manejo de errores - Caso negativo (TC-{self.test_counter:03d})",
            feature=self._generate_concise_feature(user_story, {}),
            scenario="Scenario: Validar comportamiento con datos inválidos",
            given_steps=["Given el sistema está operativo"],
            when_steps=["When el usuario ingresa datos inválidos"],
            then_steps=["Then se muestra un mensaje de error apropiado"],
            tags=["@negativo", "@error", f"@{context.get('domain', 'general')}"],
            test_type="negativo",
            priority="media",
            user_story=user_story.title[:100],
            preconditions=[]
        )
        additional_cases.append(negative_case)
        self.test_counter += 1
        
        return additional_cases
    
    def format_for_linear(self, test_case: ImprovedTestCase) -> str:
        """Formatea el caso de prueba para exportación a Linear"""
        description = f"""**Feature:** {test_case.feature}

**Scenario:** {test_case.scenario}

**Precondiciones:**
{chr(10).join(f"- {step}" for step in test_case.given_steps)}

**Pasos:**
{chr(10).join(f"{i+1}. {step}" for i, step in enumerate(test_case.when_steps))}

**Resultado Esperado:**
{chr(10).join(f"- {step}" for step in test_case.then_steps)}

**Tags:** {', '.join(test_case.tags)}"""
        
        return description
