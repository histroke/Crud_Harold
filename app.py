from flask import Flask
import pymongo

# 1. Crear el objeto Flask primero
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "./static/imagenes"

# 2. Crear la conexión a MongoDB Atlas
miConexion = pymongo.MongoClient("mongodb+srv://haroldmauricio833_db_user:1234@histroke.fugedv2.mongodb.net/?appName=histroke")
baseDatos = miConexion["GESTIONPRODUCTOS"]
productos = baseDatos["PRODUCTOS"]

# 3. IMPORTANTE: Importar el controlador DESPUÉS de crear 'app' y 'productos'
from controladores.controllerProducto import *

if __name__ == "__main__":
    app.run(port=3000, debug=True)