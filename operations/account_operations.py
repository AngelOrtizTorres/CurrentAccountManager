from exceptions.account_exception import *
from current_accounts.account import Account
from current_accounts.account_mysql import MySQLAccountDAO

def create_current_account(mysql_account):
    dni = input("Añade el DNI del cliente al que quieras crear una cuenta: ")
    
    while True:
        try:
            balance_input = input("Añade la cantidad de saldo que quieres en la cuenta (Pulsa ENTER si no quieres añadir nada): ")
            amount = float(balance_input) if balance_input else 0.0

            if amount < 0:
                raise NegativeAmountError()
            break
        except NegativeAmountError as e:
            print(f"{e}")

    try:
        current_account = Account(dni, amount)
        mysql_account.create_account(current_account)
    except NegativeAmountError as e:
        print(f"Error: {e}")

def close_current_account(mysql_account):
    while True:
        try:
            number_account = int(input("Escribe el número de la cuenta que quieras cerrar: "))
            break
        except Exception as e:
            print(f"Error: {e}")
    
    mysql_account.close_account(number_account)

def consult_balance(mysql_account):
    while True:
        try:
            number_account = int(input("Escribe el número de la cuenta que quieras ver su saldo: "))
            break
        except Exception as e:
            print(f"Error: {e}")
    
    mysql_account.get_balance(number_account)

def deposit_money(mysql_account):
    while True:
        try:
            number_account = int(input("Escribe el número de la cuenta donde quieras depositar dinero: "))

            if not mysql_account.is_account_active(number_account):
                raise AccountInactiveError()

            balance = float(input("¿Qué cantidad quieres depositar? "))
            break
        except AccountInactiveError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error: {e}")

    mysql_account.deposit(number_account, balance)

def withdraw_money(mysql_account):
    while True:
        try:
            number_account = int(input("Escribe el número de la cuenta donde quieras retirar dinero: "))

            if not mysql_account.is_account_active(number_account):
                raise AccountInactiveError()

            balance = float(input("¿Qué cantidad quieres retirar? "))
            break
        except AccountInactiveError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error: {e}")

    mysql_account.withdraw(number_account, balance)

def transfer_money(mysql_account):
    while True:
        try:
            source_account = int(input("Escribe el número de la cuenta que realizará la transferencia: "))
            target_account = int(input("Escribe el número de la cuenta receptora: "))

            if not mysql_account.is_account_active(source_account):
                raise AccountSourceInactiveError()
        
            if not mysql_account.is_account_active(target_account):
                raise AccountTargetInactiveError()

            balance = float(input("¿Qué cantidad quieres transferir? "))
            break
        
        except AccountSourceInactiveError as e:
            print(f"Error: {e}")
            return
        except AccountTargetInactiveError as e:
            print(f"Error: {e}")
            return
        except Exception as e:
            print(f"Error: {e}")

    mysql_account.transfer_to(source_account, target_account, balance)

def show_all_accounts(mysql_account):
    cursor = mysql_account.connection.cursor()
    try:
        cursor.execute("""
            SELECT c.numero_cuenta, c.dni, cu.nombre, cu.apellido, c.saldo, c.activa 
            FROM current_account c
            JOIN customer cu ON c.dni = cu.dni
            ORDER BY c.numero_cuenta
        """)
        accounts = cursor.fetchall()
        
        print("\n=== LISTADO DE CUENTAS ===")
        print("Nº Cuenta | DNI       | Nombre            | Saldo    | Estado")
        print("-" * 65)
        
        for account in accounts:
            number, dni, name, lastname, balance, active = account
            status = "Activa" if active else "Inactiva"
            print(f"{number:<9} | {dni:<9} | {name} {lastname:<15} | {balance:>8.2f}€ | {status}")
        print()
            
    except Exception as e:
        print(f"Error al consultar las cuentas: {e}")
    finally:
        cursor.close()