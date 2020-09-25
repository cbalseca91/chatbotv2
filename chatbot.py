import nltk
import numpy as np
import random
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords


# nltk.download('punkt')  # Instalar si no se tiene o si es la primera vez que se va a correr el proyecto
# nltk.download('wordnet')  # Instalar si no se tiene o si es la primera vez que se va a correr el proyecto

#TEXTOS ORIGINALES DE LA FUNCIONALIDAD DEL ALGORITMO
# f = open(r'','r',errors='ignore')
# raw = f.read()
# sent_tokens = nltk.sent_tokenize(raw)  # Convierte las respuestas en sentencias, tomando el \n como fin

from mongo import Mongo


class Chatbot:

    def __init__(self):
        self.mongo = Mongo() #Instanciamos la clase que conecta a la base de datos
        self.sent_tokens = self.mongo.gettexto() #Consultamos a la tabla todas las frases almacenadas, como es texto plano, no afecta el tamaño.

        self.lemmer = nltk.stem.WordNetLemmatizer()  # Instanciamos el lematizador de nltk, es para obtener sinónimos

        # Definimos respuestas manuales a posibles saludos
        self.saludos_inputs = ("hola", "buenas", "qué tal", "hey", "buenos días",)
        self.saludos_output = ["Hola", "Hola que tal", "Saludos. En que te puedo ayudar"]

        # Obtenemos un arreglo con los signos de puntuación para limpiar los tokens
        self.remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

    def saludar(self, sentence):
        for word in sentence.split():
            if word.lower() in self.saludos_inputs:
                return random.choice(self.saludos_output)

    # Función para obtener todos los lemas por cada token desde NLTK
    def LemTokens(self, tokens):
        return [self.lemmer.lemmatize(token) for token in tokens]

    # Función para eliminar los signos de puntuación
    def LemNormalize(self, text):
        return self.LemTokens(nltk.word_tokenize(text.lower().translate(self.remove_punct_dict)))

    # Función para comparar la similitud y lanzar respuesta
    def response(self, user_response):
        self.sent_tokens.append(user_response)
        TfidfVec = TfidfVectorizer(tokenizer=self.LemNormalize, stop_words=stopwords.words('spanish'))
        tfid = TfidfVec.fit_transform(self.sent_tokens)
        vals = cosine_similarity(tfid[-1],
                                 tfid)  # Comparamos el último que es la respuesta del usuario, contra todo el texto
        idx = vals.argsort()[0][-2]
        flat = vals.flatten()
        flat.sort()
        req_tfid = flat[-2]
        if (req_tfid == 0):
            return "Lo siento no se entiende el mensaje que solicitas"
        else:
            resp = self.sent_tokens[idx]
            url = self.mongo.getimagen(resp)
            if len(url) > 0:
                #Texto formateado con la imagen
                return f'{resp} <a href="{url}" target="_blank"> <img class="img-chat" src="{url}" alt="Respuesta Chat"> </a>'
            else:
                #Solo texto en la respuesta
                return resp

    def recibir_mensaje(self, texto):
        texto = texto.lower()
        if (self.saludar(texto) != None):
            return self.saludar(texto)
        else:
            return self.response(texto)


#chatbot = Chatbot()
#print(chatbot.recibir_mensaje('cascada'))
