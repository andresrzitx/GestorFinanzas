"""
Estilos y utilidades visuales para la aplicación de finanzas.
Paleta elegante y minimalista con tonos tenues.
"""

import tkinter as tk
from tkinter import ttk

# Paleta de colores elegante y tenue
COLORES = {
    # Colores principales - tonos suaves
    'primario': '#4A5568',          # Gris azulado oscuro
    'secundario': '#667EEA',        # Azul lavanda suave
    'acento': '#667EEA',            # Azul elegante para botones

    # Estados
    'exito': '#48BB78',             # Verde menta suave
    'peligro': '#F56565',           # Rojo coral suave
    'advertencia': '#ED8936',       # Naranja melocotón
    'info': '#4299E1',              # Azul cielo suave

    # Fondos
    'fondo': '#F7FAFC',             # Blanco humo
    'fondo_secundario': '#EDF2F7',  # Gris muy claro
    'fondo_tarjeta': '#FFFFFF',     # Blanco puro
    'fondo_input': '#F8F9FA',       # Blanco cálido para inputs

    # Texto
    'texto_primario': '#2D3748',    # Gris carbón
    'texto_secundario': '#718096',  # Gris medio
    'texto_terciario': '#A0AEC0',   # Gris claro
    'texto_blanco': '#FFFFFF',      # Blanco

    # Bordes
    'borde': '#E2E8F0',             # Gris muy claro
    'borde_hover': '#CBD5E0',       # Gris claro hover
    'borde_focus': '#667EEA',       # Azul enfocado

    # Sombras (para efectos)
    'sombra_ligera': '#E2E8F0',
    'sombra_media': '#CBD5E0',
}

def crear_tarjeta_balance(parent, ingresos=0, gastos=0, balance=0):
    """
    Crea una tarjeta moderna con el balance de ingresos/gastos.
    Diseño minimalista y elegante.

    Args:
        parent: Widget padre
        ingresos: Cantidad de ingresos
        gastos: Cantidad de gastos
        balance: Balance total

    Returns:
        Frame con las etiquetas actualizables
    """
    # Tarjeta principal con borde sutil
    card = tk.Frame(
        parent,
        bg=COLORES['fondo_tarjeta'],
        relief='flat',
        highlightthickness=1,
        highlightbackground=COLORES['borde']
    )
    card.pack(fill=tk.X, padx=20, pady=15)

    # Contenido de la tarjeta con más espaciado
    content = tk.Frame(card, bg=COLORES['fondo_tarjeta'])
    content.pack(fill=tk.BOTH, expand=True, padx=30, pady=25)

    # Contenedor de estadísticas
    stats_container = tk.Frame(content, bg=COLORES['fondo_tarjeta'])
    stats_container.pack(fill=tk.X)

    # Ingreso
    ingreso_frame = tk.Frame(stats_container, bg=COLORES['fondo_tarjeta'])
    ingreso_frame.pack(side=tk.LEFT, padx=25, expand=True)

    tk.Label(
        ingreso_frame,
        text="Ingresos",
        font=('SF Pro Display', 10),
        bg=COLORES['fondo_tarjeta'],
        fg=COLORES['texto_terciario']
    ).pack(anchor=tk.W)

    label_ingresos = tk.Label(
        ingreso_frame,
        text=f"€{ingresos:,.2f}",
        font=('SF Pro Display', 20, 'bold'),
        bg=COLORES['fondo_tarjeta'],
        fg=COLORES['exito']
    )
    label_ingresos.pack(anchor=tk.W, pady=(5, 0))

    # Separador vertical sutil
    sep1 = tk.Frame(stats_container, bg=COLORES['borde'], width=1)
    sep1.pack(side=tk.LEFT, fill=tk.Y, padx=15, pady=10)

    # Gastos
    gasto_frame = tk.Frame(stats_container, bg=COLORES['fondo_tarjeta'])
    gasto_frame.pack(side=tk.LEFT, padx=25, expand=True)

    tk.Label(
        gasto_frame,
        text="Gastos",
        font=('SF Pro Display', 10),
        bg=COLORES['fondo_tarjeta'],
        fg=COLORES['texto_terciario']
    ).pack(anchor=tk.W)

    label_gastos = tk.Label(
        gasto_frame,
        text=f"€{gastos:,.2f}",
        font=('SF Pro Display', 20, 'bold'),
        bg=COLORES['fondo_tarjeta'],
        fg=COLORES['peligro']
    )
    label_gastos.pack(anchor=tk.W, pady=(5, 0))

    # Separador vertical sutil
    sep2 = tk.Frame(stats_container, bg=COLORES['borde'], width=1)
    sep2.pack(side=tk.LEFT, fill=tk.Y, padx=15, pady=10)

    # Balance
    balance_frame = tk.Frame(stats_container, bg=COLORES['fondo_tarjeta'])
    balance_frame.pack(side=tk.LEFT, padx=25, expand=True)

    tk.Label(
        balance_frame,
        text="Balance",
        font=('SF Pro Display', 10),
        bg=COLORES['fondo_tarjeta'],
        fg=COLORES['texto_terciario']
    ).pack(anchor=tk.W)

    color_balance = COLORES['exito'] if balance >= 0 else COLORES['peligro']
    label_balance = tk.Label(
        balance_frame,
        text=f"€{balance:+,.2f}",
        font=('SF Pro Display', 24, 'bold'),
        bg=COLORES['fondo_tarjeta'],
        fg=color_balance
    )
    label_balance.pack(anchor=tk.W, pady=(5, 0))

    return {
        'card': card,
        'label_ingresos': label_ingresos,
        'label_gastos': label_gastos,
        'label_balance': label_balance
    }

