#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parser Adaptativo para Historias de Usuario
Detecta automáticamente el tipo de estructura (tradicional vs narrativa/EMS)
y extrae criterios de aceptación sin romper compatibilidad
"""

import re
from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum


class StoryStructureType(Enum):
    """Tipos de estructuras de HU detectadas"""
    TRADITIONAL = "traditional"  # Contexto, Descripción, Criterios de aceptación
    NARRATIVE = "narrative"  # Narrativa/EMS con flujos, estados, referencias
    MIXED = "mixed"  # Combina ambos formatos
    UNKNOWN = "unknown"  # No se puede determinar claramente


@dataclass
class ParsedStory:
    """Historia de usuario parseada con información completa"""
    title: str
    structure_type: StoryStructureType
    context: str
    description: str
    acceptance_criteria: List[str]
    user_flows: List[str]  # Flujos de usuario extraídos
    states: List[str]  # Estados del sistema extraídos
    ui_elements: List[str]  # Elementos de UI mencionados
    technical_requirements: List[str]  # Requisitos técnicos
    raw_text: str  # Texto original para referencia


class AdaptiveParser:
    """
    Parser adaptativo que detecta automáticamente el tipo de estructura
    y extrae información de forma inteligente
    """
    
    def __init__(self):
        # Patrones para detectar estructura tradicional
        self.traditional_patterns = {
            'context': r'(?:^|\n)\s*[Cc]ontexto[:\s]+(.*?)(?=\n\s*(?:[Dd]escripci[óo]n|[Rr]equerimiento|[Cc]riterio|$))',
            'description': r'(?:^|\n)\s*[Dd]escripci[óo]n[:\s]+(.*?)(?=\n\s*(?:[Rr]equerimiento|[Cc]riterio|$))',
            'criteria_section': r'(?:^|\n)\s*[Cc]riterios?\s+de\s+[Aa]ceptaci[óo]n[:\s]+(.*?)(?=\n\n[A-Z]|\n\s*[A-Z][a-z]+:|$)',
        }
        
        # Patrones para detectar estructura narrativa/EMS
        self.narrative_patterns = {
            'figma_links': r'https?://(?:www\.)?figma\.com/[^\s]+',
            'user_flows': r'(?:Al\s+)?(?:darle|dar|hacer|presionar|click|seleccionar|ingresar|subir|descargar|arrastrar|drag)[^\.]+\.',
            'states': r'(?:estado|state|pantalla|screen|vista|view)[:\s]+([^\.]+)',
            'ui_elements': r'(?:botón|button|campo|field|tabla|table|modal|popup|pop-up|rectángulo|calendario|loader|spinner)[:\s]*([^\.]+)',
            'actions': r'(?:debe|debería|puede|permite|valida|guarda|toma|muestra|oculta|abre|cierra)[^\.]+\.',
            'conditions': r'(?:si|cuando|al|después|antes|mientras|hasta)[^\.]+\.',
        }
        
        # Palabras clave que indican estructura narrativa
        self.narrative_keywords = [
            'figma', 'onboarding', 'configuración', 'pantalla', 'estado',
            'flujo', 'proceso', 'paso', 'pestaña', 'sección', 'pop-up',
            'modal', 'loader', 'calendario', 'drag', 'drop', 'arrastrar'
        ]
        
        # Palabras clave que indican estructura tradicional
        self.traditional_keywords = [
            'contexto', 'descripción', 'criterios de aceptación',
            'requerimientos', 'requisitos funcionales'
        ]
    
    def parse(self, text: str) -> ParsedStory:
        """
        Parsea una historia de usuario detectando automáticamente su estructura
        
        Args:
            text: Texto completo de la HU
            
        Returns:
            ParsedStory con toda la información extraída
        """
        # Detectar tipo de estructura
        structure_type = self._detect_structure_type(text)
        
        print(f"[INFO] Estructura detectada: {structure_type.value}", flush=True)
        
        # Extraer título
        title = self._extract_title(text, structure_type)
        
        # Extraer información según el tipo de estructura
        if structure_type == StoryStructureType.TRADITIONAL:
            return self._parse_traditional(text, title, structure_type)
        elif structure_type == StoryStructureType.NARRATIVE:
            return self._parse_narrative(text, title, structure_type)
        else:  # MIXED o UNKNOWN
            return self._parse_mixed(text, title, structure_type)
    
    def _detect_structure_type(self, text: str) -> StoryStructureType:
        """Detecta el tipo de estructura de la HU"""
        text_lower = text.lower()
        
        # Contar indicadores de cada tipo
        traditional_score = 0
        narrative_score = 0
        
        # Verificar estructura tradicional
        if re.search(self.traditional_patterns['context'], text, re.IGNORECASE | re.MULTILINE):
            traditional_score += 3
        if re.search(self.traditional_patterns['description'], text, re.IGNORECASE | re.MULTILINE):
            traditional_score += 3
        if re.search(self.traditional_patterns['criteria_section'], text, re.IGNORECASE | re.MULTILINE):
            traditional_score += 5
        
        for keyword in self.traditional_keywords:
            if keyword in text_lower:
                traditional_score += 1
        
        # Verificar estructura narrativa
        if re.search(self.narrative_patterns['figma_links'], text):
            narrative_score += 5
        if len(re.findall(self.narrative_patterns['user_flows'], text, re.IGNORECASE)) > 0:
            narrative_score += 3
        if len(re.findall(self.narrative_patterns['states'], text, re.IGNORECASE)) > 0:
            narrative_score += 2
        
        for keyword in self.narrative_keywords:
            if keyword in text_lower:
                narrative_score += 1
        
        # Determinar tipo
        if traditional_score >= 5 and narrative_score < 3:
            return StoryStructureType.TRADITIONAL
        elif narrative_score >= 5 and traditional_score < 3:
            return StoryStructureType.NARRATIVE
        elif traditional_score >= 3 and narrative_score >= 3:
            return StoryStructureType.MIXED
        else:
            return StoryStructureType.UNKNOWN
    
    def _extract_title(self, text: str, structure_type: StoryStructureType) -> str:
        """Extrae el título de la HU"""
        lines = text.split('\n')
        
        # Buscar primera línea significativa
        for line in lines[:5]:  # Revisar primeras 5 líneas
            line = line.strip()
            if len(line) > 10:
                # Si no es una sección conocida, es probablemente el título
                if not re.match(r'^(?:Contexto|Descripción|Requerimiento|Criterio|Análisis|Configuración)', line, re.IGNORECASE):
                    # Limpiar posibles prefijos como "HU:", "BACK:", etc.
                    title = re.sub(r'^(?:HU|BACK|FRONT|EMS|TEC|FIN)[:\s-]+\s*', '', line, flags=re.IGNORECASE)
                    if len(title) > 5:
                        return title.strip()
        
        # Fallback: primeras palabras significativas
        first_line = lines[0].strip() if lines else ""
        if len(first_line) > 10:
            return first_line[:100]
        
        return "Historia de Usuario"
    
    def _parse_traditional(self, text: str, title: str, structure_type: StoryStructureType) -> ParsedStory:
        """Parsea estructura tradicional (Contexto, Descripción, Criterios)"""
        context = self._extract_section(text, 'context')
        description = self._extract_section(text, 'description')
        criteria = self._extract_traditional_criteria(text)
        
        return ParsedStory(
            title=title,
            structure_type=structure_type,
            context=context,
            description=description,
            acceptance_criteria=criteria,
            user_flows=[],
            states=[],
            ui_elements=[],
            technical_requirements=[],
            raw_text=text
        )
    
    def _parse_narrative(self, text: str, title: str, structure_type: StoryStructureType) -> ParsedStory:
        """Parsea estructura narrativa/EMS (flujos, estados, referencias)"""
        # Extraer flujos de usuario
        user_flows = self._extract_user_flows(text)
        
        # Extraer estados del sistema
        states = self._extract_states(text)
        
        # Extraer elementos de UI
        ui_elements = self._extract_ui_elements(text)
        
        # Extraer requisitos técnicos
        technical_requirements = self._extract_technical_requirements(text)
        
        # Generar criterios de aceptación desde la narrativa
        criteria = self._generate_criteria_from_narrative(
            text, user_flows, states, ui_elements
        )
        
        # Intentar extraer contexto y descripción si existen
        context = self._extract_section(text, 'context')
        description = self._extract_section(text, 'description')
        
        # Si no hay contexto/descripción explícitos, usar el inicio del texto
        if not context and not description:
            # Usar primeras líneas como descripción
            lines = text.split('\n')
            description = ' '.join([l.strip() for l in lines[:3] if l.strip()])
        
        return ParsedStory(
            title=title,
            structure_type=structure_type,
            context=context,
            description=description or text[:500],
            acceptance_criteria=criteria,
            user_flows=user_flows,
            states=states,
            ui_elements=ui_elements,
            technical_requirements=technical_requirements,
            raw_text=text
        )
    
    def _parse_mixed(self, text: str, title: str, structure_type: StoryStructureType) -> ParsedStory:
        """Parsea estructura mixta (combina ambos formatos)"""
        # Intentar extraer partes tradicionales
        context = self._extract_section(text, 'context')
        description = self._extract_section(text, 'description')
        traditional_criteria = self._extract_traditional_criteria(text)
        
        # Extraer partes narrativas
        user_flows = self._extract_user_flows(text)
        states = self._extract_states(text)
        ui_elements = self._extract_ui_elements(text)
        technical_requirements = self._extract_technical_requirements(text)
        
        # Generar criterios adicionales desde narrativa
        narrative_criteria = self._generate_criteria_from_narrative(
            text, user_flows, states, ui_elements
        )
        
        # Combinar criterios (evitar duplicados)
        all_criteria = traditional_criteria + [
            c for c in narrative_criteria 
            if not any(tc.lower() in c.lower() or c.lower() in tc.lower() 
                      for tc in traditional_criteria)
        ]
        
        return ParsedStory(
            title=title,
            structure_type=structure_type,
            context=context,
            description=description or text[:500],
            acceptance_criteria=all_criteria,
            user_flows=user_flows,
            states=states,
            ui_elements=ui_elements,
            technical_requirements=technical_requirements,
            raw_text=text
        )
    
    def _extract_section(self, text: str, section_key: str) -> str:
        """Extrae una sección específica del texto"""
        pattern = self.traditional_patterns.get(section_key, '')
        if not pattern:
            return ""
        
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            content = match.group(1).strip()
            # Limpiar espacios múltiples
            return ' '.join(content.split())
        
        return ""
    
    def _extract_traditional_criteria(self, text: str) -> List[str]:
        """Extrae criterios de aceptación de estructura tradicional"""
        criteria = []
        
        # Buscar sección de criterios
        criteria_match = re.search(
            self.traditional_patterns['criteria_section'],
            text,
            re.IGNORECASE | re.DOTALL
        )
        
        if not criteria_match:
            return criteria
        
        criteria_text = criteria_match.group(1).strip()
        
        # Buscar criterios con emojis ✅
        emoji_criteria = re.findall(r'[✅✓☑]\s*([^✅✓☑\n]+)', criteria_text)
        if emoji_criteria:
            for crit in emoji_criteria:
                cleaned = crit.strip()
                if len(cleaned) > 15:
                    criteria.append(cleaned)
            return criteria
        
        # Buscar bullets (-, •, *)
        bullet_criteria = re.findall(
            r'(?:^|\n)\s*[-•*]\s*(.+?)(?=\n\s*[-•*]|\n\n|$)',
            criteria_text,
            re.MULTILINE | re.DOTALL
        )
        if bullet_criteria:
            for crit in bullet_criteria:
                cleaned = ' '.join(crit.split()).strip()
                if len(cleaned) > 15:
                    criteria.append(cleaned)
            return criteria
        
        # Buscar frases que empiecen con patrones típicos
        sentences = re.split(r'\.\s+(?=[A-ZÁÉÍÓÚÜÑ])', criteria_text)
        for sentence in sentences:
            sentence = sentence.strip().rstrip('.')
            if any(pattern in sentence.lower() for pattern in [
                'cuando ', 'para ', 'si ', 'el campo ', 'debe ',
                'permite ', 'valida ', 'guarda ', 'toma ', 'sigue'
            ]):
                if len(sentence) > 20:
                    criteria.append(sentence)
        
        return criteria
    
    def _extract_user_flows(self, text: str) -> List[str]:
        """Extrae flujos de usuario de texto narrativo"""
        flows = []
        
        # Buscar frases que describan acciones del usuario
        flow_patterns = [
            r'(?:Al\s+)?(?:darle|dar|hacer|presionar|click|seleccionar|ingresar|subir|descargar|arrastrar|drag)[^\.]+\.',
            r'(?:El\s+)?(?:usuario|user)[^\.]+\.',
            r'(?:Si|Cuando|Al)\s+[^\.]+(?:debe|puede|debería)[^\.]+\.',
        ]
        
        for pattern in flow_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            flows.extend([m.strip() for m in matches if len(m.strip()) > 20])
        
        return list(set(flows))  # Eliminar duplicados
    
    def _extract_states(self, text: str) -> List[str]:
        """Extrae estados del sistema mencionados"""
        states = []
        
        # Buscar menciones de estados
        state_patterns = [
            r'(?:estado|state)[:\s]+([^\.\n]+)',
            r'(?:pantalla|screen|vista|view)[:\s]+([^\.\n]+)',
            r'(?:si\s+no\s+tengo|si\s+no\s+hay|cuando\s+no)[^\.]+\.',
        ]
        
        for pattern in state_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            states.extend([m.strip() for m in matches if len(m.strip()) > 5])
        
        return list(set(states))
    
    def _extract_ui_elements(self, text: str) -> List[str]:
        """Extrae elementos de UI mencionados"""
        ui_elements = []
        
        # Buscar menciones de elementos UI
        ui_patterns = [
            r'(?:botón|button)[:\s]*([^\.\n]+)',
            r'(?:campo|field)[:\s]*([^\.\n]+)',
            r'(?:tabla|table)[:\s]*([^\.\n]+)',
            r'(?:modal|popup|pop-up)[:\s]*([^\.\n]+)',
            r'(?:calendario|calendar)[:\s]*([^\.\n]+)',
            r'(?:loader|spinner)[:\s]*([^\.\n]+)',
        ]
        
        for pattern in ui_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            ui_elements.extend([m.strip() for m in matches if len(m.strip()) > 3])
        
        return list(set(ui_elements))
    
    def _extract_technical_requirements(self, text: str) -> List[str]:
        """Extrae requisitos técnicos mencionados"""
        requirements = []
        
        # Buscar menciones técnicas
        tech_patterns = [
            r'(?:back|backend|api|endpoint|servicio|service)[^\.]+\.',
            r'(?:formato|format|archivo|file|documento)[:\s]+([^\.\n]+)',
            r'(?:debe\s+enviar|debe\s+recibir|debe\s+responder)[^\.]+\.',
        ]
        
        for pattern in tech_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            requirements.extend([m.strip() if isinstance(m, str) else ' '.join(m) 
                                for m in matches if len(str(m).strip()) > 10])
        
        return list(set(requirements))
    
    def _generate_criteria_from_narrative(self, text: str, user_flows: List[str], 
                                         states: List[str], ui_elements: List[str]) -> List[str]:
        """Genera criterios de aceptación desde texto narrativo"""
        criteria = []
        
        # Criterios desde flujos de usuario
        for flow in user_flows:
            if len(flow) > 20:
                criteria.append(f"El sistema debe permitir: {flow}")
        
        # Criterios desde estados
        for state in states:
            if 'onboarding' in state.lower() or 'configuración' in state.lower():
                criteria.append(f"El sistema debe mostrar el estado: {state}")
        
        # Criterios desde elementos UI
        for ui in ui_elements:
            if 'botón' in ui.lower() or 'button' in ui.lower():
                criteria.append(f"El botón '{ui}' debe estar presente y funcional")
            elif 'campo' in ui.lower() or 'field' in ui.lower():
                criteria.append(f"El campo '{ui}' debe permitir entrada de datos")
            elif 'modal' in ui.lower() or 'popup' in ui.lower():
                criteria.append(f"El modal '{ui}' debe abrirse y cerrarse correctamente")
        
        # Buscar acciones específicas mencionadas
        action_patterns = [
            r'(?:debe|debería)\s+([^\.]+)\.',
            r'(?:no\s+debe|no\s+debería)\s+([^\.]+)\.',
            r'(?:se\s+debe|se\s+debería)\s+([^\.]+)\.',
        ]
        
        for pattern in action_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    match = ' '.join(match)
                if len(match.strip()) > 20:
                    criteria.append(match.strip())
        
        # Eliminar duplicados y criterios muy cortos
        unique_criteria = []
        seen = set()
        for crit in criteria:
            crit_lower = crit.lower()
            if crit_lower not in seen and len(crit) > 20:
                unique_criteria.append(crit)
                seen.add(crit_lower)
        
        return unique_criteria


def parse_user_story_adaptive(text: str) -> ParsedStory:
    """
    Función de utilidad para parsear una HU con detección automática
    
    Args:
        text: Texto completo de la historia de usuario
        
    Returns:
        ParsedStory con toda la información extraída
    """
    parser = AdaptiveParser()
    return parser.parse(text)


# Test
if __name__ == "__main__":
    # Test con estructura tradicional
    traditional_hu = """
    Contexto
    Cuando una frontera llega con tipología embebida...
    
    Descripción
    Como sistema facturación, quiero que...
    
    Criterios de aceptación
    ✅ Cuando la frontera es embebida, contract relationships guarda el NT padre.
    ✅ Para fronteras embebidas, contract rates.NT toma únicamente el NT padre.
    """
    
    # Test con estructura narrativa/EMS
    narrative_hu = """
    Dentro de "Análisis", debemos de crear una nueva sección que se llame "Intensidad energética" al final.
    
    Si no tengo data subida, paso por el "onboarding":
    https://www.figma.com/design/3OBU940TcOpSqiv34PFZBp/Playground-Dani?node-id=4622-45095
    
    Al darle "Empezar": https://www.figma.com/design/3OBU940TcOpSqiv34PFZBp/Playground-Dani?node-id=4622-45144
    
    Aqui podemos animar que el botón baje, el contenido de antiguo hace fade out y el nuevo fade in.
    
    Al apretar "Iniciar configuración" ya arranco el proceso para subir información de mi negocio.
    
    Configuración:
    Debo de seleccionar:
    - Sedes que deseo actualizar
    - Métricas que deseo actualizar de mi negocio
    
    Back te va a enviar un listado de métricas (son como 30).
    De esas 30, vamos a mostrar 4 únicamente de primero que son las mas populares.
    
    Si le doy "Agregar Métrica":
    Pop-up: https://www.figma.com/design/3OBU940TcOpSqiv34PFZBp/Playground-Dani?node-id=4631-47497
    
    Al darle click, me salen todas las metricas listadas hacia abajo con un buscador.
    Mientras escribo se filtan abajo.
    
    Al seleccionar una métrica, se me agrega al la pantalla principal abajo.
    
    Al final de las métricas, me sale "+ Crear nueva métrica". 
    Esto me abre un typeform en una nueva ventana.
    
    Agrupación (Hora, Dia, Mes)
    Dependiendo de la agrupación seleccionada, las opciones del periodo cambian.
    
    Periodo
    Si selecciono "OTRO", me sale el calendario.
    
    Una vez ya se tenga toda la información, sale un "Resumen" abajo.
    
    Crear Planilla:
    Al darle "Crear Planilla", coloquemos un loader en el botón y el contenido de arriba se coloca con opacidad.
    
    Aqui le envias toda la data a back y esperas su respuesta.
    En la respuesta de back, el te debe de enviar un documento en formato XLS.
    
    "Descargar Planilla" te descarga la planilla de excel que te respondio back.
    
    El usuario puede Drag la planilla al rectangulo o puede darle click a todo el rectangulo.
    
    Empezar análisis:
    El botón de "Empezar analisis" se cambia por "Subiendo información…" con un loader.
    
    Back te debe de enviar SUCCESS o FAIL.
    Si es SUCCESS: muestra mensaje de éxito.
    Si es FAIL: Back te debe de enviar listado de errores para pintar en el pop-up.
    """
    
    parser = AdaptiveParser()
    
    print("="*80)
    print("TEST: ESTRUCTURA TRADICIONAL")
    print("="*80)
    result1 = parser.parse(traditional_hu)
    print(f"Tipo detectado: {result1.structure_type.value}")
    print(f"Título: {result1.title}")
    print(f"Criterios: {len(result1.acceptance_criteria)}")
    for i, crit in enumerate(result1.acceptance_criteria, 1):
        print(f"  {i}. {crit}")
    
    print("\n" + "="*80)
    print("TEST: ESTRUCTURA NARRATIVA/EMS")
    print("="*80)
    result2 = parser.parse(narrative_hu)
    print(f"Tipo detectado: {result2.structure_type.value}")
    print(f"Título: {result2.title}")
    print(f"Criterios: {len(result2.acceptance_criteria)}")
    for i, crit in enumerate(result2.acceptance_criteria, 1):
        print(f"  {i}. {crit}")
    print(f"\nFlujos de usuario: {len(result2.user_flows)}")
    for flow in result2.user_flows[:5]:
        print(f"  - {flow}")
    print(f"\nEstados: {len(result2.states)}")
    for state in result2.states[:5]:
        print(f"  - {state}")
    print(f"\nElementos UI: {len(result2.ui_elements)}")
    for ui in result2.ui_elements[:5]:
        print(f"  - {ui}")

