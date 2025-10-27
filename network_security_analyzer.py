#!/usr/bin/env python3
"""
Script de análisis de seguridad de red
Detecta conexiones sospechosas y actividad anómala
"""

import socket
import subprocess
import os
import json
import re
from datetime import datetime
from collections import defaultdict

class NetworkSecurityAnalyzer:
    def __init__(self):
        self.suspicious_ports = {
            # Backdoors conocidos
            1337, 31337, 12345, 12346, 20034, 20432, 
            # Troyanos comunes
            4444, 5555, 6666, 6667, 7777, 8888, 9999,
            # Servicios potencialmente peligrosos
            135, 139, 445,  # SMB/NetBIOS
            3389,  # RDP
            5900, 5901,  # VNC
            1433, 3306,  # Bases de datos
        }
        
        self.known_malicious_ips = [
            # Lista de IPs maliciosas conocidas (ejemplo)
            "192.168.56.1",  # Añadir IPs reales aquí
        ]
        
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "connections": [],
            "suspicious_connections": [],
            "open_ports": [],
            "processes": [],
            "alerts": []
        }
    
    def check_proc_net_tcp(self):
        """Analiza conexiones TCP desde /proc/net/tcp"""
        connections = []
        try:
            with open('/proc/net/tcp', 'r') as f:
                lines = f.readlines()[1:]  # Skip header
                
            for line in lines:
                parts = line.split()
                if len(parts) >= 10:
                    local_addr = self.decode_address(parts[1])
                    remote_addr = self.decode_address(parts[2])
                    state = self.get_tcp_state(parts[3])
                    uid = int(parts[7])
                    inode = parts[9]
                    
                    conn = {
                        "type": "TCP",
                        "local": local_addr,
                        "remote": remote_addr,
                        "state": state,
                        "uid": uid,
                        "inode": inode
                    }
                    
                    # Verificar si es sospechosa
                    if self.is_suspicious_connection(conn):
                        self.results["suspicious_connections"].append(conn)
                        self.results["alerts"].append(
                            f"⚠️ Conexión sospechosa: {local_addr} -> {remote_addr} (Estado: {state})"
                        )
                    
                    connections.append(conn)
                    
        except Exception as e:
            self.results["alerts"].append(f"Error leyendo /proc/net/tcp: {e}")
        
        return connections
    
    def check_proc_net_udp(self):
        """Analiza conexiones UDP desde /proc/net/udp"""
        connections = []
        try:
            with open('/proc/net/udp', 'r') as f:
                lines = f.readlines()[1:]  # Skip header
                
            for line in lines:
                parts = line.split()
                if len(parts) >= 10:
                    local_addr = self.decode_address(parts[1])
                    remote_addr = self.decode_address(parts[2])
                    uid = int(parts[7])
                    inode = parts[9]
                    
                    conn = {
                        "type": "UDP",
                        "local": local_addr,
                        "remote": remote_addr,
                        "state": "ACTIVE",
                        "uid": uid,
                        "inode": inode
                    }
                    
                    connections.append(conn)
                    
        except Exception as e:
            self.results["alerts"].append(f"Error leyendo /proc/net/udp: {e}")
        
        return connections
    
    def decode_address(self, hex_addr):
        """Decodifica direcciones hex del formato /proc/net"""
        try:
            hex_ip, hex_port = hex_addr.split(':')
            
            # Convertir IP
            ip_bytes = bytes.fromhex(hex_ip)
            ip = socket.inet_ntoa(ip_bytes[::-1])
            
            # Convertir puerto
            port = int(hex_port, 16)
            
            return f"{ip}:{port}"
        except:
            return hex_addr
    
    def get_tcp_state(self, state_hex):
        """Convierte estado TCP hex a string"""
        states = {
            '01': 'ESTABLISHED',
            '02': 'SYN_SENT',
            '03': 'SYN_RECV',
            '04': 'FIN_WAIT1',
            '05': 'FIN_WAIT2',
            '06': 'TIME_WAIT',
            '07': 'CLOSE',
            '08': 'CLOSE_WAIT',
            '09': 'LAST_ACK',
            '0A': 'LISTEN',
            '0B': 'CLOSING'
        }
        return states.get(state_hex, 'UNKNOWN')
    
    def is_suspicious_connection(self, conn):
        """Determina si una conexión es sospechosa"""
        suspicious = False
        
        # Verificar puertos sospechosos
        local_port = int(conn["local"].split(':')[1])
        remote_port = int(conn["remote"].split(':')[1])
        
        if local_port in self.suspicious_ports or remote_port in self.suspicious_ports:
            suspicious = True
        
        # Verificar IPs maliciosas
        remote_ip = conn["remote"].split(':')[0]
        if remote_ip in self.known_malicious_ips:
            suspicious = True
        
        # Verificar conexiones externas no estándar
        if not remote_ip.startswith(('127.', '0.0.0.0', '::')) and remote_port > 10000:
            if conn["state"] == "ESTABLISHED":
                suspicious = True
        
        return suspicious
    
    def check_listening_ports(self):
        """Identifica puertos en escucha"""
        listening = []
        
        # Verificar TCP
        tcp_conns = self.check_proc_net_tcp()
        for conn in tcp_conns:
            if conn["state"] == "LISTEN":
                port = int(conn["local"].split(':')[1])
                listening.append({
                    "port": port,
                    "protocol": "TCP",
                    "address": conn["local"],
                    "suspicious": port in self.suspicious_ports
                })
                
                if port in self.suspicious_ports:
                    self.results["alerts"].append(
                        f"🔴 Puerto sospechoso en escucha: {port}/TCP"
                    )
        
        return listening
    
    def get_process_info(self):
        """Obtiene información de procesos con conexiones de red"""
        processes = []
        
        try:
            # Buscar procesos por inodos
            for proc_dir in os.listdir('/proc'):
                if proc_dir.isdigit():
                    try:
                        pid = int(proc_dir)
                        fd_dir = f'/proc/{pid}/fd'
                        
                        if os.path.exists(fd_dir):
                            for fd in os.listdir(fd_dir):
                                try:
                                    link = os.readlink(f'{fd_dir}/{fd}')
                                    if 'socket:' in link:
                                        inode = link.split('[')[1].split(']')[0]
                                        
                                        # Obtener nombre del proceso
                                        with open(f'/proc/{pid}/comm', 'r') as f:
                                            comm = f.read().strip()
                                        
                                        # Obtener cmdline
                                        with open(f'/proc/{pid}/cmdline', 'r') as f:
                                            cmdline = f.read().replace('\0', ' ').strip()
                                        
                                        processes.append({
                                            "pid": pid,
                                            "name": comm,
                                            "cmdline": cmdline[:100],  # Limitar longitud
                                            "inode": inode
                                        })
                                except:
                                    pass
                    except:
                        pass
        except Exception as e:
            self.results["alerts"].append(f"Error obteniendo información de procesos: {e}")
        
        return processes
    
    def check_iptables_rules(self):
        """Verifica reglas de firewall"""
        try:
            result = subprocess.run(['iptables', '-L', '-n', '-v'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                return result.stdout
        except:
            pass
        return None
    
    def analyze_network_interfaces(self):
        """Analiza interfaces de red"""
        interfaces = []
        try:
            with open('/proc/net/dev', 'r') as f:
                lines = f.readlines()[2:]  # Skip headers
                
            for line in lines:
                parts = line.split(':')
                if len(parts) == 2:
                    iface = parts[0].strip()
                    stats = parts[1].split()
                    
                    if len(stats) >= 8:
                        interfaces.append({
                            "interface": iface,
                            "rx_bytes": int(stats[0]),
                            "rx_packets": int(stats[1]),
                            "tx_bytes": int(stats[8]),
                            "tx_packets": int(stats[9])
                        })
        except Exception as e:
            self.results["alerts"].append(f"Error analizando interfaces: {e}")
        
        return interfaces
    
    def generate_report(self):
        """Genera reporte de seguridad"""
        print("\n" + "="*80)
        print("📊 ANÁLISIS DE SEGURIDAD DE RED")
        print("="*80)
        print(f"🕐 Fecha/Hora: {self.results['timestamp']}")
        print()
        
        # Conexiones TCP
        tcp_conns = self.check_proc_net_tcp()
        self.results["connections"].extend(tcp_conns)
        print(f"📡 Conexiones TCP encontradas: {len(tcp_conns)}")
        
        # Conexiones UDP
        udp_conns = self.check_proc_net_udp()
        self.results["connections"].extend(udp_conns)
        print(f"📡 Conexiones UDP encontradas: {len(udp_conns)}")
        
        # Puertos en escucha
        listening = self.check_listening_ports()
        self.results["open_ports"] = listening
        print(f"🔌 Puertos en escucha: {len(listening)}")
        
        # Procesos
        processes = self.get_process_info()
        self.results["processes"] = processes
        print(f"⚙️  Procesos con conexiones: {len(processes)}")
        
        # Interfaces
        interfaces = self.analyze_network_interfaces()
        print(f"🌐 Interfaces de red activas: {len(interfaces)}")
        
        print("\n" + "-"*80)
        print("🔍 CONEXIONES ACTIVAS")
        print("-"*80)
        
        # Mostrar conexiones establecidas
        established = [c for c in tcp_conns if c["state"] == "ESTABLISHED"]
        if established:
            print("\n✅ Conexiones ESTABLECIDAS:")
            for conn in established[:10]:  # Limitar a 10
                print(f"   {conn['local']} -> {conn['remote']}")
            if len(established) > 10:
                print(f"   ... y {len(established)-10} más")
        
        # Mostrar puertos en escucha
        if listening:
            print("\n👂 Puertos en ESCUCHA:")
            for port in listening[:10]:
                status = "⚠️" if port["suspicious"] else "✅"
                print(f"   {status} {port['address']} ({port['protocol']})")
        
        # Mostrar alertas
        if self.results["alerts"]:
            print("\n" + "-"*80)
            print("⚠️  ALERTAS DE SEGURIDAD")
            print("-"*80)
            for alert in self.results["alerts"]:
                print(f"   {alert}")
        else:
            print("\n✅ No se detectaron conexiones sospechosas")
        
        # Mostrar conexiones sospechosas detalladas
        if self.results["suspicious_connections"]:
            print("\n" + "-"*80)
            print("🔴 CONEXIONES SOSPECHOSAS DETECTADAS")
            print("-"*80)
            for conn in self.results["suspicious_connections"]:
                print(f"\n   Tipo: {conn['type']}")
                print(f"   Local: {conn['local']}")
                print(f"   Remoto: {conn['remote']}")
                print(f"   Estado: {conn['state']}")
                print(f"   UID: {conn['uid']}")
        
        # Estadísticas de interfaces
        if interfaces:
            print("\n" + "-"*80)
            print("📊 ESTADÍSTICAS DE INTERFACES")
            print("-"*80)
            for iface in interfaces:
                if iface["rx_packets"] > 0 or iface["tx_packets"] > 0:
                    print(f"\n   Interface: {iface['interface']}")
                    print(f"   RX: {iface['rx_bytes']:,} bytes ({iface['rx_packets']:,} paquetes)")
                    print(f"   TX: {iface['tx_bytes']:,} bytes ({iface['tx_packets']:,} paquetes)")
        
        # Guardar reporte JSON
        with open('/workspace/network_security_report.json', 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print("\n" + "="*80)
        print("📄 Reporte completo guardado en: network_security_report.json")
        print("="*80)
        
        # Recomendaciones
        print("\n🛡️  RECOMENDACIONES DE SEGURIDAD:")
        print("-"*80)
        print("1. Revisa todas las conexiones establecidas a IPs externas")
        print("2. Verifica que los puertos en escucha sean necesarios")
        print("3. Considera usar un firewall para bloquear puertos no utilizados")
        print("4. Monitorea regularmente las conexiones de red")
        print("5. Investiga cualquier proceso desconocido con conexiones activas")
        
        if self.results["suspicious_connections"]:
            print("\n⚠️  ACCIÓN REQUERIDA:")
            print("   Se detectaron conexiones sospechosas.")
            print("   Revisa el archivo network_security_report.json para más detalles.")

def main():
    print("🔒 Iniciando análisis de seguridad de red...")
    print("   Esto puede tomar unos segundos...\n")
    
    analyzer = NetworkSecurityAnalyzer()
    analyzer.generate_report()

if __name__ == "__main__":
    main()