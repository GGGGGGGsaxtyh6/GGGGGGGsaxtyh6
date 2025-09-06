#!/usr/bin/env python3
"""
Script con Playwright que SÍ funciona
"""

import asyncio
import sys

async def consultar_cnmc_playwright(numero):
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        return "Error: Playwright no instalado. Ejecuta: pip install playwright && playwright install"
    
    try:
        async with async_playwright() as p:
            # Lanzar navegador
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            # Ir a la página
            url = "https://numeracionyoperadores.cnmc.es/portabilidad/movil"
            print(f"Accediendo a: {url}")
            await page.goto(url)
            
            # Esperar a que cargue
            print("Esperando a que cargue...")
            await page.wait_for_timeout(5000)
            
            # Buscar campo de entrada
            print("Buscando campo de entrada...")
            try:
                # Esperar a que aparezca cualquier input
                await page.wait_for_selector("input", timeout=10000)
                print("Campo de entrada encontrado")
            except:
                print("No se encontró campo de entrada")
                content = await page.content()
                await browser.close()
                return f"NO SE ENCONTRÓ CAMPO. HTML: {content[:1000]}..."
            
            # Escribir número
            print(f"Escribiendo número: {numero}")
            await page.fill("input", numero)
            
            # Buscar y hacer clic en botón
            try:
                # Intentar diferentes selectores de botón
                button_selectors = [
                    "button[type='submit']",
                    "input[type='submit']", 
                    "button",
                    ".btn",
                    "[role='button']"
                ]
                
                button_clicked = False
                for selector in button_selectors:
                    try:
                        await page.click(selector)
                        print(f"Botón clickeado: {selector}")
                        button_clicked = True
                        break
                    except:
                        continue
                
                if not button_clicked:
                    print("No se encontró botón, intentando con Enter...")
                    await page.press("input", "Enter")
                
            except Exception as e:
                print(f"Error con botón: {e}")
                print("Intentando con Enter...")
                await page.press("input", "Enter")
            
            # Esperar resultados
            print("Esperando resultados...")
            await page.wait_for_timeout(10000)
            
            # Obtener contenido de la página
            content = await page.content()
            
            # Buscar operador en el contenido
            print("Buscando operador...")
            operadores = ['Movistar', 'Orange', 'Vodafone', 'MásMóvil', 'Yoigo', 'Avatel', 'Simyo', 'Pepephone', 'Lowi', 'Digi', 'Finetwork', 'Jazztel', 'Tuenti']
            
            operador_encontrado = None
            for operador in operadores:
                if operador.lower() in content.lower():
                    operador_encontrado = operador
                    print(f"¡OPERADOR ENCONTRADO: {operador}!")
                    break
            
            # Si no se encuentra, buscar en texto visible
            if not operador_encontrado:
                try:
                    visible_text = await page.text_content("body")
                    print(f"Texto visible: {visible_text[:500]}...")
                    
                    for operador in operadores:
                        if operador.lower() in visible_text.lower():
                            operador_encontrado = operador
                            print(f"¡OPERADOR ENCONTRADO EN TEXTO: {operador}!")
                            break
                except Exception as e:
                    print(f"Error obteniendo texto visible: {e}")
            
            await browser.close()
            
            if operador_encontrado:
                return f"OPERADOR: {operador_encontrado}"
            else:
                return f"NO SE ENCONTRÓ OPERADOR. HTML: {content[:1000]}..."
        
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    numero = sys.argv[1] if len(sys.argv) > 1 else "689567469"
    print(f"CONSULTANDO CNMC CON PLAYWRIGHT - NÚMERO: {numero}")
    print("=" * 60)
    resultado = asyncio.run(consultar_cnmc_playwright(numero))
    print("\n" + "=" * 60)
    print("RESULTADO:")
    print("=" * 60)
    print(resultado)