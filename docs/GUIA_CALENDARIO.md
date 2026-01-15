# 📅 Calendario Integrado - Guía de Uso

## 🌟 Nueva Funcionalidad: Selector de Fechas

Se ha integrado un componente de calendario visual que facilita la selección de fechas tanto para gastos como ingresos.

## 🔧 Características del Calendario

### ✨ Funcionalidades Principales:
- **Calendario visual**: Interfaz gráfica intuitiva para seleccionar fechas
- **Navegación por meses**: Botones para navegar hacia adelante y atrás
- **Botón "Hoy"**: Selección rápida de la fecha actual
- **Día actual resaltado**: Se muestra en color azul
- **Día seleccionado resaltado**: Se muestra en color verde
- **Validación automática**: Solo permite fechas válidas

### 🎯 Ubicación en la Aplicación:
1. **Formulario de Gastos**: Campo "Fecha" con botón de calendario 📅
2. **Formulario de Ingresos**: Campo "Fecha" con botón de calendario 📅
3. **Ventanas de Edición**: Tanto para gastos como ingresos

## 📖 Cómo Usar el Calendario

### 1. Selección Básica:
- Los campos de fecha ahora muestran: `[DD] / [MM] / [YYYY] [📅]`
- Puedes escribir directamente en los campos o hacer clic en 📅

### 2. Uso del Calendario Visual:
1. **Abrir calendario**: Clic en el botón 📅
2. **Navegar por meses**: Usa los botones ◀ y ▶
3. **Seleccionar día**: Clic en el día deseado
4. **Selección rápida**: Botón "📅 Hoy" para fecha actual
5. **Cancelar**: Botón "❌ Cancelar" para cerrar sin seleccionar

### 3. Indicadores Visuales:
- **Día actual** = Fondo azul con texto blanco
- **Día seleccionado** = Fondo verde con texto blanco
- **Días normales** = Fondo gris claro

## 🔄 Integración Completa

### ✅ Formularios Actualizados:
- **Agregar Gasto**: Nuevo selector de fecha
- **Agregar Ingreso**: Nuevo selector de fecha
- **Editar Gasto**: Calendario en ventana modal
- **Editar Ingreso**: Calendario en ventana modal

### 🎨 Compatibilidad Visual:
- Se integra perfectamente con el tema visual existente
- Usa los colores definidos en `estilos.py`
- Respeta la tipografía SF Pro Display

## 🛠️ Detalles Técnicos

### Archivos Modificados:
1. **`src/calendario.py`** (NUEVO)
   - `CalendarioWidget`: Ventana modal del calendario
   - `BotonCalendario`: Componente integrable

2. **`src/vistas.py`** (ACTUALIZADO)
   - Reemplazado campos manuales con `BotonCalendario`
   - Actualizado métodos `agregar_gasto()` y `agregar_ingreso()`
   - Actualizado ventanas de edición
   - Corregido método `cambiar_anio()`

3. **`main.py`** (CORREGIDO)
   - Solucionado error de argumentos en `iniciar_aplicacion()`

### Componentes del Calendario:

#### `CalendarioWidget`:
- Ventana modal independiente
- Navegación intuitiva por meses
- Validación de fechas
- Callbacks para confirmación

#### `BotonCalendario`:
- Widget compuesto (Frame con entries + botón)
- Métodos `obtener_fecha()` y `establecer_fecha()`
- Integración seamless con formularios existentes

## 🚀 Beneficios

### Para el Usuario:
- **Más rápido**: No necesitas escribir fechas manualmente
- **Menos errores**: Validación automática de fechas
- **Más intuitivo**: Interfaz visual familiar
- **Flexible**: Aún puedes escribir fechas directamente

### Para el Código:
- **Reutilizable**: Un componente para toda la app
- **Mantenible**: Código centralizado en un archivo
- **Extensible**: Fácil agregar nuevas características
- **Compatible**: No rompe funcionalidad existente

## 🔧 Resolución de Problemas

### Si el calendario no aparece:
1. Verifica que `src/calendario.py` esté presente
2. Reinicia la aplicación
3. Revisa la consola por errores de importación

### Si hay errores de fecha:
1. El formato interno sigue siendo YYYY-MM-DD
2. La validación es automática
3. Fechas inválidas (ej: 31 Feb) se rechazan automáticamente

## 🎯 Próximas Mejoras Posibles

- **Temas visuales**: Modo oscuro/claro para el calendario
- **Rangos de fechas**: Selección de períodos
- **Fechas recurrentes**: Plantillas para gastos regulares
- **Atajos de teclado**: Navegación rápida
- **Calendario lunar**: Para diferentes culturas
- **Recordatorios**: Notificaciones de fechas importantes

---

**¡Disfruta de la nueva funcionalidad de calendario! 📅✨**
