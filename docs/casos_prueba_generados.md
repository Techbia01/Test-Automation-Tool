TC-001 – Visualización de pestaña "Histórico de anulaciones"

Objetivo: Validar que la pestaña "Histórico de anulaciones" se muestra correctamente junto a "Refacturaciones emitidas" en la vista de detalle del Source Bill ID.

Criterio: Se muestra la pestaña "Histórico de anulaciones" junto a "Refacturaciones emitidas".

Precondiciones: El usuario debe estar en la vista de detalle de un Source Bill ID que tenga refacturaciones emitidas. El sistema debe tener acceso a la información de anulaciones asociadas.

---

TC-002 – Renderizado completo de tabla con 7 columnas

Objetivo: Verificar que la tabla muestra las 7 columnas requeridas (Note ID, Estado de la nota, Tipo, Documento asociado, CUFE, ID Partner, XML) con datos válidos.

Criterio: La tabla trae las 7 columnas y los enlaces funcionan (PDF anulación, PDF asociado, XML si aplica).

Precondiciones: Debe existir al menos una anulación asociada al Source Bill ID con todos los datos completos (Note ID, estado, tipo, documento asociado, CUFE, ID Partner, XML disponible).

---

TC-003 – Click en Note ID abre PDF en modal visor

Objetivo: Validar que al hacer clic en el Note ID (texto subrayado y clicable), se abre un modal visor con el PDF del documento de anulación.

Criterio: Interacciones: Note ID y Documento asociado son clicables y abren visor PDF en modal.

Precondiciones: Debe existir una anulación con Note ID válido y el PDF del documento de anulación debe estar disponible en el backend.

---

TC-004 – Click en Documento asociado abre PDF origen en modal

Objetivo: Verificar que al hacer clic en "Documento asociado" (texto clicable), se abre un modal visor con el PDF del documento origen que fue anulado.

Criterio: Interacciones: Note ID y Documento asociado son clicables y abren visor PDF en modal.

Precondiciones: Debe existir una anulación con documento asociado válido y el PDF del documento origen debe estar disponible en el backend.

---

TC-005 – Visualización de badge "Anulación total"

Objetivo: Validar que cuando una anulación es total, se muestra el badge/chip con el texto "Anulación total" con el estilo visual correcto.

Criterio: Estado de la nota: badges/chips con dos estados: "Anulación total" y "Anulación parcial".

Precondiciones: Debe existir al menos una anulación con estado "total" asociada al Source Bill ID.

---

TC-006 – Visualización de badge "Anulación parcial"

Objetivo: Verificar que cuando una anulación es parcial, se muestra el badge/chip con el texto "Anulación parcial" con el estilo visual correcto.

Criterio: Estado de la nota: badges/chips con dos estados: "Anulación total" y "Anulación parcial".

Precondiciones: Debe existir al menos una anulación con estado "parcial" asociada al Source Bill ID.

---

TC-007 – Copia de CUFE al hacer clic en botón copiar

Objetivo: Validar que al hacer clic en el botón copiar del campo CUFE, el valor se copia al portapapeles y se muestra feedback visual al usuario.

Criterio: CUFE copiable; XML deshabilitado cuando no aplica.

Precondiciones: Debe existir una anulación con CUFE válido asociada al Source Bill ID.

---

TC-008 – Visualización de "N/A" cuando CUFE no aplica

Objetivo: Verificar que cuando el CUFE no aplica para una anulación, se muestra el texto "N/A" en lugar del valor truncado.

Criterio: CUFE: texto truncado con botón copiar; si no aplica, mostrar "N/A".

Precondiciones: Debe existir una anulación donde el CUFE no aplica (campo null o vacío) asociada al Source Bill ID.

---

TC-009 – Copia de ID Partner al hacer clic en botón copiar

Objetivo: Validar que al hacer clic en el botón copiar del campo ID Partner, el valor se copia al portapapeles y se muestra feedback visual al usuario.

Criterio: ID Partner: valor plano con botón copiar.

Precondiciones: Debe existir una anulación con ID Partner válido asociada al Source Bill ID.

---

TC-010 – Estado vacío cuando no hay anulaciones

Objetivo: Verificar que cuando no existen anulaciones para el Source Bill ID, se muestra el mensaje "Aún no hay anulaciones para este Source Bill ID" de forma clara y consistente.

Criterio: Vacío, carga y errores con mensajes claros y consistentes con el back.

Precondiciones: El Source Bill ID debe existir pero no tener anulaciones asociadas, o el backend debe retornar una lista vacía de anulaciones.

---

TC-011 – Estado de carga durante petición al backend

Objetivo: Validar que mientras se realiza la petición al backend para obtener las anulaciones, se muestra un indicador de carga (loading) apropiado.

Criterio: Vacío, carga y errores con mensajes claros y consistentes con el back.

Precondiciones: El usuario debe estar en la vista de detalle del Source Bill ID y la petición al backend debe estar en proceso (simular delay de red).

---

TC-012 – Manejo de error cuando backend retorna error 500

Objetivo: Verificar que cuando el backend retorna un error 500 (Error interno del servidor), se muestra un mensaje de error claro y consistente con el diseño del sistema.

Criterio: Vacío, carga y errores con mensajes claros y consistentes con el back.

Precondiciones: El backend debe estar configurado para retornar un error 500 al consultar las anulaciones del Source Bill ID.

---

TC-013 – Manejo de error cuando backend retorna error 404

Objetivo: Validar que cuando el Source Bill ID no existe o no tiene permisos, el backend retorna 404 y se muestra un mensaje de error apropiado.

