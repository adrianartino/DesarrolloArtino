from flask import Flask, render_template, request

app = Flask(__name__)

#index normal
@app.route("/")
def index():
    return render_template("index.html")

#cuando se le da clic al boton para validar usuario y contraseña
@app.route("/validar", methods=["POST"])
def validar():
    nombrerecibido = request.form.get("nombreusuario")
    contrarecibida = request.form.get("contrausuario")
    return f"Usuario : {nombrerecibido} ! Contraseña : {contrarecibida} !"

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





    return render_template("registro.html", error=error , textoerror=textoerror, registroexitoso=registroexitoso)
