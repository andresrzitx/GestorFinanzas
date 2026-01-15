"""
Script de migración para cambiar la columna 'monto' por 'cantidad' en la base de datos.
"""

import sqlite3
import os
from datetime import datetime

def migrar_base_datos():
    """Migra la base de datos cambiando 'monto' por 'cantidad'."""

    db_path = "gastos_mensuales.db"
    backup_path = f"gastos_mensuales_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"

    if not os.path.exists(db_path):
        print("⚠️  No se encontró la base de datos. Se creará una nueva con el esquema correcto.")
        return

    print("🔄 Iniciando migración de base de datos...")
    print(f"📦 Creando backup en: {backup_path}")

    # Crear backup
    import shutil
    shutil.copy2(db_path, backup_path)
    print("✅ Backup creado exitosamente")

    # Conectar a la base de datos
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Verificar si la columna 'monto' existe
        cursor.execute("PRAGMA table_info(gastos)")
        columnas = cursor.fetchall()
        columna_existe = any(col[1] == 'monto' for col in columnas)

        if not columna_existe:
            print("✅ La base de datos ya tiene la columna 'cantidad'. No se requiere migración.")
            conn.close()
            return

        print("🔄 Renombrando columna 'monto' a 'cantidad'...")

        # Crear tabla temporal con el nuevo esquema
        cursor.execute('''
            CREATE TABLE gastos_temp (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                descripcion TEXT NOT NULL,
                cantidad REAL NOT NULL,
                categoria_id INTEGER NOT NULL,
                fecha DATE NOT NULL,
                mes INTEGER NOT NULL,
                anio INTEGER NOT NULL,
                FOREIGN KEY (categoria_id) REFERENCES categorias(id)
            )
        ''')

        # Copiar datos de la tabla antigua a la nueva
        cursor.execute('''
            INSERT INTO gastos_temp (id, descripcion, cantidad, categoria_id, fecha, mes, anio)
            SELECT id, descripcion, monto, categoria_id, fecha, mes, anio
            FROM gastos
        ''')

        # Eliminar tabla antigua
        cursor.execute('DROP TABLE gastos')

        # Renombrar tabla temporal
        cursor.execute('ALTER TABLE gastos_temp RENAME TO gastos')

        conn.commit()

        print("✅ Migración completada exitosamente!")
        print(f"📊 Columna 'monto' renombrada a 'cantidad'")

        # Verificar cantidad de registros
        cursor.execute("SELECT COUNT(*) FROM gastos")
        total_gastos = cursor.fetchone()[0]
        print(f"✅ {total_gastos} registros migrados correctamente")

    except Exception as e:
        print(f"❌ Error durante la migración: {e}")
        print(f"💾 Puedes restaurar desde el backup: {backup_path}")
        conn.rollback()
        raise

    finally:
        conn.close()

    print("\n" + "="*80)
    print("✅ MIGRACIÓN COMPLETADA")
    print("="*80)
    print(f"Backup guardado en: {backup_path}")
    print("Ahora puedes ejecutar la aplicación normalmente con: python3 app.py")
    print("="*80)


if __name__ == "__main__":
    migrar_base_datos()

