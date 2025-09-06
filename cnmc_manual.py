#!/usr/bin/env python3
"""
Script que abre la página y te dice exactamente qué hacer
"""

import asyncio
import sys

async def consultar_cnmc_manual(numero):
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        return "Error: Playwright no instalado"
    
    try:
        async with async_playwright() as p:
            # Lanzar navegador VISIBLE
            browser = await p.chromium.launch(
                headless=False,  # VISIBLE para que veas la página
                args=[
                    '--no-sandbox',
                    '--disable-dev-shm-usage'
                ]
            )
            
            context = await browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )
            
            page = await context.new_page()
            
            # Ir a la página
            url = "https://numeracionyoperadores.cnmc.es/portabilidad/movil"
            print(f"🌐 Abriendo: {url}")
            await page.goto(url)
            
            # Escribir el número automáticamente
            print(f"📝 Escribiendo número: {numero}")
            await page.fill("input", numero)
            
            print("\n" + "="*60)
            print("🎯 INSTRUCCIONES:")
            print("="*60)
            print("1. ✅ El número ya está escrito en el campo")
            print("2. 🔍 Haz clic en el botón 'Buscar'")
            print("3. 🤖 Resuelve el CAPTCHA si aparece")
            print("4. ⏳ Espera a que aparezcan los resultados")
            print("5. 📋 Copia el nombre del operador que aparece")
            print("6. ❌ Cierra la ventana del navegador")
            print("="*60)
            print("⏰ Esperando 60 segundos para que hagas la consulta...")
            
            # Esperar 60 segundos para que el usuario haga la consulta
            await page.wait_for_timeout(60000)
            
            # Intentar obtener el resultado
            print("\n🔍 Buscando resultado...")
            visible_text = await page.text_content("body")
            
            # Buscar operador en el texto
            operadores = [
                'Movistar', 'Orange', 'Vodafone', 'MásMóvil', 'Yoigo', 
                'Avatel', 'Simyo', 'Pepephone', 'Lowi', 'Digi', 
                'Finetwork', 'Jazztel', 'Tuenti', 'Lebara', 'Lycamobile'
            ]
            
            operador_encontrado = None
            for operador in operadores:
                if operador.lower() in visible_text.lower():
                    operador_encontrado = operador
                    break
            
            await browser.close()
            
            if operador_encontrado:
                return f"✅ OPERADOR ENCONTRADO: {operador_encontrado}"
            else:
                return f"❌ No se detectó operador automáticamente. Revisa la página manualmente."
        
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    numero = sys.argv[1] if len(sys.argv) > 1 else "689567469"
    print(f"CONSULTA MANUAL CNMC - NÚMERO: {numero}")
    print("=" * 60)
    resultado = asyncio.run(consultar_cnmc_manual(numero))
    print("\n" + "=" * 60)
    print("RESULTADO:")
    print("=" * 60)
    print(resultado)