"""
Módulo de autenticación y login para FinanzApp.
"""

import tkinter as tk
from tkinter import ttk, messagebox

try:
    from .database import Database
except ImportError:
    from database import Database


class VentanaLogin:
    """Ventana de login y registro de usuarios."""

    def __init__(self, root, on_login_success):
        """
        Inicializa la ventana de login.

        Args:
            root: Ventana principal de Tkinter
            on_login_success: Función callback al hacer login exitoso (recibe usuario_id, nombre)
        """
        self.root = root
        self.on_login_success = on_login_success
        self.db = Database()

        # Configurar ventana
        self.root.title("🔐 FinanzApp - Inicio de Sesión")
        self.root.geometry("500x720")
        self.root.configure(bg='#ecf0f1')
        self.centrar_ventana()

        # Variables
        self.mostrar_registro = False

        # Configurar estilos ttk (UNA SOLA VEZ)
        self.configurar_estilos()

        # Crear interfaz
        self.crear_interfaz()

    def centrar_ventana(self):
        """Centra la ventana en la pantalla."""
        self.root.update_idletasks()
        width = 500
        height = 900  # Aumentado para incluir todos los elementos
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def configurar_estilos(self):
        """Configura los estilos de los botones ttk para macOS."""
        style = ttk.Style()

        # Estilo para botón de login (azul)
        style.configure('Login.TButton',
            background='#3498db',
            foreground='#ffffff',
            borderwidth=0,
            focuscolor='none',
            padding=[20, 12],
            font=('Segoe UI', 12, 'bold'),
            relief='flat'
        )
        style.map('Login.TButton',
            background=[('active', '#2980b9'), ('pressed', '#21618c')],
            foreground=[('active', '#ffffff'), ('pressed', '#ffffff')]
        )

        # Estilo para botón de registro (verde)
        style.configure('Registro.TButton',
            background='#27ae60',
            foreground='#ffffff',
            borderwidth=0,
            focuscolor='none',
            padding=[20, 12],
            font=('Segoe UI', 11, 'bold'),
            relief='flat'
        )
        style.map('Registro.TButton',
            background=[('active', '#229954'), ('pressed', '#1e8449')],
            foreground=[('active', '#ffffff'), ('pressed', '#ffffff')]
        )

        # Estilo para botón de crear cuenta
        style.configure('CrearCuenta.TButton',
            background='#27ae60',
            foreground='#ffffff',
            borderwidth=0,
            focuscolor='none',
            padding=[20, 12],
            font=('Segoe UI', 12, 'bold'),
            relief='flat'
        )
        style.map('CrearCuenta.TButton',
            background=[('active', '#229954'), ('pressed', '#1e8449')],
            foreground=[('active', '#ffffff'), ('pressed', '#ffffff')]
        )

        # Estilo para botón secundario (volver)
        style.configure('Volver.TButton',
            background='#ecf0f1',
            foreground='#7f8c8d',
            borderwidth=0,
            focuscolor='none',
            padding=[10, 8],
            font=('Segoe UI', 10),
            relief='flat'
        )
        style.map('Volver.TButton',
            background=[('active', '#bdc3c7'), ('pressed', '#95a5a6')],
            foreground=[('active', '#2c3e50'), ('pressed', '#2c3e50')]
        )

    def crear_interfaz(self):
        """Crea la interfaz de login."""
        # Frame principal con fondo elegante
        main_frame = tk.Frame(self.root, bg='#F7FAFC')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)

        # Logo/Título con diseño minimalista
        titulo_frame = tk.Frame(main_frame, bg='#FFFFFF', height=120)
        titulo_frame.pack(fill=tk.X, pady=(0, 25))
        titulo_frame.pack_propagate(False)

        tk.Label(
            titulo_frame,
            text="FinanzApp",
            font=('SF Pro Display', 32, 'bold'),
            bg='#FFFFFF',
            fg='#4A5568'
        ).pack(pady=(20, 5))

        tk.Label(
            titulo_frame,
            text="Gestión de Finanzas Personales",
            font=('SF Pro Display', 12),
            bg='#FFFFFF',
            fg='#A0AEC0'
        ).pack()

        # Contenedor para login/registro con borde sutil
        self.form_frame = tk.Frame(
            main_frame,
            bg='#FFFFFF',
            relief='flat',
            highlightthickness=1,
            highlightbackground='#E2E8F0'
        )
        self.form_frame.pack(fill=tk.BOTH, expand=True, pady=20)

        # Iniciar con formulario de login
        self.mostrar_formulario_login()

    def limpiar_formulario(self):
        """Limpia el formulario actual."""
        for widget in self.form_frame.winfo_children():
            widget.destroy()

    def mostrar_formulario_login(self):
        """Muestra el formulario de login."""
        self.limpiar_formulario()
        self.mostrar_registro = False

        # Padding interior
        form_content = tk.Frame(self.form_frame, bg='#FFFFFF')
        form_content.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)

        # Título elegante
        tk.Label(
            form_content,
            text="Bienvenido",
            font=('SF Pro Display', 24, 'bold'),
            bg='#FFFFFF',
            fg='#2D3748'
        ).pack(pady=(0, 10))

        tk.Label(
            form_content,
            text="Inicia sesión en tu cuenta",
            font=('SF Pro Display', 11),
            bg='#FFFFFF',
            fg='#A0AEC0'
        ).pack(pady=(0, 35))

        # Email
        tk.Label(
            form_content,
            text="Correo electrónico",
            font=('SF Pro Display', 10),
            bg='#FFFFFF',
            fg='#718096'
        ).pack(anchor=tk.W, pady=(10, 5))

        self.entry_email = tk.Entry(
            form_content,
            font=('SF Pro Display', 11),
            relief='solid',
            borderwidth=1,
            bg='#FAFAFA',
            fg='#2D3748',
            insertbackground='#2D3748',
            highlightthickness=1,
            highlightcolor='#667EEA',
            highlightbackground='#E2E8F0'
        )
        self.entry_email.pack(fill=tk.X, ipady=10)

        # Contraseña
        tk.Label(
            form_content,
            text="Contraseña",
            font=('SF Pro Display', 10),
            bg='#FFFFFF',
            fg='#718096'
        ).pack(anchor=tk.W, pady=(20, 5))

        self.entry_password = tk.Entry(
            form_content,
            font=('SF Pro Display', 11),
            show='●',
            relief='solid',
            borderwidth=1,
            bg='#FAFAFA',
            fg='#2D3748',
            insertbackground='#2D3748',
            highlightthickness=1,
            highlightcolor='#667EEA',
            highlightbackground='#E2E8F0'
        )
        self.entry_password.pack(fill=tk.X, ipady=10)
        self.entry_password.bind('<Return>', lambda e: self.hacer_login())

        # Botón de login - Elegante y minimalista
        login_frame = tk.Frame(
            form_content,
            bg='#667EEA',
            cursor='hand2',
            relief='flat',
            borderwidth=0
        )
        login_frame.pack(fill=tk.X, pady=(35, 20))

        login_label = tk.Label(
            login_frame,
            text="Iniciar Sesión",
            font=('SF Pro Display', 12, 'bold'),
            bg='#667EEA',
            fg='#FFFFFF',
            cursor='hand2',
            padx=20,
            pady=14
        )
        login_label.pack()

        # Hacer clickeable
        login_frame.bind('<Button-1>', lambda e: self.hacer_login())
        login_label.bind('<Button-1>', lambda e: self.hacer_login())

        # Efecto hover suave
        def login_enter(e):
            login_frame.config(bg='#5568F5')
            login_label.config(bg='#5568F5')

        def login_leave(e):
            login_frame.config(bg='#667EEA')
            login_label.config(bg='#667EEA')

        login_frame.bind('<Enter>', login_enter)
        login_label.bind('<Enter>', login_enter)
        login_frame.bind('<Leave>', login_leave)
        login_label.bind('<Leave>', login_leave)

        # Separador sutil
        separator = tk.Frame(form_content, bg='#E2E8F0', height=1)
        separator.pack(fill=tk.X, pady=25)

        # Texto para registro
        tk.Label(
            form_content,
            text="¿No tienes una cuenta?",
            font=('SF Pro Display', 10),
            bg='#FFFFFF',
            fg='#718096'
        ).pack(pady=(0, 12))

        # Botón de registro - Estilo outline elegante
        btn_frame = tk.Frame(
            form_content,
            bg='#FFFFFF',
            cursor='hand2',
            relief='solid',
            borderwidth=1,
            highlightthickness=1,
            highlightbackground='#667EEA'
        )
        btn_frame.pack(fill=tk.X, pady=(0, 10))

        btn_label = tk.Label(
            btn_frame,
            text="Crear Cuenta Nueva",
            font=('SF Pro Display', 12, 'bold'),
            bg='#FFFFFF',
            fg='#667EEA',
            cursor='hand2',
            padx=20,
            pady=14
        )
        btn_label.pack()

        # Hacer clickeable
        btn_frame.bind('<Button-1>', lambda e: self.mostrar_formulario_registro())
        btn_label.bind('<Button-1>', lambda e: self.mostrar_formulario_registro())

        # Efecto hover
        def on_enter(e):
            btn_frame.config(bg='#F7FAFC', highlightbackground='#5568F5')
            btn_label.config(bg='#F7FAFC', fg='#5568F5')

        def on_leave(e):
            btn_frame.config(bg='#FFFFFF', highlightbackground='#667EEA')
            btn_label.config(bg='#FFFFFF', fg='#667EEA')

        btn_frame.bind('<Enter>', on_enter)
        btn_label.bind('<Enter>', on_enter)
        btn_frame.bind('<Leave>', on_leave)
        btn_label.bind('<Leave>', on_leave)

    def mostrar_formulario_registro(self):
        """Muestra el formulario de registro."""
        self.limpiar_formulario()
        self.mostrar_registro = True

        # Padding interior
        form_content = tk.Frame(self.form_frame, bg='#FFFFFF')
        form_content.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)

        # Título elegante
        tk.Label(
            form_content,
            text="Crear Cuenta",
            font=('SF Pro Display', 24, 'bold'),
            bg='#FFFFFF',
            fg='#2D3748'
        ).pack(pady=(0, 10))

        tk.Label(
            form_content,
            text="Únete a FinanzApp",
            font=('SF Pro Display', 11),
            bg='#FFFFFF',
            fg='#A0AEC0'
        ).pack(pady=(0, 25))

        # Nombre
        tk.Label(
            form_content,
            text="Nombre completo",
            font=('SF Pro Display', 10),
            bg='#FFFFFF',
            fg='#718096'
        ).pack(anchor=tk.W, pady=(10, 5))

        self.entry_nombre = tk.Entry(
            form_content,
            font=('SF Pro Display', 11),
            relief='solid',
            borderwidth=1,
            bg='#FAFAFA',
            fg='#2D3748',
            insertbackground='#2D3748',
            highlightthickness=1,
            highlightcolor='#667EEA',
            highlightbackground='#E2E8F0'
        )
        self.entry_nombre.pack(fill=tk.X, ipady=10)

        # Email
        tk.Label(
            form_content,
            text="Correo electrónico",
            font=('SF Pro Display', 10),
            bg='#FFFFFF',
            fg='#718096'
        ).pack(anchor=tk.W, pady=(15, 5))

        self.entry_email_reg = tk.Entry(
            form_content,
            font=('SF Pro Display', 11),
            relief='solid',
            borderwidth=1,
            bg='#FAFAFA',
            fg='#2D3748',
            insertbackground='#2D3748',
            highlightthickness=1,
            highlightcolor='#667EEA',
            highlightbackground='#E2E8F0'
        )
        self.entry_email_reg.pack(fill=tk.X, ipady=10)

        # Contraseña
        tk.Label(
            form_content,
            text="Contraseña",
            font=('SF Pro Display', 10),
            bg='#FFFFFF',
            fg='#718096'
        ).pack(anchor=tk.W, pady=(15, 5))

        self.entry_password_reg = tk.Entry(
            form_content,
            font=('SF Pro Display', 11),
            show='●',
            relief='solid',
            borderwidth=1,
            bg='#FAFAFA',
            fg='#2D3748',
            insertbackground='#2D3748',
            highlightthickness=1,
            highlightcolor='#667EEA',
            highlightbackground='#E2E8F0'
        )
        self.entry_password_reg.pack(fill=tk.X, ipady=10)

        # Confirmar contraseña
        tk.Label(
            form_content,
            text="Confirmar contraseña",
            font=('SF Pro Display', 10),
            bg='#FFFFFF',
            fg='#718096'
        ).pack(anchor=tk.W, pady=(15, 5))

        self.entry_password_confirm = tk.Entry(
            form_content,
            font=('SF Pro Display', 11),
            show='●',
            relief='solid',
            borderwidth=1,
            bg='#FAFAFA',
            fg='#2D3748',
            insertbackground='#2D3748',
            highlightthickness=1,
            highlightcolor='#667EEA',
            highlightbackground='#E2E8F0'
        )
        self.entry_password_confirm.pack(fill=tk.X, ipady=10)
        self.entry_password_confirm.bind('<Return>', lambda e: self.registrar_usuario())

        # Botón de registro - Elegante
        reg_frame = tk.Frame(
            form_content,
            bg='#48BB78',
            cursor='hand2',
            relief='flat',
            borderwidth=0
        )
        reg_frame.pack(fill=tk.X, pady=(30, 15))

        reg_label = tk.Label(
            reg_frame,
            text="Crear Cuenta",
            font=('SF Pro Display', 12, 'bold'),
            bg='#48BB78',
            fg='#FFFFFF',
            cursor='hand2',
            padx=20,
            pady=14
        )
        reg_label.pack()

        # Hacer clickeable
        reg_frame.bind('<Button-1>', lambda e: self.registrar_usuario())
        reg_label.bind('<Button-1>', lambda e: self.registrar_usuario())

        # Efecto hover
        def reg_enter(e):
            reg_frame.config(bg='#38C172')
            reg_label.config(bg='#38C172')

        def reg_leave(e):
            reg_frame.config(bg='#48BB78')
            reg_label.config(bg='#48BB78')

        reg_frame.bind('<Enter>', reg_enter)
        reg_label.bind('<Enter>', reg_enter)
        reg_frame.bind('<Leave>', reg_leave)
        reg_label.bind('<Leave>', reg_leave)

        # Separador
        separator = tk.Frame(form_content, bg='#E2E8F0', height=1)
        separator.pack(fill=tk.X, pady=20)
        # Botón de volver - Frame con Label para compatibilidad macOS
        volver_frame = tk.Frame(
            form_content,
            bg='#FFFFFF',
            cursor='hand2',
            relief='flat'
        )
        volver_frame.pack(pady=(5, 0))

        volver_label = tk.Label(
            volver_frame,
            text="← Volver",
            font=('SF Pro Display', 10),
            bg='#FFFFFF',
            fg='#A0AEC0',
            cursor='hand2',
            padx=10,
            pady=8
        )
        volver_label.pack()

        # Hacer clickeable
        volver_frame.bind('<Button-1>', lambda e: self.mostrar_formulario_login())
        volver_label.bind('<Button-1>', lambda e: self.mostrar_formulario_login())

        # Efecto hover
        def volver_enter(e):
            volver_label.config(fg='#667EEA')

        def volver_leave(e):
            volver_label.config(fg='#A0AEC0')

        volver_label.bind('<Enter>', volver_enter)
        volver_label.bind('<Leave>', volver_leave)

    def hacer_login(self):
        """Procesa el login del usuario."""
        email = self.entry_email.get().strip()
        password = self.entry_password.get()

        # Validaciones
        if not email:
            messagebox.showerror("Error", "Por favor ingresa tu email")
            self.entry_email.focus()
            return

        if not password:
            messagebox.showerror("Error", "Por favor ingresa tu contraseña")
            self.entry_password.focus()
            return

        # Autenticar
        resultado = self.db.autenticar_usuario(email, password)

        if resultado:
            usuario_id, nombre, rol = resultado
            messagebox.showinfo(
                "Bienvenido",
                f"¡Hola {nombre}!\nIniciando sesión..."
            )
            # Pasar el rol a la función on_login_success
            self.on_login_success(usuario_id, nombre, rol)
        else:
            messagebox.showerror(
                "Error de Autenticación",
                "Email o contraseña incorrectos.\nPor favor verifica tus credenciales."
            )
            self.entry_password.delete(0, tk.END)
            self.entry_password.focus()

    def registrar_usuario(self):
        """Registra un nuevo usuario."""
        nombre = self.entry_nombre.get().strip()
        email = self.entry_email_reg.get().strip()
        password = self.entry_password_reg.get()
        password_confirm = self.entry_password_confirm.get()

        # Validaciones
        if not nombre:
            messagebox.showerror("Error", "Por favor ingresa tu nombre")
            self.entry_nombre.focus()
            return

        if not email:
            messagebox.showerror("Error", "Por favor ingresa tu email")
            self.entry_email_reg.focus()
            return

        if '@' not in email or '.' not in email:
            messagebox.showerror("Error", "Por favor ingresa un email válido")
            self.entry_email_reg.focus()
            return

        if not password:
            messagebox.showerror("Error", "Por favor ingresa una contraseña")
            self.entry_password_reg.focus()
            return

        if len(password) < 6:
            messagebox.showerror(
                "Error",
                "La contraseña debe tener al menos 6 caracteres"
            )
            self.entry_password_reg.focus()
            return

        if password != password_confirm:
            messagebox.showerror(
                "Error",
                "Las contraseñas no coinciden"
            )
            self.entry_password_confirm.delete(0, tk.END)
            self.entry_password_confirm.focus()
            return

        # Registrar usuario
        exito, mensaje = self.db.registrar_usuario(nombre, email, password)

        if exito:
            messagebox.showinfo(
                "Registro Exitoso",
                f"¡Bienvenido {nombre}!\n\n{mensaje}\n\nAhora puedes iniciar sesión."
            )
            self.mostrar_formulario_login()
        else:
            messagebox.showerror("Error de Registro", mensaje)
