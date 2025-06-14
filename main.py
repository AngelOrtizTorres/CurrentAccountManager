from customers.customer_mysql import MySQLCustomerDAO
from current_accounts.account_mysql import MySQLAccountDAO
from operations.customer_operations import *
from operations.account_operations import *
from menu import Menu
import os

main_menu = Menu("Gestionar Clientes", "Gestionar Cuentas Corrientes", "Operaciones en una Cuenta Corriente", "Salir", 
                 title = "Gestión de Cuentas Bancarias")

customer_menu = Menu("Añadir cliente", "Reactivar un cliente", "Dar de baja un cliente", "Modificar datos de cliente", 
                     "Ver todos los clientes", "Volver al menú principal", title = "Gestión de Clientes")

account_menu = Menu("Crear cuenta corriente", "Reabrir cuenta corriente", "Cerrar cuenta corriente", "Ver ingresos", "Ver salidas", 
                    "Ver transferencias", "Ver todas las cuentas corrientes", "Volver al menú principal", 
                    title = "Gestión de Cuentas Corrientes")

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
            case 2:
                option_account = account_menu.choose()
                choice_account(option_account)
            case 3:
                option_movements = movements_menu.choose()
                choice_movements(option_movements)
            case 4:
                exit()
            
def choice_customer(option):
    mysql_customer = MySQLCustomerDAO()
    mysql_account = MySQLAccountDAO()
    
    match option:
        case 1:
            ask_customer_data(mysql_customer)
        case 2:
            ask_customer_release(mysql_customer)
        case 3:
            ask_customer_deregister(mysql_customer, mysql_account)
        case 4:
            update_customer_data(mysql_customer)
        case 5:
            show_customers(mysql_customer)
        case 6:
            return       

def choice_account(option):
    mysql_customer = MySQLCustomerDAO()
    mysql_account = MySQLAccountDAO()
    
    match option:
        case 1:
            create_current_account(mysql_account)
        case 2:
            open_current_account(mysql_account, mysql_customer)
        case 3:
            close_current_account(mysql_account)
        case 4:
            print("Función 'Ver ingresos' aún no implementada.")
        case 5:
            print("Función 'Ver salidas' aún no implementada.")
        case 6:
            print("Función 'Ver transferencias' aún no implementada.")
        case 7:
            show_all_accounts(mysql_account)
        case 8:
            return
        
def choice_movements(option):
    mysql_account = MySQLAccountDAO()

    match option:
        case 1:
            consult_balance(mysql_account)
        case 2:
            print("Función 'Ver movimientos entre fechas' aún no implementada.")
        case 3:
            deposit_money(mysql_account)
        case 4:
            withdraw_money(mysql_account)
        case 5:
            transfer_money(mysql_account)
        case 6:
            return

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    main()