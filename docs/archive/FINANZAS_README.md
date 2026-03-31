# 💰 Sistema de Gestión Financiera Personal

## Descripción
Sistema web completo para gestionar tus finanzas personales de manera fácil y efectiva. Controla tus ingresos, gastos, deudas y pagos mensuales recurrentes, todo en una interfaz moderna e intuitiva.

## ✨ Características Principales

### 📊 Dashboard Interactivo
- Vista general de tu situación financiera
- Tarjetas de resumen con totales de ingresos, gastos, balance y deudas
- Transacciones recientes a la vista
- Accesos rápidos a todas las funcionalidades

### 💵 Gestión de Ingresos
- Registra todos tus ingresos
- Categoriza por tipo (Salario, Freelance, Inversión, etc.)
- Agrega notas y detalles adicionales
- Visualiza histórico completo

### 💸 Control de Gastos
- Registra todos tus gastos diarios
- Categorías predefinidas (Alimentos, Transporte, Vivienda, etc.)
- Seguimiento detallado de en qué gastas tu dinero
- Análisis por categoría

### 💳 Administración de Deudas
- Registra todas tus deudas
- Visualiza progreso de pago con barras de progreso
- Registra pagos parciales
- Controla intereses y fechas límite
- Estado automático (activa/pagada)

### 🔄 Pagos Mensuales Recurrentes
- Configura pagos que realizas todos los meses
- Controla renta, servicios, suscripciones, etc.
- Visualiza cuánto pagas mensualmente en total
- Organiza por día de pago

### 📈 Reportes y Estadísticas
- Análisis de ingresos y gastos por categoría
- Tendencias mensuales (últimos 6 meses)
- Consejos financieros
- Visualización clara de tu salud financiera

## 🚀 Instalación y Uso

### Requisitos Previos
- Python 3.7 o superior
- Flask (se instalará automáticamente)

### Instalación

1. **Instalar dependencias:**
```bash
pip install flask
```

2. **Ejecutar la aplicación:**
```bash
python finanzas_app.py
```

3. **Abrir en el navegador:**
```
http://localhost:5001
```

¡Listo! El sistema creará automáticamente la base de datos la primera vez que lo ejecutes.

## 📖 Guía de Uso

### Primeros Pasos

1. **Dashboard (Inicio)**
   - Visualiza tu resumen financiero general
   - Usa los botones de acciones rápidas para agregar datos

2. **Registrar Ingresos**
   - Ve a la sección "💵 Ingresos"
   - Haz clic en "➕ Nuevo Ingreso"
   - Completa el formulario con fecha, descripción, monto y categoría
   - Guarda y verás tu ingreso en la lista

3. **Registrar Gastos**
   - Ve a la sección "💸 Gastos"
   - Haz clic en "➕ Nuevo Gasto"
   - Completa los datos del gasto
   - El sistema calculará automáticamente tu balance

4. **Gestionar Deudas**
   - Ve a "💳 Deudas"
   - Registra una nueva deuda con el acreedor, monto y fechas
   - Cuando hagas pagos, usa el botón "💵 Registrar Pago"
   - La barra de progreso se actualizará automáticamente
   - Cuando completes la deuda, se marcará como "Pagada"

5. **Configurar Pagos Mensuales**
   - Ve a "🔄 Pagos Mensuales"
   - Agrega pagos recurrentes (renta, Netflix, luz, etc.)
   - Especifica el día del mes en que pagas
   - Visualiza tu compromiso mensual total

6. **Ver Reportes**
   - Ve a "📊 Reportes"
   - Analiza tus ingresos y gastos por categoría
   - Revisa tendencias de los últimos meses
   - Identifica áreas de mejora

## 💡 Consejos Financieros

### Regla 50/30/20
- **50%** de tus ingresos para necesidades básicas
- **30%** para gastos personales y entretenimiento
- **20%** para ahorro e inversión

### Fondo de Emergencia
Crea un fondo de emergencia equivalente a 3-6 meses de tus gastos mensuales.

### Control de Deudas
Prioriza pagar deudas con mayor interés primero para ahorrar dinero a largo plazo.

### Revisión Mensual
Revisa tus finanzas al menos una vez al mes para identificar patrones y áreas de mejora.

## 🎨 Características de la Interfaz

- **Diseño Moderno**: Interfaz limpia y profesional con gradientes y animaciones sutiles
- **Responsive**: Funciona perfectamente en computadoras, tablets y móviles
- **Intuitivo**: Navegación clara y fácil de usar
- **Visual**: Tarjetas coloridas, íconos y barras de progreso para mejor comprensión
- **Notificaciones**: Mensajes de confirmación para todas las acciones

## 🗄️ Base de Datos

El sistema utiliza SQLite, una base de datos local que se crea automáticamente.

**Archivo de base de datos:** `finanzas.db`

### Tablas:
- `ingresos` - Registro de todos los ingresos
- `gastos` - Registro de todos los gastos
- `deudas` - Información de deudas
- `pagos_deuda` - Historial de pagos de deudas
- `pagos_mensuales` - Configuración de pagos recurrentes
- `historial_pagos_mensuales` - Historial de pagos mensuales realizados

## 🔒 Seguridad

- Los datos se almacenan localmente en tu computadora
- No se envía información a servidores externos
- Recomendación: Respalda regularmente tu archivo `finanzas.db`

## 📦 Respaldo de Datos

Para respaldar tus datos, simplemente copia el archivo `finanzas.db` a un lugar seguro.

Para restaurar:
1. Detén la aplicación
2. Reemplaza el archivo `finanzas.db` con tu respaldo
3. Reinicia la aplicación

## 🛠️ Solución de Problemas

### La aplicación no inicia
- Verifica que tienes Python instalado: `python --version`
- Asegúrate de tener Flask instalado: `pip install flask`

### No se guardan los datos
- Verifica que tengas permisos de escritura en la carpeta
- Revisa que el archivo `finanzas.db` se haya creado

### Error al cargar la página
- Verifica que el puerto 5001 no esté en uso
- Puedes cambiar el puerto en `finanzas_app.py` (última línea)

## 📝 Notas Adicionales

- **Puerto**: La aplicación corre en el puerto 5001 por defecto
- **Desarrollo**: Modo debug activado para mejor experiencia
- **Categorías**: Puedes personalizar las categorías editando los formularios HTML

## 🎯 Mejoras Futuras Sugeridas

- Exportación a Excel/PDF
- Gráficas y visualizaciones avanzadas
- Múltiples monedas
- Calculadora de presupuesto
- Metas de ahorro
- Recordatorios de pagos
- Comparación año tras año

## 📄 Licencia

Este proyecto es de uso personal. Siéntete libre de modificarlo según tus necesidades.

## 🤝 Soporte

Si encuentras algún problema o tienes sugerencias, no dudes en mejorar el sistema según tus necesidades.

---

**¡Toma control de tus finanzas hoy! 💪💰**

*Desarrollado con ❤️ para ayudarte a administrar mejor tu dinero*

