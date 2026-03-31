#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuración Automática para Linear
Configura el sistema para trabajar directamente con Linear
"""

import os
import json
from pathlib import Path

def setup_linear_integration():
    """Configura la integración con Linear"""
    print("🔗 CONFIGURACIÓN DE INTEGRACIÓN CON LINEAR")
    print("=" * 50)
    
    # Crear archivo de configuración
    config = {
        "linear": {
            "api_key": "",
            "team_id": "",
            "team_name": "QA",
            "default_labels": ["qa-testing", "test-case"],
            "auto_generate": True,
            "sync_enabled": False
        },
        "generation": {
            "default_template": "web",
            "auto_validate": True,
            "export_formats": ["excel", "json"],
            "include_linear_metadata": True
        },
        "workflow": {
            "create_issues_automatically": False,
            "assign_to_qa_team": True,
            "use_linear_labels": True,
            "sync_test_results": False
        }
    }
    
    # Solicitar configuración
    print("📋 Configuración de Linear:")
    
    api_key = input("🔑 API Key de Linear (opcional, presiona Enter para omitir): ").strip()
    if api_key:
        config["linear"]["api_key"] = api_key
        os.environ['LINEAR_API_KEY'] = api_key
    
    team_name = input("👥 Nombre del equipo QA en Linear (default: QA): ").strip()
    if team_name:
        config["linear"]["team_name"] = team_name
    
    default_template = input("🎨 Plantilla por defecto (web/mobile/api, default: web): ").strip()
    if default_template in ["web", "mobile", "api"]:
        config["generation"]["default_template"] = default_template
    
    # Guardar configuración
    with open("linear_config.json", "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print("✅ Configuración guardada en linear_config.json")
    
    # Crear script de automatización
    create_automation_script(config)
    
    # Crear archivo .env
    create_env_file(api_key)
    
    print("\n🎉 ¡Configuración completada!")
    print("\n📖 Próximos pasos:")
    print("1. Configura tu API key de Linear en .env")
    print("2. Ejecuta: python linear_generator.py")
    print("3. O usa el script automático: python auto_linear.py")

def create_automation_script(config):
    """Crea script de automatización"""
    script_content = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Automatización para Linear
Ejecuta automáticamente la generación de casos desde Linear
"""

import os
import json
from linear_generator import LinearAPI, LinearTestCaseGenerator
from test_case_automation import TestCaseExporter

def load_config():
    """Carga configuración"""
    try:
        with open("linear_config.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ Archivo linear_config.json no encontrado")
        print("💡 Ejecuta: python setup_linear.py")
        return None

def main():
    """Función principal de automatización"""
    print("🤖 AUTOMATIZACIÓN DE CASOS DESDE LINEAR")
    print("=" * 40)
    
    config = load_config()
    if not config:
        return
    
    # Configurar API
    api_key = config["linear"]["api_key"] or os.getenv('LINEAR_API_KEY')
    if not api_key:
        print("❌ API Key de Linear no configurada")
        print("💡 Configura LINEAR_API_KEY en .env o linear_config.json")
        return
    
    # Crear cliente
    linear_api = LinearAPI(api_key)
    generator = LinearTestCaseGenerator(linear_api)
    
    # Obtener issues
    team_name = config["linear"]["team_name"]
    print(f"🔍 Buscando issues en equipo: {team_name}")
    
    issues = linear_api.get_issues_by_team(team_name)
    if not issues:
        print(f"❌ No se encontraron issues en equipo '{team_name}'")
        return
    
    print(f"📋 {len(issues)} issues encontrados")
    
    # Generar casos
    template = config["generation"]["default_template"]
    print(f"🧪 Generando casos con plantilla: {template}")
    
    test_cases_data = generator.generate_from_linear_issues(issues, template)
    
    if not test_cases_data:
        print("❌ No se pudieron generar casos")
        return
    
    print(f"✅ {len(test_cases_data)} casos generados")
    
    # Exportar
    exporter = TestCaseExporter()
    test_cases = [data['test_case'] for data in test_cases_data]
    
    formats = config["generation"]["export_formats"]
    for format_type in formats:
        if format_type == "excel":
            exporter.export_to_excel(test_cases, "linear_auto_casos.xlsx")
        elif format_type == "csv":
            exporter.export_to_csv(test_cases, "linear_auto_casos.csv")
        elif format_type == "json":
            exporter.export_to_json(test_cases, "linear_auto_casos.json")
    
    print("📤 Casos exportados automáticamente")
    
    # Mostrar resumen
    if test_cases_data:
        avg_score = sum(data['validation']['average_score'] for data in test_cases_data) / len(test_cases_data)
        print(f"📊 Puntaje promedio: {avg_score:.1f}/100")

if __name__ == "__main__":
    main()
