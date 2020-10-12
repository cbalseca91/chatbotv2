import nltk
import numpy as np
import random
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords

from mongo import Mongo
from correo import Correo


# nltk.download('punkt')  # Instalar si no se tiene o si es la primera vez que se va a correr el proyecto
# nltk.download('wordnet')  # Instalar si no se tiene o si es la primera vez que se va a correr el proyecto

#TEXTOS ORIGINALES DE LA FUNCIONALIDAD DEL ALGORITMO
# f = open(r'','r',errors='ignore')
# raw = f.read()
# sent_tokens = nltk.sent_tokenize(raw)  # Convierte las respuestas en sentencias, tomando el \n como fin




class Chatbot:

    def __init__(self):
        self.mongo = Mongo() #Instanciamos la clase que conecta a la base de datos
        self.correo = Correo() #Instanciamos la clase que conecta el servicio SMTP para envío de correos
        self.sent_tokens = self.mongo.gettexto() #Consultamos a la tabla todas las frases almacenadas, como es texto plano, no afecta el tamaño.

        self.lemmer = nltk.stem.WordNetLemmatizer()  # Instanciamos el lematizador de nltk, es para obtener sinónimos

        # Definimos respuestas manuales a posibles saludos
        self.saludos_inputs = ("hola", "buenas", "qué tal", "hey", "buenos días")
        self.saludos_output = ["Hola", "Hola que tal", "Saludos. En que te puedo ayudar"]
        self.pregunta_output = ["¿Te fue útil la respuesta?","¿La respuesta te ayudó?","¿Estás satisfecho con la respuesta?"]
        self.satisfaccion_input_pos = ("si", "bien", "de acuerdo", "de a cuerdo", "correcto", "satisfecho")
        self.satisfaccion_input_neg = ("no", "mal", "desacuerdo", "tal vez", "talvez", "incompleto", "fallo", "falló")
        self.respuesta_output = ["Gracias. Si deseas, puedes hacerme otra pregunta", "Un gusto. Si necesitas algo más, hazme una nueva pregunta."]

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
            #Enviamos mensaje de error al correo.
            msg = f"No se ha entendido la pregunta\n\nPregunta del usuario: {user_response}"
            self.correo.enviarCorreo(msg)
            return "Lo siento no se entiende el mensaje que solicitas"
        else:
            resp = self.sent_tokens[idx]
            satisfaccion = random.choice(self.pregunta_output)
            respuesta = self.mongo.getRespuesta(resp)
            resp += f"<br><br><b>{satisfaccion} [Si/No]</b>"
            if len(respuesta['urlimage']) > 0:
                url = respuesta['urlimage']
                frase = respuesta["frase"]
                #Texto formateado con la imagen
                return f'{frase} <a href="{url}" target="_blank"> <img class="img-chat" src="{url}" alt="Respuesta Chat"> </a>'
            else:
                frase = respuesta["frase"]
                #Solo texto en la respuesta
                return frase

    def recibir_mensaje(self, texto):
        texto = texto.lower()
        if (self.saludar(texto) != None):
            return self.saludar(texto)
        else:
            return self.response(texto)

    def satisfaccion(self, respuesta, pregunta,original):
        for word in respuesta.split():
            #Verificamos si es una respuesta positiva
            if word.lower() in self.satisfaccion_input_pos:
                return random.choice(self.respuesta_output)
            #Verificamos si es una respuesta negativa
            elif word.lower() in self.satisfaccion_input_neg:
                #Enviamos mensaje de insatisfecho al correo.
                msg = f"Respuesta insatisfecha:\n\nPregunta del Usuario: {original}\n\nRespuesta del chat: {pregunta}\n\nRespuesta del Usuario: {respuesta}"
                self.correo.enviarCorreo(msg)
                return random.choice(self.respuesta_output)
            #Si no es nada, se intentará responder como una pregunta cualquiera.
            else:
                return self.recibir_mensaje(respuesta)

#chatbot = Chatbot()
#print(chatbot.recibir_mensaje('cascada'))
