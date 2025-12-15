#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador Profesional de Casos de Prueba QA
Inspirado en las mejores prácticas de QA profesional
"""

import sys
import io
import re
from typing import List, Dict, Tuple
from dataclasses import dataclass
from enum import Enum

# Configurar encoding UTF-8 para Windows (soluciona error 'charmap' codec)
if sys.platform == 'win32':
<<<<<<< HEAD
    try:
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
            sys.stderr.reconfigure(encoding='utf-8', errors='replace')
        else:
            # Para versiones anteriores de Python
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    except (AttributeError, ValueError, TypeError):
        # Si falla, intentar método alternativo
        try:
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
        except:
            pass  # Si todo falla, continuar sin modificar
=======
    # Reconfigurar stdout y stderr para usar UTF-8
    if hasattr(sys.stdout, 'reconfigure'):
        try:
            sys.stdout.reconfigure(encoding='utf-8')
            sys.stderr.reconfigure(encoding='utf-8')
        except (AttributeError, ValueError):
            # Si falla, usar método alternativo
            pass
>>>>>>> ddffd247ea1c50012c5260013eb3f649b4834531

# Importar parser adaptativo
try:
    from .adaptive_parser import parse_user_story_adaptive, StoryStructureType
except ImportError:
    # Si falla el import relativo, intentar absoluto
    try:
        from src.adaptive_parser import parse_user_story_adaptive, StoryStructureType
    except ImportError:
        # Si no está disponible, usar None (fallback al método original)
        parse_user_story_adaptive = None
        StoryStructureType = None


class TestPriority(Enum):
    """Prioridad de los casos de prueba"""
    ALTA = "Alta"
    MEDIA = "Media"
    BAJA = "Baja"


class TestType(Enum):
    """Tipo de caso de prueba"""
    FUNCIONAL = "Funcional"
    INTEGRACION = "Integración"
    REGRESION = "Regresión"
    NEGATIVO = "Negativo"
    UI = "UI"


@dataclass
class TestCase:
    """Caso de prueba profesional"""
    id: str
    title: str
    criterion: str
    test_type: TestType
    priority: TestPriority
    preconditions: List[str]
    steps: List[str]
    expected_result: str
    
    def to_dict(self) -> Dict:
        """Convierte el caso de prueba a diccionario para exportar"""
        return {
            'test_case_id': self.id,
            'title': self.title,
            'description': self._format_description(),
            'preconditions': self.preconditions,  # Lista, no string
            'steps': self.steps,  # Lista, no string
            'expected_result': self.expected_result,
            'priority': self.priority.value,
            'type': self.test_type.value
        }
    
    def _format_description(self) -> str:
        """Formatea la descripción para Linear con formato Markdown profesional"""
        # Formatear precondiciones (formato Markdown)
        preconditions_text = '\n'.join([f"- {p}" for p in self.preconditions])
        
        # Formatear pasos Gherkin (formato código)
        steps_text = '\n'.join(self.steps)
        
        return f"""**Criterio de Aceptación:**
{self.criterion}

**Tipo:** {self.test_type.value} | **Prioridad:** {self.priority.value}

**Precondiciones:**
{preconditions_text}

**Pasos (lenguaje Gherkin):**
```gherkin
{steps_text}
```

