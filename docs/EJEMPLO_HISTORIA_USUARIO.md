# 📝 Ejemplo de Historia de Usuario

Este documento muestra el formato recomendado para escribir Historias de Usuario que el sistema puede procesar correctamente.

---

## ✅ Formato Recomendado

```
Título: [Breve descripción de la funcionalidad]

Contexto:
[Descripción del contexto o problema que se resuelve]

Descripción:
Como [rol/usuario], quiero [acción/funcionalidad] para [beneficio/objetivo].

Criterios de aceptación:
✅ Criterio 1: [Descripción clara del criterio]
✅ Criterio 2: [Descripción clara del criterio]
✅ Criterio 3: [Descripción clara del criterio]
```

---

## 📋 Ejemplo Completo

```
Título: Visualización de Anulaciones en Source Bill ID

Contexto:
Los usuarios necesitan ver el histórico de anulaciones asociadas a un Source Bill ID específico para poder rastrear y auditar las operaciones realizadas.

Descripción:
Como usuario del sistema de facturación, quiero visualizar el histórico de anulaciones asociadas a un Source Bill ID para poder rastrear y auditar las operaciones realizadas.

Criterios de aceptación:
✅ Se muestra la pestaña "Histórico de anulaciones" junto a "Refacturaciones emitidas"
✅ Al hacer clic en la pestaña, se muestra una tabla con las anulaciones asociadas al Source Bill ID
✅ Cada fila muestra: ID de anulación, fecha, motivo, estado
✅ El ID de anulación es copiable al portapapeles
✅ Al hacer clic en una fila, se abre un modal visor con el PDF y XML de la anulación
✅ Si no hay anulaciones, se muestra un mensaje de estado vacío
✅ Si hay error del backend, se muestra un mensaje de error apropiado
```

---

## 🎯 Formatos Alternativos

El sistema también acepta otros formatos:

### Con Bullets
```
Criterios de aceptación:
- Criterio 1: Descripción
- Criterio 2: Descripción
- Criterio 3: Descripción
```

### Con Numeración
```
Criterios de aceptación:
1. Criterio 1: Descripción
2. Criterio 2: Descripción
3. Criterio 3: Descripción
```

### Formato Gherkin
```
Criterios de aceptación:
Given que el usuario accede al módulo
When el usuario selecciona un Source Bill ID
Then se muestra la tabla de anulaciones
```

### Texto Libre
```
Criterios de aceptación:
El sistema debe mostrar la pestaña de anulaciones.
Cuando el usuario hace clic, debe cargar la tabla con los datos.
Si no hay datos, debe mostrar un mensaje apropiado.
```

---

## 💡 Consejos

1. **Sé específico**: Describe exactamente qué debe hacer el sistema
2. **Usa verbos claros**: "muestra", "valida", "guarda", "elimina"
3. **Incluye casos de error**: "Si hay error, muestra mensaje apropiado"
4. **Menciona elementos UI**: "botón", "tabla", "modal", "tooltip"
5. **Describe estados**: "vacío", "cargando", "error", "éxito"

---

## 🚀 El Sistema Generará

Para cada criterio, el sistema generará múltiples casos de prueba:

- ✅ Caso feliz (happy path)
- ✅ Estado vacío
- ✅ Manejo de errores
- ✅ Usabilidad
- ✅ Validaciones
- ✅ Y más según el tipo de criterio

**¡Mientras más detallada sea tu HU, mejores casos de prueba se generarán!**