def crear_boton_moderno(parent, text, command, style='primary'):
    """
    Crea un botón moderno con estilo elegante y minimalista.
    Usa Frame + Label para mejor compatibilidad con macOS.

    Args:
        parent: Widget padre
        text: Texto del botón
        command: Función a ejecutar
        style: Estilo ('primary', 'success', 'danger', 'secondary')

    Returns:
        Frame que actúa como botón
    """
    colores_estilo = {
        'primary': (COLORES['secundario'], '#5568F5', COLORES['texto_blanco']),
        'success': (COLORES['exito'], '#38C172', COLORES['texto_blanco']),
        'danger': (COLORES['peligro'], '#F44336', COLORES['texto_blanco']),
        'secondary': ('#CBD5E0', '#A0AEC0', COLORES['texto_primario']),
        'ghost': (COLORES['fondo_tarjeta'], COLORES['fondo_secundario'], COLORES['texto_primario'])
    }

    bg_color, hover_color, fg_color = colores_estilo.get(style, colores_estilo['primary'])

    # Crear un Frame que actuará como botón
    btn_frame = tk.Frame(
        parent,
        bg=bg_color,
        cursor='hand2',
        relief='flat',
        bd=0,
        highlightthickness=0
    )

    # Crear el Label con el texto dentro del Frame
    btn_label = tk.Label(
        btn_frame,
        text=text,
        bg=bg_color,
        fg=fg_color,
        font=('SF Pro Display', 10),
        cursor='hand2',
        padx=24,
        pady=12
    )
    btn_label.pack()

    # Función de clic
    def on_click(e):
        if command:
            command()

    # Efectos hover
    def on_enter(e):
        btn_frame.config(bg=hover_color)
        btn_label.config(bg=hover_color)

    def on_leave(e):
        btn_frame.config(bg=bg_color)
        btn_label.config(bg=bg_color)

    # Bind events al Frame y al Label
    btn_frame.bind('<Button-1>', on_click)
    btn_label.bind('<Button-1>', on_click)

    btn_frame.bind('<Enter>', on_enter)
    btn_label.bind('<Enter>', on_enter)

    btn_frame.bind('<Leave>', on_leave)
    btn_label.bind('<Leave>', on_leave)

    return btn_frame

