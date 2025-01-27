from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from PIL import Image
import pandas as pd
import pytesseract
import cv2
import os
import time
import re
import csv

# CONFIGURAR TESSERACT
pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

# CONFIGURAR DRIVER
options = Options()
options.add_argument('--start-maximized')
service = Service('C:/Users/Joseph/Documents/MINERIA/PROYECTO_FINAL/chromedriver/chromedriver.exe')
driver = webdriver.Chrome(service=service, options=options)

# NAVEGAR A LA PÁGINA
url = "https://www.senescyt.gob.ec/consulta-titulos-web/faces/vista/consulta/consulta.xhtml"
driver.get(url)

# AUMENTAR TIEMPO DE ESPERA
wait = WebDriverWait(driver, 20)

# LEER CÉDULAS
with open("cedula.txt", "r") as file:
    cedulas = [line.strip() for line in file.readlines()]

# RUTA DEL DIRECTORIO
project_dir = os.path.dirname(os.path.abspath(__file__))

# COORDENADAS PARA CAPTURA DEL CAPTCHA
left = 336.511
top = 636.511
right = 535.3
bottom = 686.5

# FUNCIONES AUXILIARES
def validar_captcha(captcha_text):
    """VALIDAR CAPTCHA"""
    return bool(re.match("^[a-z0-9]{4}$", captcha_text))

