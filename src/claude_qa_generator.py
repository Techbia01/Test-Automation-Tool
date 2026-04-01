#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de casos de prueba QA basado en Claude AI (claude-opus-4-6).
Produce instancias de TestCase compatibles con ProfessionalQAGenerator.
"""

import json
import os
from typing import List, Optional

try:
    import anthropic
except ImportError:
    anthropic = None  # type: ignore

try:
    from .professional_qa_generator import (
        TestCase,
        TestType,
        TestPriority,
        ExecutionSuitability,
    )
except ImportError:
    from professional_qa_generator import (  # type: ignore
        TestCase,
        TestType,
        TestPriority,
        ExecutionSuitability,
    )

# ---------------------------------------------------------------------------
# Prompt del sistema
# ---------------------------------------------------------------------------

_SYSTEM_PROMPT = """\
Eres un experto QA profesional con amplia experiencia generando casos de prueba \
precisos, trazables y ejecutables a partir de historias de usuario (HU).

## Reglas estrictas
- Extrae criterios de aceptación EXPLÍCITOS de la HU (Gherkin, bullets, numerados o prosa).
- NO generes casos de rendimiento, disponibilidad, SLA, carga ni NFR genéricos.
- NO repitas casos por reformulación; cada caso debe validar un comportamiento distinto.
- Si la HU usa Gherkin (Dado que/Cuando/Entonces o Given/When/Then), los pasos \
del caso deben reproducir ese escenario con exactitud.
- Los pasos van en formato Gherkin: líneas que empiezan con \
"Dado que", "Cuando", "Entonces" o "Y".
- El resultado esperado se extrae de los bloques "Entonces" / postcondición de la HU.
- Usa el contexto del proyecto solo para enriquecer precondiciones o detalles técnicos, \
no para inventar criterios ausentes en la HU.
- Prioridad: Alta = flujos principales / críticos; Media = flujos alternativos; \
Baja = edge cases menores.
- Tipos válidos: Funcional, Negativo, Integración, Regresión, UI.

