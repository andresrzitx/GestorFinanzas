# 📁 Función de las Carpetas backup/ y data/

**Fecha:** 19 de Enero de 2026  
**Proyecto:** FinanzApp

---

## 🗂️ Carpeta `data/`

### Función Principal:
**Almacena todas las bases de datos de la aplicación**

### Contenido:

```
data/
├── usuarios.db                      ← BD principal de usuarios
├── usuarios_backup_YYYYMMDD.db      ← Respaldos de usuarios
└── usuarios/                        ← BDs individuales por usuario
    ├── usuario_1_finanzas.db
    ├── usuario_2_finanzas.db
    ├── usuario_3_finanzas.db
    ├── usuario_4_finanzas.db
    └── usuario_5_finanzas.db
```

### Archivos:

#### 1. `usuarios.db` 
**Propósito:** Base de datos principal del sistema
- Tabla `usuarios` con todos los usuarios registrados
- Datos de autenticación (emails, contraseñas hasheadas)
- Roles (usuario/admin)
- Fecha de registro, último acceso
- **Compartida por toda la aplicación**

**Estructura:**
```sql
CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY,
    nombre TEXT,
    email TEXT UNIQUE,
    password_hash TEXT,
    rol TEXT DEFAULT 'usuario',
    activo INTEGER DEFAULT 1,
    fecha_registro TIMESTAMP,
    ultimo_acceso TIMESTAMP
);
```

#### 2. `usuarios/usuario_X_finanzas.db`
**Propósito:** Base de datos personal de cada usuario
- Una BD separada por usuario
- Contiene gastos, ingresos, categorías del usuario
- **Aislamiento de datos** por usuario
- **Privacidad y seguridad**

**Estructura de cada BD:**
```sql
-- Tablas por usuario:
- gastos
- ingresos  
- categorias
- grupos (opcional)
```

**Ventajas de este diseño:**
- ✅ Privacidad: datos de cada usuario en su propia BD
- ✅ Seguridad: un usuario no puede acceder a datos de otro
- ✅ Escalabilidad: fácil mover BDs de usuarios a diferentes servidores
- ✅ Backup selectivo: puedes respaldar usuarios específicos

#### 3. `usuarios_backup_YYYYMMDD_HHMMSS.db`
**Propósito:** Respaldo automático de la BD de usuarios
- Se crea antes de migraciones o cambios importantes
- Permite restaurar en caso de error
- Formato de fecha: Año-Mes-Día_Hora-Minuto-Segundo

---

## 🗄️ Carpeta `backup/`

### Función Principal:
**Almacena respaldos automáticos de las bases de datos**

### Contenido Actual:

```
backup/
├── gastos_mensuales.db                          ← BD antigua (migración)
├── gastos_mensuales_backup_20260107_095745.db   ← Respaldo 7 Ene 09:57
└── gastos_mensuales_backup_20260107_135609.db   ← Respaldo 7 Ene 13:56
```

### Archivos:

#### 1. `gastos_mensuales.db`
**Propósito:** Base de datos del sistema antiguo
- BD antes de la migración a multi-usuario
- **Histórico:** se mantiene como referencia
- **No se usa actualmente**

#### 2. Archivos `*_backup_YYYYMMDD_HHMMSS.db`
**Propósito:** Respaldos automáticos
- Se crean antes de migraciones
- Se crean antes de actualizaciones importantes
- Permiten restaurar versiones anteriores

**Cuándo se crean:**
- Al ejecutar scripts de migración
- Al hacer cambios en estructura de BD
- Manualmente si es necesario

---

## 🔄 Flujo de Trabajo con Respaldos

### Creación Automática de Backup:

```python
# scripts/migrar_db.py
def crear_backup():
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = f"backup/bd_backup_{timestamp}.db"
    shutil.copy2(db_original, backup_path)
    print(f"✅ Backup creado: {backup_path}")
```

### Cuándo se Usan:

1. **Antes de migraciones**
   ```bash
   python scripts/migrar_db.py
   # Crea backup automáticamente
   ```

2. **Antes de actualizaciones**
   ```bash
   python scripts/setup_inicial.py
   # Crea backup si BD existe
   ```

3. **Para restaurar datos**
   ```bash
   # Si algo sale mal:
   cp backup/usuarios_backup_20260115.db data/usuarios.db
   ```

---

## 📊 Diferencias Entre Carpetas

| Aspecto | `data/` | `backup/` |
|---------|---------|-----------|
| **Propósito** | Almacenar BDs activas | Almacenar respaldos |
| **Uso** | La app las usa constantemente | Solo para restauración |
| **Contenido** | BDs actuales | BDs históricas |
| **Git** | Se puede versionar | ❌ Ignorado (.gitignore) |
| **Importancia** | CRÍTICO - son los datos actuales | Importante - son copias de seguridad |

---

## ⚙️ Configuración en el Código

### En `src/database.py`:

