import os
from flask import Flask, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
app = Flask(__name__)

engine = create_engine("postgresql://postgres:marcos619@localhost:5432/airline")
db = scoped_session(sessionmaker(bind=engine))

@app.route("/") #al iniciar la app, se llena un arreglo flights
def index():
    flights = db.execute("SELECT * FROM vuelos").fetchall()
    return render_template("index.html", flights=flights)

@app.route("/book", methods=["POST"])
def book():
    """Book a flight."""

    # Get form information.
    name = request.form.get("name") #guarda el nombre
    try:
        flight_id = int(request.form.get("flight_id")) #guarda el vuelo
    except ValueError:
        return render_template("error.html", message="Invalid flight number.")


    # Make sure flight exists.
    if db.execute("SELECT * FROM vuelos WHERE id = :id", {"id": flight_id}).rowcount == 0:
        return render_template("error.html", message="No such flight with that id.")

    db.execute("INSERT INTO pasajeros (nombre, id_vuelo) VALUES (:nombre, :id_vuelo)", {"nombre": name, "id_vuelo": flight_id}) #insertar nuevo pasajero
    db.commit() #guardar datos de base de datos
    return render_template("success.html") #

@app.route("/flights")
def flights():
    """Lists all flights."""
    flights = db.execute("SELECT * FROM vuelos").fetchall()
    return render_template("flights.html", flights=flights)
@app.route("/flight/<int:flight_id>")

def flight(flight_id):
    """Lists details about a single flight."""
    flight = db.execute("SELECT * FROM vuelos WHERE id = :id", {"id": flight_id}).fetchone()
    if flight is None:
        return render_template("error.html", message="No such flight.")
    passengers = db.execute("SELECT nombre FROM pasajeros WHERE id_vuelo =:flight_id", {"flight_id": flight_id}).fetchall()
    return render_template("flight.html", flight=flight, passengers=passengers)
