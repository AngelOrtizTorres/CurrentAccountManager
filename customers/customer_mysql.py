from __future__ import annotations
from customers.customerDao import CustomerDAO
from customers.customer import Customer
from mysql.connector import Error
from typeguard import typechecked
from database.config_db import connect, create_database_if_not_exists

@typechecked
class MySQLCustomerDAO(CustomerDAO):

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
        CREATE TABLE IF NOT EXISTS customer(
        dni VARCHAR(9) PRIMARY KEY,
        nombre VARCHAR(50),
        apellido VARCHAR(50),
        telefono VARCHAR(20),
        direccion VARCHAR(150),
        activo BOOL
        )
        """
        self._execute_query(create_table_customer)

    def add_customer(self, customer: Customer):
        insert_customer = """
        INSERT INTO customer (dni, nombre, apellido, telefono, direccion, activo)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        self._execute_query(insert_customer, (customer._dni, customer.name, customer.lastname, customer.phone, 
                                         customer.address, customer.active))

    def update_customer(self, name: str, lastname: str, phone: str, address: str, dni: str):
        update_customers = """
        UPDATE customer SET nombre = %s, apellido = %s, telefono = %s, direccion = %s
        WHERE dni = %s
        """
        self._execute_query(update_customers, (name, lastname, phone, 
                                         address, dni))

    def get_customer(self, dni: str):
        select_customer = "SELECT * FROM customer WHERE dni = %s"
        cursor = self.connection.cursor()
        try:
            cursor.execute(select_customer, (dni,))
            result = cursor.fetchone()  
            if result:
                return Customer(result[0], result[1], result[2], result[3], result[4])
            return None
        finally:
            cursor.close()

    def release(self, dni: str):
        release_customer = """
        UPDATE customer SET activo = True WHERE dni = %s
        """
        self._execute_query(release_customer, (dni,))

    def deregister(self, dni: str):
        deregister_customer = """
        UPDATE customer SET activo = False WHERE dni = %s
        """
        self._execute_query(deregister_customer, (dni,))

    def is_customer_active(self, dni: str):
        customer_query = "SELECT activo FROM customer WHERE dni = %s"
        cursor = self.connection.cursor()
        try:
            cursor.execute(customer_query, (dni,))
            result = cursor.fetchone()
            if result is None:
                raise Exception(f"No se encontró cliente con DNI {dni}")
            return bool(result[0])
        except Exception as e:
            print(f"Error al verificar estado del cliente: {e}")
            raise
        finally:
            cursor.close()

    def close_connection(self):
           if self.connection and self.connection.is_connected():
               self.connection.close()