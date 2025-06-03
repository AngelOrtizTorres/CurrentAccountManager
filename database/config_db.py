from dataclasses import dataclass
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

def connect():
    """Establece la conexión a la base de datos"""
    try:
        load_dotenv()
        connection = mysql.connector.connect(
            host=os.getenv("HOST"),
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD"),
            database=os.getenv("DATABASE")
        )
        if connection.is_connected():
            print("Conexión exitosa a la base de datos")
            return connection
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")

def create_database_if_not_exists():
    """Crea la base de datos si no existe"""
    try:
        # Primero nos conectamos sin especificar la base de datos
        temporal_connect = mysql.connector.connect(
            host=os.getenv("HOST"),
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD")
        )
        cursor = temporal_connect.cursor()
        
        # Creamos la base de datos si no existe
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {os.getenv("DATABASE")}")
        temporal_connect.commit()
        cursor.close()
        temporal_connect.close()
        print(f"Base de datos '{os.getenv("DATABASE")}' verificada/creada correctamente")
    except Error as e:
        print(f"Error al crear la base de datos: {e}")