from dataclasses import dataclass
import mysql.connector
from mysql.connector import Error

@dataclass
class Database:
    host: str = "localhost"
    user: str = "angel"
    password: str = "angel"  
    database: str = "bank_account_manager"

# Configuración de la base de datos
database = Database()

def connect():
    """Establece la conexión a la base de datos"""
    try:
        connection = mysql.connector.connect(
            host=database.host,
            user=database.user,
            password=database.password,
            database=database.database
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
            host=database.host,
            user=database.user,
            password=database.password
        )
        cursor = temporal_connect.cursor()
        
        # Creamos la base de datos si no existe
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database.database}")
        temporal_connect.commit()
        cursor.close()
        temporal_connect.close()
        print(f"Base de datos '{database.database}' verificada/creada correctamente")
    except Error as e:
        print(f"Error al crear la base de datos: {e}")