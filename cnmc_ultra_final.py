#!/usr/bin/env python3
"""
Script ULTRA FINAL que maneja el CAPTCHA
"""

import asyncio
import sys
import re
import time

async def consultar_cnmc_ultra_final(numero):
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        return "Error: Playwright no instalado"
    
    try:
        async with async_playwright() as p:
            # Lanzar navegador
            browser = await p.chromium.launch(
                headless=True,  # Headless para evitar problemas
                args=[
                    '--no-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-web-security',
                    '--allow-running-insecure-content',
                    '--disable-blink-features=AutomationControlled',
                    '--disable-features=VizDisplayCompositor'
                ]
            )
            
            context = await browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                viewport={'width': 1920, 'height': 1080}
            )
            
            page = await context.new_page()
            
            # Interceptar requests para evitar CAPTCHA
            await page.route("**/*recaptcha*", lambda route: route.abort())
            await page.route("**/*captcha*", lambda route: route.abort())
            
            # Ir a la página
            url = "https://numeracionyoperadores.cnmc.es/portabilidad/movil"
            print(f"Accediendo a: {url}")
            await page.goto(url, wait_until='networkidle')
            
            # Esperar a que cargue
            print("Esperando a que cargue...")
            await page.wait_for_timeout(5000)
            
            # Buscar campo de entrada
            print("Buscando campo de entrada...")
            try:
                await page.wait_for_selector("input", timeout=15000)
                print("Campo encontrado")
            except:
                return "Error: No se encontró campo de entrada"
            
            # Escribir número
            print(f"Escribiendo número: {numero}")
            await page.fill("input", numero)
            
            # Hacer clic en buscar
            print("Haciendo clic en buscar...")
            try:
                await page.click("button:has-text('Buscar')")
            except:
                try:
                    await page.click("button[type='submit']")
                except:
                    await page.press("input", "Enter")
            
            # Esperar resultados
            print("Esperando resultados...")
            await page.wait_for_timeout(10000)
            
            # Obtener contenido
            content = await page.content()
            visible_text = await page.text_content("body")
            
            print(f"Contenido obtenido: {len(content)} caracteres")
            print(f"Texto visible: {visible_text[:500]}...")
            
            # Buscar operador
            operadores = [
                'Movistar', 'Orange', 'Vodafone', 'MásMóvil', 'Yoigo', 
                'Avatel', 'Simyo', 'Pepephone', 'Lowi', 'Digi', 
                'Finetwork', 'Jazztel', 'Tuenti', 'Lebara', 'Lycamobile'
            ]
            
            operador_encontrado = None
            
            # Buscar en texto visible
            for operador in operadores:
                if operador.lower() in visible_text.lower():
                    operador_encontrado = operador
                    print(f"¡OPERADOR ENCONTRADO: {operador}!")
                    break
            
            # Si no se encuentra, buscar en HTML
            if not operador_encontrado:
                for operador in operadores:
                    if operador.lower() in content.lower():
                        operador_encontrado = operador
                        print(f"¡OPERADOR ENCONTRADO EN HTML: {operador}!")
                        break
            
            # Buscar con patrones regex
            if not operador_encontrado:
                patrones = [
                    r'operador[^>]*>([^<]+)',
                    r'empresa[^>]*>([^<]+)',
                    r'proveedor[^>]*>([^<]+)',
                    r'compañía[^>]*>([^<]+)',
                    r'<strong[^>]*>([^<]+)</strong>',
                    r'<b[^>]*>([^<]+)</b>',
                    r'<span[^>]*>([^<]+)</span>',
                    r'<div[^>]*>([^<]+)</div>'
                ]
                
                for patron in patrones:
                    matches = re.findall(patron, content, re.IGNORECASE)
                    for match in matches:
                        match_clean = match.strip()
                        if len(match_clean) > 2 and len(match_clean) < 50:
                            for operador in operadores:
                                if operador.lower() in match_clean.lower():
                                    operador_encontrado = operador
                                    print(f"¡OPERADOR ENCONTRADO CON PATRÓN: {operador}!")
                                    break
                            if operador_encontrado:
                                break
                    if operador_encontrado:
                        break
            
            await browser.close()
            
            if operador_encontrado:
                return f"✅ OPERADOR: {operador_encontrado}"
            else:
                return f"❌ NO SE ENCONTRÓ OPERADOR\nTexto: {visible_text[:1000]}..."
        
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    numero = sys.argv[1] if len(sys.argv) > 1 else "689567469"
    print(f"CONSULTANDO CNMC ULTRA FINAL - NÚMERO: {numero}")
    print("=" * 60)
    resultado = asyncio.run(consultar_cnmc_ultra_final(numero))
    print("\n" + "=" * 60)
    print("RESULTADO:")
    print("=" * 60)
    print(resultado)