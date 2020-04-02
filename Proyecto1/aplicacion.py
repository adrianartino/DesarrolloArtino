from flask import Flask, render_template, request, redirect, url_for, session

from sqlalchemy import create_engine   #crear instancia para base de datos
from sqlalchemy.orm import scoped_session, sessionmaker

import os


app = Flask(__name__)
app.jinja_env.filters['zip'] = zip

app.secret_key = "1234"



engine = create_engine("postgres://pmhinabc:6n39qayiNGhTpt7bfayK06Ljk8AeB8FB@otto.db.elephantsql.com:5432/pmhinabc") #se conecta a la base de datos
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

        textoerror = ""

        nombrerecibido = request.form.get("nombreusuario")
        contrarecibida = request.form.get("contrausuario")

        usuarioencontrado = basededatos.execute("SELECT usuario FROM usuarios WHERE usuario=:username",{"username":nombrerecibido}).fetchone()
        contraseñaencontrada = basededatos.execute("SELECT 	contraseñausuario FROM usuarios WHERE usuario=:username",{"username":nombrerecibido}).fetchone()

        if nombrerecibido == "" or contrarecibida == "":
            error = True
            textoerror += "Te ha faltado ingresar datos!"
            return render_template("index.html", error=error, textoerror=textoerror)

        elif usuarioencontrado is None:
            error = True
            textoerror += "No se ha encontrado un usuario con ese nombre!"
            return render_template("index.html", error=error, textoerror=textoerror)
        else:

            for passwor_data in contraseñaencontrada:
                if contrarecibida == passwor_data:  #si son iguales...
                    error = False
                    session["user"] = nombrerecibido#se guarda la variable session.
                    return redirect(url_for('home')) #redirecciona a home si funciona..
                else:
                    error = True
                    textoerror += "La contraseña es incorrecta!"
                    return render_template("index.html", error=error, textoerror=textoerror)

        basededatos.commit()

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
        if "busqueda" in session:
            session.pop("busqueda", None)
        if "isbn" in session:
            session.pop("isbn", None)
        nombreusuario = basededatos.execute("SELECT nombreusuario FROM usuarios WHERE usuario=:username",{"username":usuario}).fetchone()
        apellidousuario = basededatos.execute("SELECT apellidousuario FROM usuarios WHERE usuario=:username",{"username":usuario}).fetchone()

        for row in nombreusuario:
            nusuario = nombreusuario[0]

        for row in apellidousuario:
            ausuario = apellidousuario[0]

        usuariomostrar = nusuario + " " + ausuario
        basededatos.commit()
        return render_template("sesionbusqueda.html",usuariomostrar=usuariomostrar)
    else:
        return redirect(url_for("validar"))

#Menu ya logueado
@app.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("busqueda", None)
    session.pop("isbn", None)
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




