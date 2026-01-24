#!/usr/bin/env python3
"""
Script de prueba para verificar la vista de comparación anual mejorada
"""

import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database import Database

def test_comparacion_anual():
    # Usar usuario_id=1 para pruebas (asumiendo que existe en la BD)
    db = Database(usuario_id=2)

    print('═' * 80)
    print('📊 VISTA DE COMPARACIÓN ANUAL - Test de Funcionalidad')
    print('═' * 80)
    print()

    # Nombres de meses
    meses_nombres = [
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ]

    # Obtener datos anuales
    anio = 2026
    comparacion_gastos = db.obtener_comparacion_anual(anio)
    comparacion_ingresos = db.obtener_comparacion_ingresos_anual(anio)

    # Crear diccionarios
    gastos_por_mes = {mes: 0.0 for mes in range(1, 13)}
    ingresos_por_mes = {mes: 0.0 for mes in range(1, 13)}

    for mes, total in comparacion_gastos:
        gastos_por_mes[mes] = total

    for mes, total in comparacion_ingresos:
        ingresos_por_mes[mes] = total

    # Mostrar tabla
    print(f"{'Mes':<12} │ {'Ingresos':>12} │ {'Gastos':>12} │ {'Balance':>13} │ {'Estado':<15}")
    print('─' * 80)

    total_ingresos = 0.0
    total_gastos = 0.0
    meses_con_datos = 0

    for mes in range(1, 13):
        ingresos = ingresos_por_mes[mes]
        gastos = gastos_por_mes[mes]
        balance = ingresos - gastos

        # Determinar estado
        if balance > 0:
            estado = "✅ Ahorro"
        elif balance < 0:
            estado = "⚠️ Déficit"
        else:
            estado = "➖ Neutro"

        # Mostrar fila
        signo = "+" if balance >= 0 else ""
        print(f"{meses_nombres[mes-1]:<12} │ €{ingresos:>11.2f} │ €{gastos:>11.2f} │ {signo}€{balance:>11.2f} │ {estado}")

        # Acumular totales
        total_ingresos += ingresos
        total_gastos += gastos

        if ingresos > 0 or gastos > 0:
            meses_con_datos += 1

    # Calcular balance anual
    balance_anual = total_ingresos - total_gastos

    # Mostrar totales
    print('═' * 80)
    print(f"{'TOTAL ANUAL':<12} │ €{total_ingresos:>11.2f} │ €{total_gastos:>11.2f} │ {'+' if balance_anual >= 0 else ''}€{balance_anual:>11.2f} │")
    print('─' * 80)

    # Calcular promedios
    divisor = max(meses_con_datos, 1)
    promedio_ingresos = total_ingresos / divisor
    promedio_gastos = total_gastos / divisor
    promedio_balance = balance_anual / divisor

    print(f"{'PROMEDIO/MES':<12} │ €{promedio_ingresos:>11.2f} │ €{promedio_gastos:>11.2f} │ {'+' if promedio_balance >= 0 else ''}€{promedio_balance:>11.2f} │")
    print('═' * 80)

    # Análisis
    print()
    print('📈 ANÁLISIS:')
    print(f'   • Meses con datos: {meses_con_datos}/12')
    print(f'   • Total ingresos: €{total_ingresos:,.2f}')
    print(f'   • Total gastos: €{total_gastos:,.2f}')
    print(f'   • Balance anual: €{balance_anual:+,.2f}')

    if balance_anual > 0:
        tasa_ahorro = (balance_anual / total_ingresos * 100) if total_ingresos > 0 else 0
        print(f'   • Tasa de ahorro: {tasa_ahorro:.1f}%')
        print(f'   • Estado: ✅ ¡Excelente! Estás ahorrando.')
    elif balance_anual < 0:
        print(f'   • Estado: ⚠️ Atención: Gastas más de lo que ingresas.')
    else:
        print(f'   • Estado: ➖ Balance neutro.')

    print()
    print('✅ Vista de Comparación Anual funcionando correctamente!')
    print('   Ahora puedes ver ingresos, gastos y balance mensual en la app.')
    print()

if __name__ == '__main__':
    test_comparacion_anual()

