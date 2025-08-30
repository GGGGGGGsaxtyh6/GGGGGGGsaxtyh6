#!/usr/bin/env python3
import os
from mega import Mega

# Crear instancia de Mega
mega = Mega()

# URL del archivo
url = "https://mega.nz/file/1ilSFaYT#qeNny0TDpzDr2CrHVC9f57A3Fxxfa9mmQp4cmREe8zI"

try:
    # Descargar el archivo
    print("Descargando archivo de Mega...")
    m = mega.login()  # Login anónimo
    
    # Descargar el archivo
    file = m.download_url(url, '/workspace/')
    print(f"Archivo descargado exitosamente: {file}")
    
    # Listar archivos en el directorio para ver qué se descargó
    files = os.listdir('/workspace/')
    print("\nArchivos en el directorio:")
    for f in files:
        if not f.startswith('.') and f != 'download_mega.py':
            print(f"  - {f}")
            
except Exception as e:
    print(f"Error al descargar: {e}")