@app.route("/buscar", methods=["POST", "GET"])
def buscar():
    if "user" in session:
        usuario = session["user"]
        nombreusuario = basededatos.execute("SELECT nombreusuario FROM usuarios WHERE usuario=:username",{"username":usuario}).fetchone()
        apellidousuario = basededatos.execute("SELECT apellidousuario FROM usuarios WHERE usuario=:username",{"username":usuario}).fetchone()

        for row in nombreusuario:
            nusuario = nombreusuario[0]

        for row in apellidousuario:
            ausuario = apellidousuario[0]

        usuariomostrar = nusuario + " " + ausuario



        #si se recarga y ya se habia cargado un libro
        if "busqueda" in session:
            #ver si se mando algo...
            if request.method == "POST":
                busquedarecibida = request.form.get("busqueda")

                if busquedarecibida == "":
                    textoerror = "No has buscado nada!"
                    errorbusqueda = True
                    return render_template("sesionbusqueda.html", busquedarecibida = busquedarecibida, usuariomostrar=usuariomostrar, textoerror=textoerror, errorbusqueda=errorbusqueda)

                else:
                    errorbusqueda = False
                    textoerror = "Busqueda realizada!"
                    session["busqueda"] = busquedarecibida
                    busquedasesion = session["busqueda"]
                    busqueda = True
                    #consulta para buscar cualquier resultado entre los campos que coincida con la busqueda
                    busquedaencontrada = basededatos.execute("SELECT isbn, titulo, autor, año FROM libros WHERE (LOWER(isbn) LIKE LOWER(:bus)) OR (LOWER(titulo) LIKE LOWER(:bus)) OR (LOWER(autor) LIKE LOWER(:bus)) LIMIT 10", { "bus": '%' + busquedasesion + '%'} )
                    filas = busquedaencontrada.fetchall()
                    basededatos.commit()
                    return render_template("sesionbusqueda.html", busquedarecibida = busquedarecibida, busqueda = busqueda, filas=filas, textoerror=textoerror, usuariomostrar=usuariomostrar, errorbusqueda=errorbusqueda)

            #si se recarga la página...
            else:
                busquedasesion = session["busqueda"]
                textoerror = ""
                busqueda = True
                #consulta para buscar cualquier resultado entre los campos que coincida con la busqueda
                busquedaencontrada = basededatos.execute("SELECT isbn, titulo, autor, año FROM libros WHERE (LOWER(isbn) LIKE LOWER(:bus)) OR (LOWER(titulo) LIKE LOWER(:bus)) OR (LOWER(autor) LIKE LOWER(:bus)) LIMIT 10", { "bus": '%' + busquedasesion + '%'} )
                filas = busquedaencontrada.fetchall()
                basededatos.commit()
                return render_template("sesionbusqueda.html", busqueda = busqueda, filas=filas, textoerror=textoerror, usuariomostrar=usuariomostrar)

        #si todabia no se busco un libro
        else:
            busquedarecibida = request.form.get("busqueda")

            if busquedarecibida == "":
                textoerror = "No has buscado nada!"
                errorbusqueda = True
                return render_template("sesionbusqueda.html", busquedarecibida = busquedarecibida, usuariomostrar=usuariomostrar, textoerror=textoerror, errorbusqueda=errorbusqueda)
            else:
                errorbusqueda = False
                textoerror = "Busqueda realizada!"
                session["busqueda"] = busquedarecibida
                busqueda = True
                #consulta para buscar cualquier resultado entre los campos que coincida con la busqueda
                busquedaencontrada = basededatos.execute("SELECT isbn, titulo, autor, año FROM libros WHERE (LOWER(isbn) LIKE LOWER(:bus)) OR (LOWER(titulo) LIKE LOWER(:bus)) OR (LOWER(autor) LIKE LOWER(:bus)) LIMIT 10", { "bus": '%' + busquedarecibida + '%'} )
                filas = busquedaencontrada.fetchall()

                basededatos.commit()
                return render_template("sesionbusqueda.html", busquedarecibida = busquedarecibida, busqueda = busqueda, filas=filas, usuariomostrar=usuariomostrar, textoerror=textoerror, errorbusqueda=errorbusqueda)


