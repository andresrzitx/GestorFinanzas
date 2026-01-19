"""
Tests unitarios para los modelos de FinanzApp.

Estos tests verifican que las clases del modelo funcionen correctamente
y demuestran el uso de TDD (Test-Driven Development).
"""

import unittest
from datetime import datetime
import sys
import os

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from models import Usuario, Categoria, Gasto, Ingreso, GrupoGasto


class TestUsuario(unittest.TestCase):
    """Tests para la clase Usuario."""

    def test_crear_usuario_basico(self):
        """Test: Crear un usuario con datos básicos."""
        user = Usuario(
            id=1,
            nombre="Juan Pérez",
            email="juan@test.com"
        )

        self.assertEqual(user.id, 1)
        self.assertEqual(user.nombre, "Juan Pérez")
        self.assertEqual(user.email, "juan@test.com")
        self.assertEqual(user.rol, "usuario")  # Valor por defecto
        self.assertTrue(user.activo)  # Valor por defecto

    def test_usuario_es_admin(self):
        """Test: Verificar si un usuario es administrador."""
        admin = Usuario(1, "Admin", "admin@test.com", rol="admin")
        usuario = Usuario(2, "User", "user@test.com", rol="usuario")

        self.assertTrue(admin.es_admin())
        self.assertFalse(usuario.es_admin())

    def test_usuario_es_activo(self):
        """Test: Verificar si un usuario está activo."""
        activo = Usuario(1, "Activo", "activo@test.com", activo=True)
        inactivo = Usuario(2, "Inactivo", "inactivo@test.com", activo=False)

        self.assertTrue(activo.es_activo())
        self.assertFalse(inactivo.es_activo())

    def test_actualizar_ultimo_acceso(self):
        """Test: Actualizar la fecha del último acceso."""
        user = Usuario(1, "Test", "test@test.com")

        self.assertIsNone(user.ultimo_acceso)
        user.actualizar_ultimo_acceso()
        self.assertIsNotNone(user.ultimo_acceso)
        self.assertIsInstance(user.ultimo_acceso, datetime)

    def test_usuario_to_dict(self):
        """Test: Convertir usuario a diccionario."""
        user = Usuario(1, "Test", "test@test.com", rol="admin")
        user_dict = user.to_dict()

        self.assertIsInstance(user_dict, dict)
        self.assertEqual(user_dict['id'], 1)
        self.assertEqual(user_dict['nombre'], "Test")
        self.assertEqual(user_dict['email'], "test@test.com")
        self.assertEqual(user_dict['rol'], "admin")

    def test_usuario_repr(self):
        """Test: Representación en string del usuario."""
        user = Usuario(1, "Test", "test@test.com")
        repr_str = repr(user)

        self.assertIn("Usuario", repr_str)
        self.assertIn("Test", repr_str)
        self.assertIn("test@test.com", repr_str)


class TestCategoria(unittest.TestCase):
    """Tests para la clase Categoria."""

    def test_crear_categoria(self):
        """Test: Crear una categoría básica."""
        cat = Categoria(1, "Alimentación", "Gastos en comida")

        self.assertEqual(cat.id, 1)
        self.assertEqual(cat.nombre, "Alimentación")
        self.assertEqual(cat.descripcion, "Gastos en comida")

    def test_categoria_sin_descripcion(self):
        """Test: Crear categoría sin descripción."""
        cat = Categoria(1, "Transporte")

        self.assertEqual(cat.nombre, "Transporte")
        self.assertEqual(cat.descripcion, "")

    def test_categoria_to_dict(self):
        """Test: Convertir categoría a diccionario."""
        cat = Categoria(1, "Ocio", "Entretenimiento")
        cat_dict = cat.to_dict()

        self.assertIsInstance(cat_dict, dict)
        self.assertEqual(cat_dict['id'], 1)
        self.assertEqual(cat_dict['nombre'], "Ocio")
        self.assertEqual(cat_dict['descripcion'], "Entretenimiento")

    def test_categoria_str(self):
        """Test: String legible de categoría."""
        cat = Categoria(1, "Salud")
        self.assertEqual(str(cat), "Salud")


