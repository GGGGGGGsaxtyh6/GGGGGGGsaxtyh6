#!/bin/bash

# 🔒 Security Audit Toolkit - Preparado para análisis completo
# Autor: IA Autónomo
# Fecha: $(date)

echo "🔍 Security Audit Toolkit v1.0"
echo "================================"

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para verificar si una herramienta está instalada
check_tool() {
    if command -v $1 &> /dev/null; then
        echo -e "${GREEN}✓${NC} $1 instalado"
        return 0
    else
        echo -e "${RED}✗${NC} $1 no encontrado"
        return 1
    fi
}

echo -e "\n${BLUE}[*] Verificando herramientas disponibles...${NC}"
echo "-------------------------------------------"

# Herramientas de red y web
check_tool nmap
check_tool nikto
check_tool sqlmap
check_tool curl
check_tool wget

# Herramientas de análisis de código
check_tool git
check_tool python3
check_tool pip3

# Herramientas adicionales
check_tool grep
check_tool find
check_tool sed
check_tool awk

echo -e "\n${YELLOW}[!] Toolkit preparado y listo para auditoría${NC}"
echo "Esperando la URL o archivos de la página web para comenzar el análisis..."