from pymongo import MongoClient


class Mongo:
    def __init__(self):
        self.cliente = MongoClient('localhost', port=27017)  # Para el caso de ser Local
        # Seleccionamos o creamos la base de Datos
        self.dbname = self.cliente['chatbot']

    def gettexto(self):
        respuesta = []
        # Seleccionamos o creamos la colección (Tabla)
        colection = self.dbname['textos']
        # Consultamos todos los textos y lo guardamos en un arreglo
        for frase in colection.find({}):
            respuesta.append(frase['frase'])
        return respuesta


    #{frase: 'frase', urlimage: 'http://'}
    def inserttexto(self, documento):
        # Seleccionamos o creamos la colección (Tabla)
        colection = self.dbname['textos']
        colection.insert_one(documento)

    def getimagen(self,frase):
        # Seleccionamos o creamos la colección (Tabla)
        colection = self.dbname['textos']
        respuesta = colection.find_one({'frase':frase}) #consultamos la frase exacta
        #Revisamos si existe la key caso contrario, devolvemos vacío
        try:
            return respuesta['urlimage']
        except KeyError:
            return ''


'''mongo = Mongo()
mongo.inserttexto({
    'frase': "El modelo en cascada es un proceso de desarrollo secuencial, en el que el desarrollo de software se concibe como  un conjunto de etapas que  se ejecutan una tras otra. Se le denomina así por las posiciones que ocupan las diferentes fases que componen el proyecto, colocadas una encima de otra, y siguiendo un flujo de ejecución de arriba hacia abajo, como una cascada.",
    'urlimage': "https://user.oc-static.com/upload/2017/07/11/14997883020913_Captura%20de%20pantalla%202017-07-11%20a%20las%2017.51.18.png"
})
print(mongo.getimagen("El modelo en cascada es un proceso de desarrollo secuencial, en el que el desarrollo de software se concibe como  un conjunto de etapas que  se ejecutan una tras otra. Se le denomina así por las posiciones que ocupan las diferentes fases que componen el proyecto, colocadas una encima de otra, y siguiendo un flujo de ejecución de arriba hacia abajo, como una cascada."))
'''