class TestGasto(unittest.TestCase):
    """Tests para la clase Gasto."""

    def test_crear_gasto_efectivo(self):
        """Test: Crear un gasto pagado en efectivo."""
        gasto = Gasto(
            id=1,
            descripcion="Supermercado",
            cantidad=100.50,
            categoria_id=1,
            fecha="2026-01-19",
            metodo_pago="efectivo"
        )

        self.assertEqual(gasto.id, 1)
        self.assertEqual(gasto.descripcion, "Supermercado")
        self.assertEqual(gasto.cantidad, 100.50)
        self.assertEqual(gasto.categoria_id, 1)
        self.assertEqual(gasto.fecha, "2026-01-19")
        self.assertTrue(gasto.es_efectivo())
        self.assertFalse(gasto.es_tarjeta())

    def test_crear_gasto_tarjeta(self):
        """Test: Crear un gasto pagado con tarjeta."""
        gasto = Gasto(
            id=2,
            descripcion="Ropa",
            cantidad=250,
            categoria_id=2,
            fecha="2026-01-19",
            metodo_pago="tarjeta"
        )

        self.assertTrue(gasto.es_tarjeta())
        self.assertFalse(gasto.es_efectivo())

    def test_gasto_metodo_pago_invalido(self):
        """Test: Error al usar método de pago inválido."""
        with self.assertRaises(ValueError):
            Gasto(1, "Test", 100, 1, "2026-01-19", "criptomoneda")

    def test_gasto_get_mes(self):
        """Test: Obtener mes del gasto."""
        gasto = Gasto(1, "Test", 100, 1, "2026-03-15", "efectivo")
        self.assertEqual(gasto.get_mes(), 3)

    def test_gasto_get_anio(self):
        """Test: Obtener año del gasto."""
        gasto = Gasto(1, "Test", 100, 1, "2026-03-15", "efectivo")
        self.assertEqual(gasto.get_anio(), 2026)

    def test_gasto_cantidad_como_string(self):
        """Test: Convertir cantidad string a float automáticamente."""
        gasto = Gasto(1, "Test", "123.45", 1, "2026-01-19", "efectivo")
        self.assertEqual(gasto.cantidad, 123.45)
        self.assertIsInstance(gasto.cantidad, float)

    def test_gasto_to_dict(self):
        """Test: Convertir gasto a diccionario."""
        gasto = Gasto(1, "Cena", 50, 1, "2026-01-19", "tarjeta")
        gasto_dict = gasto.to_dict()

        self.assertIsInstance(gasto_dict, dict)
        self.assertEqual(gasto_dict['descripcion'], "Cena")
        self.assertEqual(gasto_dict['cantidad'], 50)
        self.assertEqual(gasto_dict['metodo_pago'], "tarjeta")


class TestIngreso(unittest.TestCase):
    """Tests para la clase Ingreso."""

    def test_crear_ingreso(self):
        """Test: Crear un ingreso básico."""
        ingreso = Ingreso(
            id=1,
            descripcion="Salario",
            cantidad=3000,
            fecha="2026-01-15"
        )

        self.assertEqual(ingreso.id, 1)
        self.assertEqual(ingreso.descripcion, "Salario")
        self.assertEqual(ingreso.cantidad, 3000.0)
        self.assertEqual(ingreso.fecha, "2026-01-15")

    def test_ingreso_get_mes(self):
        """Test: Obtener mes del ingreso."""
        ingreso = Ingreso(1, "Bono", 500, "2026-06-10")
        self.assertEqual(ingreso.get_mes(), 6)

    def test_ingreso_get_anio(self):
        """Test: Obtener año del ingreso."""
        ingreso = Ingreso(1, "Freelance", 1000, "2025-12-20")
        self.assertEqual(ingreso.get_anio(), 2025)

    def test_ingreso_cantidad_como_string(self):
        """Test: Convertir cantidad string a float."""
        ingreso = Ingreso(1, "Venta", "450.75", "2026-01-19")
        self.assertEqual(ingreso.cantidad, 450.75)
        self.assertIsInstance(ingreso.cantidad, float)

    def test_ingreso_to_dict(self):
        """Test: Convertir ingreso a diccionario."""
        ingreso = Ingreso(1, "Salario", 3000, "2026-01-15")
        ingreso_dict = ingreso.to_dict()

        self.assertIsInstance(ingreso_dict, dict)
        self.assertEqual(ingreso_dict['id'], 1)
        self.assertEqual(ingreso_dict['descripcion'], "Salario")
        self.assertEqual(ingreso_dict['cantidad'], 3000)


