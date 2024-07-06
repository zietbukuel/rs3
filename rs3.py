#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import getopt
import yaml
from webscrapper import WebScraper

# Verifica si el archivo de configuracion exists y lo carga
config_file = "config.yaml"
config = None
if os.path.isfile(config_file):
    config = yaml.safe_load(config_file)

def help():
    """
    Muestra el mensaje de ayuda con las opciones disponibles para el uso del script
    """
    print("Usage: ./rs3.py [-f|--file=archivo.txt] [-o|--output=archivo.txt] [--db] [-h|--help] [-v|--version]")
    print("Options:")
    print("""
    -c, --config=ARCHIVO    El archivo de configuracion a procesar.
    -o, --output=ARCHIVO    Guardar los datos en un archivo de texto.
    --db                    No guardar los datos en la base de datos.
    -h, --help              Este mensaje.
    -v, --version           Muestra la versión del programa.
    """)
    sys.exit()

def main(argv):
    """
    Función principal que gestiona la lógica del script

    Parámetros:
    argv: lista de argumentos pasados al script desde la línea de comandos
    """

    # Inicializa las variables
    output = None
    config_file = "config.yml"

    try:
        opts, args = getopt.gnu_getopt(argv, "c:o:vh", ["config=", "output=" "db" "version", "help"])
    except getopt.GetoptError as err:
        # Muestra el error y termina la ejecución si los argumentos no son válidos
        print(str(err))
        sys.exit(2)

    # Procesa las opciones y argumentos
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            # Muestra el mensaje de ayuda y termina la ejecución
            help()
        elif opt in ("-v", "--version"):
            # Muestra la versión del programa y termina la ejecución
            print("1.0")
            sys.exit()
        elif opt in ("-c", "--config"):
            config_file = arg
        elif opt in ("-o", "--output"):
            output = arg
        else:
            # Opcion inválida
            print("Error: opción inválida.")
            sys.exit(1)

    config = None
    if os.path.isfile(config_file):
        with open(config_file, 'r') as stream:
            config = yaml.safe_load(stream)

    if not output:
        output = "output.csv"

    # Si el archivo output existe, eliminalo
    if os.path.isfile(output):
        os.remove(output)

    if config is not None:
        print(">> Configuración: " + config_file)

        # Carga el sitio web
        for site in config['websites']:
            print(">> Procesando Sitio Web: " + site['url'])

            # Inicializa el objeto WebScraper
            scrapper = WebScraper()

            # Inicia una busqueda por cada palabra clave
            for keyword in config['keywords']:
                print(">> Buscando: " + keyword)

                search_url = site['search_url']

                if site['data_name'] is None:
                    # Reemplazar {} con la palabra clave
                    search_url = site['search_url'].replace("{}", keyword)
                    # Reemplazar espacios con un +
                    search_url = search_url.replace(" ", "+")
                    # Realizar la solicitud GET
                    scrapper.set_url(search_url)
                    scrapper.fetch()

                if site['last_page'] is None:
                    total_pages = 1
                    rango = total_pages + 1
                else:
                    total_pages = scrapper.get_total_pages(site['last_page'])
                    rango = total_pages

                print(">> URL de Búsqueda: " + search_url)
                print(">> Total de Páginas: " + str(total_pages))

                # Navegar por todas las páginas
                for page in range(1, rango):
                    print(">> Página: " + str(page))

                    # Agregar el numero de pagina al final de la URL
                    if site['last_page'] is not None:
                        search_url = search_url + str(page) + "/"
                        print(">> URL de la Página: " + search_url)

                        scrapper.set_url(search_url)
                        scrapper.fetch()
                    else:
                        # Realizar la solicitud POST
                        scrapper.set_url(search_url)
                        scrapper.fetch('POST', { site['data_name']: keyword })

                    # Seleccionar los enlaces
                    results = scrapper.select(site['results'], text=False)
                    
                    links = []
                    for result in results:
                        link = result['href']
                        # Si el link no empieza con https:// entonces agregar el dominio
                        if not link.startswith("https://"):
                            link = site['url'] + link

                        # Ignora los enlaces que contengan /video/ en la URL
                        if "/video/" in result['href']:
                            continue

                        # Ignora los enlaces que contengan /gallery/ en la URL
                        if "/gallery/" in result['href']:
                            continue

                        # Agrega el enlace a la lista
                        links.append(link)
                        
                    # Exportar los datos
                    scrapper.export(links, site['content'], output)
                print("-----------------------------")

    if not config:
        print("Error: El archivo de configuración no existe.")
        sys.exit(1)

if __name__ == '__main__':
    main(sys.argv[1:])
