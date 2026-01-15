"""
FinanzApp - Aplicación de gestión de finanzas personales.

Módulos:
    - app: Aplicación principal
    - database: Gestión de base de datos
    - login: Sistema de autenticación
    - vistas: Vistas de la interfaz
    - estilos: Estilos y temas
    - utilidades: Funciones de utilidad
"""

from .database import Database
from .app import AplicacionGastos
from .login import VentanaLogin

__version__ = "1.0.0"
__author__ = "FinanzApp Team"

