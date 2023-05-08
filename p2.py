#!/usr/bin/env python3
# Autor: Fernando Barrado Lucia

#Librerias
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import *
from sqlalchemy.engine import reflection

# Conexión a la base de datos sakila
#Poner el usuario y contraseña con el que se desea trabajar, en este caso root 
engine = create_engine('mysql+pymysql://root:bd22223@localhost/sakila')
metadata = MetaData()
metadata.bind = engine
Session = sessionmaker(bind=engine)
Base = declarative_base()
session = Session()

# Definición de las tablas
class Country(Base):
    __tablename__ = 'country'
    country_id = Column(Integer, primary_key=True, autoincrement=True)
    country = Column(String(50))
    last_update = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

class City(Base):
    __tablename__ = 'city'
    city_id = Column(Integer, primary_key=True, autoincrement=True)
    city = Column(String(50))
    country_id = Column(Integer, ForeignKey('country.country_id'))
    country = relationship('Country')
    last_update = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    age = Column(Integer)
    email = Column(String(50), unique=True)

# Funciones auxiliares
def crear_pais():
    nombre = input("Nombre del país: ")
    try:
        pais = Country(country=nombre)
        session.add(pais)
        session.commit()
        print(f"País {nombre} creado con éxito.")
    except IntegrityError:
        session.rollback()
        print("Error no se puede crear este pais")

def listar_paises():
    paises = session.query(Country).all()
    if paises:
        for pais in paises:
            print(pais.country_id, pais.country, pais.last_update)
    else:
        print("No se encontraron países.")

#Se borrarán solo los paises que sus ciudades no esten relacionadas con otras entidades
def eliminar_pais():
    id_pais = input("ID del país a eliminar: ")
    try:
        ciudades = session.query(Country).filter_by(country_id=id_pais).all()
        pais = session.query(Country).filter_by(country_id=id_pais).first()
        for ciudad in ciudades:
            session.delete(ciudad)
        session.delete(pais)
        session.commit()
    except IntegrityError:
        session.rollback()
        print("Error no se puede borrar este pais")

def crear_ciudad():
    nombre = input("Nombre de la ciudad: ")
    id_pais = input("ID del país de la ciudad: ")
    try:
        ciudad = City(city=nombre, country=id_pais)
        session.add(ciudad)
        session.commit()
        print(f"Ciudad {nombre} creada con éxito.")
    except IntegrityError:
        session.rollback()
        print("Error no se puede una ciudad con ese pais")

def listar_ciudades():
    ciudades = session.query(City).all()
    if ciudades:
        for ciudad in ciudades:
            print(ciudad.city_id, ciudad.city, ciudad.country_id, ciudad.last_update)
    else:
        print("No se encontraron ciudades.")

#Se borraran solo las ciudades que no esten relacionadas con otras entidades
def eliminar_ciudad(session):
    id_ciudad = input("ID de la ciudad a eliminar: ")
    try:
        ciudad = session.query(Country).filter_by(country_id=id_ciudad).first()
        session.delete(ciudad)
        session.commit()
    except IntegrityError:
        session.rollback()
        print("Error no se puede borrar esta ciudad")

def crear_tabla_usuarios():
    metadata.create_all(bind=engine, tables=[User.__table__])
    print("Se ha creado la tabla usuarios")

def borrar_tabla_usuarios():
    tabla = Table('user', metadata)
    tabla.drop(engine)
    print("Se ha borrado la tabla usuarios")

#Muestra el nombre de las columnas de la tabla y los datos que posee
def mostrar_estructura_tabla_usuarios():
    inspector = inspect(engine)
    tabla = 'user'
    columns = inspector.get_columns(tabla)
    for column in columns:
        print(f"Name {column['name']} Type: {column['type']}")

# Menú principal
while True:
    print("\nMenú principal:")
    print("1. Crear país")
    print("2. Listar países")
    print("3. Eliminar país")
    print("4. Crear ciudad")
    print("5. Listar ciudades")
    print("6. Eliminar ciudad")
    print("7. Crear tabla usuarios")
    print("8. Borrar tabla usuarios")
    print("9. Mostrar estructura tabla")
    print("0. Salir")
    opcion = input("Ingrese una opción: ")

    if opcion == "1":
        crear_pais()
    elif opcion == "2":
        listar_paises()
    elif opcion == "3":
        eliminar_pais()
    elif opcion == "4":
        crear_ciudad()
    elif opcion == "5":
        listar_ciudades()
    elif opcion == "6":
        eliminar_ciudad()
    elif opcion == "7":
        crear_tabla_usuarios()
    elif opcion == "8":
        borrar_tabla_usuarios()
    elif opcion == "9":
        mostrar_estructura_tabla_usuarios()
    elif opcion == "0":
        break
    else:
        print("Opción inválida. Intente de nuevo.")
