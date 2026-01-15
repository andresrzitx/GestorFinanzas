#!/usr/bin/env python3
"""
Script simple para migrar la base de datos y crear un usuario de prueba.
"""

import sqlite3
import hashlib
import shutil
from datetime import datetime

print("=" * 70)
print("MIGRACIÓN Y SETUP INICIAL - FinanzApp")
print("=" * 70)
print()

# Hacer backup
db_name = "gastos_mensuales.db"
backup_name = f"gastos_mensuales_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"

try:
    shutil.copy2(db_name, backup_name)
    print(f"✅ Backup creado: {backup_name}")
except:
    print("⚠️  No se pudo crear backup (quizás es primera ejecución)")

print()
print("🔧 Actualizando estructura de base de datos...")

conn = sqlite3.connect(db_name)
cursor = conn.cursor()

try:
    # Verificar si la tabla usuarios existe
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='usuarios'")
    if not cursor.fetchone():
        print("📝 Creando tabla usuarios...")
        cursor.execute('''
            CREATE TABLE usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        print("✅ Tabla usuarios creada")

    # Verificar estructura de categorías
    cursor.execute("PRAGMA table_info(categorias)")
    columnas_cat = [col[1] for col in cursor.fetchall()]

    if 'usuario_id' not in columnas_cat:
        print("📝 Actualizando tabla categorías...")
        cursor.execute("ALTER TABLE categorias ADD COLUMN usuario_id INTEGER")
        print("✅ Columna usuario_id agregada a categorías")

    # Verificar estructura de gastos
    cursor.execute("PRAGMA table_info(gastos)")
    columnas_gas = [col[1] for col in cursor.fetchall()]

    if 'usuario_id' not in columnas_gas:
        print("📝 Actualizando tabla gastos...")
        cursor.execute("ALTER TABLE gastos ADD COLUMN usuario_id INTEGER DEFAULT 1")
        print("✅ Columna usuario_id agregada a gastos")

    # Verificar estructura de ingresos
    cursor.execute("PRAGMA table_info(ingresos)")
    columnas_ing = [col[1] for col in cursor.fetchall()]

    if 'usuario_id' not in columnas_ing:
        print("📝 Actualizando tabla ingresos...")
        cursor.execute("ALTER TABLE ingresos ADD COLUMN usuario_id INTEGER DEFAULT 1")
        print("✅ Columna usuario_id agregada a ingresos")

    conn.commit()

    print()
    print("👤 Creando usuario de prueba...")

    # Crear usuario de prueba
    password_hash = hashlib.sha256("123456".encode()).hexdigest()

    try:
        cursor.execute('''
            INSERT INTO usuarios (nombre, email, password_hash)
            VALUES (?, ?, ?)
        ''', ("Andrés", "andres@finanzapp.com", password_hash))
        conn.commit()
        print("✅ Usuario creado exitosamente!")
    except sqlite3.IntegrityError:
        print("⚠️  El usuario ya existe (esto es normal)")

    # Verificar login
    cursor.execute('''
        SELECT id, nombre FROM usuarios
        WHERE email = ? AND password_hash = ?
    ''', ("andres@finanzapp.com", password_hash))

    resultado = cursor.fetchone()

    print()
    print("=" * 70)
    print("✅ MIGRACIÓN COMPLETADA")
    print("=" * 70)
    print()
    print("🎉 Tu usuario de prueba está listo:")
    print()
    print("   📧 Email:      andres@finanzapp.com")
    print("   🔑 Contraseña: 123456")
    print()
    if resultado:
        print(f"   ✅ Usuario ID: {resultado[0]}")
        print(f"   👤 Nombre: {resultado[1]}")
    print()
    print("📱 Para iniciar la aplicación ejecuta:")
    print("   python3 app.py")
    print()

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    conn.rollback()
finally:
    conn.close()

