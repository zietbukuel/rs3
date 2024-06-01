# -*- coding: utf-8 -*-

import requests
import sys
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
        else:
            print('URL no establecida. Por favor, establezca la URL usando set_url.')
            sys.exit()

    def select(self, tag, **attributes):
        if self.soup:
            elements = self.soup.find_all(tag, **attributes)
            return [element.get_text() for element in elements]
        else:
            print('El objeto Soup es None. ¿Falló la solicitud?')
            return []