def guardar_datos_csv(datos, nombre_archivo="resultados.csv"):
    """GUARDAR DATOS EN CSV"""
    ruta_csv = os.path.join(project_dir, nombre_archivo)
    print(f"Guardando datos en: {ruta_csv}")

    # ENCABEZADOS
    encabezados = [
        "Identificación", "Nombres", "Género", "Nacionalidad",
        "Título", "Institución", "Tipo", "Reconocido Por", "Número Registro", 
        "Fecha Registro", "Área Conocimiento", "Observación"
    ]

    # ESCRIBIR ENCABEZADOS SI EL ARCHIVO NO EXISTE O ESTÁ VACÍO
    escribir_encabezados = not os.path.exists(ruta_csv) or os.path.getsize(ruta_csv) == 0
    print("Escribiendo encabezados:", escribir_encabezados)

    with open(ruta_csv, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if escribir_encabezados:
            writer.writerow(encabezados)
        for fila in datos:
            writer.writerow(fila)

    print("Datos guardados correctamente.")

def extraer_datos():
    """EXTRAER DATOS DEL SITIO"""
    # Datos personales
    identificacion = driver.find_element(By.ID, "formPrincipal:j_idt44").text.strip()
    nombres = driver.find_element(By.ID, "formPrincipal:j_idt47").text.strip()
    genero = driver.find_element(By.ID, "formPrincipal:j_idt49").text.strip()
    nacionalidad = driver.find_element(By.ID, "formPrincipal:j_idt51").text.strip()

    # EXTRAER DATOS POR TÍTULOS
    datos_posgrado = []
    try:
        posgrado_rows = driver.find_elements(By.CSS_SELECTOR, "#formPrincipal\\:j_idt52\\:0\\:tablaAplicaciones tr")
        for row in posgrado_rows:
            columnas = row.find_elements(By.TAG_NAME, "td")
            if len(columnas) > 0:
                datos_posgrado.append([
                    identificacion, nombres, genero, nacionalidad,
                    columnas[0].text.strip(), columnas[1].text.strip(), columnas[2].text.strip(),
                    columnas[3].text.strip(), columnas[4].text.strip(), columnas[5].text.strip(),
                    columnas[6].text.strip(), columnas[7].text.strip()
                ])
    except Exception as e:
        print(f"Error al extraer posgrado: {e}")

    # EXTRAER DATOS DE GRADO
    datos_grado = []
    try:
        grado_rows = driver.find_elements(By.CSS_SELECTOR, "#formPrincipal\\:j_idt52\\:1\\:tablaAplicaciones tr")
        for row in grado_rows:
            columnas = row.find_elements(By.TAG_NAME, "td")
            if len(columnas) > 0:
                datos_grado.append([
                    identificacion, nombres, genero, nacionalidad,
                    columnas[0].text.strip(), columnas[1].text.strip(), columnas[2].text.strip(),
                    columnas[3].text.strip(), columnas[4].text.strip(), columnas[5].text.strip(),
                    columnas[6].text.strip(), columnas[7].text.strip()
                ])
    except Exception as e:
        print(f"Error al extraer grado: {e}")

    # EXTRAER DATOS DE TERCER NIVEL
    datos_tercer_nivel = []
    try:
        tercer_nivel_rows = driver.find_elements(By.CSS_SELECTOR, "#formPrincipal\\:j_idt52\\:2\\:tablaAplicaciones tr")
        for row in tercer_nivel_rows:
            columnas = row.find_elements(By.TAG_NAME, "td")
            if len(columnas) > 0:
                datos_tercer_nivel.append([
                    identificacion, nombres, genero, nacionalidad,
                    columnas[0].text.strip(), columnas[1].text.strip(), columnas[2].text.strip(),
                    columnas[3].text.strip(), columnas[4].text.strip(), columnas[5].text.strip(),
                    columnas[6].text.strip(), columnas[7].text.strip()
                ])
    except Exception as e:
        print(f"Error al extraer tercer nivel: {e}")

    return datos_posgrado + datos_grado + datos_tercer_nivel

# IMPRIMIR DATASET
def imprimir_dataset(nombre_archivo="resultados.csv"):
    """IMPRIMIR EL DATASET"""
    df = pd.read_csv(nombre_archivo)
    print(df)

# PROCESAR CÉDULAS
for cedula in cedulas:
    while True:
        try:
            print(f"Consultando cédula: {cedula}")

            # ESPERAR A QUE CARGUE LA PÁGINA
            wait.until(EC.presence_of_element_located((By.ID, "formPrincipal:identificacion")))

            # COMPLETAR CÉDULA
            cedula_input = driver.find_element(By.ID, "formPrincipal:identificacion")
            cedula_input.clear()
            cedula_input.send_keys(cedula)

            # CAPTURAR CAPTCHA
            screenshot_path = os.path.join(project_dir, "full_screenshot.png")
            driver.save_screenshot(screenshot_path)
            full_image = Image.open(screenshot_path)
            cropped_image = full_image.crop((left, top, right, bottom))
            cropped_path = os.path.join(project_dir, f"captura_{cedula}.png")
            cropped_image.save(cropped_path)

            # PROCESAR CAPTCHA CON OPENCV
            image = cv2.imread(cropped_path)
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            threshold_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

            # USAR TESSERACT
            captcha_text = pytesseract.image_to_string(threshold_image, config='--psm 7').strip()

            # VALIDAR CAPTCHA
            if not validar_captcha(captcha_text):
                print(f"CAPTCHA incorrecto ({captcha_text}), recargando...") 
                driver.refresh()
                time.sleep(1)
                continue

            print("Texto CAPTCHA:", captcha_text)

            # INGRESAR CAPTCHA
            captcha_input = driver.find_element(By.ID, "formPrincipal:captchaSellerInput")
            captcha_input.clear()
            captcha_input.send_keys(captcha_text)

            # REALIZAR BÚSQUEDA
            buscar_button = driver.find_element(By.ID, "formPrincipal:boton-buscar")
            buscar_button.click()

            # VERIFICAR ERRORES
            try:
                wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "ui-messages-error")))

                error_message = driver.find_element(By.CLASS_NAME, "ui-messages-error").text
                if "Caracteres incorrectos" in error_message:
                    print("CAPTCHA incorrecto, recargando...")
                    driver.refresh()
                    time.sleep(1)
                    continue
            except:
                print("CAPTCHA correcto.")

            # EXTRAER Y GUARDAR DATOS
            datos = extraer_datos()
            guardar_datos_csv(datos)
            print(f"Datos de la cédula {cedula} guardados.")

            break

        except Exception as e:
            print(f"Error cédula {cedula}: {e}")
            driver.refresh()
            time.sleep(1)

# CERRAR NAVEGADOR
driver.quit()

# IMPRIMIR RESULTADOS FINALES
imprimir_dataset()