```python
# Definición de rutas
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, "data")

class Database:
    # BD principal de usuarios
    USUARIOS_DB = os.path.join(DATA_DIR, "usuarios.db")
    
    # Directorio de BDs por usuario
    USUARIOS_DATA_DIR = os.path.join(DATA_DIR, "usuarios")
    
    def __init__(self, usuario_id=None):
        # Crear directorios si no existen
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)
        if not os.path.exists(self.USUARIOS_DATA_DIR):
            os.makedirs(self.USUARIOS_DATA_DIR)
        
        # BD del usuario específico
        if usuario_id:
            self.db_name = os.path.join(
                self.USUARIOS_DATA_DIR, 
                f"usuario_{usuario_id}_finanzas.db"
            )
```

---

## 🔒 Seguridad y .gitignore

### En `.gitignore`:

```bash
# Backups (no versionados)
*_backup_*.db
backup/

# Bases de datos (opcional)
# *.db  # ← Descomenta si no quieres versionar BDs
```

**¿Por qué no versionar backups?**
- Son archivos grandes
- Cambian frecuentemente
- Datos sensibles de usuarios
- Se pueden regenerar
- Ocupan espacio en repositorio

**¿Qué sí versionar?**
- Estructura del código
- Scripts de migración
- Documentación
- Tests

---

## 📋 Buenas Prácticas

### 1. ✅ Hacer Backup Antes de Cambios

```bash
# Antes de cambios importantes
python scripts/migrar_db.py
```

### 2. ✅ Mantener Backups Recientes

```bash
# Eliminar backups antiguos (>30 días)
find backup/ -name "*_backup_*.db" -mtime +30 -delete
```

### 3. ✅ Separar Datos por Usuario

```python
# Cada usuario tiene su BD
db = Database(usuario_id=1)  # → usuario_1_finanzas.db
db = Database(usuario_id=2)  # → usuario_2_finanzas.db
```

### 4. ✅ No Versionar Datos Sensibles

```bash
# En .gitignore
backup/
*.db  # Si contiene datos reales
```

---

## 🔧 Comandos Útiles

### Ver tamaño de las BDs:

```bash
# Ver tamaño de data/
du -sh data/

# Ver tamaño de backup/
du -sh backup/

# Listar BDs con tamaño
ls -lh data/*.db
ls -lh data/usuarios/*.db
```

### Crear backup manual:

```bash
# Backup de usuarios
cp data/usuarios.db backup/usuarios_backup_$(date +%Y%m%d_%H%M%S).db

# Backup de BD de un usuario específico
cp data/usuarios/usuario_1_finanzas.db backup/usuario_1_backup_$(date +%Y%m%d_%H%M%S).db
```

### Restaurar desde backup:

```bash
# Restaurar BD de usuarios
cp backup/usuarios_backup_20260115_232422.db data/usuarios.db

# Verificar que funcionó
sqlite3 data/usuarios.db "SELECT COUNT(*) FROM usuarios;"
```

---

## 💡 Para tu Presentación

### Si te preguntan sobre gestión de datos:

> "El proyecto utiliza dos carpetas principales para datos:
> 
> **data/** contiene las bases de datos activas:
> - usuarios.db para autenticación
> - Una BD separada por cada usuario (usuarios/usuario_X_finanzas.db)
>   para privacidad y seguridad
> 
> **backup/** almacena respaldos automáticos que se crean antes de 
> migraciones o cambios importantes, permitiendo restaurar en caso 
> de error.
> 
> Este diseño garantiza aislamiento de datos entre usuarios y 
> capacidad de recuperación ante fallos."

---

## 📊 Diagrama de Estructura

```
GestorFinanzas/
│
├── data/                           ← DATOS ACTIVOS
│   ├── usuarios.db                 ← BD principal (autenticación)
│   │   └── Tabla: usuarios
│   │
│   └── usuarios/                   ← BDs por usuario
│       ├── usuario_1_finanzas.db   ← Datos usuario 1
│       │   ├── Tabla: gastos
│       │   ├── Tabla: ingresos
│       │   └── Tabla: categorias
│       │
│       ├── usuario_2_finanzas.db   ← Datos usuario 2
│       └── usuario_X_finanzas.db   ← Datos usuario X
│
└── backup/                         ← RESPALDOS
    ├── gastos_mensuales.db         ← BD antigua (histórico)
    ├── usuarios_backup_*.db        ← Respaldos de usuarios
    └── *_backup_YYYYMMDD.db        ← Otros respaldos
```

---

## ✅ Resumen

| Carpeta | Función | Contenido | Se Versiona | Importancia |
|---------|---------|-----------|-------------|-------------|
| **data/** | Almacenar BDs activas | - usuarios.db<br>- usuario_X_finanzas.db | ⚠️ Opcional | ⭐⭐⭐⭐⭐ CRÍTICO |
| **backup/** | Almacenar respaldos | - Copias de seguridad<br>- BDs antiguas | ❌ No | ⭐⭐⭐ Importante |

---

## 🎯 Conclusión

- **data/**: Tus datos actuales y activos
- **backup/**: Tu red de seguridad para recuperación
- **Diseño**: Separación por usuario para privacidad
- **Seguridad**: Backups automáticos antes de cambios

**Ambas carpetas son esenciales para el funcionamiento seguro y confiable de la aplicación.**
