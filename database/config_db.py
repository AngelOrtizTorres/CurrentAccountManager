from dataclasses import dataclass
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

def connect():
    try:
        load_dotenv()
        connection = mysql.connector.connect(
            host=os.getenv("HOST"),
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD"),
            database=os.getenv("DATABASE")
        )
        if connection.is_connected():
            print("\nConexión exitosa a la base de datos\n")
            return connection
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        raise

def create_database_if_not_exists():
    try:
        load_dotenv()
        temporal_connect = mysql.connector.connect(
            host=os.getenv("HOST"),
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD")
        )
        cursor = temporal_connect.cursor()
        
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {os.getenv("DATABASE")}")
        temporal_connect.commit()
        cursor.close()
        temporal_connect.close()
    except Error:
        print(f"\nLa base de datos ya ha sido creada")