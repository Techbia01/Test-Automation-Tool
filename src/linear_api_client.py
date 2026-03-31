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


@dataclass
class LinearIssueSummary:
    """Resumen de issue para listado (ej. por estado)."""
    id: str
    identifier: str
    title: str
    description: str
    state: str
    team_id: str


@dataclass
class LinearIssueGitContext:
    """Rama y adjuntos Git/PR asociados al issue en Linear."""
    branch_name: str
    attachment_urls: List[str]

class LinearAPIClient:
    """Cliente para interactuar con la API de Linear"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.linear.app/graphql"
        self._labels_by_team: Dict[str, List[Dict]] = {}
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
    
    def create_sub_issue(
        self,
        parent_id: str,
        title: str,
        description: str,
        team_id: str,
        priority: int = 2,
        labels: Optional[List[str]] = None,
        state_id: Optional[str] = None,
        label_ids: Optional[List[str]] = None,
    ) -> Optional[str]:
        """Crea un sub-issue vinculado a un issue padre.

        Si ``label_ids`` se pasa (lista de UUID de etiquetas), se usa tal cual
        (tras deduplicar). Si no, se resuelven los nombres en ``labels``.
        """
        if label_ids is not None:
            label_ids_resolved = list(dict.fromkeys(label_ids))
        elif labels:
            label_ids_resolved = self._get_label_ids(team_id, labels)
        else:
            label_ids_resolved = []
        
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
            "labelIds": label_ids_resolved
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
    
    def upload_test_cases_as_subissues(
        self,
        parent_issue_identifier: str,
        test_cases: List[Dict],
        team_id: Optional[str] = None,
        label_manual: Optional[str] = None,
        label_automatizable: Optional[str] = None,
    ) -> List[str]:
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

        # Obtener títulos de sub-issues ya existentes para evitar duplicados
        existing_titles = self.get_sub_issue_titles(parent_uuid)
        if existing_titles:
            print(f"[INFO] {len(existing_titles)} sub-issue(s) ya existen en {parent_issue_identifier}; se omitirán duplicados")
        
        manual_name = (label_manual or "TC_Manual").strip()
        auto_name = (label_automatizable or "TC_Automatizable").strip()
        self._labels_by_team[team_id] = self._fetch_team_labels_paginated(team_id)
        nodes = self._labels_by_team[team_id]

        print(f"[INFO] Procesando {len(test_cases)} casos de prueba...")
        print(
            "[INFO] Etiquetas ejecución: Manual=%r | Automatizable=%r (%d etiquetas cargadas)"
            % (manual_name, auto_name, len(nodes))
        )
        if not nodes:
            print(
                "[WARN] No se pudieron cargar etiquetas del equipo; "
                "revisa team_id y permisos del API key."
            )

        def _match_label(names: List[str]) -> Optional[str]:
            cur = self._labels_by_team.get(team_id) or []
            for want in names:
                if not want:
                    continue
                w = want.strip().lower()
                for node in cur:
                    if (node.get("name") or "").strip().lower() == w:
                        return node.get("id")
            return None

        def _ensure_label(names: List[str]) -> Optional[str]:
            lid = _match_label(names)
            if lid:
                return lid
            primary = next((n for n in names if n and str(n).strip()), None)
            if not primary:
                return None
            created = self._create_team_label(team_id, primary.strip())
            if created:
                self._labels_by_team.setdefault(team_id, []).append(
                    {"id": created, "name": primary.strip()}
                )
                return created
            self._labels_by_team[team_id] = self._fetch_team_labels_paginated(
                team_id
            )
            return _match_label(names)

        for i, test_case in enumerate(test_cases, 1):
            title = test_case.get("title", "Sin titulo")

            # Saltar si ya existe un sub-issue con el mismo título
            if title.strip().lower() in existing_titles:
                print(
                    "[SKIP] Caso %d/%d ya existe: %s..."
                    % (i, len(test_cases), title[:60])
                )
                continue

            print(
                "[INFO] Caso %d/%d: %s - %s..."
                % (
                    i,
                    len(test_cases),
                    test_case.get("test_case_id", "TC-%03d" % i),
                    title[:50],
                )
            )

            description = self._format_test_case_description(test_case)

            label_ids: List[str] = []
            tc_id = _match_label(["Test_Case", "test_case"])
            if tc_id and tc_id not in label_ids:
                label_ids.append(tc_id)

            raw_suit = test_case.get("execution_suitability")
            if raw_suit is None and i == 1:
                print(
                    "[WARN] Los casos no incluyen 'execution_suitability'; "
                    "solo se aplicará Test_Case. Actualiza run_linear / generador."
                )
            if isinstance(raw_suit, str):
                suit = raw_suit.strip()
            elif raw_suit is not None and hasattr(raw_suit, "value"):
                suit = str(raw_suit.value).strip()
            else:
                suit = (str(raw_suit) if raw_suit is not None else "").strip()
            if suit == "Automatizable":
                aid = _ensure_label(
                    [auto_name, "TC_Automatizable", "Automatizable"]
                )
                if aid and aid not in label_ids:
                    label_ids.append(aid)
            else:
                # Manual, Revisar (histórico) o vacío → TC_Manual
                mid = _ensure_label(
                    [manual_name, "TC_Manual", "Manual"]
                )
                if mid and mid not in label_ids:
                    label_ids.append(mid)

            print("       Creando sub-issue con team_id: %s" % team_id)
            issue_id = self.create_sub_issue(
                parent_id=parent_uuid,
                title=title,
                description=description,
                team_id=team_id,
                priority=self._get_linear_priority(
                    test_case.get("priority", "Media")
                ),
                labels=None,
                label_ids=label_ids,
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
    
    def _fetch_team_labels_paginated(self, team_id: str) -> List[Dict]:
        """Todas las etiquetas del equipo (paginado; Linear no devuelve todas en una página)."""
        out: List[Dict] = []
        cursor: Optional[str] = None
        query = """
        query($teamId: String!, $after: String) {
            team(id: $teamId) {
                labels(first: 100, after: $after) {
                    pageInfo {
                        hasNextPage
                        endCursor
                    }
                    nodes {
                        id
                        name
                    }
                }
            }
        }
        """
        try:
            while True:
                response = self._make_request(
                    query, {"teamId": team_id, "after": cursor}
                )
                team = (response.get("data") or {}).get("team") or {}
                conn = team.get("labels") or {}
                batch = conn.get("nodes") or []
                out.extend(batch)
                pi = conn.get("pageInfo") or {}
                if not pi.get("hasNextPage"):
                    break
                cursor = pi.get("endCursor")
                if not cursor:
                    break
            return out
        except Exception as e:
            print("[WARN] Error listando etiquetas del equipo: %s" % e)
            return out

    def _team_label_nodes(self, team_id: str) -> List[Dict]:
        """Compatibilidad: etiquetas del equipo (con caché)."""
        if team_id not in self._labels_by_team:
            self._labels_by_team[team_id] = self._fetch_team_labels_paginated(
                team_id
            )
        return self._labels_by_team[team_id]

    def _get_team_labels(self, team_id: str, refresh: bool = False) -> List[Dict]:
        if refresh or team_id not in self._labels_by_team:
            self._labels_by_team[team_id] = self._fetch_team_labels_paginated(
                team_id
            )
        return self._labels_by_team[team_id]

    def _find_label_id(self, team_id: str, name: str) -> Optional[str]:
        """Busca etiqueta por nombre exacto o sin distinguir mayúsculas."""
        name_lower = name.strip().lower()
        for node in self._team_label_nodes(team_id):
            if node.get("name", "").strip().lower() == name_lower:
                return node.get("id")
        return None

    def _create_team_label(self, team_id: str, name: str, color: str = "#5E6AD2") -> Optional[str]:
        """Crea una etiqueta en el equipo. Devuelve el id o None."""
        mutation = """
        mutation($input: IssueLabelCreateInput!) {
            issueLabelCreate(input: $input) {
                success
                issueLabel {
                    id
                    name
                }
            }
        }
        """
        try:
            response = self._make_request(
                mutation,
                {"input": {"teamId": team_id, "name": name.strip(), "color": color}},
            )
            err = response.get("errors")
            if err:
                for e in err:
                    print(
                        "[WARN] issueLabelCreate: %s"
                        % e.get("message", str(e))
                    )
                return None
            payload = response.get("data", {}).get("issueLabelCreate", {})
            if payload.get("success") and payload.get("issueLabel"):
                lid = payload["issueLabel"].get("id")
                print(
                    "[INFO] Etiqueta creada en el equipo: %s (%s)"
                    % (name, lid[:8] if lid else "")
                )
                return lid
        except Exception as e:
            print("[WARN] No se pudo crear la etiqueta %r: %s" % (name, e))
        return None

    def get_or_create_label_id(self, team_id: str, name: str) -> Optional[str]:
        """
        Obtiene el id de una etiqueta del equipo o la crea si no existe.
        """
        if not name or not str(name).strip():
            return None
        name = str(name).strip()
        found = self._find_label_id(team_id, name)
        if found:
            return found
        created = self._create_team_label(team_id, name)
        if created:
            return created
        return self._find_label_id(team_id, name)

    def _get_label_ids(self, team_id: str, label_names: List[str]) -> List[str]:
        """Obtiene los IDs de las labels por nombre (exacto o misma capitalización)."""
        result: List[str] = []
        for name in label_names:
            lid = self._find_label_id(team_id, name)
            if lid:
                result.append(lid)
        return result
    
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

    def _get_state_id_by_name(self, team_id: str, state_name: str) -> Optional[str]:
        """Obtiene el ID del estado del equipo por nombre (ej. 'TC Generator')."""
        query = """
        query($teamId: String!) {
            team(id: $teamId) {
                states {
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
            states = response.get("data", {}).get("team", {}).get("states", {}).get("nodes", [])
            for state in states:
                if state.get("name") == state_name:
                    return state.get("id")
            return None
        except Exception as e:
            print(f"[ERROR] Error obteniendo estado por nombre: {e}")
            return None

    def list_issues_by_state(
        self,
        state_name: str,
        team_id: Optional[str] = None,
        team_ids: Optional[List[str]] = None,
        first: int = 50,
    ) -> List[LinearIssueSummary]:
        """
        Lista issues que están en el estado indicado.
        state_name: nombre del estado en la UI de Linear (ej. 'TC Generator').
        team_id: si se indica, solo se buscan issues de ese equipo.
        team_ids: si se indica, solo se buscan en esos equipos; si team_id y team_ids son None, se usan todos.
        first: máximo de issues por equipo.
        """
        teams_to_use: List[Dict] = []
        if team_id:
            teams = self.get_teams()
            t = next((x for x in teams if x["id"] == team_id), None)
            if t:
                teams_to_use = [t]
        elif team_ids:
            teams = self.get_teams()
            teams_to_use = [x for x in teams if x["id"] in team_ids]
        else:
            teams_to_use = self.get_teams()

        result: List[LinearIssueSummary] = []
        for team in teams_to_use:
            tid = team["id"]
            state_id = self._get_state_id_by_name(tid, state_name)
            if not state_id:
                continue
            query = """
            query($filter: IssueFilter!, $first: Int!) {
                issues(filter: $filter, first: $first) {
                    nodes {
                        id
                        identifier
                        title
                        description
                        state { name }
                        team { id }
                    }
                }
            }
            """
            variables = {
                "filter": {"state": {"id": {"eq": state_id}}, "team": {"id": {"eq": tid}}},
                "first": first,
            }
            try:
                response = self._make_request(query, variables)
                nodes = response.get("data", {}).get("issues", {}).get("nodes", [])
                for n in nodes:
                    result.append(
                        LinearIssueSummary(
                            id=n["id"],
                            identifier=n["identifier"],
                            title=n.get("title") or "",
                            description=(n.get("description") or "") or "",
                            state=(n.get("state") or {}).get("name") or "",
                            team_id=(n.get("team") or {}).get("id") or tid,
                        )
                    )
            except Exception as e:
                print(f"[ERROR] list_issues_by_state para equipo {tid}: {e}")
        return result

    def get_issue_summary_by_uuid(self, issue_uuid: str) -> Optional[LinearIssueSummary]:
        """Carga identificador, descripción y equipo por UUID (útil para webhooks)."""
        query = """
        query($id: String!) {
            issue(id: $id) {
                id
                identifier
                title
                description
                state { id name }
                team { id }
            }
        }
        """
        try:
            response = self._make_request(query, {"id": issue_uuid})
            n = (response.get("data") or {}).get("issue")
            if not n:
                return None
            return LinearIssueSummary(
                id=n["id"],
                identifier=n.get("identifier") or "",
                title=n.get("title") or "",
                description=(n.get("description") or "") or "",
                state=(n.get("state") or {}).get("name") or "",
                team_id=(n.get("team") or {}).get("id") or "",
            )
        except Exception as e:
            print("[ERROR] get_issue_summary_by_uuid: %s" % e)
            return None

    def count_sub_issues(self, parent_uuid: str) -> int:
        """Número de sub-issues directos del padre."""
        query = """
        query($id: String!) {
            issue(id: $id) {
                children(first: 100) {
                    nodes { id }
                }
            }
        }
        """
        try:
            response = self._make_request(query, {"id": parent_uuid})
            ch = (response.get("data") or {}).get("issue") or {}
            nodes = (ch.get("children") or {}).get("nodes") or []
            return len(nodes)
        except Exception:
            return 0

    def get_sub_issue_titles(self, parent_uuid: str) -> set:
        """Retorna el conjunto de títulos (en minúsculas) de los sub-issues existentes."""
        query = """
        query($id: String!) {
            issue(id: $id) {
                children(first: 250) {
                    nodes { title }
                }
            }
        }
        """
        try:
            response = self._make_request(query, {"id": parent_uuid})
            ch = (response.get("data") or {}).get("issue") or {}
            nodes = (ch.get("children") or {}).get("nodes") or []
            return {(n.get("title") or "").strip().lower() for n in nodes}
        except Exception:
            return set()

    def update_issue_state(self, issue_id: str, state_name: str, team_id: str) -> bool:
        """
        Mueve un issue al estado indicado.
        issue_id: UUID del issue (id interno de Linear).
        state_name: nombre del estado en la UI (ej. 'Ready for QA').
        team_id: ID del equipo (para resolver el workflow state).
        """
        state_id = self._get_state_id_by_name(team_id, state_name)
        if not state_id:
            print(f"[WARN] Estado '{state_name}' no encontrado en el equipo")
            return False
        mutation = """
        mutation($id: String!, $input: IssueUpdateInput!) {
            issueUpdate(id: $id, input: $input) {
                success
                issue { id state { name } }
            }
        }
        """
        try:
            response = self._make_request(
                mutation,
                {"id": issue_id, "input": {"stateId": state_id}},
            )
            data = response.get("data", {}).get("issueUpdate", {})
            if data.get("success"):
                return True
            return False
        except Exception as e:
            print(f"[ERROR] update_issue_state: {e}")
            return False

    def get_issue_git_context(self, issue_uuid: str) -> LinearIssueGitContext:
        """
        Rama vinculada (branchName) y URLs de attachments (PR, enlaces).
        La rama de Git suele estar en branchName; no siempre hay URL github.com
        en los adjuntos.
        """
        query = """
        query($issueId: String!) {
            issue(id: $issueId) {
                branchName
                attachments {
                    nodes {
                        url
                    }
                }
            }
        }
        """
        try:
            response = self._make_request(query, {"issueId": issue_uuid})
            issue_data = response.get("data", {}).get("issue")
            if not issue_data:
                return LinearIssueGitContext(branch_name="", attachment_urls=[])
            branch = issue_data.get("branchName") or ""
            if isinstance(branch, str):
                branch = branch.strip()
            else:
                branch = ""
            nodes = issue_data.get("attachments", {}).get("nodes", [])
            urls = []
            for n in nodes:
                u = (n.get("url") or "").strip()
                if u:
                    urls.append(u)
            return LinearIssueGitContext(
                branch_name=branch, attachment_urls=urls
            )
        except Exception as e:
            print(f"[WARN] get_issue_git_context: {e}")
            return LinearIssueGitContext(branch_name="", attachment_urls=[])

    def get_issue_attachment_urls(self, issue_uuid: str) -> List[str]:
        """Compatibilidad: solo URLs de adjuntos."""
        return self.get_issue_git_context(issue_uuid).attachment_urls

    def _format_test_case_description(self, test_case: Dict) -> str:
        """Formatea la descripción del caso de prueba para Linear."""
        if test_case.get("linear_description_is_complete") and test_case.get(
            "description"
        ):
            return str(test_case["description"]).strip()

        description_parts = []
        suit = test_case.get("execution_suitability")
        hint = (test_case.get("automation_hint") or "").strip()
        if suit:
            note = hint if hint else "—"
            description_parts.append(
                f"**Ejecución sugerida:** {suit}\n**Nota:** {note}"
            )

        if test_case.get("description"):
            description_parts.append(test_case["description"])

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
