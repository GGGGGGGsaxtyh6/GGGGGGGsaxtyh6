#!/usr/bin/env python3
import socket
import sys
import time

def connect_to_service():
    """Conectar al servicio y analizar respuesta"""
    print("🔍 Conectando a 94.237.50.221:58110...")
    
    try:
        # Crear socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10)
        
        # Conectar
        s.connect(('94.237.50.221', 58110))
        print("✅ Conectado exitosamente")
        
        # Recibir datos iniciales
        print("\n📥 Esperando respuesta inicial...")
        data = s.recv(4096)
        print("Respuesta recibida:")
        print("-" * 50)
        print(data.decode('utf-8', errors='ignore'))
        print("-" * 50)
        
        # Intentar enviar algo y ver qué responde
        print("\n📤 Enviando línea vacía...")
        s.send(b"\n")
        
        time.sleep(1)
        
        # Recibir respuesta
        data = s.recv(4096)
        if data:
            print("Respuesta después de enviar:")
            print("-" * 50)
            print(data.decode('utf-8', errors='ignore'))
            print("-" * 50)
        
        # Mantener conexión para más análisis si es necesario
        while True:
            try:
                data = s.recv(4096)
                if not data:
                    break
                print("\nDatos adicionales recibidos:")
                print(data.decode('utf-8', errors='ignore'))
            except socket.timeout:
                print("\n⏱️ Timeout - no más datos")
                break
                
        s.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    connect_to_service()