## Formato de salida
Responde EXCLUSIVAMENTE con un array JSON válido (sin texto adicional, sin markdown fences):
[
  {
    "id": "TC-001",
    "title": "Validar que <resultado observable en tercera persona>",
    "criterion": "<criterio de aceptación textual extraído de la HU>",
    "test_type": "Funcional",
    "priority": "Alta",
    "preconditions": ["Precondición 1", "Precondición 2"],
    "steps": [
      "Dado que <contexto inicial>",
      "Cuando <acción del actor>",
      "Entonces <resultado observable>"
    ],
    "expected_result": "<descripción clara de lo que debe ocurrir>"
  }
]
"""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _build_user_message(
    user_story_text: str,
    project_name: str,
    project_context: Optional[str],
) -> str:
    parts = [f"## Historia de usuario: {project_name}\n\n{user_story_text}"]
    if project_context:
        # Limitar contexto para no exceder ventana de contexto
        ctx = project_context[:8000]
        parts.append(f"## Contexto del proyecto (código / README)\n\n{ctx}")
    parts.append(
        "Genera los casos de prueba en JSON. "
        "Responde SOLO con el array JSON, sin ningún texto adicional."
    )
    return "\n\n---\n\n".join(parts)


_TYPE_MAP = {
    "Funcional": TestType.FUNCIONAL,
    "Negativo": TestType.NEGATIVO,
    "Integración": TestType.INTEGRACION,
    "Integracion": TestType.INTEGRACION,
    "Regresión": TestType.REGRESION,
    "Regresion": TestType.REGRESION,
    "UI": TestType.UI,
}

_PRIORITY_MAP = {
    "Alta": TestPriority.ALTA,
    "Media": TestPriority.MEDIA,
    "Baja": TestPriority.BAJA,
}


# ---------------------------------------------------------------------------
# Clase principal
# ---------------------------------------------------------------------------

class ClaudeQAGenerator:
    """
    Generador de casos de prueba usando Claude claude-opus-4-6 con pensamiento adaptativo.
    Misma interfaz que ProfessionalQAGenerator para que sea intercambiable.
    """

    def __init__(self, api_key: Optional[str] = None):
        if anthropic is None:
            raise ImportError(
                "El paquete 'anthropic' no está instalado. "
                "Ejecuta: pip install anthropic"
            )
        key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not key:
            raise ValueError(
                "ANTHROPIC_API_KEY no configurada. "
                "Defínela como variable de entorno o pásala al constructor."
            )
        self._client = anthropic.Anthropic(api_key=key)

    # ------------------------------------------------------------------
    # Interfaz pública (misma firma que ProfessionalQAGenerator)
    # ------------------------------------------------------------------

    def generate_test_cases(
        self,
        user_story_text: str,
        project_name: str = "",
        project_context: Optional[str] = None,
        verbose_log: bool = False,
    ) -> List[TestCase]:
        """
        Genera casos de prueba a partir de una historia de usuario.
        Retorna List[TestCase] — compatible con el motor de reglas.
        """
        if not user_story_text or not user_story_text.strip():
            return []

        if verbose_log:
            print("[Claude] Enviando HU al modelo claude-opus-4-6...")

        user_message = _build_user_message(
            user_story_text, project_name, project_context
        )

        raw_json = self._call_api(user_message, verbose_log)
        return self._parse_response(raw_json, verbose_log)

    # ------------------------------------------------------------------
    # Internos
    # ------------------------------------------------------------------

    def _call_api(self, user_message: str, verbose_log: bool) -> str:
        """Llama a la API con streaming y retorna el texto JSON de la respuesta."""
        with self._client.messages.stream(
            model="claude-sonnet-4-6",
            max_tokens=8000,
            thinking={"type": "adaptive"},
            system=_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_message}],
        ) as stream:
            final = stream.get_final_message()

        raw = ""
        for block in final.content:
            if block.type == "text":
                raw = block.text.strip()
                break

        if verbose_log:
            print(f"[Claude] Respuesta recibida ({len(raw)} caracteres)")

        return raw

    def _parse_response(self, raw: str, verbose_log: bool) -> List[TestCase]:
        """Parsea el JSON devuelto por Claude y construye instancias TestCase."""
        text = raw

        # Remover posibles code fences que Claude agregue a pesar del prompt
        if text.startswith("```"):
            lines = text.splitlines()
            text = "\n".join(
                line for line in lines if not line.strip().startswith("```")
            ).strip()

        try:
            data = json.loads(text)
        except json.JSONDecodeError as e:
            print(f"[ERROR][Claude] No se pudo parsear JSON: {e}")
            if verbose_log:
                print(f"[Claude] Respuesta cruda (primeros 500 chars):\n{raw[:500]}")
            return []

        if not isinstance(data, list):
            print("[ERROR][Claude] La respuesta no es un array JSON")
            return []

        cases: List[TestCase] = []
        seen_titles: set = set()

        for i, item in enumerate(data, 1):
            if not isinstance(item, dict):
                continue

            title = (item.get("title") or "").strip()
            normalized = title.lower()
            if not title or normalized in seen_titles:
                if verbose_log and normalized in seen_titles:
                    print(f"[Claude][SKIP] Título duplicado: {title[:60]}")
                continue
            seen_titles.add(normalized)

            tc = TestCase(
                id=item.get("id") or f"TC-{i:03d}",
                title=title,
                criterion=item.get("criterion") or title,
                test_type=_TYPE_MAP.get(
                    item.get("test_type", ""), TestType.FUNCIONAL
                ),
                priority=_PRIORITY_MAP.get(
                    item.get("priority", ""), TestPriority.ALTA
                ),
                preconditions=item.get("preconditions") or [],
                steps=item.get("steps") or [],
                expected_result=item.get("expected_result") or "",
            )
            cases.append(tc)

        if verbose_log:
            print(f"[Claude] {len(cases)} caso(s) parseados correctamente")

        return cases
