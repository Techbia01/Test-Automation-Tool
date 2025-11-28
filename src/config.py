#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuración del Sistema de Automatización de Casos de Prueba
Configuraciones personalizables para diferentes necesidades de QA
"""

from typing import Dict, List, Any
from dataclasses import dataclass

@dataclass
class ValidationConfig:
    """Configuración para validación de casos de prueba"""
    min_steps: int = 2
    max_steps: int = 10
    min_description_length: int = 20
    required_fields: List[str] = None
    forbidden_words: List[str] = None
    
    def __post_init__(self):
        if self.required_fields is None:
            self.required_fields = ['title', 'description', 'steps', 'expected_result']
        if self.forbidden_words is None:
            self.forbidden_words = ['test', 'prueba', 'verificar', 'validar']

@dataclass
class GenerationConfig:
    """Configuración para generación de casos de prueba"""
    include_integration_tests: bool = True
    include_edge_cases: bool = True
    include_negative_tests: bool = True
    include_performance_tests: bool = False
    include_security_tests: bool = False
    max_cases_per_criteria: int = 3
    auto_generate_alternatives: bool = True

@dataclass
class ExportConfig:
    """Configuración para exportación de casos de prueba"""
    default_format: str = "excel"
    include_validation_results: bool = True
    include_metadata: bool = True
    custom_fields: List[str] = None
    
    def __post_init__(self):
        if self.custom_fields is None:
            self.custom_fields = []

class QAConfig:
    """Configuración principal del sistema QA"""
    
    def __init__(self):
        self.validation = ValidationConfig()
        self.generation = GenerationConfig()
        self.export = ExportConfig()
        self.custom_templates = {}
        self.quality_thresholds = {
            'excellent': 90,
            'good': 80,
            'acceptable': 70,
            'needs_improvement': 60
        }
    
    def load_from_file(self, config_file: str):
        """Carga configuración desde archivo JSON"""
        import json
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            
            # Actualizar configuraciones
            if 'validation' in config_data:
                self._update_validation_config(config_data['validation'])
            if 'generation' in config_data:
                self._update_generation_config(config_data['generation'])
            if 'export' in config_data:
                self._update_export_config(config_data['export'])
            
            print(f"✅ Configuración cargada desde {config_file}")
        except FileNotFoundError:
            print(f"⚠️  Archivo de configuración {config_file} no encontrado, usando configuración por defecto")
        except Exception as e:
            print(f"❌ Error al cargar configuración: {e}")
    
    def save_to_file(self, config_file: str):
        """Guarda configuración a archivo JSON"""
        import json
        config_data = {
            'validation': {
                'min_steps': self.validation.min_steps,
                'max_steps': self.validation.max_steps,
                'min_description_length': self.validation.min_description_length,
                'required_fields': self.validation.required_fields,
                'forbidden_words': self.validation.forbidden_words
            },
            'generation': {
                'include_integration_tests': self.generation.include_integration_tests,
                'include_edge_cases': self.generation.include_edge_cases,
                'include_negative_tests': self.generation.include_negative_tests,
                'include_performance_tests': self.generation.include_performance_tests,
                'include_security_tests': self.generation.include_security_tests,
                'max_cases_per_criteria': self.generation.max_cases_per_criteria,
                'auto_generate_alternatives': self.generation.auto_generate_alternatives
            },
            'export': {
                'default_format': self.export.default_format,
                'include_validation_results': self.export.include_validation_results,
                'include_metadata': self.export.include_metadata,
                'custom_fields': self.export.custom_fields
            }
        }
        
        try:
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=2, ensure_ascii=False)
            print(f"✅ Configuración guardada en {config_file}")
        except Exception as e:
            print(f"❌ Error al guardar configuración: {e}")
    
    def _update_validation_config(self, config_data: Dict[str, Any]):
        """Actualiza configuración de validación"""
        for key, value in config_data.items():
            if hasattr(self.validation, key):
                setattr(self.validation, key, value)
    
    def _update_generation_config(self, config_data: Dict[str, Any]):
        """Actualiza configuración de generación"""
        for key, value in config_data.items():
            if hasattr(self.generation, key):
                setattr(self.generation, key, value)
    
    def _update_export_config(self, config_data: Dict[str, Any]):
        """Actualiza configuración de exportación"""
        for key, value in config_data.items():
            if hasattr(self.export, key):
                setattr(self.export, key, value)
    
    def get_quality_level(self, score: float) -> str:
        """Determina el nivel de calidad basado en el puntaje"""
        if score >= self.quality_thresholds['excellent']:
            return "Excelente"
        elif score >= self.quality_thresholds['good']:
            return "Bueno"
        elif score >= self.quality_thresholds['acceptable']:
            return "Aceptable"
        elif score >= self.quality_thresholds['needs_improvement']:
            return "Necesita Mejoras"
        else:
            return "Crítico"

# Configuraciones predefinidas para diferentes tipos de proyectos
class ProjectConfigs:
    """Configuraciones predefinidas para diferentes tipos de proyectos"""
    
    @staticmethod
    def get_web_app_config() -> QAConfig:
        """Configuración para aplicaciones web"""
        config = QAConfig()
        config.generation.include_performance_tests = True
        config.generation.include_security_tests = True
        config.validation.min_description_length = 30
        config.export.default_format = "excel"
        return config
    
    @staticmethod
    def get_mobile_app_config() -> QAConfig:
        """Configuración para aplicaciones móviles"""
        config = QAConfig()
        config.generation.include_performance_tests = True
        config.validation.max_steps = 8  # Pasos más cortos para móvil
        config.export.default_format = "json"
        return config
    
    @staticmethod
    def get_api_config() -> QAConfig:
        """Configuración para APIs"""
        config = QAConfig()
        config.generation.include_security_tests = True
        config.generation.include_performance_tests = True
        config.validation.min_description_length = 25
        config.export.include_metadata = True
        return config
    
    @staticmethod
    def get_enterprise_config() -> QAConfig:
        """Configuración para aplicaciones empresariales"""
        config = QAConfig()
        config.validation.min_description_length = 40
        config.validation.max_steps = 12
        config.generation.max_cases_per_criteria = 5
        config.export.include_validation_results = True
        return config

# Instancia global de configuración
qa_config = QAConfig()

def load_config(config_file: str = "qa_config.json"):
    """Carga la configuración global"""
    global qa_config
    qa_config.load_from_file(config_file)

def save_config(config_file: str = "qa_config.json"):
    """Guarda la configuración global"""
    global qa_config
    qa_config.save_to_file(config_file)

def get_config() -> QAConfig:
    """Obtiene la configuración global"""
    return qa_config
