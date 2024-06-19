#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import getopt
from mongodb import MongoDB
from webscrapper import WebScraper
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Carga variables del archivo .env
load_dotenv()

def help():
    """
    Muestra el mensaje de ayuda con las opciones disponibles para el uso del script
    """
    print("Usage: ./rs3.py [-f|--file=archivo.txt] [-o|--output=archivo.txt] [--db] [-h|--help] [-v|--version]")
    print("Options:")
    print("""
    -f, --file=ARCHIVO      El archivo de texto conteniendo las palabras clave.
    -o, --output=ARCHIVO    Guardar los datos en un archivo de texto.
    --db                    No guardar los datos en la base de datos.
    -h, --help              Este mensaje.
    -v, --version           Muestra la versión del programa.
    """)
    sys.exit()

def save_articles(articles, keyword, content, opt, arg):
    for articulo in articles:
        # Solo incluir los resultados que contienen la palabra clave
        if keyword in articulo.text:
            print(articulo.text)

            # Visitar el articulo
            href = articulo.find_element(By.TAG_NAME, value='a').click()

            scraper = WebScraper()
            scraper.set_url(href)
            scraper.fetch()
            elements = scraper.select(content)

            output = "output.txt"
            if opt in ("-o", "--output"):
                # Guarda los datos en un archivo de texto
                output = arg

            print("++ Archivo de salida: " + output)

            with open(output, "w") as o:
                o.truncate(0)
                for element in elements:
                    o.write(element + "\n")
                o.close()

def main(argv):
    """
    Función principal que gestiona la lógica del script

    Parámetros:
    argv: lista de argumentos pasados al script desde la línea de comandos
    """
    try:
        opts, args = getopt.gnu_getopt(argv, "f:o:vh", ["file=", "output=" "db" "version", "help"])
    except getopt.GetoptError as err:
        # Muestra el error y termina la ejecución si los argumentos no son válidos
        print(str(err))
        sys.exit(2)

    file = None

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            # Muestra el mensaje de ayuda y termina la ejecución
            help()
        elif opt in ("-v", "--version"):
            # Muestra la versión del programa y termina la ejecución
            print("1.0")
            sys.exit()
        elif opt in ("-f", "--file"):
            # Establece el archivo a procesar
            file = arg
            print(">> Archivo: " + file)

            # Verifica si el archivo existe
            if not os.path.isfile(file):
                print("Error: el archivo no existe.")
                sys.exit()

            with open(file, 'r') as f:                
                for line in f: 
                    # Verificar que el formato correcto exista
                    if '|' not in line:
                        print("Error: formato incorrecto.")
                        continue

                    # "url|search|pagination|pages|results|content"
                    url, search, pagination, pages, results, content = line.strip().split('|')

                    print(">> Procesando URL: " + url)

                    driver = webdriver.Chrome()
                    driver.maximize_window()

                    try:
                        driver.get(url)

                        # Inicia una busqueda por cada palabra clave
                        for keyword in os.getenv("KEYWORDS").split(","):
                            print(">> Buscando: " + keyword)

                            search_box = driver.find_element(By.CSS_SELECTOR, value=search)
                            # Escribir en el buscador y presionar Enter
                            search_box.send_keys(keyword)
                            search_box.send_keys(Keys.RETURN)

                            # Si existe el elemento de paginación
                            if driver.find_elements(By.CSS_SELECTOR, pagination):
                                # Espera a que la página cargue
                                WebDriverWait(driver, 10).until(
                                    EC.visibility_of_all_elements_located((By.CSS_SELECTOR, pagination))
                                )

                                # Usa Selenium para navegar por las páginas de resultados
                                pagination = driver.find_element(By.CSS_SELECTOR, value=pagination)
                                pages = pagination.find_elements(By.CSS_SELECTOR, value=pages)

                                p = 1
                                for page in pages:
                                    print(">> Página: " + str(p))

                                    # Espera a que la página cargue
                                    WebDriverWait(driver, 10).until(
                                        EC.visibility_of_all_elements_located((By.CSS_SELECTOR, results))
                                    )

                                    # Usa Selenium para extraer los resultados de la página
                                    resultados = driver.find_elements(By.CSS_SELECTOR, value=results)
                                    save_articles(resultados, keyword, content, opt, arg)

                                    # Si hay una excepcion tipo selenium.common.exceptions.StaleElementReferenceException
                                    # se puede intentar con un try/except
                                    try:
                                        # Navega a la siguiente página
                                        page.click()
                                    except:
                                        # Si hay una excepcion tipo selenium.common.exceptions.StaleElementReferenceException
                                        # se puede intentar con un try/except
                                        print("Error: Elemento no encontrado.")
                                        break

                                    p += 1
                            else:
                                # Espera a que la página cargue
                                WebDriverWait(driver, 10).until(
                                    EC.visibility_of_all_elements_located((By.CSS_SELECTOR, results))
                                )

                                # Usa Selenium para extraer los resultados de la página
                                resultados = driver.find_elements(By.CSS_SELECTOR, value=results)
                                save_articles(resultados, keyword, content, opt, arg)
                    finally:
                        driver.quit()

                # Cierra el archivo
                f.close()
        else:
            assert False, "Error: opción inválida."

    if not file:
        # Muestra el mensaje de ayuda si no se especifica ningún archivo
        help()

if __name__ == '__main__':
    main(sys.argv[1:])
