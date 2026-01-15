# 📊 Actualización: Gestión de Ingresos y Balance

## ✅ Cambios Implementados

Se ha actualizado la aplicación de **Gestor de Gastos Mensuales** para incluir la gestión completa de **INGRESOS** además de gastos, permitiendo hacer comparativas ingreso/gasto y ver el balance mensual.

---

## 🆕 Nuevas Funcionalidades

### 1. **Gestión de Ingresos**
- ✅ Registro de ingresos con descripción, cantidad, fuente y fecha
- ✅ Fuentes de ingreso predefinidas: Salario, Freelance, Inversiones, Venta, Regalo, Otros
- ✅ Listado de ingresos por mes
- ✅ Eliminación de ingresos
- ✅ Totales de ingresos por mes y año

### 2. **Balance Mensual**
- ✅ Visualización del balance (Ingresos - Gastos) en cada mes
- ✅ Indicador visual con colores:
  - 🟢 **Verde**: Balance positivo (ahorros)
  - 🔴 **Rojo**: Balance negativo (déficit)
- ✅ Resumen visible en la parte superior de cada pestaña mensual:
  - Total de Ingresos del mes
  - Total de Gastos del mes
  - Balance del mes

### 3. **Interfaz Mejorada**
- ✅ Cada mes tiene dos pestañas internas:
  - 💸 **Gastos**: Para gestionar gastos
  - 💰 **Ingresos**: Para gestionar ingresos
- ✅ Panel de balance en la parte superior mostrando:
  - Ingresos totales (en verde)
  - Gastos totales (en rojo)
  - Balance neto (en verde/rojo según sea positivo/negativo)

---

## 🗄️ Cambios en la Base de Datos

### Nueva Tabla: `ingresos`
```sql
CREATE TABLE ingresos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    descripcion TEXT NOT NULL,
    cantidad REAL NOT NULL,
    fuente TEXT NOT NULL,
    fecha DATE NOT NULL,
    mes INTEGER NOT NULL,
    anio INTEGER NOT NULL
)
```

### Nuevos Métodos en `database.py`:
- `agregar_ingreso()` - Agrega un nuevo ingreso
- `obtener_ingresos_mes()` - Obtiene ingresos de un mes específico
- `obtener_total_ingresos_mes()` - Calcula total de ingresos del mes
- `obtener_total_ingresos_anual()` - Calcula total de ingresos del año
- `obtener_ingresos_por_fuente_mes()` - Agrupa ingresos por fuente
- `obtener_comparacion_ingresos_anual()` - Compara ingresos por mes
- `eliminar_ingreso()` - Elimina un ingreso
- `obtener_balance_mes()` - **Calcula balance mensual (Ingresos - Gastos)**
- `obtener_balance_anual()` - **Calcula balance anual (Ingresos - Gastos)**

---

## 📁 Archivos Modificados

### 1. **database.py**
- ✅ Agregada tabla `ingresos`
- ✅ Agregados 9 métodos nuevos para gestión de ingresos y balance
- ✅ Métodos de balance para obtener comparativas ingreso/gasto

### 2. **vistas.py**
- ✅ Vista mensual reorganizada con pestañas para Gastos e Ingresos
- ✅ Panel de balance en la parte superior
- ✅ Formularios separados para agregar gastos e ingresos
- ✅ Métodos `agregar_ingreso()`, `cargar_ingresos()`, `eliminar_ingreso()`
- ✅ Método `actualizar_balance()` para mostrar el balance en tiempo real

### 3. **agregar_datos_ejemplo.py**
- ✅ Agregados 17 ingresos de ejemplo para los meses Enero-Junio 2026
- ✅ Resumen mejorado que muestra:
  - Balance por mes
  - Total ingresos y gastos
  - Balance anual
  - Promedios mensuales

---

## 📊 Datos de Ejemplo

El script de datos de ejemplo ahora incluye:

### Ingresos (Enero - Junio 2026):
- **17 ingresos** totalizando €18,475.00
- Fuentes: Salario, Freelance, Inversiones, Ventas, Regalos
- Promedio mensual: €3,079.17

### Gastos (Enero - Junio 2026):
- **51 gastos** totalizando €3,099.32
- 8 categorías diferentes
- Promedio mensual: €516.55

