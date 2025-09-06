#!/usr/bin/env python3
"""
Script simple para consultar la CNMC
Solo consulta y devuelve el resultado
"""

import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def consultar_cnmc(numero):
    """Consulta la CNMC y devuelve el resultado"""
    url = "https://numeracionyoperadores.cnmc.es/portabilidad/movil"
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    
    try:
        # GET inicial para obtener la página
        response = session.get(url, verify=False, timeout=30)
        print(f"GET Status: {response.status_code}")
        
        # POST con el número
        data = {'numero': numero}
        response = session.post(url, data=data, verify=False, timeout=30)
        print(f"POST Status: {response.status_code}")
        
        return response.text
        
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    numero = "689567469"
    resultado = consultar_cnmc(numero)
    print(resultado)