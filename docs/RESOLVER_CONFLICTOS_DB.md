# Cómo Resolver Conflictos en data/usuarios.db

## El Problema

El archivo `data/usuarios.db` es un archivo binario (base de datos SQLite) que no puede fusionarse automáticamente por Git. Cuando intentas hacer merge entre ramas, Git no puede combinar los cambios y genera un conflicto.

## Solución Rápida

### Método 1: Usar el Script Automático

Ejecuta el script que he creado:

```bash
./resolver_conflicto_db.sh
```

El script te guiará paso a paso para resolver el conflicto.

### Método 2: Resolución Manual

**Opción A: Mantener TU versión actual (recomendado si tienes datos importantes en tu rama)**

```bash
# 1. Resolver el conflicto manteniendo tu versión
git checkout --ours data/usuarios.db

# 2. Marcar como resuelto
git add data/usuarios.db

# 3. Continuar con el merge/rebase
git commit -m "Resuelto conflicto en usuarios.db manteniendo versión local"
# o si estás en un rebase: git rebase --continue
```

**Opción B: Usar la versión de la otra rama**

```bash
# 1. Resolver el conflicto usando la versión entrante
git checkout --theirs data/usuarios.db

# 2. Marcar como resuelto
git add data/usuarios.db

# 3. Continuar con el merge/rebase
git commit -m "Resuelto conflicto en usuarios.db usando versión remota"
# o si estás en un rebase: git rebase --continue
```

## Prevención de Conflictos Futuros

### Opción 1: No versionar las bases de datos

Si las bases de datos son solo para desarrollo local y cada desarrollador puede tener su propia versión:

1. Edita `.gitignore` y descomenta las líneas:
   ```
   *.db
   *.sqlite
   *.sqlite3
   ```

2. Elimina el archivo del seguimiento de Git (pero mantenlo localmente):
   ```bash
   git rm --cached data/usuarios.db
   git commit -m "Dejar de versionar usuarios.db"
   ```

### Opción 2: Usar scripts de migración

En lugar de versionar la base de datos completa, versiona solo los scripts SQL que la crean:

1. Exporta el esquema:
   ```bash
   sqlite3 data/usuarios.db .schema > scripts/schema_usuarios.sql
   ```

2. Crea scripts de migración para cambios en la estructura

3. Versiona solo los scripts, no la base de datos

## Backup Automático

Ya se ha creado un backup en:
```
data/usuarios_backup_20260115_232422.db
```

Cada vez que uses el script `resolver_conflicto_db.sh`, se creará un nuevo backup automáticamente.

## Verificar Estado de Conflictos

Para ver si hay conflictos activos:

```bash
git status
```

Para ver qué archivos tienen conflictos:

```bash
git diff --name-only --diff-filter=U
```

## Comandos Útiles

```bash
# Ver el estado actual
git status

# Abortar un merge en progreso
git merge --abort

# Abortar un rebase en progreso
git rebase --abort

# Ver las ramas disponibles
git branch -a

# Ver el log de commits
git log --oneline -10
```

## Notas Importantes

- **Los archivos .db son binarios**: No se pueden fusionar automáticamente
- **Siempre haz backup**: El script lo hace automáticamente
- **Elige la versión correcta**: Piensa en qué versión tiene los datos más recientes o importantes
- **Considera no versionar las DBs**: Para proyectos colaborativos, es mejor versionar solo el esquema

## En Caso de Emergencia

Si algo sale mal y necesitas recuperar la versión anterior:

```bash
# Abortar el merge/rebase
git merge --abort
# o
git rebase --abort

# Restaurar desde el backup
cp data/usuarios_backup_20260115_232422.db data/usuarios.db
```
