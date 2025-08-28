#!/usr/bin/env python3
import socket
import sys
import time
import select
import threading

def connect_robust():
    """Conexión robusta que captura todo"""
    print("🔍 Iniciando conexión robusta a 94.237.50.221:58110...")
    
    try:
        # Crear socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('94.237.50.221', 58110))
        print("✅ Conectado!\n")
        
        # Variable para almacenar todos los datos recibidos
        all_data = []
        
        # Thread para recibir datos continuamente
        def receiver():
            while True:
                try:
                    # Usar select para no bloquear
                    ready = select.select([s], [], [], 0.1)
                    if ready[0]:
                        data = s.recv(4096)
                        if not data:
                            print("\n⚠️ Conexión cerrada por el servidor")
                            break
                        decoded = data.decode('utf-8', errors='ignore')
                        all_data.append(decoded)
                        print(f"📥 RECIBIDO:\n{decoded}")
                        print("-" * 50)
                except Exception as e:
                    if "timed out" not in str(e):
                        print(f"Error recibiendo: {e}")
                    break
        
        # Iniciar thread receptor
        recv_thread = threading.Thread(target=receiver)
        recv_thread.daemon = True
        recv_thread.start()
        
        # Esperar un poco para recibir datos iniciales
        time.sleep(2)
        
        # Si no hay datos iniciales, enviar algo
        if not all_data:
            print("📤 No hay datos iniciales. Enviando newline...")
            s.send(b"\n")
            time.sleep(1)
        
        # Esperar más datos
        time.sleep(3)
        
        # Si aún no hay datos, probar otros inputs
        if not all_data:
            print("\n🧪 Probando diferentes inputs...")
            test_inputs = ["", "1", "help", "?", "start", "0"]
            for inp in test_inputs:
                print(f"📤 Enviando: '{inp}'")
                s.send((inp + "\n").encode())
                time.sleep(1)
                if all_data:
                    break
        
        # Esperar un poco más
        time.sleep(2)
        
        print("\n📊 RESUMEN DE DATOS RECIBIDOS:")
        print("=" * 60)
        if all_data:
            for data in all_data:
                print(data)
        else:
            print("No se recibieron datos del servidor")
        print("=" * 60)
        
        s.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    connect_robust()