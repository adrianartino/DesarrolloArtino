from flask import Flask, render_template, request, session 
from datetime import timedelta 

app = Flask(__name__) 

app.secret_key = "whatever" #Para el cifrado, Flask necesita una SECRET_KEY definida, cualquier string.
app.permanent_session_lifetime=timedelta(minutes=1) #la sesión durará lo que pongamos aquí

@app.route("/", methods=["GET", "POST"]) 
def index(): 
    if session.get("notes") is None: #si no se manda nada..
        session["notes"] = [] #sesio vacia
        
    if request.method == "POST": #si se manda algo..
        session.permanent=True  #definir esta sesión específica como permanente, según lo que hayamos puesto de tiempo
        note = request.form.get("note") #recogemos la nota y la agregamos a la variable de sesión
        session["notes"].append(note) 
        
    return render_template("index.html", notes=session["notes"]) 
    #mandamos la variable de sesión al render