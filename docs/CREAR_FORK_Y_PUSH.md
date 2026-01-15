# Solución: Repository Not Found - Crear Fork

## El Error

```
remote: Repository not found.
fatal: repository 'https://github.com/andresrzitx/GestorFinanzas.git/' not found
```

**Causa**: El repositorio `andresrzitx/GestorFinanzas` no existe en GitHub. Necesitas crear un fork del repositorio original.

## Solución Rápida

### Paso 1: Crear el Fork en GitHub

1. **Abre tu navegador** y ve a: https://github.com/arezubi/GestorFinanzas

2. **Haz click en el botón "Fork"** (arriba a la derecha, al lado de "Star")

3. **Selecciona tu cuenta** `andresrzitx` como destino del fork

4. **Espera** a que GitHub termine de crear el fork

5. **Verifica** que ahora existe en: https://github.com/andresrzitx/GestorFinanzas

### Paso 2: Hacer Push

Una vez creado el fork, ya puedes hacer push:

```bash
cd /Users/andres.reyesz/PycharmProjects/GestorFinanzas
git push -u origin feat/add-calendar
```

## Alternativa: Usar GitHub CLI (Método Automático)

Si prefieres hacerlo desde la terminal:

### 1. Instalar GitHub CLI

```bash
# Con Homebrew
brew install gh

# O descargarlo desde: https://cli.github.com/
```

### 2. Autenticarse

```bash
gh auth login
```

Sigue las instrucciones interactivas para autenticarte.

### 3. Crear el Fork Automáticamente

```bash
cd /Users/andres.reyesz/PycharmProjects/GestorFinanzas
gh repo fork arezubi/GestorFinanzas --remote=false
```

### 4. Hacer Push

```bash
git push -u origin feat/add-calendar
```

## Verificación

Después de crear el fork, verifica que los remotos estén configurados correctamente:

```bash
git remote -v
```

Deberías ver:
```
origin    https://github.com/andresrzitx/GestorFinanzas.git (fetch)
origin    https://github.com/andresrzitx/GestorFinanzas.git (push)
upstream  https://github.com/arezubi/GestorFinanzas.git (fetch)
upstream  https://github.com/arezubi/GestorFinanzas.git (push)
```

## Si Necesitas Cambiar el Nombre de Usuario

Si tu cuenta de GitHub tiene otro nombre (no `andresrzitx`), actualiza el remote:

```bash
# Reemplaza TU_USUARIO con tu nombre de usuario real de GitHub
git remote set-url origin https://github.com/TU_USUARIO/GestorFinanzas.git
```

## Autenticación

Cuando hagas push por primera vez, GitHub te pedirá autenticación:

### Opción 1: Personal Access Token (Recomendado)

1. Ve a: https://github.com/settings/tokens
2. Click en "Generate new token" → "Generate new token (classic)"
3. Dale un nombre descriptivo (ej: "GestorFinanzas - MacBook")
4. Selecciona permisos: ✅ `repo` (todos los sub-permisos)
5. Expiration: Elige la duración que prefieras
6. Click en "Generate token"
7. **COPIA EL TOKEN** (solo se muestra una vez)
8. Cuando Git pida contraseña, **pega el token** en lugar de tu contraseña

### Opción 2: SSH (Alternativa)

Si prefieres usar SSH:

1. Genera una clave SSH (si no tienes una):
   ```bash
   ssh-keygen -t ed25519 -C "tu-email@ejemplo.com"
   ```

2. Añade la clave a GitHub:
   ```bash
   # Copia la clave pública
   cat ~/.ssh/id_ed25519.pub
   # Ve a https://github.com/settings/keys y añádela
   ```

3. Cambia el remote a SSH:
   ```bash
   git remote set-url origin git@github.com:andresrzitx/GestorFinanzas.git
   ```

4. Haz push:
   ```bash
   git push -u origin feat/add-calendar
   ```

## Después del Push

Una vez que hayas hecho push exitosamente:

1. Ve a tu repositorio: https://github.com/andresrzitx/GestorFinanzas
2. Verás un banner amarillo: "feat/add-calendar had recent pushes"
3. Click en "Compare & pull request"
4. Completa la información del Pull Request:
   - **Título**: Descripción breve de los cambios
   - **Descripción**: Detalla qué añade esta feature
5. Click en "Create pull request"
6. Espera a que `arezubi` revise y apruebe los cambios

## Resumen de Comandos

```bash
# 1. Crear fork en GitHub (navegador o con gh CLI)
# Ir a https://github.com/arezubi/GestorFinanzas y hacer click en "Fork"

# 2. Verificar remotos
git remote -v

# 3. Hacer push
git push -u origin feat/add-calendar

# 4. Crear Pull Request desde GitHub
# Ir a https://github.com/andresrzitx/GestorFinanzas
```

## Solución de Problemas

### Error: "Authentication failed"

- Usa un Personal Access Token en lugar de tu contraseña
- O configura SSH

### Error: "Permission denied"

- Verifica que el fork existe en tu cuenta
- Asegúrate de estar autenticado con la cuenta correcta

### El fork no aparece en mi cuenta

- Espera unos segundos, GitHub puede tardar un momento
- Refresca la página
- Verifica en: https://github.com/andresrzitx?tab=repositories

## Próximos Pasos

✅ Crear el fork en GitHub
✅ Configurar autenticación (Token o SSH)
✅ Hacer push: `git push -u origin feat/add-calendar`
✅ Crear Pull Request
