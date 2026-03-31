# 🚀 Guía Rápida - Sistema de Finanzas Personales

## Inicio Rápido en 3 Pasos

### 1️⃣ Instalar Flask (si no lo tienes)
```bash
pip install flask
```

### 2️⃣ Iniciar la Aplicación

**En Windows:**
- Doble clic en `iniciar_finanzas.bat`

**O manualmente:**
```bash
python finanzas_app.py
```

### 3️⃣ Abrir en el Navegador
```
http://localhost:5001
```

## 📱 Uso Básico

### ➕ Agregar un Ingreso
1. Click en "💵 Ingresos" en el menú
2. Click en "➕ Nuevo Ingreso"
3. Llenar: fecha, descripción, monto
4. Guardar

### ➖ Agregar un Gasto
1. Click en "💸 Gastos"
2. Click en "➕ Nuevo Gasto"
3. Llenar datos
4. Guardar

### 💳 Registrar una Deuda
1. Click en "💳 Deudas"
2. Click en "➕ Nueva Deuda"
3. Ingresar acreedor, monto total, fechas
4. Para pagar: Click en "💵 Registrar Pago"

### 🔄 Configurar Pago Mensual
1. Click en "🔄 Pagos Mensuales"
2. Click en "➕ Nuevo Pago Mensual"
3. Nombre (ej: Netflix, Renta, Luz)
4. Monto y día del mes
5. Guardar

### 📊 Ver Reportes
Click en "📊 Reportes" para ver:
- Gastos por categoría
- Ingresos por categoría
- Tendencias mensuales

## 💡 Tips

✅ Registra tus transacciones diariamente
✅ Usa categorías para mejor análisis
✅ Revisa tu dashboard semanalmente
✅ Paga tus deudas con mayor interés primero
✅ Mantén un fondo de emergencia

## 🎯 Meta Financiera Simple

1. **Ingresos > Gastos** = ✅ Vas bien
2. **Gastos > Ingresos** = ⚠️ Reducir gastos
3. **Ahorro recomendado**: 20% de ingresos

## 🔧 Solución Rápida de Problemas

**No inicia:**
```bash
pip install flask
python finanzas_app.py
```

**Puerto ocupado:**
Edita `finanzas_app.py`, última línea, cambia `port=5001` por otro número

**Datos perdidos:**
Tu base de datos está en `finanzas.db` - ¡respáldala!

---

¡Disfruta tu sistema de finanzas! 💰✨

