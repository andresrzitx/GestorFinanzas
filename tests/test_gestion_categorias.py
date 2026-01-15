"""
Test de funcionalidad de gestión de categorías
"""
import sys
import os

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from database import Database

def test_gestion_categorias():
    """Prueba las operaciones CRUD de categorías."""
    print("\n" + "="*80)
    print("  TEST: GESTIÓN DE CATEGORÍAS")
    print("="*80 + "\n")

    # Crear una base de datos temporal para pruebas
    db = Database(usuario_id=999)  # Usuario de prueba

    print("✅ Base de datos de prueba creada\n")

    # 1. LISTAR CATEGORÍAS INICIALES
    print("1️⃣  LISTANDO CATEGORÍAS POR DEFECTO:")
    print("-" * 80)
    categorias = db.obtener_categorias()
    for cat_id, nombre, descripcion in categorias:
        print(f"   ID: {cat_id:2d} | {nombre:20s} | {descripcion}")
    print(f"\n   Total: {len(categorias)} categorías\n")

    # 2. AGREGAR NUEVA CATEGORÍA
    print("2️⃣  AGREGANDO NUEVA CATEGORÍA:")
    print("-" * 80)
    if db.agregar_categoria("Mascotas", "Gastos relacionados con mascotas"):
        print("   ✅ Categoría 'Mascotas' agregada correctamente")
    else:
        print("   ❌ Error al agregar categoría")

    # Intentar agregar duplicada
    if not db.agregar_categoria("Mascotas", "Descripción diferente"):
        print("   ✅ Validación correcta: no permite duplicados")
    else:
        print("   ❌ Error: permitió duplicado")
    print()

    # 3. EDITAR CATEGORÍA
    print("3️⃣  EDITANDO CATEGORÍA:")
    print("-" * 80)
    categorias = db.obtener_categorias()
    mascotas_id = None
    for cat_id, nombre, _ in categorias:
        if nombre == "Mascotas":
            mascotas_id = cat_id
            break

    if mascotas_id:
        if db.editar_categoria(mascotas_id, "Mascotas y Veterinaria", "Gastos de mascotas y veterinario"):
            print("   ✅ Categoría editada correctamente")
            # Verificar cambio
            categorias = db.obtener_categorias()
            for cat_id, nombre, desc in categorias:
                if cat_id == mascotas_id:
                    print(f"   📝 Nueva info: {nombre} - {desc}")
        else:
            print("   ❌ Error al editar categoría")
    print()

    # 4. INTENTAR ELIMINAR CATEGORÍA CON GASTOS
    print("4️⃣  INTENTANDO ELIMINAR CATEGORÍA CON GASTOS:")
    print("-" * 80)
    # Primero agregar un gasto a la categoría "Alimentación" (ID 1)
    db.agregar_gasto("Gasto de prueba", 10.0, 1, "2025-01-15")
    if not db.eliminar_categoria(1):
        print("   ✅ Validación correcta: no permite eliminar categoría con gastos")
    else:
        print("   ❌ Error: permitió eliminar categoría con gastos")
    print()

    # 5. ELIMINAR CATEGORÍA SIN GASTOS
    print("5️⃣  ELIMINANDO CATEGORÍA SIN GASTOS:")
    print("-" * 80)
    if mascotas_id and db.eliminar_categoria(mascotas_id):
        print("   ✅ Categoría eliminada correctamente")
    else:
        print("   ❌ Error al eliminar categoría")
    print()

    # 6. LISTAR CATEGORÍAS FINALES
    print("6️⃣  LISTANDO CATEGORÍAS FINALES:")
    print("-" * 80)
    categorias = db.obtener_categorias()
    for cat_id, nombre, descripcion in categorias:
        print(f"   ID: {cat_id:2d} | {nombre:20s} | {descripcion}")
    print(f"\n   Total: {len(categorias)} categorías\n")

    print("="*80)
    print("  ✅ TODOS LOS TESTS COMPLETADOS")
    print("="*80 + "\n")

    # Limpiar: eliminar la base de datos de prueba
    try:
        db_path = f"data/usuarios/usuario_999_finanzas.db"
        if os.path.exists(db_path):
            os.remove(db_path)
            print("🧹 Base de datos de prueba eliminada\n")
    except Exception as e:
        print(f"⚠️  No se pudo eliminar DB de prueba: {e}\n")

if __name__ == "__main__":
    test_gestion_categorias()