@app.route("/mostrarlibro", methods=["POST", "GET"])
def mostrarlibro():


    if "user" in session:
        usuario = session["user"]
        nombreusuario = basededatos.execute("SELECT nombreusuario FROM usuarios WHERE usuario=:username",{"username":usuario}).fetchone()
        apellidousuario = basededatos.execute("SELECT apellidousuario FROM usuarios WHERE usuario=:username",{"username":usuario}).fetchone()

        for row in nombreusuario:
            nusuario = nombreusuario[0]

        for row in apellidousuario:
            ausuario = apellidousuario[0]

        usuariomostrar = nusuario + " " + ausuario

        #si ya se ha dado información de un libro
        if "isbn" in session:
            #si se quiere visualizar la información de un nuevo libro...
            if request.method == "POST":
                isbnrecibido = request.form.get("isbn")
                session["isbn"] = isbnrecibido
                isbnsesion = session["isbn"]

                datoslibro = basededatos.execute("SELECT isbn, titulo, autor, año  FROM libros WHERE isbn=:isbnrecibido",{"isbnrecibido":isbnsesion}).fetchall()

                for dato in datoslibro:
                    isbn = dato[0]
                    titulo  = dato[1]
                    autor = dato[2]
                    año = dato[3]



                #RESEÑAS-----------------------------------------
                isbnreseña = session["isbn"]
                numeroregistrosconsulta = basededatos.execute("SELECT count(*) FROM reseñas WHERE libreo_isbn=:isbnreseña",{"isbnreseña":isbnreseña}).fetchall()

                for dato in numeroregistrosconsulta:
                    numeroregistrosfor = dato[0]

                numeroregistros = str(numeroregistrosfor)
                siescero = "0"
                textoreseña =""

                if numeroregistros == siescero:
                    hayreseña = False
                    return render_template("infolibro.html",usuariomostrar=usuariomostrar, isbn=isbn, titulo=titulo, autor=autor, año=año, hayreseña=hayreseña)

                #si hay registros.. FUNCIONA!
                else:
                    hayreseña = True

                    #se obtienen resultados de la columna calificaciones.
                    calificaciones = basededatos.execute("SELECT sum(calificacion) FROM reseñas WHERE libreo_isbn=:isbnmostrado",{"isbnmostrado":isbnreseña})
                    filascalificaciones = calificaciones.fetchall()


                    for calif in filascalificaciones:
                        totalcaliffor = calif[0]

                    #resultado de la suma de todas las calificaciones de ese libro.
                    suma = str(totalcaliffor)

                    #promedio de calificaciones
                    promedioennumero = int(suma)/float(int(numeroregistros))
                    promedioredondeado = round(promedioennumero)
                    #se manda al template
                    promedio = str(promedioredondeado)

                #PROMEDIO DE ESTRELLITAS!.--------------------------------------------------
                    promedioestrellas = float((1/int(numeroregistros))*100) #50%

                    calif1 = basededatos.execute("SELECT calificacion FROM reseñas WHERE libreo_isbn=:isbnmostrado AND calificacion = '1'",{"isbnmostrado":isbnreseña})
                    calificacion1 = calif1.fetchall()

                    prom1 = float(0)

                    if calificacion1 is None:
                        prom1 = float(0)
                    else:
                        for c1 in calificacion1:
                            prom1 += float(promedioestrellas)
                    prom1redondeado = round(prom1)

                    calif2 = basededatos.execute("SELECT calificacion FROM reseñas WHERE libreo_isbn=:isbnmostrado AND calificacion = '2'",{"isbnmostrado":isbnreseña})
                    calificacion2 = calif2.fetchall()

                    prom2 = float(0)

                    if calificacion2 is None:
                        prom2 = float(0)
                    else:
                        for c2 in calificacion2:
                            prom2 += float(promedioestrellas)
                    prom2redondeado = round(prom2)

                    calif3 = basededatos.execute("SELECT calificacion FROM reseñas WHERE libreo_isbn=:isbnmostrado AND calificacion = '3'",{"isbnmostrado":isbnreseña})
                    calificacion3 = calif3.fetchall()

                    prom3 = float(0)

                    if calificacion3 is None:
                        prom3 = float(0)
                    else:
                        for c3 in calificacion3:
                            prom3 += float(promedioestrellas)
                    prom3redondeado = round(prom3)

                    calif4 = basededatos.execute("SELECT calificacion FROM reseñas WHERE libreo_isbn=:isbnmostrado AND calificacion = '4'",{"isbnmostrado":isbnreseña})
                    calificacion4 = calif4.fetchall()

                    prom4 = float(0)

                    if calificacion4 is None:
                        prom4 = float(0)
                    else:
                        for c4 in calificacion4:
                            prom4 += float(promedioestrellas)
                    prom4redondeado = round(prom4)

                    calif5 = basededatos.execute("SELECT calificacion FROM reseñas WHERE libreo_isbn=:isbnmostrado AND calificacion = '5'",{"isbnmostrado":isbnreseña})
                    calificacion5 = calif5.fetchall()

                    prom5 = float(0)

                    if calificacion5 is None:
                        prom5 = float(0)
                    else:
                        for c5 in calificacion5:
                            prom5 += float(promedioestrellas)
                    prom5redondeado = round(prom5)

                    #se obtienen todas las reseñas
                    reseña = basededatos.execute("SELECT idReseña, usuario_id, libreo_isbn, textoReseña, calificacion FROM reseñas WHERE libreo_isbn=:isbnmostrado",{"isbnmostrado":isbnreseña})
                    filasreseña = reseña.fetchall()

                    nombres = basededatos.execute("SELECT nombreusuario, apellidousuario FROM usuarios A, reseñas B WHERE B.usuario_id = A.id")
                    filasnombres = nombres.fetchall()


                    basededatos.commit()
                    return render_template("infolibro.html",usuariomostrar=usuariomostrar, isbn=isbn, titulo=titulo, autor=autor, año=año, hayreseña=hayreseña, promedio=promedio , filasreseña=filasreseña, numeroregistros=numeroregistros)


            #se recarga la página
            else:
                isbnsesion = session["isbn"]

                datoslibro = basededatos.execute("SELECT isbn, titulo, autor, año  FROM libros WHERE isbn=:isbnrecibido",{"isbnrecibido":isbnsesion}).fetchall()

                for dato in datoslibro:
                    isbn = dato[0]
                    titulo  = dato[1]
                    autor = dato[2]
                    año = dato[3]



                #RESEÑAS-----------------------------------------
                isbnreseña = session["isbn"]
                numeroregistrosconsulta = basededatos.execute("SELECT count(*) FROM reseñas WHERE libreo_isbn=:isbnreseña",{"isbnreseña":isbnreseña}).fetchall()

                for dato in numeroregistrosconsulta:
                    numeroregistrosfor = dato[0]

                numeroregistros = str(numeroregistrosfor)
                siescero = "0"
                textoreseña =""

                if numeroregistros == siescero:
                    hayreseña = False
                    return render_template("infolibro.html",usuariomostrar=usuariomostrar, isbn=isbn, titulo=titulo, autor=autor, año=año, hayreseña=hayreseña)

                #si hay registros.. FUNCIONA!
                else:
                    hayreseña = True

                    #se obtienen resultados de la columna calificaciones.
                    calificaciones = basededatos.execute("SELECT sum(calificacion) FROM reseñas WHERE libreo_isbn=:isbnmostrado",{"isbnmostrado":isbnreseña})
                    filascalificaciones = calificaciones.fetchall()


                    for calif in filascalificaciones:
                        totalcaliffor = calif[0]

                    #resultado de la suma de todas las calificaciones de ese libro.
                    suma = str(totalcaliffor)

                    #promedio de calificaciones
                    promedioennumero = int(suma)/float(int(numeroregistros))
                    promedioredondeado = round(promedioennumero)
                    #se manda al template
                    promedio = str(promedioredondeado)

                #PROMEDIO DE ESTRELLITAS!.--------------------------------------------------
                    promedioestrellas = float((1/int(numeroregistros))*100) #50%

                    calif1 = basededatos.execute("SELECT calificacion FROM reseñas WHERE libreo_isbn=:isbnmostrado AND calificacion = '1'",{"isbnmostrado":isbnreseña})
                    calificacion1 = calif1.fetchall()

                    prom1 = float(0)

                    if calificacion1 is None:
                        prom1 = float(0)
                    else:
                        for c1 in calificacion1:
                            prom1 += float(promedioestrellas)
                    prom1redondeado = round(prom1)

                    calif2 = basededatos.execute("SELECT calificacion FROM reseñas WHERE libreo_isbn=:isbnmostrado AND calificacion = '2'",{"isbnmostrado":isbnreseña})
                    calificacion2 = calif2.fetchall()

                    prom2 = float(0)

                    if calificacion2 is None:
                        prom2 = float(0)
                    else:
                        for c2 in calificacion2:
                            prom2 += float(promedioestrellas)
                    prom2redondeado = round(prom2)

                    calif3 = basededatos.execute("SELECT calificacion FROM reseñas WHERE libreo_isbn=:isbnmostrado AND calificacion = '3'",{"isbnmostrado":isbnreseña})
                    calificacion3 = calif3.fetchall()

                    prom3 = float(0)

                    if calificacion3 is None:
                        prom3 = float(0)
                    else:
                        for c3 in calificacion3:
                            prom3 += float(promedioestrellas)
                    prom3redondeado = round(prom3)

                    calif4 = basededatos.execute("SELECT calificacion FROM reseñas WHERE libreo_isbn=:isbnmostrado AND calificacion = '4'",{"isbnmostrado":isbnreseña})
                    calificacion4 = calif4.fetchall()

                    prom4 = float(0)

                    if calificacion4 is None:
                        prom4 = float(0)
                    else:
                        for c4 in calificacion4:
                            prom4 += float(promedioestrellas)
                    prom4redondeado = round(prom4)

                    calif5 = basededatos.execute("SELECT calificacion FROM reseñas WHERE libreo_isbn=:isbnmostrado AND calificacion = '5'",{"isbnmostrado":isbnreseña})
                    calificacion5 = calif5.fetchall()

                    prom5 = float(0)

                    if calificacion5 is None:
                        prom5 = float(0)
                    else:
                        for c5 in calificacion5:
                            prom5 += float(promedioestrellas)
                    prom5redondeado = round(prom5)

                    #se obtienen todas las reseñas
                    reseña = basededatos.execute("SELECT idReseña, usuario_id, libreo_isbn, textoReseña, calificacion FROM reseñas WHERE libreo_isbn=:isbnmostrado",{"isbnmostrado":isbnreseña})
                    filasreseña = reseña.fetchall()

                    nombres = basededatos.execute("SELECT nombreusuario, apellidousuario FROM usuarios A, reseñas B WHERE B.usuario_id = A.id")
                    filasnombres = nombres.fetchall()

                    basededatos.commit()
                    return render_template("infolibro.html",usuariomostrar=usuariomostrar, isbn=isbn, titulo=titulo, autor=autor, año=año, hayreseña=hayreseña, promedio=promedio , filasreseña=filasreseña , numeroregistros=numeroregistros, prom1=prom1, prom2=prom2, prom3=prom3, prom4=prom4, prom5=prom5, prom1redondeado=prom1redondeado , prom2redondeado=prom2redondeado, prom3redondeado=prom3redondeado, prom4redondeado=prom4redondeado, prom5redondeado=prom5redondeado, filasnombres=filasnombres)




        #se solicita información de un libro..
        else:
            isbnrecibido = request.form.get("isbn")
            session["isbn"] = isbnrecibido

            datoslibro = basededatos.execute("SELECT isbn, titulo, autor, año  FROM libros WHERE isbn=:isbnrecibido",{"isbnrecibido":isbnrecibido}).fetchall()

            for dato in datoslibro:
                isbn = dato[0]
                titulo  = dato[1]
                autor = dato[2]
                año = dato[3]

            session["isbn"] = isbn

            #RESEÑAS-----------------------------------------
            isbnreseña = session["isbn"]
            numeroregistrosconsulta = basededatos.execute("SELECT count(*) FROM reseñas WHERE libreo_isbn=:isbnreseña",{"isbnreseña":isbnreseña}).fetchall()

            for dato in numeroregistrosconsulta:
                numeroregistrosfor = dato[0]

            numeroregistros = str(numeroregistrosfor)
            siescero = "0"
            textoreseña =""

            if numeroregistros == siescero:
                hayreseña = False
                return render_template("infolibro.html",usuariomostrar=usuariomostrar, isbn=isbn, titulo=titulo, autor=autor, año=año, hayreseña=hayreseña, numeroregistros=numeroregistros)

            #si hay registros.. FUNCIONA!
            else:
                hayreseña = True

                #se obtienen resultados de la columna calificaciones.
                calificaciones = basededatos.execute("SELECT sum(calificacion) FROM reseñas WHERE libreo_isbn=:isbnmostrado",{"isbnmostrado":isbnreseña})
                filascalificaciones = calificaciones.fetchall()


                for calif in filascalificaciones:
                    totalcaliffor = calif[0]

                #resultado de la suma de todas las calificaciones de ese libro.
                suma = str(totalcaliffor)

                #promedio de calificaciones
                promedioennumero = int(suma)/float(int(numeroregistros))
                promedioredondeado = round(promedioennumero)
                #se manda al template
                promedio = str(promedioredondeado)

            #PROMEDIO DE ESTRELLITAS!.--------------------------------------------------
                promedioestrellas = float((1/int(numeroregistros))*100) #50%

                calif1 = basededatos.execute("SELECT calificacion FROM reseñas WHERE libreo_isbn=:isbnmostrado AND calificacion = '1'",{"isbnmostrado":isbnreseña})
                calificacion1 = calif1.fetchall()

                prom1 = float(0)

                if calificacion1 is None:
                    prom1 = float(0)
                else:
                    for c1 in calificacion1:
                        prom1 += float(promedioestrellas)
                prom1redondeado = round(prom1)

                calif2 = basededatos.execute("SELECT calificacion FROM reseñas WHERE libreo_isbn=:isbnmostrado AND calificacion = '2'",{"isbnmostrado":isbnreseña})
                calificacion2 = calif2.fetchall()

                prom2 = float(0)

                if calificacion2 is None:
                    prom2 = float(0)
                else:
                    for c2 in calificacion2:
                        prom2 += float(promedioestrellas)
                prom2redondeado = round(prom2)

                calif3 = basededatos.execute("SELECT calificacion FROM reseñas WHERE libreo_isbn=:isbnmostrado AND calificacion = '3'",{"isbnmostrado":isbnreseña})
                calificacion3 = calif3.fetchall()

                prom3 = float(0)

                if calificacion3 is None:
                    prom3 = float(0)
                else:
                    for c3 in calificacion3:
                        prom3 += float(promedioestrellas)
                prom3redondeado = round(prom3)

                calif4 = basededatos.execute("SELECT calificacion FROM reseñas WHERE libreo_isbn=:isbnmostrado AND calificacion = '4'",{"isbnmostrado":isbnreseña})
                calificacion4 = calif4.fetchall()

                prom4 = float(0)

                if calificacion4 is None:
                    prom4 = float(0)
                else:
                    for c4 in calificacion4:
                        prom4 += float(promedioestrellas)
                prom4redondeado = round(prom4)

                calif5 = basededatos.execute("SELECT calificacion FROM reseñas WHERE libreo_isbn=:isbnmostrado AND calificacion = '5'",{"isbnmostrado":isbnreseña})
                calificacion5 = calif5.fetchall()

                prom5 = float(0)

                if calificacion5 is None:
                    prom5 = float(0)
                else:
                    for c5 in calificacion5:
                        prom5 += float(promedioestrellas)
                prom5redondeado = round(prom5)

                #se obtienen todas las reseñas
                reseña = basededatos.execute("SELECT idReseña, usuario_id, libreo_isbn, textoReseña, calificacion FROM reseñas WHERE libreo_isbn=:isbnmostrado",{"isbnmostrado":isbnreseña})
                filasreseña = reseña.fetchall()

                nombres = basededatos.execute("SELECT nombreusuario, apellidousuario FROM usuarios A, reseñas B WHERE B.usuario_id = A.id")
                filasnombres = nombres.fetchall()


                basededatos.commit()
                return render_template("infolibro.html",usuariomostrar=usuariomostrar, isbn=isbn, titulo=titulo, autor=autor, año=año, hayreseña=hayreseña, promedio=promedio , filasreseña=filasreseña , numeroregistros=numeroregistros, prom1=prom1, prom2=prom2, prom3=prom3, prom4=prom4, prom5=prom5, prom1redondeado=prom1redondeado , prom2redondeado=prom2redondeado, prom3redondeado=prom3redondeado, prom4redondeado=prom4redondeado, prom5redondeado=prom5redondeado, filasnombres=filasnombres)


