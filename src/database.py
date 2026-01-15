"""
Módulo de gestión de base de datos para la aplicación de gastos mensuales.
"""

import sqlite3
import hashlib
import os
from datetime import datetime
from typing import List, Tuple, Dict, Optional


# Obtener el directorio raíz del proyecto
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, "data")


class Database:
    """Clase para manejar todas las operaciones de base de datos."""

    # Base de datos principal solo para usuarios
    USUARIOS_DB = os.path.join(DATA_DIR, "usuarios.db")

    # Directorio para las bases de datos de usuarios
    USUARIOS_DATA_DIR = os.path.join(DATA_DIR, "usuarios")

    def __init__(self, usuario_id: int = None):
        """
        Inicializa la conexión a la base de datos.

        Args:
            usuario_id: ID del usuario autenticado
        """
        self.usuario_id = usuario_id

        # Crear directorios si no existen
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)
        if not os.path.exists(self.USUARIOS_DATA_DIR):
            os.makedirs(self.USUARIOS_DATA_DIR)

        # Base de datos del usuario (si hay usuario autenticado)
        if usuario_id:
            self.db_name = os.path.join(self.USUARIOS_DATA_DIR, f"usuario_{usuario_id}_finanzas.db")
        else:
            self.db_name = None

        # Siempre crear tablas de usuarios en la DB principal
        self.create_usuarios_table()

        # Si hay usuario, crear sus tablas de finanzas
        if usuario_id:
            self.create_finanzas_tables()
            self.migrar_metodo_pago()  # Migrar columna si no existe

    def get_usuarios_connection(self):
        """Obtiene una conexión a la base de datos de usuarios."""
        return sqlite3.connect(self.USUARIOS_DB, timeout=10)

    def get_connection(self):
        """Obtiene una conexión a la base de datos de finanzas del usuario."""
        if not self.db_name:
            raise Exception("No hay usuario autenticado")
        return sqlite3.connect(self.db_name, timeout=10)

    def create_usuarios_table(self):
        """Crea la tabla de usuarios en la base de datos principal."""
        conn = self.get_usuarios_connection()
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                rol TEXT DEFAULT 'usuario',
                activo INTEGER DEFAULT 1,
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ultimo_acceso TIMESTAMP
            )
        ''')

        # Migrar columnas si no existen
        cursor.execute("PRAGMA table_info(usuarios)")
        columnas = [col[1] for col in cursor.fetchall()]

        if 'rol' not in columnas:
            cursor.execute("ALTER TABLE usuarios ADD COLUMN rol TEXT DEFAULT 'usuario'")
        if 'activo' not in columnas:
            cursor.execute("ALTER TABLE usuarios ADD COLUMN activo INTEGER DEFAULT 1")
        if 'ultimo_acceso' not in columnas:
            cursor.execute("ALTER TABLE usuarios ADD COLUMN ultimo_acceso TIMESTAMP")

        conn.commit()
        conn.close()

    def create_finanzas_tables(self):
        """Crea las tablas de finanzas en la base de datos del usuario."""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Tabla de categorías (sin usuario_id, ya que es base de datos propia)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categorias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT UNIQUE NOT NULL,
                descripcion TEXT
            )
        ''')

        # Tabla de gastos (sin usuario_id)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS gastos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                descripcion TEXT NOT NULL,
                cantidad REAL NOT NULL,
                categoria_id INTEGER NOT NULL,
                fecha DATE NOT NULL,
                mes INTEGER NOT NULL,
                anio INTEGER NOT NULL,
                metodo_pago TEXT DEFAULT 'tarjeta',
                FOREIGN KEY (categoria_id) REFERENCES categorias(id)
            )
        ''')

        # Tabla de ingresos (sin usuario_id)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ingresos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                descripcion TEXT NOT NULL,
                cantidad REAL NOT NULL,
                fuente TEXT NOT NULL,
                fecha DATE NOT NULL,
                mes INTEGER NOT NULL,
                anio INTEGER NOT NULL
            )
        ''')

        conn.commit()

        # Insertar categorías por defecto si no existen
        categorias_default = [
            ("Alimentación", "Gastos en comida y bebidas"),
            ("Transporte", "Gastos de transporte y combustible"),
            ("Servicios", "Facturas de luz, agua, internet, etc."),
            ("Entretenimiento", "Ocio, salidas, hobbies"),
            ("Salud", "Médicos, medicamentos, seguros"),
            ("Educación", "Cursos, libros, materiales"),
            ("Hogar", "Alquiler, mantenimiento, muebles"),
            ("Otros", "Gastos varios")
        ]

        for nombre, descripcion in categorias_default:
            try:
                cursor.execute(
                    "INSERT INTO categorias (nombre, descripcion) VALUES (?, ?)",
                    (nombre, descripcion)
                )
            except sqlite3.IntegrityError:
                # La categoría ya existe
                pass

        conn.commit()
        conn.close()

    def migrar_metodo_pago(self):
        """Agrega la columna metodo_pago a la tabla gastos si no existe."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            # Verificar si la columna ya existe
            cursor.execute("PRAGMA table_info(gastos)")
            columnas = [col[1] for col in cursor.fetchall()]

            if 'metodo_pago' not in columnas:
                cursor.execute("ALTER TABLE gastos ADD COLUMN metodo_pago TEXT DEFAULT 'tarjeta'")
                conn.commit()
                print("✅ Columna metodo_pago agregada exitosamente")

            conn.close()
        except Exception as e:
            print(f"Error al migrar metodo_pago: {e}")

    def agregar_gasto(self, descripcion: str, cantidad: float, categoria_id: int,
                      fecha: str = None, metodo_pago: str = 'tarjeta') -> bool:
        """
        Agrega un nuevo gasto a la base de datos.

        Args:
            descripcion: Descripción del gasto
            cantidad: Cantidad gastada
            categoria_id: ID de la categoría
            fecha: Fecha del gasto (formato YYYY-MM-DD). Si es None, usa la fecha actual
            metodo_pago: Método de pago (efectivo, tarjeta, etc.). Por defecto 'efectivo'

        Returns:
            True si se agregó correctamente, False en caso contrario
        """
        try:
            if fecha is None:
                fecha = datetime.now().strftime("%Y-%m-%d")

            fecha_obj = datetime.strptime(fecha, "%Y-%m-%d")
            mes = fecha_obj.month
            anio = fecha_obj.year

            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO gastos (descripcion, cantidad, categoria_id, fecha, mes, anio, metodo_pago)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (descripcion, cantidad, categoria_id, fecha, mes, anio, metodo_pago))

            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error al agregar gasto: {e}")
            return False

    def obtener_gastos_mes(self, mes: int, anio: int) -> List[Tuple]:
        """
        Obtiene todos los gastos de un mes específico.

        Args:
            mes: Número del mes (1-12)
            anio: Año

        Returns:
            Lista de tuplas con los datos de los gastos
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT g.id, g.descripcion, g.cantidad, c.nombre, g.fecha, g.metodo_pago
            FROM gastos g
            JOIN categorias c ON g.categoria_id = c.id
            WHERE g.mes = ? AND g.anio = ?
            ORDER BY g.fecha DESC
        ''', (mes, anio))

        gastos = cursor.fetchall()
        conn.close()
        return gastos

    def obtener_total_mes(self, mes: int, anio: int) -> float:
        """
        Obtiene el total de gastos de un mes.

        Args:
            mes: Número del mes (1-12)
            anio: Año

        Returns:
            Total de gastos del mes
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT SUM(cantidad)
            FROM gastos
            WHERE mes = ? AND anio = ?
        ''', (mes, anio))

        resultado = cursor.fetchone()[0]
        conn.close()
        return resultado if resultado else 0.0

    def obtener_gastos_por_categoria_mes(self, mes: int, anio: int) -> List[Tuple]:
        """
        Obtiene el total de gastos agrupados por categoría para un mes específico.

        Args:
            mes: Número del mes (1-12)
            anio: Año

        Returns:
            Lista de tuplas (categoria, total)
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT c.nombre, SUM(g.cantidad) as total
            FROM gastos g
            JOIN categorias c ON g.categoria_id = c.id
            WHERE g.mes = ? AND g.anio = ?
            GROUP BY c.nombre
            ORDER BY total DESC
        ''', (mes, anio))

        resultados = cursor.fetchall()
        conn.close()
        return resultados

    def obtener_comparacion_anual(self, anio: int) -> List[Tuple]:
        """
        Obtiene el total de gastos por mes para un año completo.

        Args:
            anio: Año a consultar

        Returns:
            Lista de tuplas (mes, total)
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT mes, SUM(cantidad) as total
            FROM gastos
            WHERE anio = ?
            GROUP BY mes
            ORDER BY mes
        ''', (anio,))

        resultados = cursor.fetchall()
        conn.close()
        return resultados

    def obtener_total_anual(self, anio: int) -> float:
        """
        Obtiene el total de gastos de un año completo.

        Args:
            anio: Año a consultar

        Returns:
            Total de gastos del año
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT SUM(cantidad)
            FROM gastos
            WHERE anio = ?
        ''', (anio,))

        resultado = cursor.fetchone()[0]
        conn.close()
        return resultado if resultado else 0.0

    def obtener_categorias(self) -> List[Tuple]:
        """
        Obtiene todas las categorías disponibles.

        Returns:
            Lista de tuplas (id, nombre, descripcion)
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT id, nombre, descripcion FROM categorias 
            ORDER BY nombre
        ''')

        categorias = cursor.fetchall()
        conn.close()
        return categorias

    def eliminar_gasto(self, gasto_id: int) -> bool:
        """
        Elimina un gasto de la base de datos.

        Args:
            gasto_id: ID del gasto a eliminar

        Returns:
            True si se eliminó correctamente, False en caso contrario
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute('DELETE FROM gastos WHERE id = ?', (gasto_id,))

            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error al eliminar gasto: {e}")
            return False

    def actualizar_gasto(self, gasto_id: int, descripcion: str, cantidad: float,
                        categoria_id: int, fecha: str, metodo_pago: str = 'tarjeta') -> bool:
        """
        Actualiza un gasto existente en la base de datos.

        Args:
            gasto_id: ID del gasto a actualizar
            descripcion: Nueva descripción del gasto
            cantidad: Nueva cantidad gastada
            categoria_id: ID de la nueva categoría
            fecha: Nueva fecha del gasto (formato YYYY-MM-DD)
            metodo_pago: Método de pago (efectivo, tarjeta, etc.)

        Returns:
            True si se actualizó correctamente, False en caso contrario
        """
        try:
            fecha_obj = datetime.strptime(fecha, "%Y-%m-%d")
            mes = fecha_obj.month
            anio = fecha_obj.year

            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute('''
                UPDATE gastos 
                SET descripcion = ?, cantidad = ?, categoria_id = ?, 
                    fecha = ?, mes = ?, anio = ?, metodo_pago = ?
                WHERE id = ?
            ''', (descripcion, cantidad, categoria_id, fecha, mes, anio, metodo_pago, gasto_id))

            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error al actualizar gasto: {e}")
            return False

    def obtener_gasto_por_id(self, gasto_id: int) -> Optional[Tuple]:
        """
        Obtiene los detalles de un gasto específico.

        Args:
            gasto_id: ID del gasto

        Returns:
            Tupla (id, descripcion, cantidad, categoria_id, fecha, mes, anio, metodo_pago) o None
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute('''
                SELECT id, descripcion, cantidad, categoria_id, fecha, mes, anio, metodo_pago
                FROM gastos
                WHERE id = ?
            ''', (gasto_id,))

            resultado = cursor.fetchone()
            conn.close()
            return resultado
        except Exception as e:
            print(f"Error al obtener gasto: {e}")
            return None

    def agregar_categoria(self, nombre: str, descripcion: str = "") -> bool:
        """
        Agrega una nueva categoría.

        Args:
            nombre: Nombre de la categoría
            descripcion: Descripción de la categoría

        Returns:
            True si se agregó correctamente, False en caso contrario
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute(
                'INSERT INTO categorias (nombre, descripcion) VALUES (?, ?)',
                (nombre, descripcion)
            )

            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            print("La categoría ya existe")
            return False

    def editar_categoria(self, categoria_id: int, nombre: str, descripcion: str = "") -> bool:
        """
        Edita una categoría existente.

        Args:
            categoria_id: ID de la categoría a editar
            nombre: Nuevo nombre de la categoría
            descripcion: Nueva descripción de la categoría

        Returns:
            True si se editó correctamente, False en caso contrario
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute(
                'UPDATE categorias SET nombre = ?, descripcion = ? WHERE id = ?',
                (nombre, descripcion, categoria_id)
            )

            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            print("El nombre de la categoría ya existe")
            return False
        except Exception as e:
            print(f"Error al editar categoría: {e}")
            try:
                if 'conn' in locals():
                    conn.close()
            except:
                pass
            return False

    def eliminar_categoria(self, categoria_id: int) -> bool:
        """
        Elimina una categoría de la base de datos.
        Solo se puede eliminar si no hay gastos asociados a ella.

        Args:
            categoria_id: ID de la categoría a eliminar

        Returns:
            True si se eliminó correctamente, False en caso contrario
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            # Verificar si hay gastos asociados
            cursor.execute('SELECT COUNT(*) FROM gastos WHERE categoria_id = ?', (categoria_id,))
            count = cursor.fetchone()[0]

            if count > 0:
                print(f"No se puede eliminar la categoría porque tiene {count} gasto(s) asociado(s)")
                conn.close()
                return False

            # Eliminar la categoría
            cursor.execute('DELETE FROM categorias WHERE id = ?', (categoria_id,))

            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error al eliminar categoría: {e}")
            return False

    def obtener_gastos_por_metodo_mes(self, mes: int, anio: int) -> Dict[str, float]:
        """
        Obtiene el total de gastos por método de pago para un mes específico.

        Args:
            mes: Número del mes (1-12)
            anio: Año

        Returns:
            Diccionario con totales por método {'efectivo': 0.0, 'tarjeta': 0.0}
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT metodo_pago, SUM(cantidad) as total
            FROM gastos
            WHERE mes = ? AND anio = ?
            GROUP BY metodo_pago
        ''', (mes, anio))

        resultados = cursor.fetchall()
        conn.close()

        # Crear diccionario con valores por defecto
        totales = {'efectivo': 0.0, 'tarjeta': 0.0}
        for metodo, total in resultados:
            if metodo in totales:
                totales[metodo] = total

        return totales

    def obtener_gastos_por_metodo_anual(self, anio: int) -> Dict[str, float]:
        """
        Obtiene el total de gastos por método de pago para un año completo.

        Args:
            anio: Año a consultar

        Returns:
            Diccionario con totales por método {'efectivo': 0.0, 'tarjeta': 0.0}
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT metodo_pago, SUM(cantidad) as total
            FROM gastos
            WHERE anio = ?
            GROUP BY metodo_pago
        ''', (anio,))

        resultados = cursor.fetchall()
        conn.close()

        # Crear diccionario con valores por defecto
        totales = {'efectivo': 0.0, 'tarjeta': 0.0}
        for metodo, total in resultados:
            if metodo in totales:
                totales[metodo] = total

        return totales

    def obtener_gastos_por_categoria_y_metodo(self, mes: int = None, anio: int = None) -> List[Tuple]:
        """
        Obtiene gastos agrupados por categoría y método de pago.

        Args:
            mes: Número del mes (1-12). Si es None, obtiene todo el año
            anio: Año a consultar

        Returns:
            Lista de tuplas (categoria, metodo_pago, total)
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        if mes is not None:
            cursor.execute('''
                SELECT c.nombre, g.metodo_pago, SUM(g.cantidad) as total
                FROM gastos g
                JOIN categorias c ON g.categoria_id = c.id
                WHERE g.mes = ? AND g.anio = ?
                GROUP BY c.nombre, g.metodo_pago
                ORDER BY c.nombre, g.metodo_pago
            ''', (mes, anio))
        else:
            cursor.execute('''
                SELECT c.nombre, g.metodo_pago, SUM(g.cantidad) as total
                FROM gastos g
                JOIN categorias c ON g.categoria_id = c.id
                WHERE g.anio = ?
                GROUP BY c.nombre, g.metodo_pago
                ORDER BY c.nombre, g.metodo_pago
            ''', (anio,))

        resultados = cursor.fetchall()
        conn.close()
        return resultados

    # ==================== MÉTODOS PARA INGRESOS ====================

    def agregar_ingreso(self, descripcion: str, cantidad: float, fuente: str,
                        fecha: str = None) -> bool:
        """
        Agrega un nuevo ingreso a la base de datos.

        Args:
            descripcion: Descripción del ingreso
            cantidad: Cantidad recibida
            fuente: Fuente del ingreso (salario, freelance, inversiones, etc.)
            fecha: Fecha del ingreso (formato YYYY-MM-DD). Si es None, usa la fecha actual

        Returns:
            True si se agregó correctamente, False en caso contrario
        """
        try:
            if fecha is None:
                fecha = datetime.now().strftime("%Y-%m-%d")

            fecha_obj = datetime.strptime(fecha, "%Y-%m-%d")
            mes = fecha_obj.month
            anio = fecha_obj.year

            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO ingresos (descripcion, cantidad, fuente, fecha, mes, anio)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (descripcion, cantidad, fuente, fecha, mes, anio))

            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error al agregar ingreso: {e}")
            return False

    def obtener_ingresos_mes(self, mes: int, anio: int) -> List[Tuple]:
        """
        Obtiene todos los ingresos de un mes específico.

        Args:
            mes: Número del mes (1-12)
            anio: Año

        Returns:
            Lista de tuplas con los datos de los ingresos
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT id, descripcion, cantidad, fuente, fecha
            FROM ingresos
            WHERE mes = ? AND anio = ?
            ORDER BY fecha DESC
        ''', (mes, anio))

        ingresos = cursor.fetchall()
        conn.close()
        return ingresos

    def obtener_total_ingresos_mes(self, mes: int, anio: int) -> float:
        """
        Obtiene el total de ingresos de un mes.

        Args:
            mes: Número del mes (1-12)
            anio: Año

        Returns:
            Total de ingresos del mes
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT SUM(cantidad)
            FROM ingresos
            WHERE mes = ? AND anio = ?
        ''', (mes, anio))

        resultado = cursor.fetchone()[0]
        conn.close()
        return resultado if resultado else 0.0

    def obtener_total_ingresos_anual(self, anio: int) -> float:
        """
        Obtiene el total de ingresos de un año completo.

        Args:
            anio: Año a consultar

        Returns:
            Total de ingresos del año
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT SUM(cantidad)
            FROM ingresos
            WHERE anio = ?
        ''', (anio,))

        resultado = cursor.fetchone()[0]
        conn.close()
        return resultado if resultado else 0.0

    def obtener_ingresos_por_fuente_mes(self, mes: int, anio: int) -> List[Tuple]:
        """
        Obtiene el total de ingresos agrupados por fuente para un mes específico.

        Args:
            mes: Número del mes (1-12)
            anio: Año

        Returns:
            Lista de tuplas (fuente, total)
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT fuente, SUM(cantidad) as total
            FROM ingresos
            WHERE mes = ? AND anio = ?
            GROUP BY fuente
            ORDER BY total DESC
        ''', (mes, anio))

        resultados = cursor.fetchall()
        conn.close()
        return resultados

    def obtener_comparacion_ingresos_anual(self, anio: int) -> List[Tuple]:
        """
        Obtiene el total de ingresos por mes para un año completo.

        Args:
            anio: Año a consultar

        Returns:
            Lista de tuplas (mes, total)
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT mes, SUM(cantidad) as total
            FROM ingresos
            WHERE anio = ?
            GROUP BY mes
            ORDER BY mes
        ''', (anio,))

        resultados = cursor.fetchall()
        conn.close()
        return resultados

    def eliminar_ingreso(self, ingreso_id: int) -> bool:
        """
        Elimina un ingreso de la base de datos.

        Args:
            ingreso_id: ID del ingreso a eliminar

        Returns:
            True si se eliminó correctamente, False en caso contrario
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute('DELETE FROM ingresos WHERE id = ?', (ingreso_id,))

            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error al eliminar ingreso: {e}")
            return False

    def actualizar_ingreso(self, ingreso_id: int, descripcion: str, cantidad: float,
                          fuente: str, fecha: str) -> bool:
        """
        Actualiza un ingreso existente en la base de datos.

        Args:
            ingreso_id: ID del ingreso a actualizar
            descripcion: Nueva descripción del ingreso
            cantidad: Nueva cantidad
            fuente: Nueva fuente del ingreso
            fecha: Nueva fecha del ingreso (formato YYYY-MM-DD)

        Returns:
            True si se actualizó correctamente, False en caso contrario
        """
        try:
            fecha_obj = datetime.strptime(fecha, "%Y-%m-%d")
            mes = fecha_obj.month
            anio = fecha_obj.year

            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute('''
                UPDATE ingresos 
                SET descripcion = ?, cantidad = ?, fuente = ?, 
                    fecha = ?, mes = ?, anio = ?
                WHERE id = ?
            ''', (descripcion, cantidad, fuente, fecha, mes, anio, ingreso_id))

            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error al actualizar ingreso: {e}")
            return False

    def obtener_ingreso_por_id(self, ingreso_id: int) -> Optional[Tuple]:
        """
        Obtiene los detalles de un ingreso específico.

        Args:
            ingreso_id: ID del ingreso

        Returns:
            Tupla (id, descripcion, cantidad, fuente, fecha, mes, anio) o None
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute('''
                SELECT id, descripcion, cantidad, fuente, fecha, mes, anio
                FROM ingresos
                WHERE id = ?
            ''', (ingreso_id,))

            resultado = cursor.fetchone()
            conn.close()
            return resultado
        except Exception as e:
            print(f"Error al obtener ingreso: {e}")
            return None

    def obtener_balance_mes(self, mes: int, anio: int) -> Dict[str, float]:
        """
        Obtiene el balance (ingresos - gastos) de un mes.

        Args:
            mes: Número del mes (1-12)
            anio: Año

        Returns:
            Diccionario con ingresos, gastos y balance
        """
        ingresos = self.obtener_total_ingresos_mes(mes, anio)
        gastos = self.obtener_total_mes(mes, anio)
        balance = ingresos - gastos

        return {
            'ingresos': ingresos,
            'gastos': gastos,
            'balance': balance
        }

    def obtener_balance_anual(self, anio: int) -> Dict[str, float]:
        """
        Obtiene el balance (ingresos - gastos) de un año completo.

        Args:
            anio: Año a consultar

        Returns:
            Diccionario con ingresos, gastos y balance
        """
        ingresos = self.obtener_total_ingresos_anual(anio)
        gastos = self.obtener_total_anual(anio)
        balance = ingresos - gastos

        return {
            'ingresos': ingresos,
            'gastos': gastos,
            'balance': balance
        }

    def obtener_gastos_detallados_categoria(self, categoria_nombre: str, mes: int = None,
                                            anio: int = None) -> List[Tuple]:
        """
        Obtiene todos los gastos detallados de una categoría específica.

        Args:
            categoria_nombre: Nombre de la categoría
            mes: Número del mes (1-12). Si es None, obtiene todos los meses
            anio: Año a consultar. Requerido si mes es None

        Returns:
            Lista de tuplas (id, descripcion, cantidad, fecha, mes, metodo_pago)
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        if mes is not None and anio is not None:
            # Gastos de un mes específico
            cursor.execute('''
                SELECT g.id, g.descripcion, g.cantidad, g.fecha, g.mes, g.metodo_pago
                FROM gastos g
                JOIN categorias c ON g.categoria_id = c.id
                WHERE c.nombre = ? AND g.mes = ? AND g.anio = ?
                ORDER BY g.fecha DESC
            ''', (categoria_nombre, mes, anio))
        elif anio is not None:
            # Gastos de todo el año
            cursor.execute('''
                SELECT g.id, g.descripcion, g.cantidad, g.fecha, g.mes, g.metodo_pago
                FROM gastos g
                JOIN categorias c ON g.categoria_id = c.id
                WHERE c.nombre = ? AND g.anio = ?
                ORDER BY g.fecha DESC
            ''', (categoria_nombre, anio))
        else:
            # Todos los gastos de la categoría
            cursor.execute('''
                SELECT g.id, g.descripcion, g.cantidad, g.fecha, g.mes, g.metodo_pago
                FROM gastos g
                JOIN categorias c ON g.categoria_id = c.id
                WHERE c.nombre = ?
                ORDER BY g.fecha DESC
            ''', (categoria_nombre,))

        gastos = cursor.fetchall()
        conn.close()
        return gastos

    # ==================== MÉTODOS PARA USUARIOS Y AUTENTICACIÓN ====================

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hashea una contraseña usando SHA-256.

        Args:
            password: Contraseña en texto plano

        Returns:
            Hash de la contraseña
        """
        return hashlib.sha256(password.encode()).hexdigest()

    def registrar_usuario(self, nombre: str, email: str, password: str) -> Tuple[bool, str]:
        """
        Registra un nuevo usuario en el sistema.

        Args:
            nombre: Nombre del usuario
            email: Email del usuario (único)
            password: Contraseña en texto plano

        Returns:
            Tupla (éxito, mensaje)
        """
        try:
            conn = self.get_usuarios_connection()
            cursor = conn.cursor()

            # Verificar si el email ya existe
            cursor.execute('SELECT id FROM usuarios WHERE email = ?', (email,))
            if cursor.fetchone():
                conn.close()
                return False, "El email ya está registrado"

            # Hashear la contraseña
            password_hash = self.hash_password(password)

            # Insertar usuario
            cursor.execute('''
                INSERT INTO usuarios (nombre, email, password_hash)
                VALUES (?, ?, ?)
            ''', (nombre, email, password_hash))

            usuario_id = cursor.lastrowid
            conn.commit()
            conn.close()

            # Crear base de datos personal del usuario con sus tablas
            db_usuario = Database(usuario_id=usuario_id)

            return True, "Usuario registrado exitosamente"

        except Exception as e:
            print(f"Error al registrar usuario: {e}")
            return False, f"Error al registrar: {str(e)}"

    def autenticar_usuario(self, email: str, password: str) -> Optional[Tuple[int, str, str]]:
        """
        Autentica un usuario.

        Args:
            email: Email del usuario
            password: Contraseña en texto plano

        Returns:
            Tupla (id, nombre, rol) si autenticación exitosa, None si falla o usuario inactivo
        """
        try:
            conn = self.get_usuarios_connection()
            cursor = conn.cursor()

            password_hash = self.hash_password(password)

            cursor.execute('''
                SELECT id, nombre, rol, activo FROM usuarios
                WHERE email = ? AND password_hash = ?
            ''', (email, password_hash))

            resultado = cursor.fetchone()

            if resultado:
                user_id, nombre, rol, activo = resultado

                # Verificar si la cuenta está activa
                if not activo:
                    conn.close()
                    print(f"Intento de login con cuenta inactiva: {email}")
                    return None

                # Actualizar último acceso
                cursor.execute('''
                    UPDATE usuarios
                    SET ultimo_acceso = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (user_id,))
                conn.commit()
                conn.close()

                # Retornar (id, nombre, rol)
                return (user_id, nombre, rol)

            conn.close()
            return None

        except Exception as e:
            print(f"Error al autenticar usuario: {e}")
            import traceback
            traceback.print_exc()
            return None

    def obtener_usuario(self, usuario_id: int) -> Optional[Tuple]:
        """
        Obtiene información de un usuario.

        Args:
            usuario_id: ID del usuario

        Returns:
            Tupla (id, nombre, email, fecha_registro) o None
        """
        conn = self.get_usuarios_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT id, nombre, email, fecha_registro
            FROM usuarios
            WHERE id = ?
        ''', (usuario_id,))

        usuario = cursor.fetchone()
        conn.close()
        return usuario

    def cambiar_password(self, usuario_id: int, password_actual: str, password_nueva: str) -> Tuple[bool, str]:
        """
        Cambia la contraseña de un usuario.

        Args:
            usuario_id: ID del usuario
            password_actual: Contraseña actual
            password_nueva: Nueva contraseña

        Returns:
            Tupla (éxito, mensaje)
        """
        try:
            conn = self.get_usuarios_connection()
            cursor = conn.cursor()

            # Verificar contraseña actual
            password_hash_actual = self.hash_password(password_actual)
            cursor.execute('''
                SELECT id FROM usuarios
                WHERE id = ? AND password_hash = ?
            ''', (usuario_id, password_hash_actual))

            if not cursor.fetchone():
                conn.close()
                return False, "Contraseña actual incorrecta"

            # Actualizar contraseña
            password_hash_nueva = self.hash_password(password_nueva)
            cursor.execute('''
                UPDATE usuarios
                SET password_hash = ?
                WHERE id = ?
            ''', (password_hash_nueva, usuario_id))

            conn.commit()
            conn.close()
            return True, "Contraseña cambiada exitosamente"

        except Exception as e:
            return False, f"Error al cambiar contraseña: {str(e)}"

    # ==================== MÉTODOS DE ADMINISTRACIÓN ====================

    def obtener_todos_usuarios(self) -> List[Tuple]:
        """
        Obtiene todos los usuarios registrados (solo admin).

        Returns:
            Lista de tuplas (id, nombre, email, rol, activo, fecha_registro, ultimo_acceso)
        """
        conn = self.get_usuarios_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT id, nombre, email, rol, activo, fecha_registro, ultimo_acceso
            FROM usuarios
            ORDER BY fecha_registro DESC
        ''')

        usuarios = cursor.fetchall()
        conn.close()
        return usuarios

    def cambiar_rol_usuario(self, usuario_id: int, nuevo_rol: str) -> Tuple[bool, str]:
        """
        Cambia el rol de un usuario (solo admin).

        Args:
            usuario_id: ID del usuario
            nuevo_rol: Nuevo rol ('usuario' o 'admin')

        Returns:
            Tupla (éxito, mensaje)
        """
        if nuevo_rol not in ['usuario', 'admin']:
            return False, "Rol inválido. Debe ser 'usuario' o 'admin'"

        try:
            conn = self.get_usuarios_connection()
            cursor = conn.cursor()

            cursor.execute('''
                UPDATE usuarios
                SET rol = ?
                WHERE id = ?
            ''', (nuevo_rol, usuario_id))

            conn.commit()
            conn.close()
            return True, f"Rol cambiado a '{nuevo_rol}' exitosamente"

        except Exception as e:
            return False, f"Error al cambiar rol: {str(e)}"

    def activar_desactivar_usuario(self, usuario_id: int, activo: bool) -> Tuple[bool, str]:
        """
        Activa o desactiva un usuario (solo admin).

        Args:
            usuario_id: ID del usuario
            activo: True para activar, False para desactivar

        Returns:
            Tupla (éxito, mensaje)
        """
        try:
            conn = self.get_usuarios_connection()
            cursor = conn.cursor()

            cursor.execute('''
                UPDATE usuarios
                SET activo = ?
                WHERE id = ?
            ''', (1 if activo else 0, usuario_id))

            conn.commit()
            conn.close()

            estado = "activado" if activo else "desactivado"
            return True, f"Usuario {estado} exitosamente"

        except Exception as e:
            return False, f"Error al cambiar estado: {str(e)}"

    def eliminar_usuario_admin(self, usuario_id: int) -> Tuple[bool, str]:
        """
        Elimina un usuario y todos sus datos (solo admin).

        Args:
            usuario_id: ID del usuario a eliminar

        Returns:
            Tupla (éxito, mensaje)
        """
        try:
            # Eliminar base de datos de finanzas del usuario
            import os
            db_path = os.path.join(self.USUARIOS_DATA_DIR, f"usuario_{usuario_id}_finanzas.db")
            if os.path.exists(db_path):
                os.remove(db_path)

            # Eliminar usuario de la tabla
            conn = self.get_usuarios_connection()
            cursor = conn.cursor()

            cursor.execute('DELETE FROM usuarios WHERE id = ?', (usuario_id,))

            conn.commit()
            conn.close()
            return True, "Usuario y sus datos eliminados exitosamente"

        except Exception as e:
            return False, f"Error al eliminar usuario: {str(e)}"

    def obtener_estadisticas_admin(self) -> Dict:
        """
        Obtiene estadísticas generales del sistema (solo admin).

        Returns:
            Diccionario con estadísticas
        """
        conn = self.get_usuarios_connection()
        cursor = conn.cursor()

        # Total de usuarios
        cursor.execute('SELECT COUNT(*) FROM usuarios')
        total_usuarios = cursor.fetchone()[0]

        # Usuarios activos
        cursor.execute('SELECT COUNT(*) FROM usuarios WHERE activo = 1')
        usuarios_activos = cursor.fetchone()[0]

        # Usuarios administradores
        cursor.execute("SELECT COUNT(*) FROM usuarios WHERE rol = 'admin'")
        total_admins = cursor.fetchone()[0]

        # Registros recientes (últimos 30 días)
        cursor.execute('''
            SELECT COUNT(*) FROM usuarios 
            WHERE date(fecha_registro) >= date('now', '-30 days')
        ''')
        registros_recientes = cursor.fetchone()[0]

        conn.close()

        return {
            'total_usuarios': total_usuarios,
            'usuarios_activos': usuarios_activos,
            'usuarios_inactivos': total_usuarios - usuarios_activos,
            'total_admins': total_admins,
            'registros_recientes': registros_recientes
        }

    def actualizar_ultimo_acceso(self, usuario_id: int):
        """
        Actualiza la fecha de último acceso del usuario.

        Args:
            usuario_id: ID del usuario
        """
        try:
            conn = self.get_usuarios_connection()
            cursor = conn.cursor()

            cursor.execute('''
                UPDATE usuarios
                SET ultimo_acceso = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (usuario_id,))

            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error al actualizar último acceso: {e}")
