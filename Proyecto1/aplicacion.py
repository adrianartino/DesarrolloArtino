from flask import Flask, render_template, request, redirect, url_for, session

from sqlalchemy import create_engine   #crear instancia para base de datos
from sqlalchemy.orm import scoped_session, sessionmaker

import os


app = Flask(__name__)

engine = create_engine("postgres://saciatig:qdSgbJnUJhokzzt7IQhMZSEBD41EfRGS@otto.db.elephantsql.com:5432/saciatig") #se conecta a la base de datos
basededatos = scoped_session(sessionmaker(bind=engine))

#index normal
@app.route("/")
def index():
    return render_template("index.html")

#cuando se le da clic al boton para validar usuario y contraseña
@app.route("/validar", methods=["POST"])
def validar():
    nombrerecibido = request.form.get("nombreusuario")
    contrarecibida = request.form.get("contrausuario")

    usuarioencontrado = basededatos.execute("SELECT usuario FROM usuarios WHERE usuario=:username",{"username":nombrerecibido}).fetchone()
    contraseñaencontrada = basededatos.execute("SELECT 	contraseñausuario FROM usuarios WHERE usuario=:username",{"username":nombrerecibido}).fetchone()

    if usuarioencontrado is None:
        return f"No se encontro el usuario"+nombrerecibido
    else:
        for passwor_data in contraseñaencontrada:
            if contrarecibida == passwor_data:  #si son iguales...
                return f"Bienvenido!"
                #return redirect(url_for('hello')) #to be edited from here do redict to either svm or home
            else:
                return f"La contraseña es incorrecta"
				#return render_template('login.html')

    basededatos.commit()
    #return f"Usuarios : {numerodeusuarios} ! Contraseña : {contrarecibida} !"

#registro
@app.route("/registro")
def registro():
    return render_template("registro.html")

#validar registro
@app.route("/validarregistro", methods=["POST"])
def validarregistro():
    usuarioregistrar = request.form.get("usuarioregistro")
    contraregistrar = request.form.get("contraregistro")
    contra2registrar = request.form.get("contra2registro")

    nombreregistrar = request.form.get("nombreusuarioregistro")
    apellidoregistrar = request.form.get("apellidoregistro")
    correoregistrar = request.form.get("correoregistro")
    #return f"UsuarioNuevo : {usuarioregistrar}!\nContraseña : {contraregistrar}!\nContraseñax2 : {contra2registrar}!\nNombre usuario : {nombreregistrar}!\nApellido usuario: {apellidoregistrar}!\nCorreo usuario : {correoregistrar}!"

    textoerror = ""
    registroexitoso = False

    #si todos los campos estan vacios..
    if usuarioregistrar == "" and contraregistrar == "" and contra2registrar == "" and nombreregistrar == "" and apellidoregistrar == "" and correoregistrar == "":
        error = True
        textoerror=" Te faltan rellenar todos los campos!"
        registroexitoso = False

    #si no..

    #si falta de llenar algun campo
    elif usuarioregistrar == "" or contraregistrar == "" or contra2registrar == "" or nombreregistrar == "" or apellidoregistrar == "" or correoregistrar == "":
        error = True
        textoerror=" Debes llenar el formulario completo!"
        registroexitoso = False

    #si estan todos los campos llenos..
    elif "@" not in correoregistrar and contraregistrar != contra2registrar: # si se ingresa bien el correo..
        error = True
        textoerror += " Ingrese bien el correo y verifique las contraseñas! "
        registroexitoso = False

    #si las contraseñas no coinciden
    elif contraregistrar != contra2registrar:
        error = True
        textoerror += " Las contraseñas no coinciden!"
        registroexitoso = False

    elif "@" not in correoregistrar: # si se ingresa bien el correo..
        error = True
        textoerror += " Ingrese bien el correo!"
        registroexitoso = False

    else:
        registroexitoso = True
        error = False
        #meter datos a base de datos ya que no hay errores

        #se necesita comprobar si existe o no ese nombre de usuario..
        basededatos.execute("INSERT INTO usuarios (usuario, nombreusuario, apellidousuario, contraseñausuario, correousuario) VALUES (:usuario, :nombreusuario, :apellidousuario, :contraseñausuario, :correousuario)",{"usuario": usuarioregistrar, "nombreusuario": nombreregistrar, "apellidousuario": apellidoregistrar, "contraseñausuario": contraregistrar, "correousuario": correoregistrar})
    basededatos.commit()





    return render_template("registro.html", error=error , textoerror=textoerror, registroexitoso=registroexitoso)
