import csv #libreria para importar
import os #sistema operativo

from sqlalchemy import create_engine   #crear instancia para base de datos
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine("postgres://saciatig:qdSgbJnUJhokzzt7IQhMZSEBD41EfRGS@otto.db.elephantsql.com:5432/saciatig") #se conecta a la base de datos
db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open("books.csv") #abre en una variable el archivo de los libros .csv
    reader = csv.reader(f) #lee los datos y los guarda en una variable llamada read

    #for para mandar los datos del csv a la base de datos por fila
    for dato1, dato2, dato3, dato4 in reader:
        db.execute("INSERT INTO libros (isbn, titulo, autor, año) VALUES (:isbn, :titulo, :autor, :año)",{"isbn": dato1, "titulo": dato2, "autor": dato3, "año": dato4})
        print(f"Isbn: {dato1} - Titulo: {dato2} - Autor: {dato3} - Año: {dato4}")
    db.commit()

if __name__ == "__main__":
    main()
