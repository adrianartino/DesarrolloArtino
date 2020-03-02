from flask import Flask, render_template 

app = Flask(__name__) 

@app.route("/") 
def index(): 
    grupodenombres = ["Alice", "Bob", "Charlie"] 
    return render_template("index.html", names=grupodenombres)