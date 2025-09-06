#!/usr/bin/env python3
"""
Script simple para consultar la CNMC con GET
"""

import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def consultar_cnmc(numero):
    """Consulta la CNMC con GET y devuelve el resultado"""
    url = "https://numeracionyoperadores.cnmc.es/portabilidad/movil"
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    
    try:
        # Probar diferentes parámetros
        params_list = [
            {'numero': numero},
            {'telefono': numero},
            {'movil': numero},
            {'phone': numero},
            {'q': numero}
        ]
        
        for params in params_list:
            print(f"Probando parámetros: {params}")
            response = session.get(url, params=params, verify=False, timeout=30)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200 and len(response.text) > 2000:
                print("Respuesta exitosa:")
                return response.text
            else:
                print(f"Respuesta corta: {len(response.text)} caracteres")
        
        # Si nada funciona, devolver la respuesta básica
        response = session.get(url, verify=False, timeout=30)
        return response.text
        
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    numero = "689567469"
    resultado = consultar_cnmc(numero)
    print(resultado)