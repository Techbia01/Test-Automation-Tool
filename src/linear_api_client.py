"""
Cliente API para Linear - Creación automática de sub-issues
"""
import requests
import json
from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class LinearIssue:
    """Representa un issue de Linear"""
    id: str
    title: str
    description: str
    state: str
    priority: int
    labels: List[str]

class LinearAPIClient:
    """Cliente para interactuar con la API de Linear"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.linear.app/graphql"
        self.headers = {
            "Authorization": api_key,  # Linear NO usa "Bearer", solo el API key directamente
            "Content-Type": "application/json"
        }
    
    def test_connection(self) -> bool:
        """Prueba la conexión con Linear"""
        query = """
        query {
            viewer {
                id
                name
                email
            }
        }
        """
        
        try:
            response = self._make_request(query)
            return 'viewer' in response.get('data', {})
        except Exception as e:
            print(f"Error conectando con Linear: {e}")
            return False
    
    def get_teams(self) -> List[Dict]:
        """Obtiene los equipos disponibles"""
        query = """
        query {
            teams {
                nodes {
                    id
                    name
                    key
                }
            }
        }
        """
        
        response = self._make_request(query)
        return response.get('data', {}).get('teams', {}).get('nodes', [])
    
    def get_issue_by_identifier(self, identifier: str) -> Optional[str]:
        """Obtiene el UUID interno de un issue por su identificador público (ej: FIN-1234)"""
        query = """
        query($identifier: String!) {
            issue(id: $identifier) {
                id
                identifier
                title
            }
        }
        """
        
        try:
            # Primero intentar con el identificador directo
            response = self._make_request(query, {"identifier": identifier})
            issue = response.get('data', {}).get('issue')
            
            if issue:
                print(f"[OK] Issue encontrado: {issue['identifier']} - {issue['title']}")
                return issue['id']
            
            # Si no funciona, buscar en todos los issues del equipo
            print(f"[INFO] Buscando {identifier} en todos los issues...")
            
            # Obtener issues recientes
            query2 = """
            query {
                issues(first: 50, orderBy: updatedAt) {
                    nodes {
                        id
                        identifier
                        title
                    }
                }
            }
            """
            
            response2 = self._make_request(query2)
            issues = response2.get('data', {}).get('issues', {}).get('nodes', [])
            
            for issue in issues:
                if issue['identifier'] == identifier:
                    print(f"[OK] Issue encontrado: {issue['identifier']} - {issue['title']}")
                    return issue['id']
            
            print(f"[ERROR] No se encontró issue con identificador: {identifier}")
            return None
                
        except Exception as e:
            print(f"[ERROR] Error buscando issue {identifier}: {e}")
            return None
    
    def get_issue_by_id(self, issue_id: str) -> Optional[LinearIssue]:
        """Obtiene un issue por su ID (ej: FIN-1234)"""
        query = """
        query($issueId: String!) {
            issue(id: $issueId) {
                id
                title
                description
                state {
                    name
                }
                priority
                labels {
                    nodes {
                        name
                    }
                }
            }
        }
        """
        
        try:
            response = self._make_request(query, {"issueId": issue_id})
            issue_data = response.get('data', {}).get('issue')
            
            if issue_data:
                return LinearIssue(
                    id=issue_data['id'],
                    title=issue_data['title'],
                    description=issue_data.get('description', ''),
                    state=issue_data['state']['name'],
                    priority=issue_data.get('priority', 0),
                    labels=[label['name'] for label in issue_data.get('labels', {}).get('nodes', [])]
                )
        except Exception as e:
            print(f"Error obteniendo issue {issue_id}: {e}")
        
        return None
    
    def create_sub_issue(self, parent_id: str, title: str, description: str, 
                        team_id: str, priority: int = 2, labels: Optional[List[str]] = None,
                        state_id: Optional[str] = None) -> Optional[str]:
        """Crea un sub-issue vinculado a un issue padre"""
        
        # Obtener IDs de labels
        label_ids = []
        if labels:
            label_ids = self._get_label_ids(team_id, labels)
        else:
            label_ids = []
        
        # Si no se proporciona state_id, obtener el estado "Todo" del equipo
        if not state_id:
            state_id = self._get_todo_state_id(team_id)
        
        mutation = """
        mutation($input: IssueCreateInput!) {
            issueCreate(input: $input) {
                success
                issue {
                    id
                    identifier
                    title
                    team {
                        id
                        key
                        name
                    }
                    state {
                        id
                        name
                    }
                }
            }
        }
        """
        
        input_data = {
            "title": title,
            "description": description,
            "teamId": team_id,
            "parentId": parent_id,
            "priority": priority,
            "labelIds": label_ids
        }
        
        # Agregar stateId si se proporcionó
        if state_id:
            input_data["stateId"] = state_id
        
        variables = {"input": input_data}
        
        try:
            response = self._make_request(mutation, variables)
            
            if not response:
                print("[ERROR] Response es None")
                return None
                
            result = response.get('data', {}).get('issueCreate', {})
            
            if result.get('success'):
                issue = result.get('issue', {})
                team_info = issue.get('team', {})
                state_info = issue.get('state', {})
                print(f"[OK] Sub-issue creado: {issue.get('identifier')} - {issue.get('title')}")
                print(f"       Team: {team_info.get('name')} ({team_info.get('key')})")
                print(f"       State: {state_info.get('name')}")
                return issue.get('id')
            else:
                print(f"[ERROR] Error creando sub-issue: {response}")
                if 'errors' in response:
                    for error in response['errors']:
                        print(f"       Error: {error.get('message', 'Sin mensaje')}")
        except Exception as e:
            print(f"[ERROR] Error en API: {e}")
            import traceback
            traceback.print_exc()
        
        return None
    
    def get_team_by_prefix(self, issue_identifier: str) -> Optional[str]:
        """Detecta automáticamente el equipo según el prefijo del issue (FIN-1264 → Finanzas)"""
        try:
            # Extraer prefijo del identificador (FIN-1264 → FIN)
            prefix = issue_identifier.split('-')[0].upper()
            
            # Obtener todos los equipos
            teams = self.get_teams()
            
            # Buscar equipo que coincida con el prefijo
            for team in teams:
                if team['key'].upper() == prefix:
                    print(f"[INFO] Equipo detectado automaticamente: {team['name']} ({team['key']}) para {issue_identifier}")
                    return team['id']
            
            # Si no encuentra coincidencia exacta, usar el primer equipo
            if teams:
                default_team = teams[0]
                print(f"[WARN] No se encontro equipo para prefijo '{prefix}', usando por defecto: {default_team['name']} ({default_team['key']})")
                return default_team['id']
            
            return None
            
        except Exception as e:
            print(f"[ERROR] Error detectando equipo: {e}")
            return None
    
    def upload_test_cases_as_subissues(self, parent_issue_identifier: str, test_cases: List[Dict], 
                                     team_id: Optional[str] = None) -> List[str]:
        """Sube múltiples casos de prueba como sub-issues"""
        created_issues = []
        
        print(f"[INFO] Subiendo {len(test_cases)} casos de prueba como sub-issues de {parent_issue_identifier}")
        print(f"[INFO] Team ID recibido: {team_id}")
        
        # Detectar equipo automáticamente si no se proporciona
        if not team_id:
            print("[INFO] Detectando equipo automaticamente...")
            team_id = self.get_team_by_prefix(parent_issue_identifier)
            if not team_id:
                print("[ERROR] No se pudo detectar el equipo automaticamente")
                return []
            else:
                print(f"[OK] Equipo detectado: {team_id}")
        else:
            print(f"[OK] Usando equipo proporcionado: {team_id}")
        
        # Primero obtener el UUID interno del parent issue
        print(f"[INFO] Obteniendo UUID para {parent_issue_identifier}...")
        parent_uuid = self.get_issue_by_identifier(parent_issue_identifier)
        if not parent_uuid:
            print(f"[ERROR] No se pudo encontrar la HU {parent_issue_identifier}")
            return []
        else:
            print(f"[OK] UUID obtenido: {parent_uuid}")
        
        print(f"[INFO] Procesando {len(test_cases)} casos de prueba...")
        
        for i, test_case in enumerate(test_cases, 1):
            # Usar solo el título sin duplicar el ID
            # Linear ya agrega su propio identificador (ej: FIN-1234)
            title = test_case.get('title', 'Sin titulo')
            
            print(f"[INFO] Caso {i}/{len(test_cases)}: {test_case.get('test_case_id', f'TC-{i:03d}')} - {title[:50]}...")
            
            # Construir descripción formateada
            description = self._format_test_case_description(test_case)
            
            # Solo usar etiqueta Test_Case (la prioridad va en el campo priority)
            labels = ["Test_Case"]
            
            # Crear sub-issue usando el UUID interno
            print(f"       Creando sub-issue con team_id: {team_id}")
            issue_id = self.create_sub_issue(
                parent_id=parent_uuid,  # UUID interno, no el identificador público
                title=title,
                description=description,
                team_id=team_id,
                priority=self._get_linear_priority(test_case.get('priority', 'Media')),
                labels=labels
            )
            
            if issue_id:
                print(f"       [OK] Sub-issue creado exitosamente")
                created_issues.append(issue_id)
            else:
                print(f"       [ERROR] Error creando sub-issue")
        
        print(f"[INFO] RESULTADO FINAL: {len(created_issues)}/{len(test_cases)} casos subidos")
        return created_issues
    
    def _make_request(self, query: str, variables: Optional[Dict] = None) -> Dict:
        """Hace una petición a la API de Linear"""
        payload: Dict = {"query": query}
        if variables:
            payload["variables"] = variables
        
        response = requests.post(
            self.base_url,
            headers=self.headers,
            json=payload,
            timeout=30
        )
        
        response.raise_for_status()
        return response.json()
    
    def _get_label_ids(self, team_id: str, label_names: List[str]) -> List[str]:
        """Obtiene los IDs de las labels por nombre"""
        query = """
        query($teamId: String!) {
            team(id: $teamId) {
                labels {
                    nodes {
                        id
                        name
                    }
                }
            }
        }
        """
        
        try:
            response = self._make_request(query, {"teamId": team_id})
            labels = response.get('data', {}).get('team', {}).get('labels', {}).get('nodes', [])
            
            label_map = {label['name']: label['id'] for label in labels}
            return [label_map[name] for name in label_names if name in label_map]
        except Exception as e:
            print(f"Error obteniendo labels: {e}")
            return []
    
    def _get_todo_state_id(self, team_id: str) -> Optional[str]:
        """Obtiene el ID del estado 'Todo' o 'To Do' del equipo"""
        query = """
        query($teamId: String!) {
            team(id: $teamId) {
                states {
                    nodes {
                        id
                        name
                        type
                    }
                }
            }
        }
        """
        
        try:
            response = self._make_request(query, {"teamId": team_id})
            states = response.get('data', {}).get('team', {}).get('states', {}).get('nodes', [])
            
            # Buscar estado "Todo" o "To Do" (tipo unstarted)
            for state in states:
                if state.get('name', '').lower() in ['todo', 'to do'] and state.get('type') == 'unstarted':
                    print(f"[INFO] Estado 'Todo' encontrado para el equipo: {state.get('id')}")
                    return state.get('id')
            
            # Si no se encuentra "Todo", buscar el primer estado "unstarted"
            for state in states:
                if state.get('type') == 'unstarted':
                    print(f"[INFO] Usando estado 'unstarted': {state.get('name')} ({state.get('id')})")
                    return state.get('id')
            
            print("[WARN] No se encontro estado 'Todo' o 'unstarted', se usara el estado por defecto (Triage)")
            return None
        except Exception as e:
            print(f"[ERROR] Error obteniendo estados: {e}")
            return None
    
    def _format_test_case_description(self, test_case: Dict) -> str:
        """Formatea la descripción del caso de prueba para Linear"""
        description_parts = []
        
        # La descripción ya viene formateada desde app.py
        # Solo necesitamos agregar los campos adicionales
        
        # Usar la descripción existente (ya tiene Criterio, Tipo y Prioridad)
        if test_case.get('description'):
            description_parts.append(test_case['description'])
        
        # Separador
        description_parts.append("\n---\n")
        
        # Precondiciones (convertir lista a texto)
        preconditions = test_case.get('preconditions', [])
        if preconditions:
            if isinstance(preconditions, list):
                preconditions_text = '\n'.join([f"• {p}" for p in preconditions])
            else:
                preconditions_text = str(preconditions)
            description_parts.append(f"**Precondiciones:**\n{preconditions_text}")
        
        # Pasos (convertir lista a Gherkin)
        steps = test_case.get('steps', [])
        if steps:
            if isinstance(steps, list):
                steps_text = '\n'.join(steps)
            else:
                steps_text = str(steps)
            description_parts.append(f"**Pasos:**\n```gherkin\n{steps_text}\n```")
        
        # Resultado esperado
        if test_case.get('expected_result'):
            description_parts.append(f"**Resultado Esperado:**\n{test_case['expected_result']}")
        
        return "\n\n".join(description_parts)
    
    def _get_linear_priority(self, priority_str: str) -> int:
        """Convierte prioridad de texto a número de Linear"""
        priority_map = {
            'urgente': 1,
            'alta': 2,
            'media': 3,
            'baja': 4
        }
        return priority_map.get(priority_str.lower(), 3)


# Función de utilidad para uso fácil
def upload_to_linear(api_key: str, parent_issue_id: str, test_cases: List[Dict], team_id: Optional[str] = None):
    """Función de conveniencia para subir casos de prueba a Linear"""
    client = LinearAPIClient(api_key)
    
    # Verificar conexión
    if not client.test_connection():
        print("[ERROR] No se pudo conectar con Linear. Verifica tu API Key.")
        return False
    
    # Si no se proporciona team_id, usar el primero disponible
    if not team_id:
        teams = client.get_teams()
        if teams:
            team_id = teams[0]['id']
            print(f"[INFO] Usando equipo: {teams[0]['name']} ({teams[0]['key']})")
        else:
            print("[ERROR] No se encontraron equipos disponibles.")
            return False
    
    # Subir casos de prueba
    if team_id:
        created_issues = client.upload_test_cases_as_subissues(parent_issue_id, test_cases, team_id)
    else:
        print("[ERROR] No se pudo determinar el team_id.")
        return False
    
    return len(created_issues) > 0
