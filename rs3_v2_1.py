import pandas as pd

# Cargar el archivo CSV normalizado
normalized_file_path = 'normalized_output.csv'  # Actualiza la ruta según tu archivo
normalized_df = pd.read_csv(normalized_file_path)

# Filtrar las oraciones que contienen palabras clave relacionadas con criminalidad
keywords = ['crimen', 'robo', 'asesinato', 'delito', 'violencia', 'criminal', 'agresión', 'secuestro', 'homicidio', 'disparos']
crime_related_df = normalized_df[normalized_df['Oracion'].str.contains('|'.join(keywords), case=False, na=False)]

# Guardar el DataFrame filtrado en un nuevo archivo CSV
filtered_file_path = 'crime_related_output.csv'  # Actualiza la ruta según tu archivo
crime_related_df.to_csv(filtered_file_path, index=False)

print("Archivo filtrado guardado en:", filtered_file_path)
