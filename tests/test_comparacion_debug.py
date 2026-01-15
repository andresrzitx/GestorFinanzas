"""Script para debuggear la vista de comparación anual"""
import sqlite3
import os

def test_comparacion_anual():
    # Usar la base de datos de un usuario de ejemplo
    db_path = "data/usuarios/usuario_2_finanzas.db"

    if not os.path.exists(db_path):
        print(f"❌ No se encontró la base de datos: {db_path}")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    anio = 2025

    print(f"\n📊 Datos de comparación anual para {anio}\n")
    print("="*80)

    # Obtener datos de gastos
    print("\n📉 GASTOS por mes:")
    cursor.execute('''
        SELECT mes, SUM(cantidad) as total
        FROM gastos
        WHERE anio = ?
        GROUP BY mes
        ORDER BY mes
    ''', (anio,))

    comparacion_gastos = cursor.fetchall()
    gastos_por_mes = {mes: 0.0 for mes in range(1, 13)}
    for mes, total in comparacion_gastos:
        gastos_por_mes[mes] = total
        print(f"  Mes {mes:2d}: €{total:.2f}")

    # Obtener datos de ingresos
    print("\n📈 INGRESOS por mes:")
    cursor.execute('''
        SELECT mes, SUM(cantidad) as total
        FROM ingresos
        WHERE anio = ?
        GROUP BY mes
        ORDER BY mes
    ''', (anio,))

    comparacion_ingresos = cursor.fetchall()
    ingresos_por_mes = {mes: 0.0 for mes in range(1, 13)}
    for mes, total in comparacion_ingresos:
        ingresos_por_mes[mes] = total
        print(f"  Mes {mes:2d}: €{total:.2f}")

    # Calcular balances
    print("\n💰 BALANCE por mes (Ingresos - Gastos):")
    meses_nombres = [
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ]

    total_ingresos = 0
    total_gastos = 0

    for mes in range(1, 13):
        ingresos = ingresos_por_mes[mes]
        gastos = gastos_por_mes[mes]
        balance = ingresos - gastos

        total_ingresos += ingresos
        total_gastos += gastos

        estado = "✅" if balance > 0 else "⚠️" if balance < 0 else "➖"
        print(f"  {meses_nombres[mes-1]:12s} | Ingresos: €{ingresos:8.2f} | Gastos: €{gastos:8.2f} | Balance: €{balance:+9.2f} {estado}")

    print("\n" + "="*80)
    balance_anual = total_ingresos - total_gastos
    print(f"\n💼 TOTALES ANUALES:")
    print(f"  Total Ingresos: €{total_ingresos:.2f}")
    print(f"  Total Gastos:   €{total_gastos:.2f}")
    print(f"  Balance Anual:  €{balance_anual:+.2f}")
    print()

    conn.close()

if __name__ == "__main__":
    test_comparacion_anual()

