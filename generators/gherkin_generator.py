#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de Casos de Prueba con Formato Gherkin Completo
Genera casos de prueba con estructura Gherkin profesional para Linear
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
class GherkinTestCase:
    """Caso de prueba con formato Gherkin completo"""
    id: str
    title: str
    feature: str
    background: Optional[str] = None
    scenario_outline: Optional[str] = None
    scenario: Optional[str] = None
    given_steps: List[str] = None
    when_steps: List[str] = None
    then_steps: List[str] = None
    examples: Optional[Dict[str, List[str]]] = None
    tags: List[str] = None
    test_type: str = "funcional"
    priority: str = "alta"
    user_story: str = ""
    
    def __post_init__(self):
        if self.given_steps is None:
            self.given_steps = []
        if self.when_steps is None:
            self.when_steps = []
        if self.then_steps is None:
            self.then_steps = []
        if self.tags is None:
            self.tags = []

class GherkinGenerator:
    """Generador de casos de prueba con formato Gherkin profesional"""
    
    def __init__(self):
        # Los métodos de generación se implementan directamente en las funciones correspondientes
        pass
    
    def generate_gherkin_cases(self, user_story: UserStory, qa_comments: str = "") -> List[GherkinTestCase]:
        """Genera casos de prueba con formato Gherkin completo"""
        gherkin_cases = []
        
        # Analizar contexto de la historia de usuario
        context = self._analyze_user_story_context(user_story)
        qa_context = self._analyze_qa_comments(qa_comments)
        
        # Generar casos funcionales principales
        for i, criteria in enumerate(user_story.acceptance_criteria):
            gherkin_cases.extend(self._generate_functional_gherkin(user_story, criteria, i + 1, context, qa_context))
        
        # Generar casos alternos (@alterno)
        gherkin_cases.extend(self._generate_alternate_scenarios(user_story, context, qa_context))
        
        # Generar casos de error (@error)
        gherkin_cases.extend(self._generate_error_scenarios(user_story, context, qa_context))
        
        # Generar casos específicos basados en QA
        gherkin_cases.extend(self._generate_qa_specific_gherkin(user_story, qa_context))
        
        return gherkin_cases
    
    def _analyze_user_story_context(self, user_story: UserStory) -> Dict[str, Any]:
        """Analiza el contexto de la historia de usuario"""
        text = f"{user_story.title} {user_story.description}".lower()
        
        # Determinar dominio
        domain = 'general'
        if any(word in text for word in ['login', 'sesión', 'autenticación', 'credenciales']):
            domain = 'authentication'
        elif any(word in text for word in ['registro', 'crear cuenta', 'signup']):
            domain = 'registration'
        elif any(word in text for word in ['perfil', 'usuario', 'datos personales']):
            domain = 'user_profile'
        elif any(word in text for word in ['dashboard', 'panel', 'inicio']):
            domain = 'dashboard'
        elif any(word in text for word in ['búsqueda', 'buscar', 'filtro']):
            domain = 'search'
        elif any(word in text for word in ['carrito', 'compra', 'pago']):
            domain = 'ecommerce'
        
        # Extraer componentes del sistema
        components = []
        if 'formulario' in text or 'form' in text:
            components.append('formulario')
        if 'botón' in text or 'button' in text:
            components.append('botón')
        if 'campo' in text or 'field' in text:
            components.append('campo')
        if 'menú' in text or 'menu' in text:
            components.append('menú')
        if 'tabla' in text or 'table' in text:
            components.append('tabla')
        if 'modal' in text or 'popup' in text:
            components.append('modal')
        
        return {
            'domain': domain,
            'components': components,
            'has_authentication': 'login' in text or 'sesión' in text,
            'has_forms': 'formulario' in text or 'form' in text,
            'has_buttons': 'botón' in text or 'button' in text,
            'has_redirects': 'redirigir' in text or 'redirect' in text,
            'has_validation': 'validar' in text or 'validación' in text
        }
    
    def _analyze_qa_comments(self, qa_comments: str) -> Dict[str, Any]:
        """Analiza comentarios de QA para generar casos específicos"""
        if not qa_comments:
            return {}
        
        comments_lower = qa_comments.lower()
        
        return {
            'validation_areas': self._extract_validation_areas(comments_lower),
            'specific_concerns': self._extract_specific_concerns(comments_lower),
            'test_scenarios': self._extract_test_scenarios(comments_lower),
            'priority_areas': self._extract_priority_areas(comments_lower)
        }
    
    def _extract_validation_areas(self, comments: str) -> List[str]:
        """Extrae áreas de validación de los comentarios"""
        areas = []
        if 'campos obligatorios' in comments:
            areas.append('required_fields')
        if 'formato' in comments:
            areas.append('format_validation')
        if 'longitud' in comments:
            areas.append('length_validation')
        if 'email' in comments:
            areas.append('email_validation')
        if 'contraseña' in comments:
            areas.append('password_validation')
        return areas
    
    def _extract_specific_concerns(self, comments: str) -> List[str]:
        """Extrae preocupaciones específicas"""
        concerns = []
        if 'credenciales' in comments:
            concerns.append('credentials')
        if 'error' in comments:
            concerns.append('error_handling')
        if 'redirección' in comments or 'redirigir' in comments:
            concerns.append('redirection')
        if 'seguridad' in comments:
            concerns.append('security')
        if 'performance' in comments or 'rendimiento' in comments:
            concerns.append('performance')
        return concerns
    
    def _extract_test_scenarios(self, comments: str) -> List[str]:
        """Extrae escenarios de prueba"""
        scenarios = []
        if 'inválidas' in comments or 'incorrectas' in comments:
            scenarios.append('invalid_data')
        if 'válidas' in comments or 'correctas' in comments:
            scenarios.append('valid_data')
        if 'bloqueado' in comments:
            scenarios.append('blocked_user')
        if 'timeout' in comments:
            scenarios.append('timeout')
        return scenarios
    
    def _extract_priority_areas(self, comments: str) -> List[str]:
        """Extrae áreas prioritarias"""
        areas = []
        if 'crítico' in comments:
            areas.append('critical')
        if 'importante' in comments:
            areas.append('important')
        if 'edge case' in comments or 'caso límite' in comments:
            areas.append('edge_cases')
        return areas
    
    def _generate_functional_gherkin(self, user_story: UserStory, criteria: str, criteria_index: int, 
                                   context: Dict[str, Any], qa_context: Dict[str, Any]) -> List[GherkinTestCase]:
        """Genera casos funcionales con formato Gherkin"""
        gherkin_cases = []
        
        # Caso principal funcional
        main_case = GherkinTestCase(
            id=f"TC-{criteria_index:03d}",
            title=self._generate_meaningful_title(criteria, context),
            feature=self._generate_feature_description(user_story, context),
            background=self._generate_background(context),
            scenario=self._generate_scenario_description(criteria, context),
            given_steps=self._generate_given_steps(criteria, context),
            when_steps=self._generate_when_steps(criteria, context),
            then_steps=self._generate_then_steps(criteria, context),
            tags=self._generate_tags(criteria, context, "funcional"),
            test_type="funcional",
            priority="alta",
            user_story=user_story.title
        )
        gherkin_cases.append(main_case)
        
        # Si el criterio tiene parámetros, generar Scenario Outline
        if self._has_parameters(criteria):
            outline_case = self._generate_scenario_outline(user_story, criteria, criteria_index, context)
            gherkin_cases.append(outline_case)
        
        return gherkin_cases
    
    def _generate_alternate_scenarios(self, user_story: UserStory, context: Dict[str, Any], 
                                     qa_context: Dict[str, Any]) -> List[GherkinTestCase]:
        """Genera casos alternos (@alterno)"""
        gherkin_cases = []
        
        # Caso alterno: flujo alternativo
        alt_case = GherkinTestCase(
            id="TC-ALT-001",
            title="Flujo alternativo - Opción secundaria",
            feature=f"Funcionalidad alternativa para {user_story.title}",
            background=self._generate_background(context),
            scenario="Verificar flujo alternativo cuando la opción principal no está disponible",
            given_steps=[
                "Given que el usuario está en la página principal",
                "And que la opción principal no está disponible"
            ],
            when_steps=[
                "When el usuario selecciona la opción alternativa",
                "And ejecuta la acción secundaria"
            ],
            then_steps=[
                "Then el sistema procesa la solicitud correctamente",
                "And muestra el resultado esperado"
            ],
            tags=["@alterno", "flujo-alternativo"],
            test_type="funcional",
            priority="media",
            user_story=user_story.title
        )
        gherkin_cases.append(alt_case)
        
        return gherkin_cases
    
    def _generate_error_scenarios(self, user_story: UserStory, context: Dict[str, Any], 
                                 qa_context: Dict[str, Any]) -> List[GherkinTestCase]:
        """Genera casos de error (@error)"""
        gherkin_cases = []
        
        # Caso de error: datos inválidos
        error_case = GherkinTestCase(
            id="TC-ERR-001",
            title="Manejo de errores con datos inválidos",
            feature=f"Manejo de errores para {user_story.title}",
            background=self._generate_background(context),
            scenario="Verificar que el sistema maneja correctamente los datos inválidos",
            given_steps=[
                "Given que el usuario está en el formulario correspondiente",
                "And que el sistema está funcionando normalmente"
            ],
            when_steps=[
                "When el usuario ingresa datos inválidos",
                "And intenta enviar el formulario"
            ],
            then_steps=[
                "Then el sistema muestra mensajes de error apropiados",
                "And no procesa la solicitud",
                "And mantiene los datos ingresados para corrección"
            ],
            tags=["@error", "manejo-errores", "datos-inválidos"],
            test_type="negativo",
            priority="alta",
            user_story=user_story.title
        )
        gherkin_cases.append(error_case)
        
        return gherkin_cases
    
    def _generate_qa_specific_gherkin(self, user_story: UserStory, qa_context: Dict[str, Any]) -> List[GherkinTestCase]:
        """Genera casos específicos basados en comentarios de QA"""
        gherkin_cases = []
        
        # Casos de validación si se mencionan
        if 'required_fields' in qa_context.get('validation_areas', []):
            validation_case = GherkinTestCase(
                id="TC-VAL-001",
                title="Validación de campos obligatorios",
                feature=f"Validación de campos para {user_story.title}",
                background="Given que el sistema está funcionando normalmente",
                scenario="Verificar validación de campos obligatorios",
                given_steps=[
                    "Given que el usuario está en el formulario",
                    "And que existen campos obligatorios"
                ],
                when_steps=[
                    "When el usuario deja campos obligatorios vacíos",
                    "And intenta enviar el formulario"
                ],
                then_steps=[
                    "Then el sistema muestra mensajes de error para campos vacíos",
                    "And no permite el envío del formulario",
                    "And resalta visualmente los campos faltantes"
                ],
                tags=["@validacion", "campos-obligatorios"],
                test_type="negativo",
                priority="alta",
                user_story=user_story.title
            )
            gherkin_cases.append(validation_case)
        
        return gherkin_cases
    
    def _generate_meaningful_title(self, criteria: str, context: Dict[str, Any]) -> str:
        """Genera un título significativo basado en el criterio y contexto"""
        # Extraer acción principal del criterio
        action = self._extract_main_action(criteria)
        
        # Mapear a títulos más específicos
        action_titles = {
            'login': 'Iniciar sesión',
            'register': 'Registrar usuario',
            'search': 'Buscar información',
            'edit': 'Editar datos',
            'delete': 'Eliminar elemento',
            'create': 'Crear nuevo elemento',
            'view': 'Visualizar información',
            'interact': 'Interactuar con el sistema'
        }
        
        base_title = action_titles.get(action, 'Ejecutar funcionalidad')
        
        # Agregar contexto específico
        if 'email' in criteria.lower() and 'contraseña' in criteria.lower():
            return f"{base_title} con credenciales válidas"
        elif 'error' in criteria.lower() or 'incorrecto' in criteria.lower():
            return f"{base_title} con datos inválidos"
        elif 'redirigir' in criteria.lower() or 'dashboard' in criteria.lower():
            return f"{base_title} y verificar redirección"
        else:
            return f"{base_title} según criterio de aceptación"
    
    def _extract_main_action(self, criteria: str) -> str:
        """Extrae la acción principal del criterio"""
        criteria_lower = criteria.lower()
        
        if 'iniciar sesión' in criteria_lower or 'login' in criteria_lower:
            return 'login'
        elif 'registrar' in criteria_lower or 'crear cuenta' in criteria_lower:
            return 'register'
        elif 'buscar' in criteria_lower or 'search' in criteria_lower:
            return 'search'
        elif 'editar' in criteria_lower or 'modificar' in criteria_lower:
            return 'edit'
        elif 'eliminar' in criteria_lower or 'delete' in criteria_lower:
            return 'delete'
        elif 'crear' in criteria_lower or 'create' in criteria_lower:
            return 'create'
        elif 'ver' in criteria_lower or 'view' in criteria_lower:
            return 'view'
        else:
            return 'interact'
    
    def _generate_feature_description(self, user_story: UserStory, context: Dict[str, Any]) -> str:
        """Genera descripción de la feature"""
        domain = context['domain']
        
        feature_descriptions = {
            'authentication': f"Autenticación de usuarios para {user_story.title}",
            'registration': f"Registro de usuarios para {user_story.title}",
            'user_profile': f"Gestión de perfil de usuario para {user_story.title}",
            'dashboard': f"Panel de control para {user_story.title}",
            'search': f"Búsqueda de información para {user_story.title}",
            'ecommerce': f"Funcionalidad de comercio electrónico para {user_story.title}",
            'general': f"Funcionalidad principal para {user_story.title}"
        }
        
        return feature_descriptions.get(domain, f"Funcionalidad para {user_story.title}")
    
    def _generate_background(self, context: Dict[str, Any]) -> str:
        """Genera sección Background"""
        if context['domain'] == 'authentication':
            return "Given que el sistema de autenticación está funcionando correctamente"
        elif context['domain'] == 'registration':
            return "Given que el sistema de registro está disponible"
        elif context['domain'] == 'user_profile':
            return "Given que el usuario está autenticado en el sistema"
        elif context['domain'] == 'dashboard':
            return "Given que el usuario tiene acceso al dashboard"
        else:
            return "Given que el sistema está funcionando normalmente"
    
    def _generate_scenario_description(self, criteria: str, context: Dict[str, Any]) -> str:
        """Genera descripción del escenario"""
        action = self._extract_main_action(criteria)
        
        scenario_descriptions = {
            'login': 'Iniciar sesión con credenciales válidas',
            'register': 'Registrar nuevo usuario',
            'search': 'Buscar información en el sistema',
            'edit': 'Editar información existente',
            'delete': 'Eliminar elemento del sistema',
            'create': 'Crear nuevo elemento',
            'view': 'Visualizar información',
            'interact': 'Interactuar con la funcionalidad'
        }
        
        return scenario_descriptions.get(action, 'Ejecutar funcionalidad principal')
    
    def _generate_given_steps(self, criteria: str, context: Dict[str, Any]) -> List[str]:
        """Genera pasos Given"""
        steps = []
        
        # Paso base según el dominio
        if context['domain'] == 'authentication':
            steps.append("Given que el usuario tiene credenciales válidas")
            steps.append("And que el sistema de autenticación está disponible")
        elif context['domain'] == 'registration':
            steps.append("Given que el usuario tiene datos válidos para registro")
            steps.append("And que el sistema de registro está disponible")
        elif context['domain'] == 'user_profile':
            steps.append("Given que el usuario está autenticado")
            steps.append("And que tiene un perfil existente")
        else:
            steps.append("Given que el usuario está en el sistema")
            steps.append("And que tiene los permisos necesarios")
        
        # Pasos específicos del criterio
        if 'email' in criteria.lower():
            steps.append("And que tiene un email válido")
        if 'contraseña' in criteria.lower():
            steps.append("And que tiene una contraseña válida")
        if 'dashboard' in criteria.lower():
            steps.append("And que tiene acceso al dashboard")
        
        return steps
    
    def _generate_when_steps(self, criteria: str, context: Dict[str, Any]) -> List[str]:
        """Genera pasos When"""
        steps = []
        action = self._extract_main_action(criteria)
        
        if action == 'login':
            steps.extend([
                "When el usuario navega a la página de inicio de sesión",
                "And ingresa sus credenciales válidas",
                "And hace clic en el botón de inicio de sesión"
            ])
        elif action == 'register':
            steps.extend([
                "When el usuario navega a la página de registro",
                "And completa todos los campos obligatorios",
                "And hace clic en el botón de registro"
            ])
        elif action == 'search':
            steps.extend([
                "When el usuario navega a la funcionalidad de búsqueda",
                "And ingresa el término de búsqueda",
                "And hace clic en el botón buscar"
            ])
        else:
            steps.extend([
                "When el usuario ejecuta la acción principal",
                "And confirma la operación"
            ])
        
        # Pasos específicos del criterio
        if 'redirigir' in criteria.lower() or 'dashboard' in criteria.lower():
            steps.append("And espera la redirección")
        
        return steps
    
    def _generate_then_steps(self, criteria: str, context: Dict[str, Any]) -> List[str]:
        """Genera pasos Then"""
        steps = []
        action = self._extract_main_action(criteria)
        
        if action == 'login':
            if 'dashboard' in criteria.lower() or 'redirigir' in criteria.lower():
                steps.extend([
                    "Then el usuario inicia sesión exitosamente",
                    "And es redirigido al dashboard",
                    "And puede ver su información personal"
                ])
            else:
                steps.extend([
                    "Then el usuario inicia sesión exitosamente",
                    "And puede acceder a las funcionalidades del sistema"
                ])
        elif action == 'register':
            steps.extend([
                "Then el usuario se registra exitosamente",
                "And recibe confirmación de registro",
                "And puede acceder al sistema"
            ])
        elif action == 'search':
            steps.extend([
                "Then se muestran los resultados de búsqueda",
                "And los resultados son relevantes al término buscado",
                "And se puede acceder a los detalles de cada resultado"
            ])
        else:
            steps.extend([
                "Then la funcionalidad se ejecuta correctamente",
                "And se muestra el resultado esperado",
                "And el usuario puede continuar con su flujo de trabajo"
            ])
        
        # Pasos específicos del criterio
        if 'error' in criteria.lower():
            steps = [
                "Then se muestra un mensaje de error claro",
                "And el sistema no procesa la solicitud",
                "And se mantiene el estado anterior"
            ]
        
        return steps
    
    def _generate_tags(self, criteria: str, context: Dict[str, Any], test_type: str) -> List[str]:
        """Genera tags apropiados"""
        tags = [test_type]
        
        # Tags basados en el dominio
        if context['domain'] == 'authentication':
            tags.append("autenticacion")
        elif context['domain'] == 'registration':
            tags.append("registro")
        elif context['domain'] == 'user_profile':
            tags.append("perfil-usuario")
        
        # Tags basados en el criterio
        if 'email' in criteria.lower():
            tags.append("email")
        if 'contraseña' in criteria.lower():
            tags.append("password")
        if 'dashboard' in criteria.lower():
            tags.append("dashboard")
        if 'error' in criteria.lower():
            tags.append("error-handling")
        
        return tags
    
    def _has_parameters(self, criteria: str) -> bool:
        """Verifica si el criterio tiene parámetros para Scenario Outline"""
        return '<' in criteria and '>' in criteria
    
    def _generate_scenario_outline(self, user_story: UserStory, criteria: str, criteria_index: int, 
                                  context: Dict[str, Any]) -> GherkinTestCase:
        """Genera Scenario Outline con Examples"""
        return GherkinTestCase(
            id=f"TC-{criteria_index:03d}-OUTLINE",
            title=f"Escenario parametrizado - {self._generate_meaningful_title(criteria, context)}",
            feature=self._generate_feature_description(user_story, context),
            background=self._generate_background(context),
            scenario_outline="Verificar funcionalidad con diferentes parámetros",
            given_steps=self._generate_given_steps(criteria, context),
            when_steps=self._generate_when_steps(criteria, context),
            then_steps=self._generate_then_steps(criteria, context),
            examples={
                "param1": ["valor1", "valor2", "valor3"],
                "param2": ["resultado1", "resultado2", "resultado3"]
            },
            tags=self._generate_tags(criteria, context, "parametrizado"),
            test_type="funcional",
            priority="media",
            user_story=user_story.title
        )
    
    def format_gherkin_for_linear(self, gherkin_case: GherkinTestCase) -> str:
        """Formatea un caso Gherkin para exportar a Linear"""
        gherkin_text = []
        
        # Feature
        gherkin_text.append(f"Feature: {gherkin_case.feature}")
        gherkin_text.append("")
        
        # Background
        if gherkin_case.background:
            gherkin_text.append("Background:")
            gherkin_text.append(f"  {gherkin_case.background}")
            gherkin_text.append("")
        
        # Tags
        if gherkin_case.tags:
            gherkin_text.append(" ".join([f"@{tag}" for tag in gherkin_case.tags]))
        
        # Scenario o Scenario Outline
        if gherkin_case.scenario_outline:
            gherkin_text.append(f"Scenario Outline: {gherkin_case.scenario_outline}")
        else:
            gherkin_text.append(f"Scenario: {gherkin_case.scenario}")
        
        gherkin_text.append("")
        
        # Given steps
        for step in gherkin_case.given_steps:
            gherkin_text.append(f"  {step}")
        
        # When steps
        for step in gherkin_case.when_steps:
            gherkin_text.append(f"  {step}")
        
        # Then steps
        for step in gherkin_case.then_steps:
            gherkin_text.append(f"  {step}")
        
        # Examples (si es Scenario Outline)
        if gherkin_case.examples:
            gherkin_text.append("")
            gherkin_text.append("  Examples:")
            gherkin_text.append("    | " + " | ".join(gherkin_case.examples.keys()) + " |")
            for i in range(len(list(gherkin_case.examples.values())[0])):
                row = []
                for key in gherkin_case.examples.keys():
                    row.append(gherkin_case.examples[key][i])
                gherkin_text.append("    | " + " | ".join(row) + " |")
        
        return "\n".join(gherkin_text)

