from datetime import datetime
import pandas as pd
import re

# Cargar el archivo CSV filtrado
filtered_file_path = 'crime_related_output.csv'  # Actualiza la ruta según tu archivo
crime_related_df = pd.read_csv(filtered_file_path)

# Convertir las columnas 'Titulo' y 'Oracion' a minúsculas
crime_related_df['Titulo'] = crime_related_df['Titulo'].str.lower()
crime_related_df['Oracion'] = crime_related_df['Oracion'].str.lower()

# Función para categorizar las oraciones
def categorize_sentence(sentence):
    try:
        if re.search(r'disparos|tiroteo', sentence, re.IGNORECASE):
            return 'Disparos'
        elif re.search(r'herido|muerto|fallecido|lesionado', sentence, re.IGNORECASE):
            return 'Heridos'
        elif re.search(r'desconocido|sin motivo', sentence, re.IGNORECASE):
            return 'Motivos Desconocidos'
        elif re.search(r'robo|asalto|hurto', sentence, re.IGNORECASE):
            return 'Robo'
        elif re.search(r'secuestro', sentence, re.IGNORECASE):
            return 'Secuestro'
        elif re.search(r'violencia|agresión|ataque', sentence, re.IGNORECASE):
            return 'Violencia'
        elif re.search(r'extorsión', sentence, re.IGNORECASE):
            return 'Extorsión'
        elif re.search(r'narcotráfico|drogas', sentence, re.IGNORECASE):
            return 'Narcotráfico'
        elif re.search(r'corrupción|soborno', sentence, re.IGNORECASE):
            return 'Corrupción'
        elif re.search(r'fraude|estafa', sentence, re.IGNORECASE):
            return 'Fraude'
        elif re.search(r'vandalismo', sentence, re.IGNORECASE):
            return 'Vandalismo'
        elif re.search(r'cibercrimen|ciberataque', sentence, re.IGNORECASE):
            return 'Cibercrimen'
        elif re.search(r'daños a la propiedad|destrucción', sentence, re.IGNORECASE):
            return 'Daños a la Propiedad'
        elif re.search(r'criminalidad|delito|crimen|criminal', sentence, re.IGNORECASE):
            return 'Criminalidad General'
        else:
            return 'Otros'
    except Exception as e:
        print(f"Error categorizing sentence: {e}")
        return 'Desconocido'

# Función para extraer la ubicación
def extract_location(sentence):
    try:
        locations = [
            'ancón', 'ate', 'barranco', 'breña', 'carabayllo', 'chaclacayo', 'chorrillos', 'cieneguilla',
            'comas', 'el agustino', 'independencia', 'jesús maría', 'la molina', 'la victoria', 'lince',
            'los olivos', 'lurigancho', 'lurín', 'magdalena del mar', 'pueblo libre', 'puente piedra',
            'punta hermosa', 'punta negra', 'rímac', 'san bartolo', 'san borja', 'san isidro', 'san juan de lurigancho',
            'san juan de miraflores', 'san luis', 'san martín de porres', 'san miguel', 'santa anita', 'santa maría del mar',
            'santa rosa', 'santiago de surco', 'surquillo', 'villa el salvador', 'villa maría del triunfo',
            'lima', 'miraflores', 'cusco', 'arequipa', 'trujillo', 'chiclayo',
            'piura', 'iquitos', 'huancayo', 'tacna', 'juliaca', 'puno', 'huaraz', 'cajamarca', 'ayacucho',
            'chimbote', 'ica', 'moquegua', 'pucallpa', 'tarapoto', 'tumbes', 'puerto maldonado',
            'amazonas', 'ancash', 'apurímac', 'arequipa', 'ayacucho', 'cajamarca', 'callao', 'cusco', 'huancavelica', 
            'huánuco', 'ica', 'junín', 'la libertad', 'lambayeque', 'lima', 'loreto', 'madre de dios', 'moquegua', 
            'pasco', 'piura', 'puno', 'san martín', 'tacna', 'tumbes', 'ucayali'
        ]
        
        locations_set = set(location.lower() for location in locations)
        
        for word in sentence.lower().split():
            if word in locations_set:
                return word.capitalize()
        
        return 'Desconocido'
    except Exception as e:
        print(f"Error extracting location: {e}")
        return 'Desconocido'

def determine_severity(sentence):
    try:
        sentence = sentence.lower()
        if re.search(r'\b(disparos|tiroteo|asesinato|secuestro|muerto|fallecido)\b', sentence):
            return 'Alta'
        elif re.search(r'\b(herido|lesionado|robo|asalto|hurto|violencia|agresión|extorsión|narcotráfico|drogas)\b', sentence):
            return 'Media'
        elif re.search(r'\b(corrupción|soborno|criminalidad|delito|crimen|criminal|fraude|estafa|vandalismo|cibercrimen|ciberataque|daños a la propiedad|destrucción)\b', sentence):
            return 'Baja'
        else:
            return 'Desconocido'
    except Exception as e:
        print(f"Error determining severity: {e}")
        return 'Desconocido'

