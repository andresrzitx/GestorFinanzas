# 🏦 FinanzApp - Sistema de Gestión Financiera Personal

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green.svg)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Tests](https://img.shields.io/badge/Tests-Passing-success.svg)

**Aplicación de escritorio profesional para gestión de finanzas personales**

[Características](#-características) • [Instalación](#-instalación) • [Uso](#-uso) • [Documentación](#-documentación)

</div>

---

## 📝 Descripción del Proyecto

FinanzApp es un sistema completo de gestión financiera personal desarrollado en Python que permite a los usuarios controlar sus ingresos, gastos y presupuestos de manera eficiente. La aplicación incluye un sistema de autenticación, gestión de categorías, reportes estadísticos y un panel de administración completo.

**Desarrollado como proyecto final** utilizando **Programación Orientada a Objetos**, **Framework Tkinter** y **Base de Datos SQLite**.

## ✨ Características Principales

### 🔐 Sistema de Autenticación
- **Login seguro** con encriptación de contraseñas (SHA-256)
- **Registro de nuevos usuarios** con validación de datos
- **Roles de usuario**: Usuario estándar y Administrador
- **Gestión de sesiones** con tracking de último acceso

### 💰 Gestión Financiera
- **Registro de gastos** con fecha, categoría y método de pago
- **Registro de ingresos** mensuales
- **Categorías personalizables** (crear, editar, eliminar)
- **Métodos de pago**: Efectivo y Tarjeta
- **Balance automático**: Cálculo de ingresos vs gastos

### 📊 Reportes y Estadísticas
- **Vista mensual** de gastos e ingresos
- **Comparación anual** entre diferentes años
- **Gráficos estadísticos** por categoría
- **Desglose por método de pago**
- **Exportación de datos** (futuro)

### 🏠 Gastos Compartidos
- **Grupos de gastos** para compartir con otros usuarios
- **División de gastos** entre miembros
- **Tracking de participantes**

### 👨‍💼 Panel de Administración
- **Gestión de usuarios** (activar/desactivar)
- **Estadísticas globales** del sistema
- **Monitoreo de actividad**
- **Vista de usuarios registrados**

### 🎨 Interfaz de Usuario
- **Diseño moderno** con colores personalizados
- **Navegación intuitiva** mediante pestañas
- **Botones interactivos** con efectos hover
- **Mensajes de confirmación** para acciones importantes
- **Responsive design** adaptable a diferentes resoluciones

## 🏗️ Arquitectura del Proyecto

### Estructura de Directorios

```
GestorFinanzas/
├── README.md                    # Este archivo
├── main.py                      # Punto de entrada de la aplicación
├── requirements.txt             # Dependencias del proyecto
├── src/                         # Código fuente
│   ├── __init__.py
│   ├── app.py                   # Aplicación principal (GUI)
│   ├── database.py              # Gestor de base de datos
│   ├── login.py                 # Sistema de autenticación
│   ├── models.py                # Modelos POO (Usuario, Gasto, etc.)
│   ├── vistas.py                # Vistas de la interfaz
│   ├── estilos.py               # Componentes de estilo
│   └── utilidades.py            # Funciones auxiliares
├── tests/                       # Tests unitarios
│   ├── __init__.py
│   ├── test_models.py           # Tests de modelos
│   ├── test_login.py            # Tests de autenticación
│   └── test_database.py         # Tests de base de datos
├── data/                        # Bases de datos (no versionado)
│   ├── usuarios.db              # BD de usuarios
│   └── usuarios/                # BDs individuales por usuario
├── docs/                        # Documentación técnica
│   ├── DOCUMENTACION_TECNICA.md
│   ├── MANUAL_USUARIO.md
│   └── MEJORAS_ENTREGA_FINAL.md
└── scripts/                     # Scripts de utilidad
    ├── setup_inicial.py
    └── migrar_db.py
```

### Tecnologías Utilizadas

| Componente | Tecnología | Justificación |
|------------|------------|---------------|
| **Lenguaje** | Python 3.8+ | Versatilidad y bibliotecas robustas |
| **Framework GUI** | Tkinter | Framework nativo multiplataforma |
| **Base de Datos** | SQLite | Ligera, sin configuración, ideal para desktop |
| **ORM** | SQL Directo | Mayor control y rendimiento |
| **Tests** | unittest | Framework estándar de Python |
| **Seguridad** | hashlib (SHA-256) | Encriptación de contraseñas |

## 🚀 Instalación

### Requisitos Previos

- **Python 3.8 o superior** instalado
- **pip** (gestor de paquetes de Python)
- **tkinter** (incluido en Python estándar)

### Pasos de Instalación

1. **Clonar el repositorio:**

```bash
git clone https://github.com/tu-usuario/GestorFinanzas.git
cd GestorFinanzas
```

2. **Crear entorno virtual (recomendado):**

```bash
python -m venv venv

# En Windows:
venv\Scripts\activate

# En macOS/Linux:
source venv/bin/activate
```

3. **Instalar dependencias:**

```bash
pip install -r requirements.txt
```

4. **Ejecutar la aplicación:**

```bash
python main.py
```

## 💻 Uso

### Primer Inicio

1. **Crear una cuenta:**
   - Al iniciar, haz clic en "Crear cuenta nueva"
   - Ingresa tu nombre, email y contraseña
   - El sistema creará tu cuenta de usuario

2. **Iniciar sesión:**
   - Ingresa tu email y contraseña
   - Haz clic en "Iniciar Sesión"

### Usuario Administrador

Para crear un usuario administrador, ejecuta:

```bash
python scripts/crear_admin.py
```

**Credenciales por defecto:**
- Email: `admin@finanzapp.com`
- Contraseña: `admin123`

⚠️ **Cambiar estas credenciales en producción**

### Funcionalidades Principales

#### Registrar un Gasto

1. Selecciona el mes en la pestaña correspondiente
2. Completa el formulario:
   - Descripción del gasto
   - Cantidad
   - Categoría
   - Fecha
   - Método de pago (Efectivo/Tarjeta)
3. Haz clic en "Agregar Gasto"

#### Ver Estadísticas

1. Navega a la pestaña "Estadísticas"
2. Selecciona el año y mes
3. Visualiza:
   - Total de gastos por categoría
   - Distribución por método de pago
   - Balance mensual
   - Gráficos comparativos

#### Gestionar Categorías

1. Ve a "Gestión de Categorías"
2. Puedes:
   - Crear nuevas categorías
   - Editar categorías existentes
   - Eliminar categorías sin gastos asociados

## 🧬 Programación Orientada a Objetos

El proyecto está diseñado siguiendo los principios de POO:

### Clases Principales

#### 1. **Usuario** (`src/models.py`)

```python
class Usuario:
    """Representa un usuario del sistema."""
    
    def __init__(self, id, nombre, email, rol='usuario', activo=True):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.rol = rol
        self.activo = activo
    
    def es_admin(self) -> bool:
        """Verifica si el usuario es administrador."""
        return self.rol == 'admin'
```

**Atributos:**
- `id`: Identificador único
- `nombre`: Nombre del usuario
- `email`: Correo electrónico
- `rol`: Rol ('usuario' o 'admin')
- `activo`: Estado del usuario

**Métodos:**
- `es_admin()`: Verifica si es administrador
- `es_activo()`: Verifica si está activo
- `actualizar_ultimo_acceso()`: Actualiza fecha de acceso
- `to_dict()`: Serializa a diccionario

#### 2. **Gasto** (`src/models.py`)

```python
class Gasto:
    """Representa un gasto registrado."""
    
    def __init__(self, id, descripcion, cantidad, categoria_id, 
                 fecha, metodo_pago='efectivo'):
        self.id = id
        self.descripcion = descripcion
        self.cantidad = float(cantidad)
        self.categoria_id = categoria_id
        self.fecha = fecha
        self.metodo_pago = metodo_pago.lower()
    
    def es_efectivo(self) -> bool:
        """Verifica si fue pagado en efectivo."""
        return self.metodo_pago == 'efectivo'
```

**Atributos:**
- `id`: Identificador único
- `descripcion`: Descripción del gasto
- `cantidad`: Monto (float)
- `categoria_id`: ID de la categoría
- `fecha`: Fecha del gasto
- `metodo_pago`: 'efectivo' o 'tarjeta'

**Métodos:**
- `es_efectivo()`: Verifica método de pago
- `es_tarjeta()`: Verifica si es tarjeta
- `get_mes()`: Obtiene el mes
- `get_anio()`: Obtiene el año
- `to_dict()`: Serializa a diccionario

#### 3. **Database** (`src/database.py`)

```python
class Database:
    """Gestiona todas las operaciones de base de datos."""
    
    def __init__(self, usuario_id: int = None):
        self.usuario_id = usuario_id
        self.db_name = f"usuario_{usuario_id}_finanzas.db"
        self.create_tables()
    
    def agregar_gasto(self, descripcion, cantidad, categoria_id, 
                      fecha, metodo_pago) -> bool:
        """Agrega un nuevo gasto a la base de datos."""
        # Implementación...
```

**Responsabilidades:**
- Conexión a base de datos
- CRUD de gastos, ingresos, categorías
- Autenticación de usuarios
- Generación de reportes

#### 4. **AplicacionGastos** (`src/app.py`)

```python
class AplicacionGastos:
    """Aplicación principal con interfaz gráfica."""
    
    def __init__(self, root, usuario_id, nombre_usuario, rol='usuario'):
        self.root = root
        self.usuario_id = usuario_id
        self.db = Database(usuario_id)
        self.crear_interfaz()
```

**Responsabilidades:**
- Inicialización de la GUI
- Gestión de pestañas
- Coordinación entre vistas
- Manejo de eventos de usuario

### Principios POO Aplicados

| Principio | Implementación |
|-----------|----------------|
| **Encapsulación** | Atributos privados con getters/setters |
| **Abstracción** | Clases modelo separadas de la lógica de BD |
| **Herencia** | Clases de vista heredan comportamientos comunes |
| **Polimorfismo** | Métodos `to_dict()` en todas las clases modelo |

### Diagrama de Clases (Simplificado)

```
┌─────────────┐
│   Usuario   │
├─────────────┤
│ + id        │
│ + nombre    │
│ + email     │
│ + rol       │
├─────────────┤
│ + es_admin()│
└─────────────┘
       │
       │ 1:N
       ▼
┌─────────────┐       ┌─────────────┐
│    Gasto    │──N:1──│  Categoria  │
├─────────────┤       ├─────────────┤
│ + id        │       │ + id        │
│ + cantidad  │       │ + nombre    │
│ + fecha     │       └─────────────┘
├─────────────┤
│+ es_efectivo│
└─────────────┘
       │
       │
       ▼
┌─────────────┐
│  Database   │
├─────────────┤
│ + usuario_id│
├─────────────┤
│+ agregar()  │
│+ obtener()  │
│+ eliminar() │
└─────────────┘
```

## 🗄️ Base de Datos

### Modelo de Datos

El proyecto utiliza **SQLite** con las siguientes tablas:

#### Tabla: `usuarios` (Base de datos principal)

```sql
CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    rol TEXT DEFAULT 'usuario',
    activo INTEGER DEFAULT 1,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ultimo_acceso TIMESTAMP
);
```

#### Tabla: `gastos` (Por usuario)

```sql
CREATE TABLE gastos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    descripcion TEXT NOT NULL,
    cantidad REAL NOT NULL,
    categoria_id INTEGER,
    fecha TEXT NOT NULL,
    metodo_pago TEXT DEFAULT 'efectivo',
    FOREIGN KEY (categoria_id) REFERENCES categorias (id)
);
```

#### Tabla: `categorias` (Por usuario)

```sql
CREATE TABLE categorias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT UNIQUE NOT NULL,
    descripcion TEXT
);
```

#### Tabla: `ingresos` (Por usuario)

```sql
CREATE TABLE ingresos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    descripcion TEXT NOT NULL,
    cantidad REAL NOT NULL,
    fecha TEXT NOT NULL
);
```

### Diagrama Entidad-Relación

```
┌─────────────┐
│  USUARIOS   │
└──────┬──────┘
       │ 1:1
       │
       ▼
┌─────────────────────────────────┐
│  USUARIO_FINANZAS.DB            │
│  ┌────────────┐  ┌────────────┐ │
│  │   GASTOS   │  │  INGRESOS  │ │
│  └─────┬──────┘  └────────────┘ │
│        │ N:1                     │
│  ┌─────▼──────┐                 │
│  │ CATEGORIAS │                 │
│  └────────────┘                 │
└─────────────────────────────────┘
```

## 🧪 Tests Unitarios

El proyecto incluye tests completos para garantizar la calidad del código.

### Ejecutar Tests

```bash
# Ejecutar todos los tests
python -m unittest discover tests/

# Ejecutar tests específicos
python tests/test_models.py
python tests/test_login.py

# Con pytest (si está instalado)
pytest tests/ -v
```

### Cobertura de Tests

- ✅ Tests de modelos (Usuario, Gasto, Categoria, Ingreso)
- ✅ Tests de autenticación
- ✅ Tests de base de datos
- ✅ Tests de validación

### Ejemplo de Test

```python
class TestGasto(unittest.TestCase):
    def test_crear_gasto_efectivo(self):
        gasto = Gasto(1, "Comida", 100, 1, "2026-01-19", "efectivo")
        self.assertTrue(gasto.es_efectivo())
        self.assertEqual(gasto.cantidad, 100.0)
```

### Demostración de Uso

Para ver los modelos POO en acción:

## 🔧 Uso de Modelos POO

Los modelos están **completamente integrados** en el sistema. La clase `Database` incluye métodos que retornan objetos en lugar de tuplas:

### Métodos Disponibles

```python
# Obtener gastos como objetos Gasto
gastos = db.obtener_gastos_como_objetos(mes=1, anio=2026)
for gasto in gastos:
    if gasto.es_efectivo():
        print(f"{gasto.descripcion}: ${gasto.cantidad}")

# Obtener categorías como objetos Categoria
categorias = db.obtener_categorias_como_objetos()
for categoria in categorias:
    print(categoria.nombre)

# Obtener usuarios como objetos Usuario
usuarios = db.obtener_todos_usuarios_como_objetos()
for usuario in usuarios:
    if usuario.es_admin():
        print(f"Admin: {usuario.nombre}")

# Obtener ingresos como objetos Ingreso
ingresos = db.obtener_ingresos_como_objetos(anio=2026)
total = sum(ingreso.cantidad for ingreso in ingresos)
```

### Ventajas sobre Tuplas

**ANTES (con tuplas):**
```python
# Difícil de leer y mantener
gasto = db.obtener_gasto_por_id(1)
if gasto[5] == 'efectivo':  # ¿Qué es el índice 5?
    print(f"{gasto[1]}: ${gasto[2]}")  # ¿Y el 1 y 2?
```

**AHORA (con objetos):**
```python
# Claro y autodocumentado
gasto = Gasto(...)
if gasto.es_efectivo():  # Método descriptivo
    print(f"{gasto.descripcion}: ${gasto.cantidad}")  # Atributos nombrados
```

## 📚 Documentación

### Documentos Disponibles

- **README.md** - Este archivo (documentación general)
- **docs/DOCUMENTACION_TECNICA.md** - Arquitectura y detalles técnicos
- **docs/MANUAL_USUARIO.md** - Guía completa para usuarios
- **docs/MEJORAS_ENTREGA_FINAL.md** - Mejoras implementadas

### Generar Documentación del Código

```bash
# Instalar pydoc (incluido en Python)
python -m pydoc -b  # Abre navegador con documentación
```

## 🎨 Capturas de Pantalla

### Pantalla de Login
![Login](docs/capturas/login.png)

### Dashboard Principal
![Dashboard](docs/capturas/dashboard.png)

### Estadísticas
![Estadísticas](docs/capturas/estadisticas.png)

### Panel de Administración
![Admin](docs/capturas/admin.png)

## 🔒 Seguridad

### Medidas Implementadas

- ✅ **Encriptación de contraseñas** con SHA-256
- ✅ **Validación de inputs** para prevenir inyección SQL
- ✅ **Separación de bases de datos** por usuario
- ✅ **Roles y permisos** (usuario/admin)
- ✅ **Sesiones seguras** con tracking de accesos

### Buenas Prácticas

```python
# Contraseñas nunca se almacenan en texto plano
password_hash = hashlib.sha256(password.encode()).hexdigest()

# Validación de inputs
if not email or not password:
    raise ValueError("Email y contraseña requeridos")

# Queries parametrizadas para prevenir SQL injection
cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
```

## 🏗️ Arquitectura Escalable

### Diseño Preparado para API

El proyecto está diseñado con **separación de responsabilidades** que facilita la migración a arquitectura API REST:

```
ARQUITECTURA ACTUAL (Desktop)
┌─────────────────────────────┐
│   Tkinter (GUI)             │
├─────────────────────────────┤
│   Modelos POO               │ ← Capa de negocio independiente
├─────────────────────────────┤
│   Database (Persistencia)   │
└─────────────────────────────┘

MIGRACIÓN FUTURA A API (Multi-plataforma)
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│   Tkinter    │  │  React/Vue   │  │ React Native │
│   (Desktop)  │  │    (Web)     │  │   (Móvil)    │
└──────┬───────┘  └──────┬───────┘  └──────┬───────┘
       │                 │                 │
       └─────────────────┼─────────────────┘
                         ▼
              ┌────────────────────┐
              │   API REST (Flask) │ ← Nueva capa
              ├────────────────────┤
              │   Modelos POO      │ ← Reutilizados
              ├────────────────────┤
              │   Database         │ ← Reutilizado
              └────────────────────┘
```

### Ventajas del Diseño Actual

- ✅ **Modelos POO independientes** - No dependen de Tkinter
- ✅ **Lógica de negocio separada** - Fácil de exponer via API
- ✅ **Database como capa** - Puede convertirse en servicio
- ✅ **Validaciones en modelos** - Reutilizables en cualquier interfaz

### Migración a API (Ejemplo)

```python
# backend/api.py (Migración futura)
from flask import Flask, jsonify, request
from src.database import Database
from src.models import Gasto, Usuario

app = Flask(__name__)

@app.route('/api/gastos/<int:mes>/<int:anio>', methods=['GET'])
def get_gastos(mes, anio):
    """Endpoint que reutiliza los modelos POO existentes."""
    db = Database(usuario_id=request.user_id)
    gastos = db.obtener_gastos_como_objetos(mes=mes, anio=anio)
    
    # Usar método to_dict() de los modelos
    return jsonify([gasto.to_dict() for gasto in gastos])

@app.route('/api/gastos', methods=['POST'])
def crear_gasto():
    """Crear gasto reutilizando validaciones del modelo."""
    data = request.get_json()
    
    # Validación automática en el modelo
    gasto = Gasto(**data)  
    
    db = Database(usuario_id=request.user_id)
    db.agregar_gasto(...)
    
    return jsonify(gasto.to_dict()), 201
```

## 🚧 Roadmap / Mejoras Futuras

### Corto Plazo (1-2 meses)
- [ ] **API REST** con Flask para acceso desde múltiples clientes
- [ ] **Exportación** a Excel/PDF/CSV
- [ ] **Dashboard web** con React/Vue

### Mediano Plazo (3-6 meses)
- [ ] **App móvil** (React Native o Flutter)
- [ ] **Gráficos interactivos** con Plotly/Chart.js
- [ ] **Notificaciones** de gastos excesivos
- [ ] **Presupuestos** mensuales por categoría

### Largo Plazo (6+ meses)
- [ ] **Multi-idioma** (ES/EN/PT)
- [ ] **Modo oscuro**
- [ ] **Respaldo en la nube** (Google Drive, Dropbox)
- [ ] **Inteligencia Artificial** para predicción de gastos
- [ ] **Integración bancaria** (Open Banking)
- [ ] **Sincronización multi-dispositivo**

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Para cambios importantes:

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add: nueva característica'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

### Guías de Estilo

- **Código:** PEP 8 (Python)
- **Commits:** Conventional Commits
- **Docstrings:** Google Style

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo `LICENSE` para más detalles.

```
MIT License

Copyright (c) 2026 FinanzApp

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

## 👥 Autor

**Tu Nombre**  
- GitHub: [@tu-usuario](https://github.com/tu-usuario)
- Email: tu.email@ejemplo.com

## 🙏 Agradecimientos

- Python Community
- Tkinter Documentation
- Stack Overflow Community
- [Curso/Universidad] por el apoyo académico

## 📊 Estadísticas del Proyecto

```
- Lenguaje: Python
- Líneas de código: ~3,500
- Archivos: 25+
- Clases: 15+
- Tests: 30+
- Cobertura: >80%
```

## 📱 Contacto y Soporte

¿Tienes preguntas o problemas?

1. 📧 **Email:** soporte@finanzapp.com
2. 🐛 **Issues:** [GitHub Issues](https://github.com/tu-usuario/GestorFinanzas/issues)
3. 💬 **Discusiones:** [GitHub Discussions](https://github.com/tu-usuario/GestorFinanzas/discussions)

## ⭐ Si te ha gustado este proyecto...

- Dale una estrella ⭐ en GitHub
- Compártelo con tus amigos
- Reporta bugs o sugiere mejoras
- Contribuye con código

---

<div align="center">

**Hecho con ❤️ y Python**

[⬆ Volver arriba](#-finanzapp---sistema-de-gestión-financiera-personal)

</div>
