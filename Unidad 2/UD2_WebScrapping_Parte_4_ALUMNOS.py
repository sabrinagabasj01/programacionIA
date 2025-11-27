import asyncio
import sys
import pandas as pd
from playwright.async_api import async_playwright

# --- FIX PARA WINDOWS ---
# Esto es necesario porque en Windows, el bucle de eventos por defecto a veces choca con Playwright.
# ProactorEventLoop es un tipo de motor más compatible con subprocesos en Windows.
# En linux: playwright install-deps
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

# 1. DEFINIMOS LA FUNCIÓN ASÍNCRONA (Obligatorio en .py)
# 'async' indica que esta función puede pausarse (await) mientras espera respuestas de internet
async def main():
    print("🚀 Iniciando monitor de Criptomonedas (CoinMarketCap)...")

    # 'async with': Gestor de contexto. Inicia y cierra Playwright automáticamente al terminar el bloque.
    async with async_playwright() as p:
        
        # 1. LANZAMIENTO DEL NAVEGADOR
        # chromium: El motor open-source de Chrome.
        # headless=False: 'Cabeza visible'. False significa que VEMOS la ventana del navegador. 
        #                 Si fuera True, funcionaría en segundo plano (invisible y más rápido).
        # slow_mo=50:     Retardo de 50ms entre acciones. Fundamental para ver qué hace el robot 
        #                 y parecer más humanos.
        browser = await p.chromium.launch(headless=False, slow_mo=50)
        
        # Contexto y Página
        # new_context(): Crea una sesión aislada (como modo Incógnito). No comparte cookies con otras sesiones.
        # viewport:      Simula el tamaño de la pantalla (ancho x alto).
        context = await browser.new_context(viewport={'width': 1366, 'height': 768})
        page = await context.new_page()

        # 2. NAVEGACIÓN
        url = 'https://coinmarketcap.com/'
        print(f"🌍 Yendo a: {url}")
        
        # goto: Navega a la URL.
        # wait_until='domcontentloaded': Espera solo a que el HTML básico esté listo, no espera a todas las imágenes.
        #                                Es más rápido que la opción por defecto ('load').
        await page.goto(url, wait_until='domcontentloaded')

        # 3. GESTIÓN DE POP-UPS (Bloque Try/Except para que no falle si no salen)
        try:
            # wait_for_timeout(2000): Pausa forzada de 2 segundos (2000ms) para dar tiempo a que salga el banner.
            await page.wait_for_timeout(2000)
            
            # locator: Busca elementos en la web usando selectores CSS.
            # Aquí buscamos 2 posibles botones: la cruz de cerrar O el botón de "Quizás luego".
            close_buttons = page.locator("div.cmc-cookie-policy-banner__close, button:has-text('Maybe later')")
            
            # count(): Cuenta cuántos elementos ha encontrado.
            if await close_buttons.count() > 0:
                # click(): Hace clic en el primer elemento encontrado (.first).
                await close_buttons.first.click()
                print("✅ Banner cerrado.")
        except:
            pass # Si falla (no hay banner), continuamos sin error (pass)

        # GESTIÓN DE COOKIES (Opcional pero recomendado)
        # Intentamos cerrar el banner para que no moleste, aunque para leer texto a veces no hace falta.
        try:
            print("🍪 Gestionando cookies...")
            await page.wait_for_timeout(2000) # Pequeña pausa para ver si sale
            # Buscamos botones de "Aceptar" o "Consentir"
            boton = page.locator("button:has-text('Aceptar'), button:has-text('Consentir'), #didomi-notice-agree-button")
            if await boton.count() > 0:
                await boton.first.click()
                print("✅ Cookies cerradas.")
        except:
            print("⚠️ No se pudo cerrar el banner (o no apareció). Seguimos.")
        # 4. EXTRACCIÓN DE DATOS
        print("🔍 Analizando el mercado...")
        
        # wait_for_selector: Espera INTELIGENTE. El script se pausa hasta que aparece la tabla.
        # timeout=5000: Si en 5 segundos no aparece, lanza error (evita quedarse colgado para siempre).
        try:
            await page.wait_for_selector('table tbody tr', timeout=5000)
        except:
            print("⚠️ No se encontró la tabla a tiempo.")
            await browser.close()
            return

        # Seleccionamos TODAS las filas (tr) del cuerpo de la tabla (tbody)
        filas = page.locator('table tbody tr')
        
        print(f"💎 Extrayendo el Top 5 de Criptomonedas...")
        datos_crypto = []
        
        # Bucle para sacar solo las 5 primeras
        for i in range(5):
            try:
                # .nth(i): Selecciona el elemento en la posición 'i' (0, 1, 2...)
                fila = filas.nth(i)
                
                # --- USO DE SELECTORES CSS ESPECÍFICOS ---
                # td:nth-child(3): Busca la celda (td) en la columna número 3.
                # p: Busca el párrafo dentro de esa celda.
                # first / last: Como en esa celda hay dos textos (Nombre y Siglas), cogemos el primero y el último.
                # inner_text(): Extrae el texto visible limpio dentro del elemento.
                
                nombre = await fila.locator('td:nth-child(3) p').first.inner_text()
                simbolo = await fila.locator('td:nth-child(3) p').last.inner_text()
                precio = await fila.locator('td:nth-child(4)').inner_text()
                
                print(f"   💰 #{i+1} {nombre} ({simbolo}): {precio}")
                
                datos_crypto.append({
                    "Ranking": i+1,
                    "Nombre": nombre,
                    "Simbolo": simbolo,
                    "Precio": precio
                })
            except Exception as e:
                # Capturamos errores individuales por fila para que un fallo no pare todo el script
                pass

        # 5. CIERRE
        # Es importante cerrar el navegador para liberar memoria RAM.
        await browser.close()
        
        # Mostrar resultado con Pandas
        if datos_crypto:
            df = pd.DataFrame(datos_crypto)
            print("\n📊 RESULTADOS:")
            print(df)

# 2. PUNTO DE ENTRADA (Entry Point)
# Esta condición comprueba si estamos ejecutando este archivo directamente.
# asyncio.run(): Es la función que arranca el motor asíncrono y ejecuta nuestra función 'main'.
if __name__ == "__main__":
    asyncio.run(main())