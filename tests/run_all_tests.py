"""
Test Runner Principal - Ejecuta todos los tests unitarios del proyecto.

Este script ejecuta todos los tests utilizando unittest para proporcionar
un reporte completo del estado de las pruebas.
"""

import unittest
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar todos los módulos de test
from tests import test_models, test_login, test_ingresos, test_gestion_categorias, test_gastos


def run_all_tests():
    """Ejecutar todos los tests del proyecto."""

    print("="*80)
    print(" 🧪 EJECUTANDO SUITE COMPLETA DE TESTS - FinanzApp")
    print("="*80)
    print()

    # Crear suite principal
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Agregar todos los tests
    suite.addTests(test_models.suite())
    suite.addTests(test_login.suite())
    suite.addTests(test_ingresos.suite())
    suite.addTests(test_gestion_categorias.suite())
    suite.addTests(test_gastos.suite())

    # Ejecutar con verbosidad
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Resumen final
    print()
    print("="*80)
    print(" 📊 RESUMEN DE TESTS")
    print("="*80)
    print(f" Tests ejecutados: {result.testsRun}")
    print(f" ✅ Exitosos: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f" ❌ Fallos: {len(result.failures)}")
    print(f" 💥 Errores: {len(result.errors)}")
    print("="*80)

    # Retornar código de salida
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(run_all_tests())
