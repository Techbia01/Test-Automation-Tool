# -*- coding: utf-8 -*-
"""
Plantillas de casos de prueba para la app web.
"""

from typing import List, Dict


class TemplateManager:
    """Gestor de plantillas de casos de prueba."""

    TEMPLATES = {
        "web": {
            "name": "Web / Funcional",
            "description": "Casos de prueba para aplicaciones web y flujos funcionales.",
        },
        "api": {
            "name": "API / Integración",
            "description": "Casos de prueba para APIs REST y servicios.",
        },
        "gherkin": {
            "name": "Gherkin / BDD",
            "description": "Casos en formato Given/When/Then para BDD.",
        },
    }

    def get_available_templates(self) -> List[str]:
        """Devuelve los nombres (ids) de plantillas disponibles."""
        return list(self.TEMPLATES.keys())

    def get_template_info(self, template_name: str) -> Dict[str, str]:
        """Devuelve nombre y descripción de una plantilla."""
        info = self.TEMPLATES.get(template_name, {})
        return {
            "name": info.get("name", template_name),
            "description": info.get("description", ""),
        }
