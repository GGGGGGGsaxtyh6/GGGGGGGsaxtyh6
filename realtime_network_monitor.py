#!/usr/bin/env python3
"""
Monitor de red en tiempo real
Detecta cambios y nuevas conexiones sospechosas
"""

import time
import os
import socket
from datetime import datetime
from collections import defaultdict

class RealtimeNetworkMonitor:
    def __init__(self):
        self.previous_connections = set()
        self.alert_log = []
        self.suspicious_ports = {
            # Backdoors y troyanos
            1337, 31337, 12345, 12346, 4444, 5555, 6666, 6667, 7777, 8888, 9999,
            # Servicios potencialmente peligrosos
            135, 139, 445, 3389, 5900, 5901, 1433, 3306,
            # Puertos comunes de malware
            2222, 3333, 4000, 5000, 6000, 7000, 8000, 9000, 10000,
            20000, 30000, 40000, 50000, 60000
        }
        
    def decode_address(self, hex_addr):
        """Decodifica dirección hex"""
        try:
            hex_ip, hex_port = hex_addr.split(':')
            ip_bytes = bytes.fromhex(hex_ip)
            ip = socket.inet_ntoa(ip_bytes[::-1])
            port = int(hex_port, 16)
            return f"{ip}:{port}"
        except:
            return "Unknown"
    
    def get_tcp_state(self, state_hex):
        """Convierte estado TCP"""
        states = {
            '01': 'ESTABLISHED', '02': 'SYN_SENT', '03': 'SYN_RECV',
            '04': 'FIN_WAIT1', '05': 'FIN_WAIT2', '06': 'TIME_WAIT',
            '07': 'CLOSE', '08': 'CLOSE_WAIT', '09': 'LAST_ACK',
            '0A': 'LISTEN', '0B': 'CLOSING'
        }
        return states.get(state_hex, 'UNKNOWN')
    
    def get_current_connections(self):
        """Obtiene conexiones actuales"""
        connections = []
        
        try:
            with open('/proc/net/tcp', 'r') as f:
                lines = f.readlines()[1:]
                
            for line in lines:
                parts = line.split()
                if len(parts) >= 10:
                    local = self.decode_address(parts[1])
                    remote = self.decode_address(parts[2])
                    state = self.get_tcp_state(parts[3])
                    uid = int(parts[7])
                    
                    conn_str = f"{local}->{remote}:{state}"
                    connections.append({
                        'str': conn_str,
                        'local': local,
                        'remote': remote,
                        'state': state,
                        'uid': uid
                    })
        except Exception as e:
            print(f"Error leyendo conexiones: {e}")
        
        return connections
    
    def check_suspicious(self, conn):
        """Verifica si una conexión es sospechosa"""
        alerts = []
        
        # Extraer puerto
        try:
            local_port = int(conn['local'].split(':')[1])
            remote_port = int(conn['remote'].split(':')[1])
            remote_ip = conn['remote'].split(':')[0]
            
            # Verificar puertos sospechosos
            if local_port in self.suspicious_ports:
                alerts.append(f"Puerto local sospechoso: {local_port}")
            if remote_port in self.suspicious_ports:
                alerts.append(f"Puerto remoto sospechoso: {remote_port}")
            
            # Verificar conexiones externas en puertos altos
            if not remote_ip.startswith(('127.', '0.0.0.0', '172.', '192.168.', '10.')):
                if remote_port > 10000 and remote_port not in [443, 80]:
                    alerts.append(f"Conexión externa a puerto alto: {remote_port}")
                
                # Conexiones establecidas desde root
                if conn['uid'] == 0 and conn['state'] == 'ESTABLISHED':
                    alerts.append("Conexión establecida desde root")
            
            # Múltiples conexiones al mismo destino
            if conn['state'] == 'ESTABLISHED' and remote_port not in [80, 443]:
                alerts.append("Conexión no-web establecida")
        except:
            pass
        
        return alerts
    
    def monitor_loop(self, interval=5):
        """Loop principal de monitoreo"""
        print("🔒 MONITOR DE RED EN TIEMPO REAL")
        print("="*80)
        print(f"Intervalo de verificación: {interval} segundos")
        print("Presiona Ctrl+C para detener\n")
        
        iteration = 0
        
        try:
            while True:
                iteration += 1
                current_time = datetime.now().strftime("%H:%M:%S")
                
                # Obtener conexiones actuales
                current_connections = self.get_current_connections()
                current_set = {conn['str'] for conn in current_connections}
                
                # Detectar nuevas conexiones
                new_connections = current_set - self.previous_connections
                closed_connections = self.previous_connections - current_set
                
                # Mostrar cambios
                if new_connections or closed_connections or iteration == 1:
                    print(f"\n[{current_time}] Verificación #{iteration}")
                    print("-"*60)
                    
                    # Estadísticas
                    established = sum(1 for c in current_connections if c['state'] == 'ESTABLISHED')
                    listening = sum(1 for c in current_connections if c['state'] == 'LISTEN')
                    
                    print(f"📊 Total: {len(current_connections)} | Establecidas: {established} | Escuchando: {listening}")
                    
                    # Nuevas conexiones
                    if new_connections:
                        print(f"\n✨ NUEVAS CONEXIONES ({len(new_connections)}):")
                        for conn_str in new_connections:
                            # Buscar detalles de la conexión
                            for conn in current_connections:
                                if conn['str'] == conn_str:
                                    print(f"   + {conn_str}")
                                    
                                    # Verificar si es sospechosa
                                    alerts = self.check_suspicious(conn)
                                    if alerts:
                                        print(f"     ⚠️  ALERTA: {', '.join(alerts)}")
                                        self.alert_log.append({
                                            'time': current_time,
                                            'connection': conn_str,
                                            'alerts': alerts
                                        })
                    
                    # Conexiones cerradas
                    if closed_connections:
                        print(f"\n🔚 CONEXIONES CERRADAS ({len(closed_connections)}):")
                        for conn_str in closed_connections:
                            print(f"   - {conn_str}")
                    
                    # Conexiones sospechosas activas
                    suspicious_active = []
                    for conn in current_connections:
                        if conn['state'] == 'ESTABLISHED':
                            alerts = self.check_suspicious(conn)
                            if alerts:
                                suspicious_active.append((conn, alerts))
                    
                    if suspicious_active:
                        print(f"\n🔴 CONEXIONES SOSPECHOSAS ACTIVAS ({len(suspicious_active)}):")
                        for conn, alerts in suspicious_active[:5]:  # Limitar a 5
                            print(f"   ! {conn['str']}")
                            print(f"     Razón: {', '.join(alerts)}")
                
                # Actualizar estado
                self.previous_connections = current_set
                
                # Esperar
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n\n" + "="*80)
            print("🛑 Monitor detenido")
            
            # Resumen de alertas
            if self.alert_log:
                print(f"\n📋 RESUMEN DE ALERTAS ({len(self.alert_log)} total):")
                for alert in self.alert_log[-10:]:  # Últimas 10 alertas
                    print(f"   [{alert['time']}] {alert['connection']}")
                    for a in alert['alerts']:
                        print(f"      - {a}")
            
            print("="*80)

def main():
    monitor = RealtimeNetworkMonitor()
    
    # Opciones de monitoreo
    print("\n🔍 OPCIONES DE MONITOREO:")
    print("1. Monitoreo rápido (cada 2 segundos)")
    print("2. Monitoreo normal (cada 5 segundos)")
    print("3. Monitoreo lento (cada 10 segundos)")
    
    try:
        choice = input("\nSelecciona opción (1-3) [default: 2]: ").strip()
        
        if choice == '1':
            interval = 2
        elif choice == '3':
            interval = 10
        else:
            interval = 5
        
        monitor.monitor_loop(interval)
        
    except Exception as e:
        print(f"Error: {e}")
        # Ejecutar con configuración por defecto
        monitor.monitor_loop(5)

if __name__ == "__main__":
    main()