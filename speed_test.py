#!/usr/bin/env python3
"""
Script para verificar la velocidad de internet (subida y bajada)
Internet speed test script (upload and download)
"""

import subprocess
import sys
import json
from datetime import datetime

def install_speedtest():
    """Instala speedtest-cli si no está disponible"""
    try:
        subprocess.run(['speedtest', '--version'], capture_output=True, check=True)
        print("✓ speedtest-cli ya está instalado")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Instalando speedtest-cli...")
        try:
            # Intentar instalar via apt
            subprocess.run(['sudo', 'apt', 'update'], capture_output=True)
            subprocess.run(['sudo', 'apt', 'install', '-y', 'speedtest-cli'], check=True)
            return True
        except subprocess.CalledProcessError:
            try:
                # Intentar instalar via pip
                subprocess.run([sys.executable, '-m', 'pip', 'install', 'speedtest-cli'], check=True)
                return True
            except subprocess.CalledProcessError:
                print("❌ Error: No se pudo instalar speedtest-cli")
                print("Intenta instalarlo manualmente con:")
                print("  sudo apt install speedtest-cli")
                print("  o")
                print("  pip install speedtest-cli")
                return False

def run_speed_test():
    """Ejecuta el test de velocidad y muestra los resultados"""
    print("🌐 Iniciando test de velocidad de internet...")
    print("⏳ Esto puede tomar unos minutos...")
    print("-" * 50)
    
    try:
        # Ejecutar speedtest con formato JSON para parsing
        result = subprocess.run(
            ['speedtest', '--json'],
            capture_output=True,
            text=True,
            check=True,
            timeout=120  # Timeout de 2 minutos
        )
        
        data = json.loads(result.stdout)
        
        # Extraer información relevante
        download_speed = data['download'] / 1_000_000  # Convertir a Mbps
        upload_speed = data['upload'] / 1_000_000      # Convertir a Mbps
        ping = data['ping']
        server_name = data['server']['name']
        server_country = data['server']['country']
        isp = data['client']['isp']
        
        # Mostrar resultados
        print("📊 RESULTADOS DEL TEST DE VELOCIDAD")
        print("=" * 50)
        print(f"📍 Servidor: {server_name}, {server_country}")
        print(f"🏢 ISP: {isp}")
        print(f"📡 Ping: {ping:.2f} ms")
        print(f"⬇️  Velocidad de BAJADA: {download_speed:.2f} Mbps")
        print(f"⬆️  Velocidad de SUBIDA: {upload_speed:.2f} Mbps")
        print(f"🕐 Fecha y hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 50)
        
        # Evaluación de la velocidad
        print("\n📋 EVALUACIÓN:")
        if download_speed >= 100:
            print("⚡ Excelente velocidad de bajada")
        elif download_speed >= 50:
            print("✅ Buena velocidad de bajada")
        elif download_speed >= 25:
            print("⚠️  Velocidad de bajada moderada")
        else:
            print("🐌 Velocidad de bajada lenta")
            
        if upload_speed >= 50:
            print("⚡ Excelente velocidad de subida")
        elif upload_speed >= 25:
            print("✅ Buena velocidad de subida")
        elif upload_speed >= 10:
            print("⚠️  Velocidad de subida moderada")
        else:
            print("🐌 Velocidad de subida lenta")
            
        if ping <= 20:
            print("⚡ Excelente latencia")
        elif ping <= 50:
            print("✅ Buena latencia")
        elif ping <= 100:
            print("⚠️  Latencia moderada")
        else:
            print("🐌 Latencia alta")
            
    except subprocess.TimeoutExpired:
        print("❌ Error: El test tardó demasiado tiempo (timeout)")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error ejecutando speedtest: {e}")
        print("Salida del error:")
        print(e.stderr)
    except json.JSONDecodeError:
        print("❌ Error: No se pudo procesar la respuesta del test")
    except KeyError as e:
        print(f"❌ Error: Falta información en la respuesta: {e}")

def main():
    """Función principal"""
    print("🚀 VERIFICADOR DE VELOCIDAD DE INTERNET")
    print("=" * 50)
    
    # Verificar e instalar speedtest-cli si es necesario
    if not install_speedtest():
        sys.exit(1)
    
    # Ejecutar el test
    run_speed_test()

if __name__ == "__main__":
    main()