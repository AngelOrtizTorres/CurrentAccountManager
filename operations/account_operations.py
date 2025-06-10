from exceptions.account_exception import *
from current_accounts.account import Account
from current_accounts.account_mysql import MySQLAccountDAO

def create_current_account(mysql_account):
    dni = input("Añade el DNI del cliente al que quieras crear un cuenta: ")
    amount = input("Añade la cantidad de saldo que quieres en la cuenta (Pulsa ENTER si no quieres añadir nada): ")
    if amount == "":
        balance = 0
    else:
        balance = float(amount)
    current_account = Account(dni, balance)
    mysql_account.create_account(current_account)

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
            balance = float(input("¿Qué cantidad quieres depositar? "))
            break
        except Exception as e:
            print(f"Error: {e}")

    mysql_account.deposit(number_account, balance)

def withdraw_money(mysql_account):
    while True:
        try:
            number_account = int(input("Escribe el número de la cuenta donde quieras retirar dinero: "))
            balance = float(input("¿Qué cantidad quieres retirar? "))
            break
        except Exception as e:
            print(f"Error: {e}")

    mysql_account.withdraw(number_account, balance)

def transfer_money(mysql_account):
    while True:
        try:
            source_account = int(input("Escribe el número de la cuenta que realizará la transferencia: "))
            target_account = int(input("Escribe el número de la cuenta receptora: "))
            balance = float(input("¿Qué cantidad quieres transferir? "))
            break
        except Exception as e:
            print(f"Error: {e}")

    mysql_account.transfer_to(source_account, target_account, balance)