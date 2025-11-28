# 🔗 **Guía: Importar Casos de Prueba como Sub-issues en Linear**

## 🎯 **¿Qué es esto?**

Esta funcionalidad te permite exportar todos los casos de prueba generados como **sub-issues** de una Historia de Usuario existente en Linear, manteniendo la trazabilidad completa.

## 📋 **Estructura Resultante**

```
📋 FIN-1294: FRONT | Ajuste en visual de tarifas de subsidios en Olibia
├── 🧪 TC-001: Verificar visualización de tarifas
├── 🧪 TC-002: Validar cálculo de subsidios  
├── 🧪 TC-003: Probar responsive design
└── 🧪 TC-004: Verificar integración con backend
```

## 🚀 **Proceso Paso a Paso**

### **📝 Paso 1: Generar Casos de Prueba**

1. **Crear Historia de Usuario** en tu sistema:
   ```
   Historia: FRONT | Ajuste en visual de tarifas de subsidios en Olibia
   Descripción: Replicar en olibia misma vista que la de la landing
   
   Criterios de Aceptación:
   1. Dado que soy un usuario de Olibia
      Cuando accedo a la sección de tarifas
      Entonces debo ver el mismo diseño que en landing
   
   2. Dado que visualizo las tarifas
      Cuando hay subsidios aplicables
      Entonces debo ver los descuentos claramente
   ```

2. **Generar casos** usando el sistema
3. **Validar calidad** de los casos generados

### **📤 Paso 2: Exportar como Sub-issues**

1. **En la página del proyecto**, hacer clic en:
   ```
   🔗 Exportar como Sub-issues
   ```

2. **Ingresar ID de la HU** en Linear:
   ```
   Ejemplo: FIN-1294
   ```

3. **Descargar CSV** generado:
   ```
   Archivo: linear_subissues_Ajuste_visual_tarifas_20241001_1430.csv
   ```

### **📥 Paso 3: Importar en Linear**

1. **Abrir Linear** → Tu workspace
2. **Ir a Issues** → **Import** → **CSV**
3. **Subir el archivo** CSV generado
4. **Mapear columnas:**

| CSV Column | Linear Field | ✅ Verificar |
|------------|--------------|-------------|
| `Title` | **Title** | ✅ |
| `Description` | **Description** | ✅ |
| `Labels` | **Labels** | ✅ |
| `Priority` | **Priority** | ✅ |
| `Parent` | **Parent** | ⚠️ **CRÍTICO** |
| `Type` | **Issue Type** | ✅ |
| `State` | **State** | ✅ |

5. **Configurar opciones:**
   ```
   ✅ Create missing labels: ON
   ✅ Team: QA (o tu equipo)
   ✅ Project: Subsidios PT1
   ```

6. **Importar** y verificar

## 📊 **Formato del CSV Generado**

### **🔍 Ejemplo de Contenido:**

```csv
Title,Description,Labels,Priority,Type,State,Parent,Project,Created
"TC-001: Verificar visualización de tarifas","**Objetivo:** Verificar visualización de tarifas

**Precondiciones:**
1. Usuario logueado en Olibia
2. Acceso a sección de tarifas

**Descripción (formato Gherkin):**
1. Navegar a sección de tarifas
2. Verificar que el diseño coincide con landing
3. Validar elementos visuales

**Resultado Esperado:** Diseño idéntico a landing

---
**Tipo:** Funcional
**Prioridad:** Alta","Test_Case, Type_funcional, Priority_alta","Urgent","Test Case","Todo","FIN-1294","Subsidios PT1","2024-10-01"
```

### **🔑 Campos Clave:**

- **Parent:** `FIN-1294` - Vincula con la HU
- **Title:** `TC-001: ...` - Formato estándar
- **Type:** `Test Case` - Identifica como caso de prueba
- **Labels:** Incluye `Test_Case` + tipo + prioridad

## ✅ **Verificación Post-Importación**

### **📋 Checklist:**

1. **Estructura correcta:**
   ```
   ✅ Todos los casos aparecen como sub-issues
   ✅ Parent issue es correcto (FIN-1294)
   ✅ Títulos con formato TC-XXX
   ```

2. **Metadatos correctos:**
   ```
   ✅ Etiquetas asignadas (Test_Case, Type_*, Priority_*)
   ✅ Prioridades mapeadas (Alta→Urgent, Media→High)
   ✅ Estados en "Todo"
   ✅ Tipo "Test Case"
   ```

3. **Contenido formateado:**
   ```
   ✅ Descripciones en Markdown
   ✅ Precondiciones listadas
   ✅ Pasos Gherkin estructurados
   ✅ Resultados esperados claros
   ```

## 🎯 **Ventajas de esta Implementación**

### **✅ Para el Equipo QA:**
- **Trazabilidad completa** HU → Casos de prueba
- **Seguimiento granular** de cada caso
- **Asignación individual** a testers
- **Métricas automáticas** de progreso

### **✅ Para Project Management:**
- **Visibilidad clara** del progreso de testing
- **Estimación precisa** de esfuerzo QA
- **Reportes automáticos** de cobertura
- **Integración** con workflows existentes

### **✅ Para Desarrollo:**
- **Contexto claro** de qué se está probando
- **Feedback directo** en cada caso
- **Bloqueos específicos** identificables
- **Colaboración mejorada** con QA

## 🔧 **Solución de Problemas**

### **❌ Error: "Parent issue not found"**
**✅ Solución:** Verificar que el ID ingresado existe y es accesible

### **❌ Error: "Invalid parent format"**
**✅ Solución:** Usar formato correcto: `TEAM-NUMBER` (ej: FIN-1294)

### **❌ Sub-issues no aparecen vinculados**
**✅ Solución:** Verificar mapeo de columna `Parent` en importación

### **❌ Etiquetas no se crean**
**✅ Solución:** Activar "Create missing labels" en importación

## 🚀 **Ejemplo Completo**

### **📋 Historia de Usuario Original:**
```
ID: FIN-1294
Título: FRONT | Ajuste en visual de tarifas de subsidios en Olibia
Estado: In Progress
Asignado: mateo.ortiz
Proyecto: Subsidios PT1
```

### **🧪 Casos de Prueba Generados:**
```
TC-001: Verificar layout responsive de tarifas
TC-002: Validar cálculo visual de subsidios
TC-003: Probar integración con datos backend
TC-004: Verificar accesibilidad de componentes
TC-005: Validar comportamiento en diferentes browsers
```

### **📊 Resultado en Linear:**
```
FIN-1294 (Parent Issue)
├── TC-001 (Sub-issue) - Estado: Todo, Asignado: tester1
├── TC-002 (Sub-issue) - Estado: In Progress, Asignado: tester2  
├── TC-003 (Sub-issue) - Estado: Done, Asignado: tester1
├── TC-004 (Sub-issue) - Estado: Todo, Asignado: tester3
└── TC-005 (Sub-issue) - Estado: Todo, Sin asignar
```

## 🎉 **¡Listo para Usar!**

Con esta implementación tienes:

✅ **Integración completa** con Linear  
✅ **Trazabilidad perfecta** HU → Casos  
✅ **Workflow organizado** para QA  
✅ **Métricas automáticas** de progreso  
✅ **Colaboración mejorada** entre equipos  

**¡Tu proceso de QA ahora está completamente integrado con Linear!** 🚀
