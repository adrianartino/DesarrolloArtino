import random #importar random

from flask import Flask, render_template

app = Flask(__name__) 

@app.route("/") 
def index(): 
    #la variablerandom escoge un nombre al azar:
    variablerandom = random.choice(["Hello, world!", "Hi there!", "Good morning!"]) 
    return render_template("index.html", headline=variablerandom) #La variable headline de flask es el nombre random que se eligio

