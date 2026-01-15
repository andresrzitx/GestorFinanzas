#!/usr/bin/env python3
"""Crear usuario administrador y verificar."""

from src.database import Database

# Crear instancia
db = Database()

# Credenciales
email = "admin@finanzapp.com"
password = "admin123"
nombre = "Administrador"

print("=" * 60)
print("CREANDO USUARIO ADMINISTRADOR")
print("=" * 60)

# Intentar registrar
exito, mensaje = db.registrar_usuario(nombre, email, password)
print(f"\nRegistro: {mensaje}")

# Obtener usuario
conn = db.get_usuarios_connection()
cursor = conn.cursor()
cursor.execute("SELECT id, nombre, email, rol, activo FROM usuarios WHERE email = ?", (email,))
usuario = cursor.fetchone()

if usuario:
    uid, unom, uemail, urol, uactivo = usuario
    print(f"\n✅ Usuario encontrado:")
    print(f"   ID:     {uid}")
    print(f"   Nombre: {unom}")
    print(f"   Email:  {uemail}")
    print(f"   Rol:    {urol}")
    print(f"   Activo: {uactivo}")

    # Asegurar que sea admin y activo
    if urol != 'admin':
        print(f"\n⚙️  Cambiando rol a admin...")
        db.cambiar_rol_usuario(uid, 'admin')
        print("   ✅ Rol actualizado")

    if not uactivo:
        print(f"\n⚙️  Activando usuario...")
        db.activar_desactivar_usuario(uid, True)
        print("   ✅ Usuario activado")

    # Verificar autenticación
    print(f"\n🔐 Probando autenticación...")
    resultado = db.autenticar_usuario(email, password)

    if resultado:
        auth_id, auth_nombre, auth_rol = resultado
        print(f"   ✅ LOGIN EXITOSO!")
        print(f"   ID:     {auth_id}")
        print(f"   Nombre: {auth_nombre}")
        print(f"   Rol:    {auth_rol}")
    else:
        print("   ❌ LOGIN FALLÓ")

conn.close()

print("\n" + "=" * 60)
print("CREDENCIALES:")
print("=" * 60)
print(f"Email:    {email}")
print(f"Password: {password}")
print("=" * 60)
print("\n✅ Listo! Ahora ejecuta: python3 main.py")
print("=" * 60)

