#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema Web para QA - Frontend de Generación de Casos de Prueba
Aplicación web completa para equipos QA
"""

import sys
import os
import io

# Configurar encoding UTF-8 para Windows (soluciona error 'charmap' codec)
if sys.platform == 'win32':
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

from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
import json
import pandas as pd
from datetime import datetime
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'exporters'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'generators'))

from test_case_automation import UserStoryParser, TestCaseGenerator, QAValidator, TestCaseExporter
from test_templates import TemplateManager
from linear_simple_exporter import LinearSimpleExporter
from gherkin_generator import GherkinGenerator, GherkinTestCase
from enhanced_gherkin_generator import EnhancedGherkinGenerator, EnhancedGherkinTestCase
from linear_api_client import LinearAPIClient

app = Flask(__name__, 
           template_folder='templates',
           static_folder='static')
app.secret_key = 'qa_automation_secret_key_2024'

# Configuración global
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'

# Crear directorios si no existen
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

class QAProject:
    """Clase para manejar proyectos de QA - Sistema local con JSON"""
    
    def __init__(self):
        self.projects = {}
        self.load_projects()
    
    def load_projects(self):
        """Carga proyectos desde archivo JSON local"""
        try:
            json_path = os.path.abspath('qa_projects.json')
            if os.path.exists(json_path) and os.path.isfile(json_path):
                with open(json_path, 'r', encoding='utf-8', errors='replace') as f:
                    self.projects = json.load(f)
                print(f"[INFO] {len(self.projects)} proyectos cargados desde JSON local", flush=True)
        except (OSError, IOError, PermissionError, json.JSONDecodeError) as e:
            print(f"[WARN] Error cargando proyectos: {e}", flush=True)
            self.projects = {}
        except Exception as e:
            print(f"[WARN] Error inesperado cargando proyectos: {e}", flush=True)
            self.projects = {}
    
    def save_projects(self):
        """Guarda proyectos en archivo JSON local"""
        try:
            # Obtener ruta absoluta y normalizar
            json_path = os.path.abspath('qa_projects.json')
            # Asegurar que el directorio existe
            os.makedirs(os.path.dirname(json_path) if os.path.dirname(json_path) else '.', exist_ok=True)
            
            # Escribir archivo con manejo robusto de errores
            with open(json_path, 'w', encoding='utf-8', errors='replace') as f:
                json.dump(self.projects, f, indent=2, ensure_ascii=False, default=str)
        except (OSError, IOError, PermissionError) as e:
            print(f"[ERROR] Error guardando proyectos: {e}", flush=True)
            # Intentar con ruta alternativa si falla
            try:
                alt_path = os.path.join(os.path.expanduser('~'), 'qa_projects_backup.json')
                with open(alt_path, 'w', encoding='utf-8', errors='replace') as f:
                    json.dump(self.projects, f, indent=2, ensure_ascii=False, default=str)
                print(f"[WARN] Proyectos guardados en ubicación alternativa: {alt_path}", flush=True)
            except:
                pass
        except Exception as e:
            print(f"[ERROR] Error inesperado guardando proyectos: {e}", flush=True)
    
    def create_project(self, name, description, user_story, qa_comments="", linear_hu_id=""):
        """Crea un nuevo proyecto y lo guarda localmente"""
        project_id = f"proj_{len(self.projects) + 1}_{int(datetime.now().timestamp())}"
        
        project = {
            'id': project_id,
            'name': name,
            'description': description,
            'user_story': user_story,
            'qa_comments': qa_comments,
            'linear_hu_id': linear_hu_id,
            'created_at': datetime.now().isoformat(),
            'status': 'draft',
            'test_cases': [],
            'validation_result': None,
            'template_used': None
        }
        
        self.projects[project_id] = project
        self.save_projects()
        return project_id
    
    def update_project(self, project_id, **kwargs):
        """Actualiza un proyecto localmente"""
        if project_id in self.projects:
            self.projects[project_id].update(kwargs)
            self.save_projects()
            return True
        return False
    
    def get_project(self, project_id):
        """Obtiene un proyecto del diccionario local"""
        return self.projects.get(project_id)
    
    def list_projects(self):
        """Lista todos los proyectos locales"""
        return list(self.projects.values())
    
    def delete_project(self, project_id):
        """Elimina un proyecto"""
        if project_id in self.projects:
            del self.projects[project_id]
            self.save_projects()
            return True
        return False
    
    def delete_test_case(self, project_id, test_case_id):
        """Elimina un caso de prueba específico de un proyecto"""
        if project_id in self.projects:
            project = self.projects[project_id]
            test_cases = project.get('test_cases', [])
            
            # Filtrar el caso a eliminar
            updated_cases = []
            for case in test_cases:
                case_id = case.get('id') if isinstance(case, dict) else getattr(case, 'id', None)
                if case_id != test_case_id:
                    updated_cases.append(case)
            
            project['test_cases'] = updated_cases
            self.save_projects()
            return True
        return False
    
    def update_test_case(self, project_id, test_case_id, updated_data):
        """Actualiza un caso de prueba específico"""
        if project_id in self.projects:
            project = self.projects[project_id]
            test_cases = project.get('test_cases', [])
            
            for i, case in enumerate(test_cases):
                case_id = case.get('id') if isinstance(case, dict) else getattr(case, 'id', None)
                
                if case_id == test_case_id:
                    # Actualizar campos del caso de prueba
                    if isinstance(case, dict):
                        case.update(updated_data)
                    else:
                        # Si es un objeto, actualizarlo campo por campo
                        for key, value in updated_data.items():
                            if hasattr(case, key):
                                setattr(case, key, value)
                    
                    test_cases[i] = case
                    project['test_cases'] = test_cases
                    self.save_projects()
                    return True
            
        return False

# Instancia global del gestor de proyectos
qa_manager = QAProject()

@app.route('/')
def index():
    """Página principal"""
    projects = qa_manager.list_projects()
    return render_template('index.html', projects=projects)

@app.route('/new_project')
def new_project():
    """Página para crear nuevo proyecto"""
    return render_template('new_project.html')

@app.route('/create_project', methods=['POST'])
def create_project():
    """Crea un nuevo proyecto"""
    try:
        # Intentar obtener datos de JSON primero, luego de formulario
        if request.is_json:
            data = request.get_json()
            name = data.get('name', '').strip()
            description = data.get('description', '').strip()
            user_story = data.get('user_story', '').strip()
            qa_comments = data.get('qa_comments', '').strip()
            linear_hu_id = data.get('linear_hu_id', '').strip()
        else:
            name = request.form.get('name', '').strip()
            description = request.form.get('description', '').strip()
            user_story = request.form.get('user_story', '').strip()
            qa_comments = request.form.get('qa_comments', '').strip()
            linear_hu_id = request.form.get('linear_hu_id', '').strip()
        
        if not name or not user_story:
            return jsonify({'error': 'Nombre y historia de usuario son requeridos'}), 400
        
        project_id = qa_manager.create_project(name, description, user_story, qa_comments, linear_hu_id)
        
        return jsonify({
            'success': True,
            'project_id': project_id,
            'redirect_url': url_for('project_detail', project_id=project_id)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/project/<project_id>')
def project_detail(project_id):
    """Detalle del proyecto"""
    project = qa_manager.get_project(project_id)
    if not project:
        return redirect(url_for('index'))
    
    return render_template('project_detail.html', project=project)

@app.route('/update_project/<project_id>', methods=['POST'])
def update_project_route(project_id):
    """Actualiza campos del proyecto (como linear_hu_id)"""
    try:
        data = request.get_json()
        
        project = qa_manager.get_project(project_id)
        if not project:
            return jsonify({'error': 'Proyecto no encontrado'}), 404
        
        # Actualizar linear_hu_id si se proporciona
        if 'linear_hu_id' in data:
            linear_hu_id = data['linear_hu_id'].strip()
            if not linear_hu_id:
                return jsonify({'error': 'HU ID no puede estar vacío'}), 400
            
            qa_manager.update_project(project_id, linear_hu_id=linear_hu_id)
            print(f"[OK] HU ID actualizado para proyecto {project_id}: {linear_hu_id}")
            
            return jsonify({
                'success': True,
                'message': f'HU ID actualizado: {linear_hu_id}'
            })
        
        return jsonify({'error': 'No se proporcionó ningún campo para actualizar'}), 400
        
    except Exception as e:
        print(f"[ERROR] Error actualizando proyecto: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/parse_user_story', methods=['POST'])
def parse_user_story():
    """Parsea la historia de usuario usando el generador profesional"""
    try:
        user_story_text = request.json.get('user_story', '')
        
        if not user_story_text:
            return jsonify({'error': 'Historia de usuario vacía'}), 400
        
        # Usar el generador profesional para extraer criterios
        import sys
        sys.path.insert(0, 'src')
        from professional_qa_generator import ProfessionalQAGenerator
        
        qa_gen = ProfessionalQAGenerator()
        criteria = qa_gen.extract_criteria_from_text(user_story_text)
        
        # Preparar datos para el frontend
        result = {
            'title': 'Historia de Usuario',
            'description': '',
            'acceptance_criteria': criteria,
            'criteria_count': len(criteria),
            'parsed_successfully': True
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'parsed_successfully': False
        }), 500

@app.route('/generate_test_cases', methods=['POST'])
def generate_test_cases():
    """Genera casos de prueba"""
    try:
        # print("DEBUG: Iniciando generación de casos de prueba")
        
        project_id = request.json.get('project_id')
        template = request.json.get('template', 'web')
        qa_comments = request.json.get('qa_comments', '')
        
        # print(f"DEBUG: project_id: {project_id}")
        # print(f"DEBUG: template: {template}")
        # print(f"DEBUG: qa_comments: {qa_comments}")
        
        project = qa_manager.get_project(project_id)
        if not project:
            # print("DEBUG: Proyecto no encontrado")
            return jsonify({'error': 'Proyecto no encontrado'}), 404
        
        # print(f"DEBUG: Proyecto encontrado: {project['name']}")
        # print(f"DEBUG: User story: {project['user_story'][:100]}...")
        
        # ====================================================================
        # GENERADOR PROFESIONAL DE CASOS DE PRUEBA
        # ====================================================================
        import sys
        sys.path.insert(0, 'src')
        
        # Importar TestType ANTES de professional_qa_generator para evitar conflictos
        from test_case_automation import TestCase as LegacyTestCase, TestType, Priority
        
        from professional_qa_generator import ProfessionalQAGenerator
        
        # Crear generador profesional
        qa_generator = ProfessionalQAGenerator()
        
        # Generar casos de prueba automáticamente
        professional_cases = qa_generator.generate_test_cases(
            user_story_text=project['user_story'],
            project_name=project['name']
        )
        
        # Convertir a formato compatible con el sistema
        test_cases = []
        
        for prof_case in professional_cases:
            # Mapear tipos - usar TestType de test_case_automation (FUNCTIONAL, NEGATIVE, INTEGRATION)
            type_map = {
                "Funcional": TestType.FUNCTIONAL,
                "Negativo": TestType.NEGATIVE,
                "Integración": TestType.INTEGRATION,
                "Regresión": TestType.FUNCTIONAL,  # Mapear regresión a funcional
                "UI": TestType.FUNCTIONAL  # Mapear UI a funcional
            }
            
            priority_map = {
                "Alta": Priority.HIGH,
                "Media": Priority.MEDIUM,
                "Baja": Priority.LOW
            }
            
            # 🔥 CONSTRUIR DESCRIPCIÓN ESTRUCTURADA (sin usar _format_description)
            # Cada sección separada con doble salto de línea para mejor legibilidad
            preconditions_text = '\n'.join([f"- {p}" for p in prof_case.preconditions])
            steps_text = '\n'.join(prof_case.steps)
        
            # Descripción estructurada con formato Gherkin
            structured_description = f"""**Objetivo:** Verificar funcionalidad del sistema

