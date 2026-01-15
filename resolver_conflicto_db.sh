#!/bin/bash
# Script para resolver conflictos en archivos de base de datos SQLite

echo "=== Resolver conflicto en data/usuarios.db ==="
echo ""
echo "Este script te ayudará a resolver conflictos en archivos .db"
echo ""

# Crear backup antes de resolver
echo "1. Creando backup de seguridad..."
cp data/usuarios.db "data/usuarios_backup_conflicto_$(date +%Y%m%d_%H%M%S).db" 2>/dev/null || echo "No se pudo crear backup (puede que no exista conflicto activo)"

echo ""
echo "Selecciona una opción:"
echo "1) Mantener MI versión (--ours)"
echo "2) Usar la versión ENTRANTE (--theirs)"
echo "3) Ver estado de Git"
echo "4) Cancelar"
echo ""
read -p "Opción [1-4]: " opcion

case $opcion in
    1)
        echo "Manteniendo tu versión local..."
        git checkout --ours data/usuarios.db
        git add data/usuarios.db
        echo "Conflicto resuelto. Ahora ejecuta: git commit"
        ;;
    2)
        echo "Usando la versión entrante..."
        git checkout --theirs data/usuarios.db
        git add data/usuarios.db
        echo "Conflicto resuelto. Ahora ejecuta: git commit"
        ;;
    3)
        echo "Estado actual de Git:"
        git status
        ;;
    4)
        echo "Cancelado."
        exit 0
        ;;
    *)
        echo "Opción inválida."
        exit 1
        ;;
esac
