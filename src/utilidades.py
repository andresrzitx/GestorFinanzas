"""
Utilidades para gestionar la base de datos.
"""

from database import Database
import sys


def mostrar_menu():
    """Muestra el menú de opciones."""
    print("\n" + "="*60)
    print("UTILIDADES DE BASE DE DATOS - Gestor de Gastos")
    print("="*60)
    print("1. Ver resumen de datos")
    print("2. Ver todas las categorías")
    print("3. Agregar nueva categoría")
    print("4. Ver gastos de un mes")
    print("5. Limpiar base de datos (CUIDADO)")
    print("6. Exportar datos a texto")
    print("0. Salir")
    print("="*60)


def ver_resumen():
    """Muestra un resumen de los datos en la base de datos."""
    db = Database()

    print("\n" + "-"*60)
    print("RESUMEN DE DATOS")
    print("-"*60)

    # Categorías
    categorias = db.obtener_categorias()
    print(f"Total de categorías: {len(categorias)}")

    # Gastos por año
    anios = [2024, 2025, 2026, 2027]

    for anio in anios:
        total = db.obtener_total_anual(anio)
        if total > 0:
            comparacion = db.obtener_comparacion_anual(anio)
            meses_con_datos = len(comparacion)
            print(f"\nAño {anio}:")
            print(f"  • Total gastado: €{total:.2f}")
            print(f"  • Meses con datos: {meses_con_datos}")
            if meses_con_datos > 0:
                print(f"  • Promedio mensual: €{total/meses_con_datos:.2f}")


def ver_categorias():
    """Muestra todas las categorías."""
    db = Database()
    categorias = db.obtener_categorias()

    print("\n" + "-"*60)
    print("CATEGORÍAS")
    print("-"*60)
    print(f"{'ID':<5} {'Nombre':<20} {'Descripción'}")
    print("-"*60)

    for cat_id, nombre, descripcion in categorias:
        desc_corta = descripcion[:35] + "..." if len(descripcion) > 35 else descripcion
        print(f"{cat_id:<5} {nombre:<20} {desc_corta}")


def agregar_categoria():
    """Agrega una nueva categoría."""
    db = Database()

    print("\n" + "-"*60)
    print("AGREGAR NUEVA CATEGORÍA")
    print("-"*60)

    nombre = input("Nombre de la categoría: ").strip()
    if not nombre:
        print("❌ El nombre es obligatorio")
        return

    descripcion = input("Descripción (opcional): ").strip()

    if db.agregar_categoria(nombre, descripcion):
        print(f"✓ Categoría '{nombre}' agregada correctamente")
    else:
        print(f"❌ No se pudo agregar la categoría (puede que ya exista)")


def ver_gastos_mes():
    """Muestra los gastos de un mes específico."""
    db = Database()

    print("\n" + "-"*60)
    print("VER GASTOS DE UN MES")
    print("-"*60)

    try:
        mes = int(input("Mes (1-12): "))
        anio = int(input("Año: "))

        if mes < 1 or mes > 12:
            print("❌ El mes debe estar entre 1 y 12")
            return

        gastos = db.obtener_gastos_mes(mes, anio)
        total = db.obtener_total_mes(mes, anio)

        meses_nombres = [
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ]

        print(f"\nGastos de {meses_nombres[mes-1]} {anio}")
        print("-"*60)

        if not gastos:
            print("No hay gastos registrados para este mes")
        else:
            print(f"{'Fecha':<12} {'Descripción':<25} {'Categoría':<15} {'Cantidad':>10}")
            print("-"*60)

            for gasto_id, descripcion, cantidad, categoria, fecha in gastos:
                desc_corta = descripcion[:23] + "..." if len(descripcion) > 23 else descripcion
                print(f"{fecha:<12} {desc_corta:<25} {categoria:<15} €{cantidad:>8.2f}")

            print("-"*60)
            print(f"TOTAL: €{total:.2f}")
            print(f"Total de gastos: {len(gastos)}")

    except ValueError:
        print("❌ Formato inválido")


