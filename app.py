from flask import Flask, render_template, url_for, request
import numpy as np

from chatbot import Chatbot

app = Flask(__name__)

@app.route('/')
def inicio():
    return render_template('index.html')

@app.route('/api/chatbot', methods=['GET','POST'])
def chatbot():
    if request.method == 'POST':
        chatbot = Chatbot()
        if 'text' in request.form:
            return chatbot.recibir_mensaje(request.form['text'])
        elif 'satisfaccion' in request.form and 'pregunta' in request.form:
            return chatbot.satisfaccion(request.form['satisfaccion'], request.form['pregunta'], request.form['original'])
        else:
            return "Nada que responder"
    return "No se ha solicitado ninguna pregunta."