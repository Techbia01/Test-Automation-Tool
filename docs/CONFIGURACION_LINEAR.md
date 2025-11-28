# 🔧 Configuración de Linear para Importación de Casos de Prueba

## 📋 **Preparación en Linear**

### **Paso 1: Crear Etiquetas (Labels) en Linear**

Antes de importar los casos de prueba, necesitas crear las siguientes etiquetas en tu proyecto de Linear:

#### **Etiquetas Obligatorias:**
- `Test_Case` - Identifica todos los casos de prueba
- `Type_Funcional` - Para casos de prueba funcionales
- `Type_Integracion` - Para casos de prueba de integración
- `Type_Negativo` - Para casos de prueba negativos
- `Type_Caso_Limite` - Para casos de prueba de casos límite
- `Priority_Alta` - Para casos de alta prioridad
- `Priority_Media` - Para casos de media prioridad
- `Priority_Baja` - Para casos de baja prioridad

#### **Cómo crear etiquetas en Linear:**
1. Ve a tu proyecto en Linear
2. Haz clic en **"Settings"** (Configuración)
3. Selecciona **"Labels"** (Etiquetas)
4. Haz clic en **"Create label"** (Crear etiqueta)
5. Agrega cada etiqueta de la lista anterior

### **Paso 2: Configurar Estados (States)**

Asegúrate de tener estos estados en tu proyecto:
- `Todo` - Para casos de prueba pendientes
- `In Progress` - Para casos en ejecución
- `Done` - Para casos completados
- `Blocked` - Para casos bloqueados

### **Paso 3: Configurar Tipos de Issues**

Asegúrate de tener el tipo:
- `Test Case` - Para identificar casos de prueba

## 📥 **Importación del Archivo CSV**

### **Paso 1: Descargar el Archivo**
1. En la aplicación web, genera tus casos de prueba
2. Haz clic en **"Exportar para Linear"**
3. Se descargará un archivo CSV con nombre: `linear_test_cases_[proyecto]_[fecha].csv`

### **Paso 2: Importar en Linear**
1. Ve a tu proyecto en Linear
2. Haz clic en **"..."** (más opciones) en la parte superior
3. Selecciona **"Import issues"** (Importar issues)
4. Selecciona **"CSV"** como formato
5. Sube el archivo CSV descargado
6. Mapea las columnas:
   - `Title` → **Title**
   - `Description` → **Description**
   - `Labels` → **Labels**
   - `Priority` → **Priority**
   - `Type` → **Type**
   - `State` → **State**
   - `Assignee` → **Assignee** (opcional)

### **Paso 3: Verificar la Importación**
1. Revisa que los casos se importaron correctamente
2. Verifica que las etiquetas se asignaron
3. Confirma que las prioridades se mapearon correctamente
4. Revisa que las descripciones se muestran bien formateadas

## 📊 **Estructura del Archivo CSV**

El archivo CSV generado contiene las siguientes columnas:

| Columna | Descripción | Ejemplo |
|---------|-------------|---------|
| `Title` | Título del caso de prueba | `TC-001: Verificar login con credenciales válidas` |
| `Description` | Descripción completa en formato Markdown | `**Objetivo:** ...` |
| `Labels` | Etiquetas separadas por comas | `Test_Case, Type_Funcional, Priority_Alta` |
| `Priority` | Prioridad mapeada a Linear | `Urgent`, `High`, `Normal` |
| `Type` | Tipo de issue | `Test Case` |
| `State` | Estado inicial | `Todo` |
| `Assignee` | Asignado (vacío por defecto) | `` |
| `Project` | Nombre del proyecto | `Sistema de Login` |
| `Created` | Fecha de creación | `2025-09-10` |
| `Test_ID` | ID original del caso | `TC-001` |
| `Test_Type` | Tipo de prueba original | `Funcional` |
| `Original_Priority` | Prioridad original | `Alta` |
| `Tags` | Tags originales | `login, autenticación` |
| `User_Story` | Historia de usuario | `Como usuario del sistema...` |

## 🎯 **Formato de Descripción en Linear**

Cada caso de prueba se importa con una descripción estructurada:

```
**Objetivo:** [Título del caso de prueba]

**Descripción:** [Descripción detallada]

**Precondiciones:**
1. [Precondición 1]
2. [Precondición 2]

**Pasos de Ejecución:**
1. [Paso 1]
2. [Paso 2]
3. [Paso 3]

**Resultado Esperado:** [Resultado esperado]

---
**Tipo:** [Funcional/Integración/Negativo/etc.]
**Prioridad:** [Alta/Media/Baja]
**Tags:** [tag1, tag2, tag3]

**Contexto HU:** [Historia de usuario relacionada]
```

## 🔧 **Solución de Problemas**

### **Error: "Label not found"**
- **Solución**: Crea las etiquetas faltantes en Linear antes de importar

### **Error: "Invalid priority"**
- **Solución**: Verifica que tu proyecto Linear tenga las prioridades: `Urgent`, `High`, `Normal`

### **Error: "Invalid type"**
- **Solución**: Asegúrate de tener el tipo `Test Case` en tu proyecto

### **Caracteres especiales no se muestran bien**
- **Solución**: El archivo CSV usa UTF-8, asegúrate de que Linear lo importe con la codificación correcta

### **Descripción se ve mal formateada**
- **Solución**: Linear soporta Markdown, las descripciones deberían formatearse automáticamente

## ✅ **Verificación Post-Importación**

Después de importar, verifica que:

1. ✅ **Todos los casos se importaron** - Revisa el número total
2. ✅ **Las etiquetas se asignaron** - Cada caso debe tener `Test_Case` y otras etiquetas
3. ✅ **Las prioridades son correctas** - Alta→Urgent, Media→High, Baja→Normal
4. ✅ **Las descripciones se ven bien** - Formato Markdown aplicado
5. ✅ **Los estados son correctos** - Todos en `Todo` por defecto
6. ✅ **Los tipos son correctos** - Todos como `Test Case`

## 🎉 **¡Listo para Usar!**

Con esta configuración, podrás:
- ✅ Importar casos de prueba directamente desde la aplicación web
- ✅ Mantener la estructura y formato profesional
- ✅ Organizar casos con etiquetas y prioridades
- ✅ Gestionar el flujo de trabajo en Linear
- ✅ Mantener trazabilidad desde HU hasta casos de prueba

**¡Tu equipo QA ahora tiene una integración completa con Linear!**
