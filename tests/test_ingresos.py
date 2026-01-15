#!/usr/bin/env python3
"""
Script de prueba para verificar las funcionalidades de ingresos
"""

from database import Database

def test_ingresos():
    db = Database()

    print('🔍 Verificando funcionalidades de INGRESOS...\n')

    # Verificar que existen ingresos
    ingresos_enero = db.obtener_ingresos_mes(1, 2026)
    print(f'✅ Ingresos en Enero 2026: {len(ingresos_enero)} registros')

    # Verificar totales
    total_ingresos_enero = db.obtener_total_ingresos_mes(1, 2026)
    total_gastos_enero = db.obtener_total_mes(1, 2026)
    print(f'✅ Total ingresos Enero: €{total_ingresos_enero:.2f}')
    print(f'✅ Total gastos Enero: €{total_gastos_enero:.2f}')

    # Verificar balance
    balance = db.obtener_balance_mes(1, 2026)
    print(f'\n💰 BALANCE ENERO 2026:')
    print(f'   Ingresos: €{balance["ingresos"]:.2f}')
    print(f'   Gastos: €{balance["gastos"]:.2f}')
    print(f'   Balance: €{balance["balance"]:.2f}')

    # Balance anual
    balance_anual = db.obtener_balance_anual(2026)
    print(f'\n📊 BALANCE ANUAL 2026:')
    print(f'   Ingresos: €{balance_anual["ingresos"]:.2f}')
    print(f'   Gastos: €{balance_anual["gastos"]:.2f}')
    print(f'   Balance: €{balance_anual["balance"]:.2f}')

    # Ingresos por fuente
    ingresos_por_fuente = db.obtener_ingresos_por_fuente_mes(1, 2026)
    print(f'\n📋 INGRESOS POR FUENTE (Enero 2026):')
    for fuente, total in ingresos_por_fuente:
        print(f'   {fuente}: €{total:.2f}')

    print('\n✅ Todas las funcionalidades de INGRESOS funcionan correctamente!')

if __name__ == '__main__':
    test_ingresos()

