# 📝 Guía para Escribir Historias de Usuario Óptimas para QA Automation

## 🎯 Objetivo
Esta guía te ayuda a escribir HUs que el sistema pueda **procesar correctamente** y generar **casos de prueba completos**.

---

## ✅ **Formato Recomendado para HUs**

### **Estructura Básica (Mínimo)**

```
🧩 Historia de Usuario
Como [ROL]
Quiero [FUNCIONALIDAD]
Para [BENEFICIO]

📝 Descripción
[Descripción breve del contexto y la solución]

✅ Criterios de Aceptación
1. Given [contexto] When [acción] Then [resultado esperado]
2. Given [contexto] When [acción] Then [resultado esperado]
3. Given [contexto] When [acción] Then [resultado esperado]
```

### **Estructura Completa (HUs Técnicas)**

```
🧩 Historia de Usuario
Como [ROL]
Quiero [FUNCIONALIDAD]
Para [BENEFICIO]

👀 Contexto
[Descripción del problema actual y dependencias]

📝 Descripción
[Explicación de la solución propuesta]

📝 Lógica de Negocio (Opcional para HUs técnicas)
- Validación 1: [descripción]
- Validación 2: [descripción]
- Operación 1: [descripción]

✅ Criterios de Aceptación
1. Given [contexto inicial] When [usuario realiza acción] Then [sistema responde correctamente]
2. Given [evento de actualización] When [se procesa] Then [campos actualizados]
3. Given [evento duplicado] When [se procesa] Then [no se insertan duplicados]
4. Given [error en servicio externo] When [falla integración] Then [sistema maneja error graciosamente]
5. Given [validación de campos] When [datos inválidos] Then [muestra mensaje de error]
```

---

## 🚨 **Problemas Comunes y Soluciones**

### ❌ **Problema 1: Criterios muy generales o pocos**

**MAL:**
```
✅ Criterios de Aceptación
1. El sistema debe funcionar correctamente
2. Los datos deben guardarse
```

**BIEN:**
```
✅ Criterios de Aceptación
1. Given un evento de creación válido When el consumidor lo recibe Then se inserta contacto con contratos y emails en BD
2. Given un evento con email duplicado When se procesa Then se rechaza con código 409 y mensaje descriptivo
3. Given un evento sin campos obligatorios When se valida Then se rechaza con lista de campos faltantes
4. Given una integración con MS externo When el MS falla Then se revierte la transacción y se loguea el error
5. Given datos correctos When se guardan Then se confirma persistencia y se retorna ID generado
```

---

### ❌ **Problema 2: HU muy larga con mucha documentación técnica**

**MAL:**
- 8000+ caracteres de documentación
- Ejemplos JSON extensos
- Enlaces a Google Docs
- Campos obligatorios listados (mejor en esquema técnico aparte)

**BIEN:**
- Separar la **HU funcional** de la **especificación técnica**
- La HU debe tener **máximo 2000-3000 caracteres**
- Documentación técnica (JSON schemas, ejemplos) → **archivo aparte** o **enlace**

**Ejemplo de HU bien estructurada:**

```
🧩 HU: Sincronización de usuarios desde Kafka a BD de contactos

Como equipo de IA
Quiero consumir eventos Kafka de usuarios (creación/edición/eliminación)
Para mantener sincronizada la BD de contactos en tiempo real

👀 Contexto
- Fuente: tópicos Kafka de Nebula (user-creation, user-update, user-contract-deletion)
- Dependencia: Usuario debe existir en Firebase Auth (UID)
- BD destino: prod-bia-watt (tablas: contacts, emails, phones, user_contact_contracts)

✅ Criterios de Aceptación

**Creación:**
1. Given evento de creación válido con email, nombre, contratos When se consume Then se crea contacto + emails + phones + contratos en BD
2. Given evento sin campos obligatorios When se valida Then se rechaza y loguea error sin persistir nada
3. Given email duplicado When se intenta crear Then se retorna 409 con mensaje descriptivo

**Actualización:**
4. Given evento de actualización con cambios When se procesa Then se actualizan solo campos modificados
5. Given contacto inexistente When llega update Then se loguea error y no se crea registro nuevo

**Eliminación:**
6. Given evento de eliminación de contrato When se procesa Then se marca deleted_at en user_contact_contracts
7. Given último contrato de un contacto When se elimina Then se valida que no quede contacto huérfano

**Integraciones:**
8. Given require_ems_access=true When se crea contacto Then se crea usuario en MS-users y se asocian contratos
9. Given falla creación en MS-users When se detecta error Then se revierte creación en BD principal

**Idempotencia:**
10. Given evento duplicado (mismo user_id + timestamp) When se procesa Then se ignora sin error

📎 Ver especificación técnica completa: [LINK A DOC TÉCNICO]
```

