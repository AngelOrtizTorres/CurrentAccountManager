from exceptions.customer_exception import *
from customers.customer import Customer
from current_accounts.account_mysql import MySQLAccountDAO

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

def ask_customer_deregister(mysql_customer, mysql_account):
    while True:
        dni = input("Ingresa el dni del cliente que quieras dar de baja: ")
        try:
            Customer._validate_format_dni(dni)
        except (LetterErrorDNI, FormatErrorDNI) as e:
            print(f"Error: {e}")
            continue

        if mysql_account.has_active_accounts(dni):
            print("No se puede dar de baja al cliente porque tiene cuentas corrientes activas.")
            return
        
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

def show_customers(mysql_customer):
    cursor = mysql_customer.connection.cursor()
    try:
        cursor.execute("""
            SELECT dni, nombre, apellido, telefono, direccion, activo
            FROM customer
            ORDER BY nombre, apellido
        """)
        customers = cursor.fetchall()

        print("================================ LISTADO DE CLIENTES ================================")
        print("-------------------------------------------------------------------------------------")
        print(" DNI       | Nombre               | Teléfono  | Dirección                | Estado  ")
        print("-------------------------------------------------------------------------------------")

        for customer in customers:
            dni, name, lastname, phone, address, active = customer
            status = "Activa" if active else "Inactiva"
            full_name = f"{name} {lastname}"
            print(f" {dni:<9} | {full_name:<20} | {phone:<9} | {address:<24} | {status:<7}")
        print()
    
    except Exception as e:
        print(f"Error al consultar los clientes: {e}")
    finally:
        cursor.close()