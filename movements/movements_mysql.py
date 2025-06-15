from __future__ import annotations
from movements.movements import Movements
from movements.movementsDao import MovementsDAO
from mysql.connector import Error
from typeguard import typechecked
from database.config_db import connect, create_database_if_not_exists

class MySQLMovementsDAO(MovementsDAO):

    def __init__(self):
        create_database_if_not_exists()
        self.connection = connect()
        self._create_table()

    def _execute_query(self, query: str, parameters: tuple = ()):
        cursor = None
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, parameters)
            self.connection.commit()
        except Error as e:
            print(f"Error: {e}")
        finally:
            if cursor:
                cursor.close()

    def _create_table(self):
        create_table_customer = """
        CREATE TABLE IF NOT EXISTS movements(
        id INT AUTO_INCREMENT PRIMARY KEY,
        numero_cuenta INT,
        importe DECIMAL(10, 2),
        fecha_hora DATETIME,
        tipo ENUM('ingreso', 'salida', 'transferencia enviada', 'transferencia recibida'),
        cuenta_transferencia INT,
        concepto VARCHAR(255)
        )
        """
        self._execute_query(create_table_customer)

    def create_movement(self, movement: Movements):
        add_movement = """
        INSERT INTO movements(numero_cuenta, importe, fecha_hora, tipo, cuenta_transferencia, concepto)
        VALUES(%s, %s, %s, %s, %s, %s)
        """
        self._execute_query(add_movement, (movement._number_account, movement._amount, movement._timestamp, 
                                           movement._movement_type, movement._transfer_account, movement._description))