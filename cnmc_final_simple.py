#!/usr/bin/env python3
"""
Script final simple para consultar la CNMC
Simula un navegador real
"""

import requests
import urllib3
import json
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def consultar_cnmc(numero):
    """Consulta la CNMC simulando un navegador real"""
    url = "https://numeracionyoperadores.cnmc.es/portabilidad/movil"
    
    session = requests.Session()
    
    # Headers más realistas
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Cache-Control': 'max-age=0'
    })
    
    try:
        # 1. GET inicial
        print(f"1. Obteniendo página inicial...")
        response = session.get(url, verify=False, timeout=30)
        print(f"   Status: {response.status_code}")
        
        if response.status_code != 200:
            return f"Error: No se pudo acceder a la página (Status: {response.status_code})"
        
        # 2. Buscar formulario o API endpoint
        html = response.text
        print(f"   Tamaño HTML: {len(html)} caracteres")
        
        # Buscar endpoints de API en el JavaScript
        api_endpoints = re.findall(r'["\']([^"\']*api[^"\']*)["\']', html)
        if api_endpoints:
            print(f"   Endpoints encontrados: {api_endpoints}")
        
        # 3. Probar diferentes métodos
        methods = [
            {'method': 'GET', 'params': {'numero': numero}},
            {'method': 'GET', 'params': {'telefono': numero}},
            {'method': 'POST', 'data': {'numero': numero}},
            {'method': 'POST', 'data': {'telefono': numero}},
            {'method': 'POST', 'json': {'numero': numero}},
        ]
        
        for method_info in methods:
            method = method_info['method']
            print(f"\n2. Probando {method}...")
            
            try:
                if method == 'GET':
                    response = session.get(url, params=method_info['params'], verify=False, timeout=30)
                elif method == 'POST':
                    if 'json' in method_info:
                        response = session.post(url, json=method_info['json'], verify=False, timeout=30)
                    else:
                        response = session.post(url, data=method_info['data'], verify=False, timeout=30)
                
                print(f"   Status: {response.status_code}")
                print(f"   Tamaño: {len(response.text)} caracteres")
                
                # Si la respuesta es diferente, mostrarla
                if response.status_code == 200 and len(response.text) > 2000:
                    print("   ✅ Respuesta exitosa!")
                    return response.text
                elif response.status_code != 200:
                    print(f"   ❌ Error: {response.status_code}")
                else:
                    print("   ⚠️ Respuesta corta")
                    
            except Exception as e:
                print(f"   ❌ Error: {str(e)}")
        
        # 4. Devolver la respuesta inicial si nada funciona
        print(f"\n3. Devolviendo respuesta inicial...")
        return response.text
        
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    import sys
    numero = sys.argv[1] if len(sys.argv) > 1 else "689567469"
    print(f"Consultando número: {numero}")
    print("=" * 50)
    resultado = consultar_cnmc(numero)
    print("\n" + "=" * 50)
    print("RESULTADO:")
    print("=" * 50)
    print(resultado)