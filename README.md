# Proyecto de Extracción de Datos de la SENESCYT

##Realizado por Kaar Joseph

Este proyecto está diseñado para automatizar la consulta de títulos académicos en el portal de la SENESCYT (Secretaría Nacional de Educación Superior, Ciencia, Tecnología e Innovación) de Ecuador, usando técnicas de automatización con **Selenium**, procesamiento de imágenes con **OpenCV** y reconocimiento óptico de caracteres (**OCR**) con **Tesseract**.

El sistema permite consultar los datos de las personas utilizando su cédula de identidad, capturar y validar los CAPTCHAs, y finalmente extraer la información relacionada con los títulos académicos a nivel posgrado, grado y tercer nivel.

## Requisitos

### Librerías

Este proyecto requiere las siguientes librerías de Python para su funcionamiento:

- **selenium**: Para interactuar de manera automatizada con el navegador y la página web.
- **pillow**: Para procesar las capturas de pantalla.
- **pytesseract**: Para realizar el OCR sobre las imágenes del CAPTCHA.
- **opencv-python**: Para manipular las imágenes del CAPTCHA antes de aplicar el OCR.
- **pandas**: Para manejar y almacenar los datos extraídos en formato CSV.
- **csv**: Para trabajar con archivos CSV.

Puedes instalar todas estas librerías con el siguiente comando:

```bash
pip install selenium pillow pytesseract opencv-python pandas
```

### Dependencias Adicionales

- **Tesseract OCR**: Es necesario tener Tesseract instalado en tu sistema para procesar el texto del CAPTCHA. Puedes descargarlo desde su [repositorio oficial](https://github.com/tesseract-ocr/tesseract). Asegúrate de que el ejecutable `tesseract.exe` esté en el directorio correcto y que la ruta esté configurada en el script.

- **ChromeDriver**: Necesitarás descargar el ChromeDriver correspondiente a tu versión de Google Chrome. Asegúrate de configurar correctamente la ruta de `chromedriver.exe` en el código.

---

## Descripción del Código

### Funciones Principales

- **validar_captcha(captcha_text)**: Esta función valida el texto extraído del CAPTCHA usando una expresión regular, asegurándose de que sea un texto con solo cuatro caracteres alfanuméricos en minúsculas.

- **guardar_datos_csv(datos, nombre_archivo="resultados.csv")**: Guarda los datos extraídos en un archivo CSV. Si el archivo no existe, lo crea, y si ya existe, agrega los nuevos registros al final.

- **extraer_datos()**: Extrae los datos personales del usuario (como identificación, nombres, género, nacionalidad) y los títulos académicos (posgrado, grado y tercer nivel) de la página web. El proceso de extracción incluye manejar excepciones y errores en la estructura de la página.

- **imprimir_dataset(nombre_archivo="resultados.csv")**: Imprime el dataset completo desde el archivo CSV generado, permitiendo revisar los resultados finales del proceso.

---

## Flujo de Ejecución

1. **Carga de Cédulas**: El script lee las cédulas desde un archivo de texto `cedula.txt`, donde cada línea contiene una cédula de identidad de una persona a consultar.

2. **Navegación a la Página Web**: Utiliza Selenium para abrir la página web de consulta de títulos académicos.

3. **Procesamiento del CAPTCHA**:
   - El script toma una captura de pantalla de la sección del CAPTCHA en la página web.
   - Usa OpenCV para recortar y mejorar la calidad de la imagen antes de pasarla a Tesseract, que se encarga de reconocer el texto.

4. **Validación del CAPTCHA**: Si el texto reconocido no es válido, el script recarga la página y lo vuelve a intentar. Si el CAPTCHA es correcto, el script continúa con la búsqueda.

5. **Consulta de Títulos Académicos**: El script completa el campo de la cédula en el formulario, envía la búsqueda y extrae los datos correspondientes a los títulos académicos de la persona (posgrado, grado y tercer nivel).

6. **Guardar los Datos**: Los datos extraídos se guardan en un archivo CSV llamado `resultados.csv`. Si el archivo ya existe, el script agregará los nuevos registros.

7. **Reintentos Automáticos**: Si se produce un error, como un CAPTCHA incorrecto o un fallo en la consulta, el script intenta de nuevo automáticamente.

---

## Estructura del Proyecto

```plaintext
.
├── cedula.txt                # Archivo de texto con las cédulas para consultar
├── full_screenshot.png        # Captura de pantalla completa de la página
├── captura_{cedula}.png       # Captura del CAPTCHA para cada cédula
├── resultados.csv             # Archivo CSV donde se guardan los resultados
└── program.py                 # Script principal para ejecutar el proceso
``` 
## Ejecución

Para ejecutar el script, simplemente corre el archivo `program.py` con el siguiente comando:

```bash
python program.py
```

Este comando iniciará el proceso de consulta, captura de datos y generación del archivo CSV con los resultados. Se lee el archivo `cedula.txt`.

---

## Archivo `cedula.txt`

El archivo `cedula.txt` debe contener una cédula, una por línea, de las personas que deseas consultar.

---

## Captura de CAPTCHA

El script toma automáticamente las capturas de pantalla de la sección del CAPTCHA en la página y las procesa. Sin embargo, si encuentras que el reconocimiento no es perfecto, puedes ajustar las coordenadas de la captura en el código (líneas 27-30) para adaptarlo mejor a tu pantalla.
