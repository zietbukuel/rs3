# RS3

## Instalación

Debes instalar las siguientes dependencias:

- python virtualenv/venv
- python pip

Cuando estén instalados ejecuta uno de los siguientes comandos:

Crea el virtual environment

    python3 -m venv env

Si usas bash o zsh (Linux o Mac)

    source env/bin/activate
    
Si usas fish

	. env/bin/activate.fish

Si usas csh o tcsh

	source env/bin/activate.csh

Si usas PowerShell (Windows)

	env\Scripts\Activate.ps1

Instalar las dependencias del proyecto:

	pip install -r requirements.txt
	deactivate

## Configuración

Existe un archivo `dot.env` en la carpeta del proyecto con algunas variables necesarias para conectarnos a la API de Twitter. Haz una copia de este archivo y nómbralo `.env`, una vez hecho esto llena las variables.

	CONSUMER_KEY=
	CONSUMER_SECRET=
	ACCESS_TOKEN=
	ACCESS_TOKEN_SECRET=

## Ejecución

Ejecuta el archivo rs3.py con la opcion `--file` o `-f` y la ruta de un archivo conteniendo los hashtags o palabras clave.

	./rs3.py --file archivo.txt