### Balance Total:
- **Balance Acumulado (Ene-Jun)**: +€15,375.68 ✅
- Todos los meses con balance positivo

---

## 🚀 Cómo Usar

### Iniciar la aplicación:
```bash
python3 app.py
```

### Agregar datos de ejemplo (opcional):
```bash
# Eliminar base de datos actual y crear nueva con datos de ejemplo
rm -f gastos_mensuales.db
python3 agregar_datos_ejemplo.py
```

### Navegar por la aplicación:
1. **Seleccionar un mes** de las pestañas principales
2. En cada mes verás:
   - **Balance resumen** en la parte superior
   - **Pestaña Gastos**: Agregar, ver y eliminar gastos
   - **Pestaña Ingresos**: Agregar, ver y eliminar ingresos
3. **Comparación Anual**: Pestaña para ver totales anuales
4. **Estadísticas**: Gráficos y análisis de gastos

---

## 💡 Funcionalidades Destacadas

### Balance en Tiempo Real
Cada vez que agregas o eliminas un ingreso o gasto, el balance se actualiza automáticamente mostrando:
- Total de ingresos del mes (verde)
- Total de gastos del mes (rojo)
- Balance neto (verde si es positivo, rojo si es negativo)

### Análisis Completo
Ahora puedes:
- ✅ Comparar cuánto ganas vs cuánto gastas cada mes
- ✅ Ver tu capacidad de ahorro mensual
- ✅ Identificar meses con déficit
- ✅ Analizar tendencias de ingresos y gastos
- ✅ Planificar mejor tus finanzas personales

---

## 🎯 Ejemplo de Uso

### Agregar un Ingreso:
1. Ir a la pestaña del mes deseado
2. Seleccionar la sub-pestaña "💰 Ingresos"
3. Llenar el formulario:
   - **Descripción**: "Salario mensual"
   - **Cantidad**: 2500
   - **Fuente**: Salario
   - **Fecha**: 01/01/2026
4. Clic en "➕ Agregar Ingreso"
5. El balance se actualiza automáticamente

### Ver el Balance:
- En la parte superior de cada mes verás algo como:
  ```
  Ingresos: €3030.00 | Gastos: €446.00 | Balance: €2584.00
  ```
  - Si el balance es positivo (verde) = ¡Estás ahorrando! 💰
  - Si el balance es negativo (rojo) = Gastas más de lo que ingresas ⚠️

---

## 📈 Ventajas de la Nueva Versión

1. **Visión Completa de Finanzas**: No solo gastos, también ingresos
2. **Control de Balance**: Saber si ahorras o gastas de más
3. **Mejor Planificación**: Ver patrones de ingresos y gastos
4. **Interfaz Intuitiva**: Pestañas organizadas para fácil acceso
5. **Datos Realistas**: Ejemplos con salarios, freelance, gastos reales

---

## 🔄 Migración de Datos

Si ya tenías datos previos, la aplicación automáticamente:
- ✅ Crea la nueva tabla de ingresos
- ✅ Mantiene todos los gastos existentes
- ✅ No se pierde ningún dato

---

## 📝 Notas Técnicas

### Compatibilidad
- Python 3.x
- Tkinter (incluido con Python)
- SQLite3 (incluido con Python)
- No requiere instalaciones adicionales

### Estructura de Archivos
```
ProyectoFinal/
├── app.py                      # Aplicación principal
├── database.py                 # Gestión de base de datos (con ingresos)
├── vistas.py                   # Interfaces gráficas (con balance)
├── agregar_datos_ejemplo.py    # Script de datos de ejemplo
├── migrar_db.py               # Script de migración
├── gastos_mensuales.db        # Base de datos SQLite
└── ACTUALIZACION_INGRESOS.md  # Este documento
```

---

## ✨ Resumen

Tu aplicación ahora es un **gestor completo de finanzas personales** que te permite:

✅ Registrar **ingresos** y **gastos**  
✅ Ver el **balance mensual** (cuánto ahorras o pierdes)  
✅ Comparar **ingresos vs gastos** por mes y año  
✅ Tomar mejores **decisiones financieras**  
✅ Visualizar datos de forma clara y organizada  

**¡Tu aplicación está lista para ayudarte a gestionar tus finanzas personales! 🎉**

