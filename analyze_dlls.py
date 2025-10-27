#!/usr/bin/env python3

import os
import subprocess
import hashlib
import re
from datetime import datetime

def get_file_hash(filepath):
    """Calcula el hash SHA256 del archivo"""
    try:
        with open(filepath, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()
    except:
        return "Error"

def analyze_dll_exports(dll_path):
    """Analiza las funciones exportadas de una DLL"""
    exports = []
    try:
        result = subprocess.run(['strings', dll_path], capture_output=True, text=True)
        lines = result.stdout.split('\n')
        
        # Buscar patrones de funciones exportadas
        for line in lines:
            # Patrones comunes de funciones exportadas
            if re.match(r'^[A-Z][a-zA-Z0-9_]+$', line) and len(line) > 3 and len(line) < 50:
                if any(keyword in line for keyword in ['Create', 'Open', 'Read', 'Write', 'Send', 'Recv', 'Connect', 
                                                        'Hook', 'Inject', 'Load', 'Execute', 'Download', 'Upload',
                                                        'Crypt', 'Decrypt', 'Encrypt', 'Key', 'Password']):
                    exports.append(line)
    except:
        pass
    return list(set(exports))[:10]  # Retornar solo las primeras 10 únicas

def analyze_dll_strings(dll_path):
    """Busca strings sospechosos en la DLL"""
    suspicious = {
        'network': [],
        'registry': [],
        'process': [],
        'crypto': [],
        'persistence': [],
        'data_theft': []
    }
    
    try:
        result = subprocess.run(['strings', '-n', '8', dll_path], capture_output=True, text=True)
        strings = result.stdout.split('\n')
        
        for string in strings:
            string_lower = string.lower()
            
            # Patrones de red
            if any(net in string_lower for net in ['socket', 'connect', 'send', 'recv', 'http', 'https', 'ftp', 'tcp', 'udp']):
                suspicious['network'].append(string[:50])
            
            # Patrones de registro
            if any(reg in string_lower for reg in ['hkey', 'registry', 'regedit', 'currentversion', 'software\\microsoft']):
                suspicious['registry'].append(string[:50])
            
            # Patrones de proceso
            if any(proc in string_lower for proc in ['createprocess', 'openprocess', 'terminateprocess', 'inject', 'hook']):
                suspicious['process'].append(string[:50])
            
            # Patrones de criptografía
            if any(crypto in string_lower for crypto in ['crypt', 'aes', 'rsa', 'base64', 'md5', 'sha', 'encrypt', 'decrypt']):
                suspicious['crypto'].append(string[:50])
            
            # Patrones de persistencia
            if any(pers in string_lower for pers in ['startup', 'run', 'autorun', 'service', 'scheduled', 'task']):
                suspicious['persistence'].append(string[:50])
            
            # Patrones de robo de datos
            if any(theft in string_lower for theft in ['password', 'credential', 'keylog', 'screenshot', 'webcam', 'microphone']):
                suspicious['data_theft'].append(string[:50])
    
    except:
        pass
    
    # Limitar resultados
    for key in suspicious:
        suspicious[key] = list(set(suspicious[key]))[:5]
    
    return suspicious

def check_dll_signature(dll_path):
    """Verifica si la DLL tiene firma digital"""
    try:
        result = subprocess.run(['strings', dll_path], capture_output=True, text=True)
        
        signatures = []
        if 'Microsoft' in result.stdout:
            signatures.append('Microsoft')
        if 'DigiCert' in result.stdout:
            signatures.append('DigiCert')
        if 'VeriSign' in result.stdout:
            signatures.append('VeriSign')
        if 'Entrust' in result.stdout:
            signatures.append('Entrust')
        if 'Alibaba' in result.stdout:
            signatures.append('Alibaba')
            
        return signatures
    except:
        return []

def analyze_dll_metadata(dll_path):
    """Extrae metadatos de la DLL"""
    metadata = {}
    
    try:
        # Buscar información de versión
        result = subprocess.run(['strings', dll_path], capture_output=True, text=True)
        
        # Buscar versión
        version_match = re.search(r'(\d+\.\d+\.\d+\.\d+)', result.stdout)
        if version_match:
            metadata['version'] = version_match.group(1)
        
        # Buscar nombre de compañía
        company_patterns = ['CompanyName', 'Company Name', 'Copyright']
        for pattern in company_patterns:
            if pattern in result.stdout:
                idx = result.stdout.find(pattern)
                snippet = result.stdout[idx:idx+100]
                metadata['company'] = snippet.split('\n')[0]
                break
        
        # Buscar descripción del producto
        if 'ProductName' in result.stdout:
            idx = result.stdout.find('ProductName')
            snippet = result.stdout[idx:idx+100]
            metadata['product'] = snippet.split('\n')[0]
        
        # Tamaño del archivo
        metadata['size'] = os.path.getsize(dll_path)
        
    except:
        pass
    
    return metadata

# Análisis principal
print("="*80)
print("ANÁLISIS PROFUNDO DE DLLs - MALWARE ARLY")
print("="*80)
print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# Lista de DLLs a analizar
dlls = [
    '/workspace/Arly/acproxy.dll',
    '/workspace/Arly/AcXtrnal.dll',
    '/workspace/Arly/alibabacloud-oss-cpp-sdk.dll',
    '/workspace/Arly/cpr.dll',
    '/workspace/Arly/eappprxy.dll',
    '/workspace/Arly/com/ColorManagment.dll',
    '/workspace/Arly/com/COMSupport.dll',
    '/workspace/Arly/com/WATPCSP.dll',
    '/workspace/Arly/data/1.dll',
    '/workspace/Arly/data/dav2mp4.dll',
    '/workspace/Arly/data/DecoderMgr.dll',
    '/workspace/Arly/net/cloud-disk.dll',
    '/workspace/Arly/net/FCore.dll',
    '/workspace/Arly/net/FFCore.dll',
    '/workspace/Arly/net/FFAdvancedColorAdjust.dll',
    '/workspace/Arly/net/FFEffectWidgets.dll'
]

# Analizar cada DLL
for dll_path in dlls:
    if os.path.exists(dll_path):
        dll_name = os.path.basename(dll_path)
        print("\n" + "="*60)
        print(f"DLL: {dll_name}")
        print(f"Ruta: {dll_path}")
        print("="*60)
        
        # Hash
        dll_hash = get_file_hash(dll_path)
        print(f"\n[HASH SHA256]\n{dll_hash}")
        
        # Metadatos
        metadata = analyze_dll_metadata(dll_path)
        if metadata:
            print(f"\n[METADATOS]")
            for key, value in metadata.items():
                print(f"  {key}: {value}")
        
        # Firmas digitales
        signatures = check_dll_signature(dll_path)
        if signatures:
            print(f"\n[FIRMAS DETECTADAS]")
            for sig in signatures:
                print(f"  - {sig}")
        
        # Funciones exportadas sospechosas
        exports = analyze_dll_exports(dll_path)
        if exports:
            print(f"\n[FUNCIONES EXPORTADAS SOSPECHOSAS]")
            for exp in exports:
                print(f"  - {exp}")
        
        # Strings sospechosos
        suspicious = analyze_dll_strings(dll_path)
        
        for category, items in suspicious.items():
            if items:
                print(f"\n[STRINGS SOSPECHOSOS - {category.upper()}]")
                for item in items:
                    print(f"  - {item}")

print("\n" + "="*80)
print("FIN DEL ANÁLISIS")
print("="*80)