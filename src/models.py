"""
Modelos de datos para FinanzApp.

Este módulo define las clases de modelo que representan las entidades
del sistema usando Programación Orientada a Objetos.
"""

from datetime import datetime
from typing import Optional


class Usuario:
    """
    Modelo que representa un usuario del sistema.

    Attributes:
        id (int): Identificador único del usuario
        nombre (str): Nombre completo del usuario
        email (str): Correo electrónico (único)
        rol (str): Rol del usuario ('usuario' o 'admin')
        activo (bool): Indica si el usuario está activo
        fecha_registro (datetime): Fecha de registro en el sistema
        ultimo_acceso (datetime): Última vez que accedió al sistema
    """

    def __init__(
        self,
        id: int,
        nombre: str,
        email: str,
        rol: str = 'usuario',
        activo: bool = True,
        fecha_registro: Optional[datetime] = None,
        ultimo_acceso: Optional[datetime] = None
    ):
        """
        Inicializa un usuario.

        Args:
            id: Identificador único
            nombre: Nombre del usuario
            email: Correo electrónico
            rol: Rol ('usuario' o 'admin')
            activo: Si está activo
            fecha_registro: Fecha de registro
            ultimo_acceso: Último acceso
        """
        self.id = id
        self.nombre = nombre
        self.email = email
        self.rol = rol
        self.activo = activo
        self.fecha_registro = fecha_registro or datetime.now()
        self.ultimo_acceso = ultimo_acceso

    def es_admin(self) -> bool:
        """
        Verifica si el usuario es administrador.

        Returns:
            bool: True si es admin, False en caso contrario
        """
        return self.rol == 'admin'

    def es_activo(self) -> bool:
        """
        Verifica si el usuario está activo.

        Returns:
            bool: True si está activo, False en caso contrario
        """
        return self.activo

    def actualizar_ultimo_acceso(self):
        """Actualiza la fecha del último acceso."""
        self.ultimo_acceso = datetime.now()

    def to_dict(self) -> dict:
        """
        Convierte el usuario a diccionario.

        Returns:
            dict: Representación del usuario
        """
        return {
            'id': self.id,
            'nombre': self.nombre,
            'email': self.email,
            'rol': self.rol,
            'activo': self.activo,
            'fecha_registro': self.fecha_registro.isoformat() if self.fecha_registro else None,
            'ultimo_acceso': self.ultimo_acceso.isoformat() if self.ultimo_acceso else None
        }

    def __repr__(self) -> str:
        """Representación en string del usuario."""
        return f"Usuario(id={self.id}, nombre='{self.nombre}', email='{self.email}', rol='{self.rol}')"

    def __str__(self) -> str:
        """String legible del usuario."""
        return f"{self.nombre} ({self.email}) - {self.rol}"


class Categoria:
    """
    Modelo que representa una categoría de gastos.

    Attributes:
        id (int): Identificador único de la categoría
        nombre (str): Nombre de la categoría
        descripcion (str): Descripción opcional
    """

    def __init__(self, id: int, nombre: str, descripcion: str = ""):
        """
        Inicializa una categoría.

        Args:
            id: Identificador único
            nombre: Nombre de la categoría
            descripcion: Descripción opcional
        """
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion

    def to_dict(self) -> dict:
        """
        Convierte la categoría a diccionario.

        Returns:
            dict: Representación de la categoría
        """
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion
        }

    def __repr__(self) -> str:
        """Representación en string de la categoría."""
        return f"Categoria(id={self.id}, nombre='{self.nombre}')"

    def __str__(self) -> str:
        """String legible de la categoría."""
        return self.nombre


