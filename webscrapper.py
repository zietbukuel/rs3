# -*- coding: utf-8 -*-

import requests
import sys
import os
import csv
import time
import pandas as pd
from bs4 import BeautifulSoup

class WebScraper:
    def __init__(self, headers=None):
        self.url = None
        self.headers = headers if headers else {'User-Agent': 'Mozilla/5.0'}
        self.soup = None

    def set_url(self, url):
        self.url = url

    def fetch(self):
        if self.url:
            try:
                response = requests.get(self.url, headers=self.headers)
                response.raise_for_status()  # Lanza HTTPError para respuestas incorrectas
                self.soup = BeautifulSoup(response.content, 'html.parser')
            except requests.exceptions.RequestException as e:
                print(f'Error al recuperar la página web: {e}')
                self.soup = None
            except ConnectionRefusedError:
                print('La conexión fue rechazada. Por favor, verifica tu conexión a internet y la URL.')
                self.soup = None
        else:
            print('URL no establecida. Por favor, establezca la URL usando set_url.')
            sys.exit()

    def select(self, selector):
        if self.soup:
            elements = self.soup.select(selector)
            return [element.get_text().strip() for element in elements]
        else:
            print('El objeto Soup es None. ¿Falló la solicitud?')
            return []

    def export(self, links, selector, output):
        # Si links esta vacio
        if not links:
            print("Error: No se encontraron resultados.")
            return
        
        data = []

        for link in links:
            self.url = link
            self.fetch()
            contenido = self.select(selector)
            titulo = self.select("title")[0]

            if not contenido or not titulo:
                print("Error: No se encontró el contenido o el título para la URL: " + link)
                break
            
            # Agregar los datos a la lista
            data.append([titulo, ' '.join(contenido)])

            # Esperar 5 segundos
            time.sleep(5)
            
        # Crear un DataFrame con los datos
        df = pd.DataFrame(data, columns=['Titulo', 'Contenido'])

        # Si el archivo existe
        if os.path.isfile(output):
            # Agregar los datos al archivo sin el encabezado
            df.to_csv(output, index=False, mode='a', header=False, quoting=csv.QUOTE_ALL)
        else:
            # Exporta los datos a un archivo CSV
            df.to_csv(output, index=False, quoting=csv.QUOTE_ALL)

        print("Datos exportados a: " + output)
