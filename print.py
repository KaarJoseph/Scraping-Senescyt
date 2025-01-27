import pandas as pd

# Ruta del archivo CSV
archivo_csv = 'resultados.csv'

# Cargar el CSV
df = pd.read_csv(archivo_csv)

# Mostrar TABLA
print(df)
