# -*- coding: utf-8 -*-

import requests
import sys
import os
import csv
import signalhandler
import pandas as pd
from bs4 import BeautifulSoup

class WebScraper:
    def __init__(self, headers=None):
        """
        Inicializa el objeto WebScraper con encabezados opcionales.
        """
        self.url = None
        self.headers = headers if headers else {'User-Agent': 'Mozilla/5.0'}
        self.soup = None

    def set_url(self, url):
        """
        Establece la URL que se va a raspar.
        
        :param url: La URL de la página web.
        """
        self.url = url

    def fetch(self, method='GET', data=None):
        """
        Realiza una solicitud GET a la URL establecida y parsea el contenido HTML.

        :param method: Método HTTP a utilizar ('GET' o 'POST').
        :param data: Datos a enviar en la solicitud POST (si corresponde).
        """
        if self.url:
            try:
                if method == 'POST':
                    response = requests.post(self.url, headers=self.headers, data=data)
                else:
                    response = requests.get(self.url, headers=self.headers)

                response = requests.get(self.url, headers=self.headers)
                response.raise_for_status()  # Lanza HTTPError para respuestas incorrectas
                self.soup = BeautifulSoup(response.content, 'html.parser')
            except requests.exceptions.RequestException as e:
                print(f'Error al recuperar la página web: {e}')
                self.soup = None
        else:
            print('URL no establecida. Por favor, establezca la URL usando set_url.')
            sys.exit()

    def select(self, selector, text=True):
        """
        Selecciona elementos del contenido HTML utilizando un selector CSS.
        
        :param selector: El selector CSS para los elementos deseados.
        :param text: Si es True, retorna el texto de los elementos seleccionados.
        :return: Lista de textos o elementos seleccionados.
        """
        if self.soup:
            elements = self.soup.select(selector)
            if text:
                return [element.get_text().strip() for element in elements]
            return elements
        else:
            print('El objeto Soup es None. ¿Falló la solicitud?')
            return []
        
    def get_total_pages(self, selector):
        """
        Obtiene el número total de páginas desde un elemento que contiene el número de páginas.
        
        :param selector: El selector CSS para el elemento que contiene el número total de páginas.
        :return: Número total de páginas como entero.
        """
        if self.soup:
            return int(self.select(selector)[0])
        else:
            print('El objeto Soup es None. ¿Falló la solicitud?')
            return 0

    def export(self, links, selector, output):
        """
        Exporta el contenido de varias URLs a un archivo CSV.
        
        :param links: Lista de URLs a raspar.
        :param selector: El selector CSS para los elementos de contenido.
        :param output: El nombre del archivo CSV de salida.
        """
        # Si links está vacío
        if not links:
            print("Error: No se encontraron resultados.")
            return
        
        data = []

        for link in links:
            try:
                print(f"Procesando {link} ...")
                self.url = link
                self.fetch()
                contenido = self.select(selector)
                titulo = self.select("title")[0]

                if not contenido or not titulo:
                    print("Error: No se encontró el contenido o el título para la URL: " + link)
                    break
                
                # Agregar los datos a la lista
                data.append([titulo, ' '.join(contenido)])
            except KeyboardInterrupt:
                continue
            
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
