#!/bin/bash
echo "[*] Fuzzing API endpoints..."

endpoints=(
    "/"
    "/api"
    "/v1"
    "/v2"
    "/v1/centers"
    "/v1/center"
    "/centers"
    "/center"
    "/campus"
    "/list"
    "/info"
    "/status"
    "/health"
    "/config"
    "/admin"
    "/users"
    "/data"
    "/search"
    "/query"
)

for endpoint in "${endpoints[@]}"; do
    echo "Testing: $endpoint"
    response=$(curl -s "https://api.esic.edu$endpoint" --max-time 3)
    status=$(echo "$response" | head -1)
    echo "$status"
    if [[ ! "$response" =~ "Bad Request: The Center parameter is missing" ]]; then
        echo "DIFFERENT RESPONSE!"
        echo "$response" | head -5
    fi
    echo ""
done
