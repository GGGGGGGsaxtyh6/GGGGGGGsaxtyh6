#!/usr/bin/env python3
import socket
import sys
import time
import select

def interact_with_service():
    """Interactuar con el servicio de forma más agresiva"""
    print("🔍 Conectando a 94.237.50.221:58110...")
    
    try:
        # Crear socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)  # Timeout más corto para respuestas rápidas
        
        # Conectar
        s.connect(('94.237.50.221', 58110))
        print("✅ Conectado exitosamente\n")
        
        # Función para recibir datos sin bloquear
        def receive_data():
            try:
                data = s.recv(4096)
                if data:
                    return data.decode('utf-8', errors='ignore')
            except socket.timeout:
                pass
            except:
                pass
            return None
        
        # Intentar recibir datos iniciales
        print("📥 Intentando recibir datos iniciales...")
        initial = receive_data()
        if initial:
            print("Respuesta inicial:")
            print("=" * 50)
            print(initial)
            print("=" * 50)
        else:
            print("No hay datos iniciales, el servidor espera input\n")
        
        # Probar diferentes comandos comunes
        test_commands = [
            "",           # Línea vacía
            "help",       # Comando help
            "HELP",       # HELP mayúsculas
            "?",          # Símbolo de ayuda
            "1",          # Número
            "test",       # Palabra test
            "start",      # Start
            "begin",      # Begin
            "hello",      # Hello
            "flag",       # Flag directo
            "0",          # Cero
            "a",          # Letra
        ]
        
        print("\n🧪 Probando diferentes comandos...")
        for cmd in test_commands:
            print(f"\n📤 Enviando: '{cmd}'")
            s.send((cmd + "\n").encode())
            time.sleep(0.5)  # Pequeña pausa
            
            response = receive_data()
            if response:
                print(f"📥 Respuesta:")
                print("-" * 40)
                print(response)
                print("-" * 40)
                
                # Si encontramos algo interesante, analizar más
                if any(keyword in response.lower() for keyword in ['sequence', 'compute', 'calculate', 'solve', 'input', 'output', 'pattern', 'number', 'htb{', 'flag']):
                    print("⚠️ RESPUESTA INTERESANTE DETECTADA!")
                    # Continuar interactuando si encontramos algo relevante
                    break
        
        # Intentar recibir más datos
        print("\n📥 Esperando más datos...")
        for _ in range(5):
            time.sleep(1)
            extra = receive_data()
            if extra:
                print("Datos adicionales:")
                print(extra)
        
        s.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    interact_with_service()