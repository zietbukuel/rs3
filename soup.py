import requests as rq
import pandas as pd
from bs4 import BeautifulSoup as bs
from urllib.request import FancyURLopener

url = 'https://www.universidadperu.com/empresas/categorias.php'

html = rq.get(url).content.decode('utf-8')

class MyOpener(FancyURLopener):
    version='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'

import warnings
warnings.filterwarnings('ignore')

var = MyOpener()
html=var.open(url).read()

soup = bs(html)

enlaces = soup.find_all('a')[6:-15]
nombre = enlaces[0].text
url = enlaces[0].get('href')

#for link in enlaces:
#    print(link.text,link['href'])

nombres = []
links = []

for link in enlaces :
    nombres.append(link.text)
    links.append(link['href'])

datos = pd.DataFrame(zip(nombres,links),columns=['Nombre de la cateogria','URL de la categoria'])

datos.to_excel('resultados.xlsx')

print(datos)