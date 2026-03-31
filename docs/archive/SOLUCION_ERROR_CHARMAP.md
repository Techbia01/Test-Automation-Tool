# 🔧 Solución: Error 'charmap' codec en Windows

## 🚨 **Problema**

Al intentar generar casos de prueba en Windows, se producía el siguiente error:

```
Error: 'charmap' codec can't encode characters in position 5-6: character maps to
```

Este error ocurre cuando Python intenta escribir caracteres especiales (acentos, eñes, etc.) a la consola usando la codificación por defecto de Windows (`charmap`), que no soporta todos los caracteres UTF-8.

## ✅ **Solución Implementada**

Se ha agregado configuración de encoding UTF-8 al inicio de los archivos principales:

### **Archivos Modificados:**

1. **`main.py`** - Punto de entrada principal
2. **`app.py`** - Aplicación Flask principal (raíz)
3. **`src/app.py`** - Aplicación Flask alternativa
4. **`src/professional_qa_generator.py`** - Generador de casos de prueba

### **Código Agregado:**

```python
import sys
import os
import io

# Configurar encoding UTF-8 para Windows (soluciona error 'charmap' codec)
if sys.platform == 'win32':
    # Reconfigurar stdout y stderr para usar UTF-8
    try:
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8')
            sys.stderr.reconfigure(encoding='utf-8')
        else:
            raise AttributeError("reconfigure not available")
    except (AttributeError, ValueError):
        # Para versiones anteriores de Python o si falla reconfigure
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
```

## 🎯 **Cómo Funciona**

1. **Detección de Windows:** Verifica si el sistema operativo es Windows (`sys.platform == 'win32'`)

2. **Método 1 (Python 3.7+):** Usa `reconfigure()` para cambiar el encoding de stdout/stderr a UTF-8

3. **Método 2 (Fallback):** Si `reconfigure()` no está disponible, envuelve stdout/stderr con `TextIOWrapper` configurado para UTF-8

4. **Manejo de Errores:** Usa `errors='replace'` para reemplazar caracteres problemáticos en lugar de fallar

## 📋 **Verificación**

Para verificar que la solución funciona:

1. **Reinicia el servidor:**
   ```bash
   python main.py
   ```

2. **Genera casos de prueba** con caracteres especiales (acentos, eñes, etc.)

3. **Verifica en la consola** que los mensajes se muestren correctamente:
   - ✅ Debe mostrar: "Validar que el sistema guarda correctamente..."
   - ❌ NO debe mostrar: "Error: 'charmap' codec can't encode..."

## 🔍 **Archivos Afectados**

- ✅ `main.py` - Configuración aplicada
- ✅ `app.py` - Configuración aplicada  
- ✅ `src/app.py` - Configuración aplicada
- ✅ `src/professional_qa_generator.py` - Configuración aplicada

## 📝 **Notas Adicionales**

- La solución es **compatible con Python 3.6+**
- Funciona tanto en **PowerShell** como en **CMD**
- No afecta el funcionamiento en **Linux/Mac**
- Los archivos JSON ya estaban configurados con `encoding='utf-8'` ✅

## 🚀 **Próximos Pasos**

Si el error persiste después de reiniciar el servidor:

1. Verifica que estás usando Python 3.6 o superior
2. Asegúrate de que el servidor se reinició completamente
3. Si el problema continúa, verifica la configuración regional de Windows

---

**Fecha de implementación:** 2024
**Versión:** 1.0

