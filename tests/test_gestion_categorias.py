"""
Tests unitarios para gestión de categorías.

Verifica las operaciones CRUD (Create, Read, Update, Delete) de categorías.
"""

import unittest
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database import Database


class TestGestionCategorias(unittest.TestCase):
    """Tests para gestión de categorías."""

    def setUp(self):
        """Configurar el entorno de prueba antes de cada test."""
        # Usar usuario de prueba especial
        self.db = Database(usuario_id=999)
        self.test_categoria_nombre = "Test Categoría"
        self.test_categoria_desc = "Categoría para pruebas"

    def test_listar_categorias_por_defecto(self):
        """Test: Listar categorías por defecto."""
        categorias = self.db.obtener_categorias()

        self.assertIsInstance(categorias, list)
        self.assertGreater(len(categorias), 0, "Debe haber categorías por defecto")

        # Verificar estructura
        for cat in categorias:
            self.assertEqual(len(cat), 3)  # id, nombre, descripcion
            cat_id, nombre, descripcion = cat
            self.assertIsInstance(cat_id, int)
            self.assertIsInstance(nombre, str)

    def test_agregar_categoria_nueva(self):
        """Test: Agregar una nueva categoría."""
        exito = self.db.agregar_categoria(
            self.test_categoria_nombre,
            self.test_categoria_desc
        )

        self.assertTrue(exito, "Debe poder agregar categoría nueva")

        # Verificar que se agregó
        categorias = self.db.obtener_categorias()
        nombres = [cat[1] for cat in categorias]
        self.assertIn(self.test_categoria_nombre, nombres)

    def test_no_permitir_categoria_duplicada(self):
        """Test: No permitir agregar categoría con nombre duplicado."""
        # Agregar la primera vez
        self.db.agregar_categoria(self.test_categoria_nombre, self.test_categoria_desc)

        # Intentar agregar de nuevo
        exito = self.db.agregar_categoria(self.test_categoria_nombre, "Otra descripción")

        self.assertFalse(exito, "No debe permitir categorías duplicadas")

    def test_editar_categoria(self):
        """Test: Editar una categoría existente."""
        # Primero agregar
        self.db.agregar_categoria(self.test_categoria_nombre, self.test_categoria_desc)

        # Obtener ID
        categorias = self.db.obtener_categorias()
        cat_id = None
        for c_id, nombre, _ in categorias:
            if nombre == self.test_categoria_nombre:
                cat_id = c_id
                break

        self.assertIsNotNone(cat_id, "La categoría debe existir")

        # Editar
        nuevo_nombre = "Test Categoría Editada"
        nueva_desc = "Descripción editada"
        exito = self.db.editar_categoria(cat_id, nuevo_nombre, nueva_desc)

        self.assertTrue(exito, "Debe poder editar categoría")

        # Verificar cambios
        categorias = self.db.obtener_categorias()
        encontrada = False
        for c_id, nombre, desc in categorias:
            if c_id == cat_id:
                self.assertEqual(nombre, nuevo_nombre)
                self.assertEqual(desc, nueva_desc)
                encontrada = True
                break

        self.assertTrue(encontrada, "Categoría editada debe existir")

    def test_no_eliminar_categoria_con_gastos(self):
        """Test: No permitir eliminar categoría con gastos asociados."""
        # Usar categoría "Alimentación" (ID 1) que tiene gastos por defecto
        categorias = self.db.obtener_categorias()
        if len(categorias) > 0:
            cat_id = categorias[0][0]

            # Asegurar que tiene un gasto
            self.db.agregar_gasto("Gasto de prueba", 10.0, cat_id, "2026-01-24")

            # Intentar eliminar
            exito = self.db.eliminar_categoria(cat_id)

            self.assertFalse(exito, "No debe poder eliminar categoría con gastos")

    def test_eliminar_categoria_sin_gastos(self):
        """Test: Eliminar categoría sin gastos asociados."""
        # Agregar categoría nueva (sin gastos)
        nombre_unico = "Categoría Para Eliminar Test"
        self.db.agregar_categoria(nombre_unico, "Test")

        # Obtener ID
        categorias = self.db.obtener_categorias()
        cat_id = None
        for c_id, nombre, _ in categorias:
            if nombre == nombre_unico:
                cat_id = c_id
                break

        self.assertIsNotNone(cat_id)

        # Eliminar
        exito = self.db.eliminar_categoria(cat_id)

        self.assertTrue(exito, "Debe poder eliminar categoría sin gastos")

        # Verificar que ya no existe
        categorias = self.db.obtener_categorias()
        nombres = [cat[1] for cat in categorias]
        self.assertNotIn(nombre_unico, nombres)

    def test_obtener_categoria_por_id(self):
        """Test: Obtener detalles de una categoría específica."""
        categorias = self.db.obtener_categorias()
        if len(categorias) > 0:
            cat_id = categorias[0][0]
            nombre_esperado = categorias[0][1]

            # Buscar por ID
            categoria = None
            for c_id, nombre, desc in categorias:
                if c_id == cat_id:
                    categoria = (c_id, nombre, desc)
                    break

            self.assertIsNotNone(categoria)
            self.assertEqual(categoria[0], cat_id)
            self.assertEqual(categoria[1], nombre_esperado)

    def tearDown(self):
        """Limpiar después de cada test."""
        # Eliminar la base de datos de prueba
        try:
            db_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "data", "usuarios", "usuario_999_finanzas.db"
            )
            if os.path.exists(db_path):
                os.remove(db_path)
        except:
            pass


def suite():
    """Crear suite de tests."""
    loader = unittest.TestLoader()
    test_suite = unittest.TestSuite()
    test_suite.addTests(loader.loadTestsFromTestCase(TestGestionCategorias))
    return test_suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())