class Gasto:
    """
    Modelo que representa un gasto.

    Attributes:
        id (int): Identificador único del gasto
        descripcion (str): Descripción del gasto
        cantidad (float): Monto del gasto
        categoria_id (int): ID de la categoría
        fecha (str): Fecha del gasto (YYYY-MM-DD)
        metodo_pago (str): Método de pago ('efectivo' o 'tarjeta')
    """

    METODOS_PAGO_VALIDOS = ['efectivo', 'tarjeta']

    def __init__(
        self,
        id: int,
        descripcion: str,
        cantidad: float,
        categoria_id: int,
        fecha: str,
        metodo_pago: str = 'efectivo'
    ):
        """
        Inicializa un gasto.

        Args:
            id: Identificador único
            descripcion: Descripción del gasto
            cantidad: Monto
            categoria_id: ID de la categoría
            fecha: Fecha en formato YYYY-MM-DD
            metodo_pago: 'efectivo' o 'tarjeta'

        Raises:
            ValueError: Si el método de pago no es válido
        """
        self.id = id
        self.descripcion = descripcion
        self.cantidad = float(cantidad)
        self.categoria_id = categoria_id
        self.fecha = fecha

        if metodo_pago.lower() not in self.METODOS_PAGO_VALIDOS:
            raise ValueError(f"Método de pago debe ser: {', '.join(self.METODOS_PAGO_VALIDOS)}")
        self.metodo_pago = metodo_pago.lower()

    def es_efectivo(self) -> bool:
        """
        Verifica si el pago fue en efectivo.

        Returns:
            bool: True si es efectivo, False si es tarjeta
        """
        return self.metodo_pago == 'efectivo'

    def es_tarjeta(self) -> bool:
        """
        Verifica si el pago fue con tarjeta.

        Returns:
            bool: True si es tarjeta, False si es efectivo
        """
        return self.metodo_pago == 'tarjeta'

    def get_mes(self) -> int:
        """
        Obtiene el mes del gasto.

        Returns:
            int: Número del mes (1-12)
        """
        return int(self.fecha.split('-')[1])

    def get_anio(self) -> int:
        """
        Obtiene el año del gasto.

        Returns:
            int: Año
        """
        return int(self.fecha.split('-')[0])

    def to_dict(self) -> dict:
        """
        Convierte el gasto a diccionario.

        Returns:
            dict: Representación del gasto
        """
        return {
            'id': self.id,
            'descripcion': self.descripcion,
            'cantidad': self.cantidad,
            'categoria_id': self.categoria_id,
            'fecha': self.fecha,
            'metodo_pago': self.metodo_pago
        }

    def __repr__(self) -> str:
        """Representación en string del gasto."""
        return f"Gasto(id={self.id}, descripcion='{self.descripcion}', cantidad={self.cantidad}, fecha='{self.fecha}')"

    def __str__(self) -> str:
        """String legible del gasto."""
        return f"{self.descripcion}: ${self.cantidad:.2f} ({self.fecha})"


class Ingreso:
    """
    Modelo que representa un ingreso.

    Attributes:
        id (int): Identificador único del ingreso
        descripcion (str): Descripción del ingreso
        cantidad (float): Monto del ingreso
        fecha (str): Fecha del ingreso (YYYY-MM-DD)
    """

    def __init__(self, id: int, descripcion: str, cantidad: float, fecha: str):
        """
        Inicializa un ingreso.

        Args:
            id: Identificador único
            descripcion: Descripción del ingreso
            cantidad: Monto
            fecha: Fecha en formato YYYY-MM-DD
        """
        self.id = id
        self.descripcion = descripcion
        self.cantidad = float(cantidad)
        self.fecha = fecha

    def get_mes(self) -> int:
        """
        Obtiene el mes del ingreso.

        Returns:
            int: Número del mes (1-12)
        """
        return int(self.fecha.split('-')[1])

    def get_anio(self) -> int:
        """
        Obtiene el año del ingreso.

        Returns:
            int: Año
        """
        return int(self.fecha.split('-')[0])

    def to_dict(self) -> dict:
        """
        Convierte el ingreso a diccionario.

        Returns:
            dict: Representación del ingreso
        """
        return {
            'id': self.id,
            'descripcion': self.descripcion,
            'cantidad': self.cantidad,
            'fecha': self.fecha
        }

    def __repr__(self) -> str:
        """Representación en string del ingreso."""
        return f"Ingreso(id={self.id}, descripcion='{self.descripcion}', cantidad={self.cantidad}, fecha='{self.fecha}')"

    def __str__(self) -> str:
        """String legible del ingreso."""
        return f"{self.descripcion}: ${self.cantidad:.2f} ({self.fecha})"


class GrupoGasto:
    """
    Modelo que representa un grupo de gastos compartidos.

    Attributes:
        id (int): Identificador único del grupo
        nombre (str): Nombre del grupo
        descripcion (str): Descripción del grupo
        creador_id (int): ID del usuario creador
    """

    def __init__(self, id: int, nombre: str, descripcion: str, creador_id: int):
        """
        Inicializa un grupo de gastos.

        Args:
            id: Identificador único
            nombre: Nombre del grupo
            descripcion: Descripción
            creador_id: ID del usuario creador
        """
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.creador_id = creador_id
        self.miembros = []  # Lista de IDs de miembros

    def agregar_miembro(self, usuario_id: int):
        """Agrega un miembro al grupo."""
        if usuario_id not in self.miembros:
            self.miembros.append(usuario_id)

    def remover_miembro(self, usuario_id: int):
        """Remueve un miembro del grupo."""
        if usuario_id in self.miembros:
            self.miembros.remove(usuario_id)

    def es_miembro(self, usuario_id: int) -> bool:
        """Verifica si un usuario es miembro del grupo."""
        return usuario_id in self.miembros

    def to_dict(self) -> dict:
        """
        Convierte el grupo a diccionario.

        Returns:
            dict: Representación del grupo
        """
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'creador_id': self.creador_id,
            'miembros': self.miembros
        }

    def __repr__(self) -> str:
        """Representación en string del grupo."""
        return f"GrupoGasto(id={self.id}, nombre='{self.nombre}', miembros={len(self.miembros)})"

    def __str__(self) -> str:
        """String legible del grupo."""
        return f"{self.nombre} ({len(self.miembros)} miembros)"