'''
    
    with open("auto_linear.py", "w", encoding="utf-8") as f:
        f.write(script_content)
    
    print("✅ Script de automatización creado: auto_linear.py")

def create_env_file(api_key):
    """Crea archivo .env"""
    env_content = f"""# Configuración de Linear
LINEAR_API_KEY={api_key or 'tu_api_key_aqui'}

# Configuración del equipo
LINEAR_TEAM_NAME=QA

# Configuración de generación
DEFAULT_TEMPLATE=web
AUTO_VALIDATE=true
"""
    
    with open(".env", "w", encoding="utf-8") as f:
        f.write(env_content)
    
    print("✅ Archivo .env creado")

def create_linear_workflow_guide():
    """Crea guía de flujo de trabajo con Linear"""
    guide_content = """# 🔄 Flujo de Trabajo con Linear

## 🎯 Configuración Inicial

1. **Obtener API Key de Linear:**
   - Ve a Linear → Settings → API
   - Crea una nueva API Key
   - Copia la key

2. **Configurar el sistema:**
   ```bash
   python setup_linear.py
   ```

3. **Configurar variables de entorno:**
   ```bash
   # En .env
   LINEAR_API_KEY=tu_api_key_aqui
   LINEAR_TEAM_NAME=QA
   ```

## 🚀 Flujo de Trabajo Diario

### **Opción 1: Generación Automática**
```bash
# Genera casos automáticamente desde Linear
python auto_linear.py
```

### **Opción 2: Generación Manual**
```bash
# Genera casos desde Linear con opciones
python linear_generator.py
```

### **Opción 3: Desde Labels Específicos**
1. En Linear, agrega label `qa-testing` a tus issues
2. Ejecuta: `python linear_generator.py`
3. Selecciona opción 1 (generar desde label)
4. Ingresa: `qa-testing`

## 📋 Estructura Recomendada en Linear

### **Labels para QA:**
- `qa-testing` - Issues que necesitan casos de prueba
- `test-case-generated` - Issues con casos ya generados
- `high-priority` - Casos de alta prioridad
- `regression` - Casos de regresión

### **Estados:**
- `Todo` - Issue sin casos de prueba
- `In Progress` - Generando casos de prueba
- `Done` - Casos de prueba completados

### **Equipos:**
- `QA` - Equipo principal de QA
- `QA-Automation` - Casos de automatización
- `QA-Manual` - Casos manuales

## 🔄 Automatización Avanzada

### **Webhook de Linear (Futuro):**
- Configurar webhook para generar casos automáticamente
- Cuando se crea issue con label `qa-testing`
- Generar casos automáticamente
- Actualizar issue con casos generados

### **Sincronización Bidireccional:**
- Actualizar Linear con resultados de pruebas
- Sincronizar estados de casos
- Reportar métricas de calidad

## 💡 Tips y Mejores Prácticas

### **Para Issues en Linear:**
- ✅ Usa descripciones detalladas
- ✅ Incluye criterios de aceptación
- ✅ Usa labels consistentes
- ✅ Asigna prioridades apropiadas

### **Para Casos Generados:**
- ✅ Revisa la validación de calidad
- ✅ Ajusta casos según necesidades
- ✅ Organiza por módulos/funcionalidades
- ✅ Mantén sincronización con Linear

### **Para el Equipo:**
- ✅ Establece convenciones de naming
- ✅ Usa templates apropiados
- ✅ Monitorea métricas de calidad
- ✅ Automatiza procesos repetitivos

## 🛠️ Comandos Útiles

```bash
# Configuración inicial
python setup_linear.py

# Generación automática
python auto_linear.py

# Generación manual
python linear_generator.py

# Verificar configuración
python -c "import os; print('API Key:', 'OK' if os.getenv('LINEAR_API_KEY') else 'NO CONFIGURADA')"
```

## 🆘 Solución de Problemas

### **Error: "API Key no encontrada"**
```bash
# Verificar variables de entorno
echo $LINEAR_API_KEY

# Configurar manualmente
export LINEAR_API_KEY=tu_api_key_aqui
```

### **Error: "No se encontraron issues"**
- Verificar nombre del equipo en Linear
- Verificar permisos de la API Key
- Verificar que existan issues en el equipo

### **Error: "No se pudieron generar casos"**
- Verificar que los issues tengan descripciones
- Verificar formato de criterios de aceptación
- Revisar logs de error

---

**¡Desarrollado para equipos QA que usan Linear!**
"""
    
    with open("LINEAR_WORKFLOW.md", "w", encoding="utf-8") as f:
        f.write(guide_content)
    
    print("✅ Guía de flujo de trabajo creada: LINEAR_WORKFLOW.md")

if __name__ == "__main__":
    setup_linear_integration()
    create_linear_workflow_guide()
