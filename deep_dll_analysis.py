#!/usr/bin/env python3

import os
import subprocess
import re

def analyze_network_capabilities(dll_path):
    """Analiza capacidades de red en la DLL"""
    network_functions = {
        'socket_creation': ['socket', 'WSASocket', 'WSAStartup'],
        'connection': ['connect', 'WSAConnect', 'InternetConnect', 'InternetOpen'],
        'http': ['HttpOpenRequest', 'HttpSendRequest', 'InternetReadFile', 'WinHttpOpen'],
        'data_transfer': ['send', 'recv', 'sendto', 'recvfrom', 'WSASend', 'WSARecv'],
        'dns': ['getaddrinfo', 'gethostbyname', 'DnsQuery'],
        'proxy': ['InternetSetOption', 'WinHttpSetOption', 'ProxyResolver']
    }
    
    found_capabilities = {}
    
    try:
        result = subprocess.run(['strings', dll_path], capture_output=True, text=True)
        content = result.stdout
        
        for category, functions in network_functions.items():
            found = []
            for func in functions:
                if func in content or func.lower() in content.lower():
                    found.append(func)
            if found:
                found_capabilities[category] = found
    except:
        pass
    
    return found_capabilities

def analyze_persistence_mechanisms(dll_path):
    """Busca mecanismos de persistencia"""
    persistence_indicators = {
        'registry': ['RegSetValue', 'RegCreateKey', 'RegOpenKey', 'HKEY_LOCAL_MACHINE', 
                    'HKEY_CURRENT_USER', 'Software\\Microsoft\\Windows\\CurrentVersion\\Run'],
        'services': ['CreateService', 'OpenService', 'StartService', 'ControlService'],
        'scheduled_tasks': ['ITaskScheduler', 'ITask', 'schtasks', 'TaskScheduler'],
        'startup': ['Startup', 'StartupFolder', 'shell:startup'],
        'dll_injection': ['SetWindowsHookEx', 'CreateRemoteThread', 'WriteProcessMemory', 
                         'VirtualAllocEx', 'LoadLibrary', 'GetProcAddress']
    }
    
    found_persistence = {}
    
    try:
        result = subprocess.run(['strings', '-n', '6', dll_path], capture_output=True, text=True)
        content = result.stdout
        
        for category, indicators in persistence_indicators.items():
            found = []
            for indicator in indicators:
                if indicator in content or indicator.lower() in content.lower():
                    found.append(indicator)
            if found:
                found_persistence[category] = found
    except:
        pass
    
    return found_persistence

def analyze_data_exfiltration(dll_path):
    """Busca indicadores de exfiltración de datos"""
    exfil_indicators = {
        'file_operations': ['CreateFile', 'ReadFile', 'WriteFile', 'CopyFile', 'MoveFile'],
        'compression': ['compress', 'zip', 'ZipFile', 'deflate', 'lz4', 'zlib'],
        'encryption': ['CryptEncrypt', 'CryptDecrypt', 'AES', 'RSA', 'RC4', 'Base64'],
        'screenshot': ['BitBlt', 'GetDC', 'CreateCompatibleBitmap', 'screenshot', 'capture'],
        'keylogging': ['GetAsyncKeyState', 'GetKeyState', 'SetWindowsHookEx', 'keylog', 'keyboard'],
        'clipboard': ['GetClipboardData', 'SetClipboardData', 'OpenClipboard'],
        'browser_data': ['chrome', 'firefox', 'edge', 'cookies', 'passwords', 'history']
    }
    
    found_exfil = {}
    
    try:
        result = subprocess.run(['strings', '-n', '5', dll_path], capture_output=True, text=True)
        content = result.stdout
        
        for category, indicators in exfil_indicators.items():
            found = []
            for indicator in indicators:
                if indicator in content or indicator.lower() in content.lower():
                    found.append(indicator)
            if found:
                found_exfil[category] = found
    except:
        pass
    
    return found_exfil

# DLLs más sospechosas a analizar en profundidad
suspicious_dlls = {
    'eappprxy.dll': '/workspace/Arly/eappprxy.dll',
    'WATPCSP.dll': '/workspace/Arly/com/WATPCSP.dll',
    '1.dll': '/workspace/Arly/data/1.dll',
    'cloud-disk.dll': '/workspace/Arly/net/cloud-disk.dll',
    'cpr.dll': '/workspace/Arly/cpr.dll'
}

print("="*80)
print("ANÁLISIS PROFUNDO DE CAPACIDADES MALICIOSAS EN DLLs")
print("="*80)

for dll_name, dll_path in suspicious_dlls.items():
    if os.path.exists(dll_path):
        print(f"\n{'='*60}")
        print(f"DLL: {dll_name}")
        print(f"{'='*60}")
        
        # Análisis de red
        network_caps = analyze_network_capabilities(dll_path)
        if network_caps:
            print("\n[CAPACIDADES DE RED DETECTADAS]")
            for category, functions in network_caps.items():
                print(f"  {category.upper()}:")
                for func in functions:
                    print(f"    - {func}")
        
        # Análisis de persistencia
        persistence = analyze_persistence_mechanisms(dll_path)
        if persistence:
            print("\n[MECANISMOS DE PERSISTENCIA]")
            for category, indicators in persistence.items():
                print(f"  {category.upper()}:")
                for ind in indicators:
                    print(f"    - {ind}")
        
        # Análisis de exfiltración
        exfiltration = analyze_data_exfiltration(dll_path)
        if exfiltration:
            print("\n[CAPACIDADES DE EXFILTRACIÓN DE DATOS]")
            for category, indicators in exfiltration.items():
                print(f"  {category.upper()}:")
                for ind in indicators:
                    print(f"    - {ind}")

# Buscar URLs específicas en las DLLs
print("\n" + "="*80)
print("BÚSQUEDA DE URLs Y DOMINIOS ESPECÍFICOS")
print("="*80)

for dll_name, dll_path in suspicious_dlls.items():
    if os.path.exists(dll_path):
        result = subprocess.run(['strings', dll_path], capture_output=True, text=True)
        
        # Buscar patrones de URL que no sean de certificados
        urls = re.findall(r'https?://(?!.*digicert|.*entrust)[^\s]+', result.stdout)
        domains = re.findall(r'[a-zA-Z0-9\-]+\.(?:com|net|org|io|ru|cn|tk|ml|ga|cf|xyz|top|info|biz|cc|pw|ws|club|site|online|live|space|host|website|tech|app|dev|cloud)\b', result.stdout)
        
        if urls or domains:
            print(f"\n[{dll_name}]")
            if urls:
                print("  URLs encontradas:")
                for url in set(urls[:5]):
                    print(f"    - {url}")
            if domains:
                print("  Dominios encontrados:")
                for domain in set(domains[:5]):
                    if 'digicert' not in domain.lower() and 'entrust' not in domain.lower():
                        print(f"    - {domain}")