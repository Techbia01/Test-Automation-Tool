"""
Sistema de Gestión Financiera Personal
Aplicación web para controlar ingresos, gastos, deudas y pagos recurrentes
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
from datetime import datetime, timedelta
import sqlite3
import json
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'finanzas-personales-2025'

# Configuración de base de datos
DATABASE = 'finanzas.db'

def get_db_connection():
    """Crea conexión a la base de datos"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Inicializa la base de datos con las tablas necesarias"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Tabla de ingresos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ingresos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha DATE NOT NULL,
            descripcion TEXT NOT NULL,
            monto REAL NOT NULL,
            categoria TEXT,
            notas TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabla de gastos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gastos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha DATE NOT NULL,
            descripcion TEXT NOT NULL,
            monto REAL NOT NULL,
            categoria TEXT,
            notas TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabla de deudas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS deudas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            acreedor TEXT NOT NULL,
            monto_total REAL NOT NULL,
            monto_pagado REAL DEFAULT 0,
            fecha_inicio DATE NOT NULL,
            fecha_limite DATE,
            interes REAL DEFAULT 0,
            estado TEXT DEFAULT 'activa',
            notas TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabla de pagos de deudas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pagos_deuda (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            deuda_id INTEGER NOT NULL,
            fecha DATE NOT NULL,
            monto REAL NOT NULL,
            notas TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (deuda_id) REFERENCES deudas (id)
        )
    ''')
    
    # Tabla de pagos recurrentes mensuales
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pagos_mensuales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            monto REAL NOT NULL,
            dia_pago INTEGER NOT NULL,
            categoria TEXT,
            activo INTEGER DEFAULT 1,
            notas TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabla de historial de pagos mensuales
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS historial_pagos_mensuales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pago_mensual_id INTEGER NOT NULL,
            fecha_pago DATE NOT NULL,
            monto REAL NOT NULL,
            pagado INTEGER DEFAULT 0,
            notas TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (pago_mensual_id) REFERENCES pagos_mensuales (id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Base de datos inicializada correctamente")

# Rutas principales
@app.route('/')
def index():
    """Página principal - Dashboard"""
    conn = get_db_connection()
    
    # Obtener resumen financiero
    total_ingresos = conn.execute('SELECT SUM(monto) as total FROM ingresos').fetchone()['total'] or 0
    total_gastos = conn.execute('SELECT SUM(monto) as total FROM gastos').fetchone()['total'] or 0
    total_deudas = conn.execute('SELECT SUM(monto_total - monto_pagado) as total FROM deudas WHERE estado = "activa"').fetchone()['total'] or 0
    
    # Transacciones recientes
    ingresos_recientes = conn.execute('SELECT * FROM ingresos ORDER BY fecha DESC LIMIT 5').fetchall()
    gastos_recientes = conn.execute('SELECT * FROM gastos ORDER BY fecha DESC LIMIT 5').fetchall()
    
    # Pagos mensuales pendientes
    pagos_mensuales = conn.execute('SELECT * FROM pagos_mensuales WHERE activo = 1').fetchall()
    
    conn.close()
    
    balance = total_ingresos - total_gastos
    
    return render_template('finanzas/index.html',
                         total_ingresos=total_ingresos,
                         total_gastos=total_gastos,
                         total_deudas=total_deudas,
                         balance=balance,
                         ingresos_recientes=ingresos_recientes,
                         gastos_recientes=gastos_recientes,
                         pagos_mensuales=pagos_mensuales)

# INGRESOS
@app.route('/ingresos')
def ingresos():
    """Página de gestión de ingresos"""
    conn = get_db_connection()
    ingresos = conn.execute('SELECT * FROM ingresos ORDER BY fecha DESC').fetchall()
    conn.close()
    return render_template('finanzas/ingresos.html', ingresos=ingresos)

@app.route('/api/ingresos', methods=['POST'])
def agregar_ingreso():
    """Agregar nuevo ingreso"""
    data = request.json
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO ingresos (fecha, descripcion, monto, categoria, notas)
        VALUES (?, ?, ?, ?, ?)
    ''', (data['fecha'], data['descripcion'], data['monto'], 
          data.get('categoria', ''), data.get('notas', '')))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Ingreso registrado correctamente'})

@app.route('/api/ingresos/<int:id>', methods=['DELETE'])
def eliminar_ingreso(id):
    """Eliminar ingreso"""
    conn = get_db_connection()
    conn.execute('DELETE FROM ingresos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Ingreso eliminado'})

# GASTOS
@app.route('/gastos')
def gastos():
    """Página de gestión de gastos"""
    conn = get_db_connection()
    gastos = conn.execute('SELECT * FROM gastos ORDER BY fecha DESC').fetchall()
    conn.close()
    return render_template('finanzas/gastos.html', gastos=gastos)

