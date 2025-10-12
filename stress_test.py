#!/usr/bin/env python3
"""
Pruebas extremas de estrés para la conexión a internet
Extreme stress tests for internet connection
"""

import asyncio
import aiohttp
import subprocess
import threading
import time
import json
import sys
import random
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import psutil
import signal
import os

class NetworkStressTester:
    def __init__(self):
        self.stop_flag = False
        self.results = []
        
    def signal_handler(self, signum, frame):
        print("\n🛑 Deteniendo pruebas de estrés...")
        self.stop_flag = True
        
    def get_network_stats(self):
        """Obtiene estadísticas de red actuales"""
        stats = psutil.net_io_counters()
        return {
            'bytes_sent': stats.bytes_sent,
            'bytes_recv': stats.bytes_recv,
            'packets_sent': stats.packets_sent,
            'packets_recv': stats.packets_recv,
            'timestamp': time.time()
        }
    
    async def download_test_file(self, session, url, test_name, size_mb=100):
        """Descarga un archivo de prueba"""
        try:
            start_time = time.time()
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.read()
                    end_time = time.time()
                    speed_mbps = (len(data) * 8) / (1024 * 1024) / (end_time - start_time)
                    return {
                        'test': test_name,
                        'status': 'success',
                        'size_mb': len(data) / (1024 * 1024),
                        'time_seconds': end_time - start_time,
                        'speed_mbps': speed_mbps,
                        'timestamp': datetime.now().isoformat()
                    }
                else:
                    return {
                        'test': test_name,
                        'status': 'failed',
                        'error': f'HTTP {response.status}',
                        'timestamp': datetime.now().isoformat()
                    }
        except Exception as e:
            return {
                'test': test_name,
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    async def stress_test_concurrent_downloads(self, num_connections=50):
        """Test de descargas concurrentes extremas"""
        print(f"🚀 Iniciando prueba de {num_connections} descargas concurrentes...")
        
        # URLs de archivos de prueba de diferentes tamaños
        test_files = [
            ('http://speedtest.ftp.otenet.gr/files/test10Mb.db', '10MB_file'),
            ('http://speedtest.ftp.otenet.gr/files/test100Mb.db', '100MB_file'),
            ('https://www.learningcontainer.com/wp-content/uploads/2020/05/sample-zip-file.zip', 'small_zip'),
            ('https://file-examples.com/storage/fe86c865d4981618b8bb4d6/2017/10/file_example_JPG_2500kB.jpg', 'large_image'),
        ]
        
        timeout = aiohttp.ClientTimeout(total=300)  # 5 minutos timeout
        
        async with aiohttp.ClientSession(timeout=timeout) as session:
            tasks = []
            
            for i in range(num_connections):
                url, name = random.choice(test_files)
                task_name = f"{name}_{i}"
                task = self.download_test_file(session, url, task_name)
                tasks.append(task)
                
                if self.stop_flag:
                    break
                    
                # Pequeña pausa para no sobrecargar instantáneamente
                await asyncio.sleep(0.1)
            
            print(f"⏳ Ejecutando {len(tasks)} descargas simultáneas...")
            start_stats = self.get_network_stats()
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            end_stats = self.get_network_stats()
            
            # Calcular estadísticas del test
            successful = [r for r in results if isinstance(r, dict) and r.get('status') == 'success']
            failed = [r for r in results if isinstance(r, dict) and r.get('status') in ['failed', 'error']]
            
            total_data_mb = sum(r.get('size_mb', 0) for r in successful)
            total_time = end_stats['timestamp'] - start_stats['timestamp']
            
            print(f"\n📊 RESULTADOS - DESCARGAS CONCURRENTES")
            print("=" * 60)
            print(f"✅ Descargas exitosas: {len(successful)}")
            print(f"❌ Descargas fallidas: {len(failed)}")
            print(f"📦 Datos descargados: {total_data_mb:.2f} MB")
            print(f"⏱️  Tiempo total: {total_time:.2f} segundos")
            print(f"📈 Velocidad promedio: {(total_data_mb * 8) / total_time:.2f} Mbps")
            
            if failed:
                print(f"\n⚠️  Errores encontrados:")
                for error in failed[:5]:  # Mostrar solo los primeros 5
                    print(f"   - {error.get('error', 'Error desconocido')}")
            
            return results
    
    def ping_flood_test(self, target="8.8.8.8", count=1000):
        """Test de ping flood para probar latencia bajo carga"""
        print(f"\n🏓 Iniciando ping flood test a {target} ({count} pings)...")
        
        try:
            result = subprocess.run(
                ['ping', '-c', str(count), '-i', '0.2', target],
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                # Buscar estadísticas de ping
                for line in lines:
                    if 'packet loss' in line:
                        print(f"📊 Pérdida de paquetes: {line}")
                    elif 'min/avg/max' in line or 'rtt' in line:
                        print(f"📊 Estadísticas RTT: {line}")
                        
                return True
            else:
                print(f"❌ Error en ping test: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print("⚠️  Ping test timeout - puede indicar problemas de red")
            return False
        except Exception as e:
            print(f"❌ Error ejecutando ping: {e}")
            return False
    
    def bandwidth_saturation_test(self):
        """Test de saturación de ancho de banda"""
        print("\n🌊 Iniciando test de saturación de ancho de banda...")
        
        try:
            # Múltiples tests de velocidad consecutivos
            for i in range(3):
                print(f"\n📡 Ejecutando speedtest #{i+1}/3...")
                result = subprocess.run(
                    ['speedtest', '--json'],
                    capture_output=True,
                    text=True,
                    timeout=120
                )
                
                if result.returncode == 0:
                    data = json.loads(result.stdout)
                    download_mbps = data['download'] / 1_000_000
                    upload_mbps = data['upload'] / 1_000_000
                    ping_ms = data['ping']
                    
                    print(f"   ⬇️  Bajada: {download_mbps:.2f} Mbps")
                    print(f"   ⬆️  Subida: {upload_mbps:.2f} Mbps")
                    print(f"   📡 Ping: {ping_ms:.2f} ms")
                    
                    self.results.append({
                        'test_type': 'speedtest',
                        'iteration': i + 1,
                        'download_mbps': download_mbps,
                        'upload_mbps': upload_mbps,
                        'ping_ms': ping_ms,
                        'timestamp': datetime.now().isoformat()
                    })
                else:
                    print(f"   ❌ Error en speedtest #{i+1}")
                
                if self.stop_flag:
                    break
                    
                # Pausa entre tests
                time.sleep(5)
                    
        except Exception as e:
            print(f"❌ Error en test de saturación: {e}")
    
    def connection_stability_test(self, duration_minutes=5):
        """Test de estabilidad de conexión durante un período prolongado"""
        print(f"\n🔄 Iniciando test de estabilidad ({duration_minutes} minutos)...")
        
        start_time = time.time()
        end_time = start_time + (duration_minutes * 60)
        
        ping_results = []
        connection_drops = 0
        
        while time.time() < end_time and not self.stop_flag:
            try:
                # Ping a múltiples servidores
                targets = ['8.8.8.8', '1.1.1.1', 'google.com']
                
                for target in targets:
                    result = subprocess.run(
                        ['ping', '-c', '1', '-W', '3', target],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    
                    if result.returncode == 0:
                        # Extraer tiempo de ping
                        for line in result.stdout.split('\n'):
                            if 'time=' in line:
                                ping_time = float(line.split('time=')[1].split(' ')[0])
                                ping_results.append({
                                    'target': target,
                                    'ping_ms': ping_time,
                                    'timestamp': time.time()
                                })
                                break
                    else:
                        connection_drops += 1
                        print(f"⚠️  Conexión caída detectada a {target}")
                
                # Mostrar progreso cada 30 segundos
                elapsed = time.time() - start_time
                if int(elapsed) % 30 == 0:
                    remaining = (duration_minutes * 60) - elapsed
                    print(f"⏱️  Progreso: {elapsed/60:.1f}/{duration_minutes} minutos - {remaining/60:.1f} min restantes")
                
                time.sleep(1)
                
            except Exception as e:
                print(f"❌ Error en stability test: {e}")
                connection_drops += 1
        
        # Análisis de resultados
        if ping_results:
            avg_ping = sum(r['ping_ms'] for r in ping_results) / len(ping_results)
            max_ping = max(r['ping_ms'] for r in ping_results)
            min_ping = min(r['ping_ms'] for r in ping_results)
            
            print(f"\n📊 RESULTADOS - ESTABILIDAD DE CONEXIÓN")
            print("=" * 60)
            print(f"⏱️  Duración del test: {(time.time() - start_time)/60:.2f} minutos")
            print(f"📊 Total pings enviados: {len(ping_results)}")
            print(f"❌ Conexiones caídas: {connection_drops}")
            print(f"📡 Ping promedio: {avg_ping:.2f} ms")
            print(f"📈 Ping máximo: {max_ping:.2f} ms")
            print(f"📉 Ping mínimo: {min_ping:.2f} ms")
            print(f"🎯 Tasa de éxito: {((len(ping_results) / (len(ping_results) + connection_drops)) * 100):.2f}%")
    
    def run_extreme_stress_tests(self):
        """Ejecuta todas las pruebas de estrés extremas"""
        signal.signal(signal.SIGINT, self.signal_handler)
        
        print("🔥 INICIANDO PRUEBAS EXTREMAS DE ESTRÉS DE RED")
        print("=" * 70)
        print("⚠️  ADVERTENCIA: Estas pruebas pueden saturar tu conexión")
        print("⚠️  Presiona Ctrl+C para detener en cualquier momento")
        print("=" * 70)
        
        start_time = datetime.now()
        
        try:
            # 1. Test de descargas concurrentes extremas
            if not self.stop_flag:
                asyncio.run(self.stress_test_concurrent_downloads(100))
            
            # 2. Test de ping flood
            if not self.stop_flag:
                self.ping_flood_test(count=500)
            
            # 3. Test de saturación de ancho de banda
            if not self.stop_flag:
                self.bandwidth_saturation_test()
            
            # 4. Test de estabilidad de conexión
            if not self.stop_flag:
                self.connection_stability_test(duration_minutes=3)
            
            # Resumen final
            end_time = datetime.now()
            duration = end_time - start_time
            
            print(f"\n🏁 RESUMEN FINAL DE PRUEBAS EXTREMAS")
            print("=" * 70)
            print(f"⏱️  Duración total: {duration}")
            print(f"🕐 Inicio: {start_time.strftime('%H:%M:%S')}")
            print(f"🕐 Fin: {end_time.strftime('%H:%M:%S')}")
            
            if self.stop_flag:
                print("⚠️  Las pruebas fueron interrumpidas por el usuario")
            else:
                print("✅ Todas las pruebas completadas exitosamente")
                print("🎉 Tu conexión ha resistido las pruebas extremas!")
                
        except Exception as e:
            print(f"💥 Error durante las pruebas: {e}")

def main():
    """Función principal"""
    tester = NetworkStressTester()
    tester.run_extreme_stress_tests()

if __name__ == "__main__":
    main()