#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo core de automatización de casos de prueba.
Proporciona parser, generador, validador y exportador para la app web.
"""

import csv
import os
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Any


class TestType(Enum):
    """Tipo de caso de prueba."""
    FUNCTIONAL = "Funcional"
    NEGATIVE = "Negativo"
    INTEGRATION = "Integración"
    REGRESSION = "Regresión"
    UI = "UI"


class Priority(Enum):
    """Prioridad del caso de prueba."""
    HIGH = "Alta"
    MEDIUM = "Media"
    LOW = "Baja"


@dataclass
class UserStory:
    """Historia de usuario."""
    title: str
    description: str
    acceptance_criteria: List[str]


@dataclass
class TestCase:
    """Caso de prueba para la app web (formato legacy)."""
    id: str
    title: str
    description: str
    preconditions: List[str]
    steps: List[str]
    expected_result: str
    test_type: TestType
    priority: Priority
    user_story: str = ""
    tags: List[str] = field(default_factory=lambda: ["@qa", "@automated"])


class UserStoryParser:
    """Parser de historias de usuario (compatibilidad con generadores)."""
    def parse(self, text: str) -> UserStory:
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        title = lines[0] if lines else "Historia de Usuario"
        criteria = [l.lstrip("-•* ") for l in lines[1:] if l]
        return UserStory(title=title, description="", acceptance_criteria=criteria)


class TestCaseGenerator:
    """Generador de casos de prueba (compatibilidad; la app usa ProfessionalQAGenerator)."""
    def generate(self, user_story: UserStory) -> List[TestCase]:
        return []


class QAValidator:
    """Validador de calidad de la suite de casos de prueba."""
    def validate_test_suite(self, test_cases: List[TestCase]) -> Dict[str, Any]:
        if not test_cases:
            return {
                "average_score": 0,
                "overall_quality": "Sin casos de prueba",
                "recommendations": ["Generar casos de prueba"],
            }
        n = len(test_cases)
        score = min(100, 60 + n * 2)
        return {
            "average_score": score,
            "overall_quality": "Buena" if score >= 70 else "Aceptable",
            "recommendations": [],
        }


class TestCaseExporter:
    """Exportador de casos de prueba a CSV."""
    def export_to_csv(self, test_cases: List[TestCase], filepath: str) -> None:
        os.makedirs(os.path.dirname(os.path.abspath(filepath)) or ".", exist_ok=True)
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "ID", "Título", "Descripción", "Precondiciones", "Pasos",
                "Resultado Esperado", "Tipo", "Prioridad", "Historia de Usuario", "Tags"
            ])
            for tc in test_cases:
                preconditions = "\n".join(tc.preconditions) if tc.preconditions else ""
                steps = "\n".join(tc.steps) if isinstance(tc.steps, list) else str(tc.steps)
                writer.writerow([
                    tc.id,
                    tc.title,
                    tc.description or "",
                    preconditions,
                    steps,
                    tc.expected_result or "",
                    tc.test_type.value if hasattr(tc.test_type, "value") else str(tc.test_type),
                    tc.priority.value if hasattr(tc.priority, "value") else str(tc.priority),
                    tc.user_story or "",
                    ", ".join(tc.tags) if tc.tags else "",
                ])
