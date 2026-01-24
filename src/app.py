import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

try:
    from .database import Database
    from .vistas import VistaGastosMensual, VistaComparacionAnual, VistaEstadisticas, VistaGestionCategorias, VistaAdministracion
    from .login import VentanaLogin
except ImportError:
    from database import Database
    from vistas import VistaGastosMensual, VistaComparacionAnual, VistaEstadisticas, VistaGestionCategorias, VistaAdministracion
    from login import VentanaLogin


class AplicacionGastos:
    """Aplicación principal de gestión de gastos mensuales."""

    def __init__(self, root, usuario_id, nombre_usuario, rol='usuario'):
        """
        Inicializa la aplicación.
        Args:
            root: Ventana principal de Tkinter
            usuario_id: ID del usuario autenticado
            nombre_usuario: Nombre del usuario
            rol: Rol del usuario ('usuario' o 'admin')
        """
        self.root = root
        self.usuario_id = usuario_id
        self.nombre_usuario = nombre_usuario
        self.rol = rol
        self.root.title(f"💰 FinanzApp - {nombre_usuario}" + (" [ADMIN]" if rol == 'admin' else ""))
        self.root.geometry("1200x800")

        # Centrar ventana en la pantalla
        self.centrar_ventana()

        # Configurar icono y colores de fondo
        self.root.configure(bg='#f5f6fa')

        # Intentar maximizar en algunos sistemas
        try:
            self.root.state('zoomed')  # Windows
        except:
            try:
                self.root.attributes('-zoomed', True)  # Linux
            except:
                pass  # macOS no soporta maximizar automático

        # Inicializar base de datos con el usuario autenticado
        self.db = Database(usuario_id=usuario_id)

        # Año actual
        self.anio_actual = datetime.now().year

        # Configurar estilos
        self.configurar_estilos()

        # Crear interfaz
        self.crear_interfaz()

    def centrar_ventana(self):
        """Centra la ventana en la pantalla."""
        self.root.update_idletasks()
        width = 1200
        height = 800
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def configurar_estilos(self):
        """Configurar los estilos de la aplicación."""
        try:
            from .estilos import configurar_estilo_ttk
            configurar_estilo_ttk()
        except ImportError:
            from estilos import configurar_estilo_ttk
            configurar_estilo_ttk()

    def crear_interfaz(self):
        """Crea la interfaz principal de la aplicación."""
        # Frame principal
        main_container = tk.Frame(self.root, bg='#F7FAFC')
        main_container.pack(fill=tk.BOTH, expand=True)

        # Header
        header = tk.Frame(main_container, bg='#FFFFFF', height=100)
        header.pack(fill=tk.X, padx=0, pady=0)
        header.pack_propagate(False)

        # Contenedor del header
        header_content = tk.Frame(header, bg='#FFFFFF')
        header_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)

        # Título principal
        title_frame = tk.Frame(header_content, bg='#FFFFFF')
        title_frame.pack(side=tk.LEFT)

        titulo = tk.Label(
            title_frame,
            text="FinanzApp",
            font=('SF Pro Display', 22, 'bold'),
            bg='#FFFFFF',
            fg='#4A5568'
        )
        titulo.pack(side=tk.TOP, anchor=tk.W)

        subtitulo = tk.Label(
            title_frame,
            text=f"Hola, {self.nombre_usuario}",
            font=('SF Pro Display', 11),
            bg='#FFFFFF',
            fg='#A0AEC0'
        )
        subtitulo.pack(side=tk.TOP, anchor=tk.W)

        # Panel de controles a la derecha
        controls_frame = tk.Frame(header_content, bg='#FFFFFF')
        controls_frame.pack(side=tk.RIGHT, padx=10)

        # Selector de año
        year_frame = tk.Frame(controls_frame, bg='#FFFFFF', relief='flat')
        year_frame.pack(side=tk.LEFT, padx=10)

        tk.Label(
            year_frame,
            text="Año",
            font=('SF Pro Display', 10),
            bg='#FFFFFF',
            fg='#718096'
        ).pack(side=tk.LEFT, padx=(10, 5), pady=8)

        self.combo_anio = ttk.Combobox(
            year_frame,
            values=list(range(2020, 2031)),
            width=10,
            state='readonly',
            font=('SF Pro Display', 10)
        )
        self.combo_anio.set(self.anio_actual)
        self.combo_anio.pack(side=tk.LEFT, padx=(0, 10), pady=8)
        self.combo_anio.bind('<<ComboboxSelected>>', self.cambiar_anio)

        # Botón refrescar
        try:
            from .estilos import crear_boton_moderno
        except ImportError:
            from estilos import crear_boton_moderno

        btn_refrescar = crear_boton_moderno(
            controls_frame,
            text="Actualizar",
            command=self.refrescar_vistas,
            style='primary'
        )
        btn_refrescar.pack(side=tk.LEFT, padx=8)

        # Contenedor del contenido principal
        content_frame = tk.Frame(main_container, bg='#F7FAFC')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Notebook con pestañas modernas
        self.notebook = ttk.Notebook(content_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Crear pestañas para cada mes
        self.vistas_mensuales = {}
        meses = [
            "Enero", "Febrero", "Marzo", "Abril",
            "Mayo", "Junio", "Julio", "Agosto",
            "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ]

        for i, mes in enumerate(meses, 1):
            vista = VistaGastosMensual(self.notebook, self.db, i, self.anio_actual)
            self.notebook.add(vista.frame, text=mes)
            self.vistas_mensuales[i] = vista

        # Pestaña de comparación anual
        self.vista_comparacion = VistaComparacionAnual(
            self.notebook, self.db, self.anio_actual
        )
        self.notebook.add(self.vista_comparacion.frame, text="Comparación Anual")

        # Pestaña de estadísticas
        self.vista_estadisticas = VistaEstadisticas(
            self.notebook, self.db, self.anio_actual
        )
        self.notebook.add(self.vista_estadisticas.frame, text="Estadísticas")

        # Pestaña de gestión de categorías
        self.vista_categorias = VistaGestionCategorias(
            self.notebook, self.db
        )
        self.notebook.add(self.vista_categorias.frame, text="Categorías")

        # Pestaña de administración (solo para admins)
        if self.rol == 'admin':
            # Crear instancia de Database sin usuario_id para acceso global
            db_admin = Database()
            self.vista_administracion = VistaAdministracion(
                self.notebook, db_admin
            )
            self.notebook.add(self.vista_administracion.frame, text="👨‍💼 Administración")

        # Barra de estado
        footer = tk.Frame(main_container, bg='#EDF2F7', height=35)
        footer.pack(fill=tk.X, side=tk.BOTTOM)
        footer.pack_propagate(False)

        self.barra_estado = tk.Label(
            footer,
            text=f"Año seleccionado: {self.anio_actual} • FinanzApp v3.0",
            bg='#EDF2F7',
            fg='#718096',
            font=('SF Pro Display', 9),
            anchor=tk.W,
            padx=20
        )
        self.barra_estado.pack(fill=tk.BOTH, expand=True)

    def cambiar_anio(self, event=None):
        """Cambia el año seleccionado y actualiza todas las vistas."""
        nuevo_anio = int(self.combo_anio.get())
        self.anio_actual = nuevo_anio

        # Actualizar vistas mensuales
        for mes, vista in self.vistas_mensuales.items():
            vista.cambiar_anio(nuevo_anio)

        # Actualizar vista de comparación
        self.vista_comparacion.cambiar_anio(nuevo_anio)

        # Actualizar vista de estadísticas
        self.vista_estadisticas.cambiar_anio(nuevo_anio)

        # Actualizar barra de estado
        self.barra_estado.config(text=f"Año seleccionado: {self.anio_actual} • FinanzApp v3.0")

    def refrescar_vistas(self):
        """Refresca todas las vistas."""
        # Refrescar vistas mensuales
        for vista in self.vistas_mensuales.values():
            vista.cargar_gastos()

        # Refrescar vista de comparación
        self.vista_comparacion.cargar_datos()

        # Refrescar vista de estadísticas
        self.vista_estadisticas.cargar_datos()

        # Refrescar vista de categorías
        self.vista_categorias.refrescar()

        messagebox.showinfo(
            "✓ Actualización Completada",
            "Todas las vistas han sido actualizadas correctamente.\n\n"
            "Los datos están sincronizados con la base de datos."
        )

    def cerrar_sesion(self):
        """Cierra la sesión del usuario actual."""
        respuesta = messagebox.askyesno(
            "Cerrar Sesión",
            f"¿Estás seguro de que quieres cerrar la sesión de {self.nombre_usuario}?"
        )

        if respuesta:
            # Cerrar la ventana actual
            self.root.destroy()

            # Crear nueva ventana para login
            # Nota: La función iniciar_aplicacion debe ser importada desde main
            nueva_ventana = tk.Tk()

            # Importar dinámicamente para evitar dependencias circulares
            import sys
            import os
            sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
            from main import iniciar_aplicacion

            VentanaLogin(nueva_ventana, iniciar_aplicacion)
            nueva_ventana.mainloop()