Criterio: Vacío, carga y errores con mensajes claros y consistentes con el back.

Precondiciones: El Source Bill ID debe ser inválido o el usuario no debe tener permisos para acceder a él.

---

TC-014 – XML deshabilitado cuando no aplica

Objetivo: Verificar que cuando el XML no aplica para una anulación, el botón/enlace de XML está deshabilitado y visualmente indicado como no disponible.

Criterio: CUFE copiable; XML deshabilitado cuando no aplica.

Precondiciones: Debe existir una anulación donde el XML no aplica (campo null, vacío o flag indicando no disponible) asociada al Source Bill ID.

---

TC-015 – XML habilitado y funcional cuando aplica

Objetivo: Validar que cuando el XML está disponible para una anulación, el enlace funciona correctamente y permite descargar o visualizar el XML.

Criterio: La tabla trae las 7 columnas y los enlaces funcionan (PDF anulación, PDF asociado, XML si aplica).

Precondiciones: Debe existir una anulación con XML disponible asociada al Source Bill ID.

---

TC-016 – Tooltip en Documento asociado

Objetivo: Verificar que al pasar el mouse sobre "Documento asociado", se muestra un tooltip con el texto "Documento originario de la anulación".

Criterio: Tooltip en Documento asociado: "Documento originario de la anulación".

Precondiciones: Debe existir una anulación con documento asociado válido en la tabla.

---

TC-017 – Consistencia visual con pestaña Refacturaciones emitidas

Objetivo: Validar que el diseño, colores, tipografía y espaciado de la pestaña "Histórico de anulaciones" mantiene consistencia visual con la pestaña "Refacturaciones emitidas".

Criterio: Mantener consistencia visual con la pestaña de Refacturaciones emitidas.

Precondiciones: El usuario debe poder ver ambas pestañas (Refacturaciones emitidas e Histórico de anulaciones) en la misma vista para comparar.

---

TC-018 – Verificación de solo lectura (no inicia anulación)

Objetivo: Confirmar que desde la pestaña "Histórico de anulaciones" no se puede iniciar una nueva anulación (no hay botones o acciones que permitan crear anulación).

Criterio: Solo consulta: desde esta pestaña no se inicia una nueva anulación (la anulación se dispara desde la tabla de refacturaciones emitidas).

Precondiciones: El usuario debe estar en la pestaña "Histórico de anulaciones" con permisos para crear anulaciones (si los tuviera).

---

TC-019 – Truncado de CUFE cuando es muy largo

Objetivo: Validar que cuando el CUFE es muy largo, se muestra truncado con puntos suspensivos y el botón copiar permite copiar el valor completo.

Criterio: CUFE: texto truncado con botón copiar; si no aplica, mostrar "N/A".

Precondiciones: Debe existir una anulación con CUFE de más de 50 caracteres asociada al Source Bill ID.

---

TC-020 – Navegación entre pestañas mantiene estado

Objetivo: Verificar que al cambiar entre la pestaña "Refacturaciones emitidas" y "Histórico de anulaciones", el estado de la vista se mantiene y no se pierde información.

Criterio: En la vista de detalle de un Source Bill ID, agregar pestañas: Refacturaciones emitidas e Histórico de anulaciones (esta HU).

Precondiciones: El usuario debe estar en la vista de detalle de un Source Bill ID con ambas pestañas disponibles.

---

TC-021 – Error al abrir PDF de anulación no disponible

Objetivo: Validar que cuando el PDF del documento de anulación no está disponible en el backend, se muestra un mensaje de error apropiado al intentar abrirlo.

Criterio: Interacciones: Note ID y Documento asociado son clicables y abren visor PDF en modal.

Precondiciones: Debe existir una anulación con Note ID válido pero el PDF del documento de anulación no está disponible o fue eliminado del servidor.

---

TC-022 – Error al abrir PDF de documento asociado no disponible

Objetivo: Verificar que cuando el PDF del documento origen no está disponible en el backend, se muestra un mensaje de error apropiado al intentar abrirlo desde "Documento asociado".

Criterio: Interacciones: Note ID y Documento asociado son clicables y abren visor PDF en modal.

Precondiciones: Debe existir una anulación con documento asociado válido pero el PDF del documento origen no está disponible o fue eliminado del servidor.

---

TC-023 – Visualización de tipo "NC" (Nota de Crédito)

Objetivo: Validar que cuando el tipo de anulación es "NC", se muestra correctamente en la columna Tipo de la tabla.

Criterio: Tipo: "NC" o "ND".

Precondiciones: Debe existir al menos una anulación con tipo "NC" asociada al Source Bill ID.

---

TC-024 – Visualización de tipo "ND" (Nota de Débito)

Objetivo: Verificar que cuando el tipo de anulación es "ND", se muestra correctamente en la columna Tipo de la tabla.

Criterio: Tipo: "NC" o "ND".

Precondiciones: Debe existir al menos una anulación con tipo "ND" asociada al Source Bill ID.

---

TC-025 – Tabla con múltiples anulaciones (paginación o scroll)

Objetivo: Validar que cuando hay múltiples anulaciones (más de 10), la tabla maneja correctamente la visualización mediante paginación o scroll infinito, manteniendo todas las funcionalidades.

Criterio: La tabla trae las 7 columnas y los enlaces funcionan (PDF anulación, PDF asociado, XML si aplica).

Precondiciones: Debe existir más de 10 anulaciones asociadas al Source Bill ID para probar el comportamiento con grandes volúmenes de datos.

