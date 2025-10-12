#!/bin/bash

echo "[*] Buscando CVEs conocidas para PHP 7.0.33, Apache 2.4.25, Smarty"
echo ""

echo "[*] PHP 7.0.33 released: 2017"
echo "    - parse_url() bypass CVEs"
echo "    - filter_var() bypass CVEs"
echo "    - Type juggling issues"
echo ""

echo "[*] Apache 2.4.25 (Debian) released: 2016"
echo "    - mod_rewrite issues"
echo "    - Header injection"
echo ""

echo "[*] Smarty 3.1.x"
echo "    - SSTI vulnerabilities"
echo "    - {php} tags (deprecado pero puede funcionar)"
echo "    - {system()} si está habilitado"
echo ""

echo "[*] Curl SSRF bypasses conocidos:"
echo "    - 0://evil.com (protocol confusion)"
echo "    - file:/// (local file access)"
echo "    - dict:// (DICT protocol)"
echo "    - gopher:// (raw TCP)"
echo ""

echo "[*] MySQL stored procedure SQLi:"
echo "    - Dynamic SQL con PREPARE/EXECUTE"
echo "    - Multi-statement execution"
echo ""
