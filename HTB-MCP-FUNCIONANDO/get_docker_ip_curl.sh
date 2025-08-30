#!/bin/bash

# Leer el token
TOKEN=$(grep HTB_TOKEN .env | cut -d'=' -f2)

echo "[*] Intentando obtener IP del docker con curl..."

# Endpoints a probar
endpoints=(
    "https://labs.hackthebox.com/api/v4/challenge/365/docker"
    "https://labs.hackthebox.com/api/v4/challenge/365/instance"
    "https://labs.hackthebox.com/api/v4/challenge/365/spawn"
    "https://labs.hackthebox.com/api/v4/challenge/365/connection"
    "https://labs.hackthebox.com/api/v4/challenge/docker/365"
    "https://labs.hackthebox.com/api/v4/docker/challenge/365"
    "https://labs.hackthebox.com/api/v4/instance/1661428"
    "https://labs.hackthebox.com/api/v4/docker/1661428"
    "https://labs.hackthebox.com/api/v4/sp/challenge/365"
    "https://www.hackthebox.com/api/v4/challenge/365/docker"
    "https://app.hackthebox.com/api/v4/challenge/365/docker"
)

for endpoint in "${endpoints[@]}"; do
    echo ""
    echo "[*] Probando: $endpoint"
    curl -s -H "Authorization: Bearer $TOKEN" \
         -H "User-Agent: Mozilla/5.0" \
         -H "Accept: application/json" \
         "$endpoint" | head -200
done

# También intentar con POST para obtener la conexión
echo ""
echo "[*] Intentando POST para obtener conexión..."
curl -X POST -s -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -H "User-Agent: Mozilla/5.0" \
     -d '{"challenge_id": 365}' \
     "https://labs.hackthebox.com/api/v4/challenge/connection" | head -200