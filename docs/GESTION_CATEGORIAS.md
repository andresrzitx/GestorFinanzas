# 🏷️ Gestión de Categorías

## Descripción

Se ha implementado un sistema completo de gestión de categorías que permite a los usuarios personalizar y organizar mejor sus gastos.

## Funcionalidades Implementadas

### 1. ➕ Agregar Categoría

Permite crear nuevas categorías personalizadas para clasificar los gastos.

**Características**:
- Campo de nombre (obligatorio)
- Campo de descripción (opcional)
- Validación de nombres únicos
- Interfaz moderna con diseño consistente

**Uso**:
1. Ir a la pestaña "Categorías"
2. Hacer clic en el botón "➕ Nueva Categoría"
3. Ingresar el nombre y descripción
4. Hacer clic en "💾 Guardar"

### 2. ✏️ Editar Categoría

Permite modificar las categorías existentes.

**Características**:
- Edición de nombre y descripción
- Validación de nombres únicos
- Preserva los gastos asociados

**Uso**:
1. Ir a la pestaña "Categorías"
2. Seleccionar una categoría de la lista
3. Hacer clic en el botón "✏️ Editar"
4. Modificar los campos deseados
5. Hacer clic en "💾 Guardar"

### 3. 🗑️ Eliminar Categoría

Permite eliminar categorías que ya no se utilizan.

**Características**:
- Solo se pueden eliminar categorías sin gastos asociados
- Confirmación antes de eliminar
- Mensaje informativo si hay gastos asociados

**Uso**:
1. Ir a la pestaña "Categorías"
2. Seleccionar una categoría sin gastos asociados
3. Hacer clic en el botón "🗑️ Eliminar"
4. Confirmar la eliminación

### 4. 📊 Visualización de Categorías

Muestra todas las categorías en una tabla con información detallada.

**Columnas**:
- **ID**: Identificador único de la categoría
- **Nombre**: Nombre de la categoría
- **Descripción**: Descripción de la categoría
- **Gastos Asociados**: Cantidad de gastos vinculados

## Categorías por Defecto

El sistema incluye las siguientes categorías predeterminadas:

1. **Alimentación**: Gastos en comida y bebidas
2. **Transporte**: Gastos de transporte y combustible
3. **Servicios**: Facturas de luz, agua, internet, etc.
4. **Entretenimiento**: Ocio, salidas, hobbies
5. **Salud**: Médicos, medicamentos, seguros
6. **Educación**: Cursos, libros, materiales
7. **Hogar**: Alquiler, mantenimiento, muebles
8. **Otros**: Gastos varios

## Métodos de Base de Datos

### `agregar_categoria(nombre: str, descripcion: str = "") -> bool`

Agrega una nueva categoría a la base de datos.

**Parámetros**:
- `nombre`: Nombre de la categoría (obligatorio, único)
- `descripcion`: Descripción de la categoría (opcional)

**Retorna**: `True` si se agregó correctamente, `False` si ya existe

### `editar_categoria(categoria_id: int, nombre: str, descripcion: str = "") -> bool`

Edita una categoría existente.

**Parámetros**:
- `categoria_id`: ID de la categoría a editar
- `nombre`: Nuevo nombre de la categoría
- `descripcion`: Nueva descripción de la categoría

**Retorna**: `True` si se editó correctamente, `False` en caso de error

### `eliminar_categoria(categoria_id: int) -> bool`

Elimina una categoría de la base de datos.

**Parámetros**:
- `categoria_id`: ID de la categoría a eliminar

**Retorna**: `True` si se eliminó correctamente, `False` si tiene gastos asociados

**Restricciones**: Solo se puede eliminar si no hay gastos asociados

### `obtener_categorias() -> List[Tuple]`

Obtiene todas las categorías disponibles.

**Retorna**: Lista de tuplas `(id, nombre, descripcion)`

## Interfaz de Usuario

### Diseño

La pestaña "Categorías" incluye:

- **Título**: "🏷️ Gestión de Categorías" con estilo moderno
- **Botón Nueva Categoría**: En la esquina superior derecha
- **Tabla de Categorías**: Muestra todas las categorías con scrollbar
- **Botones de Acción**: Editar y Eliminar en la parte inferior
- **Nota Informativa**: Sobre las restricciones de eliminación

### Estilos

- Usa la paleta de colores del sistema (COLORES)
- Botones con estilo moderno usando `crear_boton_moderno()`
- Campos de entrada con estilo flat y destacado al enfocar
- Ventanas emergentes modales y centradas

## Validaciones

1. **Nombre Único**: No se permiten categorías con el mismo nombre
2. **Nombre Obligatorio**: El campo de nombre no puede estar vacío
3. **Eliminación Segura**: Solo se eliminan categorías sin gastos asociados
4. **Confirmación**: Se solicita confirmación antes de eliminar

## Mensajes de Usuario

- **Éxito al agregar**: "Categoría agregada correctamente"
- **Error al agregar**: "No se pudo agregar la categoría. Es posible que ya exista."
- **Éxito al editar**: "Categoría editada correctamente"
- **Error al editar**: "No se pudo editar la categoría. Es posible que el nombre ya exista."
- **Éxito al eliminar**: "Categoría eliminada correctamente"
- **Error al eliminar**: "No se puede eliminar la categoría '{nombre}' porque tiene {n} gasto(s) asociado(s)."

## Integración con Otras Vistas

La vista de categorías está integrada con:

1. **Vistas Mensuales**: Los gastos se vinculan a categorías
2. **Vista de Estadísticas**: Muestra gastos agrupados por categoría
3. **Botón Actualizar**: Refresca la vista de categorías junto con las demás

## Archivos Modificados

### `src/database.py`

- ✅ Agregado método `editar_categoria()`
- ✅ Agregado método `eliminar_categoria()`
- ✅ Método `agregar_categoria()` ya existía

### `src/vistas.py`

- ✅ Agregada clase `VistaGestionCategorias`
- ✅ Implementados métodos de interfaz
- ✅ Ventanas modales para agregar/editar

### `src/app.py`

- ✅ Agregada importación de `VistaGestionCategorias`
- ✅ Agregada pestaña "Categorías" al notebook
- ✅ Actualizado método `refrescar_vistas()`

## Próximas Mejoras (Opcional)

- [ ] Iconos personalizados para cada categoría
- [ ] Colores personalizados por categoría
- [ ] Reasignación masiva de gastos al eliminar categoría
- [ ] Importar/Exportar categorías
- [ ] Categorías favoritas o más usadas
- [ ] Subcategorías o jerarquías

## Estado

**Fecha**: 15 de Enero de 2026
**Estado**: ✅ Implementado y funcionando
**Versión**: 3.1

La funcionalidad de gestión de categorías está completamente implementada y lista para usar. Los usuarios ahora pueden personalizar completamente sus categorías de gastos según sus necesidades.