**Criterio:** {prof_case.criterion}

**Preconditions:**
{preconditions_text}

**Pasos:**
{steps_text}

**Resultado Esperado:**
{prof_case.expected_result}"""
            
            legacy_case = LegacyTestCase(
                id=prof_case.id,
                title=prof_case.title,
                description=structured_description,
                preconditions=prof_case.preconditions,
                steps=prof_case.steps,
                expected_result=prof_case.expected_result,
                test_type=type_map.get(prof_case.test_type.value, TestType.FUNCTIONAL),
                priority=priority_map.get(prof_case.priority.value, Priority.HIGH),
                user_story=project['name'],
                tags=["@qa", "@automated"]
        )
            test_cases.append(legacy_case)
        
        print(f"[OK] {len(test_cases)} casos de prueba generados con generador profesional", flush=True)
        
        # Validar calidad (solo si hay casos de prueba)
        validator = QAValidator()
        if test_cases:
            validation_result = validator.validate_test_suite(test_cases)
        else:
            validation_result = {
                'average_score': 0,
                'overall_quality': 'Sin casos de prueba',
                'recommendations': ['Generar casos de prueba']
            }
        
        # Convertir casos de prueba a formato serializable
        serializable_test_cases = []
        for tc in test_cases:
            tc_dict = {
                'id': tc.id,
                'title': tc.title,
                'description': tc.description,
                'preconditions': tc.preconditions,
                'steps': tc.steps,
                'expected_result': tc.expected_result,
                'test_type': tc.test_type.value,
                'priority': tc.priority.value,
                'user_story': tc.user_story,
                'tags': tc.tags
            }
            serializable_test_cases.append(tc_dict)
        
        # Actualizar proyecto
        qa_manager.update_project(project_id, 
                                test_cases=serializable_test_cases,
                                validation_result=validation_result,
                                template_used=template,
                                qa_comments=qa_comments,
                                status='generated')
        
        # Preparar respuesta
        result = {
            'success': True,
            'test_cases_count': len(test_cases),
            'validation_result': validation_result,
            'template_used': template,
            'test_cases': []
        }
        
        # Convertir casos de prueba a formato serializable
        for tc in test_cases:
            tc_dict = {
                'id': tc.id,
                'title': tc.title,
                'description': tc.description,
                'preconditions': tc.preconditions,
                'steps': tc.steps,
                'expected_result': tc.expected_result,
                'test_type': tc.test_type.value,
                'priority': tc.priority.value,
                'user_story': tc.user_story,
                'tags': tc.tags
            }
            result['test_cases'].append(tc_dict)
        
        return jsonify(result)
        
    except Exception as e:
        import traceback
        # print(f"DEBUG: Error en generate_test_cases: {str(e)}")
        # print(f"DEBUG: Traceback: {traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500

@app.route('/export_project/<project_id>')
def export_project(project_id):
    """Exporta proyecto a CSV"""
    try:
        project = qa_manager.get_project(project_id)
        if not project:
            return jsonify({'error': 'Proyecto no encontrado'}), 404
        
        if not project.get('test_cases'):
            return jsonify({'error': 'No hay casos de prueba para exportar'}), 400
        
        # Convertir casos de prueba a objetos TestCase
        from test_case_automation import TestCase, TestType, Priority
        
        test_cases = []
        for tc_data in project['test_cases']:
            # Manejar tanto formato string como enum
            test_type = tc_data['test_type'] if isinstance(tc_data['test_type'], str) else tc_data['test_type'].value
            priority = tc_data['priority'] if isinstance(tc_data['priority'], str) else tc_data['priority'].value
            
            tc = TestCase(
                id=tc_data['id'],
                title=tc_data['title'],
                description=tc_data['description'],
                preconditions=tc_data['preconditions'],
                steps=tc_data['steps'],
                expected_result=tc_data['expected_result'],
                test_type=TestType(test_type),
                priority=Priority(priority),
                user_story=tc_data['user_story'],
                tags=tc_data['tags']
            )
            test_cases.append(tc)
        
        # Exportar a CSV
        exporter = TestCaseExporter()
        filename = f"proyecto_{project_id}_casos.csv"
        # Sanitizar nombre de archivo
        filename = "".join(c for c in filename if c.isalnum() or c in (' ', '-', '_', '.')).strip()
        filepath = os.path.abspath(os.path.join(app.config['OUTPUT_FOLDER'], filename))
        
        # Asegurar que el directorio existe
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Validar que el archivo se creó correctamente
        exporter.export_to_csv(test_cases, filepath)
        
        if not os.path.exists(filepath):
            return jsonify({'error': 'No se pudo crear el archivo de exportación'}), 500
        
        try:
            return send_file(filepath, as_attachment=True, download_name=filename, mimetype='text/csv')
        except (OSError, IOError, PermissionError) as e:
            return jsonify({'error': f'Error al enviar archivo: {str(e)}'}), 500
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/export_linear/<project_id>')
def export_linear(project_id):
    """Exporta proyecto para Linear"""
    try:
        project = qa_manager.get_project(project_id)
        if not project:
            return jsonify({'error': 'Proyecto no encontrado'}), 404
        
        if not project.get('test_cases'):
            return jsonify({'error': 'No hay casos de prueba para exportar'}), 400
        
        # Convertir casos de prueba a objetos TestCase
        from test_case_automation import TestCase, TestType, Priority
        
        test_cases = []
        for tc_data in project['test_cases']:
            # Manejar tanto formato string como enum
            test_type = tc_data['test_type'] if isinstance(tc_data['test_type'], str) else tc_data['test_type'].value
            priority = tc_data['priority'] if isinstance(tc_data['priority'], str) else tc_data['priority'].value
            
            tc = TestCase(
                id=tc_data['id'],
                title=tc_data['title'],
                description=tc_data['description'],
                preconditions=tc_data['preconditions'],
                steps=tc_data['steps'],
                expected_result=tc_data['expected_result'],
                test_type=TestType(test_type),
                priority=Priority(priority),
                user_story=tc_data['user_story'],
                tags=tc_data['tags']
            )
            test_cases.append(tc)
        
        # Exportar para Linear
        exporter = LinearSimpleExporter(app.config['OUTPUT_FOLDER'])
        filename = f"proyecto_{project_id}_linear.csv"
        # Sanitizar nombre de archivo
        filename = "".join(c for c in filename if c.isalnum() or c in (' ', '-', '_', '.')).strip()
        filepath = os.path.abspath(os.path.join(app.config['OUTPUT_FOLDER'], filename))
        
        # Asegurar que el directorio existe
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Convertir casos de prueba a formato serializable para LinearSimpleExporter
        serializable_cases = []
        for tc in test_cases:
            tc_dict = {
                'id': tc.id,
                'title': tc.title,
                'description': tc.description,
                'preconditions': tc.preconditions,
                'steps': tc.steps,
                'expected_result': tc.expected_result,
                'test_type': tc.test_type.value,
                'priority': tc.priority.value,
                'user_story': tc.user_story,
                'tags': tc.tags
            }
            serializable_cases.append(tc_dict)
        
        csv_file = exporter.export_to_linear_csv(serializable_cases, f"proyecto_{project_id}", project.get('user_story', ''))
        
        # Validar que el archivo existe
        if not os.path.exists(csv_file):
            return jsonify({'error': 'No se pudo crear el archivo de exportación'}), 500
        
        try:
            return send_file(csv_file, as_attachment=True, download_name=os.path.basename(csv_file), mimetype='text/csv')
        except (OSError, IOError, PermissionError) as e:
            return jsonify({'error': f'Error al enviar archivo: {str(e)}'}), 500
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/templates')
def get_templates():
    """Obtiene plantillas disponibles"""
    try:
        template_manager = TemplateManager()
        templates = []
        
        for template_name in template_manager.get_available_templates():
            info = template_manager.get_template_info(template_name)
            templates.append({
                'id': template_name,
                'name': info['name'],
                'description': info['description']
            })
        
        return jsonify({'templates': templates})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/project/<project_id>/validation')
def get_validation_details(project_id):
    """Obtiene detalles de validación"""
    try:
        project = qa_manager.get_project(project_id)
        if not project:
            return jsonify({'error': 'Proyecto no encontrado'}), 404
        
        validation_result = project.get('validation_result')
        if not validation_result:
            return jsonify({'error': 'No hay validación disponible'}), 400
        
        return jsonify(validation_result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/export_linear_simple/<project_id>')
def export_linear_simple(project_id):
    """Exporta proyecto para Linear en formato simplificado"""
    try:
        project = qa_manager.get_project(project_id)
        if not project:
            return jsonify({'error': 'Proyecto no encontrado'}), 404
        
        if not project.get('test_cases'):
            return jsonify({'error': 'No hay casos de prueba para exportar'}), 400
        
        # Usar el exportador simplificado
        linear_exporter = LinearSimpleExporter(app.config['OUTPUT_FOLDER'])
        csv_file = linear_exporter.export_to_linear_csv(
            project['test_cases'],
            project['name'],
            project.get('user_story', '')
        )
        
        # Validar que el archivo existe y obtener ruta absoluta
        if not csv_file or not os.path.exists(csv_file):
            return jsonify({'error': 'No se pudo crear el archivo de exportación'}), 500
        
        csv_file = os.path.abspath(csv_file)
        filename = os.path.basename(csv_file)
        
        try:
            return send_file(csv_file, as_attachment=True, download_name=filename, mimetype='text/csv')
        except (OSError, IOError, PermissionError) as e:
            return jsonify({'error': f'Error al enviar archivo: {str(e)}'}), 500
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/export_linear_subissues/<project_id>')
def export_linear_subissues(project_id):
    """Exporta proyecto como sub-issues para Linear"""
    try:
        project = qa_manager.get_project(project_id)
        if not project:
            return jsonify({'error': 'Proyecto no encontrado'}), 404
        
        if not project.get('test_cases'):
            return jsonify({'error': 'No hay casos de prueba para exportar'}), 400
        
        # Obtener parent_issue_id del parámetro de query
        parent_issue_id = request.args.get('parent_id', '')
        
        # Usar el exportador para sub-issues
        linear_exporter = LinearSimpleExporter(app.config['OUTPUT_FOLDER'])
        csv_file = linear_exporter.export_as_subissues(
            project['test_cases'],
            project['name'],
            parent_issue_id,
            project.get('user_story', '')
        )
        
        # Validar que el archivo existe y obtener ruta absoluta
        if not csv_file or not os.path.exists(csv_file):
            return jsonify({'error': 'No se pudo crear el archivo de exportación'}), 500
        
        csv_file = os.path.abspath(csv_file)
        filename = os.path.basename(csv_file)
        
        try:
            return send_file(csv_file, as_attachment=True, download_name=filename, mimetype='text/csv')
        except (OSError, IOError, PermissionError) as e:
            return jsonify({'error': f'Error al enviar archivo: {str(e)}'}), 500
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/upload_to_linear/<project_id>', methods=['POST'])
def upload_to_linear_api(project_id):
    """Sube casos de prueba directamente a Linear usando la API"""
    try:
        project = qa_manager.get_project(project_id)
        if not project:
            return jsonify({'error': 'Proyecto no encontrado'}), 404
        
        if not project.get('test_cases'):
            return jsonify({'error': 'No hay casos de prueba para exportar'}), 400
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No se proporcionaron datos'}), 400
        
        # Obtener parámetros
        api_key = data.get('api_key', '').strip()
        parent_issue_id = data.get('parent_issue_id', '').strip()
        
        # Si no se proporciona parent_issue_id, usar el del proyecto
        if not parent_issue_id and project.get('linear_hu_id'):
            parent_issue_id = project['linear_hu_id']
            print(f"[INFO] Usando HU ID del proyecto: {parent_issue_id}")
        
        if not api_key:
            return jsonify({'error': 'API Key de Linear es requerida'}), 400
        
        if not parent_issue_id:
            return jsonify({'error': 'ID de Historia de Usuario es requerido'}), 400
        
        # Crear cliente Linear
        import sys
        print("="*80, flush=True)
        print(f"[INFO] Iniciando subida a Linear...", flush=True)
        print(f"       HU ID: {parent_issue_id}", flush=True)
        print(f"       Casos: {len(project['test_cases'])}", flush=True)
        print("="*80, flush=True)
        sys.stdout.flush()
        
        client = LinearAPIClient(api_key)
        
        # Verificar conexión
        print("[INFO] Verificando conexion con Linear API...", flush=True)
        if not client.test_connection():
            print("[ERROR] No se pudo conectar con Linear", flush=True)
            return jsonify({'error': 'No se pudo conectar con Linear. Verifica tu API Key'}), 400
        print("[OK] Conexion exitosa con Linear API", flush=True)
        
        # Convertir casos al formato correcto
        formatted_cases = []
        for case in project['test_cases']:
            if isinstance(case, dict):
                formatted_cases.append(case)
            else:
                case_dict = {
                    'test_case_id': str(getattr(case, 'id', f'TC-{len(formatted_cases)+1:03d}')),
                    'title': str(getattr(case, 'title', 'Sin título')),
                    'description': str(getattr(case, 'description', '')),
                    'preconditions': str(getattr(case, 'preconditions', '')),
                    'steps': str(getattr(case, 'steps', '')),
                    'expected_result': str(getattr(case, 'expected_result', '')),
                    'priority': str(getattr(case, 'priority', 'Media')),
                    'type': str(getattr(case, 'type', 'Funcional'))
                }
                formatted_cases.append(case_dict)
        
        # Subir casos a Linear
        print(f"[INFO] Llamando a upload_test_cases_as_subissues con {len(formatted_cases)} casos...", flush=True)
        print(f"[INFO] Parent Issue ID: {parent_issue_id}", flush=True)
        print(f"[INFO] Team ID: None (deteccion automatica)", flush=True)
        print("="*80, flush=True)
        sys.stdout.flush()
        
        created_issues = client.upload_test_cases_as_subissues(
            parent_issue_identifier=parent_issue_id,
            test_cases=formatted_cases,
            team_id=None  # Auto-detectar
        )
        
        print("="*80, flush=True)
        if created_issues:
            print(f"[OK] {len(created_issues)} casos subidos exitosamente", flush=True)
            print(f"[OK] IDs creados: {created_issues[:3]}... (mostrando primeros 3)", flush=True)
            print("="*80, flush=True)
            sys.stdout.flush()
            return jsonify({
                'success': True,
                'message': f'{len(created_issues)} casos de prueba subidos exitosamente',
                'created_issues': created_issues
            })
        else:
            print("[ERROR] No se crearon issues en Linear")
            print("="*80)
            return jsonify({'error': 'No se pudieron crear los casos en Linear'}), 500
        
    except Exception as e:
        print(f"[ERROR] Error subiendo a Linear: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/project/<project_id>/test_case/<test_case_id>', methods=['GET'])
def get_test_case(project_id, test_case_id):
    """Obtiene los datos de un caso de prueba específico"""
    try:
        project = qa_manager.get_project(project_id)
        if not project:
            return jsonify({'error': 'Proyecto no encontrado'}), 404
        
        # Buscar el caso de prueba
        test_cases = project.get('test_cases', [])
        test_case = None
        for tc in test_cases:
            if tc.get('id') == test_case_id:
                test_case = tc
                break
        
        if test_case is None:
            return jsonify({'error': 'Caso de prueba no encontrado'}), 404
        
        return jsonify({
            'success': True,
            'test_case': test_case
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/project/<project_id>/test_case/<test_case_id>', methods=['PUT'])
def update_test_case(project_id, test_case_id):
    """Actualiza un caso de prueba específico"""
    try:
        project = qa_manager.get_project(project_id)
        if not project:
            return jsonify({'error': 'Proyecto no encontrado'}), 404
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No se proporcionaron datos'}), 400
        
        # Buscar el caso de prueba
        test_cases = project.get('test_cases', [])
        test_case_index = None
        for i, tc in enumerate(test_cases):
            if tc.get('id') == test_case_id:
                test_case_index = i
                break
        
        if test_case_index is None:
            return jsonify({'error': 'Caso de prueba no encontrado'}), 404
        
        # Actualizar el caso de prueba
        updated_test_case = {
            'id': test_case_id,
            'title': data.get('title', test_cases[test_case_index]['title']),
            'description': data.get('description', test_cases[test_case_index]['description']),
            'preconditions': data.get('preconditions', test_cases[test_case_index]['preconditions']),
            'steps': data.get('steps', test_cases[test_case_index]['steps']),
            'expected_result': data.get('expected_result', test_cases[test_case_index]['expected_result']),
            'test_type': data.get('test_type', test_cases[test_case_index]['test_type']),
            'priority': data.get('priority', test_cases[test_case_index]['priority']),
            'user_story': data.get('user_story', test_cases[test_case_index]['user_story']),
            'tags': data.get('tags', test_cases[test_case_index]['tags'])
        }
        
        test_cases[test_case_index] = updated_test_case
        
        # Actualizar el proyecto
        qa_manager.update_project(project_id, test_cases=test_cases)
        
        return jsonify({
            'success': True,
            'message': 'Caso de prueba actualizado correctamente',
            'test_case': updated_test_case
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/project/<project_id>/test_case/<test_case_id>', methods=['DELETE'])
def delete_test_case(project_id, test_case_id):
    """Elimina un caso de prueba específico"""
    try:
        project = qa_manager.get_project(project_id)
        if not project:
            return jsonify({'error': 'Proyecto no encontrado'}), 404
        
        # Buscar y eliminar el caso de prueba
        test_cases = project.get('test_cases', [])
        original_count = len(test_cases)
        test_cases = [tc for tc in test_cases if tc.get('id') != test_case_id]
        
        if len(test_cases) == original_count:
            return jsonify({'error': 'Caso de prueba no encontrado'}), 404
        
        # Actualizar el proyecto
        qa_manager.update_project(project_id, test_cases=test_cases)
        
        return jsonify({
            'success': True,
            'message': 'Caso de prueba eliminado correctamente',
            'remaining_count': len(test_cases)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/project/<project_id>', methods=['DELETE'])
def delete_project(project_id):
    """Elimina un proyecto completo"""
    try:
        project = qa_manager.get_project(project_id)
        if not project:
            return jsonify({'error': 'Proyecto no encontrado'}), 404
        
        # Eliminar el proyecto
        success = qa_manager.delete_project(project_id)
        
        if success:
            print(f"[OK] Proyecto eliminado: {project_id}", flush=True)
            return jsonify({
                'success': True,
                'message': 'Proyecto eliminado correctamente'
            })
        else:
            return jsonify({'error': 'No se pudo eliminar el proyecto'}), 500
        
    except Exception as e:
        print(f"[ERROR] Error eliminando proyecto: {e}", flush=True)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
