import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine("postgresql://postgres:marcos619@localhost:5432/airline")
db = scoped_session(sessionmaker(bind=engine))

def main():

    #Primero: Listar todos los vuelos.
    flights = db.execute("SELECT id, origen, destino, duracion FROM vuelos").fetchall()
    for flight in flights:
        print(f"Vuelos {flight.id}: {flight.origen} to {flight.destino}, {flight.duracion} minutes.")

    #segundo: Solicitar al usuario que elija un vuelo.
    flight_id = int(input("\nFlight ID: "))
    flight = db.execute("SELECT origen, destino, duracion FROM vuelos WHERE id = :id",{"id": flight_id}).fetchone()

    #Asegurarse de que el nuevo vuela sea válido.
    if flight is None:
        print("Error: No existe tal vuelo.")
        return

    #Tercero: Lista de pasajeros.
    passengers = db.execute("SELECT nombre FROM pasajeros WHERE id_vuelo = :flight_id",{"flight_id": flight_id}).fetchall()

    print("\nPasajeros:")
    for passenger in passengers:
        print(passenger.nombre)

    if len(passengers) == 0:
        print("No hay pasajeros")
if __name__ == "__main__":
    main()