def main():
    """Función principal para probar el generador Gherkin"""
    # Ejemplo de uso
    user_story = UserStory(
        title="Como usuario quiero iniciar sesión para acceder al sistema",
        description="El usuario necesita poder iniciar sesión con sus credenciales para acceder a las funcionalidades del sistema",
        acceptance_criteria=[
            "Dado que tengo credenciales válidas, cuando ingreso email y contraseña, entonces debo ser redirigido al dashboard",
            "Dado que tengo credenciales inválidas, cuando intento iniciar sesión, entonces debo ver un mensaje de error"
        ]
    )
    
    qa_comments = "Validar campos obligatorios, verificar redirección al dashboard, manejar errores de credenciales"
    
    generator = GherkinGenerator()
    gherkin_cases = generator.generate_gherkin_cases(user_story, qa_comments)
    
    print(f"Generados {len(gherkin_cases)} casos de prueba con formato Gherkin:")
    print("=" * 60)
    
    for case in gherkin_cases:
        print(f"\nCaso: {case.id} - {case.title}")
        print(f"Feature: {case.feature}")
        print(f"Tags: {', '.join(case.tags)}")
        print(f"Tipo: {case.test_type} | Prioridad: {case.priority}")
        print("\nFormato Gherkin:")
        print(generator.format_gherkin_for_linear(case))
        print("-" * 60)

if __name__ == "__main__":
    main()
