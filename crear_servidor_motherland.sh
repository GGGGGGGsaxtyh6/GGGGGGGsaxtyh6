#!/bin/bash

# Idea loca: ¿Y si creo MI PROPIO servidor que responda como motherland.com?
# Y luego intento hacer que el servidor objetivo lo use

echo "[*] Esta idea requeriría:"
echo "    1. Un servidor público que yo controle"
echo "    2. Configurar DNS para un dominio que termine en motherland.com"
echo "    3. Hacer que el servidor objetivo use MI DNS"
echo ""
echo "[-] Esto NO es viable porque:"
echo "    - No controlo motherland.com"
echo "    - No puedo cambiar el DNS del servidor objetivo"
echo "    - El regex requiere que la URL TERMINE en motherland.com"
echo ""
echo "[*] A menos que..."
echo "    ¿Pueda registrar un dominio diferente que el regex acepte?"
echo "    Regex: /motherland\.com$/"
echo "    Solo acepta strings que terminen exactamente con 'motherland.com'"
echo ""
echo "[-] No hay bypass obvio"
