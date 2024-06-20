import requests
from bs4 import BeautifulSoup as bs

url = 'https://www.universidadperu.com/empresas/categorias.php'

# Realizar la solicitud
response = requests.get(url)
response.raise_for_status()  # Asegurarse de que la solicitud fue exitosa

# Analizar el contenido HTML
soup = bs(response.content, 'html.parser')

# Encontrar todas las categorías
categorias = soup.find_all('div', class_='list-group')

# Recorrer cada categoría y mostrar sus datos
for categoria in categorias:
    nombre_categoria = categoria.find('h4', class_='list-group-item-heading').text.strip()
    empresas = categoria.find_all('a', class_='list-group-item')
    print(f'Categoría: {nombre_categoria}')
    for empresa in empresas:
        nombre_empresa = empresa.text.strip()
        link_empresa = empresa['href']
        print(f'- Empresa: {nombre_empresa} | Link: {link_empresa}')
    print()
