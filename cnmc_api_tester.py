#!/usr/bin/env python3
"""
Probador de APIs de la CNMC
Prueba diferentes endpoints para encontrar la API correcta
"""

import requests
import json
import re
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class CNMCAPITester:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Referer': 'https://numeracionyoperadores.cnmc.es/portabilidad/movil'
        })
        
        self.base_url = "https://numeracionyoperadores.cnmc.es"
        
        # Endpoints encontrados
        self.endpoints = [
            "/consulta/movil",
            "/api/consulta/movil", 
            "/numeracion/movil",
            "/api/numeracion/movil"
        ]

    def test_endpoint_get(self, endpoint, phone_number):
        """Prueba un endpoint con GET"""
        url = self.base_url + endpoint
        print(f"🔍 Probando GET: {url}")
        
        try:
            # Probar con parámetros en query string
            params = {
                'numero': phone_number,
                'telefono': phone_number,
                'movil': phone_number,
                'phone': phone_number
            }
            
            response = self.session.get(url, params=params, verify=False, timeout=30)
            print(f"   📊 Estado: {response.status_code}")
            print(f"   📄 Tamaño: {len(response.text)} caracteres")
            
            if response.status_code == 200:
                return self.analyze_response(response, "GET", endpoint)
            else:
                print(f"   ❌ Error HTTP: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            return None

    def test_endpoint_post(self, endpoint, phone_number):
        """Prueba un endpoint con POST"""
        url = self.base_url + endpoint
        print(f"🔍 Probando POST: {url}")
        
        try:
            # Diferentes formatos de datos
            data_formats = [
                {'numero': phone_number},
                {'telefono': phone_number},
                {'movil': phone_number},
                {'phone': phone_number},
                {'numero_telefono': phone_number},
                {'numero_movil': phone_number}
            ]
            
            for i, data in enumerate(data_formats):
                print(f"   📤 Formato {i+1}: {data}")
                response = self.session.post(url, data=data, verify=False, timeout=30)
                print(f"   📊 Estado: {response.status_code}")
                
                if response.status_code == 200:
                    result = self.analyze_response(response, "POST", endpoint)
                    if result:
                        return result
                elif response.status_code not in [404, 405]:
                    print(f"   ⚠️ Estado inesperado: {response.status_code}")
            
            return None
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            return None

    def test_endpoint_json(self, endpoint, phone_number):
        """Prueba un endpoint con JSON"""
        url = self.base_url + endpoint
        print(f"🔍 Probando JSON: {url}")
        
        try:
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            
            json_data = {
                'numero': phone_number,
                'telefono': phone_number,
                'movil': phone_number
            }
            
            response = self.session.post(url, json=json_data, headers=headers, verify=False, timeout=30)
            print(f"   📊 Estado: {response.status_code}")
            
            if response.status_code == 200:
                return self.analyze_response(response, "JSON", endpoint)
            else:
                print(f"   ❌ Error HTTP: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            return None

    def analyze_response(self, response, method, endpoint):
        """Analiza la respuesta de la API"""
        print(f"   ✅ RESPUESTA EXITOSA:")
        print(f"   📊 Método: {method}")
        print(f"   🔗 Endpoint: {endpoint}")
        print(f"   📄 Tamaño: {len(response.text)} caracteres")
        
        # Intentar parsear como JSON
        try:
            json_data = response.json()
            print(f"   📋 JSON válido: {len(json_data)} campos")
            print(f"   📋 Contenido: {json.dumps(json_data, indent=2)[:500]}...")
            return {
                'success': True,
                'method': method,
                'endpoint': endpoint,
                'data': json_data,
                'type': 'json'
            }
        except:
            pass
        
        # Analizar como HTML
        if '<html' in response.text.lower():
            print(f"   📄 HTML detectado")
            return self.parse_html_response(response.text, method, endpoint)
        
        # Analizar como texto plano
        print(f"   📄 Texto plano: {response.text[:200]}...")
        return {
            'success': True,
            'method': method,
            'endpoint': endpoint,
            'data': response.text,
            'type': 'text'
        }

    def parse_html_response(self, html, method, endpoint):
        """Parsea una respuesta HTML"""
        print(f"   🔍 Analizando HTML...")
        
        # Buscar información del operador
        operador_patterns = [
            r'operador[^>]*>([^<]+)',
            r'empresa[^>]*>([^<]+)',
            r'proveedor[^>]*>([^<]+)',
            r'compañía[^>]*>([^<]+)'
        ]
        
        operador = None
        for pattern in operador_patterns:
            match = re.search(pattern, html, re.IGNORECASE)
            if match:
                operador = match.group(1).strip()
                break
        
        if operador:
            print(f"   🏢 Operador encontrado: {operador}")
        
        return {
            'success': True,
            'method': method,
            'endpoint': endpoint,
            'data': html,
            'type': 'html',
            'operador': operador
        }

    def test_all_endpoints(self, phone_number):
        """Prueba todos los endpoints con diferentes métodos"""
        print(f"🧪 PROBANDO TODOS LOS ENDPOINTS - NÚMERO: {phone_number}")
        print("=" * 80)
        
        results = []
        
        for endpoint in self.endpoints:
            print(f"\n🔗 ENDPOINT: {endpoint}")
            print("-" * 50)
            
            # Probar GET
            result = self.test_endpoint_get(endpoint, phone_number)
            if result:
                results.append(result)
            
            # Probar POST
            result = self.test_endpoint_post(endpoint, phone_number)
            if result:
                results.append(result)
            
            # Probar JSON
            result = self.test_endpoint_json(endpoint, phone_number)
            if result:
                results.append(result)
        
        return results

    def comprehensive_test(self, phone_numbers):
        """Prueba completa con múltiples números"""
        print("🚀 PRUEBA COMPLETA DE APIs CNMC")
        print("=" * 80)
        
        all_results = []
        
        for phone in phone_numbers:
            print(f"\n📞 PROBANDO NÚMERO: {phone}")
            print("=" * 60)
            
            results = self.test_all_endpoints(phone)
            all_results.extend(results)
        
        # Resumen de resultados
        print(f"\n📊 RESUMEN DE RESULTADOS:")
        print("-" * 50)
        print(f"   🔗 Endpoints probados: {len(self.endpoints)}")
        print(f"   📞 Números probados: {len(phone_numbers)}")
        print(f"   ✅ Respuestas exitosas: {len(all_results)}")
        
        if all_results:
            print(f"\n🎯 RESULTADOS EXITOSOS:")
            for i, result in enumerate(all_results):
                print(f"   {i+1}. {result['method']} {result['endpoint']} - {result['type']}")
                if 'operador' in result:
                    print(f"      🏢 Operador: {result['operador']}")
        
        return all_results

if __name__ == "__main__":
    tester = CNMCAPITester()
    
    # Probar con los números que tenemos
    phone_numbers = ["689567469", "644883718"]
    
    results = tester.comprehensive_test(phone_numbers)