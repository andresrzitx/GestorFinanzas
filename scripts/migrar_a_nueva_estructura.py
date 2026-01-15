#!/usr/bin/env python3
"""Script para migrar usuarios de la base de datos antigua a la nueva estructura."""

import sqlite3
import os

def migrar_usuarios():
    """Migra los usuarios de gastos_mensuales.db a usuarios.db"""

    antigua_db = "gastos_mensuales.db"
    nueva_db = "usuarios.db"

    if not os.path.exists(antigua_db):
        print(f"No se encontró {antigua_db}, no hay nada que migrar.")
        return

    print("Migrando usuarios de la base de datos antigua...")

    # Conectar a la base de datos antigua
    conn_antigua = sqlite3.connect(antigua_db, timeout=10)
    cursor_antigua = conn_antigua.cursor()

    # Verificar si existe la tabla usuarios en la antigua
    cursor_antigua.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='usuarios'")
    if not cursor_antigua.fetchone():
        print("No hay tabla de usuarios en la base de datos antigua.")
        conn_antigua.close()
        return

    # Obtener usuarios existentes
    cursor_antigua.execute("SELECT id, nombre, email, password_hash, fecha_registro FROM usuarios")
    usuarios = cursor_antigua.fetchall()

    if not usuarios:
        print("No hay usuarios para migrar.")
        conn_antigua.close()
        return

    print(f"Encontrados {len(usuarios)} usuarios para migrar.")

    # Conectar a la nueva base de datos
    conn_nueva = sqlite3.connect(nueva_db, timeout=10)
    cursor_nueva = conn_nueva.cursor()

    # Crear tabla si no existe
    cursor_nueva.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Migrar usuarios
    migrados = 0
    for usuario in usuarios:
        id_usuario, nombre, email, password_hash, fecha_registro = usuario
        try:
            cursor_nueva.execute('''
                INSERT OR IGNORE INTO usuarios (id, nombre, email, password_hash, fecha_registro)
                VALUES (?, ?, ?, ?, ?)
            ''', (id_usuario, nombre, email, password_hash, fecha_registro))
            if cursor_nueva.rowcount > 0:
                migrados += 1
                print(f"  ✓ Migrado: {nombre} ({email})")
        except sqlite3.IntegrityError:
            print(f"  - Usuario ya existe: {email}")

    conn_nueva.commit()
    conn_nueva.close()
    conn_antigua.close()

    print(f"\n✓ Migración completada: {migrados} usuarios migrados.")

if __name__ == '__main__':
    migrar_usuarios()