---

### ❌ **Problema 3: Criterios sin formato Given/When/Then**

**MAL:**
```
✅ Criterios
- Validar campos obligatorios
- Guardar datos correctamente
- Manejar errores
```

**BIEN:**
```
✅ Criterios de Aceptación
1. Given datos con campos obligatorios faltantes When se validan Then se rechaza con lista específica de errores
2. Given datos válidos When se guardan Then se persisten en BD y se retorna ID de confirmación
3. Given error en servicio externo When se detecta When se loguea error y se retorna 500 con mensaje descriptivo
```

---

## 📊 **¿Cuántos Criterios Incluir?**

| Tipo de HU | Criterios Mínimos | Criterios Recomendados |
|------------|-------------------|------------------------|
| **Simple** (CRUD básico) | 3-5 | 5-8 |
| **Media** (con validaciones) | 5-8 | 8-12 |
| **Compleja** (integraciones, Kafka) | 8-12 | 12-20 |

**Tip:** Si tienes **menos de 5 criterios**, probablemente estés siendo muy genérico.

---

## 🧪 **Checklist antes de enviar HU a QA**

- [ ] Tiene formato Given/When/Then en al menos 80% de criterios
- [ ] Cada criterio es **específico y verificable**
- [ ] Incluye casos positivos (happy path)
- [ ] Incluye casos negativos (validaciones, errores)
- [ ] Menciona integraciones con servicios externos
- [ ] Define qué pasa cuando algo falla
- [ ] Documentación técnica está **separada** o enlazada
- [ ] Tiene entre **5-15 criterios** dependiendo complejidad

---

## 💡 **Tips para Equipos Técnicos (AIA, EMS, OPS)**

### Para HUs de **Integraciones/APIs/Kafka:**

Siempre incluir criterios para:
1. ✅ Happy path (datos válidos)
2. ❌ Validaciones (campos faltantes, formatos incorrectos)
3. 🔄 Idempotencia (eventos duplicados)
4. ⚠️ Manejo de errores (fallos de red, timeouts, servicios caídos)
5. 🔗 Integraciones exitosas y fallidas
6. 🗄️ Persistencia de datos (commit/rollback)

### Ejemplo de criterios robustos:

```
✅ Criterios de Aceptación - Consumo de Kafka

**Happy Path:**
1. Given evento válido en tópico When consumer lo procesa Then se parsea correctamente y se persiste en BD

**Validaciones:**
2. Given payload sin campo email When se valida Then se rechaza y loguea error específico
3. Given formato de teléfono inválido When se parsea Then se normaliza con formato por defecto

**Idempotencia:**
4. Given mismo evento consumido 2 veces When se detecta duplicado Then se ignora sin error

**Errores e Integraciones:**
5. Given BD no disponible When se intenta persistir Then se reintenta con backoff exponencial
6. Given MS-users retorna 500 When se crea usuario Then se loguea, se revierte transacción y se retorna error
7. Given timeout en MS-users When pasan 30s Then se cancela operación y se marca para retry

**Casos Especiales:**
8. Given evento de eliminación del último contrato When se valida Then se alerta y no se deja contacto huérfano
```

---

## 🚀 **Resultado Esperado**

Con HUs bien escritas, el sistema generará:
- ✅ **8-15 casos de prueba** automáticamente
- ✅ Casos de prueba **específicos y accionables**
- ✅ Cobertura de **happy path + edge cases**
- ✅ Casos negativos y de manejo de errores
- ✅ Listos para subir a Linear como sub-issues

---

## 📞 **¿Necesitas Ayuda?**

Si tienes dudas sobre cómo estructurar tu HU, contacta al equipo de QA antes de empezar desarrollo.

**¡Mejor HU = Mejores Test Cases = Menos Bugs en Producción!** 🎉

