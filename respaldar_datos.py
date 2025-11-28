#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para respaldar los datos del sistema QA
Crea una copia de seguridad de qa_projects.json
"""

import os
import shutil
from datetime import datetime

def crear_respaldo():
    """Crea un respaldo del archivo de proyectos"""
    
    archivo_datos = 'qa_projects.json'
    
    if not os.path.exists(archivo_datos):
        print("[INFO] No hay datos para respaldar (qa_projects.json no existe)")
        return False
    
    # Crear carpeta de respaldos si no existe
    carpeta_respaldos = 'respaldos'
    os.makedirs(carpeta_respaldos, exist_ok=True)
    
    # Nombre del respaldo con fecha y hora
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    nombre_respaldo = f'qa_projects_backup_{timestamp}.json'
    ruta_respaldo = os.path.join(carpeta_respaldos, nombre_respaldo)
    
    try:
        # Copiar archivo
        shutil.copy2(archivo_datos, ruta_respaldo)
        
        # Obtener tamaño del archivo
        tamano = os.path.getsize(ruta_respaldo)
        tamano_kb = tamano / 1024
        
        print("=" * 60)
        print("[OK] RESPALDO CREADO EXITOSAMENTE")
        print("=" * 60)
        print(f"\nArchivo: {ruta_respaldo}")
        print(f"Tamaño: {tamano_kb:.2f} KB")
        print(f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        
        # Listar respaldos existentes
        respaldos = sorted([f for f in os.listdir(carpeta_respaldos) if f.endswith('.json')])
        
        if len(respaldos) > 1:
            print(f"\nRespaldos totales: {len(respaldos)}")
            print("\nÚltimos 5 respaldos:")
            for respaldo in respaldos[-5:]:
                print(f"  - {respaldo}")
        
        print("\n[INFO] Para restaurar un respaldo:")
        print(f"       copy {ruta_respaldo} qa_projects.json")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] No se pudo crear el respaldo: {e}")
        return False

if __name__ == '__main__':
    import sys
    sys.exit(0 if crear_respaldo() else 1)

