# 🏦 FinanzApp - Sistema de Gestión Financiera Personal

Aplicación de escritorio para gestión de finanzas personales con soporte para gastos compartidos entre usuarios.

## 📋 Características

- ✅ Sistema de autenticación de usuarios
- 💰 Gestión de ingresos y gastos mensuales
- 🏷️ Categorización personalizable de gastos
- 💳 Registro de método de pago (efectivo/tarjeta)
- 🏠 Gastos compartidos entre usuarios (grupos)
- 👨‍💼 Panel de administración
- 📊 Comparación y estadísticas anuales
- 🎨 Interfaz moderna y elegante
- 🗄️ Base de datos SQLite por usuario

## 🚀 Instalación

1. Clonar el repositorio:
```bash
git clone <url-del-repositorio>
cd ProyectoFinal
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Ejecutar la aplicación:
```bash
python main.py
```

## 🌿 Flujo de Trabajo con Git

### Ramas

- **`main`**: Rama principal con código estable y probado
- **`desarrollo`**: Rama para desarrollo activo y nuevas funcionalidades

### Proceso de Desarrollo

1. **Trabajar en la rama de desarrollo:**
```bash
git checkout desarrollo
```

2. **Hacer cambios y commits:**
```bash
git add .
git commit -m "feat: descripción del cambio"
```

3. **Crear Pull Request:**
   - Cuando una funcionalidad esté completa y probada
   - Crear PR desde `desarrollo` hacia `main`
   - Revisar los cambios antes de fusionar

4. **Fusionar a main:**
```bash
git checkout main
git merge desarrollo
```

### Convenciones de Commits

Usamos [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` Nueva funcionalidad
- `fix:` Corrección de bugs
- `docs:` Cambios en documentación
- `style:` Cambios de formato (no afectan funcionalidad)
- `refactor:` Refactorización de código
- `test:` Agregar o modificar tests
- `chore:` Tareas de mantenimiento

## 📁 Estructura del Proyecto

```
ProyectoFinal/
├── main.py                 # Punto de entrada de la aplicación
├── requirements.txt        # Dependencias Python
├── .gitignore             # Archivos ignorados por Git
├── README.md              # Este archivo
├── src/                   # Código fuente
│   ├── app.py            # Aplicación principal
│   ├── database.py       # Gestión de base de datos
│   ├── login.py          # Sistema de autenticación
│   ├── vistas.py         # Vistas de la interfaz
│   ├── estilos.py        # Estilos y componentes UI
│   └── utilidades.py     # Funciones auxiliares
├── data/                  # Bases de datos (ignorado en Git)
│   ├── usuarios.db       # DB de usuarios
│   └── usuarios/         # DBs financieras por usuario
├── backup/                # Backups de BD (ignorado en Git)
├── docs/                  # Documentación
└── scripts/               # Scripts de utilidad
    ├── migrar_db.py      # Migración de BD
    └── setup_inicial.py  # Configuración inicial
```

## 🔐 Usuario Administrador

**Email:** admin@finanzapp.com  
**Contraseña:** admin123

## 🛠️ Tecnologías

- **Python 3.12+**
- **Tkinter**: Interfaz gráfica
- **SQLite**: Base de datos
- **Git**: Control de versiones

## 📝 Notas de Desarrollo

### Estado Actual

**Rama `main`**: Versión estable con funcionalidades básicas
- Sistema de login
- Gestión de gastos/ingresos
- Categorías
- Panel de administración
- Gastos compartidos (básico)

**Rama `desarrollo`**: Incluye mejoras adicionales
- Mejora de visibilidad de gastos compartidos
- Texto verde oscuro + negrita en gastos compartidos
- Mejor contraste visual (WCAG AAA)

## 🤝 Contribuir

1. Hacer fork del proyecto
2. Crear rama de feature (`git checkout -b feature/AmazingFeature`)
3. Commit de cambios (`git commit -m 'feat: Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## 📄 Licencia

Este proyecto es de código abierto para fines educativos.

## 👨‍💻 Autor

Andrés Reyes - ProyectoFinal

## 📧 Contacto

Para preguntas o sugerencias, crear un issue en el repositorio.

---

**FinanzApp** - Gestiona tus finanzas de forma simple y elegante 💰

# gestor_gastos
