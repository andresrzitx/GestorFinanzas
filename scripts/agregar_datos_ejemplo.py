"""
Script para agregar datos de ejemplo a la base de datos.
Ejecuta este archivo para poblar la base de datos con gastos de ejemplo.
"""

from database import Database


def agregar_datos_ejemplo():
    """Agrega datos de ejemplo a la base de datos."""
    db = Database()

    # Obtener categorías
    categorias = db.obtener_categorias()
    print(f"✓ Categorías disponibles: {len(categorias)}")

    # Datos de ejemplo de INGRESOS
    ejemplos_ingresos = [
        # Enero
        ("Salario mensual", 2500.00, "Salario", "2026-01-01"),
        ("Proyecto freelance", 450.00, "Freelance", "2026-01-15"),
        ("Venta artículo usado", 80.00, "Venta", "2026-01-20"),

        # Febrero
        ("Salario mensual", 2500.00, "Salario", "2026-02-01"),
        ("Trabajo extra", 300.00, "Freelance", "2026-02-12"),
        ("Regalo cumpleaños", 100.00, "Regalo", "2026-02-18"),

        # Marzo
        ("Salario mensual", 2500.00, "Salario", "2026-03-01"),
        ("Consultoría", 600.00, "Freelance", "2026-03-10"),
        ("Dividendos inversiones", 120.00, "Inversiones", "2026-03-25"),

        # Abril
        ("Salario mensual", 2500.00, "Salario", "2026-04-01"),
        ("Proyecto web", 750.00, "Freelance", "2026-04-14"),

        # Mayo
        ("Salario mensual", 2500.00, "Salario", "2026-05-01"),
        ("Bonificación", 400.00, "Salario", "2026-05-05"),
        ("Venta online", 150.00, "Venta", "2026-05-22"),

        # Junio
        ("Salario mensual", 2500.00, "Salario", "2026-06-01"),
        ("Curso online impartido", 500.00, "Freelance", "2026-06-15"),
        ("Intereses cuenta", 25.00, "Inversiones", "2026-06-30"),
    ]

    # Datos de ejemplo para diferentes meses - GASTOS
    ejemplos_gastos = [
        # Enero
        ("Compra en supermercado", 85.50, "Alimentación", "2026-01-05"),
        ("Gasolina", 45.00, "Transporte", "2026-01-07"),
        ("Factura de luz", 65.30, "Servicios", "2026-01-10"),
        ("Cine con amigos", 25.00, "Entretenimiento", "2026-01-12"),
        ("Compra en mercado", 52.80, "Alimentación", "2026-01-15"),
        ("Metro mensual", 35.00, "Transporte", "2026-01-18"),
        ("Internet", 40.00, "Servicios", "2026-01-20"),
        ("Restaurante", 68.50, "Alimentación", "2026-01-22"),
        ("Farmacia", 28.90, "Salud", "2026-01-25"),

        # Febrero
        ("Supermercado", 92.30, "Alimentación", "2026-02-03"),
        ("Gasolina", 48.00, "Transporte", "2026-02-06"),
        ("Agua", 25.50, "Servicios", "2026-02-08"),
        ("Libros", 45.90, "Educación", "2026-02-10"),
        ("Compra semanal", 78.20, "Alimentación", "2026-02-14"),
        ("Mantenimiento coche", 120.00, "Transporte", "2026-02-17"),
        ("Spotify + Netflix", 25.98, "Entretenimiento", "2026-02-20"),
        ("Dentista", 85.00, "Salud", "2026-02-23"),
        ("Muebles IKEA", 150.00, "Hogar", "2026-02-25"),

        # Marzo
        ("Mercadona", 88.75, "Alimentación", "2026-03-02"),
        ("Gasolina", 50.00, "Transporte", "2026-03-05"),
        ("Luz", 72.40, "Servicios", "2026-03-08"),
        ("Concierto", 55.00, "Entretenimiento", "2026-03-12"),
        ("Compra diaria", 34.50, "Alimentación", "2026-03-15"),
        ("Seguro médico", 65.00, "Salud", "2026-03-18"),
        ("Curso online", 99.00, "Educación", "2026-03-20"),
        ("Ropa nueva", 125.00, "Otros", "2026-03-23"),
        ("Restaurante familia", 95.80, "Alimentación", "2026-03-27"),

        # Abril
        ("Supermercado grande", 105.60, "Alimentación", "2026-04-04"),
        ("Combustible", 52.00, "Transporte", "2026-04-07"),
        ("Internet y teléfono", 45.50, "Servicios", "2026-04-10"),
        ("Gimnasio mensual", 40.00, "Salud", "2026-04-12"),
        ("Compras varias", 67.30, "Alimentación", "2026-04-16"),
        ("Cine 3D", 18.50, "Entretenimiento", "2026-04-19"),
        ("Material oficina", 32.90, "Otros", "2026-04-22"),
        ("Pizza delivery", 24.00, "Alimentación", "2026-04-25"),

        # Mayo
        ("Compra mensual", 98.40, "Alimentación", "2026-05-03"),
        ("Gasolina viaje", 60.00, "Transporte", "2026-05-06"),
        ("Factura agua", 28.30, "Servicios", "2026-05-09"),
        ("Parque de atracciones", 75.00, "Entretenimiento", "2026-05-11"),
        ("Mercado local", 45.80, "Alimentación", "2026-05-15"),
        ("Revisión médica", 50.00, "Salud", "2026-05-18"),
        ("Decoración casa", 85.00, "Hogar", "2026-05-21"),
        ("Sushi", 42.50, "Alimentación", "2026-05-24"),

        # Junio
        ("Gran compra", 115.90, "Alimentación", "2026-06-02"),
        ("Combustible", 55.00, "Transporte", "2026-06-05"),
        ("Luz verano", 58.20, "Servicios", "2026-06-08"),
        ("Videojuegos", 69.99, "Entretenimiento", "2026-06-12"),
        ("Panadería y frutas", 28.40, "Alimentación", "2026-06-16"),
        ("Taxi aeropuerto", 35.00, "Transporte", "2026-06-19"),
        ("Aire acondicionado", 45.00, "Servicios", "2026-06-22"),
        ("Helados y postres", 18.70, "Alimentación", "2026-06-26"),
    ]

    # Mapear nombres de categorías a IDs
    categorias_map = {cat[1]: cat[0] for cat in categorias}

    gastos_agregados = 0
    ingresos_agregados = 0
    errores = 0

    # Agregar INGRESOS
    print("\nAgregando ingresos de ejemplo...")
    for descripcion, cantidad, fuente, fecha in ejemplos_ingresos:
        if db.agregar_ingreso(descripcion, cantidad, fuente, fecha):
            ingresos_agregados += 1
            print(f"  ✓ {fecha}: {descripcion} - €{cantidad:.2f} ({fuente})")
        else:
            errores += 1
            print(f"  ✗ Error agregando ingreso: {descripcion}")

    # Agregar GASTOS
    print("\nAgregando gastos de ejemplo...")
    for descripcion, cantidad, categoria_nombre, fecha in ejemplos_gastos:
        if categoria_nombre in categorias_map:
            categoria_id = categorias_map[categoria_nombre]
            if db.agregar_gasto(descripcion, cantidad, categoria_id, fecha):
                gastos_agregados += 1
                print(f"  ✓ {fecha}: {descripcion} - €{cantidad:.2f} ({categoria_nombre})")
            else:
                errores += 1
                print(f"  ✗ Error agregando: {descripcion}")
        else:
            print(f"  ! Categoría no encontrada: {categoria_nombre}")
            errores += 1

    print(f"\n{'='*60}")
    print(f"Resumen:")
    print(f"  • Ingresos agregados correctamente: {ingresos_agregados}")
    print(f"  • Gastos agregados correctamente: {gastos_agregados}")
    print(f"  • Errores: {errores}")
    print(f"{'='*60}")

    # Mostrar algunos totales y balances
    print(f"\nBalance por mes (2026):")
    meses_nombres = [
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ]

    total_ingresos_anual = 0
    total_gastos_anual = 0

    for i, mes_nombre in enumerate(meses_nombres[:6], 1):  # Solo primeros 6 meses con datos
        balance = db.obtener_balance_mes(i, 2026)
        if balance['ingresos'] > 0 or balance['gastos'] > 0:
            signo = "+" if balance['balance'] >= 0 else ""
            color_balance = "✓" if balance['balance'] >= 0 else "✗"
            print(f"  {color_balance} {mes_nombre}: Ingresos: €{balance['ingresos']:.2f} | Gastos: €{balance['gastos']:.2f} | Balance: {signo}€{balance['balance']:.2f}")
            total_ingresos_anual += balance['ingresos']
            total_gastos_anual += balance['gastos']

    balance_anual = total_ingresos_anual - total_gastos_anual
    signo = "+" if balance_anual >= 0 else ""

    print(f"\n{'-'*60}")
    print(f"  TOTAL INGRESOS (Ene-Jun): €{total_ingresos_anual:.2f}")
    print(f"  TOTAL GASTOS (Ene-Jun): €{total_gastos_anual:.2f}")
    print(f"  BALANCE ANUAL: {signo}€{balance_anual:.2f}")
    print(f"  Promedio mensual ingresos: €{total_ingresos_anual/6:.2f}")
    print(f"  Promedio mensual gastos: €{total_gastos_anual/6:.2f}")

    print(f"\n✓ Datos de ejemplo agregados exitosamente!")
    print(f"  Ahora puedes ejecutar 'python3 app.py' para ver la aplicación con datos.")
    print(f"  La aplicación ahora incluye gestión de INGRESOS y GASTOS con balance mensual.")



if __name__ == "__main__":
    agregar_datos_ejemplo()

