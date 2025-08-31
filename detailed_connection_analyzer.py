#!/usr/bin/env python3
"""
Analizador detallado de conexiones y procesos
"""

import os
import subprocess
import socket
from datetime import datetime

def get_process_details(pid):
    """Obtiene detalles completos de un proceso"""
    details = {}
    try:
        # Nombre del proceso
        with open(f'/proc/{pid}/comm', 'r') as f:
            details['name'] = f.read().strip()
        
        # Línea de comando completa
        with open(f'/proc/{pid}/cmdline', 'r') as f:
            details['cmdline'] = f.read().replace('\0', ' ').strip()
        
        # Estado del proceso
        with open(f'/proc/{pid}/status', 'r') as f:
            status_lines = f.readlines()
            for line in status_lines:
                if line.startswith('State:'):
                    details['state'] = line.split()[1]
                elif line.startswith('Uid:'):
                    details['uid'] = line.split()[1]
                elif line.startswith('Gid:'):
                    details['gid'] = line.split()[1]
        
        # Ejecutable
        try:
            details['exe'] = os.readlink(f'/proc/{pid}/exe')
        except:
            details['exe'] = 'N/A'
        
        # Directorio de trabajo
        try:
            details['cwd'] = os.readlink(f'/proc/{pid}/cwd')
        except:
            details['cwd'] = 'N/A'
            
    except:
        pass
    
    return details

def analyze_connection_details():
    """Análisis detallado de cada conexión"""
    print("\n" + "="*80)
    print("🔬 ANÁLISIS DETALLADO DE CONEXIONES")
    print("="*80)
    
    # Mapeo de inodos a PIDs
    inode_to_pid = {}
    for proc_dir in os.listdir('/proc'):
        if proc_dir.isdigit():
            pid = int(proc_dir)
            try:
                fd_dir = f'/proc/{pid}/fd'
                if os.path.exists(fd_dir):
                    for fd in os.listdir(fd_dir):
                        try:
                            link = os.readlink(f'{fd_dir}/{fd}')
                            if 'socket:' in link:
                                inode = link.split('[')[1].split(']')[0]
                                inode_to_pid[inode] = pid
                        except:
                            pass
            except:
                pass
    
    # Analizar conexiones TCP
    connections_analyzed = 0
    with open('/proc/net/tcp', 'r') as f:
        lines = f.readlines()[1:]
    
    for line in lines:
        parts = line.split()
        if len(parts) >= 10:
            state = parts[3]
            if state == '01':  # ESTABLISHED
                connections_analyzed += 1
                inode = parts[9]
                
                # Decodificar direcciones
                local_hex = parts[1]
                remote_hex = parts[2]
                
                local_ip, local_port = decode_address(local_hex)
                remote_ip, remote_port = decode_address(remote_hex)
                
                print(f"\n📌 Conexión #{connections_analyzed}")
                print(f"   Local:  {local_ip}:{local_port}")
                print(f"   Remoto: {remote_ip}:{remote_port}")
                
                # Obtener información del proceso
                if inode in inode_to_pid:
                    pid = inode_to_pid[inode]
                    proc_details = get_process_details(pid)
                    
                    print(f"   PID: {pid}")
                    print(f"   Proceso: {proc_details.get('name', 'Unknown')}")
                    print(f"   Ejecutable: {proc_details.get('exe', 'N/A')}")
                    print(f"   Comando: {proc_details.get('cmdline', 'N/A')[:100]}")
                    
                    # Análisis de seguridad
                    security_check(remote_ip, remote_port, proc_details)
                else:
                    print("   ⚠️  No se pudo identificar el proceso")
    
    print(f"\n📊 Total de conexiones establecidas analizadas: {connections_analyzed}")

def decode_address(hex_addr):
    """Decodifica dirección hex"""
    try:
        hex_ip, hex_port = hex_addr.split(':')
        ip_bytes = bytes.fromhex(hex_ip)
        ip = socket.inet_ntoa(ip_bytes[::-1])
        port = int(hex_port, 16)
        return ip, port
    except:
        return "Unknown", 0

def security_check(ip, port, proc_details):
    """Verificaciones de seguridad adicionales"""
    alerts = []
    
    # Verificar si es IP privada o pública
    if not ip.startswith(('127.', '10.', '172.', '192.168.', '0.0.0.0')):
        print(f"   🌍 Conexión a IP pública: {ip}")
        
        # Verificar país/región (simulado)
        if port == 443:
            print(f"   🔒 Conexión HTTPS estándar")
        elif port == 80:
            print(f"   🔓 Conexión HTTP no segura")
        elif port > 10000:
            print(f"   ⚠️  Puerto alto no estándar: {port}")
    
    # Verificar proceso sospechoso
    exe = proc_details.get('exe', '')
    if exe and not exe.startswith(('/usr/', '/bin/', '/sbin/')):
        print(f"   ⚠️  Ejecutable en ubicación no estándar: {exe}")

def check_network_statistics():
    """Estadísticas de red adicionales"""
    print("\n" + "="*80)
    print("📈 ESTADÍSTICAS DE RED")
    print("="*80)
    
    try:
        # Estadísticas TCP
        with open('/proc/net/snmp', 'r') as f:
            lines = f.readlines()
            for i in range(0, len(lines), 2):
                if 'Tcp:' in lines[i]:
                    headers = lines[i].split()[1:]
                    values = lines[i+1].split()[1:]
                    
                    stats = dict(zip(headers, values))
                    print("\n📊 Estadísticas TCP:")
                    print(f"   Conexiones activas: {stats.get('CurrEstab', 'N/A')}")
                    print(f"   Conexiones fallidas: {stats.get('AttemptFails', 'N/A')}")
                    print(f"   Resets enviados: {stats.get('OutRsts', 'N/A')}")
                    print(f"   Segmentos retransmitidos: {stats.get('RetransSegs', 'N/A')}")
    except Exception as e:
        print(f"   Error obteniendo estadísticas: {e}")

def check_suspicious_files():
    """Busca archivos sospechosos relacionados con red"""
    print("\n" + "="*80)
    print("🔍 VERIFICACIÓN DE ARCHIVOS SOSPECHOSOS")
    print("="*80)
    
    suspicious_paths = [
        '/tmp',
        '/var/tmp',
        '/dev/shm'
    ]
    
    suspicious_patterns = [
        '.hidden',
        'backdoor',
        'rootkit',
        'exploit'
    ]
    
    found_suspicious = False
    
    for path in suspicious_paths:
        if os.path.exists(path):
            try:
                files = os.listdir(path)
                for file in files:
                    file_lower = file.lower()
                    for pattern in suspicious_patterns:
                        if pattern in file_lower:
                            print(f"   ⚠️  Archivo sospechoso encontrado: {path}/{file}")
                            found_suspicious = True
            except:
                pass
    
    if not found_suspicious:
        print("   ✅ No se encontraron archivos sospechosos en directorios temporales")

def main():
    print("🔒 ANÁLISIS DETALLADO DE SEGURIDAD DE RED")
    print("   Fecha/Hora:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    # Análisis detallado de conexiones
    analyze_connection_details()
    
    # Estadísticas de red
    check_network_statistics()
    
    # Verificación de archivos sospechosos
    check_suspicious_files()
    
    print("\n" + "="*80)
    print("✅ Análisis completado")
    print("="*80)

if __name__ == "__main__":
    main()