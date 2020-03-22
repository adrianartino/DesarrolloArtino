import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine("postgresql://postgres:marcos619@localhost:5432/airline")
db = scoped_session(sessionmaker(bind=engine))

def main():
    flights = db.execute("SELECT origen, destino, duracion FROM vuelos").fetchall()
    for flight in flights:
        print(f"{flight.origen} to {flight.destino}, {flight.duracion} minutos.")

if __name__ == "__main__":
    main()