class TestGrupoGasto(unittest.TestCase):
    """Tests para la clase GrupoGasto."""

    def test_crear_grupo(self):
        """Test: Crear un grupo de gastos."""
        grupo = GrupoGasto(
            id=1,
            nombre="Viaje a la playa",
            descripcion="Vacaciones en grupo",
            creador_id=1
        )

        self.assertEqual(grupo.id, 1)
        self.assertEqual(grupo.nombre, "Viaje a la playa")
        self.assertEqual(grupo.creador_id, 1)
        self.assertEqual(len(grupo.miembros), 0)

    def test_agregar_miembro(self):
        """Test: Agregar miembros al grupo."""
        grupo = GrupoGasto(1, "Cena", "Cena grupal", 1)

        grupo.agregar_miembro(2)
        grupo.agregar_miembro(3)

        self.assertEqual(len(grupo.miembros), 2)
        self.assertIn(2, grupo.miembros)
        self.assertIn(3, grupo.miembros)

    def test_agregar_miembro_duplicado(self):
        """Test: No agregar miembros duplicados."""
        grupo = GrupoGasto(1, "Test", "Test", 1)

        grupo.agregar_miembro(2)
        grupo.agregar_miembro(2)  # Duplicado

        self.assertEqual(len(grupo.miembros), 1)

    def test_remover_miembro(self):
        """Test: Remover miembro del grupo."""
        grupo = GrupoGasto(1, "Test", "Test", 1)
        grupo.agregar_miembro(2)
        grupo.agregar_miembro(3)

        grupo.remover_miembro(2)

        self.assertEqual(len(grupo.miembros), 1)
        self.assertNotIn(2, grupo.miembros)
        self.assertIn(3, grupo.miembros)

    def test_es_miembro(self):
        """Test: Verificar si un usuario es miembro."""
        grupo = GrupoGasto(1, "Test", "Test", 1)
        grupo.agregar_miembro(2)

        self.assertTrue(grupo.es_miembro(2))
        self.assertFalse(grupo.es_miembro(3))

    def test_grupo_to_dict(self):
        """Test: Convertir grupo a diccionario."""
        grupo = GrupoGasto(1, "Fiesta", "Cumpleaños", 1)
        grupo.agregar_miembro(2)
        grupo.agregar_miembro(3)

        grupo_dict = grupo.to_dict()

        self.assertIsInstance(grupo_dict, dict)
        self.assertEqual(grupo_dict['nombre'], "Fiesta")
        self.assertEqual(len(grupo_dict['miembros']), 2)


def suite():
    """
    Crea una suite de tests.

    Returns:
        unittest.TestSuite: Suite con todos los tests
    """
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(TestUsuario))
    test_suite.addTest(unittest.makeSuite(TestCategoria))
    test_suite.addTest(unittest.makeSuite(TestGasto))
    test_suite.addTest(unittest.makeSuite(TestIngreso))
    test_suite.addTest(unittest.makeSuite(TestGrupoGasto))
    return test_suite


if __name__ == '__main__':
    # Ejecutar tests
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())
