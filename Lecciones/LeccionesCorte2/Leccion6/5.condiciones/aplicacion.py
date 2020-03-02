import datetime #libreria para fechas y tiempos

from flask import Flask, render_template 

app = Flask(__name__) 

@app.route("/") 
def index(): 
    now = datetime.datetime.now()  #fecha y hora actuales guardada en variable now
    new_year = (now.month == 1) and (now.day == 1) 
    new_year = True #para hacer que si sea año nuevo
    return render_template("index.html", new_year=new_year)