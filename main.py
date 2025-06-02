import mysql.connector
from utils.customer_exception import *
from customers.customerDao import CustomerDAO
from customers.customer_mysql import MySQLCustomerDAO
from customers.customer import Customer
"""from current_accounts.account_dao import AccountDAO
from current_accounts.accounts import CurrentAccount"""
from menu import Menu
import os

main_menu = Menu("Gestionar Clientes", "Gestionar Cuentas Corrientes", "Operaciones en una Cuenta Corriente", "Salir", 
                 title = "Gestión de Cuentas Bancarias")

customer_menu = Menu("Añadir cliente", "Dar de alta un cliente", "Dar de baja un cliente", "Modificar datos de cliente",
                     "Volver al menú principal", title = "Gestión de Clientes")

account_menu = Menu("Crear cuenta corriente", "Cerrar cuenta", "Ver ingresos", "Ver salidas", "Ver transferencias", 
                    "Volver al menú principal", title = "Gestión de Cuentas Corrientes")

movements_menu = Menu("Consultar saldo", "Ver movimientos entre fechas", "Ingresar dinero", "Retirar dinero", 
                      "Hacer transferencia", "Volver al menú principal", title = "Gestión de movimientos")

def main():
    while True:
        option = main_menu.choose()
        clear_terminal()
        match option:
            case 1:
                option_customer = customer_menu.choose()
                choice_customer(option_customer)
                clear_terminal()
            case 2:
                option_account = account_menu.choose()
                choice_account(option_account)
                clear_terminal()
            case 3:
                option_movements = movements_menu.choose()
                choice_movements(option_movements)
                clear_terminal()
            case 4:
                exit()
            
def choice_customer(option):
    mysql_customer = MySQLCustomerDAO()
    match option:
        case 1:
            while True:
                try:
                    dni = input("Añade tu DNI: ")
                    Customer._validate_format_dni(dni)
                    break
                except LetterErrorDNI as e:
                    print(f"Error: {e}")
                except FormatErrorDNI as e:
                    print(f"Error: {e}")
            
            name = input("Añade tu nombre: ")
            lastname = input("Añade tu apellido: ")

            while True:
                try:
                    phone = input("Añade tu número de teléfono: ")
                    Customer._validate_phone(phone)
                    break
                except ValidationException as e:
                    print(f"Error: {e}")

            address = input("Añade tu dirección: ")

            customer = Customer(dni, name, lastname, phone, address)
            mysql_customer.add_customer(customer)
            
        case 2:
            while True:
                dni = input("Ingresa el dni del cliente que quieras dar de alta: ")
                Customer._validate_format_dni(dni)
                mysql_customer.release(dni)
        case 3:
            while True:
                dni = input("Ingresa el dni del cliente que quieras dar de baja: ")
                Customer._validate_format_dni(dni)
                mysql_customer.deregister(dni)
        case 4:
            pass

def choice_account(option):
    pass

def choice_movements(option):
    pass

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    main()