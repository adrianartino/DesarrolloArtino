from flask import Flask, render_template, request 

app = Flask(__name__) 

@app.route("/") 
def index(): 
    return render_template("index.html") 

@app.route("/hello", methods=["GET","POST"]) #get es cuando se entra directo y post cuando ya se manda algo
def hello(): 
    
    if request.method=="GET":  #cuando se quiera entrar directamente a la ruta..
        return "Please submit the form instead." #Decir que porfavor ingrese datos y de clic al boton
    
    else:
        name = request.form.get("name") 
        return render_template("hello.html", name=name) 