@app.route('/api/gastos', methods=['POST'])
def agregar_gasto():
    """Agregar nuevo gasto"""
    data = request.json
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO gastos (fecha, descripcion, monto, categoria, notas)
        VALUES (?, ?, ?, ?, ?)
    ''', (data['fecha'], data['descripcion'], data['monto'], 
          data.get('categoria', ''), data.get('notas', '')))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Gasto registrado correctamente'})

@app.route('/api/gastos/<int:id>', methods=['DELETE'])
def eliminar_gasto(id):
    """Eliminar gasto"""
    conn = get_db_connection()
    conn.execute('DELETE FROM gastos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Gasto eliminado'})

# DEUDAS
@app.route('/deudas')
def deudas():
    """Página de gestión de deudas"""
    conn = get_db_connection()
    deudas = conn.execute('SELECT * FROM deudas ORDER BY fecha_inicio DESC').fetchall()
    conn.close()
    return render_template('finanzas/deudas.html', deudas=deudas)

@app.route('/api/deudas', methods=['POST'])
def agregar_deuda():
    """Agregar nueva deuda"""
    data = request.json
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO deudas (acreedor, monto_total, fecha_inicio, fecha_limite, interes, notas)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (data['acreedor'], data['monto_total'], data['fecha_inicio'], 
          data.get('fecha_limite'), data.get('interes', 0), data.get('notas', '')))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Deuda registrada correctamente'})

@app.route('/api/deudas/<int:id>/pagar', methods=['POST'])
def pagar_deuda(id):
    """Registrar pago de deuda"""
    data = request.json
    conn = get_db_connection()
    
    # Registrar el pago
    conn.execute('''
        INSERT INTO pagos_deuda (deuda_id, fecha, monto, notas)
        VALUES (?, ?, ?, ?)
    ''', (id, data['fecha'], data['monto'], data.get('notas', '')))
    
    # Actualizar monto pagado de la deuda
    conn.execute('''
        UPDATE deudas 
        SET monto_pagado = monto_pagado + ?
        WHERE id = ?
    ''', (data['monto'], id))
    
    # Verificar si la deuda está completamente pagada
    deuda = conn.execute('SELECT monto_total, monto_pagado FROM deudas WHERE id = ?', (id,)).fetchone()
    if deuda['monto_pagado'] >= deuda['monto_total']:
        conn.execute('UPDATE deudas SET estado = "pagada" WHERE id = ?', (id,))
    
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Pago registrado correctamente'})

@app.route('/api/deudas/<int:id>', methods=['DELETE'])
def eliminar_deuda(id):
    """Eliminar deuda"""
    conn = get_db_connection()
    conn.execute('DELETE FROM pagos_deuda WHERE deuda_id = ?', (id,))
    conn.execute('DELETE FROM deudas WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Deuda eliminada'})

# PAGOS MENSUALES
@app.route('/pagos-mensuales')
def pagos_mensuales():
    """Página de gestión de pagos mensuales"""
    conn = get_db_connection()
    pagos = conn.execute('SELECT * FROM pagos_mensuales WHERE activo = 1 ORDER BY dia_pago').fetchall()
    conn.close()
    return render_template('finanzas/pagos_mensuales.html', pagos=pagos)

@app.route('/api/pagos-mensuales', methods=['POST'])
def agregar_pago_mensual():
    """Agregar nuevo pago mensual"""
    data = request.json
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO pagos_mensuales (nombre, monto, dia_pago, categoria, notas)
        VALUES (?, ?, ?, ?, ?)
    ''', (data['nombre'], data['monto'], data['dia_pago'], 
          data.get('categoria', ''), data.get('notas', '')))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Pago mensual registrado correctamente'})

@app.route('/api/pagos-mensuales/<int:id>', methods=['DELETE'])
def eliminar_pago_mensual(id):
    """Eliminar pago mensual"""
    conn = get_db_connection()
    conn.execute('UPDATE pagos_mensuales SET activo = 0 WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'message': 'Pago mensual desactivado'})

# REPORTES
@app.route('/reportes')
def reportes():
    """Página de reportes y estadísticas"""
    conn = get_db_connection()
    
    # Estadísticas por categoría
    ingresos_categoria = conn.execute('''
        SELECT categoria, SUM(monto) as total 
        FROM ingresos 
        GROUP BY categoria
    ''').fetchall()
    
    gastos_categoria = conn.execute('''
        SELECT categoria, SUM(monto) as total 
        FROM gastos 
        GROUP BY categoria
    ''').fetchall()
    
    # Tendencia mensual (últimos 6 meses)
    tendencia = conn.execute('''
        SELECT 
            strftime('%Y-%m', fecha) as mes,
            SUM(CASE WHEN tipo = 'ingreso' THEN monto ELSE 0 END) as ingresos,
            SUM(CASE WHEN tipo = 'gasto' THEN monto ELSE 0 END) as gastos
        FROM (
            SELECT fecha, monto, 'ingreso' as tipo FROM ingresos
            UNION ALL
            SELECT fecha, monto, 'gasto' as tipo FROM gastos
        )
        WHERE fecha >= date('now', '-6 months')
        GROUP BY mes
        ORDER BY mes
    ''').fetchall()
    
    conn.close()
    
    return render_template('finanzas/reportes.html',
                         ingresos_categoria=ingresos_categoria,
                         gastos_categoria=gastos_categoria,
                         tendencia=tendencia)

if __name__ == '__main__':
    # Inicializar base de datos
    if not os.path.exists(DATABASE):
        print("🔧 Creando base de datos...")
        init_db()
    
    print("=" * 50)
    print("💰 Sistema de Gestión Financiera Personal")
    print("=" * 50)
    print("\n✨ Funcionalidades:")
    print("  • Registrar ingresos y gastos")
    print("  • Gestionar deudas y pagos")
    print("  • Control de pagos mensuales recurrentes")
    print("  • Reportes y estadísticas")
    print("\n🌐 Abriendo aplicación en http://localhost:5001")
    print("💡 Presiona Ctrl+C para detener el servidor\n")
    
    app.run(debug=True, port=5001, host='0.0.0.0')

