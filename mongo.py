from pymongo import MongoClient
from bson.objectid import ObjectId
from passlib.context import CryptContext

class Mongo:
    def __init__(self):
        self.cliente = MongoClient('localhost', port=27017)  # Para el caso de ser Local
        # Seleccionamos o creamos la base de Datos
        self.dbname = self.cliente['chatbot']
        self.pwd_context = CryptContext(
            schemes=["pbkdf2_sha256"],
            default="pbkdf2_sha256",
            pbkdf2_sha256__default_rounds=30000
        )

    def getall(self):
        # Seleccionamos o creamos la colección (Tabla)
        colection = self.dbname['textos']
        # Retonamos todos los textos
        return colection.find({})

    def gettexto(self):
        respuesta = []
        # Seleccionamos o creamos la colección (Tabla)
        colection = self.dbname['textos']
        # Consultamos todos los textos y lo guardamos en un arreglo
        for frase in colection.find({}):
            try:
                respuesta.append(frase['titulo'])
            except KeyError:
                print("No está bien definido el documento de la colección.")
        return respuesta

    # {frase: 'frase', urlimage: 'http://'}
    def inserttexto(self, documento):
        # Seleccionamos o creamos la colección (Tabla)
        colection = self.dbname['textos']
        return colection.insert_one(documento)

    # {frase: 'frase', urlimage: 'http://'}
    def updatetexto(self, documento, id):
        # Seleccionamos o creamos la colección (Tabla)
        colection = self.dbname['textos']
        myquery = {'_id': ObjectId(id)}
        newvalues = {'$set': documento}
        return colection.update_one(myquery, newvalues)

    def getRespuesta(self, titulo):
        urlimage = ""
        frase = ""
        # Seleccionamos o creamos la colección (Tabla)
        colection = self.dbname['textos']
        respuesta = colection.find_one({'titulo': titulo})  # consultamos la frase exacta
        # Revisamos si existe la key caso contrario, devolvemos vacío
        # Revisamos que tenga datos en url
        try:
            urlimage = respuesta['urlimage']
        except KeyError:
            urlimage = ""
        # Revisamos que tenga datos en frase
        try:
            frase = respuesta['frase']
        except KeyError:
            frase = ""

        return {"urlimage": urlimage, "frase": frase}

    def eliminarDocumento(self, id):
        # Seleccionamos o creamos la colección (Tabla)
        colection = self.dbname['textos']
        return colection.delete_one({'_id': ObjectId(id)})

    # {email: 'cbalseca@est.ups.edu.ec', name: 'Christian Balseca', password: 'cbalseca2021!'}
    def insertUser(self, documento):
        # Seleccionamos o creamos la colección (Tabla)
        colection = self.dbname['users']
        documento['password'] = self.pwd_context.encrypt(documento['password'])
        return colection.insert_one(documento)

    def existsEmail(self, email):
        # Seleccionamos o creamos la colección (Tabla)
        colection = self.dbname['users']
        respuesta = colection.find_one({"email": email})
        return True if respuesta else False

    def getUser(self, userdata):
        # Seleccionamos o creamos la colección (Tabla)
        colection = self.dbname['users']
        user = colection.find_one({
            "email": userdata["email"]
        })
        if self.pwd_context.verify(userdata['password'], user['password']):
            return user
        else:
            return None

    def getAllUser(self):
        # Seleccionamos o creamos la colección (Tabla)
        colection = self.dbname['users']
        user = colection.find({})
        return user

    def deleteUser(self, id):
        # Seleccionamos o creamos la colección (Tabla)
        colection = self.dbname['users']
        return colection.delete_one({'_id': ObjectId(id)})

'''
mongo = Mongo()
mongo.inserttexto({
    'titulo': "definición modelo cascada",
    'frase': "El modelo en cascada es un proceso de desarrollo secuencial, en el que el desarrollo de software se concibe como  un conjunto de etapas que  se ejecutan una tras otra. Se le denomina así por las posiciones que ocupan las diferentes fases que componen el proyecto, colocadas una encima de otra, y siguiendo un flujo de ejecución de arriba hacia abajo, como una cascada.",
    'urlimage': "https://user.oc-static.com/upload/2017/07/11/14997883020913_Captura%20de%20pantalla%202017-07-11%20a%20las%2017.51.18.png"
})
print(mongo.getRespuesta("definición modelo cascada"))
'''
