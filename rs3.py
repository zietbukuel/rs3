#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import getopt
from mongodb import MongoDB
from webscrapper import WebScraper
from dotenv import load_dotenv

# Carga variables del archivo .env
load_dotenv()

def help():
    """
    Muestra el mensaje de ayuda con las opciones disponibles para el uso del script
    """
    print("Usage: ./rs3.py [-f|--file=archivo.txt]")
    print("Options:")
    print("""
    -f, --file=ARCHIVO      El archivo de texto conteniendo las palabras clave.
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
    try:
        opts, args = getopt.gnu_getopt(argv, "f:vh", ["file=", "db" "version", "help"])
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
            print("Archivo: " + file)

            # Verifica si el archivo existe
            if not os.path.isfile(file):
                print("Error: el archivo no existe.")
                sys.exit()

            with open(file, 'r') as f:
                if opt in ("--db"):
                    db = MongoDB(
                        os.getenv("MONGODB_HOST"),
                        int(os.getenv("MONGODB_PORT")),
                        os.getenv("MONGODB_DATABASE")
                    )
                    db.connect()
                
                for line in f: 
                    # Verificar que el formato correcto exista
                    if '|' not in line:
                        print("Error: formato incorrecto.")
                        continue

                    # "url:selector" (url y selector son separados por "|")
                    url, selector = line.strip().split('|')
                    print("URL: " + url)
                    print("Selector: " + selector)
                    scraper = WebScraper()
                    scraper.set_url(url)
                    scraper.fetch()
                    elements = scraper.select(selector)
                    print(elements)

                    if opt in ("--db"):
                        # Guarda los datos en MongoDB
                        db.create("webdata", elements)
                        db.disconnect()

            # Cierra el archivo
            f.close()
        else:
            assert False, "Error: opción inválida."

    if not file:
        # Muestra el mensaje de ayuda si no se especifica ningún archivo
        help()

if __name__ == '__main__':
    main(sys.argv[1:])