# Función para extraer la fuente de la información
def extract_source(title):
    try:
        if 'rpp noticias' in title:
            return 'RPP Noticias'
        elif 'el comercio perú' in title:
            return 'EL COMERCIO PERÚ'
        elif 'correo' in title:
            return 'CORREO'
        elif 'peru21' in title:
            return 'PERU21'
        else:
            return 'Desconocido'
    except Exception as e:
        print(f"Error extracting source: {e}")
        return 'Desconocido'

# Función para determinar el tipo específico de incidente
def determine_incident_type(sentence):
    try:
        if re.search(r'disparos|tiroteo', sentence, re.IGNORECASE):
            return 'Tiroteo'
        elif re.search(r'robo a mano armada', sentence, re.IGNORECASE):
            return 'Robo a Mano Armada'
        elif re.search(r'asesinato|homicidio', sentence, re.IGNORECASE):
            return 'Asesinato'
        else:
            return 'Otros'
    except Exception as e:
        print(f"Error determining incident type: {e}")
        return 'Desconocido'

months = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']

def extract_date(sentence):
    try:
        match = re.search(r'\b(\d{1,2})[-/](\d{1,2})[-/](\d{2,4})\b', sentence)
        if match:
            day = match.group(1)
            month = match.group(2)
            year = match.group(3)
            return f"{day}/{month}/{year}"
        
        match = re.search(r'\b(\d{1,2})\s*de\s*(\w+)\s*de\s*(\d{2,4})\b', sentence, re.IGNORECASE)
        if match:
            day = match.group(1)
            month = match.group(2).lower()
            year = match.group(3)
            month_number = months.index(month) + 1
            return f"{day}/{month_number:02d}/{year}"
        
        return 'Desconocido'
    except Exception as e:
        print(f"Error extracting date: {e}")
        return 'Desconocido'

# Función para determinar el número de víctimas
def extract_victim_count(sentence):
    try:
        match = re.search(r'(\d+)\s*(muertos|heridos|víctimas|lesionados|fallecidos)', sentence, re.IGNORECASE)
        if match:
            return match.group(1)
    except Exception as e:
        print(f"Error extracting victim count: {e}")
    
    return 'Desconocido'

# Función para determinar las acciones de la policía
def extract_police_action(sentence):
    try:
        if re.search(r'arresto|detención|captura|investigación|patrullaje', sentence, re.IGNORECASE):
            return 'Acción Policial'
    except Exception as e:
        print(f"Error extracting police action: {e}")
    
    return 'Sin Acción Policial'

# Función para crear la descripción del suceso
def create_description(row):
    try:
        description = f"Incidente de {row['Categoria']} ocurrido en {row['Ubicacion']}."
        if row['Número de Víctimas'] != 'Desconocido':
            description += f" Número de víctimas: {row['Número de Víctimas']}."
        if row['Acciones de la Policía'] == 'Acción Policial':
            description += " La policía ha tomado medidas."
        return description
    except Exception as e:
        print(f"Error creating description: {e}")
        return 'Desconocido'

# Aplicar las funciones para obtener las nuevas columnas
crime_related_df['Categoria'] = crime_related_df['Oracion'].apply(lambda x: categorize_sentence(x) if pd.notnull(x) else 'Desconocido')
crime_related_df['Ubicacion'] = crime_related_df['Oracion'].apply(lambda x: extract_location(x) if pd.notnull(x) else 'Desconocido')
crime_related_df['Nivel de gravedad'] = crime_related_df['Oracion'].apply(lambda x: determine_severity(x) if pd.notnull(x) else 'Desconocido')
crime_related_df['Fuente'] = crime_related_df['Titulo'].apply(lambda x: extract_source(x) if pd.notnull(x) else 'Desconocido')
crime_related_df['Tipo de Incidente'] = crime_related_df['Oracion'].apply(lambda x: determine_incident_type(x) if pd.notnull(x) else 'Desconocido')
crime_related_df['Fecha del Suceso'] = crime_related_df['Oracion'].apply(lambda x: extract_date(x) if pd.notnull(x) else 'Desconocido')
crime_related_df['Número de Víctimas'] = crime_related_df['Oracion'].apply(lambda x: extract_victim_count(x) if pd.notnull(x) else 'Desconocido')
crime_related_df['Acciones de la Policía'] = crime_related_df['Oracion'].apply(lambda x: extract_police_action(x) if pd.notnull(x) else 'Desconocido')

# Crear la columna de Descripción
crime_related_df['Descripción'] = crime_related_df.apply(lambda row: create_description(row) if pd.notnull(row).all() else 'Desconocido', axis=1)

# Guardar el DataFrame con las nuevas columnas en un nuevo archivo CSV
categorized_file_path = 'categorized_crime_related_output.csv'  # Actualiza la ruta según tu archivo
crime_related_df.to_csv(categorized_file_path, index=False)

print("Archivo categorizado guardado en:", categorized_file_path)
