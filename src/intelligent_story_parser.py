#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analizador Inteligente de Historias de Usuario
Procesa texto completo de manera robusta para extraer todos los criterios de valor
"""

import re
import json
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

@dataclass
class IntelligentUserStory:
    """Historia de usuario con análisis inteligente"""
    title: str
    description: str
    acceptance_criteria: List[str]
    technical_requirements: List[str]
    business_rules: List[str]
    ui_elements: List[str]
    data_requirements: List[str]
    integration_points: List[str]
    validation_rules: List[str]
    epic: Optional[str] = None
    story_points: Optional[int] = None
    priority: str = "Media"
    domain: str = "General"
    complexity_score: float = 0.0

class IntelligentStoryParser:
    """Parser inteligente que analiza todo el contenido de valor"""
    
    def __init__(self):
        # Patrones para diferentes tipos de contenido
        self.patterns = {
            # Criterios de aceptación
            'acceptance_criteria': [
                r'(?:dado|given)\s+(.+?)(?:\s+(?:cuando|when)\s+(.+?))?(?:\s+(?:entonces|then)\s+(.+?))?',
                r'(?:criterio|acceptance|ac)[\s\d]*[:\.]?\s*(.+)',
                r'(?:debe|should|tiene que|must)\s+(.+)',
                r'(?:el sistema|the system)\s+(.+)',
                r'(?:se debe|should be|debe ser)\s+(.+)',
            ],
            
            # Requisitos técnicos
            'technical_requirements': [
                r'(?:json|xml|api|rest|graphql|database|db|sql)\s+(.+)',
                r'(?:backend|frontend|server|client)\s+(.+)',
                r'(?:endpoint|service|microservice)\s+(.+)',
                r'(?:configurar|configure|setup)\s+(.+)',
                r'(?:integrar|integrate|conectar|connect)\s+(.+)',
            ],
            
            # Reglas de negocio
            'business_rules': [
                r'(?:regla|rule|política|policy)\s+(.+)',
                r'(?:si|if)\s+(.+?)(?:\s+(?:entonces|then)\s+(.+))?',
                r'(?:cuando|when)\s+(.+?)(?:\s+(?:debe|should)\s+(.+))?',
                r'(?:porcentaje|percentage|cálculo|calculation)\s+(.+)',
                r'(?:validar|validate|verificar|verify)\s+(.+)',
            ],
            
            # Elementos de UI
            'ui_elements': [
                r'(?:botón|button|campo|field|formulario|form)\s+(.+)',
                r'(?:tabla|table|lista|list|grid)\s+(.+)',
                r'(?:modal|popup|dialog|ventana|window)\s+(.+)',
                r'(?:icono|icon|imagen|image)\s+(.+)',
                r'(?:menú|menu|navegación|navigation)\s+(.+)',
                r'(?:responsive|móvil|mobile|desktop)\s+(.+)',
            ],
            
            # Requisitos de datos
            'data_requirements': [
                r'(?:campo|field|variable|parameter)\s+(.+)',
                r'(?:enviar|send|recibir|receive)\s+(.+)',
                r'(?:guardar|save|almacenar|store)\s+(.+)',
                r'(?:cargar|load|obtener|get|fetch)\s+(.+)',
                r'(?:formato|format|estructura|structure)\s+(.+)',
            ],
            
            # Puntos de integración
            'integration_points': [
                r'(?:odoo|erp|crm|sistema externo|external system)\s+(.+)',
                r'(?:api|servicio|service|endpoint)\s+(.+)',
                r'(?:base de datos|database|bd|db)\s+(.+)',
                r'(?:sincronizar|sync|actualizar|update)\s+(.+)',
            ],
            
            # Reglas de validación
            'validation_rules': [
                r'(?:validar|validate|verificar|verify|comprobar|check)\s+(.+)',
                r'(?:obligatorio|required|requerido|mandatory)\s+(.+)',
                r'(?:opcional|optional|no requerido)\s+(.+)',
                r'(?:formato|format|patrón|pattern)\s+(.+)',
                r'(?:longitud|length|tamaño|size)\s+(.+)',
            ]
        }
        
        # Palabras clave para detectar dominios
        self.domain_keywords = {
            'backend': ['backend', 'api', 'servidor', 'base de datos', 'odoo', 'erp'],
            'frontend': ['frontend', 'ui', 'interfaz', 'usuario', 'pantalla', 'vista'],
            'integration': ['integración', 'api', 'servicio', 'conectar', 'sincronizar'],
            'data': ['datos', 'información', 'campo', 'variable', 'json', 'xml'],
            'business': ['negocio', 'regla', 'política', 'proceso', 'flujo'],
            'validation': ['validación', 'verificar', 'comprobar', 'obligatorio']
        }
        
        # Indicadores de complejidad
        self.complexity_indicators = {
            'high': ['integración', 'api', 'múltiple', 'complejo', 'avanzado', 'dinámico'],
            'medium': ['configurar', 'validar', 'procesar', 'calcular', 'generar'],
            'low': ['mostrar', 'visualizar', 'listar', 'simple', 'básico']
        }
    
    def parse_intelligent(self, text: str) -> IntelligentUserStory:
        """Análisis inteligente completo del texto"""
        
        # Limpiar y preparar texto
        clean_text = self._clean_text(text)
        sentences = self._split_into_sentences(clean_text)
        
        # Extraer información básica
        title = self._extract_title(clean_text)
        description = self._extract_description(clean_text)
        
        # Análisis inteligente por categorías
        acceptance_criteria = self._extract_by_patterns(sentences, 'acceptance_criteria')
        technical_requirements = self._extract_by_patterns(sentences, 'technical_requirements')
        business_rules = self._extract_by_patterns(sentences, 'business_rules')
        ui_elements = self._extract_by_patterns(sentences, 'ui_elements')
        data_requirements = self._extract_by_patterns(sentences, 'data_requirements')
        integration_points = self._extract_by_patterns(sentences, 'integration_points')
        validation_rules = self._extract_by_patterns(sentences, 'validation_rules')
        
        # Análisis de dominio y complejidad
        domain = self._detect_domain(clean_text)
        complexity_score = self._calculate_complexity(clean_text)
        
        # Si no hay criterios explícitos, generar desde el contenido
        if not acceptance_criteria:
            acceptance_criteria = self._generate_criteria_from_content(
                sentences, technical_requirements, business_rules, ui_elements
            )
        
        return IntelligentUserStory(
            title=title,
            description=description,
            acceptance_criteria=acceptance_criteria,
            technical_requirements=technical_requirements,
            business_rules=business_rules,
            ui_elements=ui_elements,
            data_requirements=data_requirements,
            integration_points=integration_points,
            validation_rules=validation_rules,
            domain=domain,
            complexity_score=complexity_score
        )
    
    def _clean_text(self, text: str) -> str:
        """Limpia y normaliza el texto"""
        # Remover caracteres especiales innecesarios
        text = re.sub(r'[✓✅]', '', text)
        # Normalizar espacios
        text = re.sub(r'\s+', ' ', text)
        # Normalizar puntuación
        text = re.sub(r'\.{2,}', '.', text)
        return text.strip()
    
    def _split_into_sentences(self, text: str) -> List[str]:
        """Divide el texto en oraciones inteligentemente"""
        # Dividir por puntos, pero mantener contexto
        sentences = re.split(r'[.!?]\s+', text)
        
        # Dividir también por saltos de línea significativos
        all_sentences = []
        for sentence in sentences:
            if '\n' in sentence:
                sub_sentences = [s.strip() for s in sentence.split('\n') if s.strip()]
                all_sentences.extend(sub_sentences)
            else:
                if sentence.strip():
                    all_sentences.append(sentence.strip())
        
        # Filtrar oraciones muy cortas o vacías
        return [s for s in all_sentences if len(s) > 10]
    
    def _extract_title(self, text: str) -> str:
        """Extrae el título de manera inteligente"""
        lines = text.split('\n')
        
        # Buscar patrones de título
        for line in lines[:5]:  # Solo en las primeras líneas
            line = line.strip()
            if not line:
                continue
                
            # Patrones de historia de usuario
            if re.match(r'como\s+.+\s+quiero\s+.+\s+para\s+', line.lower()):
                return line
            
            # Títulos descriptivos
            if any(keyword in line.lower() for keyword in ['backend', 'frontend', 'sistema', 'configurar']):
                return line
        
        # Si no encuentra patrón específico, usar la primera línea significativa
        for line in lines:
            line = line.strip()
            if len(line) > 20 and not line.lower().startswith(('descripción', 'criterio')):
                return line
        
        return "Historia de Usuario"
    
    def _extract_description(self, text: str) -> str:
        """Extrae descripción de manera inteligente"""
        lines = text.split('\n')
        description_lines = []
        
        in_description = False
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Detectar inicio de descripción
            if any(keyword in line.lower() for keyword in ['descripción', 'description', 'contexto']):
                in_description = True
                continue
            
            # Detectar fin de descripción
            if any(keyword in line.lower() for keyword in ['criterio', 'acceptance', 'requisito']):
                break
            
            # Si estamos en descripción o es contenido descriptivo
            if in_description or (not any(keyword in line.lower() for keyword in ['como', 'as a'])):
                if len(line) > 15:  # Solo líneas con contenido sustancial
                    description_lines.append(line)
        
        return ' '.join(description_lines)
    
    def _extract_by_patterns(self, sentences: List[str], category: str) -> List[str]:
        """Extrae contenido usando patrones específicos"""
        results = []
        patterns = self.patterns.get(category, [])
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) < 10:
                continue
                
            # Para requisitos técnicos, buscar patrones específicos
            if category == 'technical_requirements':
                if any(word in sentence.lower() for word in ['json', 'backend', 'frontend', 'api', 'odoo']):
                    results.append(sentence)
            
            # Para requisitos de datos, buscar patrones específicos
            elif category == 'data_requirements':
                if any(word in sentence.lower() for word in ['campo', 'variable', 'json', 'tabla', 'anexo']):
                    results.append(sentence)
            
            # Para reglas de negocio, buscar patrones específicos
            elif category == 'business_rules':
                if any(word in sentence.lower() for word in ['regla', 'cálculo', 'proceso', 'condicional']):
                    results.append(sentence)
            
            # Para criterios de aceptación, usar patrones regex
            elif category == 'acceptance_criteria':
                for pattern in patterns:
                    matches = re.findall(pattern, sentence, re.IGNORECASE)
                    for match in matches:
                        if isinstance(match, tuple):
                            # Para patrones con grupos, combinar los grupos no vacíos
                            combined = ' '.join([m for m in match if m.strip()])
                            if combined and len(combined) > 10:
                                results.append(combined.strip())
                        else:
                            if match and len(match) > 10:
                                results.append(match.strip())
            
            # Para otras categorías, usar patrones regex normales
            else:
                for pattern in patterns:
                    matches = re.findall(pattern, sentence, re.IGNORECASE)
                    for match in matches:
                        if isinstance(match, tuple):
                            combined = ' '.join([m for m in match if m.strip()])
                            if combined and len(combined) > 10:
                                results.append(combined.strip())
                        else:
                            if match and len(match) > 10:
                                results.append(match.strip())
        
        # Remover duplicados manteniendo orden
        seen = set()
        unique_results = []
        for item in results:
            if item.lower() not in seen:
                seen.add(item.lower())
                unique_results.append(item)
        
        return unique_results
    
    def _generate_criteria_from_content(self, sentences: List[str], 
                                      technical_req: List[str], 
                                      business_rules: List[str], 
                                      ui_elements: List[str]) -> List[str]:
        """Genera criterios de aceptación desde el contenido disponible"""
        criteria = []
        
        # Analizar oraciones para extraer criterios específicos
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) < 15:
                continue
                
            # Patrones específicos para generar criterios completos
            if 'variables dinámicas' in sentence.lower() and 'json' in sentence.lower():
                criteria.append(f"Dado que el backend procesa datos, cuando las variables dinámicas son enviadas, entonces deben llegar en formato JSON")
            
            elif 'párrafos condicionales' in sentence.lower() and 'reglas' in sentence.lower():
                criteria.append(f"Dado que existen párrafos condicionales, cuando se procesan los RECs, entonces se deben construir según las reglas establecidas")
            
            elif 'porcentajes' in sentence.lower() and 'backend' in sentence.lower():
                criteria.append(f"Dado que se requieren cálculos, cuando se procesan porcentajes y valores, entonces deben calcularse en backend y no en frontend")
            
            elif 'anexo' in sentence.lower() and 'tabla dinámica' in sentence.lower():
                criteria.append(f"Dado que se requiere el Anexo 1, cuando se solicita la información, entonces debe enviarse como tabla dinámica en JSON")
            
            elif 'mail_notificaciones' in sentence.lower():
                criteria.append(f"Dado que se configuran notificaciones, cuando se procesa la información, entonces el campo mail_notificaciones debe incluirse en JSON")
            
            elif 'links embebidos' in sentence.lower():
                criteria.append(f"Dado que existen links embebidos, cuando se procesa el contenido, entonces deben enviarse para renderizado en frontend")
            
            elif 'frontera' in sentence.lower() and ('región' in sentence.lower() or 'capex' in sentence.lower()):
                criteria.append(f"Dado que se procesan datos de frontera, cuando se calculan valores por región, entonces {sentence}")
            
            elif 'eholder' in sentence.lower():
                criteria.append(f"Dado que se requiere información de imagen, cuando se procesa el eholder, entonces debe incluirse correctamente")
            
            elif 'certificados' in sentence.lower() and 'días' in sentence.lower():
                criteria.append(f"Dado que se gestionan certificados, cuando se procesan las fechas, entonces deben entregarse dentro de los 10 días hábiles siguientes")
            
            elif 'arreglo' in sentence.lower() and 'fronteras' in sentence.lower():
                criteria.append(f"Dado que se requiere información de fronteras, cuando el backend procesa los datos, entonces debe enviar arreglo con todas las fronteras del cliente")
            
            # Patrones generales
            elif any(word in sentence.lower() for word in ['debe', 'tiene que', 'se requiere', 'es necesario']):
                criteria.append(f"Dado el contexto del sistema, cuando se ejecuta la funcionalidad, entonces {sentence}")
            
            elif any(word in sentence.lower() for word in ['json', 'api', 'backend', 'frontend']):
                criteria.append(f"Requisito técnico: {sentence}")
            
            elif any(word in sentence.lower() for word in ['regla', 'cálculo', 'proceso']):
                criteria.append(f"Regla de negocio: {sentence}")
        
        # Generar criterios desde requisitos técnicos
        for req in technical_req:
            if req not in [c for c in criteria]:  # Evitar duplicados
                criteria.append(f"Requisito técnico: {req}")
        
        # Generar criterios desde reglas de negocio
        for rule in business_rules:
            if rule not in [c for c in criteria]:  # Evitar duplicados
                criteria.append(f"Regla de negocio: {rule}")
        
        # Generar criterios desde elementos UI
        for element in ui_elements:
            criteria.append(f"Elemento UI: {element}")
        
        return criteria[:15]  # Limitar a 15 criterios principales
    
    def _detect_domain(self, text: str) -> str:
        """Detecta el dominio principal del texto"""
        text_lower = text.lower()
        domain_scores = {}
        
        for domain, keywords in self.domain_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                domain_scores[domain] = score
        
        if domain_scores:
            return max(domain_scores, key=domain_scores.get)
        return "General"
    
    def _calculate_complexity(self, text: str) -> float:
        """Calcula un score de complejidad"""
        text_lower = text.lower()
        complexity_score = 0.0
        
        # Contar indicadores de complejidad
        for level, indicators in self.complexity_indicators.items():
            count = sum(1 for indicator in indicators if indicator in text_lower)
            if level == 'high':
                complexity_score += count * 3
            elif level == 'medium':
                complexity_score += count * 2
            else:
                complexity_score += count * 1
        
        # Normalizar entre 0 y 10
        return min(complexity_score / 2, 10.0)
    
    def get_analysis_summary(self, story: IntelligentUserStory) -> Dict[str, Any]:
        """Genera un resumen del análisis"""
        return {
            'title': story.title,
            'domain': story.domain,
            'complexity_score': story.complexity_score,
            'total_criteria': len(story.acceptance_criteria),
            'technical_requirements_count': len(story.technical_requirements),
            'business_rules_count': len(story.business_rules),
            'ui_elements_count': len(story.ui_elements),
            'data_requirements_count': len(story.data_requirements),
            'integration_points_count': len(story.integration_points),
            'validation_rules_count': len(story.validation_rules),
            'analysis_quality': self._assess_analysis_quality(story)
        }
    
    def _assess_analysis_quality(self, story: IntelligentUserStory) -> str:
        """Evalúa la calidad del análisis"""
        total_elements = (
            len(story.acceptance_criteria) +
            len(story.technical_requirements) +
            len(story.business_rules) +
            len(story.ui_elements) +
            len(story.data_requirements)
        )
        
        if total_elements >= 10:
            return "Excelente"
        elif total_elements >= 6:
            return "Buena"
        elif total_elements >= 3:
            return "Aceptable"
        else:
            return "Necesita mejora"

def main():
    """Función de prueba"""
    # Ejemplo de uso
    sample_text = """
    Como backend de Odoo,
    
    Todas las variables dinámicas llegan en JSON. Los párrafos condicionales de RECs se construyen según reglas. 
    Los porcentajes y valores se calculan en backend y no en front. El Anexo 1 se envía como tabla dinámica en JSON. 
    El campo mail_notificaciones se incluye en JSON. Links embebidos se envían para renderizado en front.
    """
    
    parser = IntelligentStoryParser()
    story = parser.parse_intelligent(sample_text)
    summary = parser.get_analysis_summary(story)
    
    print("📋 ANÁLISIS INTELIGENTE")
    print("=" * 50)
    print(f"Título: {story.title}")
    print(f"Dominio: {story.domain}")
    print(f"Complejidad: {story.complexity_score}/10")
    print(f"Criterios de Aceptación: {len(story.acceptance_criteria)}")
    print(f"Requisitos Técnicos: {len(story.technical_requirements)}")
    print(f"Reglas de Negocio: {len(story.business_rules)}")
    print(f"Calidad del Análisis: {summary['analysis_quality']}")
    
    print("\n📝 CRITERIOS DE ACEPTACIÓN:")
    for i, criteria in enumerate(story.acceptance_criteria, 1):
        print(f"{i}. {criteria}")

if __name__ == "__main__":
    main()
