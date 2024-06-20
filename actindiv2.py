import requests
from bs4 import BeautifulSoup
import os

def guardar_contenido_body_sin_lineas_blancas(url):
    try:
        # Hacer una solicitud a la URL
        response = requests.get(url)
        response.raise_for_status()
        
        # Analizar el contenido HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extraer el cuerpo del contenido
        body = soup.find('body')
        
        if not body:
            print("No se encontró el cuerpo del contenido en la página.")
            return
        
        # Obtener el título de la página para usar como nombre del archivo
        titulo = soup.find('title').text.strip()
        
        # Crear el nombre del archivo con el título de la página
        nombre_archivo = f"{titulo}.txt"
        
        # Extraer el texto del cuerpo y eliminar líneas en blanco
        texto_body = body.get_text()
        lineas = [linea.strip() for linea in texto_body.splitlines() if linea.strip()]
        
        # Guardar el contenido del cuerpo en el archivo TXT sin líneas en blanco
        with open(nombre_archivo, 'w', encoding='utf-8') as file:
            for linea in lineas:
                file.write(linea + '\n')
        
        print(f"El contenido del cuerpo de la página se ha guardado en {nombre_archivo} sin líneas en blanco.")
    
    except requests.RequestException as e:
        print(f"Error al hacer la solicitud: {e}")
    except Exception as e:
        print(f"Se produjo un error: {e}")

# Ejemplo de uso
url_pagina = 'https://es.m.wikipedia.org/wiki/Christian_Nodal'  # Reemplaza esta URL con la URL de la página que deseas scrape.
guardar_contenido_body_sin_lineas_blancas(url_pagina)
