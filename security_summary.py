#!/usr/bin/env python3
"""
Resumen completo de seguridad de red
"""

import json
import os
from datetime import datetime

def print_security_summary():
    print("\n" + "="*80)
    print("🔒 RESUMEN DE SEGURIDAD DE RED")
    print("="*80)
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Leer reporte JSON si existe
    if os.path.exists('/workspace/network_security_report.json'):
        with open('/workspace/network_security_report.json', 'r') as f:
            report = json.load(f)
        
        print("📊 ESTADÍSTICAS GENERALES:")
        print("-"*40)
        print(f"• Total de conexiones: {len(report['connections'])}")
        print(f"• Conexiones sospechosas: {len(report['suspicious_connections'])}")
        print(f"• Puertos abiertos: {len(report['open_ports'])}")
        print(f"• Alertas generadas: {len(report['alerts'])}")
        print()
        
        print("🔍 ANÁLISIS DETALLADO:")
        print("-"*40)
        
        # Conexiones por estado
        states = {}
        for conn in report['connections']:
            state = conn['state']
            states[state] = states.get(state, 0) + 1
        
        print("Estados de conexión:")
        for state, count in states.items():
            print(f"  • {state}: {count}")
        print()
        
        # IPs externas únicas
        external_ips = set()
        for conn in report['connections']:
            remote_ip = conn['remote'].split(':')[0]
            if not remote_ip.startswith(('0.0.0.0', '127.', '172.', '192.168.', '10.')):
                external_ips.add(remote_ip)
        
        if external_ips:
            print(f"IPs externas conectadas ({len(external_ips)}):")
            for ip in sorted(external_ips):
                print(f"  • {ip}")
            print()
        
        # Puertos en escucha
        if report['open_ports']:
            print("Puertos en escucha:")
            for port in report['open_ports']:
                status = "⚠️" if port.get('suspicious') else "✅"
                print(f"  {status} {port['address']} ({port['protocol']})")
            print()
        
        # Alertas
        if report['alerts']:
            print("⚠️  ALERTAS ACTIVAS:")
            for alert in report['alerts'][:5]:  # Primeras 5 alertas
                print(f"  • {alert}")
            if len(report['alerts']) > 5:
                print(f"  ... y {len(report['alerts'])-5} alertas más")
            print()
    
    print("🛡️  RECOMENDACIONES DE SEGURIDAD:")
    print("-"*40)
    print("1. ✅ Revisar todas las conexiones a IPs externas")
    print("2. ✅ Verificar que los puertos abiertos sean necesarios")
    print("3. ✅ Investigar conexiones sospechosas identificadas")
    print("4. ✅ Configurar firewall para bloquear puertos no utilizados")
    print("5. ✅ Implementar monitoreo continuo de red")
    print("6. ✅ Revisar logs de sistema regularmente")
    print("7. ✅ Mantener el sistema actualizado")
    print()
    
    print("📝 ARCHIVOS GENERADOS:")
    print("-"*40)
    files = [
        ('network_security_analyzer.py', 'Analizador principal de seguridad'),
        ('network_security_report.json', 'Reporte detallado en JSON'),
        ('detailed_connection_analyzer.py', 'Análisis detallado de conexiones'),
        ('realtime_network_monitor.py', 'Monitor en tiempo real'),
        ('security_summary.py', 'Este script de resumen')
    ]
    
    for filename, description in files:
        path = f'/workspace/{filename}'
        if os.path.exists(path):
            size = os.path.getsize(path)
            print(f"  ✅ {filename} ({size:,} bytes)")
            print(f"     {description}")
    
    print("\n" + "="*80)
    print("✅ Análisis de seguridad completado exitosamente")
    print("="*80)

if __name__ == "__main__":
    print_security_summary()