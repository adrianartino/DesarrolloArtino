from flask import Flask #Importar flask

app = Flask(__name__) #archivo que representa aplicacion web

#ruta principal (index)
@app.route("/")
def index():   #funcion index o /
    return "Hello, world!!!"

#Cuando se agege la ruta david
@app.route("/david") 
def david(): 
    return "Hello, David!"

#Para saludar a maria
@app.route("/maria") 
def maria(): 
    return "Hello, Maria!"

#para cualquier nombre
@app.route("/<string:name>") #Hacer que el nombre que se escriba lo guarde en una variable name
def hello(name):  #funcion hello(el nombre que se ha puesto)
    return f"Hello, {name}!" #Saluda con el nombre

#si se pone un espacio, la ruta debe de ser Marcos%20Adrian

app.run(port=5000, debug=True)