# 📋 Guía de Pull Requests - FinanzApp

## 🎯 Propósito

Esta guía explica cómo crear y gestionar Pull Requests (PRs) para mantener un flujo de trabajo ordenado entre las ramas `desarrollo` y `main`.

---

## 🌿 Estructura de Ramas

### `main` (Rama Principal)
- Contiene código **estable y probado**
- Solo se fusiona código que ha pasado revisión
- Representa la versión "producción" de la aplicación

### `desarrollo` (Rama de Desarrollo)
- Donde se desarrollan **nuevas funcionalidades**
- Permite experimentar sin afectar main
- Se prueba antes de fusionar a main

---

## 📝 Flujo de Trabajo Completo

### 1. Trabajar en Desarrollo

```bash
# Asegurarse de estar en la rama desarrollo
git checkout desarrollo

# Ver el estado actual
git status

# Hacer cambios en los archivos...
# (editar código, agregar funcionalidades, etc.)

# Agregar los cambios al staging
git add .
# o agregar archivos específicos:
git add src/vistas.py src/database.py

# Hacer commit con mensaje descriptivo
git commit -m "feat: Agregar filtro por fecha en estadísticas"
```

### 2. Verificar los Cambios

```bash
# Ver el historial de commits
git log --oneline -5

# Ver las diferencias con main
git diff main..desarrollo

# Ver archivos modificados
git diff --name-only main..desarrollo
```

### 3. Preparar para Pull Request

Antes de crear un PR, asegúrate de:

- ✅ El código funciona correctamente
- ✅ No hay errores en consola
- ✅ Has probado la funcionalidad
- ✅ El código sigue las convenciones del proyecto
- ✅ Los commits tienen mensajes claros

### 4. Simular Pull Request (Local)

```bash
# Ver qué se fusionaría
git checkout main
git diff main..desarrollo

# Si todo se ve bien, hacer merge
git merge desarrollo

# O hacer merge con --no-ff para mantener historial
git merge --no-ff desarrollo -m "Merge branch 'desarrollo': Mejoras de visibilidad"
```

---

## 🔄 Proceso de Pull Request

### Opción A: PR Local (Sin GitHub/GitLab)

```bash
# 1. Estar en rama main
git checkout main

# 2. Ver los cambios que se fusionarán
git log main..desarrollo --oneline

# 3. Fusionar desarrollo en main
git merge desarrollo

# 4. Si hay conflictos, resolverlos
# (editar archivos conflictivos)
git add <archivos-resueltos>
git commit -m "Merge desarrollo into main"

# 5. Verificar que todo funciona
python main.py  # Probar la aplicación

# 6. Si todo está bien, el PR está completo
```

### Opción B: PR con GitHub/GitLab

1. **Subir rama desarrollo:**
```bash
git push origin desarrollo
```

2. **En la plataforma (GitHub/GitLab):**
   - Ir a la sección "Pull Requests"
   - Clic en "New Pull Request"
   - Base: `main` ← Compare: `desarrollo`
   - Agregar título y descripción
   - Crear Pull Request

3. **Revisar el PR:**
   - Verificar los cambios
   - Ejecutar tests (si existen)
   - Aprobar o solicitar cambios

4. **Fusionar el PR:**
   - Clic en "Merge Pull Request"
   - Elegir tipo de merge (merge commit, squash, rebase)
   - Confirmar

---

## 📊 Ejemplo de Pull Request

### Título
```
feat: Mejorar visibilidad de gastos compartidos
```

### Descripción
```markdown
## 🎨 Cambios Realizados

- Mejorar contraste de gastos compartidos
- Agregar texto verde oscuro (#1B5E20)
- Aplicar negrita a gastos compartidos
- Mejorar accesibilidad (WCAG AAA)

## 🧪 Pruebas

- ✅ Verificado en vistas mensuales
- ✅ Gastos compartidos visibles correctamente
- ✅ No afecta gastos personales
- ✅ Balance calcula correctamente

## 📸 Screenshots

(Agregar capturas de pantalla si es necesario)

## ⚠️ Notas

- Requiere base de datos con tabla `grupos` y `gastos_compartidos`
- Compatible con versión anterior
```

---

## 🔍 Revisión de Código

