#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema Web para QA - Frontend de Generación de Casos de Prueba
Aplicación web completa para equipos QA
"""

from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
import json
import os
import pandas as pd
from datetime import datetime
from test_case_automation import UserStoryParser, TestCaseGenerator, QAValidator, TestCaseExporter
from test_templates import TemplateManager
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from exporters.linear_simple_exporter import LinearSimpleExporter
from generators.gherkin_generator import GherkinGenerator, GherkinTestCase
from generators.enhanced_gherkin_generator import EnhancedGherkinGenerator, EnhancedGherkinTestCase
from improved_test_generator import ImprovedTestGenerator, ImprovedTestCase
from quick_fix_generator import QuickTestGenerator, QuickTestCase
from linear_api_client import LinearAPIClient

app = Flask(__name__)
app.secret_key = 'qa_automation_secret_key_2024'

# Configuración global
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'

# Crear directorios si no existen
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

class QAProject:
    """Clase para manejar proyectos de QA"""
    
    def __init__(self):
        self.projects = {}
        self.load_projects()
    
    def load_projects(self):
        """Carga proyectos existentes"""
        try:
            if os.path.exists('qa_projects.json'):
                with open('qa_projects.json', 'r', encoding='utf-8') as f:
                    self.projects = json.load(f)
        except Exception as e:
            print(f"Error cargando proyectos: {e}")
            self.projects = {}
    
    def save_projects(self):
        """Guarda proyectos"""
        try:
            with open('qa_projects.json', 'w', encoding='utf-8') as f:
                json.dump(self.projects, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error guardando proyectos: {e}")
    
    def create_project(self, name, description="", user_story="", qa_comments="", linear_hu_id=""):
        """Crea un nuevo proyecto"""
        project_id = f"proj_{len(self.projects) + 1}_{int(datetime.now().timestamp())}"
        
        # Generar descripción automática si no se proporciona
        if not description and user_story:
            # Extraer una descripción breve del user_story
            first_line = user_story.split('\n')[0].strip()
            description = first_line[:100] + "..." if len(first_line) > 100 else first_line
        
        project = {
            'id': project_id,
            'name': name,
            'description': description,
            'user_story': user_story,
            'qa_comments': qa_comments,
            'linear_hu_id': linear_hu_id,  # ¡NUEVO CAMPO!
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
        """Actualiza un proyecto"""
        if project_id in self.projects:
            self.projects[project_id].update(kwargs)
            self.save_projects()
            return True
        return False
    
    def get_project(self, project_id):
        """Obtiene un proyecto"""
        return self.projects.get(project_id)
    
    def list_projects(self):
        """Lista todos los proyectos"""
        return list(self.projects.values())

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
        
        if not name or not user_story or not linear_hu_id:
            return jsonify({'error': 'Nombre, historia de usuario e ID de HU son requeridos'}), 400
        
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
def update_project(project_id):
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
            print(f"✅ HU ID actualizado para proyecto {project_id}: {linear_hu_id}")
            
            return jsonify({
                'success': True,
                'message': f'HU ID actualizado: {linear_hu_id}'
            })
        
        return jsonify({'error': 'No se proporcionó ningún campo para actualizar'}), 400
        
    except Exception as e:
        print(f"❌ Error actualizando proyecto: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/parse_user_story', methods=['POST'])
def parse_user_story():
    """Parsea la historia de usuario"""
    try:
        user_story_text = request.json.get('user_story', '')
        
        if not user_story_text:
            return jsonify({'error': 'Historia de usuario vacía'}), 400
        
        # Parsear historia
        parser = UserStoryParser()
        parsed_story = parser.parse_from_text(user_story_text)
        
        # Preparar datos para el frontend
        result = {
            'title': parsed_story.title,
            'description': parsed_story.description,
            'acceptance_criteria': parsed_story.acceptance_criteria,
            'criteria_count': len(parsed_story.acceptance_criteria),
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
        
        # Parsear historia de usuario
        parser = UserStoryParser()
        user_story = parser.parse_from_text(project['user_story'])
        
        # Debug: Verificar tipo de user_story
        # print(f"DEBUG: user_story type: {type(user_story)}")
        # print(f"DEBUG: user_story: {user_story}")
        
        # GENERAR CASOS MEJORADOS DIRECTAMENTE AQUÍ
        print("DEBUG: Generando casos mejorados directamente")
        test_cases = []
        test_counter = 1
        
        # Generar casos específicos para cada criterio
        for i, criteria in enumerate(user_story.acceptance_criteria, 1):
            # Generar título completo y claro
            title = f"TC-{test_counter:03d}: Validación de {criteria[:50]}..." if len(criteria) > 50 else f"TC-{test_counter:03d}: Validación de {criteria}"
            
            # Descripción concisa
            description = f"""**Objetivo:** Verificar funcionalidad del sistema

**Criterio:** {criteria[:100]}{'...' if len(criteria) > 100 else ''}

