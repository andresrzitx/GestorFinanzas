# 🧪 Tests Unitarios - FinanzApp

## 📋 Descripción

Suite completa de tests unitarios utilizando el framework `unittest` de Python para verificar la funcionalidad de FinanzApp.

## ✅ Estado Actual

**48 tests pasando exitosamente** ✨

## 🗂️ Estructura de Tests

```
tests/
├── __init__.py                    # Inicialización del paquete
├── test_models.py                 # Tests de modelos POO (28 tests)
├── test_login.py                  # Tests de autenticación (6 tests)
├── test_ingresos.py               # Tests de ingresos (7 tests)
├── test_gestion_categorias.py     # Tests de categorías (7 tests)
├── test_comparacion_anual.py      # Test funcional de comparación anual
└── run_all_tests.py               # ⭐ Ejecutor principal de todos los tests
```

## 🚀 Cómo Ejecutar los Tests

### Ejecutar TODOS los tests

```bash
python tests/run_all_tests.py
```

### Ejecutar tests individuales

```bash
# Tests de modelos POO
python tests/test_models.py

# Tests de login
python tests/test_login.py

# Tests de ingresos
python tests/test_ingresos.py

# Tests de gestión de categorías
python tests/test_gestion_categorias.py
```

### Ejecutar con pytest (opcional)

```bash
pytest tests/ -v
```

## 📊 Cobertura de Tests

### test_models.py (28 tests)
- ✅ **Usuario**: Creación, roles, activación, autenticación
- ✅ **Categoría**: CRUD completo
- ✅ **Gasto**: Creación, validación, métodos de pago
- ✅ **Ingreso**: Creación, validación, conversiones
- ✅ **GrupoGasto**: Gestión de miembros

### test_login.py (6 tests)
- ✅ Autenticación con credenciales válidas/inválidas
- ✅ Registro de nuevos usuarios
- ✅ Validación de duplicados
- ✅ Cambio de roles
- ✅ Verificación de usuario admin

### test_ingresos.py (7 tests)
- ✅ Obtención de ingresos por mes
- ✅ Cálculo de totales
- ✅ Balance mensual y anual
- ✅ Agrupación por fuente
- ✅ Agregar nuevos ingresos
- ✅ Comparación ingresos vs gastos

### test_gestion_categorias.py (7 tests)
- ✅ Listar categorías
- ✅ Agregar nueva categoría
- ✅ Validación de duplicados
- ✅ Editar categoría
- ✅ Eliminar categoría (con validaciones)
- ✅ Obtener por ID

## 📈 Ejemplo de Salida

```
================================================================================
 🧪 EJECUTANDO SUITE COMPLETA DE TESTS - FinanzApp
================================================================================

test_crear_usuario_basico ... ok
test_usuario_es_admin ... ok
...

----------------------------------------------------------------------
Ran 58 tests in 0.068s

OK

================================================================================
 📊 RESUMEN DE TESTS
================================================================================
 Tests ejecutados: 58
 ✅ Exitosos: 58
 ❌ Fallos: 0
 💥 Errores: 0
================================================================================
```

## 🔧 Requisitos

- Python 3.8+
- Módulos del proyecto (`src/`)
- Base de datos SQLite (se crea automáticamente)

## 💡 Buenas Prácticas Implementadas

1. **✅ Uso de `unittest`**: Framework estándar de Python
2. **✅ Nomenclatura clara**: `test_<funcionalidad>`
3. **✅ Docstrings**: Cada test está documentado
4. **✅ setUp/tearDown**: Preparación y limpieza automática
5. **✅ Assertions específicos**: Mensajes claros de error
6. **✅ Tests aislados**: Cada test es independiente
7. **✅ Suite runner**: Ejecutor centralizado

## 🎯 Próximos Pasos

- [ ] Agregar tests de integración
- [ ] Implementar coverage report
- [ ] Tests de interfaz gráfica (Tkinter)
- [ ] Tests de rendimiento
- [ ] CI/CD con GitHub Actions

## 📝 Notas

- Los tests usan `usuario_id=999` para pruebas (se limpia automáticamente)
- Las bases de datos de test se crean y eliminan automáticamente
- Todos los tests son independientes y pueden ejecutarse en cualquier orden

## 🆘 Solución de Problemas

### Error: "No module named 'src'"
```bash
# Ejecutar desde el directorio raíz del proyecto
cd /ruta/al/proyecto
python tests/run_all_tests.py
```

### Error: "Database locked"
```bash
# Eliminar bases de datos temporales
rm data/usuarios/usuario_999_finanzas.db
```

---

**Mantén los tests actualizados** 🚀 - Cada nueva funcionalidad debe tener su test correspondiente.
