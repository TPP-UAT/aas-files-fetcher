# 📄 Web Scraper de PDFs de American Astronomical Society

Este script en Python descarga automáticamente todos los archivos PDF de artículos científicos disponibles en los volúmenes de la revista *The Astrophysical Journal* (AAS) alojados en el sitio [iopscience.iop.org](https://iopscience.iop.org/).

## 🧠 ¿Qué hace este script?

- Navega por las distintas ediciones (issues) de una revista científica, comenzando desde una URL inicial.
- Extrae todos los enlaces a PDFs de cada página.
- Descarga los artículos y los guarda en carpetas organizadas por volumen y número.
- Detecta posibles bloqueos por CAPTCHA.
- Registra errores y el progreso en un archivo de log (`data_scrapper.log`).
- Permite reintentar URLs fallidas si ocurre algún error durante la descarga.

## 🛠️ Requisitos

Antes de ejecutar el script, asegurate de tener instalado:

- Python 3.7 o superior
- Las siguientes librerías (pueden instalarse con pip):

```bash
pip install requests beautifulsoup4 PyPDF2
```

## 📂 Estructura de carpetas

Los archivos PDF se guardarán dentro de la carpeta `./webscraping`, y a su vez, dentro de subcarpetas con el nombre del volumen y número de edición. Por ejemplo:

```
./webscraping/
├── 954-1/
│   ├── abc123.pdf
│   └── def456.pdf
├── 953-2/
│   └── ...
```

## ▶️ Cómo usarlo

1. **Ajustá la URL de inicio (teniendo en cuenta el volúmen y el número):**

   ```python
   initial_url = "https://iopscience.iop.org/issue/0004-637X/864/1"
   ```

2. **Ajustá el volumen final para definir hasta dónde querés descargar:**

   ```python
   final_volume = '850'
   ```

3. **Modificá las cookies `cookie_page` y `cookie_pdf`.**

   Esto es necesario para evitar restricciones del CAPTCHA.

4. **Ejecutá el script con:**

   ```bash
   python AAS-scrapper.py
   ```

## ⚠️ Advertencias

- El sitio puede aplicar restricciones si detecta muchas descargas en poco tiempo. Por eso, el script incluye una pausa (`time.sleep(5)`) entre cada PDF.
- Si se presenta una página de verificación (CAPTCHA), el script detectará el error y lo registrará en los logs, agregando la URL a una lista de pendientes (`failed_urls`).
- En caso de que un PDF no se descargue correctamente, se imprime un mensaje en consola y se registra en el log.

## 📌 Autor

Este script fue creado para facilitar la descarga masiva de artículos científicos con fines educativos o de investigación. Usalo responsablemente y respetá los [términos de uso de IOPscience](https://iopscience.iop.org/page/terms).
