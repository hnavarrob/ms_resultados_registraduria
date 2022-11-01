from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS
import json
from waitress import serve
#Importaciones para la DB, conexión y pruebas
import pymongo
import certifi
ca = certifi.where()
client = pymongo.MongoClient("mongodb+srv://usuarioPruebas:RegistraduriaProject@cluster0.bz6sxhf.mongodb.net/?retryWrites=true&w=majority")
db = client.test
print(db)
baseDatos = client["db-resultados-registraduria"]
print(baseDatos.list_collection_names())

app=Flask(__name__)
cors = CORS(app)

#Impo


#Métodos de Partido con su respectivo endpoint
from Controladores.ControladorPartido import ControladorPartido
miControladorPartido=ControladorPartido()

@app.route("/partido",methods=['GET'])
def getPartidos():
    json=miControladorPartido.index()
    return jsonify(json)

@app.route("/partido",methods=['POST'])
def crearPartido():
    data = request.get_json()
    json=miControladorPartido.create(data)
    return jsonify(json)

@app.route("/partido/<string:id>",methods=['GET'])
def getPartido(id):
    json=miControladorPartido.show(id)
    return jsonify(json)

@app.route("/partido/<string:id>",methods=['PUT'])
def modificarPatido(id):
    data = request.get_json()
    json=miControladorPartido.update(id,data)
    return jsonify(json)

@app.route("/partido/<string:id>",methods=['DELETE'])
def eliminarPartido(id):
    json=miControladorPartido.delete(id)
    return jsonify(json)

#Métodos de Candidato con su respectivo endpoint
from Controladores.ControladorCandidato import ControladorCandidato
miControladorCandidato=ControladorCandidato()

@app.route("/candidato/",methods=['POST'])
def crearCandidato():
    data = request.get_json()
    json=miControladorCandidato.create(data)
    return jsonify(json)

#Métodos de Mesa con su respectivo endpoint
from Controladores.ControladorMesa import ControladorMesa
miControladorMesa=ControladorMesa()

@app.route("/mesa/",methods=['POST'])
def crearMesa():
    data = request.get_json()
    json=miControladorMesa.create(data)
    return jsonify(json)

#Método y endpoint para Candidato - Partido
from Controladores.ControladorCandidato import ControladorCandidato#Falta en la Guía
miControladorCandidato=ControladorCandidato() #Falta en la Guía
@app.route("/candidato/<string:id>/partido/<string:id_partido>",methods=['PUT'])
def asignarPartidoACandidato(id,id_partido):
    json=miControladorCandidato.asignarPartido(id,id_partido)
    return jsonify(json)

#Método y endpoint para Resultados
from Controladores.ControladorResultado import ControladorResultado
miControladorResultado=ControladorResultado()
@app.route("/resultado/",methods=['GET'])
def getResultados():
    json=miControladorResultado.index()
    return jsonify(json)

@app.route("/resultado/<string:id>",methods=['GET'])
def getResultado(id):
    json=miControladorResultado.show(id)
    return jsonify(json)

@app.route("/resultado/mesa/<string:id_candidato>/candidato/<string:id_mesa>",methods=['POST'])
def crearResultado(id_mesa,id_candidato):
    data = request.get_json()
    json=miControladorResultado.create(data,id_mesa,id_candidato)
    return jsonify(json)

@app.route("/resultado/<string:id_resultado>/candidato/<string:id_candidato>/mesa/<string:id_mesa>",methods=['PUT'])
def modificarResultado(id_resultado,id_candidato,id_mesa):
    data = request.get_json()
    json=miControladorResultado.update(id_resultado,data,id_candidato,id_mesa)
    return jsonify(json)

@app.route("/resultado/<string:id_resultado>",methods=['DELETE'])
def eliminarResultado(id_resultado):
    json=miControladorResultado.delete(id_resultado)
    return jsonify(json)


#Test endpoint
@app.route("/",methods=['GET'])
def test():
    json = {}
    json["message"]="Server running ..."
    return jsonify(json)

def loadFileConfig():
    with open('config.json') as f:
        data = json.load(f)
    return data

if __name__=='__main__':
    dataConfig = loadFileConfig()
    print("Server running : "+"http://"+dataConfig["url-backend"]+":" + str(dataConfig["port"]))
    serve(app,host=dataConfig["url-backend"],port=dataConfig["port"])