def limpiar_base_datos():
    """Limpia todos los gastos de la base de datos."""
    print("\n" + "-"*60)
    print("⚠️  LIMPIAR BASE DE DATOS")
    print("-"*60)
    print("ADVERTENCIA: Esta acción eliminará TODOS los gastos registrados.")
    print("Las categorías se mantendrán.")

    confirmacion = input("\n¿Estás seguro? Escribe 'CONFIRMAR' para continuar: ")

    if confirmacion != "CONFIRMAR":
        print("❌ Operación cancelada")
        return

    db = Database()
    conn = db.get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM gastos")

    filas_eliminadas = cursor.rowcount
    conn.commit()
    conn.close()

    print(f"✓ Base de datos limpiada. {filas_eliminadas} gastos eliminados.")


def exportar_datos():
    """Exporta los datos a un archivo de texto."""
    db = Database()

    print("\n" + "-"*60)
    print("EXPORTAR DATOS")
    print("-"*60)

    try:
        anio = int(input("Año a exportar: "))

        nombre_archivo = f"gastos_{anio}.txt"

        with open(nombre_archivo, 'w', encoding='utf-8') as f:
            f.write(f"REPORTE DE GASTOS - AÑO {anio}\n")
            f.write("="*80 + "\n\n")

            # Total anual
            total_anual = db.obtener_total_anual(anio)
            f.write(f"TOTAL ANUAL: €{total_anual:.2f}\n")
            f.write("="*80 + "\n\n")

            # Por mes
            meses_nombres = [
                "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
            ]

            for i, mes_nombre in enumerate(meses_nombres, 1):
                gastos = db.obtener_gastos_mes(i, anio)
                total_mes = db.obtener_total_mes(i, anio)

                if gastos:
                    f.write(f"\n{mes_nombre.upper()} {anio}\n")
                    f.write("-"*80 + "\n")

                    for gasto_id, descripcion, cantidad, categoria, fecha in gastos:
                        f.write(f"{fecha}  |  {categoria:<15}  |  {descripcion:<30}  |  €{cantidad:>8.2f}\n")

                    f.write("-"*80 + "\n")
                    f.write(f"Total {mes_nombre}: €{total_mes:.2f}\n")
                    f.write("\n")

            # Estadísticas por categoría
            f.write("\n" + "="*80 + "\n")
            f.write("ESTADÍSTICAS POR CATEGORÍA\n")
            f.write("="*80 + "\n\n")

            conn = db.get_connection()
            cursor = conn.cursor()

            cursor.execute('''
                SELECT c.nombre, SUM(g.cantidad) as total, COUNT(g.id) as cantidad
                FROM categorias c
                LEFT JOIN gastos g ON c.id = g.categoria_id AND g.anio = ?
                GROUP BY c.nombre
                HAVING total > 0
                ORDER BY total DESC
            ''', (anio,))

            resultados = cursor.fetchall()
            conn.close()

            for categoria, total, cantidad in resultados:
                porcentaje = (total / total_anual * 100) if total_anual > 0 else 0
                f.write(f"{categoria:<20}  |  €{total:>10.2f}  |  {cantidad:>3} gastos  |  {porcentaje:>5.1f}%\n")

        print(f"✓ Datos exportados a '{nombre_archivo}'")

    except ValueError:
        print("❌ Formato inválido")
    except Exception as e:
        print(f"❌ Error al exportar: {e}")


def main():
    """Función principal."""
    while True:
        mostrar_menu()

        try:
            opcion = input("\nSelecciona una opción: ").strip()

            if opcion == "0":
                print("\n¡Hasta pronto! 👋")
                break
            elif opcion == "1":
                ver_resumen()
            elif opcion == "2":
                ver_categorias()
            elif opcion == "3":
                agregar_categoria()
            elif opcion == "4":
                ver_gastos_mes()
            elif opcion == "5":
                limpiar_base_datos()
            elif opcion == "6":
                exportar_datos()
            else:
                print("❌ Opción no válida")

            input("\nPresiona Enter para continuar...")

        except KeyboardInterrupt:
            print("\n\n¡Hasta pronto! 👋")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            input("\nPresiona Enter para continuar...")


if __name__ == "__main__":
    main()

