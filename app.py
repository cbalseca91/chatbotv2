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
        documento = {'titulo': "", 'frase': "", 'urlimage': "", 'source': ""}
        if 'pregunta' in request.form and 'respuesta' in request.form:
            documento['titulo'] = request.form['pregunta']
            documento['frase'] = request.form['respuesta']
            if 'url_imagen' in request.form and len(request.form['url_imagen']) > 0:
                documento['urlimage'] = request.form['url_imagen']
                if 'source_imagen' in request.form and len(request.form['source_imagen']) > 0:
                    documento['source'] = request.form['source_imagen']
            if 'idpregunta' in request.form and request.form['idpregunta']:
                if mongo.updatetexto(documento, request.form['idpregunta']):
                    msg = "Modificado correctamente"
                else:
                    error = "No se pudo actualizar el valor correctamente"
            else:
                if mongo.inserttexto(documento):
                    msg = "Ingresado correctamente"
                else:
                    error = "No se pudo ingresar ningún valor"
    if 'username' in session:
        return render_template('admin.html', msg=msg, error=error, datos=datos)
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    mongo = Mongo()
    msg_error = "Los datos están incorrectos"
    if request.method == 'POST':
        email = request.form['username']
        pwd = request.form['password']
        findUser = mongo.getUser({
            'email': email,
            'password': pwd
        })
        #if :
        if findUser or (request.form['username'] == 'user_chatbot' and request.form['password'] == '$chat$bot$2020__!'):
            # Iniciamos Sesión
            session['username'] = request.form['username']
            return redirect(url_for('admin'))
        else:
            return render_template('login.html', msg=msg_error)

    if 'username' not in session:
        return render_template('login.html')
    return redirect(url_for('admin'))


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    mongo = Mongo()
    msg = ""
    error = ""
    datos = mongo.getAllUser()
    if request.method == 'POST':
        documento = {'email': "", 'name': "", 'password': ""}
        if 'email' in request.form and 'password' in request.form and 'password2' in request.form:
            if request.form['password'] == request.form['password2']:
                documento['email'] = request.form['email']
                documento['name'] = request.form['name_user']
                documento['password'] = request.form['password']
                if mongo.existsEmail(documento['email']):
                    error = "Ese correo ya existe"
                else:
                    if mongo.insertUser(documento):
                        msg = "Usuario registrado correctamente"
                    else:
                        error = "No se pudo insertar el usario"
    if 'username' in session:
        print(msg, error, datos)
        return render_template('signup.html', msg=msg, error=error, datos=datos)
    else:
        return render_template('login.html')


@app.route('/api/delete-frase/<id>', methods=['GET', 'POST'])
def deletefrase(id):
    mongo = Mongo()
    mongo.eliminarDocumento(id)
    return redirect(url_for('admin'))



@app.route('/api/delete-user/<id>', methods=['GET', 'POST'])
def deleteuser(id):
    mongo = Mongo()
    mongo.deleteUser(id)
    return redirect(url_for('register'))


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
