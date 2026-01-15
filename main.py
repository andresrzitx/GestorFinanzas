#!/usr/bin/env python3
"""
FinanzApp - Punto de entrada principal.

Aplicación de gestión de finanzas personales con sistema de login
y bases de datos separadas por usuario.
"""

import sys
import os

# Agregar el directorio src al path para importaciones
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import tkinter as tk
from src.login import VentanaLogin
from src.app import AplicacionGastos


def iniciar_aplicacion(usuario_id: int, nombre_usuario: str, rol: str = 'usuario'):
    """
    Inicia la aplicación principal después del login exitoso.

    Args:
        usuario_id: ID del usuario autenticado
        nombre_usuario: Nombre del usuario
        rol: Rol del usuario (por defecto 'usuario')
    """
    root = tk.Tk()
    app = AplicacionGastos(root, usuario_id, nombre_usuario)
    root.mainloop()


def main():
    """Función principal para ejecutar la aplicación."""
    root = tk.Tk()
    VentanaLogin(root, iniciar_aplicacion)
    root.mainloop()


if __name__ == "__main__":
    main()

