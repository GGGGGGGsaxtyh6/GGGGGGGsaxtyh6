#!/usr/bin/env python3
"""
Script que funciona para consultar la CNMC
"""

import time
import sys

def consultar_cnmc(numero):
    try:
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service
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
        
        # Usar ChromeDriver del sistema
        service = Service("/usr/bin/chromedriver")
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Ir a la página
        url = "https://numeracionyoperadores.cnmc.es/portabilidad/movil"
        print(f"Accediendo a: {url}")
        driver.get(url)
        
        # Esperar a que cargue
        wait = WebDriverWait(driver, 15)
        time.sleep(3)
        
        # Buscar campo de entrada
        print("Buscando campo de entrada...")
        input_selectors = [
            "input[type='tel']",
            "input[name='numero']",
            "input[placeholder*='número']",
            "input[placeholder*='telefono']",
            "input[placeholder*='móvil']"
        ]
        
        input_element = None
        for selector in input_selectors:
            try:
                input_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                print(f"Campo encontrado: {selector}")
                break
            except TimeoutException:
                continue
        
        if not input_element:
            print("No se encontró campo de entrada")
            return driver.page_source
        
        # Escribir número
        print(f"Escribiendo número: {numero}")
        input_element.clear()
        input_element.send_keys(numero)
        
        # Buscar botón
        print("Buscando botón...")
        button_selectors = [
            "button[type='submit']",
            "input[type='submit']",
            "button:contains('Buscar')",
            "button:contains('Consultar')",
            ".btn-primary",
            ".btn-submit"
        ]
        
        button_element = None
        for selector in button_selectors:
            try:
                if ":contains" in selector:
                    text = selector.split(":contains('")[1].split("')")[0]
                    button_element = driver.find_element(By.XPATH, f"//button[contains(text(), '{text}')]")
                else:
                    button_element = driver.find_element(By.CSS_SELECTOR, selector)
                print(f"Botón encontrado: {selector}")
                break
            except NoSuchElementException:
                continue
        
        if not button_element:
            print("No se encontró botón, intentando con Enter...")
            from selenium.webdriver.common.keys import Keys
            input_element.send_keys(Keys.RETURN)
        else:
            print("Haciendo clic en botón...")
            button_element.click()
        
        # Esperar resultados
        print("Esperando resultados...")
        time.sleep(5)
        
        # Obtener resultado
        result = driver.page_source
        
        # Buscar información del operador
        print("Buscando información del operador...")
        operador_keywords = ['Movistar', 'Orange', 'Vodafone', 'MásMóvil', 'Yoigo', 'Avatel', 'Simyo', 'Pepephone', 'Lowi', 'Digi']
        
        for keyword in operador_keywords:
            if keyword.lower() in result.lower():
                print(f"Operador encontrado: {keyword}")
                break
        
        driver.quit()
        
        return result
        
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    numero = sys.argv[1] if len(sys.argv) > 1 else "689567469"
    print(f"Consultando número: {numero}")
    resultado = consultar_cnmc(numero)
    print("\n" + "="*50)
    print("RESULTADO:")
    print("="*50)
    print(resultado)