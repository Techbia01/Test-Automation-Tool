#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parser Simple y Efectivo para Criterios de Aceptación
Extrae criterios completos sin cortar, respetando el formato original
"""

import re
from typing import List, Tuple
from dataclasses import dataclass

@dataclass
class ParsedUserStory:
    """Historia de usuario parseada con criterios completos"""
    title: str
    context: str
    description: str
    requirements: List[str]
    acceptance_criteria: List[str]
    
    def __str__(self):
        return f"HU: {self.title}\nCriterios: {len(self.acceptance_criteria)}"


class SimpleCriteriaParser:
    """Parser que extrae criterios de aceptación completos sin cortar"""
    
    def __init__(self):
        # Patrones para identificar secciones
        self.section_patterns = {
            'context': r'(?:contexto|context)[:\s]+(.*?)(?=\n(?:descripci[óo]n|description|requerimiento|criterio|$))',
            'description': r'(?:descripci[óo]n|description)[:\s]+(.*?)(?=\n(?:requerimiento|criterio|$))',
            'requirements': r'(?:requerimiento|requirement|requisito)[s]?[:\s]+(.*?)(?=\n(?:criterio|$))',
            'criteria': r'(?:criterio|criteria|acceptance\s*criteria)[s]?\s*(?:de\s*aceptaci[óo]n)?[:\s]+(.*?)$'
        }
    
    def parse(self, user_story_text: str) -> ParsedUserStory:
        """
        Parsea una historia de usuario completa
        
        Args:
            user_story_text: Texto completo de la HU
            
        Returns:
            ParsedUserStory con todos los criterios extraídos
        """
        # Limpiar el texto
        text = self._clean_text(user_story_text)
        
        # Extraer título (primera línea significativa)
        title = self._extract_title(text)
        
        # Extraer contexto
        context = self._extract_section(text, 'context')
        
        # Extraer descripción
        description = self._extract_section(text, 'description')
        
        # Extraer requerimientos
        requirements = self._extract_requirements(text)
        
        # Extraer criterios de aceptación (✅ bullets)
        criteria = self._extract_acceptance_criteria(text)
        
        return ParsedUserStory(
            title=title,
            context=context,
            description=description,
            requirements=requirements,
            acceptance_criteria=criteria
        )
    
    def _clean_text(self, text: str) -> str:
        """Limpia el texto preservando la estructura"""
        # Normalizar saltos de línea
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        
        # Eliminar múltiples espacios pero preservar líneas
        lines = []
        for line in text.split('\n'):
            line = ' '.join(line.split())  # Normalizar espacios dentro de la línea
            if line:  # Solo agregar líneas no vacías
                lines.append(line)
        
        return '\n'.join(lines)
    
    def _extract_title(self, text: str) -> str:
        """Extrae el título de la HU"""
        lines = text.split('\n')
        
        # Buscar la primera línea significativa
        for line in lines:
            line = line.strip()
            if len(line) > 10 and not line.lower().startswith(('contexto', 'descripción', 'requerimiento', 'criterio')):
                return line
        
        return "Historia de Usuario"
    
    def _extract_section(self, text: str, section_key: str) -> str:
        """Extrae una sección completa del texto"""
        pattern = self.section_patterns.get(section_key, '')
        if not pattern:
            return ""
        
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            content = match.group(1).strip()
            # Limpiar y devolver
            return ' '.join(content.split())
        
        return ""
    
    def _extract_requirements(self, text: str) -> List[str]:
        """Extrae la sección de requerimientos completa"""
        requirements = []
        
        # Buscar sección de requerimientos
        req_match = re.search(
            r'(?:requerimiento|requirement|requisito)[s]?[:\s]+(.*?)(?=\n\s*(?:criterio|criteria|$))',
            text,
            re.IGNORECASE | re.DOTALL
        )
        
        if req_match:
            req_section = req_match.group(1)
            
            # Buscar subsecciones (Al sincronizar..., Al poblar..., etc.)
            subsections = re.findall(
                r'(?:^|\n)([A-Z][^:\n]+):([^\n]+(?:\n(?![A-Z][^:\n]+:)[^\n]+)*)',
                req_section,
                re.MULTILINE
            )
            
            for title, content in subsections:
                # Limpiar y combinar
                req_text = f"{title.strip()}: {' '.join(content.split())}"
                requirements.append(req_text)
        
        return requirements
    
    def _extract_acceptance_criteria(self, text: str) -> List[str]:
        """
        Extrae criterios de aceptación de forma ULTRA ROBUSTA
        Funciona CON o SIN emojis, CON o SIN saltos de línea
        """
        criteria = []
        
        # Paso 1: Buscar la sección "Criterios de aceptación"
        criteria_match = re.search(
            r'criterios?\s+de\s+aceptaci[óo]n\s*[:\s]+(.*?)(?:\n\n|$)',
            text,
            re.IGNORECASE | re.DOTALL
        )
        
        if not criteria_match:
            return self._extract_criteria_fallback(text)
        
        criteria_text = criteria_match.group(1).strip()
        
        # Paso 2: Intentar encontrar criterios con emojis ✅
        emoji_criteria = re.findall(
            r'[✅✓]\s*([^✅✓\n]+)',
            criteria_text
        )
        
        if emoji_criteria:
            for crit in emoji_criteria:
                cleaned = crit.strip()
                if len(cleaned) > 15:
                    criteria.append(cleaned)
            return criteria
        
        # Paso 3: Sin emojis - buscar frases que empiecen con patrones típicos de criterios
        # Dividir por frases completas (punto seguido de mayúscula)
        sentences = re.split(r'\.\s+(?=[A-ZÁÉÍÓÚÜÑ])', criteria_text)
        
        for sentence in sentences:
            sentence = sentence.strip().rstrip('.')
            
            # Buscar patrones típicos de criterios de aceptación
            if any(pattern in sentence.lower() for pattern in [
                'cuando ', 'para ', 'si ', 'el campo ', 'debe ', 
                'permite ', 'valida ', 'guarda ', 'toma ', 'sigue'
            ]):
                if len(sentence) > 20:
                    criteria.append(sentence)
        
        # Si aún no tenemos criterios, intentar fallback final
        if not criteria:
            criteria = self._extract_criteria_fallback(text)
        
        return criteria
    
    def _extract_criteria_fallback(self, text: str) -> List[str]:
        """
        Fallback: extrae criterios usando bullets normales (-, •, *)
        """
        criteria = []
        
        # Buscar sección de criterios
        criteria_match = re.search(
            r'(?:criterio|criteria)[s]?\s*(?:de\s*aceptaci[óo]n)?[:\s]+(.*?)$',
            text,
            re.IGNORECASE | re.DOTALL
        )
        
        if criteria_match:
            criteria_section = criteria_match.group(1)
            
            # Buscar items con bullets
            bullet_items = re.findall(
                r'(?:^|\n)\s*[•\-\*]\s*(.+?)(?=\n\s*[•\-\*]|\n\n|$)',
                criteria_section,
                re.DOTALL
            )
            
            for item in bullet_items:
                criterion = ' '.join(item.split())
                criterion = criterion.strip('.,;')
                
                if len(criterion) > 10:
                    criteria.append(criterion)
        
        return criteria


def parse_user_story(text: str) -> ParsedUserStory:
    """
    Función de utilidad para parsear una HU
    
    Args:
        text: Texto completo de la historia de usuario
        
    Returns:
        ParsedUserStory con criterios completos extraídos
    """
    parser = SimpleCriteriaParser()
    return parser.parse(text)


# Test rápido
if __name__ == "__main__":
    test_hu = """
    BACK I Ajustar el insumo del campo de NT en CR cuando una frontera es embebida
    
    Contexto
    Cuando una frontera llega con tipología embebida, hoy el sistema guarda en contract rates el NT del hijo y luego lo reemplaza por el del padre.
    
    Descripción
    Como sistema facturación,
    quiero que cuando llegue una frontera con tipología embebida, se guarde el NT padre en contract relationships y sea ese el que se use para poblar contract rates,
    para asegurar consistencia y evitar almacenar NT del hijo en Bills.
    
    Criterios de aceptación
    ✅ Cuando la frontera es embebida, contract relationships guarda el NT padre.
    ✅ Para fronteras embebidas, contract rates.NT toma únicamente el NT padre desde contract relationships.
    ✅ Para fronteras no embebidas, el flujo sigue igual (toma el NT directo).
    ✅ El campo embedded_tension_child ya no existe ni se guarda NT hijo en Bills.
    """
    
    result = parse_user_story(test_hu)
    print(f"Título: {result.title}")
    print(f"\nCriterios encontrados: {len(result.acceptance_criteria)}")
    for i, crit in enumerate(result.acceptance_criteria, 1):
        print(f"  {i}. {crit}")