@app.route("/review", methods=["POST", "GET"])
def review():
    isbnreview= request.form.get("isbnreview")
    texto_reseña = request.form.get("texto_reseña")
    calificacion = request.form.get("calificacion")

    if "user" in session:
        usuariosesion = session["user"]

        datosusuario =  basededatos.execute("SELECT id, usuario, nombreusuario FROM usuarios WHERE usuario=:nusuario",{"nusuario":usuariosesion}).fetchall()


        for dato in datosusuario:
            idusuario = dato[0]

        idusuario2 = str(idusuario)

        basededatos.execute("INSERT INTO reseñas (usuario_id, libreo_isbn, textoReseña, calificacion) VALUES (:dato1, :dato2, :dato3, :dato4)",{"dato1": idusuario2, "dato2": isbnreview, "dato3": texto_reseña, "dato4": calificacion})
        basededatos.commit()

        return redirect(url_for("mostrarlibro"))


@app.route("/opiniones", methods=["POST", "GET"])
def opiniones():
    if "user" in session:

        usuario = session["user"]

        nombreusuario = basededatos.execute("SELECT nombreusuario FROM usuarios WHERE usuario=:username",{"username":usuario}).fetchone()
        apellidousuario = basededatos.execute("SELECT apellidousuario FROM usuarios WHERE usuario=:username",{"username":usuario}).fetchone()
        idu = basededatos.execute("SELECT id FROM usuarios WHERE usuario=:username",{"username":usuario}).fetchone()

        for row in nombreusuario:
            nusuario = nombreusuario[0]

        for row in apellidousuario:
            ausuario = apellidousuario[0]

        for row in idu:
            idus = idu[0]

        idusuario = str(idus)
        usuariomostrar = nusuario + " " + ausuario

        opinionespersonales = basededatos.execute("SELECT usuario_id, libreo_isbn, textoreseña, calificacion FROM reseñas WHERE usuario_id=:id",{"id":idus})
        filasopinionespersonales = opinionespersonales.fetchall()

        nombreslibros = basededatos.execute("SELECT titulo, autor, año FROM libros A, reseñas B WHERE B.libreo_isbn = A.isbn")
        filasnombreslibros = nombreslibros.fetchall()

        if opinionespersonales is None:
            erroropinion = True
            basededatos.commit()
            return render_template("opiniones.html",usuariomostrar=usuariomostrar, erroropinion=erroropinion)

        else:
            opinion = True
            basededatos.commit()
            return render_template("opiniones.html",usuariomostrar=usuariomostrar, filasopinionespersonales= filasopinionespersonales, opinion=opinion, filasnombreslibros=filasnombreslibros)
