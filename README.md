# RS3

## Instalación

Debes instalar las siguientes dependencias:

- python virtualenv/venv
- python pip

Cuando estén instalados ejecuta uno de los siguientes comandos:

Crea el virtual environment

    python3 -m venv venv

Si usas bash o zsh (Linux o Mac)

    source venv/bin/activate
    
Si usas fish

	. venv/bin/activate.fish

Si usas csh o tcsh

	source venv/bin/activate.csh

Si usas PowerShell (Windows)

	venv\Scripts\Activate.ps1

Instalar las dependencias del proyecto:

	pip install -r requirements.txt

## Configuración

Existe un archivo `dot.env` en la carpeta del proyecto con algunas variables necesarias para ejecutar el script. Por el momento tenemos KEYWORDS que son las palabras clave para hacer búsquedas en los sitios web de notificias.

	KEYWORDS=

## Ejecución

Ejecuta el archivo rs3.py con la opcion `--file` o `-f` y la ruta de un archivo conteniendo los hashtags o palabras clave.

	./rs3.py --file archivo.txt

Para ver una lista completa de todas las opciones ejecuta:

	./rs3.py --help