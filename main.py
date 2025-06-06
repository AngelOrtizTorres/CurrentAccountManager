import mysql.connector
from exceptions.customer_exception import *
from customers.customerDao import CustomerDAO
from customers.customer_mysql import MySQLCustomerDAO
from customers.customer import Customer
"""from current_accounts.account_dao import AccountDAO
from current_accounts.accounts import CurrentAccount"""
from menu import Menu
import os

main_menu = Menu("Gestionar Clientes", "Gestionar Cuentas Corrientes", "Operaciones en una Cuenta Corriente", "Salir", 
                 title = "Gestión de Cuentas Bancarias")

customer_menu = Menu("Añadir cliente", "Reactivar un cliente", "Dar de baja un cliente", "Modificar datos de cliente",
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
            ask_customer_data(mysql_customer)
            
        case 2:
            ask_customer_release(mysql_customer)
        case 3:
            ask_customer_deregister(mysql_customer)
        case 4:
            update_customer_data(mysql_customer)
        case 5:
            return
                

def choice_account(option):
    pass

def choice_movements(option):
    pass

def ask_customer_data(mysql_customer):
    while True:
        try:
            dni = input("Añade tu DNI: ")
            Customer._validate_format_dni(dni)
            break
        except (LetterErrorDNI, FormatErrorDNI) as e:
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

def ask_customer_release(mysql_customer):
    while True:
        dni = input("Ingresa el dni del cliente que quieras reactivar: ")
        Customer._validate_format_dni(dni)
        mysql_customer.release(dni)
        break

def ask_customer_deregister(mysql_customer):
    while True:
        dni = input("Ingresa el dni del cliente que quieras dar de baja: ")
        Customer._validate_format_dni(dni)
        mysql_customer.deregister(dni)
        break

def update_customer_data(mysql_customer):
    while True:
        try:
            dni = input("Añade el DNI del cliente que quieras modificar: ")
            Customer._validate_format_dni(dni)
            current_customer = mysql_customer.get_customer(dni)
            if not current_customer:
                print("No se encontró ningún cliente con ese DNI.")
                continue
            break
        except (LetterErrorDNI, FormatErrorDNI) as e:
            print(f"Error: {e}")
            return

    try:
        name = input("Añade el nuevo nombre (Enter para mantener el actual): ")
        name = name if name.strip() else current_customer.name
        
        lastname = input("Añade el nuevo apellido (Enter para mantener el actual): ")
        lastname = lastname if lastname.strip() else current_customer.lastname

        phone = get_updated_phone(current_customer.phone)
        
        address = input("Añade la nueva dirección (Enter para mantener el actual): ")
        address = address if address.strip() else current_customer.address

        mysql_customer.update_customer(name, lastname, phone, address, dni)
        print("Cliente actualizado correctamente.")
    except Exception as e:
        print(f"Error al actualizar el cliente: {e}")

def get_updated_phone(current_phone):
    while True:
        try:
            phone = input("Añade el nuevo número de teléfono (Enter para mantener el actual): ")
            if phone.strip():
                Customer._validate_phone(phone)
                return phone
            return current_phone
        except ValidationException as e:
            print(f"Error: {e}")

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    main()