"""
Tests unitarios para las funcionalidades de ingresos.

Verifica que todas las operaciones relacionadas con ingresos funcionen correctamente.
"""

import unittest
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database import Database


class TestIngresos(unittest.TestCase):
    """Tests para las funcionalidades de ingresos."""

    def setUp(self):
        """Configurar el entorno de prueba antes de cada test."""
        # Usar usuario_id=1 para pruebas (debe existir en la BD)
        self.db = Database(usuario_id=1)
        self.mes_prueba = 1
        self.anio_prueba = 2026

    def test_obtener_ingresos_mes(self):
        """Test: Obtener ingresos de un mes específico."""
        ingresos = self.db.obtener_ingresos_mes(self.mes_prueba, self.anio_prueba)
        self.assertIsInstance(ingresos, list)
        # Verificar estructura de cada ingreso
        for ingreso in ingresos:
            self.assertGreaterEqual(len(ingreso), 4)  # id, descripcion, cantidad, fuente, fecha

    def test_obtener_total_ingresos_mes(self):
        """Test: Obtener total de ingresos de un mes."""
        total = self.db.obtener_total_ingresos_mes(self.mes_prueba, self.anio_prueba)
        self.assertIsInstance(total, (int, float))
        self.assertGreaterEqual(total, 0)

    def test_obtener_balance_mes(self):
        """Test: Obtener balance (ingresos - gastos) de un mes."""
        balance = self.db.obtener_balance_mes(self.mes_prueba, self.anio_prueba)

        self.assertIsInstance(balance, dict)
        self.assertIn('ingresos', balance)
        self.assertIn('gastos', balance)
        self.assertIn('balance', balance)

        # Verificar que el balance es la diferencia
        self.assertEqual(
            balance['balance'],
            balance['ingresos'] - balance['gastos']
        )

    def test_obtener_balance_anual(self):
        """Test: Obtener balance anual."""
        balance_anual = self.db.obtener_balance_anual(self.anio_prueba)

        self.assertIsInstance(balance_anual, dict)
        self.assertIn('ingresos', balance_anual)
        self.assertIn('gastos', balance_anual)
        self.assertIn('balance', balance_anual)

        # El balance debe ser ingresos - gastos
        self.assertEqual(
            balance_anual['balance'],
            balance_anual['ingresos'] - balance_anual['gastos']
        )

    def test_obtener_ingresos_por_fuente_mes(self):
        """Test: Obtener ingresos agrupados por fuente."""
        ingresos_por_fuente = self.db.obtener_ingresos_por_fuente_mes(
            self.mes_prueba,
            self.anio_prueba
        )

        self.assertIsInstance(ingresos_por_fuente, list)

        # Verificar estructura: cada elemento debe ser (fuente, total)
        for item in ingresos_por_fuente:
            self.assertEqual(len(item), 2)
            fuente, total = item
            self.assertIsInstance(fuente, str)
            self.assertIsInstance(total, (int, float))
            self.assertGreaterEqual(total, 0)

    def test_agregar_ingreso(self):
        """Test: Agregar un nuevo ingreso."""
        descripcion = "Test Ingreso"
        cantidad = 1000.0
        fecha = "2026-01-15"

        # Agregar ingreso
        exito = self.db.agregar_ingreso(descripcion, cantidad, fecha)
        self.assertTrue(exito, "No se pudo agregar el ingreso")

        # Verificar que se agregó
        ingresos = self.db.obtener_ingresos_mes(self.mes_prueba, self.anio_prueba)
        ingreso_agregado = any(
            ing[1] == descripcion and ing[2] == cantidad
            for ing in ingresos
        )
        self.assertTrue(ingreso_agregado, "El ingreso no se encuentra en la BD")

    def test_comparacion_ingresos_vs_gastos(self):
        """Test: Comparar ingresos vs gastos."""
        balance = self.db.obtener_balance_mes(self.mes_prueba, self.anio_prueba)

        ingresos = balance['ingresos']
        gastos = balance['gastos']

        # Ambos deben ser números no negativos
        self.assertGreaterEqual(ingresos, 0)
        self.assertGreaterEqual(gastos, 0)

        # El balance debe reflejar la diferencia
        if ingresos > gastos:
            self.assertGreater(balance['balance'], 0, "Balance positivo esperado")
        elif gastos > ingresos:
            self.assertLess(balance['balance'], 0, "Balance negativo esperado")
        else:
            self.assertEqual(balance['balance'], 0, "Balance neutro esperado")


def suite():
    """Crear suite de tests."""
    loader = unittest.TestLoader()
    test_suite = unittest.TestSuite()
    test_suite.addTests(loader.loadTestsFromTestCase(TestIngresos))
    return test_suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())
