"""
Tests unitarios para gestión de gastos.

Verifica las operaciones CRUD (Create, Read, Update, Delete) de gastos
y todas las funcionalidades relacionadas.
"""

import unittest
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database import Database


class TestGestionGastos(unittest.TestCase):
    """Tests para gestión de gastos."""

    def setUp(self):
        """Configurar el entorno de prueba antes de cada test."""
        # Usar usuario de prueba especial
        self.db = Database(usuario_id=998)
        self.mes_prueba = 1
        self.anio_prueba = 2026

        # Asegurar que existe una categoría para usar
        self.db.agregar_categoria("Test Categoría", "Para pruebas")
        categorias = self.db.obtener_categorias()
        self.categoria_id = categorias[0][0]

    def test_agregar_gasto(self):
        """Test: Agregar un nuevo gasto."""
        descripcion = "Compra de prueba"
        cantidad = 50.0
        fecha = "2026-01-15"

        exito = self.db.agregar_gasto(descripcion, cantidad, self.categoria_id, fecha)
        self.assertTrue(exito, "Debe poder agregar un gasto")

        # Verificar que se agregó
        gastos = self.db.obtener_gastos_mes(self.mes_prueba, self.anio_prueba)
        encontrado = any(g[1] == descripcion for g in gastos)
        self.assertTrue(encontrado, "El gasto debe estar en la BD")

    def test_agregar_gasto_con_metodo_pago(self):
        """Test: Agregar gasto especificando método de pago."""
        # Efectivo
        exito = self.db.agregar_gasto("Gasto efectivo", 30.0, self.categoria_id,
                                       "2026-01-16", metodo_pago="efectivo")
        self.assertTrue(exito)

        # Tarjeta
        exito = self.db.agregar_gasto("Gasto tarjeta", 40.0, self.categoria_id,
                                       "2026-01-17", metodo_pago="tarjeta")
        self.assertTrue(exito)

    def test_obtener_gastos_mes(self):
        """Test: Obtener gastos de un mes específico."""
        # Agregar algunos gastos
        self.db.agregar_gasto("Gasto 1", 10.0, self.categoria_id, "2026-01-05")
        self.db.agregar_gasto("Gasto 2", 20.0, self.categoria_id, "2026-01-10")

        gastos = self.db.obtener_gastos_mes(self.mes_prueba, self.anio_prueba)

        self.assertIsInstance(gastos, list)
        self.assertGreaterEqual(len(gastos), 2)

    def test_obtener_total_mes(self):
        """Test: Obtener total de gastos de un mes."""
        # Limpiar y agregar gastos conocidos
        cantidad1 = 100.0
        cantidad2 = 50.0
        self.db.agregar_gasto("Gasto 1", cantidad1, self.categoria_id, "2026-01-08")
        self.db.agregar_gasto("Gasto 2", cantidad2, self.categoria_id, "2026-01-09")

        total = self.db.obtener_total_mes(self.mes_prueba, self.anio_prueba)

        self.assertIsInstance(total, (int, float))
        self.assertGreaterEqual(total, cantidad1 + cantidad2)

    def test_actualizar_gasto(self):
        """Test: Actualizar un gasto existente."""
        # Agregar gasto
        self.db.agregar_gasto("Gasto original", 100.0, self.categoria_id, "2026-01-12")

        # Obtener ID
        gastos = self.db.obtener_gastos_mes(self.mes_prueba, self.anio_prueba)
        gasto_id = None
        for g in gastos:
            if g[1] == "Gasto original":
                gasto_id = g[0]
                break

        self.assertIsNotNone(gasto_id, "El gasto debe existir")

        # Actualizar
        nueva_desc = "Gasto modificado"
        nueva_cantidad = 150.0
        exito = self.db.actualizar_gasto(
            gasto_id, nueva_desc, nueva_cantidad,
            self.categoria_id, "2026-01-12", "tarjeta"
        )

        self.assertTrue(exito, "Debe poder actualizar el gasto")

        # Verificar cambios
        gastos = self.db.obtener_gastos_mes(self.mes_prueba, self.anio_prueba)
        encontrado = False
        for g in gastos:
            if g[0] == gasto_id:
                self.assertEqual(g[1], nueva_desc)
                self.assertEqual(g[2], nueva_cantidad)
                encontrado = True
                break

        self.assertTrue(encontrado, "Gasto actualizado debe existir")

    def test_eliminar_gasto(self):
        """Test: Eliminar un gasto."""
        # Agregar gasto
        descripcion_unica = "Gasto para eliminar XYZ"
        self.db.agregar_gasto(descripcion_unica, 25.0, self.categoria_id, "2026-01-20")

        # Obtener ID
        gastos = self.db.obtener_gastos_mes(self.mes_prueba, self.anio_prueba)
        gasto_id = None
        for g in gastos:
            if g[1] == descripcion_unica:
                gasto_id = g[0]
                break

        self.assertIsNotNone(gasto_id)

        # Eliminar
        exito = self.db.eliminar_gasto(gasto_id)
        self.assertTrue(exito, "Debe poder eliminar el gasto")

        # Verificar que ya no existe
        gastos = self.db.obtener_gastos_mes(self.mes_prueba, self.anio_prueba)
        encontrado = any(g[1] == descripcion_unica for g in gastos)
        self.assertFalse(encontrado, "El gasto no debe existir")

    def test_obtener_gastos_por_categoria_mes(self):
        """Test: Obtener gastos agrupados por categoría."""
        # Agregar gastos
        self.db.agregar_gasto("Gasto cat test", 75.0, self.categoria_id, "2026-01-11")

        gastos_categoria = self.db.obtener_gastos_por_categoria_mes(
            self.mes_prueba, self.anio_prueba
        )

        self.assertIsInstance(gastos_categoria, list)
        # Verificar que hay datos
        self.assertGreater(len(gastos_categoria), 0)

    def test_obtener_gastos_por_metodo_mes(self):
        """Test: Obtener gastos agrupados por método de pago."""
        # Agregar gastos con diferentes métodos
        self.db.agregar_gasto("Efectivo test", 50.0, self.categoria_id,
                              "2026-01-13", metodo_pago="efectivo")
        self.db.agregar_gasto("Tarjeta test", 100.0, self.categoria_id,
                              "2026-01-14", metodo_pago="tarjeta")

        gastos_metodo = self.db.obtener_gastos_por_metodo_mes(
            self.mes_prueba, self.anio_prueba
        )

        self.assertIsInstance(gastos_metodo, dict)
        self.assertIn('efectivo', gastos_metodo)
        self.assertIn('tarjeta', gastos_metodo)

        # Verificar que los totales son correctos
        self.assertGreaterEqual(gastos_metodo['efectivo'], 50.0)
        self.assertGreaterEqual(gastos_metodo['tarjeta'], 100.0)

    def test_obtener_comparacion_anual(self):
        """Test: Obtener comparación de gastos mensuales del año."""
        # Agregar gastos en diferentes meses
        self.db.agregar_gasto("Enero", 100.0, self.categoria_id, "2026-01-01")
        self.db.agregar_gasto("Febrero", 150.0, self.categoria_id, "2026-02-01")

        comparacion = self.db.obtener_comparacion_anual(self.anio_prueba)

        self.assertIsInstance(comparacion, list)
        # Devuelve solo los meses con datos
        self.assertGreaterEqual(len(comparacion), 2, "Debe haber al menos 2 meses con datos")

        # Verificar estructura: (mes, total)
        for mes_data in comparacion:
            self.assertIsInstance(mes_data, tuple)
            self.assertEqual(len(mes_data), 2)

    def test_obtener_total_anual(self):
        """Test: Obtener total de gastos del año completo."""
        # Agregar gastos en diferentes meses
        self.db.agregar_gasto("Enero", 100.0, self.categoria_id, "2026-01-01")
        self.db.agregar_gasto("Febrero", 150.0, self.categoria_id, "2026-02-01")
        self.db.agregar_gasto("Marzo", 200.0, self.categoria_id, "2026-03-01")

        total_anual = self.db.obtener_total_anual(self.anio_prueba)

        self.assertIsInstance(total_anual, (int, float))
        self.assertGreaterEqual(total_anual, 450.0)

    def tearDown(self):
        """Limpiar después de cada test."""
        # Eliminar la base de datos de prueba
        try:
            db_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "data", "usuarios", "usuario_998_finanzas.db"
            )
            if os.path.exists(db_path):
                os.remove(db_path)
        except:
            pass


def suite():
    """Crear suite de tests."""
    loader = unittest.TestLoader()
    test_suite = unittest.TestSuite()
    test_suite.addTests(loader.loadTestsFromTestCase(TestGestionGastos))
    return test_suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())