**Resultado Esperado:**
{self.expected_result}"""


class ProfessionalQAGenerator:
    """
    Generador profesional de casos de prueba
    Extrae criterios y genera casos de prueba de alta calidad
    """
    
    def __init__(self):
        # Patrones para identificar criterios de aceptación
        self.criterion_patterns = [
            r'✅\s*(.+?)(?=\n✅|\n\n|$)',  # Con emoji
            r'(?:^|\n)[-•]\s*(.+?)(?=\n[-•]|\n\n|$)',  # Con bullets
        ]
    
    def _clean_technical_noise(self, text: str) -> str:
        """
        Limpia el texto de ruido técnico (código, URLs, ejemplos JSON)
        para mejorar la extracción de criterios
        """
        cleaned = text
        
        try:
            # Remover bloques de código JSON (entre llaves grandes)
            cleaned = re.sub(r'\{[^}]{100,}\}', '', cleaned, flags=re.DOTALL)
        except Exception as e:
            print(f"[WARN] Error limpiando JSON: {e}", flush=True)
        
        try:
            # Remover URLs
            cleaned = re.sub(r'https?://[^\s]+', '', cleaned)
        except Exception as e:
            print(f"[WARN] Error limpiando URLs: {e}", flush=True)
        
        try:
            # Remover bloques de "Ejemplos:" hasta el siguiente salto de línea doble
            cleaned = re.sub(r'Ejemplos?:.*?(?=\n\n|$)', '', cleaned, flags=re.IGNORECASE | re.DOTALL)
        except Exception as e:
            print(f"[WARN] Error limpiando Ejemplos: {e}", flush=True)
        
        try:
            # Remover menciones de "Para determinar..." y bloques técnicos
            cleaned = re.sub(r'Para determinar[^\.]+\.', '', cleaned, flags=re.IGNORECASE)
        except Exception as e:
            print(f"[WARN] Error limpiando Para determinar: {e}", flush=True)
        
        try:
            # Remover bloques de "Campos obligatorios" y similares hasta salto de línea doble
            cleaned = re.sub(r'Campos\s+(?:obligatorios?|opcionales?)[:\s].*?(?=\n\n|$)', '', cleaned, flags=re.IGNORECASE | re.DOTALL)
        except Exception as e:
            print(f"[WARN] Error limpiando Campos: {e}", flush=True)
        
        print(f"[INFO] Texto limpiado: {len(text)} -> {len(cleaned)} caracteres", flush=True)
        return cleaned
    
    def extract_criteria_from_text(self, text: str) -> List[str]:
        """
        Extrae criterios de aceptación del texto de forma ULTRA ROBUSTA
        Funciona con CUALQUIER formato: FIN, EMS, OPS, AIA, etc.
        Especialmente diseñado para HUs técnicas complejas con código y ejemplos.
        
        Ahora usa parser adaptativo que detecta automáticamente el tipo de estructura.
        """
        criteria = []
        
        print("[INFO] Iniciando extracción de criterios...", flush=True)
        print(f"[INFO] Tamaño del texto: {len(text)} caracteres", flush=True)
        
        # PASO 0: Intentar usar parser adaptativo (si está disponible)
        if parse_user_story_adaptive is not None:
            try:
                print("[INFO] Usando parser adaptativo para detectar estructura...", flush=True)
                parsed_story = parse_user_story_adaptive(text)
                
                print(f"[INFO] Estructura detectada: {parsed_story.structure_type.value}", flush=True)
                
                # Si es estructura narrativa o mixta, usar los criterios del parser adaptativo
                if parsed_story.structure_type in [StoryStructureType.NARRATIVE, StoryStructureType.MIXED]:
                    criteria = parsed_story.acceptance_criteria
                    if criteria:
                        print(f"[OK] {len(criteria)} criterios extraídos con parser adaptativo (narrativo/mixto)", flush=True)
                        # Complementar con análisis técnico si hay pocos criterios
                        if len(criteria) < 5:
                            print("[INFO] Complementando con análisis técnico...", flush=True)
                            technical_criteria = self._extract_technical_requirements(text)
                            criteria.extend(technical_criteria)
                        return criteria
                # Si es tradicional, continuar con el método original (más robusto para ese formato)
                elif parsed_story.structure_type == StoryStructureType.TRADITIONAL:
                    print("[INFO] Estructura tradicional detectada, usando método robusto original...", flush=True)
                    # Continuar con el método original (más abajo)
                else:
                    print("[INFO] Estructura desconocida, usando método robusto original...", flush=True)
                    # Continuar con el método original
            except Exception as e:
                print(f"[WARN] Error en parser adaptativo, usando método original: {e}", flush=True)
                # Continuar con el método original
        
        # PASO 0: Limpiar el texto de ruido (código JSON, URLs, etc.)
        cleaned_text = self._clean_technical_noise(text)
        
        # MÉTODO 1: Buscar sección explícita de "Criterios de aceptación"
        criteria_section_patterns = [
            r'Criterios?\s+de\s+[Aa]ceptaci[oó]n[:\s]*(.+?)(?=\n\n[A-Z][a-z]+:|$)',
            r'Criterios?\s+de\s+[Aa]ceptaci[oó]n[:\s]*(.+)$',
            r'Acceptance\s+[Cc]riteria[:\s]*(.+?)(?=\n\n[A-Z][a-z]+:|$)',
            r'AC[:\s]*(.+)$',  # Para formatos cortos "AC:"
        ]
        
        criteria_text = None
        for pattern in criteria_section_patterns:
            match = re.search(pattern, cleaned_text, re.IGNORECASE | re.DOTALL)
            if match:
                criteria_text = match.group(1).strip()
                print(f"[OK] Sección de criterios encontrada (patrón: {pattern[:30]}...)", flush=True)
                break
        
        if not criteria_text:
            print("[WARN] No se encontró sección explícita de criterios", flush=True)
            print("[INFO] Buscando criterios en todo el texto...", flush=True)
            # Si no hay sección explícita, usar todo el texto después de "Descripción"
            desc_match = re.search(r'Descripci[oó]n[:\s]*(.+)$', cleaned_text, re.IGNORECASE | re.DOTALL)
            if desc_match:
                criteria_text = desc_match.group(1).strip()
            else:
                criteria_text = cleaned_text
        
        # MÉTODO 2: Extraer criterios con diferentes formatos
        
        # 2A: FORMATO GHERKIN (Given/When/Then) - PRIORIDAD MÁXIMA para HUs técnicas
        gherkin_criteria = re.findall(
            r'Given\s+[^\.]+When\s+[^\.]+Then\s+[^\.]+',
            criteria_text,
            re.IGNORECASE
        )
        if gherkin_criteria:
            criteria = [c.strip() for c in gherkin_criteria]
            print(f"[OK] {len(criteria)} criterios encontrados (formato Gherkin Given/When/Then)", flush=True)
            
            # Si solo hay pocos criterios Gherkin, complementar con criterios técnicos
            if len(criteria) < 5:
                print("[INFO] Pocos criterios Gherkin, complementando con análisis técnico...", flush=True)
                technical_criteria = self._extract_technical_requirements(text)
                criteria.extend(technical_criteria)
                print(f"[OK] Total: {len(criteria)} criterios (Gherkin + técnicos)", flush=True)
            
            return criteria
        
        # 2B: Con emojis ✅ o ✓
        emoji_criteria = re.findall(r'[✅✓]\s*([^\n✅✓]+)', criteria_text)
        if emoji_criteria:
            criteria = [c.strip() for c in emoji_criteria if len(c.strip()) > 10]
            print(f"[OK] {len(criteria)} criterios encontrados con emojis", flush=True)
            
            # NUEVO: Complementar con reglas de negocio y ejemplos si hay pocos criterios
            if len(criteria) < 8:
                print("[INFO] Pocos criterios con emojis, complementando con reglas de negocio...", flush=True)
                business_rules = self._extract_business_rules(text)
                criteria.extend(business_rules)
                print(f"[OK] Total: {len(criteria)} criterios (emojis + reglas)", flush=True)
            
            return criteria
        
        # 2B: Listas numeradas (1., 2., etc.)
        numbered_criteria = re.findall(r'(?:^|\n)\s*\d+[\.)]\s*([^\n]+)', criteria_text, re.MULTILINE)
        if numbered_criteria:
            criteria = [c.strip() for c in numbered_criteria if len(c.strip()) > 10]
            print(f"[OK] {len(criteria)} criterios encontrados (lista numerada)", flush=True)
            return criteria
        
        # 2C: Bullets (-, •, *)
        bullet_criteria = re.findall(r'(?:^|\n)\s*[-•*]\s*([^\n]+)', criteria_text, re.MULTILINE)
        if bullet_criteria:
            criteria = [c.strip() for c in bullet_criteria if len(c.strip()) > 10]
            print(f"[OK] {len(criteria)} criterios encontrados (bullets)", flush=True)
            return criteria
        
        # MÉTODO 3: Dividir por líneas y filtrar líneas que parezcan criterios
        print("[INFO] No se encontraron listas, analizando líneas individuales...", flush=True)
        lines = criteria_text.split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Saltar líneas muy cortas o títulos
            if len(line) < 15:
                continue
            
            # Saltar líneas que son títulos de sección
            if re.match(r'^[A-Z][a-záéíóúüñ\s]+:$', line):
                continue
            
            # Si la línea parece un criterio, agregarla
            if self._looks_like_criterion(line):
                criteria.append(line)
        
        if criteria:
            print(f"[OK] {len(criteria)} criterios encontrados (análisis de líneas)", flush=True)
            return criteria
        
        # MÉTODO 4: Último recurso - dividir por frases (punto + mayúscula)
        print("[INFO] Intentando dividir por frases...", flush=True)
        sentences = re.split(r'\.\s+(?=[A-ZÁÉÍÓÚÜÑ])', criteria_text)
        
        for sentence in sentences:
            sentence = sentence.strip().rstrip('.')
            
            if self._is_valid_criterion(sentence):
                criteria.append(sentence)
        
        if criteria:
            print(f"[OK] {len(criteria)} criterios encontrados (división por frases)", flush=True)
        else:
            print("[ERROR] No se pudieron extraer criterios con ningún método", flush=True)
        
        return criteria
    
    def _extract_business_rules(self, full_text: str) -> List[str]:
        """
        Extrae reglas de negocio, ejemplos y condiciones adicionales
        Especialmente útil para HUs con pocas marcas explícitas pero mucha lógica
        """
        business_criteria = []
        
        print("[INFO] Analizando reglas de negocio y ejemplos...", flush=True)
        
        # 1. BUSCAR SECCIÓN "Reglas de negocio"
        try:
            rules_match = re.search(r'Reglas?\s+de\s+negocio[:\s]*(.+?)(?=\n\n[A-Z]|Criterios|Ejemplos|$)', 
                                   full_text, re.IGNORECASE | re.DOTALL)
            if rules_match:
                rules_section = rules_match.group(1)
                
                # Extraer líneas que empiezan con condiciones o descripciones
                rule_lines = re.findall(r'(?:^|\n)\s*([A-Z][^:\n]{15,}[\.:].*?)(?=\n|$)', 
                                       rules_section, re.MULTILINE)
                for rule in rule_lines:
                    rule = rule.strip().rstrip('.:')
                    if len(rule) > 20 and any(kw in rule.lower() for kw in 
                        ['si ', 'cuando', 'debe', 'genera', 'no genera', 'actualiza', 'crea']):
                        business_criteria.append(rule)
        except Exception as e:
            print(f"[WARN] Error extrayendo reglas de negocio: {e}", flush=True)
        
        # 2. BUSCAR EJEMPLOS ESPECÍFICOS (formato: "X, mes, NT: condición → resultado")
        try:
            examples = re.findall(
                r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*),\s*([A-Z][a-z]+-\d{4}),\s*(NT\d+):\s*(.+?)\s*→\s*(.+?)(?=\n|$)',
                full_text
            )
            for comercializador, fecha, nt, condicion, resultado in examples:
                criterio = f"Caso {comercializador} {fecha} {nt}: {condicion.strip()} debe {resultado.strip()}"
                business_criteria.append(criterio)
        except Exception as e:
            print(f"[WARN] Error extrayendo ejemplos: {e}", flush=True)
        
        # 3. BUSCAR CONDICIONES "Se genera alerta si..."
        try:
            alert_conditions = re.findall(
                r'(?:Se genera alerta|Genera alerta|Crea alerta)\s+(?:si y solo si|si|cuando)[:\s]*(.+?)(?=\n\n|\n[A-Z][a-z]+:|$)',
                full_text, re.IGNORECASE | re.DOTALL
            )
            for condition in alert_conditions:
                # Dividir por saltos de línea o puntos para obtener sub-condiciones
                sub_conditions = re.split(r'\.\s*(?=[A-Z])|(?:\n\s*[-•]\s*)', condition)
                for sub in sub_conditions:
                    sub = sub.strip().rstrip('.')
                    if len(sub) > 25:
                        business_criteria.append(f"Genera alerta si: {sub}")
        except Exception as e:
            print(f"[WARN] Error extrayendo condiciones de alerta: {e}", flush=True)
        
        # 4. BUSCAR CONDICIONES NEGATIVAS "No genera alerta si..."
        try:
            no_alert_conditions = re.findall(
                r'(?:No\s+genera\s+alerta|No\s+se\s+crean?\s+alertas?)\s+(?:si|cuando)[:\s]*(.+?)(?=\n\n|\n[A-Z]|$)',
                full_text, re.IGNORECASE | re.DOTALL
            )
            for condition in no_alert_conditions:
                # Dividir por puntos o "o"
                sub_conditions = re.split(r'\.\s*(?=[A-Z])|\s+o\s+', condition)
                for sub in sub_conditions:
                    sub = sub.strip().rstrip('.')
                    if len(sub) > 25:
                        business_criteria.append(f"No genera alerta si: {sub}")
        except Exception as e:
            print(f"[WARN] Error extrayendo condiciones negativas: {e}", flush=True)
        
        # 5. BUSCAR PLANTILLAS DE MENSAJE
        try:
            message_templates = re.findall(
                r'(?:Plantilla|Mensaje|Formato)[:\s]*["\'](.+?)["\']',
                full_text, re.IGNORECASE
            )
            for template in message_templates:
                if len(template) > 30:
                    business_criteria.append(f"Validar formato de mensaje: debe seguir plantilla especificada")
        except Exception as e:
            print(f"[WARN] Error extrayendo plantillas: {e}", flush=True)
        
        # 6. BUSCAR "Actualizaciones:" o "Reimportar"
        try:
            update_rules = re.findall(
                r'(?:Si se reimporta|Reimportar|Actualización)[:\s]*(.+?)(?=\n\n|\n[A-Z][a-z]+:|$)',
                full_text, re.IGNORECASE
            )
            for rule in update_rules:
                rule = rule.strip().rstrip('.')
                if len(rule) > 25:
                    business_criteria.append(f"Actualización: {rule}")
        except Exception as e:
            print(f"[WARN] Error extrayendo reglas de actualización: {e}", flush=True)
        
        print(f"[OK] {len(business_criteria)} criterios de reglas de negocio extraídos", flush=True)
        
        # Limitar a los 15 más relevantes si hay demasiados
        if len(business_criteria) > 15:
            business_criteria = business_criteria[:15]
            print(f"[INFO] Limitando a 15 criterios de negocio más relevantes", flush=True)
        
        return business_criteria
    
    def _extract_technical_requirements(self, full_text: str) -> List[str]:
        """
        Extrae criterios técnicos implícitos de HUs muy técnicas
        Genera criterios de prueba basándose en la lógica de negocio descrita
        """
        technical_criteria = []
        
        print("[INFO] Analizando lógica de negocio técnica...", flush=True)
        
        # Buscar secciones específicas de lógica técnica
        sections_to_analyze = []
        
        # 1. Buscar "Lógica de negocio"
        try:
            logic_match = re.search(r'Lógica\s+de\s+negocio[:\s]*(.+?)(?=\n\n|$)', full_text, re.IGNORECASE | re.DOTALL)
            if logic_match:
                sections_to_analyze.append(("Lógica de negocio", logic_match.group(1)))
        except Exception as e:
            print(f"[WARN] Error buscando lógica de negocio: {e}", flush=True)
        
        # 2. Buscar "Procesamiento para..."
        processing_matches = re.finditer(r'Procesamiento\s+para\s+([^:]+):(.+?)(?=\n\nProcesamiento|$)', full_text, re.IGNORECASE | re.DOTALL)
        for match in processing_matches:
            sections_to_analyze.append((f"Procesamiento {match.group(1)}", match.group(2)))
        
        # 3. Buscar "Validar", "Verificar", "Asegurar"
        validation_patterns = [
            r'Validar?\s+([^\.]+\.)',
            r'Verificar?\s+([^\.]+\.)',
            r'Asegurar?\s+que\s+([^\.]+\.)',
            r'Comprobar?\s+que\s+([^\.]+\.)'
        ]
        
        for pattern in validation_patterns:
            matches = re.findall(pattern, full_text, re.IGNORECASE)
            for match in matches:
                if len(match) > 20:
                    technical_criteria.append(f"Validar que {match.strip()}")
        
        # 4. Analizar cada sección y extraer operaciones clave
        for section_name, section_text in sections_to_analyze:
            # Buscar acciones clave: Insertar, Actualizar, Eliminar, Crear, Buscar
            actions = {
                'insertar': r'Insertar?\s+en\s+([^\.]+)',
                'crear': r'Crear?\s+([^\.]+?)\s+(?:en|con)',
                'actualizar': r'Actualizar?\s+([^\.]+)',
                'eliminar': r'Eliminar?\s+([^\.]+)',
                'marcar': r'Marcar?\s+([^\.]+)',
                'buscar': r'Buscar?\s+([^\.]+)',
                'validar': r'Validar?\s+([^\.]+)',
            }
            
            for action, pattern in actions.items():
                matches = re.findall(pattern, section_text, re.IGNORECASE)
                for match in matches:
                    if len(match) > 10:
                        criterion = f"{action.capitalize()} {match.strip()}"
                        if criterion not in technical_criteria:
                            technical_criteria.append(criterion)
        
        # 5. Buscar manejo de errores y casos especiales
        error_handling = re.findall(
            r'(?:Si\s+falla|En\s+caso\s+de\s+error|Manejo\s+de\s+errores?)[:\s]*([^\.]+\.)',
            full_text,
            re.IGNORECASE
        )
        for error in error_handling:
            if len(error) > 20:
                technical_criteria.append(f"Manejo de error: {error.strip()}")
        
        # 6. Buscar integraciones con otros servicios
        integrations = re.findall(
            r'(?:Integr(?:a|ación)\s+con|Llama(?:da)?\s+(?:al|a)|Consumir?)\s+([A-Z][a-z-]+[A-Za-z0-9-]*)',
            full_text
        )
        for integration in set(integrations):  # Eliminar duplicados
            if len(integration) > 3:
                technical_criteria.append(f"Integración con {integration}")
        
        print(f"[OK] {len(technical_criteria)} criterios técnicos extraídos", flush=True)
        
        # Limitar a los 10 más relevantes si hay demasiados
        if len(technical_criteria) > 10:
            technical_criteria = technical_criteria[:10]
            print(f"[INFO] Limitando a 10 criterios más relevantes", flush=True)
        
        return technical_criteria
    
    def _looks_like_criterion(self, text: str) -> bool:
        """
        Verifica si una línea parece ser un criterio de aceptación
        Versión ULTRA EXPANDIDA con 120+ palabras clave
        """
        text_lower = text.lower()
        
        # ========== PALABRAS CLAVE EXPANDIDAS (120+) ==========
        
        # 1. VERBOS DE ACCIÓN (40)
        action_verbs = [
            'debe', 'puede', 'permite', 'valida', 'verifica', 'guarda', 
            'muestra', 'crea', 'genera', 'envía', 'recibe', 'procesa',
            'almacena', 'elimina', 'actualiza', 'consulta', 'modifica',
            'agrega', 'añade', 'borra', 'quita', 'limpia', 'resetea',
            'carga', 'descarga', 'sube', 'baja', 'importa', 'exporta',
            'sincroniza', 'autentica', 'autoriza', 'registra', 'loguea',
            'calcula', 'computa', 'suma', 'resta', 'multiplica'
        ]
        
        # 2. VERBOS DE VALIDACIÓN Y VERIFICACIÓN (20)
        validation_verbs = [
            'valida', 'verifica', 'comprueba', 'confirma', 'revisa',
            'asegura', 'garantiza', 'chequea', 'testea', 'prueba',
            'certifica', 'audita', 'inspecciona', 'examina', 'analiza',
            'evalúa', 'detecta', 'identifica', 'reconoce', 'compara'
        ]
        
        # 3. CONDICIONALES Y FLUJOS (15)
        conditionals = [
            'cuando', 'si ', 'para', 'dado que', 'entonces', 'y ',
            'siempre que', 'en caso de', 'mientras', 'hasta que',
            'después de', 'antes de', 'durante', 'al momento de', 'tras'
        ]
        
        # 4. SUJETOS DEL SISTEMA (15)
        subjects = [
            'el sistema', 'el usuario', 'la aplicación', 'el servicio',
            'el módulo', 'el componente', 'la interfaz', 'el backend',
            'el frontend', 'la api', 'el endpoint', 'la bd', 'la base de datos',
            'el servidor', 'el cliente'
        ]
        
        # 5. EXPRESIONES DE POSIBILIDAD (12)
        possibility = [
            'que el', 'que la', 'se debe', 'se puede', 'se permite',
            'no se permite', 'solo ', 'únicamente', 'exclusivamente',
            'solamente', 'es posible', 'es necesario'
        ]
        
        # 6. EXPRESIONES DE NECESIDAD Y OBLIGACIÓN (10)
        necessity = [
            'es necesario', 'es obligatorio', 'es requerido', 'es mandatorio',
            'tiene que', 'necesita', 'requiere', 'hace falta', 'exige', 'demanda'
        ]
        
        # 7. PALABRAS UI/UX (20)
        ui_keywords = [
            'field', 'button', 'table', 'form', 'input', 'output',
            'campo', 'botón', 'tabla', 'formulario', 'entrada', 'salida',
            'modal', 'dropdown', 'checkbox', 'radio', 'select', 'textarea',
            'pantalla', 'vista'
        ]
        
        # 8. ESTADOS DE DATOS (15)
        data_states = [
            'obligatorio', 'requerido', 'opcional', 'por defecto',
            'vacío', 'nulo', 'null', 'undefined', 'inválido', 'válido',
            'correcto', 'incorrecto', 'completo', 'incompleto', 'duplicado'
        ]
        
        # 9. OPERACIONES DE BD Y PERSISTENCIA (18)
        db_operations = [
            'inserta', 'insertar', 'guarda', 'guardar', 'almacena', 'almacenar',
            'persiste', 'persistir', 'actualiza', 'actualizar', 'modifica', 'modificar',
            'elimina', 'eliminar', 'borra', 'borrar', 'marca', 'marcar'
        ]
        
        # 10. RESPUESTAS Y RESULTADOS (15)
        responses = [
            'retorna', 'devuelve', 'responde', 'muestra', 'presenta',
            'despliega', 'exhibe', 'informa', 'notifica', 'alerta',
            'avisa', 'comunica', 'indica', 'señala', 'reporta'
        ]
        
        # 11. MENSAJES Y FEEDBACK (12)
        feedback = [
            'mensaje', 'error', 'alerta', 'warning', 'éxito', 'success',
            'confirmación', 'notificación', 'toast', 'feedback', 'aviso', 'info'
        ]
        
        # 12. INTEGRACIONES Y SERVICIOS (10)
        integrations = [
            'integra', 'conecta', 'consume', 'llama', 'invoca',
            'comunica con', 'se conecta a', 'interactúa con', 'envía a', 'recibe de'
        ]
        
        # 13. MANEJO DE ERRORES (10)
        error_handling = [
            'si falla', 'en caso de error', 'cuando falla', 'si error',
            'manejo de error', 'captura error', 'loguea error', 'reporta error',
            'rollback', 'revierte'
        ]
        
        # 14. PALABRAS TÉCNICAS (10)
        technical = [
            'api', 'endpoint', 'request', 'response', 'json', 'xml',
            'token', 'session', 'cookie', 'header'
        ]
        
        # Combinar todas las listas
        criterion_keywords = (
            action_verbs + validation_verbs + conditionals + subjects +
            possibility + necessity + ui_keywords + data_states +
            db_operations + responses + feedback + integrations +
            error_handling + technical
        )
        
        # Si contiene alguna palabra clave, es muy probable que sea un criterio
        return any(keyword in text_lower for keyword in criterion_keywords)
    
    def _is_valid_criterion(self, text: str) -> bool:
        """
        Valida si un texto es un criterio de aceptación válido
        Versión expandida con 50+ inicios válidos
        """
        text_lower = text.lower()
        
        # Debe tener longitud mínima
        if len(text) < 20:
            return False
        
        # ========== INICIOS VÁLIDOS EXPANDIDOS (50+) ==========
        valid_starts = [
            # Condicionales
            'cuando ', 'si ', 'siempre que ', 'en caso de ', 'al ',
            'después de ', 'antes de ', 'mientras ', 'durante ',
            
            # Propósitos
            'para ', 'a fin de ', 'con el objetivo de ', 'con el fin de ',
            
            # Sujetos + Campos
            'el campo ', 'el sistema ', 'el usuario ', 'la aplicación ',
            'el servicio ', 'el módulo ', 'el componente ', 'la interfaz ',
            'el botón ', 'la tabla ', 'el formulario ', 'la pantalla ',
            
            # Acciones directas
            'debe ', 'puede ', 'permite ', 'valida ', 'guarda ', 'toma ',
            'crea ', 'genera ', 'muestra ', 'presenta ', 'despliega ',
            'actualiza ', 'modifica ', 'elimina ', 'borra ', 'marca ',
            'retorna ', 'devuelve ', 'responde ', 'envía ', 'recibe ',
            
            # Negaciones
            'no existe', 'ya no existe', 'no se permite', 'no debe ',
            'no puede ', 'no hay ', 'no tiene ',
            
            # Verificaciones
            'asegurar ', 'verificar ', 'comprobar ', 'confirmar ',
            'garantizar ', 'revisar ', 'validar '
        ]
        
        return any(text_lower.startswith(start) for start in valid_starts)
    
    def generate_test_cases(self, user_story_text: str, project_name: str = "") -> List[TestCase]:
        """
        Genera casos de prueba profesionales a partir de una historia de usuario
        DESCOMPONE cada criterio en múltiples casos específicos (felices, errores, usabilidad, etc.)
        Ahora usa el contexto completo de la HU para generar casos más específicos y menos ambiguos.
        
        Args:
            user_story_text: Texto completo de la HU
            project_name: Nombre del proyecto (opcional)
            
        Returns:
            Lista de casos de prueba generados
        """
        print("\n" + "="*80)
        print("[INFO] GENERADOR PROFESIONAL DE CASOS DE PRUEBA MEJORADO")
        print("="*80)
        
        # Extraer contexto completo de la HU usando parser adaptativo
        parsed_story = None
        if parse_user_story_adaptive is not None:
            try:
                parsed_story = parse_user_story_adaptive(user_story_text)
                print(f"[INFO] Contexto extraído - Tipo: {parsed_story.structure_type.value}")
                print(f"[INFO] - Título: {parsed_story.title[:50]}...")
                print(f"[INFO] - Contexto: {parsed_story.context[:50] if parsed_story.context else 'N/A'}...")
                print(f"[INFO] - Descripción: {parsed_story.description[:50] if parsed_story.description else 'N/A'}...")
                print(f"[INFO] - Flujos: {len(parsed_story.user_flows)}")
                print(f"[INFO] - Estados: {len(parsed_story.states)}")
                print(f"[INFO] - Elementos UI: {len(parsed_story.ui_elements)}")
            except Exception as e:
                print(f"[WARN] Error usando parser adaptativo: {e}", flush=True)
        
        # Extraer criterios de aceptación
        criteria = self.extract_criteria_from_text(user_story_text)
        
        print(f"[OK] Criterios de aceptación encontrados: {len(criteria)}")
        for i, c in enumerate(criteria, 1):
            print(f"  {i}. {c[:70]}{'...' if len(c) > 70 else ''}")
        print("="*80)
        
        if not criteria:
            print("[ERROR] No se pudieron extraer criterios de aceptación")
            return []
        
        # Generar casos de prueba DESCOMPONIENDO cada criterio
        test_cases = []
        test_counter = 1
        
        for criterion in criteria:
            # DESCOMPONER cada criterio en múltiples casos específicos
            decomposed_cases = self._decompose_criterion_into_test_cases(
                criterion=criterion,
                start_number=test_counter,
                project_name=project_name,
                user_story_text=user_story_text,
                parsed_story=parsed_story  # Pasar contexto completo
            )
            test_cases.extend(decomposed_cases)
            test_counter += len(decomposed_cases)
        
        # Agregar casos adicionales globales (estados vacíos, errores generales, etc.)
        global_cases = self._generate_global_test_cases(
            start_number=test_counter,
            project_name=project_name,
            user_story_text=user_story_text,
            parsed_story=parsed_story  # Pasar contexto completo
        )
        test_cases.extend(global_cases)
        
        print(f"[OK] {len(test_cases)} casos de prueba generados exitosamente")
        print("="*80 + "\n")
        
        return test_cases
    
    def _decompose_criterion_into_test_cases(self, criterion: str, start_number: int, project_name: str, user_story_text: str, parsed_story=None) -> List[TestCase]:
        """
        Genera casos de prueba ÚNICOS y NO redundantes a partir de un criterio de aceptación.
        
        REGLAS OBLIGATORIAS (QA Lead):
        - Máximo 1 caso por criterio, salvo que aplique creación vs edición
        - Cada caso debe validar una regla de negocio distinta
        - No generar variantes del mismo caso con redacción diferente
        - No separar "persistencia" como caso distinto si pertenece al mismo flujo
        - Si dos casos validan lo mismo, consolidarlos en uno solo
        """
        test_cases = []
        counter = start_number
        criterion_lower = criterion.lower()
        
        # Detectar si el criterio menciona tanto creación como edición (reglas de negocio distintas)
        mentions_creation = any(word in criterion_lower for word in ['crea', 'crear', 'nuevo', 'nueva'])
        mentions_edition = any(word in criterion_lower for word in ['edita', 'editar', 'modifica', 'actualiza', 'cambia'])
        
        # Si menciona creación Y edición, generar casos separados (son reglas de negocio distintas)
        if mentions_creation and mentions_edition:
            # Caso para creación
            creation_criterion = self._extract_creation_part(criterion)
            if creation_criterion:
                creation_case = self._generate_happy_path_case(
                    criterion=creation_criterion,
                    test_number=counter,
                    project_name=project_name,
                    parsed_story=parsed_story
                )
                # Marcar explícitamente que es para creación
                creation_case.criterion = f"Objetivo: Validar funcionalidad de CREACIÓN\nCriterio: {creation_criterion}"
                test_cases.append(creation_case)
                counter += 1
            
            # Caso para edición
            edition_criterion = self._extract_edition_part(criterion)
            if edition_criterion:
                edition_case = self._generate_happy_path_case(
                    criterion=edition_criterion,
                    test_number=counter,
                    project_name=project_name,
                    parsed_story=parsed_story
                )
                # Marcar explícitamente que es para edición
                edition_case.criterion = f"Objetivo: Validar funcionalidad de EDICIÓN\nCriterio: {edition_criterion}"
                test_cases.append(edition_case)
                counter += 1
        else:
            # CASO ÚNICO: Happy Path que incluye persistencia si aplica
            # El happy path ya incluye validación de persistencia en el resultado esperado
            happy_case = self._generate_happy_path_case(
                criterion=criterion,
                test_number=counter,
                project_name=project_name,
                parsed_story=parsed_story
            )
            
            # Si el criterio menciona guardar/almacenar, asegurar que el resultado esperado incluya persistencia
            if any(word in criterion_lower for word in ['guarda', 'almacena', 'persiste', 'guardar', 'almacenar']):
                # Asegurar que el resultado esperado mencione persistencia
                if 'persiste' not in happy_case.expected_result.lower() and 'persistir' not in happy_case.expected_result.lower():
                    happy_case.expected_result += " Los datos deben persistir correctamente en el sistema."
            
            test_cases.append(happy_case)
            counter += 1
        
        # Solo generar casos adicionales si son reglas de negocio EXPLÍCITAS y DISTINTAS
        # (no variantes del mismo caso)
        
        # Caso negativo solo si el criterio explícitamente menciona validación de datos inválidos
        if any(word in criterion_lower for word in ['valida', 'verifica', 'comprueba']) and any(word in criterion_lower for word in ['inválido', 'incorrecto', 'error', 'no válido']):
            negative_case = self._generate_negative_validation_case(
                criterion=criterion,
                test_number=counter,
                project_name=project_name
            )
            test_cases.append(negative_case)
            counter += 1
        
        # Caso de estado deshabilitado solo si el criterio explícitamente menciona condiciones de deshabilitado
        if any(word in criterion_lower for word in ['deshabilitado', 'disabled', 'no aplica', 'n/a', 'no se muestra']) and any(word in criterion_lower for word in ['si', 'cuando', 'condición']):
            disabled_case = self._generate_disabled_state_case(
                criterion=criterion,
                test_number=counter,
                project_name=project_name
            )
            test_cases.append(disabled_case)
            counter += 1
        
        return test_cases
    
    def _extract_creation_part(self, criterion: str) -> str:
        """Extrae la parte del criterio relacionada con creación"""
        # Buscar frases que mencionen creación
        creation_patterns = [
            r'([^\.]+(?:crea|crear|nuevo|nueva)[^\.]+)',
            r'(?:al|cuando)\s+crear[^\.]+',
        ]
        
        for pattern in creation_patterns:
            match = re.search(pattern, criterion, re.IGNORECASE)
            if match:
                return match.group(1).strip() if match.groups() else match.group(0).strip()
        
        return None
    
    def _extract_edition_part(self, criterion: str) -> str:
        """Extrae la parte del criterio relacionada con edición"""
        # Buscar frases que mencionen edición
        edition_patterns = [
            r'([^\.]+(?:edita|editar|modifica|actualiza|cambia)[^\.]+)',
            r'(?:al|cuando)\s+(?:editar|modificar|actualizar)[^\.]+',
        ]
        
        for pattern in edition_patterns:
            match = re.search(pattern, criterion, re.IGNORECASE)
            if match:
                return match.group(1).strip() if match.groups() else match.group(0).strip()
        
        return None
    
    def _generate_global_test_cases(self, start_number: int, project_name: str, user_story_text: str, parsed_story=None) -> List[TestCase]:
        """Genera casos de prueba globales (estados vacíos generales, errores del sistema, etc.)"""
        test_cases = []
        counter = start_number
        
        # Solo generar casos globales si son relevantes para el contexto
        # Si la HU es muy específica (narrativa), no agregar casos genéricos
        if parsed_story and parsed_story.structure_type == StoryStructureType.NARRATIVE:
            # Para HUs narrativas, solo agregar casos relevantes al contexto
            if any("error" in flow.lower() or "falla" in flow.lower() for flow in parsed_story.user_flows):
                error_case = self._generate_backend_error_case(
                    test_number=counter,
                    project_name=project_name,
                    error_code=500
                )
                test_cases.append(error_case)
                counter += 1
        else:
            # Para HUs tradicionales, agregar casos globales estándar
            # Caso de estado vacío general
            empty_state_case = self._generate_general_empty_state_case(
                test_number=counter,
                project_name=project_name
            )
            test_cases.append(empty_state_case)
            counter += 1
            
            # Caso de error 500 del backend
            error_500_case = self._generate_backend_error_case(
                test_number=counter,
                project_name=project_name,
                error_code=500
            )
            test_cases.append(error_500_case)
            counter += 1
            
            # Caso de error 404 del backend
            error_404_case = self._generate_backend_error_case(
                test_number=counter,
                project_name=project_name,
                error_code=404
            )
            test_cases.append(error_404_case)
            counter += 1
        
        return test_cases
    
    # ========== MÉTODOS AUXILIARES PARA GENERAR CASOS ESPECÍFICOS ==========
    
    def _generate_happy_path_case(self, criterion: str, test_number: int, project_name: str, parsed_story=None) -> TestCase:
        """Genera caso feliz (happy path) para un criterio usando contexto real de la HU"""
        # Extraer objetivo del criterio (más específico)
        objective = self._extract_objective_from_criterion(criterion, parsed_story)
        
        # Título específico basado en el criterio y contexto
        title = self._generate_contextual_title(criterion, parsed_story)
        
        # Precondiciones específicas usando contexto de la HU
        preconditions = self._generate_contextual_preconditions(criterion, parsed_story)
        
        # Pasos específicos usando contexto y flujos de la HU
        steps = self._generate_contextual_steps(criterion, "happy_path", parsed_story)
        
        # Resultado esperado específico basado en el criterio y contexto
        expected_result = self._generate_contextual_expected_result(criterion, "happy_path", parsed_story)
        
        return TestCase(
            id=f"TC-{test_number:03d}",
            title=title,
            criterion=f"Objetivo: {objective}\nCriterio: {criterion}",
            test_type=TestType.FUNCIONAL,
            priority=TestPriority.ALTA,
            preconditions=preconditions,
            steps=steps,
            expected_result=expected_result
        )
    
    def _generate_empty_state_case(self, criterion: str, test_number: int, project_name: str) -> TestCase:
        """Genera caso de estado vacío"""
        objective = "Validar que cuando no hay datos disponibles, se muestra el estado vacío correctamente"
        title = self._generate_short_title(criterion)
        
        preconditions = [
            "El sistema está operativo",
            "El Source Bill ID existe pero no tiene datos asociados",
            "El backend retorna una lista vacía"
        ]
        
        steps = [
            "Given que el usuario accede al módulo",
            "When el sistema consulta los datos y no encuentra resultados",
            "Then el sistema muestra el mensaje de estado vacío apropiado",
            "And el mensaje es claro y consistente con el diseño del sistema"
        ]
        
        expected_result = "Se muestra el mensaje de estado vacío (ej: 'Aún no hay anulaciones para este Source Bill ID') de forma clara y consistente con el backend"
        
        return TestCase(
            id=f"TC-{test_number:03d}",
            title=title,
            criterion=f"Objetivo: {objective}\nCriterio: {criterion}",
            test_type=TestType.FUNCIONAL,
            priority=TestPriority.MEDIA,
            preconditions=preconditions,
            steps=steps,
            expected_result=expected_result
        )
    
    def _generate_error_case(self, criterion: str, test_number: int, project_name: str, error_type: str = "backend") -> TestCase:
        """Genera caso de manejo de errores"""
        if error_type == "backend":
            objective = "Validar que cuando el backend retorna un error, se muestra un mensaje de error apropiado"
            title = self._generate_short_title(criterion)
            preconditions = [
                "El sistema está operativo",
                "El backend está configurado para retornar un error 500"
            ]
            expected_result = "Se muestra un mensaje de error claro y consistente con el diseño del sistema cuando el backend retorna error 500"
        else:  # resource_not_available
            objective = "Validar que cuando un recurso (PDF, XML) no está disponible, se muestra un mensaje de error apropiado"
            title = self._generate_short_title(criterion)
            preconditions = [
                "El sistema está operativo",
                "Existe una anulación con ID válido pero el recurso (PDF/XML) no está disponible en el servidor"
            ]
            expected_result = "Se muestra un mensaje de error apropiado indicando que el recurso no está disponible"
        
        steps = [
            "Given que el usuario accede al módulo",
            f"When el sistema intenta {self._extract_action_from_criterion(criterion)}",
            "And ocurre un error (backend o recurso no disponible)",
            "Then el sistema muestra un mensaje de error claro y apropiado",
            "And el mensaje es consistente con el diseño del sistema"
        ]
        
        return TestCase(
            id=f"TC-{test_number:03d}",
            title=title,
            criterion=f"Objetivo: {objective}\nCriterio: {criterion}",
            test_type=TestType.NEGATIVO,
            priority=TestPriority.MEDIA,
            preconditions=preconditions,
            steps=steps,
            expected_result=expected_result
        )
    
    def _generate_usability_case(self, criterion: str, test_number: int, project_name: str) -> TestCase:
        """Genera caso de usabilidad"""
        objective = "Validar aspectos de usabilidad relacionados con el criterio"
        title = self._generate_short_title(criterion)
        
        preconditions = [
            "El sistema está operativo",
            "Los datos de prueba están disponibles"
        ]
        
        steps = [
            "Given que el usuario accede al módulo",
            f"When el usuario interactúa con {self._extract_ui_element_from_criterion(criterion)}",
            "Then los elementos interactivos responden correctamente",
            "And la retroalimentación visual es clara y apropiada"
        ]
        
        expected_result = "Los elementos de UI son claramente interactivos, la retroalimentación es inmediata y el comportamiento es intuitivo"
        
        return TestCase(
            id=f"TC-{test_number:03d}",
            title=title,
            criterion=f"Objetivo: {objective}\nCriterio: {criterion}",
            test_type=TestType.UI,
            priority=TestPriority.MEDIA,
            preconditions=preconditions,
            steps=steps,
            expected_result=expected_result
        )
    
    def _generate_negative_validation_case(self, criterion: str, test_number: int, project_name: str) -> TestCase:
        """Genera caso negativo de validación"""
        objective = "Validar que las validaciones funcionan correctamente con datos inválidos"
        title = self._generate_short_title(criterion)
        
        preconditions = [
            "El sistema está operativo",
            "Se tienen datos inválidos preparados para la prueba"
        ]
        
        steps = [
            "Given que el usuario accede al módulo",
            "When el usuario intenta realizar la acción con datos inválidos",
            "Then el sistema valida y muestra mensajes de error apropiados",
            "And no permite continuar hasta corregir los datos"
        ]
        
        expected_result = "El sistema valida correctamente, muestra mensajes de error claros y no permite continuar con datos inválidos"
        
        return TestCase(
            id=f"TC-{test_number:03d}",
            title=title,
            criterion=f"Objetivo: {objective}\nCriterio: {criterion}",
            test_type=TestType.NEGATIVO,
            priority=TestPriority.MEDIA,
            preconditions=preconditions,
            steps=steps,
            expected_result=expected_result
        )
    
    def _generate_persistence_case(self, criterion: str, test_number: int, project_name: str) -> TestCase:
        """Genera caso de persistencia de datos"""
        objective = "Validar que los datos se persisten correctamente en el sistema"
        title = self._generate_short_title(criterion)
        
        preconditions = [
            "El sistema está operativo",
            "El usuario tiene permisos para realizar la operación",
            "Los datos de prueba están disponibles"
        ]
        
        steps = [
            "Given que el usuario accede al módulo",
            f"When el usuario ejecuta la acción de {self._extract_action_from_criterion(criterion)}",
            "And el sistema confirma la operación exitosa",
            "Then los datos deben persistir correctamente en el sistema",
            "And al recargar la página, los datos deben estar disponibles"
        ]
        
        expected_result = "Los datos se guardan correctamente en el sistema y persisten después de recargar la página"
        
        return TestCase(
            id=f"TC-{test_number:03d}",
            title=title,
            criterion=f"Objetivo: {objective}\nCriterio: {criterion}",
            test_type=TestType.FUNCIONAL,
            priority=TestPriority.ALTA,
            preconditions=preconditions,
            steps=steps,
            expected_result=expected_result
        )
    
    def _generate_ui_element_case(self, criterion: str, test_number: int, project_name: str) -> TestCase:
        """Genera caso específico para elementos UI"""
        objective = "Validar el comportamiento y visualización de elementos UI específicos"
        title = self._generate_short_title(criterion)
        
        preconditions = [
            "El sistema está operativo",
            "Los datos de prueba están disponibles"
        ]
        
        ui_element = self._extract_ui_element_from_criterion(criterion)
        
        steps = [
            "Given que el usuario accede al módulo",
            f"When el usuario visualiza el elemento {ui_element}",
            "Then el elemento se muestra correctamente con el estilo apropiado",
            "And el elemento es funcional y responde a las interacciones"
        ]
        
        expected_result = f"El elemento {ui_element} se muestra correctamente, tiene el estilo apropiado y funciona según lo esperado"
        
        return TestCase(
            id=f"TC-{test_number:03d}",
            title=title,
            criterion=f"Objetivo: {objective}\nCriterio: {criterion}",
            test_type=TestType.UI,
            priority=TestPriority.MEDIA,
            preconditions=preconditions,
            steps=steps,
            expected_result=expected_result
        )
    
    def _generate_copy_action_case(self, criterion: str, test_number: int, project_name: str) -> TestCase:
        """Genera caso específico para acciones de copiar"""
        objective = "Validar que la funcionalidad de copiar al portapapeles funciona correctamente"
        title = self._generate_short_title(criterion)
        
        preconditions = [
            "El sistema está operativo",
            "Existe un valor copiable disponible"
        ]
        
        steps = [
            "Given que el usuario accede al módulo",
            "When el usuario hace clic en el botón copiar",
            "Then el valor se copia al portapapeles",
            "And se muestra feedback visual al usuario indicando que se copió"
        ]
        
        expected_result = "El valor se copia correctamente al portapapeles y se muestra feedback visual al usuario"
        
        return TestCase(
            id=f"TC-{test_number:03d}",
            title=title,
            criterion=f"Objetivo: {objective}\nCriterio: {criterion}",
            test_type=TestType.UI,
            priority=TestPriority.MEDIA,
            preconditions=preconditions,
            steps=steps,
            expected_result=expected_result
        )
    
    def _generate_disabled_state_case(self, criterion: str, test_number: int, project_name: str) -> TestCase:
        """Genera caso para estado deshabilitado"""
        objective = "Validar que cuando un elemento no aplica, se muestra deshabilitado correctamente"
        title = self._generate_short_title(criterion)
        
        preconditions = [
            "El sistema está operativo",
            "Existe un elemento que no aplica para el contexto actual"
        ]
        
        steps = [
            "Given que el usuario accede al módulo",
            "When el sistema determina que un elemento no aplica",
            "Then el elemento se muestra deshabilitado visualmente",
            "And el elemento no es clicable ni funcional"
        ]
        
        expected_result = "El elemento se muestra claramente deshabilitado y no permite interacción"
        
        return TestCase(
            id=f"TC-{test_number:03d}",
            title=title,
            criterion=f"Objetivo: {objective}\nCriterio: {criterion}",
            test_type=TestType.UI,
            priority=TestPriority.MEDIA,
            preconditions=preconditions,
            steps=steps,
            expected_result=expected_result
        )
    
    def _generate_error_handling_case(self, criterion: str, test_number: int, project_name: str) -> TestCase:
        """Genera caso específico de manejo de errores"""
        objective = "Validar que el sistema maneja errores apropiadamente según el criterio"
        title = self._generate_short_title(criterion)
        
        preconditions = [
            "El sistema está operativo",
            "Se puede simular el escenario de error descrito"
        ]
        
        steps = [
            "Given que el usuario accede al módulo",
            "When ocurre el error descrito en el criterio",
            "Then el sistema maneja el error apropiadamente",
            "And muestra mensajes claros al usuario",
            "And mantiene la estabilidad del sistema"
        ]
        
        expected_result = "El sistema maneja el error correctamente, muestra mensajes apropiados y mantiene la estabilidad"
        
        return TestCase(
            id=f"TC-{test_number:03d}",
            title=title,
            criterion=f"Objetivo: {objective}\nCriterio: {criterion}",
            test_type=TestType.NEGATIVO,
            priority=TestPriority.ALTA,
            preconditions=preconditions,
            steps=steps,
            expected_result=expected_result
        )
    
    def _generate_general_empty_state_case(self, test_number: int, project_name: str) -> TestCase:
        """Genera caso general de estado vacío"""
        return TestCase(
            id=f"TC-{test_number:03d}",
            title="Validar que cuando no existen datos en el sistema, se muestre el estado vacío con mensajes claros y consistentes",
            criterion="Objetivo: Validar que cuando no existen datos, se muestra el estado vacío correctamente\nCriterio: El sistema debe mostrar mensajes claros cuando no hay datos disponibles",
            test_type=TestType.FUNCIONAL,
            priority=TestPriority.MEDIA,
            preconditions=[
                "El sistema está operativo",
                "No existen datos asociados al contexto actual"
            ],
            steps=[
                "Given que el usuario accede al módulo",
                "When el sistema consulta los datos y no encuentra resultados",
                "Then se muestra el mensaje de estado vacío apropiado",
                "And el mensaje es claro y consistente con el diseño"
            ],
            expected_result="Se muestra el mensaje de estado vacío de forma clara y consistente"
        )
    
    def _generate_backend_error_case(self, test_number: int, project_name: str, error_code: int) -> TestCase:
        """Genera caso de error del backend"""
        error_name = "Error interno del servidor" if error_code == 500 else "Recurso no encontrado"
        return TestCase(
            id=f"TC-{test_number:03d}",
            title=f"Validar que cuando el backend retorna error {error_code}, el sistema muestre un mensaje de error apropiado y claro al usuario",
            criterion=f"Objetivo: Validar que cuando el backend retorna error {error_code}, se muestra un mensaje apropiado\nCriterio: El sistema debe manejar errores del backend ({error_code}) mostrando mensajes claros",
            test_type=TestType.NEGATIVO,
            priority=TestPriority.MEDIA,
            preconditions=[
                "El sistema está operativo",
                f"El backend está configurado para retornar error {error_code}"
            ],
            steps=[
                "Given que el usuario accede al módulo",
                f"When el backend retorna error {error_code}",
                "Then el sistema muestra un mensaje de error apropiado",
                "And el mensaje es claro y consistente con el diseño del sistema"
            ],
            expected_result=f"Se muestra un mensaje de error apropiado cuando el backend retorna {error_code}"
        )
    
    # ========== MÉTODOS AUXILIARES PARA EXTRAER INFORMACIÓN ==========
    
    def _extract_objective_from_criterion(self, criterion: str, parsed_story=None) -> str:
        """Extrae el objetivo del criterio usando contexto de la HU"""
        criterion_lower = criterion.lower()
        
        # Si tenemos contexto, usarlo para hacer el objetivo más específico
        if parsed_story and parsed_story.description:
            # Extraer palabras clave del contexto
            context_keywords = []
            if "botón" in parsed_story.description.lower() or "button" in parsed_story.description.lower():
                context_keywords.append("botón")
            if "modal" in parsed_story.description.lower() or "popup" in parsed_story.description.lower():
                context_keywords.append("modal")
            if "tabla" in parsed_story.description.lower() or "table" in parsed_story.description.lower():
                context_keywords.append("tabla")
            
            context_suffix = f" relacionado con {', '.join(context_keywords)}" if context_keywords else ""
        else:
            context_suffix = ""
        
        if "muestra" in criterion_lower or "visualiza" in criterion_lower or "aparece" in criterion_lower or "sale" in criterion_lower:
            return f"Validar que la información se muestra correctamente{context_suffix}"
        elif "abre" in criterion_lower or "abrir" in criterion_lower:
            return f"Validar que los recursos se abren correctamente{context_suffix}"
        elif "guarda" in criterion_lower or "almacena" in criterion_lower or "persiste" in criterion_lower:
            return f"Validar que los datos se guardan y persisten correctamente en el sistema{context_suffix}"
        elif "valida" in criterion_lower or "verifica" in criterion_lower:
            return f"Validar que las validaciones funcionan correctamente{context_suffix}"
        elif "copiar" in criterion_lower or "copy" in criterion_lower:
            return f"Validar que la funcionalidad de copiar funciona correctamente{context_suffix}"
        elif "crear" in criterion_lower or "crea" in criterion_lower:
            return f"Validar que la funcionalidad de crear funciona correctamente{context_suffix}"
        elif "seleccionar" in criterion_lower or "selecciona" in criterion_lower:
            return f"Validar que la funcionalidad de seleccionar funciona correctamente{context_suffix}"
        else:
            # Intentar extraer el verbo principal del criterio
            words = criterion.split()
            if len(words) > 0:
                first_verb = words[0] if words[0] else "ejecutar"
                return f"Validar que {first_verb.lower()} funciona correctamente según el criterio{context_suffix}"
            return f"Validar funcionalidad del sistema según el criterio{context_suffix}"
    
    def _generate_short_title(self, criterion: str, prefix: str = "") -> str:
        """Genera un título profesional siguiendo el patrón: 'Validar que [evento] [entidad] [condición] [resultado]'"""
        return self._generate_professional_title(criterion, prefix)
    
    def _generate_professional_title(self, criterion: str, prefix: str = "") -> str:
        """
        Genera un título profesional completo siguiendo el patrón QA Senior:
        "Validar que [evento o acción] [entidad] [condición específica] [resultado esperado observable]"
        
        REGLAS ABSOLUTAS:
        - NO truncar frases
        - NO resumir
        - NO cortar oraciones
        - Oración completa, cerrada y clara
        - Longitud objetivo: 120-180 caracteres
        - Si supera 180, REFORMULAR, no cortar
        - PROHIBIDO: prefijos como "Persistencia de datos:", "...", títulos genéricos
        """
        criterion_lower = criterion.lower()
        
        # PROHIBIR prefijos no permitidos
        if prefix and prefix.lower() in ["persistencia de datos", "estado vacío", "manejo de error", "recurso no disponible", 
                                         "usabilidad", "validación negativa", "elemento ui", "copia al portapapeles", 
                                         "estado deshabilitado", "manejo de errores"]:
            prefix = ""  # Ignorar prefijos prohibidos
        
        # Extraer componentes del criterio
        evento_accion = self._extract_evento_accion(criterion)
        entidad = self._extract_entidad(criterion)
        condicion = self._extract_condicion_clave(criterion)
        resultado = self._extract_resultado_esperado(criterion)
        
        # Construir título siguiendo el patrón obligatorio
        title_parts = ["Validar que"]
        
        # Agregar evento/acción
        if evento_accion:
            title_parts.append(evento_accion)
        
        # Agregar entidad
        if entidad:
            title_parts.append(entidad)
        
        # Agregar condición específica
        if condicion:
            title_parts.append(condicion)
        
        # Agregar resultado esperado observable
        if resultado:
            title_parts.append(resultado)
        
        # Si no se pudo extraer suficiente información, construir desde el criterio completo
        if len(title_parts) <= 1 or not any([evento_accion, entidad, resultado]):
            # Intentar construir desde el criterio completo de forma inteligente
            title = self._build_complete_title_from_criterion(criterion)
            if title and len(title) >= 50:  # Asegurar que tenga contenido suficiente
                return title
        
        # Unir las partes
        title = " ".join(title_parts)
        
        # Si el título es muy corto o incompleto, reformular desde el criterio
        if len(title) < 50 or title == "Validar que":
            title = self._build_complete_title_from_criterion(criterion)
        
        # Si el título supera 180 caracteres, REFORMULAR (no truncar)
        if len(title) > 180:
            title = self._reformulate_long_title(criterion, title)
        
        # Asegurar que termine con punto si es necesario y no tenga "..."
        title = title.rstrip("...").rstrip(".")
        if not title.endswith(".") and len(title) > 100:
            title += "."
        
        return title
    
    def _build_complete_title_from_criterion(self, criterion: str) -> str:
        """Construye un título completo desde el criterio sin truncar"""
        criterion_lower = criterion.lower()
        
        # Patrón 1: "Cuando X, Y"
        when_match = re.search(r'cuando\s+([^,\.]+?)(?:,\s*|\s+)([^\.]+)', criterion, re.IGNORECASE)
        if when_match:
            condition = when_match.group(1).strip()
            result = when_match.group(2).strip()
            title = f"Validar que cuando {condition}, {result}"
            if 120 <= len(title) <= 180:
                return title
        
        # Patrón 2: "Si X, Y"
        if_match = re.search(r'si\s+([^,\.]+?)(?:,\s*|\s+)([^\.]+)', criterion, re.IGNORECASE)
        if if_match:
            condition = if_match.group(1).strip()
            result = if_match.group(2).strip()
            title = f"Validar que si {condition}, {result}"
            if 120 <= len(title) <= 180:
                return title
        
        # Patrón 3: "Al [acción] [entidad] [condición], [resultado]"
        action_patterns = [
            (r'al\s+guardar\s+([^,\.]+?)(?:,\s*|\s+)([^\.]+)', "al guardar"),
            (r'al\s+crear\s+([^,\.]+?)(?:,\s*|\s+)([^\.]+)', "al crear"),
            (r'al\s+editar\s+([^,\.]+?)(?:,\s*|\s+)([^\.]+)', "al editar"),
            (r'al\s+cambiar\s+([^,\.]+?)(?:,\s*|\s+)([^\.]+)', "al cambiar"),
        ]
        
        for pattern, action in action_patterns:
            match = re.search(pattern, criterion, re.IGNORECASE)
            if match:
                entity = match.group(1).strip()
                result = match.group(2).strip()
                title = f"Validar que {action} {entity}, {result}"
                if 120 <= len(title) <= 180:
                    return title
        
        # Patrón 4: Construir desde el criterio completo de forma inteligente
        # Extraer las partes más importantes del criterio
        words = criterion.split()
        
        # Buscar verbos clave para construir la oración
        key_verbs = ["guarda", "toma", "muestra", "actualiza", "reasigna", "crea", "edita", "selecciona"]
        verb_found = None
        verb_index = -1
        
        for i, word in enumerate(words):
            if any(verb in word.lower() for verb in key_verbs):
                verb_found = word
                verb_index = i
                break
        
        if verb_found and verb_index > 0:
            # Construir título con contexto antes y después del verbo
            before_verb = " ".join(words[max(0, verb_index-3):verb_index])
            after_verb = " ".join(words[verb_index:min(len(words), verb_index+8)])
            title = f"Validar que {before_verb} {after_verb}"
            
            # Asegurar longitud adecuada
            if len(title) > 180:
                # Acortar la parte después del verbo
                after_verb = " ".join(words[verb_index:min(len(words), verb_index+5)])
                title = f"Validar que {before_verb} {after_verb}"
            
            if 50 <= len(title) <= 200:
                return title
        
        # Fallback: usar el criterio completo pero reformulado
        # Eliminar palabras muy comunes y construir oración completa
        important_words = [w for w in words if w.lower() not in ["el", "la", "los", "las", "de", "del", "en", "con", "por", "para", "un", "una"]]
        
        if len(important_words) > 5:
            # Tomar las primeras 12-15 palabras importantes
            selected_words = important_words[:15]
            title = f"Validar que {' '.join(selected_words)}"
            
            # Si aún es muy largo, reformular
            if len(title) > 180:
                title = self._reformulate_long_title(criterion, title)
            
            return title
        
        # Último fallback: usar el criterio directamente pero con "Validar que"
        title = f"Validar que {criterion}"
        if len(title) > 180:
            title = self._reformulate_long_title(criterion, title)
        
        return title
    
    def _reformulate_long_title(self, criterion: str, current_title: str) -> str:
        """Reformula un título largo sin truncar, manteniendo la estructura completa"""
        # Extraer los componentes clave del criterio
        evento_accion = self._extract_evento_accion(criterion)
        entidad = self._extract_entidad(criterion)
        condicion = self._extract_condicion_clave(criterion)
        resultado = self._extract_resultado_esperado(criterion)
        
        # Construir título más conciso pero completo
        parts = ["Validar que"]
        
        if evento_accion:
            # Acortar el evento/acción si es muy largo
            if len(evento_accion) > 30:
                # Simplificar manteniendo el sentido
                if "al cambiar" in evento_accion:
                    parts.append("al cambiar")
                elif "al crear" in evento_accion:
                    parts.append("al crear")
                elif "al guardar" in evento_accion:
                    parts.append("al guardar")
                else:
                    parts.append(evento_accion[:30])
            else:
                parts.append(evento_accion)
        
        if entidad:
            # Acortar la entidad si es muy larga
            if len(entidad) > 40:
                # Extraer solo el nombre principal
                if "campo de" in entidad:
                    field_match = re.search(r'campo\s+de\s+([^"\']+)', entidad)
                    if field_match:
                        parts.append(f"el campo de {field_match.group(1).strip()[:25]}")
                    else:
                        parts.append("el campo")
                else:
                    parts.append(entidad[:40])
            else:
                parts.append(entidad)
        
        if condicion:
            # Acortar condición si es muy larga
            if len(condicion) > 35:
                # Simplificar
                if "cuando el usuario tiene" in condicion:
                    parts.append("cuando se cumplan las condiciones especificadas")
                else:
                    parts.append(condicion[:35])
            else:
                parts.append(condicion)
        
        if resultado:
            # Acortar resultado si es muy largo
            if len(resultado) > 40:
                # Simplificar manteniendo el sentido
                if "se guarde" in resultado:
                    parts.append("se guarden los datos correctamente")
                elif "se muestre" in resultado:
                    parts.append("se muestre la información correctamente")
                elif "se actualice" in resultado or "se reasigne" in resultado:
                    parts.append("se actualice el valor correctamente")
                else:
                    parts.append(resultado[:40])
            else:
                parts.append(resultado)
        
        title = " ".join(parts)
        
        # Si aún es muy largo, usar una versión más concisa del criterio
        if len(title) > 180:
            # Extraer solo las palabras clave más importantes
            words = criterion.split()
            key_words = []
            skip_words = {"el", "la", "los", "las", "de", "del", "en", "con", "por", "para", "un", "una", "y", "o"}
            
            for word in words[:20]:  # Primeras 20 palabras
                if word.lower() not in skip_words and len(word) > 2:
                    key_words.append(word)
            
            title = f"Validar que {' '.join(key_words[:12])}"
        
        return title
    
    def _extract_evento_accion(self, criterion: str) -> str:
        """Extrae el evento o acción principal del criterio"""
        criterion_lower = criterion.lower()
        
        # Patrones comunes de eventos/acciones
        if "al cambiar" in criterion_lower or "cuando cambia" in criterion_lower:
            # Buscar qué cambia
            change_match = re.search(r'(?:al\s+cambiar|cuando\s+cambia)\s+([^\.\n]+?)(?:\s+de|\s+a|\s+por|$)', criterion, re.IGNORECASE)
            if change_match:
                what = change_match.group(1).strip()
                return f"al cambiar {what}"
        
        if "al crear" in criterion_lower or "cuando se crea" in criterion_lower:
            create_match = re.search(r'(?:al\s+crear|cuando\s+se\s+crea)\s+([^\.\n]+)', criterion, re.IGNORECASE)
            if create_match:
                what = create_match.group(1).strip()
                return f"al crear {what}"
        
        if "al editar" in criterion_lower or "cuando se edita" in criterion_lower:
            edit_match = re.search(r'(?:al\s+editar|cuando\s+se\s+edita)\s+([^\.\n]+)', criterion, re.IGNORECASE)
            if edit_match:
                what = edit_match.group(1).strip()
                return f"al editar {what}"
        
        if "al seleccionar" in criterion_lower or "cuando se selecciona" in criterion_lower:
            select_match = re.search(r'(?:al\s+seleccionar|cuando\s+se\s+selecciona)\s+([^\.\n]+)', criterion, re.IGNORECASE)
            if select_match:
                what = select_match.group(1).strip()
                return f"al seleccionar {what}"
        
        # Buscar verbos de acción directos
        action_verbs = {
            "guarda": "al guardar",
            "almacena": "al almacenar",
            "toma": "al tomar",
            "marca": "al marcar",
            "valida": "al validar",
            "muestra": "al mostrar",
            "visualiza": "al visualizar",
            "abre": "al abrir",
            "cierra": "al cerrar",
        }
        
        for verb, action in action_verbs.items():
            if verb in criterion_lower:
                return action
        
        return None
    
    def _extract_entidad(self, criterion: str) -> str:
        """Extrae la entidad afectada (frontera, campo, funcionalidad, etc.)"""
        criterion_lower = criterion.lower()
        
        # Buscar entidades específicas
        entities = {
            "frontera": "una frontera",
            "fronteras": "las fronteras",
            "campo": "el campo",
            "campos": "los campos",
            "grupo": "un grupo",
            "grupos": "los grupos",
            "sede": "una sede",
            "sedes": "las sedes",
            "métrica": "una métrica",
            "métricas": "las métricas",
            "planilla": "la planilla",
            "tabla": "la tabla",
            "botón": "el botón",
            "modal": "el modal",
            "pop-up": "el pop-up",
            "popup": "el popup",
        }
        
        for key, entity in entities.items():
            if key in criterion_lower:
                # Buscar nombre específico si existe
                if key == "campo":
                    field_match = re.search(r'campo\s+(?:de\s+)?["\']?([^"\'\n\.]+)["\']?', criterion, re.IGNORECASE)
                    if field_match:
                        field_name = field_match.group(1).strip()
                        return f"el campo de {field_name}"
                elif key == "botón":
                    button_match = re.search(r'botón\s+["\']?([^"\'\n\.]+)["\']?', criterion, re.IGNORECASE)
                    if button_match:
                        button_name = button_match.group(1).strip()
                        return f"el botón '{button_name}'"
                elif key == "frontera":
                    # Buscar tipo de frontera
                    if "embebida" in criterion_lower:
                        return "una frontera embebida"
                    elif "no embebida" in criterion_lower:
                        return "una frontera no embebida"
                
                return entity
        
        # Si no encuentra entidad específica, buscar en el contexto
        if "contract relationships" in criterion_lower or "contract rates" in criterion_lower:
            return "los datos en contract relationships"
        
        return None
    
    def _extract_condicion_clave(self, criterion: str) -> str:
        """Extrae la condición clave o cambio relevante"""
        criterion_lower = criterion.lower()
        
        # Buscar condiciones específicas
        if "de tipo" in criterion_lower:
            type_match = re.search(r'de\s+tipo\s+["\']?([^"\'\n\.]+)["\']?', criterion, re.IGNORECASE)
            if type_match:
                tipo = type_match.group(1).strip()
                return f"de tipo '{tipo}'"
        
        if "a tipo" in criterion_lower or "a Industrial" in criterion_lower or "a Residencial" in criterion_lower:
            type_match = re.search(r'a\s+tipo\s+["\']?([^"\'\n\.]+)["\']?', criterion, re.IGNORECASE)
            if type_match:
                tipo = type_match.group(1).strip()
                return f"a tipo '{tipo}'"
        
        if "con tipología embebida" in criterion_lower or "es embebida" in criterion_lower:
            return "con tipología embebida"
        
        if "con estrato previo" in criterion_lower:
            return "con estrato previo distinto"
        
        if "5 sedes" in criterion_lower or "cinco sedes" in criterion_lower:
            return "cuando el usuario tiene 5 o más sedes"
        
        if "menos de 5 sedes" in criterion_lower:
            return "cuando el usuario tiene menos de 5 sedes"
        
        if "no tiene grupos" in criterion_lower:
            return "cuando el usuario no tiene grupos creados"
        
        if "todas las sedes" in criterion_lower:
            return "cuando se seleccionan todas las sedes"
        
        return None
    
    def _extract_resultado_esperado(self, criterion: str) -> str:
        """Extrae el resultado esperado o comportamiento del sistema"""
        criterion_lower = criterion.lower()
        
        # Buscar resultados específicos
        if "guarda" in criterion_lower or "almacena" in criterion_lower:
            if "NT padre" in criterion_lower:
                return "se guarde el NT padre correctamente"
            elif "NT hijo" in criterion_lower:
                return "se guarde el NT hijo correctamente"
            return "se guarden los datos correctamente"
        
        if "toma" in criterion_lower:
            if "NT padre" in criterion_lower:
                return "se tome el NT padre desde contract relationships"
            elif "NT directo" in criterion_lower:
                return "se tome el NT directo"
            return "se tome el valor correcto"
        
        if "reasigne" in criterion_lower or "reasignación" in criterion_lower:
            if "estrato" in criterion_lower:
                return "se reasigne el estrato correctamente"
            return "se reasigne el valor correctamente"
        
        if "muestra" in criterion_lower or "aparece" in criterion_lower:
            if "botón" in criterion_lower:
                return "se muestre el botón correctamente"
            return "se muestre la información correctamente"
        
        if "no se muestra" in criterion_lower or "no aparece" in criterion_lower:
            return "no se muestre en la interfaz"
        
        if "se abre" in criterion_lower or "abre" in criterion_lower:
            if "pop-up" in criterion_lower or "modal" in criterion_lower:
                return "se abra el modal/pop-up correctamente"
            return "se abra el recurso correctamente"
        
        if "sigue igual" in criterion_lower or "mantiene" in criterion_lower:
            return "se mantenga el comportamiento actual"
        
        if "ya no existe" in criterion_lower or "no se guarda" in criterion_lower:
            return "no se persista en el sistema"
        
        return None
    
    def _build_title_from_criterion(self, criterion: str) -> str:
        """
        DEPRECADO: Usar _build_complete_title_from_criterion en su lugar.
        Mantenido por compatibilidad.
        """
        return self._build_complete_title_from_criterion(criterion)
    
    def _shorten_title_intelligently(self, title: str, max_length: int) -> str:
        """
        DEPRECADO: Este método ya no se usa.
        Los títulos ahora se reformulan completamente en lugar de truncarse.
        """
        # Este método ya no debería ser llamado, pero lo mantenemos por compatibilidad
        # Si se llama, reformular en lugar de truncar
        return self._reformulate_long_title("", title)
    
    def _extract_specific_element(self, criterion: str) -> str:
        """Extrae el elemento específico mencionado en el criterio"""
        criterion_lower = criterion.lower()
        
        # Buscar campos específicos
        field_match = re.search(r'campo\s+(?:de\s+)?["\']?([^"\'\n\.]+)["\']?', criterion_lower)
        if field_match:
            return f"campo '{field_match.group(1).strip()[:30]}'"
        
        # Buscar botones específicos
        button_match = re.search(r'botón\s+["\']?([^"\'\n\.]+)["\']?', criterion_lower)
        if button_match:
            return f"botón '{button_match.group(1).strip()[:30]}'"
        
        # Buscar elementos UI
        if "modal" in criterion_lower or "popup" in criterion_lower or "pop-up" in criterion_lower:
            return "modal/pop-up"
        if "tabla" in criterion_lower:
            return "tabla"
        if "grupo" in criterion_lower:
            return "grupo"
        if "sede" in criterion_lower or "sedes" in criterion_lower:
            return "sedes"
        if "métrica" in criterion_lower or "métricas" in criterion_lower:
            return "métricas"
        if "planilla" in criterion_lower:
            return "planilla"
        
        return None
    
    def _extract_specific_action(self, criterion: str) -> str:
        """Extrae la acción específica del criterio"""
        criterion_lower = criterion.lower()
        
        # Mapeo de acciones a verbos en infinitivo
        action_map = {
            "muestra": "visualización de",
            "visualiza": "visualización de",
            "aparece": "aparición de",
            "sale": "aparición de",
            "crear": "creación de",
            "crea": "creación de",
            "guarda": "guardado de",
            "almacena": "almacenamiento de",
            "persiste": "persistencia de",
            "valida": "validación de",
            "verifica": "verificación de",
            "seleccionar": "selección de",
            "selecciona": "selección de",
            "abre": "apertura de",
            "abrir": "apertura de",
            "descarga": "descarga de",
            "descargar": "descarga de",
            "sube": "subida de",
            "subir": "subida de",
            "copia": "copia de",
            "copiar": "copia de",
            "edita": "edición de",
            "editar": "edición de",
            "elimina": "eliminación de",
            "eliminar": "eliminación de",
        }
        
        for key, value in action_map.items():
            if key in criterion_lower:
                return value
        
        return None
    
    def _generate_contextual_title(self, criterion: str, parsed_story=None) -> str:
        """Genera un título profesional usando el contexto de la HU"""
        # Usar el método profesional que ya implementa el patrón correcto
        title = self._generate_professional_title(criterion)
        
        # Si hay contexto de la HU, intentar enriquecer el título
        if parsed_story and parsed_story.title:
            # El título ya debería ser específico, pero podemos verificar si necesita más contexto
            if len(title) < 50:  # Si el título es muy corto, podría necesitar más contexto
                # Intentar agregar contexto sin hacer el título genérico
                pass  # Por ahora mantenemos el título generado
        
        return title
    
    def _extract_main_action(self, criterion: str) -> str:
        """Extrae la acción principal del criterio (retorna solo el verbo, sin 'Validar')"""
        criterion_lower = criterion.lower()
        
        action_map = {
            "muestra": "visualización de",
            "visualiza": "visualización de",
            "aparece": "aparición de",
            "sale": "aparición de",
            "crea": "creación de",
            "crear": "creación de",
            "guarda": "guardado de",
            "almacena": "almacenamiento de",
            "valida": "validación de",
            "verifica": "verificación de",
            "selecciona": "selección de",
            "seleccionar": "selección de",
            "abre": "apertura de",
            "abrir": "apertura de",
        }
        
        for key, value in action_map.items():
            if key in criterion_lower:
                return value
        
        return None
    
    def _generate_specific_preconditions(self, criterion: str) -> List[str]:
        """Genera precondiciones específicas basadas en el criterio"""
        preconditions = [
            "El sistema está operativo y accesible",
            "El usuario tiene los permisos necesarios"
        ]
        
        criterion_lower = criterion.lower()
        
        if "tabla" in criterion_lower:
            preconditions.append("Debe existir al menos un registro en la tabla")
        if "modal" in criterion_lower or "abre" in criterion_lower:
            preconditions.append("El recurso (PDF/XML) debe estar disponible en el backend")
        if "vacío" in criterion_lower or "empty" in criterion_lower:
            preconditions.append("No deben existir datos asociados")
        
        return preconditions
    
    def _generate_contextual_preconditions(self, criterion: str, parsed_story=None) -> List[str]:
        """Genera precondiciones específicas usando contexto de la HU"""
        preconditions = []
        criterion_lower = criterion.lower()
        
        # Precondiciones base
        preconditions.append("El sistema está operativo y accesible")
        
        # Extraer precondiciones del contexto de la HU
        if parsed_story:
            # Si hay contexto, extraer información relevante
            if parsed_story.context:
                # Buscar condiciones específicas en el contexto
                if "usuario" in parsed_story.context.lower():
                    preconditions.append("El usuario está autenticado y tiene acceso al sistema")
                if "datos" in parsed_story.context.lower() or "data" in parsed_story.context.lower():
                    preconditions.append("Los datos de prueba están disponibles")
            
            # Usar estados extraídos
            if parsed_story.states:
                for state in parsed_story.states[:2]:  # Primeros 2 estados
                    if "onboarding" in state.lower():
                        preconditions.append("El usuario no ha completado el onboarding")
                    elif "configuración" in state.lower():
                        preconditions.append("El usuario está en el proceso de configuración")
        else:
            preconditions.append("El usuario tiene los permisos necesarios")
        
        # Precondiciones específicas del criterio
        if "5 sedes" in criterion_lower or "sedes" in criterion_lower:
            preconditions.append("El usuario tiene 5 o más sedes configuradas")
        if "grupos" in criterion_lower:
            if "no tiene grupos" in criterion_lower or "sin grupos" in criterion_lower:
                preconditions.append("El usuario no tiene grupos creados")
            else:
                preconditions.append("El usuario tiene grupos configurados")
        if "todas las sedes" in criterion_lower or "todas sedes" in criterion_lower:
            preconditions.append("El usuario tiene 'Todas' las sedes seleccionadas")
        if "botón" in criterion_lower or "button" in criterion_lower:
            preconditions.append("El botón debe estar visible en la interfaz")
        if "modal" in criterion_lower or "popup" in criterion_lower or "pop-up" in criterion_lower:
            preconditions.append("El modal/popup debe poder abrirse")
        if "tabla" in criterion_lower:
            preconditions.append("Debe existir al menos un registro en la tabla")
        if "vacío" in criterion_lower or "empty" in criterion_lower or "no hay" in criterion_lower:
            preconditions.append("No deben existir datos asociados")
        
        # Si no hay precondiciones específicas, agregar genéricas
        if len(preconditions) < 2:
            preconditions.append("El usuario tiene los permisos necesarios")
            preconditions.append("Los datos de prueba están disponibles")
        
        return preconditions
    
    def _generate_specific_steps(self, criterion: str, case_type: str) -> List[str]:
        """Genera pasos específicos basados en el criterio y tipo de caso"""
        criterion_lower = criterion.lower()
        
        if case_type == "happy_path":
            if "muestra" in criterion_lower or "visualiza" in criterion_lower:
                return [
                    "Given que el usuario accede al módulo",
                    "When el sistema carga los datos",
                    "Then la información se muestra correctamente",
                    "And todos los elementos están visibles y funcionales"
                ]
            elif "abre" in criterion_lower:
                return [
                    "Given que el usuario accede al módulo",
                    "When el usuario hace clic en el elemento clicable",
                    "Then se abre el modal visor con el recurso",
                    "And el recurso se muestra correctamente"
                ]
        
        return [
            "Given que el usuario accede al módulo",
            "When el usuario ejecuta la acción correspondiente",
            "Then el sistema responde correctamente"
        ]
    
    def _generate_contextual_steps(self, criterion: str, case_type: str, parsed_story=None) -> List[str]:
        """Genera pasos específicos usando contexto de la HU y flujos extraídos"""
        steps = []
        criterion_lower = criterion.lower()
        
        # Given: usar contexto de la HU
        if parsed_story and parsed_story.context:
            # Extraer información del contexto
            if "análisis" in parsed_story.context.lower() or "análisis" in criterion_lower:
                steps.append("Given que el usuario está en la sección 'Análisis'")
            else:
                steps.append("Given que el usuario accede al módulo correspondiente")
        else:
            steps.append("Given que el usuario accede al módulo correspondiente")
        
        # When: extraer acción específica del criterio
        action_step = self._extract_action_step_from_criterion(criterion, parsed_story)
        steps.append(f"When {action_step}")
        
        # And: pasos adicionales basados en el criterio
        additional_steps = self._extract_additional_steps_from_criterion(criterion, parsed_story)
        steps.extend(additional_steps)
        
        # Then: resultado esperado específico
        result_step = self._extract_result_step_from_criterion(criterion, parsed_story)
        steps.append(f"Then {result_step}")
        
        return steps
    
    def _extract_action_step_from_criterion(self, criterion: str, parsed_story=None) -> str:
        """Extrae el paso de acción del criterio"""
        criterion_lower = criterion.lower()
        
        # Buscar acciones específicas
        if "al darle" in criterion_lower or "al dar" in criterion_lower:
            # Extraer qué acción se hace
            action_match = re.search(r'al\s+darle?\s+["\']?([^"\'\n\.]+)["\']?', criterion, re.IGNORECASE)
            if action_match:
                action = action_match.group(1).strip()
                return f"el usuario hace clic en '{action}'"
        
        if "crear" in criterion_lower or "crea" in criterion_lower:
            if "grupo" in criterion_lower:
                return "el usuario hace clic en el botón 'Crear Grupo'"
            return "el usuario inicia el proceso de creación"
        
        if "seleccionar" in criterion_lower or "selecciona" in criterion_lower:
            # Buscar qué se selecciona
            select_match = re.search(r'seleccionar\s+([^\.\n]+)', criterion_lower)
            if select_match:
                what = select_match.group(1).strip()[:40]
                return f"el usuario selecciona {what}"
            return "el usuario realiza una selección"
        
        if "muestra" in criterion_lower or "aparece" in criterion_lower or "sale" in criterion_lower:
            if "botón" in criterion_lower:
                return "el sistema evalúa las condiciones para mostrar el botón"
            return "el sistema carga y procesa la información"
        
        if "abre" in criterion_lower or "abrir" in criterion_lower:
            return "el usuario hace clic en el elemento para abrir"
        
        # Usar flujos de la HU si están disponibles
        if parsed_story and parsed_story.user_flows:
            # Buscar flujo relevante
            for flow in parsed_story.user_flows:
                if any(word in flow.lower() for word in criterion_lower.split()[:3]):
                    # Extraer acción del flujo
                    flow_lower = flow.lower()
                    if "darle" in flow_lower or "dar" in flow_lower:
                        return f"el usuario {flow[:60]}"
        
        return "el usuario ejecuta la acción correspondiente"
    
    def _extract_additional_steps_from_criterion(self, criterion: str, parsed_story=None) -> List[str]:
        """Extrae pasos adicionales del criterio"""
        additional = []
        criterion_lower = criterion.lower()
        
        # Buscar condiciones específicas
        if "si el usuario" in criterion_lower or "cuando el usuario" in criterion_lower:
            # Extraer condición
            condition_match = re.search(r'(?:si|cuando)\s+el\s+usuario\s+([^\.]+)', criterion_lower)
            if condition_match:
                condition = condition_match.group(1).strip()
                additional.append(f"And el usuario {condition}")
        
        if "5 sedes" in criterion_lower:
            additional.append("And el usuario tiene 5 o más sedes configuradas")
        if "no tiene grupos" in criterion_lower:
            additional.append("And el usuario no tiene grupos creados")
        if "todas las sedes" in criterion_lower:
            additional.append("And el usuario tiene 'Todas' las sedes seleccionadas")
        
        return additional
    
    def _extract_result_step_from_criterion(self, criterion: str, parsed_story=None) -> str:
        """Extrae el resultado esperado del criterio"""
        criterion_lower = criterion.lower()
        
        # Buscar resultados específicos
        if "muestra" in criterion_lower or "aparece" in criterion_lower or "sale" in criterion_lower:
            if "botón" in criterion_lower:
                # Buscar nombre del botón
                button_match = re.search(r'(?:botón|button)[:\s]*["\']?([^"\'\n\.]+)["\']?', criterion, re.IGNORECASE)
                if button_match:
                    button_name = button_match.group(1).strip()
                    return f"el botón '{button_name}' se muestra correctamente"
                return "el botón se muestra según las condiciones especificadas"
            return "la información se muestra correctamente"
        
        if "abre" in criterion_lower or "abrir" in criterion_lower:
            if "pop-up" in criterion_lower or "popup" in criterion_lower or "modal" in criterion_lower:
                return "se abre el modal/pop-up correctamente"
            return "se abre el recurso correctamente"
        
        if "crear" in criterion_lower or "crea" in criterion_lower:
            if "grupo" in criterion_lower:
                return "se abre el pop-up de creación de grupo sin sedes pre-seleccionadas"
            return "se completa el proceso de creación correctamente"
        
        if "seleccionar" in criterion_lower or "selecciona" in criterion_lower:
            return "la selección se realiza correctamente"
        
        # Usar el criterio directamente si es descriptivo
        if len(criterion) < 100:
            return f"el sistema cumple con: {criterion[:80]}"
        
        return "el sistema responde correctamente según el criterio"
    
    def _generate_specific_expected_result(self, criterion: str, case_type: str) -> str:
        """Genera resultado esperado específico"""
        criterion_lower = criterion.lower()
        
        if case_type == "happy_path":
            if "muestra" in criterion_lower:
                return "La información se muestra correctamente, todos los campos son visibles y no hay errores de visualización"
            elif "abre" in criterion_lower:
                return "El modal se abre correctamente, el recurso se carga y se muestra apropiadamente"
            elif "guarda" in criterion_lower:
                return "Los datos se guardan correctamente y se muestra confirmación exitosa"
        
        return "El sistema cumple con el criterio especificado"
    
    def _generate_contextual_expected_result(self, criterion: str, case_type: str, parsed_story=None) -> str:
        """Genera resultado esperado específico usando contexto de la HU"""
        criterion_lower = criterion.lower()
        
        # Construir resultado basado en el criterio específico
        result_parts = []
        
        # Extraer resultado específico del criterio
        if "muestra" in criterion_lower or "aparece" in criterion_lower or "sale" in criterion_lower:
            if "botón" in criterion_lower:
                button_match = re.search(r'(?:botón|button)[:\s]*["\']?([^"\'\n\.]+)["\']?', criterion, re.IGNORECASE)
                if button_match:
                    button_name = button_match.group(1).strip()
                    result_parts.append(f"El botón '{button_name}' se muestra correctamente")
                else:
                    result_parts.append("El botón se muestra según las condiciones especificadas")
                
                # Agregar condiciones específicas
                if "5 sedes" in criterion_lower:
                    result_parts.append("solo si el usuario tiene 5 o más sedes")
                if "no tiene grupos" in criterion_lower:
                    result_parts.append("solo si el usuario no tiene grupos creados")
                if "todas las sedes" in criterion_lower:
                    result_parts.append("solo si el usuario tiene 'Todas' las sedes seleccionadas")
            else:
                result_parts.append("La información se muestra correctamente")
        
        elif "abre" in criterion_lower or "abrir" in criterion_lower:
            if "pop-up" in criterion_lower or "popup" in criterion_lower or "modal" in criterion_lower:
                if "crear grupo" in criterion_lower:
                    result_parts.append("Se abre el pop-up de creación de grupo")
                    result_parts.append("sin ninguna sede pre-seleccionada")
                else:
                    result_parts.append("Se abre el modal/pop-up correctamente")
            else:
                result_parts.append("Se abre el recurso correctamente")
        
        elif "crear" in criterion_lower or "crea" in criterion_lower:
            if "grupo" in criterion_lower:
                result_parts.append("Se crea el grupo correctamente")
                if "pre-selecciona" in criterion_lower or "pre selecciona" in criterion_lower:
                    result_parts.append("y se pre-selecciona en el breadcrumb de las sedes")
            else:
                result_parts.append("Se completa el proceso de creación correctamente")
        
        elif "seleccionar" in criterion_lower or "selecciona" in criterion_lower:
            result_parts.append("La selección se realiza correctamente")
            if "sedes" in criterion_lower:
                result_parts.append("y las sedes seleccionadas se reflejan en la interfaz")
        
        elif "no se muestra" in criterion_lower or "no muestra" in criterion_lower:
            if "menos de 5 sedes" in criterion_lower:
                result_parts.append("El botón NO se muestra si el usuario tiene menos de 5 sedes")
            if "grupos creados" in criterion_lower:
                result_parts.append("El botón NO se muestra si el usuario ya tiene grupos creados")
        
        # Si no hay resultado específico, usar el criterio directamente
        if not result_parts:
            # Usar el criterio pero hacerlo más específico
            if len(criterion) < 150:
                result_parts.append(f"El sistema cumple con: {criterion}")
            else:
                # Extraer parte clave del criterio
                words = criterion.split()[:15]
                result_parts.append(f"El sistema cumple con: {' '.join(words)}...")
        
        # Agregar validaciones adicionales
        if case_type == "happy_path":
            result_parts.append("No se presentan errores en el proceso")
            result_parts.append("La interfaz responde correctamente")
        
        return ". ".join(result_parts) + "."
    
    def _extract_action_from_criterion(self, criterion: str) -> str:
        """Extrae la acción principal del criterio"""
        criterion_lower = criterion.lower()
        
        if "muestra" in criterion_lower:
            return "mostrar la información"
        elif "abre" in criterion_lower:
            return "abrir el recurso"
        elif "guarda" in criterion_lower:
            return "guardar los datos"
        elif "valida" in criterion_lower:
            return "validar los datos"
        else:
            return "ejecutar la acción"
    
    def _extract_ui_element_from_criterion(self, criterion: str) -> str:
        """Extrae el elemento UI mencionado en el criterio"""
        criterion_lower = criterion.lower()
        
        if "botón" in criterion_lower or "button" in criterion_lower:
            return "botón"
        elif "tabla" in criterion_lower or "table" in criterion_lower:
            return "tabla"
        elif "modal" in criterion_lower:
            return "modal"
        elif "badge" in criterion_lower or "chip" in criterion_lower:
            return "badge/chip"
        elif "tooltip" in criterion_lower:
            return "tooltip"
        else:
            return "elemento UI"
    
    def _generate_functional_test(self, criterion: str, test_number: int, project_name: str) -> TestCase:
        """Genera un caso de prueba funcional inteligente basado en un criterio"""
        
        # Título: el criterio completo (sin ID, Linear lo agrega)
        title = criterion
        
        # Precondiciones estándar profesionales
        preconditions = [
            "El sistema está operativo y accesible",
            "El usuario tiene los permisos necesarios",
            "Los datos de prueba están disponibles y configurados"
        ]
        
        # Generar pasos Gherkin inteligentes basados en el criterio
        steps = self._generate_gherkin_steps(criterion)
        
        # Resultado esperado más específico
        expected_result = self._generate_smart_expected_result(criterion)
        
        return TestCase(
            id=f"TC-{test_number:03d}",
            title=title,
            criterion=criterion,
            test_type=TestType.FUNCIONAL,
            priority=TestPriority.ALTA,
            preconditions=preconditions,
            steps=steps,
            expected_result=expected_result
        )
    
    def _generate_gherkin_steps(self, criterion: str) -> List[str]:
        """
        Genera pasos en formato Gherkin basados en el criterio
        Analiza el criterio para crear pasos específicos
        """
        criterion_lower = criterion.lower()
        
        # Given (contexto/precondición)
        given = "Given que el sistema está operativo y el usuario tiene acceso al módulo"
        
        # When (acción principal) - intentar extraer la acción del criterio
        when_action = "el usuario accede al módulo correspondiente"
        
        # Detectar acciones específicas
        if "visualiza" in criterion_lower or "muestra" in criterion_lower:
            when_action = "el usuario accede a la sección para visualizar"
        elif "crea" in criterion_lower or "crear" in criterion_lower:
            when_action = "el usuario inicia el proceso de creación"
        elif "edita" in criterion_lower or "modifica" in criterion_lower:
            when_action = "el usuario selecciona el elemento a editar"
        elif "guarda" in criterion_lower or "almacena" in criterion_lower:
            when_action = "el usuario ejecuta la acción de guardar"
        elif "valida" in criterion_lower or "verifica" in criterion_lower:
            when_action = "el usuario ejecuta la validación"
        elif "bloquea" in criterion_lower or "deshabilita" in criterion_lower:
            when_action = "el usuario intenta acceder a la función bloqueada"
        
        # Then (resultado esperado) - basado en el criterio
        then_result = "el sistema muestra el resultado correcto"
        
        if "guarda" in criterion_lower or "almacena" in criterion_lower:
            then_result = "el sistema guarda correctamente y confirma la operación"
        elif "muestra" in criterion_lower or "visualiza" in criterion_lower:
            then_result = "el sistema muestra la información correctamente"
        elif "valida" in criterion_lower:
            then_result = "el sistema valida y muestra feedback apropiado"
        elif "bloquea" in criterion_lower or "no permite" in criterion_lower:
            then_result = "el sistema bloquea la acción e informa al usuario"
        
        # Construir pasos Gherkin
        steps = [
            given,
            f"When {when_action}",
            "And configura el escenario de prueba con los datos disponibles",
            f"And ejecuta la acción para {self._extract_action_verb(criterion)}",
            f"Then {then_result}"
        ]
        
        return steps
    
    def _extract_action_verb(self, criterion: str) -> str:
        """Extrae el verbo de acción del criterio"""
        criterion_lower = criterion.lower()
        
        # Buscar verbos clave
        if "visualiza" in criterion_lower or "muestra" in criterion_lower:
            return "visualizar"
        elif "crea" in criterion_lower or "crear" in criterion_lower:
            return "crear"
        elif "edita" in criterion_lower or "modifica" in criterion_lower:
            return "editar"
        elif "guarda" in criterion_lower:
            return "guardar"
        elif "valida" in criterion_lower:
            return "validar"
        elif "bloquea" in criterion_lower:
            return "bloquear"
        else:
            return "ejecutar la acción especificada"
    
    def _generate_smart_expected_result(self, criterion: str) -> str:
        """
        Genera un resultado esperado inteligente y específico
        No solo repite el criterio, sino que explica QUÉ se debe validar
        """
        criterion_lower = criterion.lower()
        base_result = f"El sistema debe cumplir con el criterio: {criterion}."
        
        # Agregar validaciones específicas según el tipo de criterio
        validations = []
        
        if "visualiza" in criterion_lower or "muestra" in criterion_lower:
            validations.append("Todos los campos deben ser visibles")
            validations.append("la información debe mostrarse correctamente formateada")
            validations.append("no deben presentarse errores de visualización")
        
        if "tabla" in criterion_lower:
            validations.append("el estado de edición debe reflejarse correctamente")
        
        if "guarda" in criterion_lower or "almacena" in criterion_lower:
            validations.append("Los datos deben persistir correctamente en el sistema")
            validations.append("debe mostrarse confirmación exitosa")
        
        if "valida" in criterion_lower:
            validations.append("Las validaciones deben ejecutarse correctamente")
            validations.append("debe mostrarse feedback claro")
        
        if "bloquea" in criterion_lower or "no permite" in criterion_lower:
            validations.append("La acción debe estar bloqueada")
            validations.append("debe mostrarse un mensaje informativo al usuario")
        
        if "crea" in criterion_lower:
            validations.append("El elemento debe crearse correctamente")
            validations.append("debe aparecer en el sistema")
        
        # Si no hay validaciones específicas, usar genéricas
        if not validations:
            validations = [
                "El comportamiento debe ser el esperado",
                "no deben presentarse errores"
            ]
        
        # Construir resultado esperado completo
        if validations:
            validation_text = ", ".join(validations)
            return f"{base_result}\n{validation_text.capitalize()}."
        else:
            return base_result
    
    def _generate_negative_test(self, test_number: int, project_name: str) -> TestCase:
        """Genera un caso de prueba negativo"""
        
        title = "Validación de manejo de errores y casos no contemplados"
        criterion = "El sistema debe manejar correctamente errores, datos inválidos y casos no contemplados, mostrando mensajes apropiados"
        
        preconditions = [
            "El sistema está operativo",
            "Se tienen datos inválidos preparados para la prueba"
        ]
        
        steps = [
            "Acceder al sistema",
            "Ingresar datos inválidos o fuera del rango esperado",
            "Intentar realizar acciones sin cumplir las precondiciones necesarias",
            "Verificar que el sistema maneja los errores apropiadamente"
        ]
        
        expected_result = "El sistema debe mostrar mensajes de error claros y mantener la estabilidad sin fallos inesperados"
        
        return TestCase(
            id=f"TC-{test_number:03d}",
            title=title,
            criterion=criterion,
            test_type=TestType.NEGATIVO,
            priority=TestPriority.MEDIA,
            preconditions=preconditions,
            steps=steps,
            expected_result=expected_result
        )
    
    def _extract_action(self, criterion: str) -> str:
        """Extrae la acción principal de un criterio"""
        # Buscar verbos clave
        verbs = ['guarda', 'toma', 'marca', 'valida', 'permite', 'asegura']
        
        for verb in verbs:
            if verb in criterion.lower():
                # Extraer la frase alrededor del verbo
                parts = criterion.lower().split(verb)
                if len(parts) > 1:
                    return f"{verb} {parts[1][:50]}..."
        
        # Si no encuentra verbo, retornar primeras palabras
        return criterion[:60] + "..."


# Test
if __name__ == "__main__":
    test_hu = """
    Contexto BACK I Ajustar el insumo del campo de NT en CR cuando una frontera es embebida
    
    Cuando una frontera llega con tipología embebida, hoy el sistema guarda en contract rates el NT del hijo y luego lo reemplaza por el del padre.
    
    Descripción
    Como sistema facturación, quiero que cuando llegue una frontera con tipología embebida, se guarde el NT padre en contract relationships.
    
    Criterios de aceptación
    Cuando la frontera es embebida, contract relationships guarda el NT padre.
    Para fronteras embebidas, contract rates.NT toma únicamente el NT padre desde contract relationships.
    Para fronteras no embebidas, el flujo sigue igual (toma el NT directo).
    El campo embedded_tension_child ya no existe ni se guarda NT hijo en Bills.
    """
    
    generator = ProfessionalQAGenerator()
    test_cases = generator.generate_test_cases(test_hu, "Test Project")
    
    print("\n=== CASOS DE PRUEBA GENERADOS ===\n")
    for tc in test_cases:
        print(f"{tc.id}. {tc.title}")
        print(f"   Tipo: {tc.test_type.value} | Prioridad: {tc.priority.value}")
        print()

