from flask import Flask, render_template, url_for, request, session
from werkzeug.utils import redirect
import numpy as np

from chatbot import Chatbot
from mongo import Mongo

app = Flask(__name__)
app.secret_key = b'_Ch4Tb0t2o2o."#$'


@app.route('/')
def inicio():
    return render_template('index.html')


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    mongo = Mongo()
    msg = ""
    error = ""
    datos = mongo.getall()
    if request.method == 'POST':
        documento = {'titulo': "", 'frase': "", 'urlimage': ""}
        if 'pregunta' in request.form and 'respuesta' in request.form:
            documento['titulo'] = request.form['pregunta']
            documento['frase'] = request.form['respuesta']
            if 'url_imagen' in request.form and len(request.form['url_imagen']) > 0:
                documento['urlimage'] = request.form['url_imagen']
            if mongo.inserttexto(documento):
                msg = "Ingresado correctamente"
            else:
                error = "No se pudo ingresar ningún valor"
    if 'username' in session:
        return render_template('admin.html', msg=msg, error=error, datos=datos)
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg_error = ""
    if request.method == 'POST':
        if request.form['username'] == 'user_chatbot' and request.form['password'] == '$chat$bot$2020__!':
            # Iniciamos Sesión
            session['username'] = request.form['username']
            return redirect(url_for('admin'))
        else:
            return render_template('login.html', msg='Los datos están incorrectos')

    if 'username' not in session:
        return render_template('login.html')
    return redirect(url_for('admin'))

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/api/delete-frase/<id>', methods=['GET', 'POST'])
def deletefrase(id):
    mongo = Mongo()
    mongo.eliminarDocumento(id)
    return redirect(url_for('admin'))


@app.route('/api/chatbot', methods=['GET', 'POST'])
def chatbot():
    if request.method == 'POST':
        chatbot = Chatbot()
        if 'text' in request.form:
            return chatbot.recibir_mensaje(request.form['text'])
        elif 'satisfaccion' in request.form and 'pregunta' in request.form:
            return chatbot.satisfaccion(request.form['satisfaccion'], request.form['pregunta'],
                                        request.form['original'])
        else:
            return "Nada que responder"
    return "No se ha solicitado ninguna pregunta."
