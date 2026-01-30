"""
Script para crear un usuario administrador.
"""

import sys
import os

# Agregar el directorio raíz al path para poder importar desde src
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database import Database


def crear_admin():
    print("=" * 70)
    print("  CREAR USUARIO ADMINISTRADOR - FinanzApp")
    print("=" * 70)
    print()

    # Crear instancia de Database sin usuario (solo para gestión de usuarios)
    db = Database()

    # Solicitar datos del administrador
    print("Ingresa los datos del nuevo administrador:")
    print("-" * 70)

    nombre = input("Nombre completo: ").strip()
    if not nombre:
        print("❌ Error: El nombre es obligatorio")
        return False

    email = input("Email: ").strip()
    if not email:
        print("❌ Error: El email es obligatorio")
        return False

    # Validación básica de email
    if '@' not in email or '.' not in email:
        print("❌ Error: El email no parece válido")
        return False

    password = input("Contraseña: ").strip()
    if not password:
        print("❌ Error: La contraseña es obligatoria")
        return False

    if len(password) < 6:
        print("⚠️  Advertencia: La contraseña es muy corta (mínimo recomendado: 6 caracteres)")
        confirmar = input("¿Continuar de todas formas? (s/n): ").lower()
        if confirmar != 's':
            print("❌ Operación cancelada")
            return False

    print()
    print("-" * 70)
    print("Resumen:")
    print(f"  Nombre: {nombre}")
    print(f"  Email:  {email}")
    print(f"  Rol:    Administrador")
    print("-" * 70)

    confirmar = input("\n¿Crear este usuario administrador? (s/n): ").lower()

    if confirmar != 's':
        print("❌ Operación cancelada")
        return False

    print()
    print("Creando usuario...")

    # Intentar registrar el usuario
    exito, mensaje = db.registrar_usuario(nombre, email, password)

    if not exito:
        print(f"❌ Error al crear usuario: {mensaje}")

        # Si el error es que ya existe, ofrecer cambiar a admin
        if "ya está registrado" in mensaje.lower():
            print()
            cambiar = input("¿Quieres cambiar este usuario a administrador? (s/n): ").lower()

            if cambiar == 's':
                # Obtener el ID del usuario
                conn = db.get_usuarios_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT id FROM usuarios WHERE email = ?", (email,))
                result = cursor.fetchone()
                conn.close()

                if result:
                    user_id = result[0]
                    db.cambiar_rol_usuario(user_id, "admin")
                    print(f"✅ Usuario '{email}' convertido a administrador")
                    print(f"   ID: {user_id}")
                    return True
                else:
                    print("❌ Error: No se pudo encontrar el usuario")
                    return False

        return False

    # Obtener el ID del usuario creado
    conn = db.get_usuarios_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM usuarios WHERE email = ?", (email,))
    result = cursor.fetchone()

    if not result:
        print("❌ Error: Usuario creado pero no se pudo obtener su ID")
        conn.close()
        return False

    user_id = result[0]

    # Cambiar el rol a administrador
    db.cambiar_rol_usuario(user_id, "admin")

    conn.close()

    print()
    print("=" * 70)
    print("✅ USUARIO ADMINISTRADOR CREADO EXITOSAMENTE")
    print("=" * 70)
    print(f"ID:     {user_id}")
    print(f"Nombre: {nombre}")
    print(f"Email:  {email}")
    print(f"Rol:    Administrador")
    print("=" * 70)
    print()
    print("Ahora puedes iniciar sesión en la aplicación con estas credenciales.")
    print()

    return True


def listar_admins():
    """Lista todos los administradores actuales del sistema."""
    db = Database()

    conn = db.get_usuarios_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, nombre, email, fecha_registro, activo
        FROM usuarios
        WHERE rol = 'admin'
        ORDER BY id
    """)

    admins = cursor.fetchall()
    conn.close()

    if not admins:
        print("No hay administradores registrados en el sistema.")
        return

    print()
    print("=" * 80)
    print("  ADMINISTRADORES DEL SISTEMA")
    print("=" * 80)
    print(f"{'ID':<5} {'Nombre':<20} {'Email':<30} {'Estado':<10}")
    print("-" * 80)

    for user_id, nombre, email, fecha_reg, activo in admins:
        estado = "✅ Activo" if activo else "❌ Inactivo"
        print(f"{user_id:<5} {nombre:<20} {email:<30} {estado:<10}")

    print("-" * 80)
    print(f"Total: {len(admins)} administrador(es)")
    print("=" * 80)
    print()


def convertir_a_admin():
    """Convierte un usuario existente a administrador."""
    db = Database()

    print()
    print("=" * 70)
    print("  CONVERTIR USUARIO A ADMINISTRADOR")
    print("=" * 70)
    print()

    # Listar usuarios no-admin
    conn = db.get_usuarios_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, nombre, email
        FROM usuarios
        WHERE rol != 'admin'
        ORDER BY id
    """)

    usuarios = cursor.fetchall()

    if not usuarios:
        print("No hay usuarios estándar en el sistema.")
        conn.close()
        return

    print("Usuarios disponibles:")
    print("-" * 70)
    print(f"{'ID':<5} {'Nombre':<25} {'Email'}")
    print("-" * 70)

    for user_id, nombre, email in usuarios:
        print(f"{user_id:<5} {nombre:<25} {email}")

    print("-" * 70)
    print()

    try:
        user_id = int(input("Ingresa el ID del usuario a convertir (0 para cancelar): "))

        if user_id == 0:
            print("❌ Operación cancelada")
            conn.close()
            return

        # Verificar que el usuario existe
        cursor.execute("SELECT nombre, email FROM usuarios WHERE id = ?", (user_id,))
        result = cursor.fetchone()

        if not result:
            print(f"❌ Error: No existe un usuario con ID {user_id}")
            conn.close()
            return

        nombre, email = result

        print()
        print(f"Usuario seleccionado:")
        print(f"  ID:    {user_id}")
        print(f"  Nombre: {nombre}")
        print(f"  Email:  {email}")
        print()

        confirmar = input("¿Convertir a administrador? (s/n): ").lower()

        if confirmar != 's':
            print("❌ Operación cancelada")
            conn.close()
            return

        # Cambiar rol
        db.cambiar_rol_usuario(user_id, "admin")

        print()
        print(f"✅ Usuario '{nombre}' convertido a administrador exitosamente")

    except ValueError:
        print("❌ Error: ID inválido")

    finally:
        conn.close()


def menu_principal():
    """Menú principal del script."""
    while True:
        print()
        print("=" * 70)
        print("  GESTIÓN DE ADMINISTRADORES - FinanzApp")
        print("=" * 70)
        print()
        print("1. Crear nuevo administrador")
        print("2. Listar administradores existentes")
        print("3. Convertir usuario existente a admin")
        print("0. Salir")
        print()

        opcion = input("Selecciona una opción: ").strip()

        if opcion == "0":
            print()
            print("¡Hasta pronto! 👋")
            print()
            break

        elif opcion == "1":
            crear_admin()

        elif opcion == "2":
            listar_admins()

        elif opcion == "3":
            convertir_a_admin()

        else:
            print("❌ Opción inválida")


if __name__ == "__main__":
    print()
    print("🔐 Gestor de Administradores - FinanzApp")
    print()

    try:
        menu_principal()
    except KeyboardInterrupt:
        print()
        print()
        print("❌ Operación interrumpida por el usuario")
        print()
    except Exception as e:
        print()
        print(f"❌ Error inesperado: {e}")
        print()
        import traceback
        traceback.print_exc()
