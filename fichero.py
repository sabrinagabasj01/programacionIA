"""
### 📝 Ejercicio Final: Detective de Noticias

**Objetivo**: Crear un script que vigile la portada de un periódico digital (ej: `elpais.com`, `elmundo.es`, o `marca.com`) y detecte si aparecen ciertas palabras clave en los titulares.

**Instrucciones**:
1.  Usa `Playwright` para abrir la web.
2.  Busca todos los titulares (inspecciona la web para ver qué etiqueta usan, suele ser `h2`, `h3` o `article`).
3.  Recorre los textos y busca si contienen palabras como "Crisis", "Fútbol", "Gobierno" o lo que prefieras.
4.  Imprime "¡ALERTA! Noticia encontrada: [Titular]" si hay coincidencia.evuelve una lista con las coincidencias encontradas, ordenadas por similitud.

"""


# ¡OJO! Ejecutar en un fichero .py ya que en Jupyter no funciona 

# Plantilla (opcional):

import asyncio
from playwright.async_api import async_playwright

# --- FIX PARA WINDOWS ---
# Mantenemos esto siempre para asegurar que funciona bien en Windows
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

# 1. FUNCIÓN PRINCIPAL ASÍNCRONA
async def main():
    
    # PALABRAS CLAVE: Lo que queremos buscar (puedes cambiarlas)
    palabras_clave = []
    print(f"📋 Buscando: {', '.join(palabras_clave)}")

    async with async_playwright() as p:
        
        # 2. LANZAMIENTO
        # Usamos headless=False para ver cómo el 'detective' abre el periódico
        browser = await p.chromium.launch(headless=True)
        
        page = await browser.new_page()
                
        # 3. NAVEGACIÓN
        target_url =  "https://elpais.com"
        print(f"🌍 Abriendo la portada de: {target_url}")
        
        # wait_until='domcontentloaded': Espera a que esté el texto listo (es más rápido que esperar a todas las fotos)
        await page.goto(target_url, wait_until="networkidle")
        
        # 4. GESTIÓN DE COOKIES (Opcional pero recomendado)
        # Intentamos cerrar el banner para que no moleste, aunque para leer texto a veces no hace falta.

        

        # 5. EXTRACCIÓN MASIVA DE TITULARES
        print("🔍 Escaneando titulares...")
        
        # page.locator: Le decimos que busque TODAS las etiquetas de título o con algún selector en particular
        # .all_inner_texts(): Esta función es MÁGICA. En lugar de hacer un bucle manual,
        # nos devuelve directamente una LISTA con el texto de todos los elementos encontrados.

        
        print(f"📉 Se han encontrado {len(titulares)} posibles titulares. Analizando...")
        
        # 6. LÓGICA DE DETECTIVE (Filtrado)
        noticias_encontradas = 0
        
        for texto in titulares:
            # Limpiamos espacios en blanco al principio y final
            texto_limpio = texto.strip()
            
            texto_min = texto_limpio.lower()
            
            # Si el titular está vacío, pasamos al siguiente
               
                
            # Comprobamos si alguna palabra clave está dentro del texto
                    # Usamos break para no imprimir la misma noticia 2 veces si tiene dos palabras clave
                    break 

        if noticias_encontradas == 0:
            print("😴 Todo tranquilo. No se encontraron las palabras clave en la portada.")
        else:
            print(f"✅ Análisis completado. Total alertas: {noticias_encontradas}")

        # 7. CIERRE
        

# PUNTO DE ARRANQUE DEL SCRIPT
if __name__ == "__main__":
    asyncio.run(main())