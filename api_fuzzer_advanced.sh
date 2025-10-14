#!/bin/bash
echo "[*] Advanced API fuzzing of /api/Script..."

# Test more methods
for method in get_campus get_programs get_areas get_types list index view show fetch load read write create update delete save remove add insert execute run test debug admin panel dashboard config settings; do
    echo "Testing /api/Script/$method"
    response=$(curl -s "https://www.esic.edu/api/Script/$method" --max-time 3 2>/dev/null)
    status=$(echo "$response" | head -c 100)
    if [[ ! "$response" =~ "404 Page Not Found" ]] && [[ -n "$response" ]]; then
        echo "  [+] FOUND! Response: $status"
    fi
done

echo -e "\n[*] Testing POST methods..."
for method in create insert update modify edit delete remove; do
    response=$(curl -s -X POST "https://www.esic.edu/api/Script/$method" -d "test=1" --max-time 3 2>/dev/null | head -c 200)
    if [[ ! "$response" =~ "404 Page Not Found" ]] && [[ -n "$response" ]]; then
        echo "[+] POST /api/Script/$method: $response"
    fi
done
