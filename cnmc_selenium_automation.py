#!/usr/bin/env python3
"""
Automatización con Selenium para la CNMC
Requiere instalar selenium y un driver de navegador
"""

import time
import json
from datetime import datetime

# Intentar importar selenium
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    from selenium.common.exceptions import TimeoutException, NoSuchElementException
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

class CNMCSeleniumAutomation:
    def __init__(self):
        self.base_url = "https://numeracionyoperadores.cnmc.es/portabilidad/movil"
        self.driver = None
        
    def setup_driver(self):
        """Configura el driver de Selenium"""
        if not SELENIUM_AVAILABLE:
            print("❌ Selenium no está disponible")
            print("💡 Instala con: pip install selenium")
            return False
        
        try:
            print("🔧 Configurando driver de Chrome...")
            chrome_options = Options()
            chrome_options.add_argument("--headless")  # Ejecutar sin interfaz gráfica
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            
            self.driver = webdriver.Chrome(options=chrome_options)
            print("✅ Driver configurado correctamente")
            return True
            
        except Exception as e:
            print(f"❌ Error configurando driver: {str(e)}")
            print("💡 Asegúrate de tener ChromeDriver instalado")
            return False

    def query_phone_number(self, phone_number):
        """Consulta un número de teléfono usando Selenium"""
        if not self.driver:
            print("❌ Driver no configurado")
            return None
        
        try:
            print(f"🌐 Navegando a: {self.base_url}")
            self.driver.get(self.base_url)
            
            # Esperar a que la página cargue
            wait = WebDriverWait(self.driver, 10)
            
            # Buscar el campo de entrada del número
            print("🔍 Buscando campo de entrada...")
            input_selectors = [
                "input[name='numero']",
                "input[name='telefono']",
                "input[name='movil']",
                "input[type='tel']",
                "input[placeholder*='número']",
                "input[placeholder*='telefono']",
                "input[placeholder*='móvil']"
            ]
            
            input_element = None
            for selector in input_selectors:
                try:
                    input_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                    print(f"✅ Campo encontrado: {selector}")
                    break
                except TimeoutException:
                    continue
            
            if not input_element:
                print("❌ No se encontró el campo de entrada")
                return None
            
            # Limpiar y escribir el número
            print(f"📝 Escribiendo número: {phone_number}")
            input_element.clear()
            input_element.send_keys(phone_number)
            
            # Buscar el botón de envío
            print("🔍 Buscando botón de envío...")
            button_selectors = [
                "button[type='submit']",
                "input[type='submit']",
                "button:contains('Buscar')",
                "button:contains('Consultar')",
                "button:contains('Enviar')",
                ".btn-primary",
                ".btn-submit"
            ]
            
            button_element = None
            for selector in button_selectors:
                try:
                    if ":contains" in selector:
                        button_element = self.driver.find_element(By.XPATH, f"//button[contains(text(), '{selector.split(':contains(')[1].split(')')[0]}')]")
                    else:
                        button_element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    print(f"✅ Botón encontrado: {selector}")
                    break
                except NoSuchElementException:
                    continue
            
            if not button_element:
                print("❌ No se encontró el botón de envío")
                return None
            
            # Hacer clic en el botón
            print("🖱️ Haciendo clic en el botón...")
            button_element.click()
            
            # Esperar a que aparezcan los resultados
            print("⏳ Esperando resultados...")
            time.sleep(3)
            
            # Buscar información del operador en la página
            result = self.extract_operator_info(phone_number)
            return result
            
        except Exception as e:
            print(f"❌ Error durante la consulta: {str(e)}")
            return None

    def extract_operator_info(self, phone_number):
        """Extrae información del operador de la página de resultados"""
        try:
            print("🔍 Extrayendo información del operador...")
            
            # Buscar patrones de información del operador
            operador_patterns = [
                "//*[contains(text(), 'Operador') or contains(text(), 'operador')]",
                "//*[contains(text(), 'Empresa') or contains(text(), 'empresa')]",
                "//*[contains(text(), 'Proveedor') or contains(text(), 'proveedor')]",
                "//*[contains(text(), 'Compañía') or contains(text(), 'compañía')]"
            ]
            
            operador = None
            for pattern in operador_patterns:
                try:
                    elements = self.driver.find_elements(By.XPATH, pattern)
                    for element in elements:
                        text = element.text.strip()
                        if text and len(text) > 3 and len(text) < 100:
                            operador = text
                            print(f"✅ Operador encontrado: {operador}")
                            break
                    if operador:
                        break
                except:
                    continue
            
            # Si no se encuentra con XPath, buscar en el texto de la página
            if not operador:
                page_text = self.driver.page_source
                operador_keywords = ['Movistar', 'Orange', 'Vodafone', 'MásMóvil', 'Yoigo', 'Avatel', 'Simyo', 'Pepephone', 'Lowi', 'Digi']
                
                for keyword in operador_keywords:
                    if keyword.lower() in page_text.lower():
                        operador = keyword
                        print(f"✅ Operador encontrado en texto: {operador}")
                        break
            
            # Capturar screenshot para debug
            screenshot_path = f"/workspace/cnmc_result_{phone_number}_{int(time.time())}.png"
            try:
                self.driver.save_screenshot(screenshot_path)
                print(f"📸 Screenshot guardado: {screenshot_path}")
            except:
                pass
            
            return {
                'success': True,
                'phone_number': phone_number,
                'operador': operador or 'No encontrado',
                'timestamp': datetime.now().isoformat(),
                'screenshot': screenshot_path if 'screenshot_path' in locals() else None
            }
            
        except Exception as e:
            print(f"❌ Error extrayendo información: {str(e)}")
            return {
                'success': False,
                'phone_number': phone_number,
                'error': str(e)
            }

    def close_driver(self):
        """Cierra el driver"""
        if self.driver:
            self.driver.quit()
            print("🔒 Driver cerrado")

    def automated_query(self, phone_numbers):
        """Consulta automatizada de múltiples números"""
        print("🤖 CONSULTA AUTOMATIZADA CON SELENIUM")
        print("=" * 60)
        
        if not self.setup_driver():
            return []
        
        results = []
        
        try:
            for phone in phone_numbers:
                print(f"\n📞 Consultando: {phone}")
                print("-" * 40)
                
                result = self.query_phone_number(phone)
                if result:
                    results.append(result)
                    print(f"✅ Resultado: {result['operador']}")
                else:
                    print("❌ No se pudo obtener resultado")
                
                # Pausa entre consultas
                time.sleep(2)
        
        finally:
            self.close_driver()
        
        return results

    def show_results(self, results):
        """Muestra los resultados de forma organizada"""
        print(f"\n📊 RESULTADOS FINALES:")
        print("=" * 60)
        
        if not results:
            print("❌ No se obtuvieron resultados")
            return
        
        for i, result in enumerate(results, 1):
            print(f"\n{i}. Número: {result['phone_number']}")
            if result['success']:
                print(f"   🏢 Operador: {result['operador']}")
                print(f"   ⏰ Timestamp: {result['timestamp']}")
                if result.get('screenshot'):
                    print(f"   📸 Screenshot: {result['screenshot']}")
            else:
                print(f"   ❌ Error: {result.get('error', 'Desconocido')}")

if __name__ == "__main__":
    if not SELENIUM_AVAILABLE:
        print("❌ SELENIUM NO DISPONIBLE")
        print("=" * 50)
        print("Para instalar Selenium:")
        print("1. pip install selenium")
        print("2. Descargar ChromeDriver desde: https://chromedriver.chromium.org/")
        print("3. Añadir ChromeDriver al PATH")
        print("\n💡 Alternativa: Usar la consulta manual en:")
        print("   https://numeracionyoperadores.cnmc.es/portabilidad/movil")
    else:
        automation = CNMCSeleniumAutomation()
        phone_numbers = ["689567469", "644883718"]
        results = automation.automated_query(phone_numbers)
        automation.show_results(results)