**Tipo:** Funcional | **Prioridad:** Alta"""
            
            # Crear caso de prueba
            test_case = TestCase(
                id=f"TC-{test_counter:03d}",
                title=title,
                description=description,
                preconditions=["El sistema está operativo", "Los datos de prueba están disponibles"],
                steps=[
                    "Acceder al sistema",
                    f"Ejecutar: {criteria[:80]}{'...' if len(criteria) > 80 else ''}",
                    "Verificar el resultado"
                ],
                expected_result="El sistema debe completar la operación exitosamente",
                test_type=TestType.FUNCTIONAL,
                priority=Priority.HIGH,
                user_story=user_story.title,
                tags=["@funcional", "@validacion"]
            )
            test_cases.append(test_case)
            test_counter += 1
            
            print(f"DEBUG: Caso generado - {title}")
        
        # Generar caso negativo
        negative_title = f"TC-{test_counter:03d}: Validación de manejo de errores"
        negative_description = """**Objetivo:** Verificar manejo de errores

**Criterio:** El sistema debe manejar errores apropiadamente

**Tipo:** Negativo | **Prioridad:** Media"""
        
        negative_case = TestCase(
            id=f"TC-{test_counter:03d}",
            title=negative_title,
            description=negative_description,
            preconditions=["El sistema está operativo"],
            steps=[
                "Acceder al sistema",
                "Ingresar datos inválidos",
                "Verificar manejo de errores"
            ],
            expected_result="El sistema debe mostrar mensaje de error apropiado",
            test_type=TestType.NEGATIVE,
            priority=Priority.MEDIUM,
            user_story=user_story.title,
            tags=["@negativo", "@error"]
        )
        test_cases.append(negative_case)
        
        print(f"DEBUG: Total casos generados: {len(test_cases)}")
        
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
        filepath = os.path.join(app.config['OUTPUT_FOLDER'], filename)
        
        exporter.export_to_csv(test_cases, filepath)
        
        return send_file(filepath, as_attachment=True, download_name=filename)
        
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
        exporter = LinearExporter()
        filename = f"proyecto_{project_id}_linear.csv"
        filepath = os.path.join(app.config['OUTPUT_FOLDER'], filename)
        
        exporter.create_linear_import_template(test_cases, filepath)
        
        return send_file(filepath, as_attachment=True, download_name=filename)
        
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
        
        return send_file(csv_file, as_attachment=True, download_name=os.path.basename(csv_file))
        
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
        
        return send_file(csv_file, as_attachment=True, download_name=os.path.basename(csv_file))
        
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
        
        # Obtener parámetros requeridos
        api_key = data.get('api_key', '').strip()
        parent_issue_id = data.get('parent_issue_id', '').strip()
        team_id = data.get('team_id', '').strip()
        
        # Si no se proporciona parent_issue_id, usar el del proyecto
        if not parent_issue_id and project.get('linear_hu_id'):
            parent_issue_id = project['linear_hu_id']
            print(f"🎯 Usando HU ID del proyecto: {parent_issue_id}")
        
        if not api_key:
            return jsonify({'error': 'API Key de Linear es requerida'}), 400
        
        if not parent_issue_id:
            return jsonify({'error': 'ID de Historia de Usuario es requerido (en datos o proyecto)'}), 400
        
        # Crear cliente Linear
        client = LinearAPIClient(api_key)
        
        # Verificar conexión
        if not client.test_connection():
            return jsonify({'error': 'No se pudo conectar con Linear. Verifica tu API Key'}), 400
        
        # Si no se proporciona team_id, se detectará automáticamente
        # Convertir casos de prueba al formato correcto
        print(f"🔍 Debug: Proyecto tiene {len(project['test_cases'])} casos")
        print(f"🎯 Debug: HU ID recibido: {parent_issue_id}")
        print(f"🏢 Debug: Team ID recibido: {team_id}")
        
        # Convertir objetos TestCase a diccionarios si es necesario
        formatted_cases = []
        for i, case in enumerate(project['test_cases']):
            print(f"📝 Debug: Procesando caso {i+1}: {type(case)}")
            
            if isinstance(case, dict):
                # Ya es diccionario
                formatted_cases.append(case)
                print(f"   ✅ Caso {i+1} ya es diccionario: {case.get('title', 'Sin título')}")
            else:
                # Es objeto, convertir a diccionario
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
                print(f"   🔄 Caso {i+1} convertido: {case_dict['title']}")
        
        print(f"✅ Total casos formateados: {len(formatted_cases)}")
        
        # Debug: Mostrar primeros casos
        for i, case in enumerate(formatted_cases[:3]):
            print(f"📋 Caso {i+1}: {case['title'][:50]}...")
        
        if len(formatted_cases) > 3:
            print(f"   ... y {len(formatted_cases) - 3} casos más")
        
        # Subir casos de prueba como sub-issues
        created_issues = client.upload_test_cases_as_subissues(
            parent_issue_id, 
            formatted_cases,  # Usar casos formateados
            team_id  # Puede ser None, se detectará automáticamente
        )
        
        if created_issues:
            return jsonify({
                'success': True,
                'message': f'Se crearon {len(created_issues)} sub-issues exitosamente',
                'created_issues': len(created_issues),
                'total_cases': len(project['test_cases'])
            })
        else:
            return jsonify({'error': 'No se pudieron crear los sub-issues'}), 500
        
    except Exception as e:
        return jsonify({'error': f'Error interno: {str(e)}'}), 500

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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
