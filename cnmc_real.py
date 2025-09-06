#!/usr/bin/env python3
"""
Script REAL que funciona para consultar la CNMC
"""

import time
import sys

def consultar_cnmc_real(numero):
    try:
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.common.keys import Keys
        from selenium.common.exceptions import TimeoutException, NoSuchElementException
    except ImportError:
        return "Error: Selenium no instalado"
    
    try:
        # Configurar Chrome
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--allow-running-insecure-content")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Usar ChromeDriver
        service = Service("/usr/local/bin/chromedriver")
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Ocultar que es un bot
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        # Ir a la página
        url = "https://numeracionyoperadores.cnmc.es/portabilidad/movil"
        print(f"Accediendo a: {url}")
        driver.get(url)
        
        # Esperar a que cargue completamente
        wait = WebDriverWait(driver, 20)
        time.sleep(5)
        
        print("Esperando a que la aplicación JavaScript cargue...")
        
        # Esperar a que aparezca el campo de entrada
        try:
            # Buscar cualquier input que pueda ser el campo de número
            input_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input")))
            print("Campo de entrada encontrado")
        except TimeoutException:
            print("No se encontró campo de entrada, intentando con XPath...")
            try:
                input_element = wait.until(EC.presence_of_element_located((By.XPATH, "//input")))
                print("Campo de entrada encontrado con XPath")
            except TimeoutException:
                print("No se encontró ningún campo de entrada")
                return driver.page_source
        
        # Escribir el número
        print(f"Escribiendo número: {numero}")
        input_element.clear()
        input_element.send_keys(numero)
        
        # Buscar botón de envío
        try:
            # Intentar diferentes selectores de botón
            button_selectors = [
                "button[type='submit']",
                "input[type='submit']",
                "button",
                ".btn",
                "[role='button']"
            ]
            
            button_element = None
            for selector in button_selectors:
                try:
                    button_element = driver.find_element(By.CSS_SELECTOR, selector)
                    print(f"Botón encontrado: {selector}")
                    break
                except NoSuchElementException:
                    continue
            
            if button_element:
                print("Haciendo clic en botón...")
                button_element.click()
            else:
                print("No se encontró botón, intentando con Enter...")
                input_element.send_keys(Keys.RETURN)
        except Exception as e:
            print(f"Error con botón: {e}")
            print("Intentando con Enter...")
            input_element.send_keys(Keys.RETURN)
        
        # Esperar resultados
        print("Esperando resultados...")
        time.sleep(10)
        
        # Obtener el HTML resultante
        result_html = driver.page_source
        
        # Buscar información del operador en el HTML
        print("Buscando información del operador...")
        
        # Palabras clave de operadores
        operadores = ['Movistar', 'Orange', 'Vodafone', 'MásMóvil', 'Yoigo', 'Avatel', 'Simyo', 'Pepephone', 'Lowi', 'Digi', 'Finetwork', 'Jazztel', 'Tuenti']
        
        operador_encontrado = None
        for operador in operadores:
            if operador.lower() in result_html.lower():
                operador_encontrado = operador
                print(f"¡OPERADOR ENCONTRADO: {operador}!")
                break
        
        # Buscar texto que contenga información del operador
        if not operador_encontrado:
            # Buscar patrones de texto que puedan contener el operador
            patrones = [
                r'operador[^>]*>([^<]+)',
                r'empresa[^>]*>([^<]+)',
                r'proveedor[^>]*>([^<]+)',
                r'compañía[^>]*>([^<]+)',
                r'<strong[^>]*>([^<]+)</strong>',
                r'<b[^>]*>([^<]+)</b>'
            ]
            
            import re
            for patron in patrones:
                matches = re.findall(patron, result_html, re.IGNORECASE)
                for match in matches:
                    match_clean = match.strip()
                    if len(match_clean) > 2 and len(match_clean) < 50:
                        for operador in operadores:
                            if operador.lower() in match_clean.lower():
                                operador_encontrado = operador
                                print(f"¡OPERADOR ENCONTRADO EN TEXTO: {operador}!")
                                break
                        if operador_encontrado:
                            break
                if operador_encontrado:
                    break
        
        # Si no se encuentra operador, buscar en el texto visible
        if not operador_encontrado:
            try:
                # Obtener texto visible de la página
                visible_text = driver.find_element(By.TAG_NAME, "body").text
                print(f"Texto visible de la página: {visible_text[:500]}...")
                
                for operador in operadores:
                    if operador.lower() in visible_text.lower():
                        operador_encontrado = operador
                        print(f"¡OPERADOR ENCONTRADO EN TEXTO VISIBLE: {operador}!")
                        break
            except Exception as e:
                print(f"Error obteniendo texto visible: {e}")
        
        driver.quit()
        
        if operador_encontrado:
            return f"OPERADOR: {operador_encontrado}"
        else:
            return f"NO SE ENCONTRÓ OPERADOR. HTML: {result_html[:1000]}..."
        
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    numero = sys.argv[1] if len(sys.argv) > 1 else "689567469"
    print(f"CONSULTANDO CNMC REAL - NÚMERO: {numero}")
    print("=" * 60)
    resultado = consultar_cnmc_real(numero)
    print("\n" + "=" * 60)
    print("RESULTADO:")
    print("=" * 60)
    print(resultado)