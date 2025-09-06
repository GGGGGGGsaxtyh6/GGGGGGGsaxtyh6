#!/usr/bin/env python3
"""
Script simple con Selenium para consultar la CNMC
"""

import time
import sys

def consultar_cnmc_selenium(numero):
    """Consulta la CNMC usando Selenium"""
    try:
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.chrome.options import Options
        from selenium.common.exceptions import TimeoutException, NoSuchElementException
    except ImportError:
        return "Error: Selenium no instalado. Ejecuta: pip install selenium"
    
    try:
        # Configurar Chrome
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        driver = webdriver.Chrome(options=chrome_options)
        
        # Ir a la página
        url = "https://numeracionyoperadores.cnmc.es/portabilidad/movil"
        driver.get(url)
        
        # Esperar a que cargue
        wait = WebDriverWait(driver, 10)
        
        # Buscar campo de entrada
        input_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='tel'], input[name='numero'], input[placeholder*='número']")))
        
        # Escribir número
        input_element.clear()
        input_element.send_keys(numero)
        
        # Buscar botón
        button = driver.find_element(By.CSS_SELECTOR, "button[type='submit'], input[type='submit'], .btn-primary")
        
        # Hacer clic
        button.click()
        
        # Esperar resultados
        time.sleep(3)
        
        # Obtener resultado
        result = driver.page_source
        
        driver.quit()
        
        return result
        
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    numero = sys.argv[1] if len(sys.argv) > 1 else "689567469"
    resultado = consultar_cnmc_selenium(numero)
    print(resultado)