from flask import Flask, render_template, request, redirect, url_for, session

from sqlalchemy import create_engine   #crear instancia para base de datos
from sqlalchemy.orm import scoped_session, sessionmaker

import os


app = Flask(__name__)
app.secret_key = "1234"



engine = create_engine("postgres://saciatig:qdSgbJnUJhokzzt7IQhMZSEBD41EfRGS@otto.db.elephantsql.com:5432/saciatig") #se conecta a la base de datos
basededatos = scoped_session(sessionmaker(bind=engine))

#index normal
@app.route("/")
def index():
    if "user" in session:
        return redirect(url_for("home"))
    else:
        return render_template("index.html")

#cuando se le da clic al boton para validar usuario y contraseña
@app.route("/validar", methods=["POST", "GET"])
def validar():
    #Checa a ver si se mando algo...
    if request.method == "POST":
        nombrerecibido = request.form.get("nombreusuario")
        contrarecibida = request.form.get("contrausuario")

        usuarioencontrado = basededatos.execute("SELECT usuario FROM usuarios WHERE usuario=:username",{"username":nombrerecibido}).fetchone()
        contraseñaencontrada = basededatos.execute("SELECT 	contraseñausuario FROM usuarios WHERE usuario=:username",{"username":nombrerecibido}).fetchone()

        nombrereal = basededatos.execute("SELECT nombreusuario FROM usuarios WHERE usuario=:username",{"username":nombrerecibido}).fetchone()
        apellidoreal = basededatos.execute("SELECT apellidousuario FROM usuarios WHERE usuario=:username",{"username":nombrerecibido}).fetchone()
        idusuario = basededatos.execute("SELECT id FROM usuarios WHERE usuario=:username",{"username":nombrerecibido}).fetchone()

        if usuarioencontrado is None:
            return f"No se encontro el usuario "+nombrerecibido
            #falta splash de error
        else:

            for passwor_data in contraseñaencontrada:
                if contrarecibida == passwor_data:  #si son iguales...

                    session["user"] = nombrerecibido#se guarda la variable session.
                    return redirect(url_for('home')) #redirecciona a home si funciona..
                else:
                    return f"La contraseña es incorrecta"
    				#return render_template('login.html')
                    #falta splash de error

        basededatos.commit()
        #return f"Usuarios : {numerodeusuarios} ! Contraseña : {contrarecibida} !"

    #si no se mando nada...
    else:
        #si hay una sesion iniciada... que lo mande a home.
        if "user" in session:
            return redirect(url_for("home"))

        return render_template("index.html")

#Menu ya logueado
@app.route("/home")
def home():
    if "user" in session:
        usuario = session["user"]
        nombreusuario = basededatos.execute("SELECT nombreusuario FROM usuarios WHERE usuario=:username",{"username":usuario}).fetchone()
        apellidousuario = basededatos.execute("SELECT apellidousuario FROM usuarios WHERE usuario=:username",{"username":usuario}).fetchone()

        for row in nombreusuario:
            nusuario = nombreusuario[0]

        for row in apellidousuario:
            ausuario = apellidousuario[0]

        usuariomostrar = nusuario + " " + ausuario
        #nusuario = nombreusuario
        #ausuario = apellidousuario

        return render_template("sesionbusqueda.html",usuariomostrar=usuariomostrar)
    else:
        return redirect(url_for("validar"))

#Menu ya logueado
@app.route("/logout")
def logout():
    session.pop("user", None)
    #return render_template("index.html")
    return redirect(url_for("index"))


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

    usuarioencontrado = basededatos.execute("SELECT usuario FROM usuarios WHERE usuario=:username",{"username":usuarioregistrar}).fetchone()

    #si se encuentra un usuario con ese nombre...
    if usuarioencontrado is not None:
        error = True
        error1 = True
        textoerror=" Ya hay alguien registrado con ese nombre de usuario!"
        registroexitoso = False

    #si todos los campos estan vacios..
    elif usuarioregistrar == "" and contraregistrar == "" and contra2registrar == "" and nombreregistrar == "" and apellidoregistrar == "" and correoregistrar == "":
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





    return render_template("registro.html", error=error , textoerror=textoerror, usuarioregistrar=usuarioregistrar, nombreregistrar=nombreregistrar, apellidoregistrar=apellidoregistrar, correoregistrar=correoregistrar)
