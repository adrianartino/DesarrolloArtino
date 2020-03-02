from flask import Flask, render_template #se usara un template, osea un archivo

app = Flask(__name__) 

@app.route("/") 
def index(): 
    variableenindex = "Hello, world informatico!" #variable string
    return render_template("index.html", headline=variableenindex) #ejectuar index.html 
    #La variable variableenindex declarada aqui, ira como headline en archivo index.html

#ruta bye    
@app.route("/bye") 
def bye(): 
    variablebye = "Goodbye!" #variable 
    return render_template("index.html", headline=variablebye)

#aqui se utiliza la funcion headline para cambiar el nombre o mensaje, dependiendo de la ruta