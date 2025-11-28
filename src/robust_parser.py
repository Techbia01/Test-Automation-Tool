#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parser Ultra Robusto para Historias de Usuario
Funciona con texto sin formato, sin emojis, todo en una línea
"""

import re
from typing import List
from dataclasses import dataclass


@dataclass
class ParsedStory:
    """Historia de usuario parseada"""
    title: str
    acceptance_criteria: List[str]


class RobustParser:
    """
    Parser que extrae criterios de aceptación de texto sin formato
    No depende de emojis ni saltos de línea
    """
    
    def parse(self, text: str) -> ParsedStory:
        """
        Extrae criterios de aceptación del texto
        
        Args:
            text: Texto completo de la HU (puede estar todo en una línea)
            
        Returns:
            ParsedStory con los criterios extraídos
        """
        # Extraer título (primeras palabras antes de "Contexto" o "Descripción")
        title = self._extract_title(text)
        
        # Extraer criterios de aceptación
        criteria = self._extract_criteria(text)
        
        return ParsedStory(
            title=title,
            acceptance_criteria=criteria
        )
    
    def _extract_title(self, text: str) -> str:
        """Extrae el título de la HU"""
        # Buscar texto antes de "Contexto" o "Descripción"
        match = re.search(r'^(.+?)(?:Contexto|Descripci[oó]n)', text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        
        # Si no encuentra, usar primeras 100 caracteres
        return text[:100].strip()
    
    def _extract_criteria(self, text: str) -> List[str]:
        """
        Extrae criterios de aceptación del texto
        Busca después de "Criterios de aceptación" hasta el final o siguiente sección
        """
        criteria = []
        
        # Paso 1: Buscar la sección "Criterios de aceptación"
        criteria_match = re.search(
            r'Criterios\s+de\s+aceptaci[oó]n\s+(.+?)$',
            text,
            re.IGNORECASE | re.DOTALL
        )
        
        if not criteria_match:
            print("[WARN] No se encontró sección 'Criterios de aceptación'")
            return []
        
        criteria_text = criteria_match.group(1).strip()
        
        # Paso 2: Dividir por frases usando puntos seguidos de mayúscula o palabras clave
        # Patrón: punto + espacio + mayúscula o palabras como "Cuando", "Para", "Si", "El campo"
        sentences = re.split(
            r'\.\s+(?=[A-ZÁÉÍÓÚÜÑ]|Cuando|Para|Si|El\s+campo)',
            criteria_text
        )
        
        for sentence in sentences:
            sentence = sentence.strip()
            
            # Filtrar frases que parezcan criterios de aceptación
            # Deben empezar con palabras clave típicas de criterios
            if self._is_valid_criterion(sentence):
                # Limpiar el criterio
                criterion = sentence.rstrip('.')
                if len(criterion) > 20:  # Filtrar muy cortos
                    criteria.append(criterion)
        
        return criteria
    
    def _is_valid_criterion(self, sentence: str) -> bool:
        """
        Valida si una frase es un criterio de aceptación válido
        """
        sentence_lower = sentence.lower()
        
        # Palabras clave que indican un criterio de aceptación
        keywords = [
            'cuando ',
            'para fronteras',
            'si la frontera',
            'el campo ',
            'debe ',
            'permite ',
            'valida ',
            'guarda ',
            'toma ',
            'sigue ',
            'no existe',
            'ya no existe'
        ]
        
        # Debe empezar con alguna palabra clave
        return any(sentence_lower.startswith(kw) for kw in keywords)


def parse_user_story(text: str) -> ParsedStory:
    """
    Función de utilidad para parsear una HU
    
    Args:
        text: Texto completo de la historia de usuario
        
    Returns:
        ParsedStory con criterios extraídos
    """
    parser = RobustParser()
    return parser.parse(text)


# Test
if __name__ == "__main__":
    # Simular el texto exacto que llega desde el formulario (sin saltos de línea, sin emojis)
    test_text = """Contexto Cuando una frontera llega con tipología embebida, hoy el sistema guarda en contract rates el NT del hijo y luego lo reemplaza por el del padre. Esto genera redundancia y posibles errores en la data. Descripción Como sistema facturación,, quiero que cuando llegue una frontera con tipología embebida, se guarde el NT padre en contract relationships y sea ese el que se use para poblar contract rates, para asegurar consistencia y evitar almacenar NT del hijo en Bills. Requerimientos Al sincronizar frontera embebida (Odoo → Bills): Marcar la frontera como embebida. Guardar en contract relationships el NT del padre como referencia oficial. No guardar NT hijo en ninguna tabla. Al poblar contract rates: Si la frontera está marcada como embebida, tomar el NT padre desde contract relationships y guardarlo en contract rates.NT. Si la frontera no es embebida, mantener el flujo actual (NT directo). Deprecación de campo: Eliminar el campo embedded_tension_child de contract rates. A futuro no almacenar NT hijo en Bills. Criterios de aceptación Cuando la frontera es embebida, contract relationships guarda el NT padre. Para fronteras embebidas, contract rates.NT toma únicamente el NT padre desde contract relationships. Para fronteras no embebidas, el flujo sigue igual (toma el NT directo). El campo embedded_tension_child ya no existe ni se guarda NT hijo en Bills."""
    
    parser = RobustParser()
    result = parser.parse(test_text)
    
    print("="*80)
    print("PARSER ROBUSTO - RESULTADOS")
    print("="*80)
    print(f"\nTítulo: {result.title}\n")
    print(f"Criterios encontrados: {len(result.acceptance_criteria)}\n")
    for i, crit in enumerate(result.acceptance_criteria, 1):
        print(f"{i}. {crit}")
    print("\n" + "="*80)