def aplicar_estilo_treeview(tree):
    """

    Aplica estilos modernos y elegantes a un Treeview.

    Args:
        tree: Widget Treeview
    """
    # Configurar colores alternados en las filas con tonos muy suaves
    tree.tag_configure('oddrow', background=COLORES['fondo_tarjeta'])
    tree.tag_configure('evenrow', background=COLORES['fondo'])

    # Estilos para diferentes estados
    tree.tag_configure('positivo', foreground=COLORES['exito'])
    tree.tag_configure('negativo', foreground=COLORES['peligro'])
    tree.tag_configure('neutral', foreground=COLORES['texto_secundario'])

def crear_campo_entrada_moderno(parent, label_text, row, column, width=30):
    """
    Crea un campo de entrada con etiqueta moderna y elegante.

    Args:
        parent: Widget padre
        label_text: Texto de la etiqueta
        row: Fila en el grid
        column: Columna en el grid
        width: Ancho del campo

    Returns:
        Entry widget creado
    """
    # Etiqueta con tipografía sutil
    label = tk.Label(
        parent,
        text=label_text,
        font=('SF Pro Display', 10),
        bg=COLORES['fondo_tarjeta'],
        fg=COLORES['texto_secundario']
    )
    label.grid(row=row, column=column, sticky=tk.W, padx=10, pady=10)

    # Campo de entrada con borde sutil
    entry = tk.Entry(
        parent,
        font=('SF Pro Display', 10),
        relief='solid',
        borderwidth=1,
        width=width,
        bg=COLORES['fondo_input'],
        fg=COLORES['texto_primario'],
        insertbackground=COLORES['texto_primario'],
        highlightthickness=1,
        highlightcolor=COLORES['borde_focus'],
        highlightbackground=COLORES['borde']
    )
    entry.grid(row=row, column=column+1, sticky=tk.W, padx=10, pady=10)

    return entry

def configurar_estilo_ttk():
    """
    Configura los estilos globales para widgets ttk con paleta elegante.
    """
    style = ttk.Style()

    # Estilo para Notebook (pestañas)
    style.configure(
        'TNotebook',
        background=COLORES['fondo'],
        borderwidth=0
    )

    style.configure(
        'TNotebook.Tab',
        background=COLORES['fondo_secundario'],
        foreground=COLORES['texto_secundario'],
        padding=[20, 10],
        font=('SF Pro Display', 10),
        borderwidth=0
    )

    style.map(
        'TNotebook.Tab',
        background=[('selected', COLORES['fondo_tarjeta'])],
        foreground=[('selected', COLORES['primario'])],
        expand=[('selected', [1, 1, 1, 0])]
    )

    # Estilo para Combobox
    style.configure(
        'TCombobox',
        fieldbackground=COLORES['fondo_input'],
        background=COLORES['fondo_tarjeta'],
        foreground=COLORES['texto_primario'],
        borderwidth=1,
        relief='solid'
    )

    # Estilo para LabelFrame
    style.configure(
        'TLabelframe',
        background=COLORES['fondo_tarjeta'],
        borderwidth=1,
        relief='solid'
    )

    style.configure(
        'TLabelframe.Label',
        background=COLORES['fondo_tarjeta'],
        foreground=COLORES['texto_secundario'],
        font=('SF Pro Display', 11, 'bold')
    )

    # Estilo para Treeview
    style.configure(
        'Treeview',
        background=COLORES['fondo_tarjeta'],
        foreground=COLORES['texto_primario'],
        fieldbackground=COLORES['fondo_tarjeta'],
        borderwidth=1,
        relief='solid',
        rowheight=30,
        font=('SF Pro Display', 10)
    )

    style.configure(
        'Treeview.Heading',
        background=COLORES['fondo_secundario'],
        foreground=COLORES['texto_secundario'],
        borderwidth=0,
        font=('SF Pro Display', 10, 'bold')
    )

    style.map(
        'Treeview',
        background=[('selected', COLORES['secundario'])],
        foreground=[('selected', COLORES['texto_blanco'])]
    )

