# -*- coding: utf-8 -*-

import tweepy

class XClient:
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        """
        Constructor que inicializa los parámetros de autenticación de la API de Twitter

        Parámetros:
        consumer_key: clave del consumidor de la API de Twitter
        consumer_secret: secreto del consumidor de la API de Twitter
        access_token: token de acceso para la API de Twitter
        access_token_secret: secreto del token de acceso para la API de Twitter
        """
        self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(self.auth)

    def get_tweets(self, hashtag):
        """
        Método para obtener tweets que contienen un hashtag específico

        Parámetros:
        hashtag: el hashtag a buscar en los tweets

        Retorna:
        Una lista de tweets que contienen el hashtag especificado
        """
        tweets = self.api.search_tweets(q=hashtag, lang="en", rpp=10)

        return tweets
