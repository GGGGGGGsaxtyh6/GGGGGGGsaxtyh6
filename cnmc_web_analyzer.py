#!/usr/bin/env python3
"""
Analizador web de la CNMC para entender la estructura del formulario
"""

import requests
import re
import json
from urllib.parse import urljoin, urlparse
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class CNMCWebAnalyzer:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
        
        self.base_url = "https://numeracionyoperadores.cnmc.es"
        self.mobile_url = "https://numeracionyoperadores.cnmc.es/portabilidad/movil"

    def analyze_page_structure(self):
        """Analiza la estructura de la página web"""
        print("🔍 ANALIZANDO ESTRUCTURA DE LA PÁGINA CNMC")
        print("=" * 60)
        
        try:
            print(f"📡 Conectando a: {self.mobile_url}")
            response = self.session.get(self.mobile_url, verify=False, timeout=30)
            
            print(f"📊 Estado HTTP: {response.status_code}")
            print(f"📄 Tamaño del contenido: {len(response.text)} caracteres")
            print(f"🌐 URL final: {response.url}")
            
            if response.status_code == 200:
                self.analyze_html_content(response.text)
                self.analyze_forms(response.text)
                self.analyze_scripts(response.text)
            else:
                print(f"❌ Error: No se pudo acceder a la página")
                
        except Exception as e:
            print(f"❌ Error conectando: {str(e)}")

    def analyze_html_content(self, html):
        """Analiza el contenido HTML"""
        print("\n📄 ANÁLISIS DEL CONTENIDO HTML:")
        print("-" * 40)
        
        # Buscar título
        title_match = re.search(r'<title[^>]*>([^<]+)</title>', html, re.IGNORECASE)
        if title_match:
            print(f"📋 Título: {title_match.group(1).strip()}")
        
        # Buscar meta description
        desc_match = re.search(r'<meta[^>]*name="description"[^>]*content="([^"]*)"', html, re.IGNORECASE)
        if desc_match:
            print(f"📝 Descripción: {desc_match.group(1).strip()}")
        
        # Buscar campos de entrada
        input_fields = re.findall(r'<input[^>]*name="([^"]*)"[^>]*>', html, re.IGNORECASE)
        if input_fields:
            print(f"🔧 Campos de entrada encontrados: {', '.join(set(input_fields))}")
        
        # Buscar botones
        buttons = re.findall(r'<button[^>]*>([^<]+)</button>', html, re.IGNORECASE)
        if buttons:
            print(f"🔘 Botones encontrados: {', '.join(set(buttons))}")
        
        # Buscar enlaces
        links = re.findall(r'<a[^>]*href="([^"]*)"[^>]*>([^<]+)</a>', html, re.IGNORECASE)
        if links:
            print(f"🔗 Enlaces encontrados: {len(links)}")
            for href, text in links[:5]:  # Mostrar solo los primeros 5
                print(f"   - {text.strip()}: {href}")

    def analyze_forms(self, html):
        """Analiza los formularios en la página"""
        print("\n📝 ANÁLISIS DE FORMULARIOS:")
        print("-" * 40)
        
        forms = re.findall(r'<form[^>]*>(.*?)</form>', html, re.DOTALL | re.IGNORECASE)
        print(f"📋 Formularios encontrados: {len(forms)}")
        
        for i, form in enumerate(forms):
            print(f"\n📝 Formulario {i+1}:")
            
            # Buscar action
            action_match = re.search(r'action="([^"]*)"', form, re.IGNORECASE)
            if action_match:
                print(f"   🎯 Action: {action_match.group(1)}")
            
            # Buscar method
            method_match = re.search(r'method="([^"]*)"', form, re.IGNORECASE)
            if method_match:
                print(f"   📤 Method: {method_match.group(1)}")
            
            # Buscar campos
            inputs = re.findall(r'<input[^>]*name="([^"]*)"[^>]*>', form, re.IGNORECASE)
            if inputs:
                print(f"   🔧 Campos: {', '.join(inputs)}")
            
            # Buscar selects
            selects = re.findall(r'<select[^>]*name="([^"]*)"[^>]*>', form, re.IGNORECASE)
            if selects:
                print(f"   📋 Selects: {', '.join(selects)}")

    def analyze_scripts(self, html):
        """Analiza los scripts JavaScript"""
        print("\n⚙️ ANÁLISIS DE SCRIPTS:")
        print("-" * 40)
        
        scripts = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL | re.IGNORECASE)
        print(f"📜 Scripts encontrados: {len(scripts)}")
        
        for i, script in enumerate(scripts):
            if len(script.strip()) > 50:  # Solo scripts con contenido
                print(f"\n📜 Script {i+1} (primeros 200 caracteres):")
                print(f"   {script.strip()[:200]}...")
                
                # Buscar URLs o endpoints
                urls = re.findall(r'["\']([^"\']*api[^"\']*)["\']', script, re.IGNORECASE)
                if urls:
                    print(f"   🔗 URLs encontradas: {', '.join(urls)}")

    def test_different_endpoints(self):
        """Prueba diferentes endpoints posibles"""
        print("\n🧪 PROBANDO DIFERENTES ENDPOINTS:")
        print("-" * 40)
        
        endpoints = [
            "/portabilidad/movil",
            "/api/portabilidad/movil",
            "/consulta/movil",
            "/api/consulta/movil",
            "/numeracion/movil",
            "/api/numeracion/movil"
        ]
        
        for endpoint in endpoints:
            url = self.base_url + endpoint
            try:
                print(f"🔍 Probando: {url}")
                response = self.session.get(url, verify=False, timeout=10)
                print(f"   📊 Estado: {response.status_code}")
                if response.status_code == 200:
                    print(f"   ✅ Accesible")
                elif response.status_code == 404:
                    print(f"   ❌ No encontrado")
                else:
                    print(f"   ⚠️ Estado inesperado")
            except Exception as e:
                print(f"   ❌ Error: {str(e)}")

    def search_for_api_endpoints(self, html):
        """Busca endpoints de API en el HTML"""
        print("\n🔍 BUSCANDO ENDPOINTS DE API:")
        print("-" * 40)
        
        # Buscar patrones de API
        api_patterns = [
            r'["\']([^"\']*api[^"\']*)["\']',
            r'["\']([^"\']*consulta[^"\']*)["\']',
            r'["\']([^"\']*portabilidad[^"\']*)["\']',
            r'["\']([^"\']*numeracion[^"\']*)["\']'
        ]
        
        all_endpoints = set()
        for pattern in api_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            all_endpoints.update(matches)
        
        if all_endpoints:
            print(f"🔗 Endpoints encontrados:")
            for endpoint in sorted(all_endpoints):
                if endpoint.startswith('/') or endpoint.startswith('http'):
                    print(f"   - {endpoint}")
        else:
            print("   ❌ No se encontraron endpoints de API")

    def comprehensive_analysis(self):
        """Análisis completo de la página"""
        print("🚀 ANÁLISIS COMPLETO DE LA CNMC")
        print("=" * 80)
        
        # 1. Análisis de estructura
        self.analyze_page_structure()
        
        # 2. Prueba de endpoints
        self.test_different_endpoints()
        
        # 3. Recomendaciones
        print("\n💡 RECOMENDACIONES:")
        print("-" * 40)
        print("   🌐 La página puede requerir JavaScript habilitado")
        print("   🔐 Puede tener protección CSRF o captcha")
        print("   📡 Puede usar AJAX para las consultas")
        print("   🤖 Considera usar Selenium para automatización completa")
        print("   📞 Contacta directamente con el operador como alternativa")

if __name__ == "__main__":
    analyzer = CNMCWebAnalyzer()
    analyzer.comprehensive_analysis()