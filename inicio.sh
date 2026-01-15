#!/bin/bash
# Script de inicio rápido para la aplicación de Gastos Mensuales

echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║                                                                              ║"
echo "║              💰 GESTOR DE GASTOS MENSUALES - INICIO RÁPIDO 💰                ║"
echo "║                                                                              ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo ""
echo "Selecciona una opción:"
echo ""
echo "  1) Ejecutar aplicación"
echo "  2) Agregar datos de ejemplo y ejecutar"
echo "  3) Abrir utilidades de gestión"
echo "  4) Ver resumen del proyecto"
echo "  5) Salir"
echo ""
read -p "Opción [1-5]: " opcion

case $opcion in
    1)
        echo ""
        echo "🚀 Ejecutando aplicación..."
        python3 main.py
        ;;
    2)
        echo ""
        echo "📦 Agregando datos de ejemplo..."
        python3 scripts/agregar_datos_ejemplo.py
        echo ""
        echo "🚀 Ejecutando aplicación..."
        python3 main.py
        ;;
    3)
        echo ""
        echo "🛠️ Abriendo utilidades..."
        python3 src/utilidades.py
        ;;
    4)
        echo ""
        cat docs/RESUMEN_FINAL.txt
        ;;
    5)
        echo ""
        echo "👋 ¡Hasta pronto!"
        exit 0
        ;;
    *)
        echo ""
        echo "❌ Opción no válida"
        exit 1
        ;;
esac