### Checklist para Revisor

- [ ] El código funciona correctamente
- [ ] No introduce bugs nuevos
- [ ] Sigue las convenciones de código
- [ ] Los commits son claros
- [ ] La funcionalidad está completa
- [ ] No hay código comentado innecesario
- [ ] Las variables tienen nombres descriptivos

### Checklist para Autor

- [ ] He probado los cambios localmente
- [ ] El código está limpio y formateado
- [ ] He actualizado la documentación si es necesario
- [ ] Los mensajes de commit son descriptivos
- [ ] No hay archivos temporales incluidos
- [ ] He resuelto todos los conflictos

---

## 🚨 Resolución de Conflictos

Si hay conflictos al fusionar:

```bash
# 1. Intentar fusionar
git merge desarrollo

# Si hay conflictos, Git te avisará:
# CONFLICT (content): Merge conflict in src/vistas.py

# 2. Ver archivos en conflicto
git status

# 3. Abrir archivos y resolver conflictos
# Buscar marcadores:
# <<<<<<< HEAD
# código de main
# =======
# código de desarrollo
# >>>>>>> desarrollo

# 4. Editar y decidir qué código mantener

# 5. Agregar archivos resueltos
git add src/vistas.py

# 6. Completar el merge
git commit -m "Resolve merge conflicts in vistas.py"
```

---

## 📋 Comandos Útiles

```bash
# Ver estado de las ramas
git branch -v

# Ver commits diferentes entre ramas
git log main..desarrollo --oneline

# Ver archivos diferentes entre ramas
git diff --name-only main desarrollo

# Deshacer último commit (mantener cambios)
git reset --soft HEAD~1

# Deshacer último commit (borrar cambios) ⚠️
git reset --hard HEAD~1

# Ver historial gráfico
git log --graph --oneline --all

# Cambiar a main y traer últimos cambios
git checkout main
git pull origin main

# Actualizar desarrollo desde main
git checkout desarrollo
git merge main
```

---

## 🎯 Mejores Prácticas

### 1. **Commits Pequeños y Frecuentes**
```bash
# Malo:
git commit -m "varios cambios"

# Bueno:
git commit -m "feat: Agregar validación de email"
git commit -m "fix: Corregir cálculo de balance"
git commit -m "style: Mejorar formato de código"
```

### 2. **Mensajes Descriptivos**
```bash
# Malo:
git commit -m "fix"

# Bueno:
git commit -m "fix: Corregir error al eliminar categoría con gastos asociados"
```

### 3. **Revisar Antes de Fusionar**
```bash
# Siempre revisar los cambios
git diff main..desarrollo

# Probar la aplicación
python main.py
```

### 4. **Mantener Desarrollo Actualizado**
```bash
# Periódicamente traer cambios de main
git checkout desarrollo
git merge main
```

---

## 📚 Recursos

- [Git Documentation](https://git-scm.com/doc)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [GitHub Flow](https://guides.github.com/introduction/flow/)

---

## 💡 Ejemplo Práctico Completo

### Escenario: Agregar nueva funcionalidad

```bash
# 1. Ir a desarrollo
git checkout desarrollo

# 2. Verificar estado
git status

# 3. Hacer cambios en los archivos
# (editar src/vistas.py, por ejemplo)

# 4. Probar que funciona
python main.py

# 5. Agregar cambios
git add src/vistas.py

# 6. Hacer commit
git commit -m "feat: Agregar exportación de gastos a PDF"

# 7. Ver el commit
git log -1

# 8. Cambiar a main
git checkout main

# 9. Ver diferencias
git diff main..desarrollo

# 10. Fusionar
git merge desarrollo --no-ff -m "Merge: Agregar exportación a PDF"

# 11. Verificar
python main.py

# 12. Listo! ✅
```

---

## ✅ Resumen

1. **Desarrollo** → Trabajar en `desarrollo`
2. **Commit** → Hacer commits descriptivos
3. **Probar** → Verificar que funciona
4. **Revisar** → Ver diferencias con main
5. **Fusionar** → Merge de desarrollo a main
6. **Verificar** → Probar en main

**¡Siempre probar antes de fusionar a main!** 🚀

---

**FinanzApp - Flujo de Trabajo con Git** 💻

