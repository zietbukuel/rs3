import pandas as pd
import re

# Cargar el archivo CSV original
file_path = 'output (1).csv'
data = pd.read_csv(file_path)

# Crear una lista para almacenar los datos normalizados
normalized_data = []

# Procesar cada fila del DataFrame
for index, row in data.iterrows():
    title = row['Titulo']
    content = row['Contenido']
    
    # Dividir el contenido en oraciones utilizando una expresión regular
    sentences = re.split(r'(?<=[.!?]) +', content)
    
    for sentence in sentences:
        # Crear un diccionario para almacenar el título y la oración
        normalized_row = {'Titulo': title, 'Oracion': sentence}
        normalized_data.append(normalized_row)

# Crear un nuevo DataFrame con los datos normalizados
normalized_df = pd.DataFrame(normalized_data)

# Guardar el DataFrame normalizado en un nuevo archivo CSV
normalized_file_path = 'normalized_output.csv'  # Actualiza la ruta según tu archivo
normalized_df.to_csv(normalized_file_path, index=False)

print("Archivo normalizado guardado en:", normalized_file_path)