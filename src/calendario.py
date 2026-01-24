"""
Componente de calendario para seleccionar fechas.
"""

import tkinter as tk
from tkinter import ttk
import calendar
from datetime import datetime, date
from typing import Callable, Optional

try:
    from .estilos import COLORES
except ImportError:
    from estilos import COLORES


class CalendarioWidget(tk.Toplevel):
    """Widget de calendario."""

    def __init__(self, parent, callback: Callable[[str], None], fecha_inicial: Optional[str] = None):
        """
        Inicializa el calendario.
        Args:
            parent: Ventana padre
            callback: Función que se ejecuta cuando se selecciona una fecha
            fecha_inicial: Fecha inicial en formato YYYY-MM-DD (opcional)
        """
        super().__init__(parent)
        self.callback = callback
        self.fecha_seleccionada = None

        # Configurar ventana
        self.title("📅 Seleccionar Fecha")
        self.geometry("600x600")
        self.resizable(False, False)
        self.configure(bg=COLORES['fondo'])

        # Hacer modal
        self.transient(parent)
        self.grab_set()

        # Centrar en la ventana padre
        self.center_window(parent)

        # Configurar fecha inicial
        if fecha_inicial:
            try:
                self.fecha_actual = datetime.strptime(fecha_inicial, "%Y-%m-%d").date()
            except ValueError:
                self.fecha_actual = date.today()
        else:
            self.fecha_actual = date.today()

        self.mes_actual = self.fecha_actual.month
        self.anio_actual = self.fecha_actual.year

        # Aplicar estilo de ventana
        self.aplicar_estilos()
        self.crear_interfaz()

        # Focus en la ventana
        self.focus_force()

        # Animación de entrada suave
        self.attributes('-alpha', 0.0)
        self.fade_in()

    def aplicar_estilos(self):
        """Aplica estilos modernos a la ventana."""
        try:
            if hasattr(self, 'tk'):
                self.attributes('-titlebar', False)
        except:
            pass

    def fade_in(self):
        """Animación suave de entrada."""
        alpha = self.attributes('-alpha')
        if alpha < 1.0:
            alpha += 0.1
            self.attributes('-alpha', alpha)
            self.after(20, self.fade_in)

    def center_window(self, parent):
        """Centra la ventana en relación a su padre, asegurando que esté siempre visible."""
        parent.update_idletasks()

        # Dimensiones del calendario
        cal_width = 500
        cal_height = 600

        # Obtener dimensiones y posición de la pantalla
        try:
            screen_width = parent.winfo_screenwidth()
            screen_height = parent.winfo_screenheight()

            # Obtener información de la ventana padre
            parent_x = parent.winfo_x()
            parent_y = parent.winfo_y()
            parent_width = parent.winfo_width()
            parent_height = parent.winfo_height()
        except:
            # Fallback si hay algún error obteniendo información
            screen_width = 1920
            screen_height = 1080
            parent_x = 100
            parent_y = 100
            parent_width = 800
            parent_height = 600

        # Margen de seguridad desde los bordes de la pantalla
        margin = 50

        # Estrategia de posicionamiento en orden de preferencia:
        positions = [
            # 1. Centrado en el padre (posición ideal)
            (parent_x + (parent_width // 2) - (cal_width // 2),
             parent_y + (parent_height // 2) - (cal_height // 2)),

            # 2. A la derecha del padre
            (parent_x + parent_width + 20,
             parent_y + (parent_height // 2) - (cal_height // 2)),

            # 3. A la izquierda del padre
            (parent_x - cal_width - 20,
             parent_y + (parent_height // 2) - (cal_height // 2)),

            # 4. Debajo del padre
            (parent_x + (parent_width // 2) - (cal_width // 2),
             parent_y + parent_height + 20),

            # 5. Arriba del padre
            (parent_x + (parent_width // 2) - (cal_width // 2),
             parent_y - cal_height - 20),

            # 6. Centro de la pantalla (fallback)
            (screen_width // 2 - cal_width // 2,
             screen_height // 2 - cal_height // 2),
        ]

        # Función para verificar si una posición es válida
        def is_valid_position(x, y):
            return (margin <= x <= screen_width - cal_width - margin and
                    margin <= y <= screen_height - cal_height - margin)

        # Buscar la primera posición válida
        final_x, final_y = positions[-1]  # Fallback por defecto

        for x, y in positions:
            if is_valid_position(x, y):
                final_x, final_y = x, y
                break

        # Si ninguna posición es completamente válida, ajustar a los límites
        if not is_valid_position(final_x, final_y):
            final_x = max(margin, min(final_x, screen_width - cal_width - margin))
            final_y = max(margin, min(final_y, screen_height - cal_height - margin))

        # Aplicar la posición final
        self.geometry(f"+{final_x}+{final_y}")

        # Debug info (solo en desarrollo)
        DEBUG_CALENDAR_POSITION = False  # Cambiar a True para debug
        if DEBUG_CALENDAR_POSITION:
            print(f"Calendario posicionado en: x={final_x}, y={final_y}")
            print(f"Pantalla: {screen_width}x{screen_height}, Padre: {parent_x}+{parent_y} {parent_width}x{parent_height}")

    def crear_interfaz(self):
        """Crea la interfaz del calendario con diseño moderno."""
        # Frame principal con altura fija
        main_frame = tk.Frame(self, bg=COLORES['fondo'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)

        # Header con título elegante
        self.crear_header(main_frame)

        # Navegación de mes/año con diseño mejorado
        self.crear_navegacion(main_frame)

        # Separador visual
        separador = tk.Frame(main_frame, height=1, bg=COLORES['borde'], relief='flat')
        separador.pack(fill=tk.X, pady=20)

        # Frame del calendario con altura fija y scroll si es necesario
        calendario_frame = tk.Frame(main_frame, bg=COLORES['fondo_tarjeta'], height=300, width=420)
        calendario_frame.pack(fill=tk.X, pady=(0, 20))
        calendario_frame.pack_propagate(False)  # Mantener tamaño fijo

        # Frame interno para el calendario
        self.frame_calendario = tk.Frame(calendario_frame, bg=COLORES['fondo_tarjeta'])
        self.frame_calendario.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # Centrar contenido

        # Frame para botones con diseño mejorado
        self.crear_botones_frame(main_frame)

        # Actualizar calendario después de crear la estructura
        self.actualizar_calendario()

    def crear_header(self, parent):
        """Crea el header con título elegante."""
        header_frame = tk.Frame(parent, bg=COLORES['fondo'])
        header_frame.pack(fill=tk.X, pady=(0, 20))

        # Icono y título
        titulo_frame = tk.Frame(header_frame, bg=COLORES['fondo'])
        titulo_frame.pack()

        titulo = tk.Label(
            titulo_frame,
            text="📅 Seleccionar Fecha",
            font=('SF Pro Display', 18, 'bold'),
            bg=COLORES['fondo'],
            fg=COLORES['texto_primario']
        )
        titulo.pack()

        subtitulo = tk.Label(
            titulo_frame,
            text="Haz clic en el día deseado",
            font=('SF Pro Display', 11),
            bg=COLORES['fondo'],
            fg=COLORES['texto_secundario']
        )
        subtitulo.pack(pady=(3, 0))

    def crear_navegacion(self, parent):
        """Crea la navegación de mes/año con botones modernos."""
        nav_frame = tk.Frame(parent, bg=COLORES['fondo'])
        nav_frame.pack(fill=tk.X, pady=(0, 20))

        # Botón mes anterior con diseño moderno
        btn_anterior = tk.Button(
            nav_frame,
            text="❮",
            font=('SF Pro Display', 16, 'bold'),
            bg=COLORES['fondo_secundario'],
            fg=COLORES['texto_primario'],
            activebackground=COLORES['acento'],
            activeforeground='white',
            border=0,
            width=3,
            height=1,
            cursor='hand2',
            command=self.mes_anterior
        )
        btn_anterior.pack(side=tk.LEFT)

        # Efecto hover para botón anterior
        btn_anterior.bind('<Enter>', lambda e: btn_anterior.config(bg=COLORES['acento'], fg='white'))
        btn_anterior.bind('<Leave>', lambda e: btn_anterior.config(bg=COLORES['fondo_secundario'], fg=COLORES['texto_primario']))

        # Label mes y año con diseño elegante
        self.label_mes_anio = tk.Label(
            nav_frame,
            font=('SF Pro Display', 16, 'bold'),
            bg=COLORES['fondo'],
            fg=COLORES['texto_primario']
        )
        self.label_mes_anio.pack(side=tk.LEFT, expand=True)

        # Botón mes siguiente con diseño moderno
        btn_siguiente = tk.Button(
            nav_frame,
            text="❯",
            font=('SF Pro Display', 16, 'bold'),
            bg=COLORES['fondo_secundario'],
            fg=COLORES['texto_primario'],
            activebackground=COLORES['acento'],
            activeforeground='white',
            border=0,
            width=3,
            height=1,
            cursor='hand2',
            command=self.mes_siguiente
        )
        btn_siguiente.pack(side=tk.RIGHT)

        # Efecto hover para botón siguiente
        btn_siguiente.bind('<Enter>', lambda e: btn_siguiente.config(bg=COLORES['acento'], fg='white'))
        btn_siguiente.bind('<Leave>', lambda e: btn_siguiente.config(bg=COLORES['fondo_secundario'], fg=COLORES['texto_primario']))


    def crear_botones_frame(self, parent):
        """Crea el frame de botones con diseño moderno."""
        btn_frame = tk.Frame(parent, bg=COLORES['fondo'])
        btn_frame.pack(fill=tk.X)

        # Botón hoy con diseño moderno
        btn_hoy = tk.Button(
            btn_frame,
            text="📅 Hoy",
            font=('SF Pro Display', 11, 'bold'),
            bg=COLORES['acento'],
            fg='white',
            activebackground='#2c5282',
            border=0,
            padx=25,
            pady=10,
            cursor='hand2',
            command=self.seleccionar_hoy
        )
        btn_hoy.pack(side=tk.LEFT)

        # Efectos hover
        btn_hoy.bind('<Enter>', lambda e: btn_hoy.config(bg='#2c5282'))
        btn_hoy.bind('<Leave>', lambda e: btn_hoy.config(bg=COLORES['acento']))

        # Botón cancelar con diseño moderno
        btn_cancelar = tk.Button(
            btn_frame,
            text="✖ Cancelar",
            font=('SF Pro Display', 11),
            bg=COLORES['fondo_secundario'],
            fg=COLORES['texto_primario'],
            activebackground='#e74c3c',
            activeforeground='white',
            border=0,
            padx=25,
            pady=10,
            cursor='hand2',
            command=self.cancelar
        )
        btn_cancelar.pack(side=tk.RIGHT)

        # Efectos hover
        btn_cancelar.bind('<Enter>', lambda e: btn_cancelar.config(bg='#e74c3c', fg='white'))
        btn_cancelar.bind('<Leave>', lambda e: btn_cancelar.config(bg=COLORES['fondo_secundario'], fg=COLORES['texto_primario']))

    def actualizar_calendario(self):
        """Actualiza la visualización del calendario con diseño mejorado."""
        # Limpiar calendario anterior
        for widget in self.frame_calendario.winfo_children():
            widget.destroy()

        # Actualizar label de mes/año
        meses = [
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ]
        self.label_mes_anio.config(text=f"{meses[self.mes_actual - 1]} {self.anio_actual}")

        # Crear encabezados de días de la semana
        dias_semana = ["L", "M", "X", "J", "V", "S", "D"]
        colores_dia = ['#2d3748', '#2d3748', '#2d3748', '#2d3748', '#2d3748', '#e53e3e', '#e53e3e']

        for i, dia in enumerate(dias_semana):
            label = tk.Label(
                self.frame_calendario,
                text=dia,
                font=('SF Pro Display', 11, 'bold'),
                bg=COLORES['fondo_tarjeta'],
                fg=colores_dia[i],
                width=5,
                height=2
            )
            label.grid(row=0, column=i, padx=1, pady=1)

        # Obtener calendario del mes
        cal = calendar.monthcalendar(self.anio_actual, self.mes_actual)

        # Crear botones para cada día
        for semana_num, semana in enumerate(cal, 1):
            for dia_num, dia in enumerate(semana):
                if dia == 0:
                    # Día vacío
                    label = tk.Label(
                        self.frame_calendario,
                        text="",
                        width=5,
                        height=2,
                        bg=COLORES['fondo_tarjeta']
                    )
                    label.grid(row=semana_num, column=dia_num, padx=1, pady=1)
                else:
                    # Determinar estilo del botón
                    self.crear_boton_dia_simple(semana_num, dia_num, dia)

    def crear_boton_dia_simple(self, row, col, dia):
        """Crea un botón de día con diseño simple y funcional."""
        # Colores base
        bg_color = COLORES['fondo']
        fg_color = COLORES['texto_primario']

        # Resaltar día actual
        hoy = date.today()
        es_hoy = (dia == hoy.day and
                 self.mes_actual == hoy.month and
                 self.anio_actual == hoy.year)

        # Resaltar día seleccionado
        es_seleccionado = (self.fecha_seleccionada and
                          dia == self.fecha_seleccionada.day and
                          self.mes_actual == self.fecha_seleccionada.month and
                          self.anio_actual == self.fecha_seleccionada.year)

        if es_hoy:
            bg_color = COLORES['acento']
            fg_color = 'white'
        elif es_seleccionado:
            bg_color = '#27ae60'
            fg_color = 'white'
        elif col >= 5:  # Fin de semana
            fg_color = '#e53e3e'

        # Crear botón simple
        btn = tk.Button(
            self.frame_calendario,
            text=str(dia),
            font=('SF Pro Display', 11, 'bold' if es_hoy or es_seleccionado else 'normal'),
            bg=bg_color,
            fg=fg_color,
            border=0,
            width=5,
            height=2,
            cursor='hand2',
            command=lambda d=dia: self.seleccionar_dia(d)
        )
        btn.grid(row=row, column=col, padx=1, pady=1)

    def mes_anterior(self):
        """Navega al mes anterior."""
        if self.mes_actual == 1:
            self.mes_actual = 12
            self.anio_actual -= 1
        else:
            self.mes_actual -= 1
        self.actualizar_calendario()

    def mes_siguiente(self):
        """Navega al mes siguiente."""
        if self.mes_actual == 12:
            self.mes_actual = 1
            self.anio_actual += 1
        else:
            self.mes_actual += 1
        self.actualizar_calendario()

    def seleccionar_dia(self, dia):
        """Selecciona un día específico."""
        try:
            self.fecha_seleccionada = date(self.anio_actual, self.mes_actual, dia)

            # Debug: imprimir la fecha seleccionada
            fecha_str = self.fecha_seleccionada.strftime("%Y-%m-%d")
            print(f"Día seleccionado: {dia}, Fecha: {fecha_str}")

            # Actualizar visualmente primero
            self.actualizar_calendario()

            # Pequeña pausa para asegurar que la UI se actualice
            self.after(10, lambda: self._ejecutar_callback(fecha_str))

        except ValueError:
            # Fecha inválida (ej: 31 de febrero)
            print(f"Fecha inválida: {dia}/{self.mes_actual}/{self.anio_actual}")

    def _ejecutar_callback(self, fecha_str):
        """Ejecuta el callback y cierra el calendario."""
        try:
            print(f"Ejecutando callback con fecha: {fecha_str}")
            if self.callback:
                self.callback(fecha_str)
            self.destroy()
        except Exception as e:
            print(f"Error al ejecutar callback: {e}")
            self.destroy()

    def seleccionar_hoy(self):
        """Selecciona la fecha de hoy."""
        hoy = date.today()
        self.mes_actual = hoy.month
        self.anio_actual = hoy.year
        self.seleccionar_dia(hoy.day)

    def cancelar(self):
        """Cancela la selección y cierra el calendario."""
        self.destroy()


class BotonCalendario(tk.Frame):
    """Botón con entradas de fecha y calendario desplegable con diseño moderno."""

    def __init__(self, parent, fecha_inicial=None, **kwargs):
        """
        Inicializa el botón de calendario con diseño mejorado.

        Args:
            parent: Widget padre
            fecha_inicial: Fecha inicial en formato YYYY-MM-DD (opcional)
        """
        super().__init__(parent, **kwargs)

        self.configure(bg=kwargs.get('bg', COLORES['fondo']))

        # Inicializar variables StringVar en el contexto correcto
        self.dia_var = tk.StringVar(self)
        self.mes_var = tk.StringVar(self)
        self.anio_var = tk.StringVar(self)

        # Configurar valores iniciales
        if fecha_inicial:
            try:
                fecha_obj = datetime.strptime(fecha_inicial, "%Y-%m-%d")
                self.dia_var.set(f"{fecha_obj.day:02d}")
                self.mes_var.set(f"{fecha_obj.month:02d}")
                self.anio_var.set(str(fecha_obj.year))
            except ValueError:
                fecha_hoy = date.today()
                self.dia_var.set(f"{fecha_hoy.day:02d}")
                self.mes_var.set(f"{fecha_hoy.month:02d}")
                self.anio_var.set(str(fecha_hoy.year))
        else:
            fecha_hoy = date.today()
            self.dia_var.set(f"{fecha_hoy.day:02d}")
            self.mes_var.set(f"{fecha_hoy.month:02d}")
            self.anio_var.set(str(fecha_hoy.year))

        self.crear_widgets()

    def crear_widgets(self):
        """Crea los widgets del botón calendario con diseño moderno."""
        # Contenedor principal con estilo de tarjeta
        container = tk.Frame(self, bg=COLORES['fondo_input'], relief='flat', bd=0)
        container.pack(fill=tk.BOTH, expand=True)

        # Frame interno con padding
        inner_frame = tk.Frame(container, bg=COLORES['fondo_input'])
        inner_frame.pack(padx=12, pady=8)

        # Entry para día con diseño moderno
        self.entry_dia = tk.Entry(
            inner_frame,
            textvariable=self.dia_var,
            width=3,
            font=('SF Pro Display', 12, 'bold'),
            bg=COLORES['fondo_input'],
            fg=COLORES['texto_primario'],
            justify='center',
            relief='flat',
            bd=0,
            highlightthickness=0,
            insertbackground=COLORES['acento']
        )
        self.entry_dia.pack(side=tk.LEFT)

        # Separador elegante
        sep1 = tk.Label(
            inner_frame,
            text="/",
            bg=COLORES['fondo_input'],
            fg=COLORES['texto_secundario'],
            font=('SF Pro Display', 12, 'bold')
        )
        sep1.pack(side=tk.LEFT, padx=3)

        # Entry para mes con diseño moderno
        self.entry_mes = tk.Entry(
            inner_frame,
            textvariable=self.mes_var,
            width=3,
            font=('SF Pro Display', 12, 'bold'),
            bg=COLORES['fondo_input'],
            fg=COLORES['texto_primario'],
            justify='center',
            relief='flat',
            bd=0,
            highlightthickness=0,
            insertbackground=COLORES['acento']
        )
        self.entry_mes.pack(side=tk.LEFT)

        # Separador elegante
        sep2 = tk.Label(
            inner_frame,
            text="/",
            bg=COLORES['fondo_input'],
            fg=COLORES['texto_secundario'],
            font=('SF Pro Display', 12, 'bold')
        )
        sep2.pack(side=tk.LEFT, padx=3)

        # Entry para año con diseño moderno
        self.entry_anio = tk.Entry(
            inner_frame,
            textvariable=self.anio_var,
            width=5,
            font=('SF Pro Display', 12, 'bold'),
            bg=COLORES['fondo_input'],
            fg=COLORES['texto_primario'],
            justify='center',
            relief='flat',
            bd=0,
            highlightthickness=0,
            insertbackground=COLORES['acento']
        )
        self.entry_anio.pack(side=tk.LEFT)

        # Separador vertical elegante
        separator_frame = tk.Frame(inner_frame, width=1, bg=COLORES['borde'])
        separator_frame.pack(side=tk.LEFT, fill=tk.Y, padx=8)

        # Botón calendario con diseño moderno
        self.btn_calendario = tk.Button(
            inner_frame,
            text="📅",
            font=('SF Pro Display', 14),
            bg=COLORES['acento'],
            fg='white',
            activebackground='#2c5282',
            activeforeground='white',
            border=0,
            width=3,
            height=1,
            cursor='hand2',
            command=self.abrir_calendario
        )
        self.btn_calendario.pack(side=tk.LEFT)

        # Efectos hover para el botón calendario
        self.btn_calendario.bind('<Enter>', self.on_calendar_hover)
        self.btn_calendario.bind('<Leave>', self.on_calendar_leave)

        # Efectos focus para las entradas
        self.aplicar_efectos_focus()

    def aplicar_efectos_focus(self):
        """Aplica efectos de focus a las entradas."""
        entries = [self.entry_dia, self.entry_mes, self.entry_anio]

        for entry in entries:
            entry.bind('<FocusIn>', lambda e, ent=entry: self.on_entry_focus_in(ent))
            entry.bind('<FocusOut>', lambda e, ent=entry: self.on_entry_focus_out(ent))

    def on_entry_focus_in(self, entry):
        """Efecto al enfocar una entrada."""
        entry.config(bg='#ffffff', fg='#1a202c')

    def on_entry_focus_out(self, entry):
        """Efecto al desenfocar una entrada."""
        entry.config(bg=COLORES['fondo_input'], fg=COLORES['texto_primario'])

    def on_calendar_hover(self, event):
        """Efecto hover para el botón calendario."""
        self.btn_calendario.config(bg='#2c5282', relief='raised')

    def on_calendar_leave(self, event):
        """Efecto al salir del hover del botón calendario."""
        self.btn_calendario.config(bg=COLORES['acento'], relief='flat')

    def abrir_calendario(self):
        """Abre el widget de calendario con animación."""
        fecha_actual = self.obtener_fecha()
        # Efecto de clic
        self.btn_calendario.config(relief='sunken')
        self.after(100, lambda: self.btn_calendario.config(relief='flat'))

        CalendarioWidget(self, self.establecer_fecha, fecha_actual)

    def obtener_fecha(self):
        """Obtiene la fecha actual en formato YYYY-MM-DD."""
        try:
            dia = int(self.dia_var.get())
            mes = int(self.mes_var.get())
            anio = int(self.anio_var.get())
            return f"{anio:04d}-{mes:02d}-{dia:02d}"
        except ValueError:
            return date.today().strftime("%Y-%m-%d")

    def establecer_fecha(self, fecha_str):
        """Establece la fecha desde el calendario."""
        try:
            fecha_obj = datetime.strptime(fecha_str, "%Y-%m-%d")

            # Establecer nuevos valores con formato consistente
            dia_formateado = f"{fecha_obj.day:02d}"
            mes_formateado = f"{fecha_obj.month:02d}"
            anio_formateado = str(fecha_obj.year)

            # Debug: imprimir los valores (opcional, se puede quitar después)
            print(f"Estableciendo fecha: {fecha_str} -> {dia_formateado}/{mes_formateado}/{anio_formateado}")

            # Método 1: Usar StringVar (puede fallar en algunos casos)
            self.dia_var.set(dia_formateado)
            self.mes_var.set(mes_formateado)
            self.anio_var.set(anio_formateado)

            # Método 2: Actualización directa de los Entry widgets (más confiable)
            if hasattr(self, 'entry_dia') and self.entry_dia.winfo_exists():
                self.entry_dia.delete(0, tk.END)
                self.entry_dia.insert(0, dia_formateado)

            if hasattr(self, 'entry_mes') and self.entry_mes.winfo_exists():
                self.entry_mes.delete(0, tk.END)
                self.entry_mes.insert(0, mes_formateado)

            if hasattr(self, 'entry_anio') and self.entry_anio.winfo_exists():
                self.entry_anio.delete(0, tk.END)
                self.entry_anio.insert(0, anio_formateado)

            # Forzar actualización completa del widget
            self.update()

        except ValueError as e:
            print(f"Error al establecer fecha: {e}")
        except Exception as e:
            print(f"Error inesperado al establecer fecha: {e}")

    def obtener_valores(self):
        """Obtiene los valores actuales de día, mes y año."""
        return {
            'dia': self.dia_var.get(),
            'mes': self.mes_var.get(),
            'anio': self.anio_var.get()
        }

    def establecer_valores(self, dia, mes, anio):
        """Establece los valores de día, mes y año."""
        # Convertir a enteros si son strings
        dia_int = int(dia) if isinstance(dia, str) else dia
        mes_int = int(mes) if isinstance(mes, str) else mes

        self.dia_var.set(f"{dia_int:02d}")
        self.mes_var.set(f"{mes_int:02d}")
        self.anio_var.set(str(anio))