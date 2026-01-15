#!/usr/bin/env python3
"""Script simple para crear el usuario administrador."""

import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database import Database

def main():
    print("=" * 70)
    print("CREANDO USUARIO ADMINISTRADOR")
    print("=" * 70)

    db = Database()

    # Credenciales
    nombre = "Administrador"
    email = "admin@finanzapp.com"
    password = "admin123"

    print(f"\nIntentando crear usuario:")
    print(f"  Nombre: {nombre}")
    print(f"  Email:  {email}")
    print(f"  Pass:   {password}")

    # Registrar usuario
    exito, mensaje = db.registrar_usuario(nombre, email, password)

    if exito:
        print(f"\n✅ {mensaje}")

        # Obtener ID del usuario recién creado
        conn = db.get_usuarios_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM usuarios WHERE email = ?', (email,))
        result = cursor.fetchone()

        if result:
            usuario_id = result[0]

            # Cambiar rol a admin
            print(f"\n👨‍💼 Asignando rol de administrador (ID: {usuario_id})...")
            exito_rol, mensaje_rol = db.cambiar_rol_usuario(usuario_id, 'admin')

            if exito_rol:
                print(f"✅ {mensaje_rol}")

                # Verificar
                cursor.execute('SELECT id, nombre, email, rol, activo FROM usuarios WHERE id = ?', (usuario_id,))
                usuario = cursor.fetchone()

                if usuario:
                    uid, unom, uemail, urol, uactivo = usuario
                    print(f"\n✅ VERIFICACIÓN:")
                    print(f"  ID:     {uid}")
                    print(f"  Nombre: {unom}")
                    print(f"  Email:  {uemail}")
                    print(f"  Rol:    {urol}")
                    print(f"  Activo: {'Sí' if uactivo else 'No'}")

                    # Probar autenticación
                    print(f"\n🔐 Probando autenticación...")
                    resultado = db.autenticar_usuario(email, password)

                    if resultado:
                        auth_id, auth_nombre, auth_rol = resultado
                        print(f"✅ Autenticación EXITOSA!")
                        print(f"  ID:     {auth_id}")
                        print(f"  Nombre: {auth_nombre}")
                        print(f"  Rol:    {auth_rol}")
                    else:
                        print(f"❌ Autenticación FALLÓ")

        conn.close()

    else:
        if "ya está registrado" in mensaje:
            print(f"\n💡 {mensaje}")
            print(f"\n✅ El administrador ya existe en el sistema")

            # Verificar que sea admin
            conn = db.get_usuarios_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT id, nombre, email, rol, activo FROM usuarios WHERE email = ?', (email,))
            usuario = cursor.fetchone()

            if usuario:
                uid, unom, uemail, urol, uactivo = usuario
                print(f"\n📋 Datos del usuario existente:")
                print(f"  ID:     {uid}")
                print(f"  Nombre: {unom}")
                print(f"  Email:  {uemail}")
                print(f"  Rol:    {urol}")
                print(f"  Activo: {'Sí' if uactivo else 'No'}")

                # Si no es admin, hacerlo admin
                if urol != 'admin':
                    print(f"\n⚠️  El usuario existe pero NO es admin")
                    print(f"👨‍💼 Cambiando rol a admin...")
                    db.cambiar_rol_usuario(uid, 'admin')
                    print(f"✅ Rol actualizado a admin")

                # Si está inactivo, activarlo
                if not uactivo:
                    print(f"\n⚠️  El usuario está INACTIVO")
                    print(f"🔄 Activando usuario...")
                    db.activar_desactivar_usuario(uid, True)
                    print(f"✅ Usuario activado")

                # Probar autenticación
                print(f"\n🔐 Probando autenticación...")
                resultado = db.autenticar_usuario(email, password)

                if resultado:
                    auth_id, auth_nombre, auth_rol = resultado
                    print(f"✅ Autenticación EXITOSA!")
                    print(f"  ID:     {auth_id}")
                    print(f"  Nombre: {auth_nombre}")
                    print(f"  Rol:    {auth_rol}")
                else:
                    print(f"❌ Autenticación FALLÓ")
                    print(f"⚠️  Verifica que la contraseña sea correcta")

            conn.close()
        else:
            print(f"\n❌ Error: {mensaje}")

    print("\n" + "=" * 70)
    print("CREDENCIALES DE ACCESO:")
    print("=" * 70)
    print(f"Email:    {email}")
    print(f"Password: {password}")
    print("=" * 70)
    print("\n⚠️  IMPORTANTE: Cambia la contraseña después del primer login")
    print("=" * 70)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()

