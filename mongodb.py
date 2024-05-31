# -*- coding: utf-8 -*-

from pymongo import MongoClient

class MongoDB:
    def __init__(self, host, port, database):
        """
        Constructor que inicializa los parámetros de conexión

        Parámetros:
        host: la dirección del servidor MongoDB
        port: el puerto en el que el servidor MongoDB está escuchando
        database: el nombre de la base de datos a la que se conectará
        """
        self.host = host
        self.port = port
        self.database = database
        self.client = None
        self.db = None

    def connect(self):
        """
        Método para establecer la conexión con la base de datos
        """
        self.client = MongoClient(self.host, self.port)
        self.db = self.client[self.database]

    def disconnect(self):
        """
        Método para cerrar la conexión con la base de datos
        """
        if self.client:
            self.client.close()

    def create(self, collection, data):
        """
        Método para insertar un documento en una colección

        Parámetros:
        collection: el nombre de la colección en la que se insertará el documento
        data: el documento que se insertará (en formato de diccionario)
        """
        self.db[collection].insert_one(data)

    def read(self, collection, query):
        """
        Método para leer documentos de una colección según un criterio de búsqueda

        Parámetros:
        collection: el nombre de la colección de la que se leerán los documentos
        query: el criterio de búsqueda (en formato de diccionario)
        """
        return self.db[collection].find(query)

    def update(self, collection, query, data):
        """
        Método para actualizar documentos en una colección según un criterio de búsqueda

        Parámetros:
        collection: el nombre de la colección en la que se actualizarán los documentos
        query: el criterio de búsqueda para encontrar los documentos a actualizar (en formato de diccionario)
        data: los nuevos datos para actualizar los documentos (en formato de diccionario)
        """
        self.db[collection].update_many(query, {"$set": data})

    def delete(self, collection, query):
        """
        Método para eliminar documentos de una colección según un criterio de búsqueda

        Parámetros:
        collection: el nombre de la colección de la que se eliminarán los documentos
        query: el criterio de búsqueda para encontrar los documentos a eliminar (en formato de diccionario)
        """
        self.db[collection].delete_many(query)