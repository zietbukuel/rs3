import requests
from bs4 import BeautifulSoup
import os

def guardar_contenido_wiki(url):
    try:
        # Hacer una solicitud a la URL
        response = requests.get(url)
        response.raise_for_status()
        
        # Analizar el contenido HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extraer el bloque de contenido
        contenido = soup.find(id='mw-content-text')
        
        if not contenido:
            print("No se encontró el bloque de contenido en la página.")
            return
        
        # Obtener el título de la página para usar como nombre del archivo
        titulo = soup.find('h1', {'id': 'firstHeading'}).text.strip()
        
        # Crear el nombre del archivo con el título de la wiki
        nombre_archivo = f"{titulo}.txt"
        
        # Guardar el contenido en el archivo TXT
        with open(nombre_archivo, 'w', encoding='utf-8') as file:
            file.write(contenido.get_text())
        
        print(f"El contenido de la wiki se ha guardado en {nombre_archivo}.")
    
    except requests.RequestException as e:
        print(f"Error al hacer la solicitud: {e}")
    except Exception as e:
        print(f"Se produjo un error: {e}")

# Ejemplo de uso
url_wiki = 'https://es.m.wikipedia.org/wiki/Christian_Nodal'
guardar_contenido_wiki(url_wiki)
