#!/bin/bash

# Verifica si se proporcionó un archivo como argumento
if [ "$#" -ne 1 ]; then
    echo "Uso: $0 <ruta/al/archivo>"
    exit 1
fi

# Asigna el primer argumento a la variable FILE
FILE="$1"

# Verifica si el archivo existe
if [ ! -f "$FILE" ]; then
    echo "Error: El archivo '$FILE' no existe."
    exit 1
fi

echo "Subiendo archivo: $FILE"

# Realiza la solicitud para obtener el servidor de carga
echo "Obteniendo servidor de carga..."
SERVER_RESPONSE=$(curl -s https://api.gofile.io/getServer)
SERVER=$(echo "$SERVER_RESPONSE" | jq -r '.data.server')

# Verifica si se obtuvo un servidor válido
if [ "$SERVER" == "null" ]; then
    echo "Error: No se pudo obtener el servidor de carga."
    echo "Respuesta: $SERVER_RESPONSE"
    exit 1
fi

echo "Servidor obtenido: $SERVER"

# Sube el archivo al servidor obtenido
echo "Subiendo archivo..."
UPLOAD_RESPONSE=$(curl -s -F "file=@$FILE" "https://$SERVER.gofile.io/uploadFile")
STATUS=$(echo "$UPLOAD_RESPONSE" | jq -r '.status')

# Verifica si la carga fue exitosa
if [ "$STATUS" != "ok" ]; then
    echo "Error: No se pudo subir el archivo."
    echo "Respuesta: $UPLOAD_RESPONSE"
    exit 1
fi

# Extrae y muestra el enlace de descarga
DOWNLOAD_LINK=$(echo "$UPLOAD_RESPONSE" | jq -r '.data.downloadPage')
echo "✅ Archivo subido exitosamente!"
echo "🔗 Enlace de descarga: $DOWNLOAD_LINK"