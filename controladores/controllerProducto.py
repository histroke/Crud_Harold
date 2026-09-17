from app import app, productos
from flask import Flask, request, render_template, redirect
import pymongo
from werkzeug.utils import secure_filename
import os
from bson.objectid import ObjectId

# 1. Ruta principal: Listar productos
@app.route("/")
def inicio():
    listaProductos = productos.find()
    return render_template("listarProductos.html", listaProductos=listaProductos)

# 2. Ruta para mostrar el formulario de agregar
@app.route("/frmAgregarProducto")
def vistaAgregar():
    return render_template("frmAgregarProducto.html")

# Función auxiliar para validar código existente
def consultarProductoPorCodigo(codigo):
    try:
        consulta = {"codigo": codigo}
        producto = productos.find_one(consulta)
        return producto is not None
    except pymongo.errors as error:
        print(error)
        return False

# 3. Ruta para procesar el guardado de un nuevo producto
@app.route("/agregarProducto", methods=["POST"])
def agregarProducto():
    producto = {}
    try:
        mensaje = ""
        codigo = int(request.form["txtCodigo"])
        nombre = request.form["txtNombre"]
        precio = int(request.form["txtPrecio"])
        categoria = request.form["cbCategoria"]

        producto = {
            "codigo": codigo,
            "nombre": nombre,
            "precio": precio,
            "categoria": categoria
        }

        archivo = request.files["fileFoto"]
        if archivo and archivo.filename != "":
            nombreArchivo = secure_filename(archivo.filename)
            extension = nombreArchivo.rsplit(".", 1)[-1].lower() if "." in nombreArchivo else "jpg"
        else:
            extension = "jpg"

        existe = consultarProductoPorCodigo(codigo)
        if existe:
            mensaje = "Ya existe un producto con ese código"
            return render_template("frmAgregarProducto.html", producto=producto, mensaje=mensaje)
        else:
            resultado = productos.insert_one(producto)
            if resultado.acknowledged:
                idProducto = resultado.inserted_id
                nuevoNombre = str(idProducto) + "." + str(extension)
                archivo.save(os.path.join(app.config["UPLOAD_FOLDER"], nuevoNombre))
                return redirect("/")
    except Exception as error:
        mensaje = str(error)
        return render_template("frmAgregarProducto.html", producto=producto, mensaje=mensaje)

# 4. Ruta para consultar un producto por su ID
@app.route("/consultar/<string:idProducto>", methods=["GET"])
def consultarPorId(idProducto):
    try:
        idObj = ObjectId(idProducto)
        consulta = {"_id": idObj}
        producto = productos.find_one(consulta)
        return render_template("frmEditarProducto.html", producto=producto)
    except pymongo.errors as error:
        mensaje = error
        listaProductos = productos.find()
        return render_template("listarProductos.html", mensaje=mensaje, listaProductos=listaProductos)

# 5. Ruta para actualizar el producto
@app.route("/actualizar", methods=["POST"])
def actualizarProducto():
    try:
        codigo = int(request.form["txtCodigo"])
        nombre = request.form["txtNombre"]
        precio = int(request.form["txtPrecio"])
        categoria = request.form["cbCategoria"]
        idProducto = ObjectId(request.form["idProducto"])

        criterio = {"_id": idProducto}
        datosActualizar = {
            "$set": {
                "codigo": codigo,
                "nombre": nombre,
                "precio": precio,
                "categoria": categoria
            }
        }
        resultado = productos.update_one(criterio, datosActualizar)

        if resultado.acknowledged:
            archivo = request.files["fileFoto"]
            if archivo and archivo.filename != "":
                nombreArchivo = secure_filename(archivo.filename)
                extension = nombreArchivo.rsplit(".", 1)[-1].lower() if "." in nombreArchivo else "jpg"
                nombreArchivoActualizar = str(idProducto) + "." + str(extension)
                archivo.save(os.path.join(app.config["UPLOAD_FOLDER"], nombreArchivoActualizar))
            return redirect("/")
    except Exception as error:
        print(error)
        return redirect("/")

# 6. Ruta para eliminar
@app.route("/eliminar/<string:idProducto>", methods=["GET"])
def eliminarProducto(idProducto):
    try:
        idObj = ObjectId(idProducto)
        consulta = {"_id": idObj}
        productos.delete_one(consulta)
        return redirect("/")
    except Exception as error:
        print(error)
        return redirect("/")

