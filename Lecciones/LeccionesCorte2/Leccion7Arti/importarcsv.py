import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine("postgresql://postgres:marcos619@localhost:5432/airline")
db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open("flights.csv")
    reader = csv.reader(f)
    for origen, destino, duracion in reader:
        db.execute("INSERT INTO vuelos (origen, destino, duracion) VALUES (:origen, :destino, :duracion)",{"origen": origen, "destino": destino, "duracion": duracion})
        print(f"Added flight from {origen} to {destino} lasting {duracion} minutes.")
    db.commit()

if __name__ == "__main__":
    main()
