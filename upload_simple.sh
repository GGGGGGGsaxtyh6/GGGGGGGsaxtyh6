#!/bin/bash

# Script simplificado para subir a gofile.io sin jq
FILE="$1"

if [ ! -f "$FILE" ]; then
    echo "Error: El archivo '$FILE' no existe."
    exit 1
fi

echo "Subiendo archivo: $FILE"

# Obtener servidor
echo "Obteniendo servidor..."
SERVER_RESPONSE=$(curl -s https://api.gofile.io/getServer)
echo "Respuesta del servidor: $SERVER_RESPONSE"

# Extraer servidor manualmente (sin jq)
SERVER=$(echo "$SERVER_RESPONSE" | grep -o '"server":"[^"]*"' | cut -d'"' -f4)
echo "Servidor extraído: $SERVER"

if [ -z "$SERVER" ]; then
    echo "Error: No se pudo obtener el servidor"
    exit 1
fi

# Subir archivo
echo "Subiendo archivo al servidor $SERVER..."
UPLOAD_RESPONSE=$(curl -s -F "file=@$FILE" "https://$SERVER.gofile.io/uploadFile")
echo "Respuesta de subida: $UPLOAD_RESPONSE"

# Extraer enlace manualmente
DOWNLOAD_LINK=$(echo "$UPLOAD_RESPONSE" | grep -o '"downloadPage":"[^"]*"' | cut -d'"' -f4)

if [ -n "$DOWNLOAD_LINK" ]; then
    echo "✅ Archivo subido exitosamente!"
    echo "🔗 Enlace de descarga: $DOWNLOAD_LINK"
else
    echo "❌ Error al subir el archivo"
    echo "Respuesta completa: $UPLOAD_RESPONSE"
fi