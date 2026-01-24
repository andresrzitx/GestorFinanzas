"""
Tests unitarios para el sistema de login y autenticación.

Verifica que el sistema de autenticación y registro de usuarios funcione correctamente.
"""

import unittest
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database import Database


class TestLogin(unittest.TestCase):
    """Tests para el sistema de login y autenticación."""

    def setUp(self):
        """Configurar el entorno de prueba antes de cada test."""
        self.db = Database()
        self.test_email = "test_user@finanzapp.com"
        self.test_password = "test123"
        self.admin_email = "admin@finanzapp.com"
        self.admin_password = "admin123"

    def test_autenticar_credenciales_invalidas(self):
        """Test: Autenticar con credenciales inválidas debe fallar."""
        resultado = self.db.autenticar_usuario("noexiste@test.com", "wrongpass")
        self.assertIsNone(resultado)

    def test_registrar_nuevo_usuario(self):
        """Test: Registrar un nuevo usuario correctamente."""
        # Limpiar usuario de prueba si existe
        conn = self.db.get_usuarios_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM usuarios WHERE email = ?", (self.test_email,))
        conn.commit()
        conn.close()

        # Registrar usuario
        exito, mensaje = self.db.registrar_usuario("Test User", self.test_email, self.test_password)
        self.assertTrue(exito, f"Registro falló: {mensaje}")

        # Verificar que se puede autenticar
        resultado = self.db.autenticar_usuario(self.test_email, self.test_password)
        self.assertIsNotNone(resultado)
        user_id, nombre, rol = resultado
        self.assertEqual(nombre, "Test User")
        self.assertEqual(rol, "usuario")

    def test_registrar_usuario_duplicado(self):
        """Test: No permitir registrar usuario con email duplicado."""
        # Asegurar que existe el usuario
        self.db.registrar_usuario("Test User", self.test_email, self.test_password)

        # Intentar registrar de nuevo
        exito, mensaje = self.db.registrar_usuario("Otro Nombre", self.test_email, self.test_password)
        self.assertFalse(exito)
        self.assertIn("ya está registrado", mensaje.lower())

    def test_autenticar_usuario_existente(self):
        """Test: Autenticar usuario existente correctamente."""
        # Crear usuario si no existe
        self.db.registrar_usuario("Test User", self.test_email, self.test_password)

        # Autenticar
        resultado = self.db.autenticar_usuario(self.test_email, self.test_password)
        self.assertIsNotNone(resultado)
        self.assertEqual(len(resultado), 3)  # user_id, nombre, rol

    def test_cambiar_rol_usuario(self):
        """Test: Cambiar el rol de un usuario."""
        # Crear usuario
        self.db.registrar_usuario("Test User", self.test_email, self.test_password)

        # Obtener ID
        conn = self.db.get_usuarios_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM usuarios WHERE email = ?", (self.test_email,))
        user_id = cursor.fetchone()[0]
        conn.close()

        # Cambiar a admin
        self.db.cambiar_rol_usuario(user_id, "admin")

        # Verificar cambio
        resultado = self.db.autenticar_usuario(self.test_email, self.test_password)
        _, _, rol = resultado
        self.assertEqual(rol, "admin")

    def test_admin_usuario_existe(self):
        """Test: Verificar que el usuario admin existe o crearlo."""
        # Intentar autenticar admin
        resultado = self.db.autenticar_usuario(self.admin_email, self.admin_password)

        if not resultado:
            # Crear admin si no existe
            exito, _ = self.db.registrar_usuario("Administrador", self.admin_email, self.admin_password)

            if exito or True:  # Si ya existía o se creó
                # Obtener ID y hacer admin
                conn = self.db.get_usuarios_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT id FROM usuarios WHERE email = ?", (self.admin_email,))
                uid = cursor.fetchone()[0]
                conn.close()

                self.db.cambiar_rol_usuario(uid, "admin")

                # Verificar que ahora funciona
                resultado = self.db.autenticar_usuario(self.admin_email, self.admin_password)

        self.assertIsNotNone(resultado)
        _, nombre, rol = resultado
        self.assertEqual(rol, "admin")

    def tearDown(self):
        """Limpiar después de cada test."""
        # Eliminar usuario de prueba
        try:
            conn = self.db.get_usuarios_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM usuarios WHERE email = ?", (self.test_email,))
            conn.commit()
            conn.close()
        except:
            pass


def suite():
    """Crear suite de tests."""
    loader = unittest.TestLoader()
    test_suite = unittest.TestSuite()
    test_suite.addTests(loader.loadTestsFromTestCase(TestLogin))
    return test_suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())


