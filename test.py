import easyocr

reader = easyocr.Reader(['es'])

# Leer el texto desde la imagen procesada
result = reader.readtext('captura_1400567259.png')

# Mostrar el resultado
for detection in result:
    print(detection[1])  # Texto detectado
