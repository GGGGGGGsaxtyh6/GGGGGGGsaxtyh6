#!/usr/bin/env python3
"""
Script FINAL que funciona con Playwright
Maneja el CAPTCHA y obtiene el resultado real
"""

import asyncio
import sys
import re

async def consultar_cnmc_final(numero):
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        return "Error: Playwright no instalado"
    
    try:
        async with async_playwright() as p:
            # Lanzar navegador con más opciones
            browser = await p.chromium.launch(
                headless=False,  # Cambiar a True si no quieres ver la ventana
                args=[
                    '--no-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-web-security',
                    '--allow-running-insecure-content'
                ]
            )
            
            context = await browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )
            
            page = await context.new_page()
            
            # Ir a la página
            url = "https://numeracionyoperadores.cnmc.es/portabilidad/movil"
            print(f"Accediendo a: {url}")
            await page.goto(url, wait_until='networkidle')
            
            # Esperar a que cargue completamente
            print("Esperando a que cargue la aplicación...")
            await page.wait_for_timeout(3000)
            
            # Buscar campo de entrada
            print("Buscando campo de entrada...")
            try:
                # Esperar a que aparezca el input específico
                await page.wait_for_selector("input[type='tel'], input[placeholder*='número'], input[placeholder*='móvil']", timeout=10000)
                print("Campo de entrada encontrado")
            except:
                print("Buscando cualquier input...")
                await page.wait_for_selector("input", timeout=10000)
            
            # Escribir número
            print(f"Escribiendo número: {numero}")
            await page.fill("input", numero)
            
            # Buscar botón de búsqueda
            print("Buscando botón de búsqueda...")
            try:
                # Intentar hacer clic en el botón "Buscar"
                await page.click("button:has-text('Buscar')")
                print("Botón 'Buscar' clickeado")
            except:
                try:
                    # Intentar con otros selectores
                    await page.click("button[type='submit']")
                    print("Botón submit clickeado")
                except:
                    try:
                        await page.click("input[type='submit']")
                        print("Input submit clickeado")
                    except:
                        print("No se encontró botón, usando Enter...")
                        await page.press("input", "Enter")
            
            # Esperar a que aparezcan los resultados
            print("Esperando resultados...")
            await page.wait_for_timeout(5000)
            
            # Verificar si hay CAPTCHA
            try:
                captcha_frame = await page.query_selector("iframe[src*='recaptcha']")
                if captcha_frame:
                    print("⚠️ CAPTCHA detectado - requiere intervención manual")
                    print("Esperando 30 segundos para resolver CAPTCHA...")
                    await page.wait_for_timeout(30000)
            except:
                pass
            
            # Buscar resultados en la página
            print("Buscando resultados...")
            
            # Obtener todo el texto visible
            visible_text = await page.text_content("body")
            print(f"Texto visible: {visible_text[:1000]}...")
            
            # Buscar información del operador
            operadores = [
                'Movistar', 'Orange', 'Vodafone', 'MásMóvil', 'Yoigo', 
                'Avatel', 'Simyo', 'Pepephone', 'Lowi', 'Digi', 
                'Finetwork', 'Jazztel', 'Tuenti', 'Lebara', 'Lycamobile'
            ]
            
            operador_encontrado = None
            
            # Buscar en el texto visible
            for operador in operadores:
                if operador.lower() in visible_text.lower():
                    operador_encontrado = operador
                    print(f"¡OPERADOR ENCONTRADO EN TEXTO: {operador}!")
                    break
            
            # Si no se encuentra, buscar en el HTML
            if not operador_encontrado:
                content = await page.content()
                for operador in operadores:
                    if operador.lower() in content.lower():
                        operador_encontrado = operador
                        print(f"¡OPERADOR ENCONTRADO EN HTML: {operador}!")
                        break
            
            # Buscar patrones específicos de resultado
            if not operador_encontrado:
                # Buscar texto que contenga "operador" o similar
                patrones = [
                    r'operador[^>]*>([^<]+)',
                    r'empresa[^>]*>([^<]+)',
                    r'proveedor[^>]*>([^<]+)',
                    r'compañía[^>]*>([^<]+)',
                    r'<strong[^>]*>([^<]+)</strong>',
                    r'<b[^>]*>([^<]+)</b>',
                    r'<span[^>]*>([^<]+)</span>'
                ]
                
                content = await page.content()
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
            
            # Buscar mensajes de error o información
            if not operador_encontrado:
                error_messages = [
                    'no encontrado', 'no existe', 'no válido', 'error',
                    'no se encontró', 'sin resultados'
                ]
                
                for error_msg in error_messages:
                    if error_msg.lower() in visible_text.lower():
                        print(f"Mensaje de error detectado: {error_msg}")
                        break
            
            await browser.close()
            
            if operador_encontrado:
                return f"✅ OPERADOR ENCONTRADO: {operador_encontrado}"
            else:
                return f"❌ NO SE ENCONTRÓ OPERADOR PARA EL NÚMERO {numero}\nTexto visible: {visible_text[:500]}..."
        
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    numero = sys.argv[1] if len(sys.argv) > 1 else "689567469"
    print(f"CONSULTANDO CNMC FINAL - NÚMERO: {numero}")
    print("=" * 60)
    resultado = asyncio.run(consultar_cnmc_final(numero))
    print("\n" + "=" * 60)
    print("RESULTADO:")
    print("=" * 60)
    print(resultado)