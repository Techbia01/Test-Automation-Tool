#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador Mejorado de Casos de Prueba con Formato Gherkin Profesional
Genera casos específicos y detallados como ChatGPT
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
class EnhancedGherkinTestCase:
    """Caso de prueba con formato Gherkin mejorado y específico"""
    id: str
    title: str
    feature: str
    background: Optional[str] = None
    scenario: Optional[str] = None
    given_steps: List[str] = None
    when_steps: List[str] = None
    then_steps: List[str] = None
    tags: List[str] = None
    test_type: str = "funcional"
    priority: str = "alta"
    user_story: str = ""
    preconditions: List[str] = None
    
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

class EnhancedGherkinGenerator:
    """Generador mejorado de casos de prueba con formato Gherkin específico"""
    
    def __init__(self):
        self.domain_patterns = {
            'alumbrado_publico': {
                'keywords': ['alumbrado', 'público', 'municipio', 'acuerdo', 'condicional'],
                'ui_elements': ['icono de alerta', 'tooltip', 'tabla de condicionales', 'modal de errores'],
                'actions': ['consultar', 'crear', 'editar', 'importar', 'exportar'],
                'states': ['vigente', 'sin acuerdo', 'con acuerdo', 'expirado']
            },
            'authentication': {
                'keywords': ['login', 'sesión', 'credenciales', 'usuario', 'contraseña'],
                'ui_elements': ['formulario', 'botón', 'mensaje de error', 'dashboard'],
                'actions': ['iniciar sesión', 'cerrar sesión', 'recuperar contraseña'],
                'states': ['autenticado', 'no autenticado', 'sesión expirada']
            },
            'ecommerce': {
                'keywords': ['carrito', 'compra', 'pago', 'producto', 'orden'],
                'ui_elements': ['botón comprar', 'carrito de compras', 'formulario de pago'],
                'actions': ['agregar al carrito', 'proceder al pago', 'confirmar compra'],
                'states': ['disponible', 'agotado', 'en proceso', 'completado']
            }
        }
    
    def generate_enhanced_cases(self, user_story: UserStory, qa_comments: str = "") -> List[EnhancedGherkinTestCase]:
        """Genera casos de prueba mejorados con especificidad ChatGPT"""
        enhanced_cases = []
        
        # Analizar contexto profundo
        context = self._analyze_deep_context(user_story, qa_comments)
        
        # Generar casos específicos para cada criterio
        for i, criteria in enumerate(user_story.acceptance_criteria):
            enhanced_cases.extend(self._generate_specific_criteria_cases(user_story, criteria, i + 1, context))
        
        # Generar casos adicionales basados en contexto
        enhanced_cases.extend(self._generate_contextual_cases(user_story, context))
        
        return enhanced_cases
    
    def _analyze_deep_context(self, user_story: UserStory, qa_comments: str) -> Dict[str, Any]:
        """Análisis profundo del contexto para generar casos específicos"""
        full_text = f"{user_story.title} {user_story.description} {qa_comments}".lower()
        
        # Detectar dominio específico
        domain = self._detect_specific_domain(full_text)
        
        # Extraer elementos UI específicos
        ui_elements = self._extract_ui_elements(full_text, domain)
        
        # Extraer acciones específicas
        actions = self._extract_specific_actions(full_text, domain)
        
        # Extraer estados del sistema
        states = self._extract_system_states(full_text, domain)
        
        # Extraer mensajes específicos
        messages = self._extract_specific_messages(full_text)
        
        # Extraer validaciones específicas
        validations = self._extract_specific_validations(qa_comments)
        
        return {
            'domain': domain,
            'ui_elements': ui_elements,
            'actions': actions,
            'states': states,
            'messages': messages,
            'validations': validations,
            'has_import_export': 'importar' in full_text or 'exportar' in full_text,
            'has_agreements': 'acuerdo' in full_text,
            'has_conditionals': 'condicional' in full_text,
            'has_municipalities': 'municipio' in full_text
        }
    
    def _detect_specific_domain(self, text: str) -> str:
        """Detecta el dominio específico de la aplicación"""
        if any(word in text for word in ['alumbrado', 'público', 'municipio', 'acuerdo']):
            return 'alumbrado_publico'
        elif any(word in text for word in ['login', 'sesión', 'credenciales']):
            return 'authentication'
        elif any(word in text for word in ['carrito', 'compra', 'pago']):
            return 'ecommerce'
        else:
            return 'general'
    
    def _extract_ui_elements(self, text: str, domain: str) -> List[str]:
        """Extrae elementos UI específicos mencionados"""
        elements = []
        
        # Elementos comunes
        if 'icono' in text:
            elements.append('icono de alerta')
        if 'tooltip' in text:
            elements.append('tooltip')
        if 'tabla' in text:
            elements.append('tabla de condicionales')
        if 'modal' in text:
            elements.append('modal de errores')
        if 'formulario' in text:
            elements.append('formulario')
        if 'botón' in text:
            elements.append('botón')
        if 'mensaje' in text:
            elements.append('mensaje de error')
        
        return elements
    
    def _extract_specific_actions(self, text: str, domain: str) -> List[str]:
        """Extrae acciones específicas del usuario"""
        actions = []
        
        if 'consultar' in text:
            actions.append('consultar tabla')
        if 'crear' in text:
            actions.append('crear condicional')
        if 'editar' in text:
            actions.append('editar condicional')
        if 'importar' in text:
            actions.append('importar archivo')
        if 'exportar' in text:
            actions.append('exportar datos')
        
        return actions
    
    def _extract_system_states(self, text: str, domain: str) -> List[str]:
        """Extrae estados específicos del sistema"""
        states = []
        
        if 'vigente' in text:
            states.append('acuerdo vigente')
        if 'sin acuerdo' in text:
            states.append('sin acuerdo vigente')
        if 'expirado' in text:
            states.append('acuerdo expirado')
        
        return states
    
    def _extract_specific_messages(self, text: str) -> List[str]:
        """Extrae mensajes específicos mencionados"""
        messages = []
        
        # Buscar mensajes literales
        message_patterns = [
            r'"([^"]+)"',  # Texto entre comillas
            r'mensaje literal[^"]*"([^"]+)"',  # Mensaje literal específico
            r'literalmente[^"]*"([^"]+)"'  # Literalmente específico
        ]
        
        for pattern in message_patterns:
            matches = re.findall(pattern, text)
            messages.extend(matches)
        
        return messages
    
    def _extract_specific_validations(self, qa_comments: str) -> List[str]:
        """Extrae validaciones específicas de comentarios QA"""
        validations = []
        
        if not qa_comments:
            return validations
        
        comments_lower = qa_comments.lower()
        
        if 'campos obligatorios' in comments_lower:
            validations.append('validar campos obligatorios')
        if 'formato' in comments_lower:
            validations.append('validar formato de datos')
        if 'longitud' in comments_lower:
            validations.append('validar longitud de campos')
        if 'consistencia' in comments_lower:
            validations.append('verificar consistencia cross-platform')
        if 'rendimiento' in comments_lower:
            validations.append('verificar rendimiento')
        
        return validations
    
    def _generate_specific_criteria_cases(self, user_story: UserStory, criteria: str, criteria_index: int, 
                                         context: Dict[str, Any]) -> List[EnhancedGherkinTestCase]:
        """Genera casos específicos basados en criterios de aceptación"""
        cases = []
        
        # Analizar el criterio específico
        criteria_analysis = self._analyze_criteria(criteria, context)
        
        # Generar caso principal específico
        main_case = self._create_specific_case(
            user_story, criteria, criteria_index, context, criteria_analysis, "funcional"
        )
        cases.append(main_case)
        
        # Generar casos adicionales si el criterio lo amerita
        if criteria_analysis['has_negative_scenario']:
            negative_case = self._create_specific_case(
                user_story, criteria, criteria_index, context, criteria_analysis, "negativo"
            )
            cases.append(negative_case)
        
        if criteria_analysis['has_edge_case']:
            edge_case = self._create_specific_case(
                user_story, criteria, criteria_index, context, criteria_analysis, "edge_case"
            )
            cases.append(edge_case)
        
        return cases
    
    def _analyze_criteria(self, criteria: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analiza un criterio específico para extraer detalles"""
        criteria_lower = criteria.lower()
        
        return {
            'has_negative_scenario': any(word in criteria_lower for word in ['error', 'inválido', 'incorrecto', 'fallo']),
            'has_edge_case': any(word in criteria_lower for word in ['límite', 'máximo', 'mínimo', 'vacío']),
            'has_ui_interaction': any(word in criteria_lower for word in ['hacer clic', 'seleccionar', 'navegar', 'consultar']),
            'has_validation': any(word in criteria_lower for word in ['validar', 'verificar', 'comprobar']),
            'has_error_handling': any(word in criteria_lower for word in ['error', 'fallo', 'excepción']),
            'specific_elements': self._extract_criteria_elements(criteria_lower, context)
        }
    
    def _extract_criteria_elements(self, criteria: str, context: Dict[str, Any]) -> List[str]:
        """Extrae elementos específicos del criterio"""
        elements = []
        
        # Buscar elementos UI específicos
        if 'icono' in criteria:
            elements.append('icono de alerta')
        if 'tooltip' in criteria:
            elements.append('tooltip')
        if 'tabla' in criteria:
            elements.append('tabla')
        if 'modal' in criteria:
            elements.append('modal')
        if 'formulario' in criteria:
            elements.append('formulario')
        
        return elements
    
    def _create_specific_case(self, user_story: UserStory, criteria: str, criteria_index: int, 
                             context: Dict[str, Any], criteria_analysis: Dict[str, Any], 
                             case_type: str) -> EnhancedGherkinTestCase:
        """Crea un caso específico y detallado"""
        
        # Generar título específico
        title = self._generate_specific_title(criteria, context, case_type)
        
        # Generar feature específica
        feature = self._generate_specific_feature(user_story, context)
        
        # Generar precondiciones específicas
        preconditions = self._generate_specific_preconditions(criteria, context)
        
        # Generar escenario específico
        scenario = self._generate_specific_scenario(criteria, context, case_type)
        
        # Generar pasos específicos
        given_steps = self._generate_specific_given_steps(criteria, context, case_type)
        when_steps = self._generate_specific_when_steps(criteria, context, case_type)
        then_steps = self._generate_specific_then_steps(criteria, context, case_type)
        
        # Generar tags específicos
        tags = self._generate_specific_tags(criteria, context, case_type)
        
        return EnhancedGherkinTestCase(
            id=f"TC-{criteria_index:03d}" + (f"-{case_type.upper()}" if case_type != "funcional" else ""),
            title=title,
            feature=feature,
            preconditions=preconditions,
            scenario=scenario,
            given_steps=given_steps,
            when_steps=when_steps,
            then_steps=then_steps,
            tags=tags,
            test_type=case_type,
            priority="alta" if case_type == "funcional" else "media",
            user_story=user_story.title
        )
    
    def _generate_specific_title(self, criteria: str, context: Dict[str, Any], case_type: str) -> str:
        """Genera título específico y descriptivo como ChatGPT"""
        criteria_lower = criteria.lower()
        
        if context['domain'] == 'alumbrado_publico':
            if 'mostrar' in criteria_lower and 'alerta' in criteria_lower and 'icono' in criteria_lower:
                return "Mostrar alerta cuando no hay acuerdo vigente"
            elif 'no mostrar' in criteria_lower and 'icono' in criteria_lower:
                return "No mostrar alerta cuando hay acuerdo vigente"
            elif 'bloqueo' in criteria_lower and 'crear' in criteria_lower:
                return "Bloqueo al crear condicional en municipio sin acuerdo vigente"
            elif 'importar' in criteria_lower and 'bloqueo' in criteria_lower:
                return "Bloqueo al importar condicionales en municipio sin acuerdo vigente"
            elif 'editar' in criteria_lower and 'alerta' in criteria_lower:
                return "Mensaje de alerta en edición de condicional sin acuerdo vigente"
            elif 'tooltip' in criteria_lower:
                return "Verificar tooltip con mensaje del backend"
            elif 'consistencia' in criteria_lower:
                return "Consistencia en desktop y móvil"
            elif 'rendimiento' in criteria_lower:
                return "Verificar rendimiento de la funcionalidad"
        
        # Fallback genérico
        return f"Verificar funcionalidad - {case_type.title()}"
    
    def _generate_specific_feature(self, user_story: UserStory, context: Dict[str, Any]) -> str:
        """Genera feature específica"""
        if context['domain'] == 'alumbrado_publico':
            return "Gestión de condicionales de alumbrado público"
        elif context['domain'] == 'authentication':
            return "Autenticación de usuarios"
        else:
            return f"Funcionalidad para {user_story.title}"
    
    def _generate_specific_preconditions(self, criteria: str, context: Dict[str, Any]) -> List[str]:
        """Genera precondiciones específicas y detalladas"""
        preconditions = []
        criteria_lower = criteria.lower()
        
        if context['domain'] == 'alumbrado_publico':
            if 'municipio' in criteria_lower:
                if 'sin acuerdo' in criteria_lower:
                    preconditions.append("Existe un municipio con condicionales de alumbrado.")
                    preconditions.append("Dicho municipio no tiene acuerdo vigente registrado en el módulo de acuerdos.")
                else:
                    preconditions.append("Existe un municipio con acuerdo vigente en el módulo de acuerdos.")
                    preconditions.append("Dicho municipio tiene condicionales de alumbrado registradas.")
            
            if 'importar' in criteria_lower:
                preconditions.append("Archivo Excel con condicionales de alumbrado para municipio sin acuerdo vigente.")
            
            if 'editar' in criteria_lower:
                preconditions.append("Municipio con condicionales creadas previamente.")
                preconditions.append("El acuerdo de alumbrado ya no está vigente.")
        
        return preconditions
    
    def _generate_specific_scenario(self, criteria: str, context: Dict[str, Any], case_type: str) -> str:
        """Genera escenario específico como ChatGPT"""
        criteria_lower = criteria.lower()
        
        if context['domain'] == 'alumbrado_publico':
            if 'mostrar' in criteria_lower and 'alerta' in criteria_lower and 'icono' in criteria_lower:
                return "Mostrar icono de alerta en condicionales sin acuerdo"
            elif 'no mostrar' in criteria_lower and 'icono' in criteria_lower:
                return "No mostrar icono en municipios con acuerdo vigente"
            elif 'bloqueo' in criteria_lower and 'crear' in criteria_lower:
                return "Bloquear creación de condicional sin acuerdo vigente"
            elif 'importar' in criteria_lower and 'bloqueo' in criteria_lower:
                return "Bloquear importación de condicionales sin acuerdo vigente"
            elif 'editar' in criteria_lower and 'alerta' in criteria_lower:
                return "Mostrar alerta al editar condicional sin acuerdo vigente"
            elif 'tooltip' in criteria_lower:
                return "Verificar tooltip con mensaje literal del backend"
            elif 'consistencia' in criteria_lower:
                return "Verificar consistencia cross-platform"
            elif 'rendimiento' in criteria_lower:
                return "Verificar que no afecta el rendimiento"
        
        return f"Verificar funcionalidad - {case_type}"
    
    def _generate_specific_given_steps(self, criteria: str, context: Dict[str, Any], case_type: str) -> List[str]:
        """Genera pasos Given específicos"""
        steps = []
        criteria_lower = criteria.lower()
        
        if context['domain'] == 'alumbrado_publico':
            if 'municipio' in criteria_lower and 'sin acuerdo' in criteria_lower:
                steps.append("un municipio con condicionales de tipo Alumbrado y sin acuerdo vigente")
            elif 'municipio' in criteria_lower and 'con acuerdo' in criteria_lower:
                steps.append("un municipio con acuerdo de alumbrado vigente")
            elif 'importar' in criteria_lower:
                steps.append("un archivo de importación con condicionales de tipo Alumbrado")
                steps.append("el municipio de destino no tiene acuerdo vigente")
            elif 'editar' in criteria_lower:
                steps.append("un municipio sin acuerdo de alumbrado vigente")
                steps.append("una condicional de alumbrado previamente creada")
        
        return steps
    
    def _generate_specific_when_steps(self, criteria: str, context: Dict[str, Any], case_type: str) -> List[str]:
        """Genera pasos When específicos"""
        steps = []
        criteria_lower = criteria.lower()
        
        if context['domain'] == 'alumbrado_publico':
            if 'consultar' in criteria_lower or 'tabla' in criteria_lower:
                steps.append("el usuario consulta la tabla de condicionales en Impuestos Adicionales")
            elif 'crear' in criteria_lower:
                steps.append("el usuario intenta crear una nueva condicional manualmente")
            elif 'importar' in criteria_lower:
                steps.append("el usuario importa el archivo")
            elif 'editar' in criteria_lower:
                steps.append("el usuario edita la condicional")
        
        return steps
    
    def _generate_specific_then_steps(self, criteria: str, context: Dict[str, Any], case_type: str) -> List[str]:
        """Genera pasos Then específicos como ChatGPT"""
        steps = []
        criteria_lower = criteria.lower()
        
        if context['domain'] == 'alumbrado_publico':
            if 'mostrar' in criteria_lower and 'icono' in criteria_lower and 'tooltip' in criteria_lower:
                steps.append("se muestra un icono de alerta (⚠) en la fila de cada condicional afectada")
                steps.append("al hacer hover sobre el icono aparece un tooltip con el mensaje literal del backend")
            elif 'no mostrar' in criteria_lower and 'icono' in criteria_lower:
                steps.append("no se muestra ningún icono de alerta en las filas de condicionales")
            elif 'bloqueo' in criteria_lower and 'crear' in criteria_lower:
                steps.append("el sistema muestra un mensaje de error en rojo")
                steps.append('el mensaje indica literalmente: "El municipio <X> no tiene un acuerdo de alumbrado vigente"')
            elif 'importar' in criteria_lower and 'bloqueo' in criteria_lower:
                steps.append("el sistema rechaza las filas correspondientes")
                steps.append("muestra en la modal de errores el detalle por línea con el mensaje literal enviado por backend")
            elif 'editar' in criteria_lower and 'alerta' in criteria_lower:
                steps.append("se muestra un mensaje de alerta en la parte superior del formulario")
                steps.append("el mensaje es el literal enviado por backend")
            elif 'consistencia' in criteria_lower:
                steps.append("la funcionalidad es consistente en ambos dispositivos")
                steps.append("el comportamiento es idéntico en desktop y móvil")
            elif 'rendimiento' in criteria_lower:
                steps.append("el rendimiento no se ve afectado")
                steps.append("la navegación de la tabla es fluida")
                steps.append("el icono y tooltip no impactan la velocidad de carga")
        
        return steps
    
    def _generate_specific_tags(self, criteria: str, context: Dict[str, Any], case_type: str) -> List[str]:
        """Genera tags específicos"""
        tags = [case_type]
        
        if context['domain'] == 'alumbrado_publico':
            tags.extend(['alumbrado-publico', 'municipio', 'acuerdo'])
        
        if 'icono' in criteria.lower():
            tags.append('ui-element')
        if 'tooltip' in criteria.lower():
            tags.append('tooltip')
        if 'error' in criteria.lower():
            tags.append('error-handling')
        if 'validación' in criteria.lower():
            tags.append('validacion')
        
        return tags
    
    def _generate_contextual_cases(self, user_story: UserStory, context: Dict[str, Any]) -> List[EnhancedGherkinTestCase]:
        """Genera casos adicionales basados en contexto"""
        cases = []
        
        # Caso de consistencia cross-platform si se menciona
        if any('consistente' in validation for validation in context['validations']):
            consistency_case = EnhancedGherkinTestCase(
                id="TC-CONS-001",
                title="Consistencia en desktop y móvil",
                feature=context['domain'],
                preconditions=["Sistema funcionando en diferentes dispositivos"],
                scenario="Verificar consistencia cross-platform",
                given_steps=["un usuario accediendo desde desktop", "un usuario accediendo desde móvil"],
                when_steps=["ambos usuarios realizan la misma acción"],
                then_steps=["la funcionalidad es consistente en ambos dispositivos"],
                tags=["consistencia", "cross-platform"],
                test_type="funcional",
                priority="media",
                user_story=user_story.title
            )
            cases.append(consistency_case)
        
        # Caso de rendimiento si se menciona
        if any('rendimiento' in validation for validation in context['validations']):
            performance_case = EnhancedGherkinTestCase(
                id="TC-PERF-001",
                title="Verificar rendimiento de la funcionalidad",
                feature=context['domain'],
                preconditions=["Sistema con datos de prueba"],
                scenario="Verificar que no afecta el rendimiento",
                given_steps=["una tabla con múltiples registros"],
                when_steps=["el usuario realiza la acción"],
                then_steps=["el rendimiento no se ve afectado", "la navegación es fluida"],
                tags=["rendimiento", "performance"],
                test_type="funcional",
                priority="media",
                user_story=user_story.title
            )
            cases.append(performance_case)
        
        return cases
    
    def format_enhanced_gherkin_for_linear(self, enhanced_case: EnhancedGherkinTestCase) -> str:
        """Formatea un caso mejorado para exportar a Linear"""
        gherkin_text = []
        
        # Feature
        gherkin_text.append(f"Feature: {enhanced_case.feature}")
        gherkin_text.append("")
        
        # Background
        if enhanced_case.background:
            gherkin_text.append("Background:")
            gherkin_text.append(f"  {enhanced_case.background}")
            gherkin_text.append("")
        
        # Tags
        if enhanced_case.tags:
            gherkin_text.append(" ".join([f"@{tag}" for tag in enhanced_case.tags]))
        
        # Scenario
        gherkin_text.append(f"Scenario: {enhanced_case.scenario}")
        gherkin_text.append("")
        
        # Given steps
        for step in enhanced_case.given_steps:
            gherkin_text.append(f"  Given {step}")
        
        # When steps
        for step in enhanced_case.when_steps:
            gherkin_text.append(f"  When {step}")
        
        # Then steps
        for step in enhanced_case.then_steps:
            gherkin_text.append(f"  Then {step}")
        
        return "\n".join(gherkin_text)

def main():
    """Función principal para probar el generador mejorado"""
    # Ejemplo con alumbrado público
    user_story = UserStory(
        title="Como usuario quiero gestionar condicionales de alumbrado público",
        description="El usuario necesita poder ver alertas cuando no hay acuerdos vigentes para condicionales de alumbrado público",
        acceptance_criteria=[
            "Dado que existe un municipio con condicionales de alumbrado sin acuerdo vigente, cuando el usuario consulta la tabla de condicionales, entonces se muestra un icono de alerta con tooltip informativo",
            "Dado que existe un municipio con acuerdo vigente, cuando el usuario consulta la tabla, entonces no se muestra ningún icono de alerta",
            "Dado que un municipio no tiene acuerdo vigente, cuando el usuario intenta crear una condicional, entonces el sistema muestra un mensaje de error bloqueando la acción"
        ]
    )
    
    qa_comments = """
    Validaciones importantes:
    - Verificar que el icono de alerta se muestra correctamente
    - Validar que el tooltip muestra el mensaje literal del backend
    - Verificar que no se muestra icono cuando hay acuerdo vigente
    - Validar consistencia en desktop y móvil
    - Verificar que no afecta el rendimiento de la tabla
    - Validar mensajes de error específicos para bloqueos
    """
    
    print("🚀 Probando Generador Gherkin Mejorado")
    print("=" * 60)
    
    generator = EnhancedGherkinGenerator()
    enhanced_cases = generator.generate_enhanced_cases(user_story, qa_comments)
    
    print(f"📊 Casos generados: {len(enhanced_cases)}")
    print()
    
    for i, case in enumerate(enhanced_cases, 1):
        print(f"📋 CASO {i}: {case.id} - {case.title}")
        print(f"🏷️  Tags: {', '.join(case.tags)}")
        print(f"📝 Tipo: {case.test_type} | Prioridad: {case.priority}")
        print(f"📋 Precondiciones: {', '.join(case.preconditions)}")
        print()
        
        gherkin_text = generator.format_enhanced_gherkin_for_linear(case)
        print("📄 Formato Gherkin Mejorado:")
        print("-" * 40)
        print(gherkin_text)
        print("-" * 40)
        print()
    
    print("✅ Prueba completada exitosamente!")

if __name__ == "__main__":
    main()
