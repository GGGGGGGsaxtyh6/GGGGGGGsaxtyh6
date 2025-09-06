#!/usr/bin/env python3
"""
Script final que funciona sin Selenium
Usa requests con headers realistas
"""

import requests
import urllib3
import json
import re
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def consultar_cnmc(numero):
    """Consulta la CNMC y devuelve el resultado completo"""
    url = "https://numeracionyoperadores.cnmc.es/portabilidad/movil"
    
    session = requests.Session()
    
    # Headers realistas de un navegador real
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
        print(f"1. Obteniendo página inicial...")
        response = session.get(url, verify=False, timeout=30)
        print(f"   Status: {response.status_code}")
        print(f"   Tamaño: {len(response.text)} caracteres")
        
        if response.status_code != 200:
            return f"Error: No se pudo acceder (Status: {response.status_code})"
        
        # Buscar información en el HTML
        html = response.text
        print(f"2. Analizando contenido HTML...")
        
        # Buscar el título
        title_match = re.search(r'<title[^>]*>([^<]+)</title>', html, re.IGNORECASE)
        if title_match:
            print(f"   Título: {title_match.group(1).strip()}")
        
        # Buscar formularios
        forms = re.findall(r'<form[^>]*>(.*?)</form>', html, re.DOTALL | re.IGNORECASE)
        print(f"   Formularios encontrados: {len(forms)}")
        
        # Buscar campos de entrada
        inputs = re.findall(r'<input[^>]*name="([^"]*)"[^>]*>', html, re.IGNORECASE)
        if inputs:
            print(f"   Campos de entrada: {', '.join(set(inputs))}")
        
        # Buscar scripts
        scripts = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL | re.IGNORECASE)
        print(f"   Scripts encontrados: {len(scripts)}")
        
        # Buscar endpoints de API en los scripts
        api_endpoints = []
        for script in scripts:
            endpoints = re.findall(r'["\']([^"\']*api[^"\']*)["\']', script, re.IGNORECASE)
            api_endpoints.extend(endpoints)
        
        if api_endpoints:
            print(f"   Endpoints de API: {', '.join(set(api_endpoints))}")
        
        # Probar diferentes métodos de consulta
        print(f"3. Probando consulta con número: {numero}")
        
        # Método 1: GET con parámetros
        params = {'numero': numero}
        response_get = session.get(url, params=params, verify=False, timeout=30)
        print(f"   GET con parámetros - Status: {response_get.status_code}, Tamaño: {len(response_get.text)}")
        
        # Método 2: POST con datos
        data = {'numero': numero}
        response_post = session.post(url, data=data, verify=False, timeout=30)
        print(f"   POST con datos - Status: {response_post.status_code}, Tamaño: {len(response_post.text)}")
        
        # Método 3: POST con JSON
        json_data = {'numero': numero}
        response_json = session.post(url, json=json_data, verify=False, timeout=30)
        print(f"   POST con JSON - Status: {response_json.status_code}, Tamaño: {len(response_json.text)}")
        
        # Devolver la respuesta más completa
        responses = [
            ("GET inicial", response),
            ("GET con parámetros", response_get),
            ("POST con datos", response_post),
            ("POST con JSON", response_json)
        ]
        
        # Elegir la respuesta más larga (probablemente más completa)
        best_response = max(responses, key=lambda x: len(x[1].text))
        print(f"4. Mejor respuesta: {best_response[0]} ({len(best_response[1].text)} caracteres)")
        
        return best_response[1].text
        
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    import sys
    numero = sys.argv[1] if len(sys.argv) > 1 else "689567469"
    print(f"CONSULTANDO CNMC - NÚMERO: {numero}")
    print("=" * 60)
    resultado = consultar_cnmc(numero)
    print("\n" + "=" * 60)
    print("RESULTADO COMPLETO:")
    print("=" * 60)
    print(resultado)