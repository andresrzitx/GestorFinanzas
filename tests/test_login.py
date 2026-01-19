from src.database import Database

print("Iniciando...")
db = Database()

email = "admin@finanzapp.com"
password = "admin123"

print(f"Intentando autenticar: {email}")
resultado = db.autenticar_usuario(email, password)

print(f"Resultado: {resultado}")

if resultado:
    user_id, nombre, rol = resultado
    print(f"✅ LOGIN EXITOSO!")
    print(f"ID: {user_id}")
    print(f"Nombre: {nombre}")
    print(f"Rol: {rol}")
else:
    print("❌ LOGIN FALLÓ - Creando usuario...")

    # Crear usuario
    exito, msg = db.registrar_usuario("Administrador", email, password)
    print(f"Registro: {msg}")

    if exito or "ya está registrado" in msg:
        # Obtener ID
        conn = db.get_usuarios_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM usuarios WHERE email = ?", (email,))
        uid = cursor.fetchone()[0]
        conn.close()

        # Hacer admin
        db.cambiar_rol_usuario(uid, "admin")
        print(f"Usuario {uid} es ahora admin")

        # Intentar de nuevo
        resultado = db.autenticar_usuario(email, password)
        if resultado:
            print(f"✅ Ahora funciona: {resultado}")
        else:
            print("❌ Aún falla")

