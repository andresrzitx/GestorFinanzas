# 📖 Guía de Uso - Gestor de Gastos Mensuales

## 🎯 Primeros Pasos

### 1. Primera Ejecución

Al ejecutar la aplicación por primera vez:
```bash
python3 app.py
```

- Se creará automáticamente el archivo `gastos_mensuales.db`
- Se insertarán 8 categorías predeterminadas
- La aplicación se abrirá mostrando el año actual

### 2. Agregar Datos de Prueba (Recomendado)

Si quieres ver la aplicación funcionando con datos de ejemplo:
```bash
python3 agregar_datos_ejemplo.py
python3 app.py
```

Esto agregará ~50 gastos realistas en los primeros 6 meses del año.

## 💡 Consejos de Uso

### Gestión de Gastos

1. **Agregar gastos rápidamente**
   - La fecha se completa automáticamente con el día actual
   - Solo necesitas cambiarla si el gasto fue de otro día
   - El mes y año se ajustan según la pestaña activa

2. **Descripción efectiva**
   - Sé específico: "Compra Mercadona - verduras" mejor que "Compra"
   - Usa términos consistentes para facilitar búsquedas futuras

3. **Categorías**
   - Usa siempre la categoría más apropiada
   - Evita usar "Otros" a menos que sea necesario
   - Puedes agregar nuevas categorías con el script de utilidades

### Análisis de Datos

1. **Comparación Mensual**
   - Ve a la pestaña "Comparación Anual" para ver tendencias
   - Identifica meses con gastos inusualmente altos
   - Compara con meses anteriores del mismo año

2. **Estadísticas por Categoría**
   - Usa el selector para ver estadísticas de un mes específico
   - Identifica categorías donde gastas más
   - Establece objetivos de reducción en categorías específicas

3. **Análisis Multi-Año**
   - Cambia el año con el selector superior
   - Compara gastos del mismo mes en diferentes años
   - Identifica tendencias a largo plazo

## 🎨 Mejores Prácticas

### 1. Registro Constante
- Registra gastos diariamente o semanalmente
- No dejes pasar mucho tiempo o olvidarás gastos pequeños
- Los gastos pequeños suman y son importantes

### 2. Categorización Consistente
- Usa siempre las mismas categorías para gastos similares
- Esto facilita el análisis y las comparaciones
- Revisa tus categorías periódicamente

### 3. Revisión Mensual
- Al final de cada mes, revisa tus gastos
- Compara con el presupuesto que tenías planeado
- Identifica áreas de mejora

### 4. Backup de Datos
- El archivo `gastos_mensuales.db` contiene todos tus datos
- Haz copias de seguridad regularmente
- Guarda el archivo en la nube o disco externo

## 🔍 Funciones Avanzadas

### Exportar Datos

Genera un reporte en texto plano:
```bash
python3 utilidades.py
# Selecciona opción 6
```

El archivo generado incluye:
- Total anual
- Gastos detallados por mes
- Estadísticas por categoría
- Porcentajes y cantidades

### Gestionar Categorías

Agregar una nueva categoría:
```bash
python3 utilidades.py
# Selecciona opción 3
```

### Ver Resumen Rápido

Sin abrir la interfaz gráfica:
```bash
python3 utilidades.py
# Selecciona opción 1
```

## 🐛 Solución de Problemas

### La aplicación no inicia
- Verifica que tienes Python 3.6 o superior: `python3 --version`
- Asegúrate de estar en el directorio correcto
- En macOS, Tkinter viene preinstalado con Python

### Error al agregar gasto
- Verifica que el monto sea un número válido (usa punto decimal, no coma)
- La fecha debe ser válida (no puedes poner 30 de febrero)
- Todos los campos son obligatorios

### Los datos no se guardan
- Verifica que tienes permisos de escritura en el directorio
- No cierres la aplicación abruptamente (usa la X de la ventana)
- El archivo `gastos_mensuales.db` no debe estar en uso por otra aplicación

### Quiero empezar de cero
```bash
python3 utilidades.py
# Selecciona opción 5 y confirma
```

**⚠️ ADVERTENCIA**: Esto eliminará TODOS los gastos (no las categorías)

## 📊 Casos de Uso Comunes

### Caso 1: Presupuesto Mensual
1. Define un presupuesto objetivo para cada categoría
2. Registra gastos durante el mes
3. Al final del mes, compara con tu objetivo
4. Ajusta gastos del siguiente mes según resultados

### Caso 2: Ahorro Anual
1. Define un objetivo de ahorro anual
2. Usa la Comparación Anual para ver tu progreso
3. Identifica meses donde gastas más
4. Reduce gastos en categorías no esenciales

### Caso 3: Análisis Familiar
1. Registra todos los gastos del hogar
2. Usa categorías para dividir por tipo (hogar, niños, personal)
3. Genera reportes mensuales
4. Toma decisiones informadas sobre gastos futuros

## 🚀 Tips Pro

1. **Usa comandos de teclado**
   - Tab para moverte entre campos
   - Enter después de llenar el formulario (si configuras el botón)

2. **Nombres de categorías descriptivos**
   - Si tienes muchas subcategorías, usa nombres como:
     - "Transporte - Gasolina"
     - "Transporte - Mantenimiento"
     - "Transporte - Peajes"

3. **Exporta datos regularmente**
   - Al final de cada trimestre o semestre
   - Útil para declaraciones de impuestos
   - Respaldo en formato legible

4. **Análisis de tendencias**
   - Compara los mismos meses de diferentes años
   - Identifica patrones estacionales
   - Planifica mejor gastos predecibles

## 📞 Soporte

Si encuentras problemas o tienes sugerencias:
- Revisa esta guía primero
- Verifica que estás usando Python 3.6+
- Asegúrate de que todos los archivos estén en el mismo directorio

---

¡Feliz gestión de gastos! 💰✨

