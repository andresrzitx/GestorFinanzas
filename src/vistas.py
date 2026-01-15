"""
Módulo de vistas para la aplicación de gastos mensuales.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


try:
    from .estilos import crear_tarjeta_balance, crear_boton_moderno, COLORES
except ImportError:
    from estilos import crear_tarjeta_balance, crear_boton_moderno, COLORES


class VistaGastosMensual:
    """Vista para mostrar y gestionar los gastos de un mes específico."""

    def __init__(self, parent, db, mes: int, anio: int):
        """
        Inicializa la vista mensual.

        Args:
            parent: Widget padre
            db: Instancia de la base de datos
            mes: Número del mes (1-12)
            anio: Año
        """
        self.db = db
        self.mes = mes
        self.anio = anio

        # Frame principal (usar tk.Frame para soportar bg)
        self.frame = tk.Frame(parent, bg=COLORES['fondo'])

        # Crear interfaz
        self.crear_interfaz()

        # Cargar gastos
        self.cargar_gastos()

    def crear_interfaz(self):
        """Crea la interfaz de la vista mensual con diseño moderno."""

        # Tarjeta de balance moderna
        self.balance_widgets = crear_tarjeta_balance(self.frame, 0, 0, 0)

        # Notebook para gastos e ingresos
        self.notebook = ttk.Notebook(self.frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))

        # Pestaña de gastos
        self.frame_gastos = tk.Frame(self.notebook, bg=COLORES['fondo_tarjeta'])
        self.notebook.add(self.frame_gastos, text="💸 Gastos")

        # Pestaña de ingresos
        self.frame_ingresos = tk.Frame(self.notebook, bg=COLORES['fondo_tarjeta'])
        self.notebook.add(self.frame_ingresos, text="💰 Ingresos")

        # Crear interfaz de gastos
        self.crear_interfaz_gastos()

        # Crear interfaz de ingresos
        self.crear_interfaz_ingresos()

        # Cargar datos
        self.cargar_gastos()
        self.cargar_ingresos()

    def crear_interfaz_gastos(self):
        """Crea la interfaz para gestionar gastos."""
        # Frame superior: formulario para agregar gastos
        frame_formulario = ttk.LabelFrame(
            self.frame_gastos,
            text="Agregar Nuevo Gasto",
            padding="10"
        )
        frame_formulario.pack(fill=tk.X, padx=10, pady=10)

        # Fila 1: Descripción
        ttk.Label(frame_formulario, text="Descripción:").grid(
            row=0, column=0, sticky=tk.W, padx=5, pady=5
        )
        self.entry_descripcion = ttk.Entry(frame_formulario, width=40)
        self.entry_descripcion.grid(row=0, column=1, columnspan=2, padx=5, pady=5)

        # Fila 2: Cantidad y Categoría
        ttk.Label(frame_formulario, text="Cantidad:").grid(
            row=1, column=0, sticky=tk.W, padx=5, pady=5
        )
        self.entry_cantidad = ttk.Entry(frame_formulario, width=15)
        self.entry_cantidad.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)

        ttk.Label(frame_formulario, text="Categoría:").grid(
            row=1, column=2, sticky=tk.W, padx=5, pady=5
        )

        # Cargar categorías
        categorias = self.db.obtener_categorias()
        self.categorias_dict = {cat[1]: cat[0] for cat in categorias}

        self.combo_categoria = ttk.Combobox(
            frame_formulario,
            values=list(self.categorias_dict.keys()),
            width=20,
            state='readonly'
        )
        if self.categorias_dict:
            self.combo_categoria.current(0)
        self.combo_categoria.grid(row=1, column=3, padx=5, pady=5)

        # Fila 3: Fecha y Método de Pago
        ttk.Label(frame_formulario, text="Fecha:").grid(
            row=2, column=0, sticky=tk.W, padx=5, pady=5
        )

        # Importar el componente de calendario
        try:
            from .calendario import BotonCalendario
        except ImportError:
            from calendario import BotonCalendario

        # Widget de calendario para gastos
        fecha_actual = f"{self.anio:04d}-{self.mes:02d}-{datetime.now().day:02d}"
        self.fecha_gasto = BotonCalendario(
            frame_formulario,
            fecha_inicial=fecha_actual,
            bg='#f8f9fa'
        )
        self.fecha_gasto.grid(row=2, column=1, columnspan=1, sticky=tk.W, padx=5, pady=5)

        # Método de pago
        ttk.Label(frame_formulario, text="Método:").grid(
            row=2, column=2, sticky=tk.W, padx=5, pady=5
        )

        self.combo_metodo_pago = ttk.Combobox(
            frame_formulario,
            values=["💵 Efectivo", "💳 Tarjeta"],
            width=15,
            state='readonly'
        )
        self.combo_metodo_pago.current(1)  # Tarjeta por defecto
        self.combo_metodo_pago.grid(row=2, column=3, padx=5, pady=5)

        # Botón agregar (nueva fila)
        btn_agregar = ttk.Button(
            frame_formulario,
            text="➕ Agregar Gasto",
            command=self.agregar_gasto
        )
        btn_agregar.grid(row=3, column=3, padx=5, pady=5)

        # Frame medio: Lista de gastos
        frame_lista = ttk.LabelFrame(
            self.frame_gastos,
            text="Gastos del Mes",
            padding="10"
        )
        frame_lista.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Crear Treeview
        columnas = ("ID", "Fecha", "Descripción", "Categoría", "Método", "Monto")
        self.tree_gastos = ttk.Treeview(
            frame_lista,
            columns=columnas,
            show="headings",
            height=15
        )

        # Configurar columnas
        self.tree_gastos.heading("ID", text="ID")
        self.tree_gastos.heading("Fecha", text="Fecha")
        self.tree_gastos.heading("Descripción", text="Descripción")
        self.tree_gastos.heading("Categoría", text="Categoría")
        self.tree_gastos.heading("Método", text="Método")
        self.tree_gastos.heading("Monto", text="Cantidad (€)")

        self.tree_gastos.column("ID", width=50, anchor=tk.CENTER)
        self.tree_gastos.column("Fecha", width=100, anchor=tk.CENTER)
        self.tree_gastos.column("Descripción", width=250)
        self.tree_gastos.column("Categoría", width=120)
        self.tree_gastos.column("Método", width=80, anchor=tk.CENTER)
        self.tree_gastos.column("Monto", width=100, anchor=tk.E)

        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_lista, orient=tk.VERTICAL, command=self.tree_gastos.yview)
        self.tree_gastos.configure(yscrollcommand=scrollbar.set)

        self.tree_gastos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Frame para botones
        btn_frame = tk.Frame(frame_lista, bg=COLORES['fondo_tarjeta'])
        btn_frame.pack(pady=5)

        # Botón editar
        try:
            from .estilos import crear_boton_moderno
        except ImportError:
            from estilos import crear_boton_moderno

        btn_editar = crear_boton_moderno(
            btn_frame,
            text="✏️ Editar",
            command=self.editar_gasto,
            style='secondary'
        )
        btn_editar.pack(side=tk.LEFT, padx=5)

        # Botón eliminar
        btn_eliminar = crear_boton_moderno(
            btn_frame,
            text="🗑️ Eliminar",
            command=self.eliminar_gasto,
            style='danger'
        )
        btn_eliminar.pack(side=tk.LEFT, padx=5)

        # Total de gastos
        self.label_total_gastos = ttk.Label(
            self.frame_gastos,
            text="Total gastos: €0.00",
            font=('Arial', 11, 'bold'),
            foreground='red'
        )
        self.label_total_gastos.pack(pady=5)

    def crear_interfaz_ingresos(self):
        """Crea la interfaz para gestionar ingresos."""
        # Frame superior: formulario para agregar ingresos
        frame_formulario = ttk.LabelFrame(
            self.frame_ingresos,
            text="Agregar Nuevo Ingreso",
            padding="10"
        )
        frame_formulario.pack(fill=tk.X, padx=10, pady=10)

        # Fila 1: Descripción
        ttk.Label(frame_formulario, text="Descripción:").grid(
            row=0, column=0, sticky=tk.W, padx=5, pady=5
        )
        self.entry_descripcion_ingreso = ttk.Entry(frame_formulario, width=40)
        self.entry_descripcion_ingreso.grid(row=0, column=1, columnspan=2, padx=5, pady=5)

        # Fila 2: Cantidad y Fuente
        ttk.Label(frame_formulario, text="Cantidad:").grid(
            row=1, column=0, sticky=tk.W, padx=5, pady=5
        )
        self.entry_cantidad_ingreso = ttk.Entry(frame_formulario, width=15)
        self.entry_cantidad_ingreso.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)

        ttk.Label(frame_formulario, text="Fuente:").grid(
            row=1, column=2, sticky=tk.W, padx=5, pady=5
        )

        # Fuentes comunes de ingreso
        fuentes = ["Salario", "Freelance", "Inversiones", "Venta", "Regalo", "Otros"]
        self.combo_fuente = ttk.Combobox(
            frame_formulario,
            values=fuentes,
            width=20
        )
        self.combo_fuente.current(0)
        self.combo_fuente.grid(row=1, column=3, padx=5, pady=5)

        # Fila 3: Fecha
        ttk.Label(frame_formulario, text="Fecha:").grid(
            row=2, column=0, sticky=tk.W, padx=5, pady=5
        )

        # Importar el componente de calendario
        try:
            from .calendario import BotonCalendario
        except ImportError:
            from calendario import BotonCalendario

        # Widget de calendario para ingresos
        fecha_actual = f"{self.anio:04d}-{self.mes:02d}-{datetime.now().day:02d}"
        self.fecha_ingreso = BotonCalendario(
            frame_formulario,
            fecha_inicial=fecha_actual,
            bg='#f8f9fa'
        )
        self.fecha_ingreso.grid(row=2, column=1, columnspan=2, sticky=tk.W, padx=5, pady=5)

        # Botón agregar
        btn_agregar = ttk.Button(
            frame_formulario,
            text="➕ Agregar Ingreso",
            command=self.agregar_ingreso
        )
        btn_agregar.grid(row=2, column=3, padx=5, pady=5)

        # Frame medio: Lista de ingresos
        frame_lista = ttk.LabelFrame(
            self.frame_ingresos,
            text="Ingresos del Mes",
            padding="10"
        )
        frame_lista.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Crear Treeview para ingresos
        columnas = ("ID", "Fecha", "Descripción", "Fuente", "Monto")
        self.tree_ingresos = ttk.Treeview(
            frame_lista,
            columns=columnas,
            show="headings",
            height=15
        )

        # Configurar columnas
        self.tree_ingresos.heading("ID", text="ID")
        self.tree_ingresos.heading("Fecha", text="Fecha")
        self.tree_ingresos.heading("Descripción", text="Descripción")
        self.tree_ingresos.heading("Fuente", text="Fuente")
        self.tree_ingresos.heading("Monto", text="Cantidad (€)")

        self.tree_ingresos.column("ID", width=50, anchor=tk.CENTER)
        self.tree_ingresos.column("Fecha", width=100, anchor=tk.CENTER)
        self.tree_ingresos.column("Descripción", width=300)
        self.tree_ingresos.column("Fuente", width=150)
        self.tree_ingresos.column("Monto", width=100, anchor=tk.E)

        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_lista, orient=tk.VERTICAL, command=self.tree_ingresos.yview)
        self.tree_ingresos.configure(yscrollcommand=scrollbar.set)

        self.tree_ingresos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Frame para botones
        btn_frame_ing = tk.Frame(frame_lista, bg=COLORES['fondo_tarjeta'])
        btn_frame_ing.pack(pady=5)

        # Botón editar
        btn_editar_ing = crear_boton_moderno(
            btn_frame_ing,
            text="✏️ Editar",
            command=self.editar_ingreso,
            style='secondary'
        )
        btn_editar_ing.pack(side=tk.LEFT, padx=5)

        # Botón eliminar
        btn_eliminar_ing = crear_boton_moderno(
            btn_frame_ing,
            text="🗑️ Eliminar",
            command=self.eliminar_ingreso,
            style='danger'
        )
        btn_eliminar_ing.pack(side=tk.LEFT, padx=5)

        # Total de ingresos
        self.label_total_ingresos = ttk.Label(
            self.frame_ingresos,
            text="Total ingresos: €0.00",
            font=('Arial', 11, 'bold'),
            foreground='green'
        )
        self.label_total_ingresos.pack(pady=5)

    def agregar_gasto(self):
        """Agrega un nuevo gasto."""
        # Validar campos
        descripcion = self.entry_descripcion.get().strip()
        cantidad_str = self.entry_cantidad.get().strip()
        categoria_nombre = self.combo_categoria.get()

        if not descripcion:
            messagebox.showerror("Error", "La descripción es obligatoria")
            return

        if not cantidad_str:
            messagebox.showerror("Error", "La cantidad es obligatoria")
            return

        try:
            cantidad = float(cantidad_str)
            if cantidad <= 0:
                raise ValueError("La cantidad debe ser positiva")
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número positivo")
            return

        if not categoria_nombre:
            messagebox.showerror("Error", "Debe seleccionar una categoría")
            return

        categoria_id = self.categorias_dict[categoria_nombre]

        # Obtener método de pago
        metodo_seleccionado = self.combo_metodo_pago.get()
        metodo_pago = 'efectivo' if '💵' in metodo_seleccionado else 'tarjeta'

        # Construir fecha
        try:
            valores_fecha = self.fecha_gasto.obtener_valores()
            dia = int(valores_fecha['dia'])
            mes = int(valores_fecha['mes'])
            anio = int(valores_fecha['anio'])
            fecha = f"{anio:04d}-{mes:02d}-{dia:02d}"
            # Validar fecha
            datetime.strptime(fecha, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Fecha inválida")
            return

        # Agregar a la base de datos
        if self.db.agregar_gasto(descripcion, cantidad, categoria_id, fecha, metodo_pago):
            messagebox.showinfo("Éxito", "Gasto agregado correctamente")

            # Limpiar campos
            self.entry_descripcion.delete(0, tk.END)
            self.entry_cantidad.delete(0, tk.END)
            # Resetear fecha a hoy
            fecha_hoy = datetime.now()
            self.fecha_gasto.establecer_valores(fecha_hoy.day, fecha_hoy.month, fecha_hoy.year)
            self.combo_metodo_pago.current(1)  # Resetear a tarjeta

            # Recargar gastos
            self.cargar_gastos()
        else:
            messagebox.showerror("Error", "No se pudo agregar el gasto")

    def agregar_ingreso(self):
        """Agrega un nuevo ingreso."""
        # Validar campos
        descripcion = self.entry_descripcion_ingreso.get().strip()
        cantidad_str = self.entry_cantidad_ingreso.get().strip()
        fuente = self.combo_fuente.get()

        if not descripcion:
            messagebox.showerror("Error", "La descripción es obligatoria")
            return

        if not cantidad_str:
            messagebox.showerror("Error", "La cantidad es obligatoria")
            return

        try:
            cantidad = float(cantidad_str)
            if cantidad <= 0:
                raise ValueError("La cantidad debe ser positiva")
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número positivo")
            return

        if not fuente:
            messagebox.showerror("Error", "Debe seleccionar una fuente")
            return

        # Construir fecha
        try:
            valores_fecha = self.fecha_ingreso.obtener_valores()
            dia = int(valores_fecha['dia'])
            mes = int(valores_fecha['mes'])
            anio = int(valores_fecha['anio'])
            fecha = f"{anio:04d}-{mes:02d}-{dia:02d}"
            # Validar fecha
            datetime.strptime(fecha, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Fecha inválida")
            return

        # Agregar a la base de datos
        if self.db.agregar_ingreso(descripcion, cantidad, fuente, fecha):
            messagebox.showinfo("Éxito", "Ingreso agregado correctamente")

            # Limpiar campos
            self.entry_descripcion_ingreso.delete(0, tk.END)
            self.entry_cantidad_ingreso.delete(0, tk.END)
            # Resetear fecha a hoy
            fecha_hoy = datetime.now()
            self.fecha_ingreso.establecer_valores(fecha_hoy.day, fecha_hoy.month, fecha_hoy.year)

            # Recargar ingresos
            self.cargar_ingresos()
        else:
            messagebox.showerror("Error", "No se pudo agregar el ingreso")

    def cargar_gastos(self):
        """Carga los gastos del mes en el Treeview."""
        # Limpiar tree
        for item in self.tree_gastos.get_children():
            self.tree_gastos.delete(item)

        # Obtener gastos
        gastos = self.db.obtener_gastos_mes(self.mes, self.anio)

        # Agregar al tree
        for gasto in gastos:
            # Manejar ambos formatos: con y sin metodo_pago
            if len(gasto) == 6:
                gasto_id, descripcion, cantidad, categoria, fecha, metodo_pago = gasto
            else:
                gasto_id, descripcion, cantidad, categoria, fecha = gasto
                metodo_pago = 'tarjeta'  # Valor por defecto

            # Mostrar icono según método de pago
            metodo_texto = "💵 Efectivo" if metodo_pago == 'efectivo' else "💳 Tarjeta"

            self.tree_gastos.insert(
                "",
                tk.END,
                values=(gasto_id, fecha, descripcion, categoria, metodo_texto, f"{cantidad:.2f}")
            )

        # Actualizar totales y balance
        self.actualizar_balance()

    def cargar_ingresos(self):
        """Carga los ingresos del mes en el Treeview."""
        # Limpiar tree
        for item in self.tree_ingresos.get_children():
            self.tree_ingresos.delete(item)

        # Obtener ingresos
        ingresos = self.db.obtener_ingresos_mes(self.mes, self.anio)

        # Agregar al tree
        for ingreso in ingresos:
            ingreso_id, descripcion, cantidad, fuente, fecha = ingreso
            self.tree_ingresos.insert(
                "",
                tk.END,
                values=(ingreso_id, fecha, descripcion, fuente, f"{cantidad:.2f}")
            )

        # Actualizar totales y balance
        self.actualizar_balance()

    def actualizar_balance(self):
        """Actualiza los labels de balance, ingresos y gastos con estilo moderno."""
        balance_data = self.db.obtener_balance_mes(self.mes, self.anio)

        ingresos = balance_data['ingresos']
        gastos = balance_data['gastos']
        balance = balance_data['balance']

        # Actualizar tarjeta de balance
        self.balance_widgets['label_ingresos'].config(text=f"€{ingresos:,.2f}")
        self.balance_widgets['label_gastos'].config(text=f"€{gastos:,.2f}")

        # Color dinámico para el balance
        color_balance = COLORES['exito'] if balance >= 0 else COLORES['peligro']
        self.balance_widgets['label_balance'].config(
            text=f"€{balance:+,.2f}",
            fg=color_balance
        )

        # Actualizar totales individuales si existen (para compatibilidad)
        if hasattr(self, 'label_total_gastos'):
            self.label_total_gastos.config(text=f"Total gastos: €{gastos:,.2f}")
        if hasattr(self, 'label_total_ingresos'):
            self.label_total_ingresos.config(text=f"Total ingresos: €{ingresos:,.2f}")

    def eliminar_gasto(self):
        """Elimina el gasto seleccionado."""
        seleccion = self.tree_gastos.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un gasto para eliminar")
            return

        # Confirmar eliminación
        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este gasto?"):
            item = self.tree_gastos.item(seleccion[0])
            gasto_id = item['values'][0]

            if self.db.eliminar_gasto(gasto_id):
                messagebox.showinfo("Éxito", "Gasto eliminado correctamente")
                self.cargar_gastos()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el gasto")

    def eliminar_ingreso(self):
        """Elimina el ingreso seleccionado."""
        seleccion = self.tree_ingresos.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un ingreso para eliminar")
            return

        # Confirmar eliminación
        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este ingreso?"):
            item = self.tree_ingresos.item(seleccion[0])
            ingreso_id = item['values'][0]

            if self.db.eliminar_ingreso(ingreso_id):
                messagebox.showinfo("Éxito", "Ingreso eliminado correctamente")
                self.cargar_ingresos()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el ingreso")

    def editar_gasto(self):
        """Edita el gasto seleccionado."""
        seleccion = self.tree_gastos.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un gasto para editar")
            return

        # Obtener el ID del gasto seleccionado
        item = self.tree_gastos.item(seleccion[0])
        gasto_id = item['values'][0]

        # Obtener los detalles del gasto
        gasto = self.db.obtener_gasto_por_id(gasto_id)
        if not gasto:
            messagebox.showerror("Error", "No se pudo obtener la información del gasto")
            return

        # Crear ventana de edición
        self.ventana_editar_gasto(gasto)

    def ventana_editar_gasto(self, gasto):
        """
        Muestra una ventana emergente para editar un gasto.

        Args:
            gasto: Tupla (id, descripcion, cantidad, categoria_id, fecha, mes, anio, metodo_pago)
        """
        # Desempaquetar con valor por defecto para compatibilidad con bases de datos antiguas
        if len(gasto) == 8:
            gasto_id, descripcion, cantidad, categoria_id, fecha, mes, anio, metodo_pago = gasto
        else:
            gasto_id, descripcion, cantidad, categoria_id, fecha, mes, anio = gasto
            metodo_pago = 'tarjeta'  # Valor por defecto

        # Crear ventana emergente
        ventana = tk.Toplevel(self.frame.winfo_toplevel())
        ventana.title("Editar Gasto")
        ventana.geometry("450x480")
        ventana.configure(bg=COLORES['fondo_tarjeta'])
        ventana.transient(self.frame.winfo_toplevel())
        ventana.grab_set()

        # Título
        tk.Label(
            ventana,
            text="✏️ Editar Gasto",
            font=('SF Pro Display', 16, 'bold'),
            bg=COLORES['fondo_tarjeta'],
            fg=COLORES['texto_primario']
        ).pack(pady=15)

        # Frame del formulario
        form = tk.Frame(ventana, bg=COLORES['fondo_tarjeta'])
        form.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)

        # Descripción
        tk.Label(form, text="Descripción:", font=('SF Pro Display', 10),
                bg=COLORES['fondo_tarjeta'], fg=COLORES['texto_secundario']).grid(
            row=0, column=0, sticky=tk.W, pady=(10, 5))

        entry_desc = tk.Entry(form, font=('SF Pro Display', 10), width=30,
                             bg=COLORES['fondo_input'], fg=COLORES['texto_primario'])
        entry_desc.grid(row=0, column=1, pady=(10, 5), sticky=tk.EW)
        entry_desc.insert(0, descripcion)

        # Cantidad
        tk.Label(form, text="Cantidad (€):", font=('SF Pro Display', 10),
                bg=COLORES['fondo_tarjeta'], fg=COLORES['texto_secundario']).grid(
            row=1, column=0, sticky=tk.W, pady=5)

        entry_cant = tk.Entry(form, font=('SF Pro Display', 10), width=30,
                             bg=COLORES['fondo_input'], fg=COLORES['texto_primario'])
        entry_cant.grid(row=1, column=1, pady=5, sticky=tk.EW)
        entry_cant.insert(0, str(cantidad))

        # Categoría
        tk.Label(form, text="Categoría:", font=('SF Pro Display', 10),
                bg=COLORES['fondo_tarjeta'], fg=COLORES['texto_secundario']).grid(
            row=2, column=0, sticky=tk.W, pady=5)

        categorias = self.db.obtener_categorias()
        nombres_cat = [cat[1] for cat in categorias]

        combo_cat = ttk.Combobox(form, values=nombres_cat, state='readonly',
                                font=('SF Pro Display', 10), width=28)
        combo_cat.grid(row=2, column=1, pady=5, sticky=tk.EW)

        # Seleccionar la categoría actual
        for cat in categorias:
            if cat[0] == categoria_id:
                combo_cat.set(cat[1])
                break

        # Fecha
        tk.Label(form, text="Fecha:", font=('SF Pro Display', 10),
                bg=COLORES['fondo_tarjeta'], fg=COLORES['texto_secundario']).grid(
            row=3, column=0, sticky=tk.W, pady=5)

        # Widget de calendario para editar gasto
        try:
            from .calendario import BotonCalendario
        except ImportError:
            from calendario import BotonCalendario

        fecha_calendario_gasto = BotonCalendario(
            form,
            fecha_inicial=fecha,
            bg=COLORES['fondo_tarjeta']
        )
        fecha_calendario_gasto.grid(row=3, column=1, pady=5, sticky=tk.W)

        # Método de pago
        tk.Label(form, text="Método de Pago:", font=('SF Pro Display', 10),
                bg=COLORES['fondo_tarjeta'], fg=COLORES['texto_secundario']).grid(
            row=4, column=0, sticky=tk.W, pady=5)

        combo_metodo = ttk.Combobox(form, values=["💵 Efectivo", "💳 Tarjeta"],
                                    state='readonly', font=('SF Pro Display', 10), width=28)
        combo_metodo.grid(row=4, column=1, pady=5, sticky=tk.EW)
        # Seleccionar el método actual
        combo_metodo.current(0 if metodo_pago == 'efectivo' else 1)

        form.columnconfigure(1, weight=1)

        # Frame para botones
        btn_frame = tk.Frame(ventana, bg=COLORES['fondo_tarjeta'])
        btn_frame.pack(pady=20)

        try:
            from .estilos import crear_boton_moderno
        except ImportError:
            from estilos import crear_boton_moderno

        def guardar_cambios():
            # Validar
            nueva_desc = entry_desc.get().strip()
            nueva_cant_str = entry_cant.get().strip()
            nueva_cat = combo_cat.get()
            nueva_fecha = fecha_calendario_gasto.obtener_fecha()

            if not nueva_desc or not nueva_cant_str or not nueva_cat:
                messagebox.showerror("Error", "Todos los campos son obligatorios")
                return

            try:
                nueva_cant = float(nueva_cant_str)
                if nueva_cant <= 0:
                    raise ValueError()
            except ValueError:
                messagebox.showerror("Error", "La cantidad debe ser un número positivo")
                return

            # Validar fecha
            try:
                datetime.strptime(nueva_fecha, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Error", "Fecha inválida")
                return

            # Obtener ID de categoría
            nueva_cat_id = None
            for cat in categorias:
                if cat[1] == nueva_cat:
                    nueva_cat_id = cat[0]
                    break

            if not nueva_cat_id:
                messagebox.showerror("Error", "Categoría no válida")
                return

            # Obtener método de pago
            metodo_seleccionado = combo_metodo.get()
            nuevo_metodo_pago = 'efectivo' if '💵' in metodo_seleccionado else 'tarjeta'

            # Actualizar en la base de datos
            if self.db.actualizar_gasto(gasto_id, nueva_desc, nueva_cant, nueva_cat_id, nueva_fecha, nuevo_metodo_pago):
                messagebox.showinfo("Éxito", "Gasto actualizado correctamente")
                ventana.destroy()
                self.cargar_gastos()
            else:
                messagebox.showerror("Error", "No se pudo actualizar el gasto")

        # Botones
        btn_guardar = crear_boton_moderno(btn_frame, "💾 Guardar", guardar_cambios, 'success')
        btn_guardar.pack(side=tk.LEFT, padx=5)

        btn_cancelar = crear_boton_moderno(btn_frame, "✖ Cancelar", ventana.destroy, 'secondary')
        btn_cancelar.pack(side=tk.LEFT, padx=5)

    def editar_ingreso(self):
        """Edita el ingreso seleccionado."""
        seleccion = self.tree_ingresos.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un ingreso para editar")
            return

        # Obtener el ID del ingreso seleccionado
        item = self.tree_ingresos.item(seleccion[0])
        ingreso_id = item['values'][0]

        # Obtener los detalles del ingreso
        ingreso = self.db.obtener_ingreso_por_id(ingreso_id)
        if not ingreso:
            messagebox.showerror("Error", "No se pudo obtener la información del ingreso")
            return

        # Crear ventana de edición
        self.ventana_editar_ingreso(ingreso)

    def ventana_editar_ingreso(self, ingreso):
        """
        Muestra una ventana emergente para editar un ingreso.

        Args:
            ingreso: Tupla (id, descripcion, cantidad, fuente, fecha, mes, anio)
        """
        ingreso_id, descripcion, cantidad, fuente, fecha, mes, anio = ingreso

        # Crear ventana emergente
        ventana = tk.Toplevel(self.frame.winfo_toplevel())
        ventana.title("Editar Ingreso")
        ventana.geometry("450x350")
        ventana.configure(bg=COLORES['fondo_tarjeta'])
        ventana.transient(self.frame.winfo_toplevel())
        ventana.grab_set()

        # Título
        tk.Label(
            ventana,
            text="✏️ Editar Ingreso",
            font=('SF Pro Display', 16, 'bold'),
            bg=COLORES['fondo_tarjeta'],
            fg=COLORES['texto_primario']
        ).pack(pady=15)

        # Frame del formulario
        form = tk.Frame(ventana, bg=COLORES['fondo_tarjeta'])
        form.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)

        # Descripción
        tk.Label(form, text="Descripción:", font=('SF Pro Display', 10),
                bg=COLORES['fondo_tarjeta'], fg=COLORES['texto_secundario']).grid(
            row=0, column=0, sticky=tk.W, pady=(10, 5))

        entry_desc = tk.Entry(form, font=('SF Pro Display', 10), width=30,
                             bg=COLORES['fondo_input'], fg=COLORES['texto_primario'])
        entry_desc.grid(row=0, column=1, pady=(10, 5), sticky=tk.EW)
        entry_desc.insert(0, descripcion)

        # Cantidad
        tk.Label(form, text="Cantidad (€):", font=('SF Pro Display', 10),
                bg=COLORES['fondo_tarjeta'], fg=COLORES['texto_secundario']).grid(
            row=1, column=0, sticky=tk.W, pady=5)

        entry_cant = tk.Entry(form, font=('SF Pro Display', 10), width=30,
                             bg=COLORES['fondo_input'], fg=COLORES['texto_primario'])
        entry_cant.grid(row=1, column=1, pady=5, sticky=tk.EW)
        entry_cant.insert(0, str(cantidad))

        # Fuente
        tk.Label(form, text="Fuente:", font=('SF Pro Display', 10),
                bg=COLORES['fondo_tarjeta'], fg=COLORES['texto_secundario']).grid(
            row=2, column=0, sticky=tk.W, pady=5)

        entry_fuente = tk.Entry(form, font=('SF Pro Display', 10), width=30,
                               bg=COLORES['fondo_input'], fg=COLORES['texto_primario'])
        entry_fuente.grid(row=2, column=1, pady=5, sticky=tk.EW)
        entry_fuente.insert(0, fuente)

        # Fecha
        tk.Label(form, text="Fecha:", font=('SF Pro Display', 10),
                bg=COLORES['fondo_tarjeta'], fg=COLORES['texto_secundario']).grid(
            row=3, column=0, sticky=tk.W, pady=5)

        # Widget de calendario para editar ingreso
        try:
            from .calendario import BotonCalendario
        except ImportError:
            from calendario import BotonCalendario

        fecha_calendario_ingreso = BotonCalendario(
            form,
            fecha_inicial=fecha,
            bg=COLORES['fondo_tarjeta']
        )
        fecha_calendario_ingreso.grid(row=3, column=1, pady=5, sticky=tk.W)

        form.columnconfigure(1, weight=1)

        # Frame para botones
        btn_frame = tk.Frame(ventana, bg=COLORES['fondo_tarjeta'])
        btn_frame.pack(pady=20)

        try:
            from .estilos import crear_boton_moderno
        except ImportError:
            from estilos import crear_boton_moderno

        def guardar_cambios():
            # Validar
            nueva_desc = entry_desc.get().strip()
            nueva_cant_str = entry_cant.get().strip()
            nueva_fuente = entry_fuente.get()
            nueva_fecha = fecha_calendario_ingreso.obtener_fecha()

            if not nueva_desc or not nueva_cant_str or not nueva_fuente:
                messagebox.showerror("Error", "Todos los campos son obligatorios")
                return

            try:
                nueva_cant = float(nueva_cant_str)
                if nueva_cant <= 0:
                    raise ValueError()
            except ValueError:
                messagebox.showerror("Error", "La cantidad debe ser un número positivo")
                return

            # Validar fecha
            try:
                datetime.strptime(nueva_fecha, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Error", "Fecha inválida")
                return

            # Actualizar en la base de datos
            if self.db.actualizar_ingreso(ingreso_id, nueva_desc, nueva_cant, nueva_fuente, nueva_fecha):
                messagebox.showinfo("Éxito", "Ingreso actualizado correctamente")
                ventana.destroy()
                self.cargar_ingresos()
            else:
                messagebox.showerror("Error", "No se pudo actualizar el ingreso")

        # Botones
        btn_guardar = crear_boton_moderno(btn_frame, "💾 Guardar", guardar_cambios, 'success')
        btn_guardar.pack(side=tk.LEFT, padx=5)

        btn_cancelar = crear_boton_moderno(btn_frame, "✖ Cancelar", ventana.destroy, 'secondary')
        btn_cancelar.pack(side=tk.LEFT, padx=5)

    def cambiar_anio(self, nuevo_anio: int):
        """
        Cambia el año de la vista.

        Args:
            nuevo_anio: Nuevo año
        """
        self.anio = nuevo_anio

        # Actualizar componentes de calendario para gastos
        if hasattr(self, 'fecha_gasto'):
            valores_gasto = self.fecha_gasto.obtener_valores()
            self.fecha_gasto.establecer_valores(valores_gasto['dia'], valores_gasto['mes'], nuevo_anio)

        # Actualizar componentes de calendario para ingresos
        if hasattr(self, 'fecha_ingreso'):
            valores_ingreso = self.fecha_ingreso.obtener_valores()
            self.fecha_ingreso.establecer_valores(valores_ingreso['dia'], valores_ingreso['mes'], nuevo_anio)

        self.cargar_gastos()
        self.cargar_ingresos()


class VistaComparacionAnual:
    """Vista para comparar los gastos de todos los meses del año."""

    def __init__(self, parent, db, anio: int):
        """
        Inicializa la vista de comparación anual.

        Args:
            parent: Widget padre
            db: Instancia de la base de datos
            anio: Año
        """
        self.db = db
        self.anio = anio

        # Frame principal con fondo
        self.frame = tk.Frame(parent, bg=COLORES['fondo'])

        # Crear interfaz
        self.crear_interfaz()

        # Cargar datos
        self.cargar_datos()

    def crear_interfaz(self):
        """Crea la interfaz de la vista de comparación."""
        # Frame de título
        frame_titulo = ttk.Frame(self.frame)
        frame_titulo.pack(fill=tk.X, padx=10, pady=10)

        titulo = ttk.Label(
            frame_titulo,
            text="📊 Comparación Anual: Ingresos vs Gastos",
            font=('Arial', 14, 'bold')
        )
        titulo.pack()

        # Frame de tabla
        frame_tabla = ttk.Frame(self.frame)
        frame_tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Crear Treeview con columnas para ingresos, gastos y balance
        columnas = ("Mes", "Ingresos", "Gastos", "Balance", "Estado")
        self.tree = ttk.Treeview(
            frame_tabla,
            columns=columnas,
            show="headings",
            height=15
        )

        self.tree.heading("Mes", text="Mes")
        self.tree.heading("Ingresos", text="Ingresos (€)")
        self.tree.heading("Gastos", text="Gastos (€)")
        self.tree.heading("Balance", text="Balance (€)")
        self.tree.heading("Estado", text="Estado")

        self.tree.column("Mes", width=150, anchor=tk.CENTER)
        self.tree.column("Ingresos", width=150, anchor=tk.E)
        self.tree.column("Gastos", width=150, anchor=tk.E)
        self.tree.column("Balance", width=150, anchor=tk.E)
        self.tree.column("Estado", width=150, anchor=tk.CENTER)

        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configurar tags para colores
        self.tree.tag_configure('positivo', foreground='green', font=('Arial', 10, 'bold'))
        self.tree.tag_configure('negativo', foreground='red', font=('Arial', 10, 'bold'))
        self.tree.tag_configure('cero', foreground='gray')

        # Frame de totales anuales
        frame_totales = ttk.Frame(self.frame)
        frame_totales.pack(fill=tk.X, padx=10, pady=10)

        # Totales anuales en una fila
        frame_totales_row = ttk.Frame(frame_totales)
        frame_totales_row.pack(pady=5)

        self.label_total_ingresos_anual = ttk.Label(
            frame_totales_row,
            text="Total Ingresos: €0.00",
            font=('Arial', 12, 'bold'),
            foreground='green'
        )
        self.label_total_ingresos_anual.pack(side=tk.LEFT, padx=20)

        self.label_total_gastos_anual = ttk.Label(
            frame_totales_row,
            text="Total Gastos: €0.00",
            font=('Arial', 12, 'bold'),
            foreground='red'
        )
        self.label_total_gastos_anual.pack(side=tk.LEFT, padx=20)

        self.label_balance_anual = ttk.Label(
            frame_totales_row,
            text="Balance Anual: €0.00",
            font=('Arial', 14, 'bold'),
            foreground='blue'
        )
        self.label_balance_anual.pack(side=tk.LEFT, padx=20)

        # Promedios mensuales
        frame_promedios = ttk.Frame(frame_totales)
        frame_promedios.pack(pady=5)

        self.label_promedio_ingresos = ttk.Label(
            frame_promedios,
            text="Promedio Ingresos/mes: €0.00",
            font=('Arial', 10),
            foreground='green'
        )
        self.label_promedio_ingresos.pack(side=tk.LEFT, padx=20)

        self.label_promedio_gastos = ttk.Label(
            frame_promedios,
            text="Promedio Gastos/mes: €0.00",
            font=('Arial', 10),
            foreground='red'
        )
        self.label_promedio_gastos.pack(side=tk.LEFT, padx=20)

        self.label_promedio_balance = ttk.Label(
            frame_promedios,
            text="Promedio Balance/mes: €0.00",
            font=('Arial', 10),
            foreground='blue'
        )
        self.label_promedio_balance.pack(side=tk.LEFT, padx=20)

        # Frame de gastos por método de pago
        frame_metodos = ttk.LabelFrame(self.frame, text="Distribución por Método de Pago")
        frame_metodos.pack(fill=tk.X, padx=10, pady=10)

        frame_metodos_content = ttk.Frame(frame_metodos)
        frame_metodos_content.pack(pady=10)

        self.label_efectivo = ttk.Label(
            frame_metodos_content,
            text="💵 Efectivo: €0.00 (0%)",
            font=('Arial', 11, 'bold'),
            foreground='#2E7D32'
        )
        self.label_efectivo.pack(side=tk.LEFT, padx=30)

        self.label_tarjeta = ttk.Label(
            frame_metodos_content,
            text="💳 Tarjeta: €0.00 (0%)",
            font=('Arial', 11, 'bold'),
            foreground='#1976D2'
        )
        self.label_tarjeta.pack(side=tk.LEFT, padx=30)

        # Cargar datos iniciales
        self.cargar_datos()

    def cargar_datos(self):
        """Carga los datos de comparación anual con ingresos, gastos y balance."""
        # Limpiar tree
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Nombres de meses
        meses_nombres = [
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ]

        # Obtener datos de ingresos y gastos
        comparacion_gastos = self.db.obtener_comparacion_anual(self.anio)
        comparacion_ingresos = self.db.obtener_comparacion_ingresos_anual(self.anio)

        # Crear diccionarios
        gastos_por_mes = {mes: 0.0 for mes in range(1, 13)}
        ingresos_por_mes = {mes: 0.0 for mes in range(1, 13)}

        for mes, total in comparacion_gastos:
            gastos_por_mes[mes] = total

        for mes, total in comparacion_ingresos:
            ingresos_por_mes[mes] = total

        # Variables para totales anuales
        total_ingresos_anual = 0.0
        total_gastos_anual = 0.0
        meses_con_datos = 0

        # Agregar cada mes al tree
        for mes in range(1, 13):
            ingresos = ingresos_por_mes[mes]
            gastos = gastos_por_mes[mes]
            balance = ingresos - gastos

            # Determinar estado y tag
            if balance > 0:
                estado = "✅ Ahorro"
                tag = 'positivo'
            elif balance < 0:
                estado = "⚠️ Déficit"
                tag = 'negativo'
            else:
                estado = "➖ Neutro"
                tag = 'cero'

            # Insertar fila
            self.tree.insert(
                "",
                tk.END,
                values=(
                    meses_nombres[mes - 1],
                    f"{ingresos:.2f}",
                    f"{gastos:.2f}",
                    f"{balance:+.2f}",  # El + muestra el signo
                    estado
                ),
                tags=(tag,)
            )

            # Acumular totales
            total_ingresos_anual += ingresos
            total_gastos_anual += gastos

            # Contar meses con datos
            if ingresos > 0 or gastos > 0:
                meses_con_datos += 1

        # Calcular balance anual
        balance_anual = total_ingresos_anual - total_gastos_anual

        # Actualizar labels de totales anuales
        self.label_total_ingresos_anual.config(
            text=f"Total Ingresos Anual: €{total_ingresos_anual:.2f}"
        )
        self.label_total_gastos_anual.config(
            text=f"Total Gastos Anual: €{total_gastos_anual:.2f}"
        )

        # Balance anual con color
        color_balance = 'green' if balance_anual >= 0 else 'red'
        signo = "+" if balance_anual >= 0 else ""
        self.label_balance_anual.config(
            text=f"Balance Anual: {signo}€{balance_anual:.2f}",
            foreground=color_balance
        )

        # Calcular promedios (dividir entre 12 o meses con datos)
        divisor = max(meses_con_datos, 1)  # Evitar división por cero
        promedio_ingresos = total_ingresos_anual / divisor
        promedio_gastos = total_gastos_anual / divisor
        promedio_balance = balance_anual / divisor

        self.label_promedio_ingresos.config(
            text=f"Promedio Ingresos/mes: €{promedio_ingresos:.2f}"
        )
        self.label_promedio_gastos.config(
            text=f"Promedio Gastos/mes: €{promedio_gastos:.2f}"
        )

        color_promedio = 'green' if promedio_balance >= 0 else 'red'
        self.label_promedio_balance.config(
            text=f"Promedio Balance/mes: €{promedio_balance:+.2f}",
            foreground=color_promedio
        )

        # Calcular distribución por método de pago
        metodos_pago = self.db.obtener_gastos_por_metodo_anual(self.anio)

        total_efectivo = metodos_pago.get('efectivo', 0.0)
        total_tarjeta = metodos_pago.get('tarjeta', 0.0)

        # Actualizar labels de métodos de pago
        total_gastos = total_efectivo + total_tarjeta
        porcentaje_efectivo = (total_efectivo / total_gastos * 100) if total_gastos > 0 else 0
        porcentaje_tarjeta = (total_tarjeta / total_gastos * 100) if total_gastos > 0 else 0

        self.label_efectivo.config(
            text=f"💵 Efectivo: €{total_efectivo:.2f} ({porcentaje_efectivo:.1f}%)"
        )
        self.label_tarjeta.config(
            text=f"💳 Tarjeta: €{total_tarjeta:.2f} ({porcentaje_tarjeta:.1f}%)"
        )

    def cambiar_anio(self, nuevo_anio: int):
        """
        Cambia el año de la vista.

        Args:
            nuevo_anio: Nuevo año
        """
        self.anio = nuevo_anio
        self.cargar_datos()



class VistaEstadisticas:
    """Vista para mostrar estadísticas detalladas de los gastos."""

    def __init__(self, parent, db, anio: int):
        """
        Inicializa la vista de estadísticas.

        Args:
            parent: Widget padre
            db: Instancia de la base de datos
            anio: Año
        """
        self.db = db
        self.anio = anio

        # Frame principal con fondo
        self.frame = tk.Frame(parent, bg=COLORES['fondo'])

        # Crear interfaz
        self.crear_interfaz()

        # Cargar datos
        self.cargar_datos()

    def crear_interfaz(self):
        """Crea la interfaz de la vista de estadísticas."""
        # Frame de título
        frame_titulo = ttk.Frame(self.frame)
        frame_titulo.pack(fill=tk.X, padx=10, pady=10)

        titulo = ttk.Label(
            frame_titulo,
            text="📈 Estadísticas por Categoría",
            font=('Arial', 14, 'bold')
        )
        titulo.pack()

        # Selector de mes
        frame_selector = ttk.Frame(self.frame)
        frame_selector.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(frame_selector, text="Ver estadísticas de:").pack(side=tk.LEFT, padx=5)

        meses_opciones = ["Todo el Año"] + [
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ]

        self.combo_mes = ttk.Combobox(
            frame_selector,
            values=meses_opciones,
            width=20,
            state='readonly'
        )
        self.combo_mes.current(0)
        self.combo_mes.pack(side=tk.LEFT, padx=5)
        self.combo_mes.bind('<<ComboboxSelected>>', lambda e: self.cargar_datos())

        # Frame de tabla
        frame_tabla = ttk.Frame(self.frame)
        frame_tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Crear Treeview
        columnas = ("Categoría", "Total", "Porcentaje", "Cantidad")
        self.tree = ttk.Treeview(
            frame_tabla,
            columns=columnas,
            show="headings",
            height=12
        )

        self.tree.heading("Categoría", text="Categoría")
        self.tree.heading("Total", text="Total Gastado (€)")
        self.tree.heading("Porcentaje", text="% del Total")
        self.tree.heading("Cantidad", text="Nº Gastos")

        self.tree.column("Categoría", width=200)
        self.tree.column("Total", width=200, anchor=tk.E)
        self.tree.column("Porcentaje", width=150, anchor=tk.CENTER)
        self.tree.column("Cantidad", width=150, anchor=tk.CENTER)

        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Agregar evento de doble clic para mostrar detalles
        self.tree.bind('<Double-Button-1>', self.mostrar_detalles_categoria)

        # Etiqueta de ayuda
        label_ayuda = ttk.Label(
            self.frame,
            text="💡 Haz doble clic en una categoría para ver los gastos desglosados",
            font=('Arial', 9, 'italic'),
            foreground='#666'
        )
        label_ayuda.pack(pady=5)

        # Frame de información adicional
        frame_info = ttk.LabelFrame(self.frame, text="Información Adicional", padding="10")
        frame_info.pack(fill=tk.X, padx=10, pady=10)

        self.label_categoria_mayor = ttk.Label(
            frame_info,
            text="Categoría con mayor gasto: -",
            font=('Arial', 11)
        )
        self.label_categoria_mayor.pack(pady=3)

        self.label_categoria_menor = ttk.Label(
            frame_info,
            text="Categoría con menor gasto: -",
            font=('Arial', 11)
        )
        self.label_categoria_menor.pack(pady=3)

    def cargar_datos(self):
        """Carga las estadísticas por categoría."""
        # Limpiar tree
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Determinar mes seleccionado
        seleccion = self.combo_mes.get()

        if seleccion == "Todo el Año":
            # Obtener estadísticas de todo el año
            estadisticas = self.obtener_estadisticas_anuales()
        else:
            # Obtener mes
            meses_nombres = [
                "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
            ]
            mes = meses_nombres.index(seleccion) + 1
            estadisticas = self.obtener_estadisticas_mensuales(mes)

        # Calcular total
        total_general = sum(stat['total'] for stat in estadisticas)

        # Agregar al tree
        categoria_mayor = None
        categoria_menor = None
        mayor_gasto = 0
        menor_gasto = float('inf')

        for stat in estadisticas:
            porcentaje = (stat['total'] / total_general * 100) if total_general > 0 else 0

            self.tree.insert(
                "",
                tk.END,
                values=(
                    stat['categoria'],
                    f"{stat['total']:.2f}",
                    f"{porcentaje:.1f}%",
                    stat['cantidad']
                )
            )

            # Determinar mayor y menor
            if stat['total'] > mayor_gasto:
                mayor_gasto = stat['total']
                categoria_mayor = stat['categoria']

            if stat['total'] > 0 and stat['total'] < menor_gasto:
                menor_gasto = stat['total']
                categoria_menor = stat['categoria']

        # Actualizar etiquetas
        if categoria_mayor:
            self.label_categoria_mayor.config(
                text=f"Categoría con mayor gasto: {categoria_mayor} (€{mayor_gasto:.2f})"
            )
        else:
            self.label_categoria_mayor.config(text="Categoría con mayor gasto: -")

        if categoria_menor and categoria_menor != categoria_mayor:
            self.label_categoria_menor.config(
                text=f"Categoría con menor gasto: {categoria_menor} (€{menor_gasto:.2f})"
            )
        else:
            self.label_categoria_menor.config(text="Categoría con menor gasto: -")

    def obtener_estadisticas_anuales(self):
        """Obtiene estadísticas de todas las categorías para el año completo."""
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT c.nombre, SUM(g.cantidad) as total, COUNT(g.id) as cantidad
            FROM categorias c
            LEFT JOIN gastos g ON c.id = g.categoria_id AND g.anio = ?
            GROUP BY c.nombre
            HAVING total > 0
            ORDER BY total DESC
        ''', (self.anio,))

        resultados = cursor.fetchall()
        conn.close()

        return [
            {'categoria': cat, 'total': total, 'cantidad': cantidad}
            for cat, total, cantidad in resultados
        ]

    def obtener_estadisticas_mensuales(self, mes: int):
        """Obtiene estadísticas de todas las categorías para un mes específico."""
        conn = self.db.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT c.nombre, SUM(g.cantidad) as total, COUNT(g.id) as cantidad
            FROM categorias c
            LEFT JOIN gastos g ON c.id = g.categoria_id 
                AND g.mes = ? AND g.anio = ?
            GROUP BY c.nombre
            HAVING total > 0
            ORDER BY total DESC
        ''', (mes, self.anio))

        resultados = cursor.fetchall()
        conn.close()

        return [
            {'categoria': cat, 'total': total, 'cantidad': cantidad}
            for cat, total, cantidad in resultados
        ]

    def cambiar_anio(self, nuevo_anio: int):
        """
        Cambia el año de la vista.

        Args:
            nuevo_anio: Nuevo año
        """
        self.anio = nuevo_anio
        self.cargar_datos()

    def mostrar_detalles_categoria(self, event):
        """
        Muestra un pop-up con los gastos desglosados de la categoría seleccionada.

        Args:
            event: Evento de doble clic
        """
        # Obtener item seleccionado
        seleccion = self.tree.selection()
        if not seleccion:
            return

        # Obtener datos del item
        item = self.tree.item(seleccion[0])
        categoria_nombre = item['values'][0]
        total_categoria = item['values'][1]

        # Determinar mes seleccionado
        seleccion_mes = self.combo_mes.get()
        mes = None

        if seleccion_mes != "Todo el Año":
            meses_nombres = [
                "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
            ]
            mes = meses_nombres.index(seleccion_mes) + 1

        # Obtener gastos detallados
        gastos_detallados = self.db.obtener_gastos_detallados_categoria(
            categoria_nombre, mes, self.anio
        )

        # Crear ventana popup
        popup = tk.Toplevel(self.frame)
        popup.title(f"Gastos Detallados - {categoria_nombre}")
        popup.geometry("700x500")

        # Frame de título
        frame_titulo = ttk.Frame(popup, padding="10")
        frame_titulo.pack(fill=tk.X)

        titulo_texto = f"📋 Gastos de {categoria_nombre}"
        if seleccion_mes != "Todo el Año":
            titulo_texto += f" - {seleccion_mes}"
        titulo_texto += f" {self.anio}"

        ttk.Label(
            frame_titulo,
            text=titulo_texto,
            font=('Arial', 14, 'bold')
        ).pack()

        ttk.Label(
            frame_titulo,
            text=f"Total: €{total_categoria}",
            font=('Arial', 12),
            foreground='#d32f2f'
        ).pack(pady=5)

        # Frame de tabla
        frame_tabla = ttk.Frame(popup, padding="10")
        frame_tabla.pack(fill=tk.BOTH, expand=True)

        # Crear Treeview para los detalles
        columnas = ("Fecha", "Descripción", "Método", "Cantidad", "Mes")
        tree_detalle = ttk.Treeview(
            frame_tabla,
            columns=columnas,
            show="headings",
            height=15
        )

        tree_detalle.heading("Fecha", text="Fecha")
        tree_detalle.heading("Descripción", text="Descripción")
        tree_detalle.heading("Método", text="Método")
        tree_detalle.heading("Cantidad", text="Cantidad (€)")
        tree_detalle.heading("Mes", text="Mes")

        tree_detalle.column("Fecha", width=100, anchor=tk.CENTER)
        tree_detalle.column("Descripción", width=250)
        tree_detalle.column("Método", width=90, anchor=tk.CENTER)
        tree_detalle.column("Cantidad", width=100, anchor=tk.E)
        tree_detalle.column("Mes", width=100, anchor=tk.CENTER)

        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL, command=tree_detalle.yview)
        tree_detalle.configure(yscrollcommand=scrollbar.set)

        tree_detalle.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Nombres de meses para mostrar
        meses_nombres = [
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ]

        # Agregar gastos al tree
        if gastos_detallados:
            for gasto in gastos_detallados:
                # Manejar ambos formatos: con y sin metodo_pago
                if len(gasto) == 6:
                    gasto_id, descripcion, cantidad, fecha, mes_num, metodo_pago = gasto
                else:
                    gasto_id, descripcion, cantidad, fecha, mes_num = gasto
                    metodo_pago = 'tarjeta'  # Valor por defecto

                mes_texto = meses_nombres[mes_num - 1] if mes_num else ""

                # Mostrar icono según método de pago
                metodo_texto = "💵 Efectivo" if metodo_pago == 'efectivo' else "💳 Tarjeta"

                tree_detalle.insert(
                    "",
                    tk.END,
                    values=(
                        fecha,
                        descripcion,
                        metodo_texto,
                        f"{cantidad:.2f}",
                        mes_texto
                    )
                )
        else:
            # Mostrar mensaje si no hay gastos
            ttk.Label(
                frame_tabla,
                text="No hay gastos registrados para esta categoría",
                font=('Arial', 11, 'italic'),
                foreground='#999'
            ).pack(pady=20)

        # Frame de botones
        frame_botones = ttk.Frame(popup, padding="10")
        frame_botones.pack(fill=tk.X)

        ttk.Button(
            frame_botones,
            text="Cerrar",
            command=popup.destroy
        ).pack(side=tk.RIGHT, padx=5)

        # Centrar la ventana
        popup.transient(self.frame.winfo_toplevel())
        popup.grab_set()


class VistaGestionCategorias:
    """Vista para gestionar las categorías (agregar, editar, eliminar)."""

    def __init__(self, parent, db):
        """
        Inicializa la vista de gestión de categorías.

        Args:
            parent: Widget padre
            db: Instancia de la base de datos
        """
        self.db = db

        # Frame principal con fondo
        self.frame = tk.Frame(parent, bg=COLORES['fondo'])

        # Crear interfaz
        self.crear_interfaz()

        # Cargar categorías
        self.cargar_categorias()

    def crear_interfaz(self):
        """Crea la interfaz de gestión de categorías."""

        # Título
        titulo_frame = tk.Frame(self.frame, bg=COLORES['fondo'])
        titulo_frame.pack(fill=tk.X, padx=20, pady=(20, 10))

        tk.Label(
            titulo_frame,
            text="🏷️ Gestión de Categorías",
            font=('SF Pro Display', 24, 'bold'),
            bg=COLORES['fondo'],
            fg=COLORES['texto_primario']
        ).pack(side=tk.LEFT)

        # Botón para agregar nueva categoría
        btn_nueva = crear_boton_moderno(
            titulo_frame,
            "➕ Nueva Categoría",
            self.ventana_nueva_categoria,
            'success'
        )
        btn_nueva.pack(side=tk.RIGHT, padx=5)

        # Frame de tabla
        frame_tabla = tk.Frame(self.frame, bg=COLORES['fondo'])
        frame_tabla.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Crear Treeview para mostrar categorías
        columnas = ("ID", "Nombre", "Descripción", "Gastos")
        self.tree = ttk.Treeview(
            frame_tabla,
            columns=columnas,
            show="headings",
            height=15
        )

        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Descripción", text="Descripción")
        self.tree.heading("Gastos", text="Gastos Asociados")

        self.tree.column("ID", width=50, anchor=tk.CENTER)
        self.tree.column("Nombre", width=150, anchor=tk.W)
        self.tree.column("Descripción", width=300, anchor=tk.W)
        self.tree.column("Gastos", width=120, anchor=tk.CENTER)

        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Frame de botones de acción
        frame_botones = tk.Frame(self.frame, bg=COLORES['fondo'])
        frame_botones.pack(fill=tk.X, padx=20, pady=(10, 20))

        btn_editar = crear_boton_moderno(
            frame_botones,
            "✏️ Editar",
            self.editar_categoria,
            'primary'
        )
        btn_editar.pack(side=tk.LEFT, padx=5)

        btn_eliminar = crear_boton_moderno(
            frame_botones,
            "🗑️ Eliminar",
            self.eliminar_categoria,
            'danger'
        )
        btn_eliminar.pack(side=tk.LEFT, padx=5)

        # Info
        info_frame = tk.Frame(self.frame, bg=COLORES['fondo_tarjeta'], relief=tk.RIDGE, bd=1)
        info_frame.pack(fill=tk.X, padx=20, pady=(0, 20))

        tk.Label(
            info_frame,
            text="ℹ️ Nota: Solo se pueden eliminar categorías sin gastos asociados",
            font=('SF Pro Display', 10),
            bg=COLORES['fondo_tarjeta'],
            fg=COLORES['texto_secundario'],
            pady=10
        ).pack()

    def cargar_categorias(self):
        """Carga las categorías en el Treeview."""
        # Limpiar tree
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Obtener categorías
        categorias = self.db.obtener_categorias()

        # Obtener cantidad de gastos por categoría
        conn = self.db.get_connection()
        cursor = conn.cursor()

        for cat_id, nombre, descripcion in categorias:
            # Contar gastos asociados
            cursor.execute('SELECT COUNT(*) FROM gastos WHERE categoria_id = ?', (cat_id,))
            count = cursor.fetchone()[0]

            self.tree.insert(
                "",
                tk.END,
                values=(
                    cat_id,
                    nombre,
                    descripcion or "(Sin descripción)",
                    count
                )
            )

        conn.close()

    def ventana_nueva_categoria(self):
        """Abre una ventana para agregar una nueva categoría."""
        ventana = tk.Toplevel(self.frame.winfo_toplevel())
        ventana.title("Nueva Categoría")
        ventana.geometry("450x320")
        ventana.configure(bg=COLORES['fondo_tarjeta'])
        ventana.transient(self.frame.winfo_toplevel())
        ventana.grab_set()

        # Título
        tk.Label(
            ventana,
            text="➕ Nueva Categoría",
            font=('SF Pro Display', 16, 'bold'),
            bg=COLORES['fondo_tarjeta'],
            fg=COLORES['texto_primario']
        ).pack(pady=15)

        # Frame del formulario
        form_frame = tk.Frame(ventana, bg=COLORES['fondo_tarjeta'])
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Nombre
        tk.Label(
            form_frame,
            text="Nombre:",
            font=('SF Pro Display', 11),
            bg=COLORES['fondo_tarjeta'],
            fg=COLORES['texto_primario']
        ).pack(anchor=tk.W, pady=(0, 5))

        entry_nombre = tk.Entry(
            form_frame,
            font=('SF Pro Display', 11),
            bg='white',
            fg='#1A202C',  # Gris muy oscuro, casi negro
            relief=tk.FLAT,
            bd=0,
            highlightthickness=1,
            highlightbackground=COLORES['borde'],
            highlightcolor=COLORES['primario'],
            insertbackground='#1A202C'  # Color del cursor
        )
        entry_nombre.pack(fill=tk.X, pady=(0, 15), ipady=8)

        # Descripción
        tk.Label(
            form_frame,
            text="Descripción:",
            font=('SF Pro Display', 11),
            bg=COLORES['fondo_tarjeta'],
            fg=COLORES['texto_primario']
        ).pack(anchor=tk.W, pady=(0, 5))

        entry_descripcion = tk.Entry(
            form_frame,
            font=('SF Pro Display', 11),
            bg='white',
            fg='#1A202C',  # Gris muy oscuro, casi negro
            relief=tk.FLAT,
            bd=0,
            highlightthickness=1,
            highlightbackground=COLORES['borde'],
            highlightcolor=COLORES['primario'],
            insertbackground='#1A202C'  # Color del cursor
        )
        entry_descripcion.pack(fill=tk.X, pady=(0, 15), ipady=8)

        def guardar():
            nombre = entry_nombre.get().strip()
            descripcion = entry_descripcion.get().strip()

            if not nombre:
                messagebox.showerror("Error", "El nombre es obligatorio")
                return

            if self.db.agregar_categoria(nombre, descripcion):
                messagebox.showinfo("Éxito", "Categoría agregada correctamente")
                self.cargar_categorias()
                ventana.destroy()
            else:
                messagebox.showerror("Error", "No se pudo agregar la categoría. Es posible que ya exista.")

        # Botones
        btn_frame = tk.Frame(ventana, bg=COLORES['fondo_tarjeta'])
        btn_frame.pack(fill=tk.X, padx=20, pady=(0, 15))

        btn_guardar = crear_boton_moderno(btn_frame, "💾 Guardar", guardar, 'success')
        btn_guardar.pack(side=tk.LEFT, padx=5)

        btn_cancelar = crear_boton_moderno(btn_frame, "✖ Cancelar", ventana.destroy, 'secondary')
        btn_cancelar.pack(side=tk.LEFT, padx=5)

    def editar_categoria(self):
        """Abre una ventana para editar la categoría seleccionada."""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona una categoría para editar")
            return

        # Obtener datos de la categoría seleccionada
        valores = self.tree.item(seleccion[0])['values']
        cat_id, nombre, descripcion, _ = valores

        # Si la descripción es el texto por defecto, ponerla vacía
        if descripcion == "(Sin descripción)":
            descripcion = ""

        # Crear ventana
        ventana = tk.Toplevel(self.frame.winfo_toplevel())
        ventana.title("Editar Categoría")
        ventana.geometry("450x320")
        ventana.configure(bg=COLORES['fondo_tarjeta'])
        ventana.transient(self.frame.winfo_toplevel())
        ventana.grab_set()

        # Título
        tk.Label(
            ventana,
            text="✏️ Editar Categoría",
            font=('SF Pro Display', 16, 'bold'),
            bg=COLORES['fondo_tarjeta'],
            fg=COLORES['texto_primario']
        ).pack(pady=15)

        # Frame del formulario
        form_frame = tk.Frame(ventana, bg=COLORES['fondo_tarjeta'])
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Nombre
        tk.Label(
            form_frame,
            text="Nombre:",
            font=('SF Pro Display', 11),
            bg=COLORES['fondo_tarjeta'],
            fg=COLORES['texto_primario']
        ).pack(anchor=tk.W, pady=(0, 5))

        entry_nombre = tk.Entry(
            form_frame,
            font=('SF Pro Display', 11),
            bg='white',
            fg='#1A202C',
            relief=tk.FLAT,
            bd=0,
            highlightthickness=1,
            highlightbackground=COLORES['borde'],
            highlightcolor=COLORES['primario'],
            insertbackground='#1A202C'
        )
        entry_nombre.insert(0, nombre)
        entry_nombre.pack(fill=tk.X, pady=(0, 15), ipady=8)

        # Descripción
        tk.Label(
            form_frame,
            text="Descripción:",
            font=('SF Pro Display', 11),
            bg=COLORES['fondo_tarjeta'],
            fg=COLORES['texto_primario']
        ).pack(anchor=tk.W, pady=(0, 5))

        entry_descripcion = tk.Entry(
            form_frame,
            font=('SF Pro Display', 11),
            bg='white',
            fg='#1A202C',
            relief=tk.FLAT,
            bd=0,
            highlightthickness=1,
            highlightbackground=COLORES['borde'],
            highlightcolor=COLORES['primario'],
            insertbackground='#1A202C'
        )
        entry_descripcion.insert(0, descripcion)
        entry_descripcion.pack(fill=tk.X, pady=(0, 15), ipady=8)

        def guardar():
            nuevo_nombre = entry_nombre.get().strip()
            nueva_descripcion = entry_descripcion.get().strip()

            if not nuevo_nombre:
                messagebox.showerror("Error", "El nombre es obligatorio")
                return

            if self.db.editar_categoria(cat_id, nuevo_nombre, nueva_descripcion):
                messagebox.showinfo("Éxito", "Categoría editada correctamente")
                self.cargar_categorias()
                ventana.destroy()
            else:
                messagebox.showerror("Error", "No se pudo editar la categoría. Es posible que el nombre ya exista.")

        # Botones
        btn_frame = tk.Frame(ventana, bg=COLORES['fondo_tarjeta'])
        btn_frame.pack(fill=tk.X, padx=20, pady=(0, 15))

        btn_guardar = crear_boton_moderno(btn_frame, "💾 Guardar", guardar, 'success')
        btn_guardar.pack(side=tk.LEFT, padx=5)

        btn_cancelar = crear_boton_moderno(btn_frame, "✖ Cancelar", ventana.destroy, 'secondary')
        btn_cancelar.pack(side=tk.LEFT, padx=5)

    def eliminar_categoria(self):
        """Elimina la categoría seleccionada."""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona una categoría para eliminar")
            return

        # Obtener datos de la categoría seleccionada
        valores = self.tree.item(seleccion[0])['values']
        cat_id, nombre, _, gastos_count = valores

        # Confirmar eliminación
        if gastos_count > 0:
            messagebox.showerror(
                "Error",
                f"No se puede eliminar la categoría '{nombre}' porque tiene {gastos_count} gasto(s) asociado(s).\n\n"
                "Primero debes eliminar o reasignar esos gastos."
            )
            return

        respuesta = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Estás seguro de que deseas eliminar la categoría '{nombre}'?"
        )

        if respuesta:
            if self.db.eliminar_categoria(cat_id):
                messagebox.showinfo("Éxito", "Categoría eliminada correctamente")
                self.cargar_categorias()
            else:
                messagebox.showerror("Error", "No se pudo eliminar la categoría")


class VistaAdministracion:
    """Vista del panel de administración (solo para admins)."""

    def __init__(self, parent, db):
        """
        Inicializa la vista de administración.

        Args:
            parent: Widget padre
            db: Instancia de la base de datos
        """
        self.db = db

        # Frame principal con fondo
        self.frame = tk.Frame(parent, bg=COLORES['fondo'])

        # Crear interfaz
        self.crear_interfaz()

        # Cargar datos
        self.cargar_datos()

    def crear_interfaz(self):
        """Crea la interfaz del panel de administración."""

        # Título
        titulo_frame = tk.Frame(self.frame, bg=COLORES['fondo'])
        titulo_frame.pack(fill=tk.X, padx=20, pady=(20, 10))

        tk.Label(
            titulo_frame,
            text="👨‍💼 Panel de Administración",
            font=('SF Pro Display', 24, 'bold'),
            bg=COLORES['fondo'],
            fg=COLORES['texto_primario']
        ).pack(side=tk.LEFT)

        # Botón refrescar
        btn_refrescar = crear_boton_moderno(
            titulo_frame,
            "🔄 Refrescar",
            self.cargar_datos,
            'primary'
        )
        btn_refrescar.pack(side=tk.RIGHT, padx=5)

        # Sección de estadísticas
        self.crear_seccion_estadisticas()

        # Tabla de usuarios
        self.crear_tabla_usuarios()

        # Botones de acción
        self.crear_botones_accion()

    def crear_seccion_estadisticas(self):
        """Crea la sección de estadísticas del sistema."""
        stats_frame = ttk.LabelFrame(self.frame, text="📊 Estadísticas del Sistema", padding="15")
        stats_frame.pack(fill=tk.X, padx=20, pady=10)

        # Contenedor para las tarjetas
        cards_frame = tk.Frame(stats_frame, bg=COLORES['fondo'])
        cards_frame.pack(fill=tk.X)

        # Tarjeta 1: Total de usuarios
        card1 = tk.Frame(cards_frame, bg=COLORES['fondo_tarjeta'], relief=tk.RIDGE, bd=1)
        card1.pack(side=tk.LEFT, padx=10, pady=5, fill=tk.BOTH, expand=True)

        tk.Label(
            card1,
            text="👥 Total Usuarios",
            font=('SF Pro Display', 11),
            bg=COLORES['fondo_tarjeta'],
            fg=COLORES['texto_secundario']
        ).pack(pady=(10, 5))

        self.label_total_usuarios = tk.Label(
            card1,
            text="0",
            font=('SF Pro Display', 28, 'bold'),
            bg=COLORES['fondo_tarjeta'],
            fg=COLORES['primario']
        )
        self.label_total_usuarios.pack(pady=(0, 10))

        # Tarjeta 2: Usuarios activos
        card2 = tk.Frame(cards_frame, bg=COLORES['fondo_tarjeta'], relief=tk.RIDGE, bd=1)
        card2.pack(side=tk.LEFT, padx=10, pady=5, fill=tk.BOTH, expand=True)

        tk.Label(
            card2,
            text="✅ Usuarios Activos",
            font=('SF Pro Display', 11),
            bg=COLORES['fondo_tarjeta'],
            fg=COLORES['texto_secundario']
        ).pack(pady=(10, 5))

        self.label_usuarios_activos = tk.Label(
            card2,
            text="0",
            font=('SF Pro Display', 28, 'bold'),
            bg=COLORES['fondo_tarjeta'],
            fg=COLORES['exito']
        )
        self.label_usuarios_activos.pack(pady=(0, 10))

        # Tarjeta 3: Administradores
        card3 = tk.Frame(cards_frame, bg=COLORES['fondo_tarjeta'], relief=tk.RIDGE, bd=1)
        card3.pack(side=tk.LEFT, padx=10, pady=5, fill=tk.BOTH, expand=True)

        tk.Label(
            card3,
            text="👨‍💼 Administradores",
            font=('SF Pro Display', 11),
            bg=COLORES['fondo_tarjeta'],
            fg=COLORES['texto_secundario']
        ).pack(pady=(10, 5))

        self.label_admins = tk.Label(
            card3,
            text="0",
            font=('SF Pro Display', 28, 'bold'),
            bg=COLORES['fondo_tarjeta'],
            fg=COLORES['advertencia']
        )
        self.label_admins.pack(pady=(0, 10))

        # Tarjeta 4: Registros recientes
        card4 = tk.Frame(cards_frame, bg=COLORES['fondo_tarjeta'], relief=tk.RIDGE, bd=1)
        card4.pack(side=tk.LEFT, padx=10, pady=5, fill=tk.BOTH, expand=True)

        tk.Label(
            card4,
            text="🆕 Últimos 30 días",
            font=('SF Pro Display', 11),
            bg=COLORES['fondo_tarjeta'],
            fg=COLORES['texto_secundario']
        ).pack(pady=(10, 5))

        self.label_registros_recientes = tk.Label(
            card4,
            text="0",
            font=('Arial', 28, 'bold'),
            bg=COLORES['fondo_tarjeta'],
            fg=COLORES['info']
        )
        self.label_registros_recientes.pack(pady=(0, 10))

    def crear_tabla_usuarios(self):
        """Crea la tabla de gestión de usuarios."""
        frame_tabla = tk.Frame(self.frame, bg=COLORES['fondo'])
        frame_tabla.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Título de sección
        tk.Label(
            frame_tabla,
            text="📋 Gestión de Usuarios",
            font=('SF Pro Display', 16, 'bold'),
            bg=COLORES['fondo'],
            fg=COLORES['texto_primario']
        ).pack(anchor=tk.W, pady=(0, 10))

        # Crear Treeview
        columnas = ("ID", "Nombre", "Email", "Rol", "Estado", "Registro", "Último Acceso")
        self.tree = ttk.Treeview(
            frame_tabla,
            columns=columnas,
            show="headings",
            height=12
        )

        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Rol", text="Rol")
        self.tree.heading("Estado", text="Estado")
        self.tree.heading("Registro", text="Fecha Registro")
        self.tree.heading("Último Acceso", text="Último Acceso")

        self.tree.column("ID", width=50, anchor=tk.CENTER)
        self.tree.column("Nombre", width=150, anchor=tk.W)
        self.tree.column("Email", width=200, anchor=tk.W)
        self.tree.column("Rol", width=80, anchor=tk.CENTER)
        self.tree.column("Estado", width=80, anchor=tk.CENTER)
        self.tree.column("Registro", width=150, anchor=tk.CENTER)
        self.tree.column("Último Acceso", width=150, anchor=tk.CENTER)

        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configurar colores para estados
        self.tree.tag_configure('admin', foreground='#FF6B35')
        self.tree.tag_configure('activo', foreground='#27AE60')
        self.tree.tag_configure('inactivo', foreground='#E74C3C')

    def crear_botones_accion(self):
        """Crea los botones de acción."""
        frame_botones = tk.Frame(self.frame, bg=COLORES['fondo'])
        frame_botones.pack(fill=tk.X, padx=20, pady=(10, 20))

        # Botón: Cambiar rol
        btn_cambiar_rol = crear_boton_moderno(
            frame_botones,
            "👨‍💼 Cambiar Rol",
            self.cambiar_rol,
            'primary'
        )
        btn_cambiar_rol.pack(side=tk.LEFT, padx=5)

        # Botón: Activar/Desactivar
        btn_toggle_estado = crear_boton_moderno(
            frame_botones,
            "🔄 Activar/Desactivar",
            self.toggle_estado_usuario,
            'secondary'
        )
        btn_toggle_estado.pack(side=tk.LEFT, padx=5)

        # Botón: Eliminar usuario
        btn_eliminar = crear_boton_moderno(
            frame_botones,
            "🗑️ Eliminar Usuario",
            self.eliminar_usuario,
            'danger'
        )
        btn_eliminar.pack(side=tk.LEFT, padx=5)

        # Info
        tk.Label(
            frame_botones,
            text="💡 Selecciona un usuario de la tabla para realizar acciones",
            font=('SF Pro Display', 10, 'italic'),
            bg=COLORES['fondo'],
            fg=COLORES['texto_secundario']
        ).pack(side=tk.RIGHT, padx=10)

    def cargar_datos(self):
        """Carga los datos de usuarios y estadísticas."""
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Obtener estadísticas
        stats = self.db.obtener_estadisticas_admin()

        # Actualizar labels de estadísticas
        self.label_total_usuarios.config(text=str(stats['total_usuarios']))
        self.label_usuarios_activos.config(text=str(stats['usuarios_activos']))
        self.label_admins.config(text=str(stats['total_admins']))
        self.label_registros_recientes.config(text=str(stats['registros_recientes']))

        # Obtener usuarios
        usuarios = self.db.obtener_todos_usuarios()

        # Agregar a la tabla
        for usuario in usuarios:
            user_id, nombre, email, rol, activo, fecha_registro, ultimo_acceso = usuario

            # Formatear datos
            estado = "✅ Activo" if activo else "❌ Inactivo"
            rol_texto = "👨‍💼 Admin" if rol == 'admin' else "👤 Usuario"

            # Formatear fechas
            try:
                fecha_reg = fecha_registro[:10] if fecha_registro else "N/A"
            except:
                fecha_reg = "N/A"

            try:
                ultimo_acc = ultimo_acceso[:16] if ultimo_acceso else "Nunca"
            except:
                ultimo_acc = "Nunca"

            # Determinar tag para color
            tag = 'admin' if rol == 'admin' else ('activo' if activo else 'inactivo')

            self.tree.insert(
                "",
                tk.END,
                values=(user_id, nombre, email, rol_texto, estado, fecha_reg, ultimo_acc),
                tags=(tag,)
            )

    def cambiar_rol(self):
        """Cambia el rol del usuario seleccionado."""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona un usuario de la tabla")
            return

        # Obtener datos del usuario seleccionado
        valores = self.tree.item(seleccion[0])['values']
        usuario_id, nombre, email, rol_actual = valores[0], valores[1], valores[2], valores[3]

        # Determinar nuevo rol
        rol_actual_str = 'admin' if '👨‍💼' in rol_actual else 'usuario'
        nuevo_rol = 'usuario' if rol_actual_str == 'admin' else 'admin'

        # Confirmar cambio
        mensaje = f"¿Cambiar el rol de '{nombre}' de {rol_actual_str} a {nuevo_rol}?"
        if not messagebox.askyesno("Confirmar Cambio de Rol", mensaje):
            return

        # Cambiar rol
        exito, msg = self.db.cambiar_rol_usuario(usuario_id, nuevo_rol)

        if exito:
            messagebox.showinfo("Éxito", msg)
            self.cargar_datos()
        else:
            messagebox.showerror("Error", msg)

    def toggle_estado_usuario(self):
        """Activa o desactiva el usuario seleccionado."""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona un usuario de la tabla")
            return

        # Obtener datos
        valores = self.tree.item(seleccion[0])['values']
        usuario_id, nombre, estado_actual = valores[0], valores[1], valores[4]

        # Determinar nuevo estado
        esta_activo = "✅" in estado_actual
        nuevo_estado = not esta_activo

        # Confirmar
        accion = "desactivar" if esta_activo else "activar"
        mensaje = f"¿Seguro que deseas {accion} la cuenta de '{nombre}'?"
        if not messagebox.askyesno(f"Confirmar {accion.capitalize()}", mensaje):
            return

        # Cambiar estado
        exito, msg = self.db.activar_desactivar_usuario(usuario_id, nuevo_estado)

        if exito:
            messagebox.showinfo("Éxito", msg)
            self.cargar_datos()
        else:
            messagebox.showerror("Error", msg)

    def eliminar_usuario(self):
        """Elimina el usuario seleccionado y todos sus datos."""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona un usuario de la tabla")
            return

        # Obtener datos
        valores = self.tree.item(seleccion[0])['values']
        usuario_id, nombre, email = valores[0], valores[1], valores[2]

        # Advertencia seria
        mensaje = (
            f"⚠️ ADVERTENCIA CRÍTICA ⚠️\n\n"
            f"Estás a punto de ELIMINAR PERMANENTEMENTE:\n"
            f"Usuario: {nombre}\n"
            f"Email: {email}\n\n"
            f"Esto eliminará:\n"
            f"• Todos los gastos del usuario\n"
            f"• Todos los ingresos del usuario\n"
            f"• Todas las categorías personalizadas\n"
            f"• La base de datos completa del usuario\n\n"
            f"⚠️ ESTA ACCIÓN NO SE PUEDE DESHACER ⚠️\n\n"
            f"¿Estás SEGURO de continuar?"
        )

        if not messagebox.askyesno("⚠️ CONFIRMAR ELIMINACIÓN", mensaje):
            return

        # Confirmación doble
        confirmacion = messagebox.askyesno(
            "Última Confirmación",
            f"Escribe el nombre del usuario para confirmar:\n\n"
            f"¿Eliminar definitivamente a '{nombre}'?"
        )

        if not confirmacion:
            messagebox.showinfo("Cancelado", "Eliminación cancelada")
            return

        # Eliminar usuario
        exito, msg = self.db.eliminar_usuario_admin(usuario_id)

        if exito:
            messagebox.showinfo("Usuario Eliminado", msg)
            self.cargar_datos()
        else:
            messagebox.showerror("Error", msg)
