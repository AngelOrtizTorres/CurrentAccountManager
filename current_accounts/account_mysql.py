from __future__ import annotations
from current_accounts.account import Account
from current_accounts.accountDao import AccountDAO
from mysql.connector import Error
from exceptions.account_exception import *
from typeguard import typechecked
from database.config_db import connect, create_database_if_not_exists

@typechecked
class MySQLAccountDAO(AccountDAO):

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

    def _execute_transaction(self, queries_with_params: list[tuple[str, tuple]]):
        cursor = None
        try:
            cursor = self.connection.cursor()
            for query, params in queries_with_params:
                cursor.execute(query, params)
            self.connection.commit()
        except Error as e:
            self.connection.rollback()
            print(f"Error en transacción: {e}")
            raise
        finally:
            if cursor:
                cursor.close()

    def _create_table(self):
        create_table_customer = """
        CREATE TABLE IF NOT EXISTS current_account(
        numero_cuenta int PRIMARY KEY,
        dni VARCHAR(9),
        saldo DECIMAL(18, 2) CHECK (saldo >= 0), 
        activa BOOL
        )
        """
        self._execute_query(create_table_customer)

    def create_account(self, account: Account):

        if account._balance < 0:
            raise NegativeAmountError()
    
        insert_query = """
        INSERT INTO current_account (numero_cuenta, dni, saldo, activa)
        VALUES (%s, %s, %s, %s)
        """
        self._execute_query(insert_query, (account._account_number, account._dni, account._balance, account.state))

    def open_account(self, account_number: int):
        active_account = """
        UPDATE current_account SET activa = True WHERE numero_cuenta = %s
        """
        self._execute_query(active_account, (account_number,))

    def close_account(self, account_number: int):
        deactivate_account = """
        UPDATE current_account SET activa = False WHERE numero_cuenta = %s
        """
        self._execute_query(deactivate_account, (account_number,))

    def is_account_active(self, account_number: int) -> bool:
        get_state = """
        SELECT activa FROM current_account WHERE numero_cuenta = %s
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute(get_state, (account_number,))
            result = cursor.fetchone()
            if result is None:
                raise AccountNotFoundError()
            return bool(result[0])
        except Error as e:
            print(f"Error: {e}")
            raise
        finally:
            cursor.close()

    def deposit(self, account_number: int, amount: float):
        if amount <= 0:
            raise NegativeAmountError()
        deposit_movement = "UPDATE current_account SET saldo = saldo + %s WHERE numero_cuenta = %s"
        self._execute_query(deposit_movement, (amount, account_number))

    def withdraw(self, account_number: int, amount: float):
        if amount <= 0:
            raise NegativeAmountError()
        balance = self.get_balance(account_number)
        if balance < amount:
            raise InsufficientBalanceError()
        withdraw_movement = "UPDATE current_account SET saldo = saldo - %s WHERE numero_cuenta = %s"
        self._execute_query(withdraw_movement, (amount, account_number))

    def get_balance(self, account_number: int):
        get_balance_account = "SELECT saldo FROM current_account WHERE numero_cuenta = %s"
        cursor = self.connection.cursor()
        try:
            cursor.execute(get_balance_account, (account_number,))
            result = cursor.fetchone()
            if result is None:
                raise AccountNotFoundError()
            return float(result[0])
        except Error as e:
            print(f"Error al obtener el saldo: {e}")
            raise
        finally:
            cursor.close()

    def transfer_to(self, source_account: int, target_account: int, amount: float):
        if amount <= 0:
            raise NegativeAmountError()
        if self.get_balance(source_account) < amount:
            raise InsufficientBalanceError()

        transactions = [
            ("UPDATE current_account SET saldo = saldo - %s WHERE numero_cuenta = %s", (amount, source_account)),
            ("UPDATE current_account SET saldo = saldo + %s WHERE numero_cuenta = %s", (amount, target_account)),
        ]
        self._execute_transaction(transactions)

    def has_active_accounts(self, dni: str):
        count_query = "SELECT COUNT(*) FROM current_account WHERE dni = %s AND activa = TRUE"
        cursor = self.connection.cursor()
        try:
            cursor.execute(count_query, (dni,))
            result = cursor.fetchone()
            return result[0] > 0
        finally:
            cursor.close()
    
    def get_dni_by_account(self, account_number: int):
        get_dni_query = "SELECT dni FROM current_account WHERE numero_cuenta = %s"
        cursor = self.connection.cursor()
        try:
            cursor.execute(get_dni_query, (account_number,))
            result = cursor.fetchone()
            if result:
                return result[0]
            return None
        except Exception as e:
            print(f"Error al obtener DNI por cuenta: {e}")
            return None
        finally:
            cursor.close()

    def close_connection(self):
           if self.connection and self.connection.is_connected():
               self.connection.close()