from exceptions.account_exception import *
from exceptions.customer_exception import *
from current_accounts.account import Account
from movements.movements_mysql import MySQLMovementsDAO
from movements.movements import Movements

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

def open_current_account(mysql_account, mysql_customer):
    while True:
        try:
            number_account = int(input("Escribe el número de la cuenta que quieras reabrir: "))
            dni = mysql_account.get_dni_by_account(number_account)
            
            if not dni:
                raise DNINotFoundError()
            
            if not mysql_customer.is_customer_active(dni):
                raise CustomerInactiveError()
            
            mysql_account.open_account(number_account)
            print("Cuenta reabierta correctamente.")
            break
        except DNINotFoundError as e:
            print(f"Error: {e}")
            return
        except CustomerInactiveError as e:
            print(f"Error: {e}")
            return
        except Exception as e:
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
    
    balance = mysql_account.get_balance(number_account)
    print(f"El saldo de la cuenta {number_account:010} es: {balance} €\n")

def deposit_money(mysql_account):
    while True:
        try:
            number_account = int(input("Escribe el número de la cuenta donde quieras depositar dinero: "))

            if not mysql_account.is_account_active(number_account):
                raise AccountInactiveError()

            balance = float(input("¿Qué cantidad quieres depositar? "))
            description = input("Escribe el concepto del deposito (Pulsa ENTER si no quieres añadir concepto): ")
            break
        except AccountInactiveError as e:
            print(f"Error: {e}")
            return
        except Exception as e:
            print(f"Error: {e}")

    deposit = Movements(number_account, balance, "ingreso", None, description)
    mysql_account.deposit(number_account, balance)
    movement = MySQLMovementsDAO()
    movement.create_movement(deposit)

def withdraw_money(mysql_account):
    while True:
        try:
            number_account = int(input("Escribe el número de la cuenta donde quieras retirar dinero: "))

            if not mysql_account.is_account_active(number_account):
                raise AccountInactiveError()

            balance = float(input("¿Qué cantidad quieres retirar? "))
            description = input("Escribe el concepto de la salida (Pulsa ENTER si no quieres añadir concepto): ")
            break
        except AccountInactiveError as e:
            print(f"Error: {e}")
            return
        except Exception as e:
            print(f"Error: {e}")

    withdraw = Movements(number_account, balance, "salida", None, description)
    mysql_account.withdraw(number_account, balance)
    movement = MySQLMovementsDAO()
    movement.create_movement(withdraw)

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
            description = input("Escribe el concepto de la transferencia (Pulsa ENTER si no quieres añadir concepto): ")
            break

        except AccountSourceInactiveError as e:
            print(f"Error: {e}")
            return
        except AccountTargetInactiveError as e:
            print(f"Error: {e}")
            return
        except Exception as e:
            print(f"Error: {e}")

    source_transfer = Movements(source_account, balance, "transferencia enviada", target_account, description)
    target_transfer = Movements(target_account, balance, "transferencia recibida", source_account, description)
    mysql_account.transfer_to(source_account, target_account, balance)
    movement = MySQLMovementsDAO()
    movement.create_movement(source_transfer)
    movement.create_movement(target_transfer)

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
        
        print("\n================= LISTADO DE CUENTAS CORRIENTES ==================")
        print("--------------------------------------------------------------------")
        print(" Nº Cuenta  | DNI       | Nombre               | Saldo     | Estado")
        print("--------------------------------------------------------------------")
        
        for account in accounts:
            number, dni, name, lastname, balance, active = account
            status = "Activa" if active else "Inactiva"
            full_name = f"{name} {lastname}"
            print(f" {number:010} | {dni:<9} | {full_name:<20} | {balance:>8.2f}€ | {status:<8}")
        print()
            
    except Exception as e:
        print(f"Error al consultar las cuentas: {e}")
    finally:
        cursor.close()