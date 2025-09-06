#!/usr/bin/env python3
"""
Consultor automático de la CNMC para identificación de operadores telefónicos
Envía solicitudes automáticas a https://numeracionyoperadores.cnmc.es/portabilidad/movil
"""

import requests
import json
import re
import time
from datetime import datetime
from urllib.parse import urljoin
import urllib3

# Deshabilitar warnings de SSL para evitar problemas de certificados
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class CNMCAutomatedLookup:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0'
        })
        
        self.base_url = "https://numeracionyoperadores.cnmc.es"
        self.mobile_url = "https://numeracionyoperadores.cnmc.es/portabilidad/movil"
        
    def get_csrf_token(self):
        """Obtiene el token CSRF del formulario"""
        try:
            print("🔐 Obteniendo token CSRF...")
            response = self.session.get(self.mobile_url, verify=False, timeout=30)
            
            if response.status_code == 200:
                # Buscar token CSRF en el HTML
                csrf_match = re.search(r'name="csrf_token"[^>]*value="([^"]*)"', response.text)
                if csrf_match:
                    token = csrf_match.group(1)
                    print(f"   ✅ Token CSRF obtenido: {token[:20]}...")
                    return token
                else:
                    print("   ⚠️ No se encontró token CSRF en el HTML")
                    return None
            else:
                print(f"   ❌ Error HTTP: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"   ❌ Error obteniendo token CSRF: {str(e)}")
            return None

    def get_captcha_info(self):
        """Obtiene información sobre el captcha"""
        try:
            print("🤖 Analizando captcha...")
            response = self.session.get(self.mobile_url, verify=False, timeout=30)
            
            if response.status_code == 200:
                # Buscar información del captcha
                captcha_match = re.search(r'captcha[^>]*src="([^"]*)"', response.text, re.IGNORECASE)
                if captcha_match:
                    captcha_url = captcha_match.group(1)
                    if not captcha_url.startswith('http'):
                        captcha_url = urljoin(self.base_url, captcha_url)
                    print(f"   ✅ Captcha encontrado: {captcha_url}")
                    return captcha_url
                else:
                    print("   ⚠️ No se encontró captcha en el formulario")
                    return None
            else:
                print(f"   ❌ Error HTTP: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"   ❌ Error analizando captcha: {str(e)}")
            return None

    def submit_phone_query(self, phone_number, csrf_token=None, captcha_solution=None):
        """Envía la consulta del número de teléfono"""
        try:
            print(f"📞 Enviando consulta para: {phone_number}")
            
            # Preparar datos del formulario
            form_data = {
                'numero': phone_number,
                'tipo': 'movil'
            }
            
            if csrf_token:
                form_data['csrf_token'] = csrf_token
            
            if captcha_solution:
                form_data['captcha'] = captcha_solution
            
            # Headers adicionales para el POST
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Origin': self.base_url,
                'Referer': self.mobile_url,
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-User': '?1'
            }
            
            print("   📤 Enviando petición POST...")
            response = self.session.post(
                self.mobile_url,
                data=form_data,
                headers=headers,
                verify=False,
                timeout=30,
                allow_redirects=True
            )
            
            print(f"   📊 Respuesta HTTP: {response.status_code}")
            
            if response.status_code == 200:
                return self.parse_response(response.text, phone_number)
            else:
                print(f"   ❌ Error en la respuesta: {response.status_code}")
                return {"error": f"HTTP {response.status_code}", "success": False}
                
        except Exception as e:
            print(f"   ❌ Error enviando consulta: {str(e)}")
            return {"error": str(e), "success": False}

    def parse_response(self, html_content, phone_number):
        """Parsea la respuesta HTML para extraer información del operador"""
        try:
            print("🔍 Analizando respuesta...")
            
            # Buscar información del operador en la respuesta
            operador_match = re.search(r'operador[^>]*>([^<]+)', html_content, re.IGNORECASE)
            if operador_match:
                operador = operador_match.group(1).strip()
                print(f"   ✅ Operador encontrado: {operador}")
            else:
                operador = "No encontrado"
                print("   ⚠️ No se encontró información del operador")
            
            # Buscar otros datos relevantes
            estado_match = re.search(r'estado[^>]*>([^<]+)', html_content, re.IGNORECASE)
            estado = estado_match.group(1).strip() if estado_match else "Desconocido"
            
            tipo_match = re.search(r'tipo[^>]*>([^<]+)', html_content, re.IGNORECASE)
            tipo = tipo_match.group(1).strip() if tipo_match else "Desconocido"
            
            # Buscar mensajes de error
            error_match = re.search(r'error[^>]*>([^<]+)', html_content, re.IGNORECASE)
            error_msg = error_match.group(1).strip() if error_match else None
            
            if error_msg:
                print(f"   ⚠️ Mensaje de error: {error_msg}")
            
            return {
                "success": True,
                "phone_number": phone_number,
                "operador": operador,
                "estado": estado,
                "tipo": tipo,
                "error_message": error_msg,
                "raw_html": html_content[:1000] + "..." if len(html_content) > 1000 else html_content
            }
            
        except Exception as e:
            print(f"   ❌ Error parseando respuesta: {str(e)}")
            return {"error": f"Error parseando: {str(e)}", "success": False}

    def automated_lookup(self, phone_number):
        """Proceso completo de consulta automatizada"""
        print(f"🤖 CONSULTA AUTOMATIZADA CNMC - NÚMERO: {phone_number}")
        print("=" * 80)
        
        # 1. Obtener token CSRF
        print("\n🔐 1. OBTENIENDO TOKEN CSRF:")
        print("-" * 50)
        csrf_token = self.get_csrf_token()
        
        # 2. Analizar captcha
        print("\n🤖 2. ANALIZANDO CAPTCHA:")
        print("-" * 50)
        captcha_url = self.get_captcha_info()
        
        if captcha_url:
            print("   ⚠️ CAPTCHA DETECTADO - Requiere intervención manual")
            print(f"   🌐 URL del captcha: {captcha_url}")
            print("   💡 Solución: Implementar OCR o usar servicio de resolución de captcha")
        
        # 3. Enviar consulta
        print("\n📞 3. ENVIANDO CONSULTA:")
        print("-" * 50)
        result = self.submit_phone_query(phone_number, csrf_token)
        
        # 4. Mostrar resultados
        print("\n📊 4. RESULTADOS:")
        print("-" * 50)
        if result.get("success"):
            print(f"   ✅ ÉXITO:")
            print(f"   📞 Número: {result['phone_number']}")
            print(f"   🏢 Operador: {result['operador']}")
            print(f"   📊 Estado: {result['estado']}")
            print(f"   📱 Tipo: {result['tipo']}")
            if result.get('error_message'):
                print(f"   ⚠️ Mensaje: {result['error_message']}")
        else:
            print(f"   ❌ ERROR: {result.get('error', 'Desconocido')}")
        
        # 5. Recomendaciones
        print("\n💡 5. RECOMENDACIONES:")
        print("-" * 50)
        if captcha_url:
            print("   🤖 Implementar resolución automática de captcha")
            print("   🔍 Usar servicios como 2captcha o Anti-Captcha")
            print("   👁️ Implementar OCR para leer el captcha")
        else:
            print("   ✅ No se detectó captcha - consulta directa posible")
        
        print("   🌐 Consulta manual: https://numeracionyoperadores.cnmc.es/portabilidad/movil")
        print("   📞 Contacta directamente con el operador")
        
        return result

    def test_multiple_numbers(self, phone_numbers):
        """Prueba múltiples números"""
        print(f"🧪 PRUEBA DE MÚLTIPLES NÚMEROS")
        print("=" * 50)
        
        results = []
        for phone in phone_numbers:
            print(f"\n📞 Probando: {phone}")
            result = self.automated_lookup(phone)
            results.append(result)
            time.sleep(2)  # Pausa entre consultas
        
        return results

if __name__ == "__main__":
    lookup = CNMCAutomatedLookup()
    
    # Probar con el número específico
    phone = "689567469"
    result = lookup.automated_lookup(phone)
    
    # También probar con el número anterior
    print("\n" + "="*80)
    phone2 = "644883718"
    result2 = lookup.automated_lookup(phone2)