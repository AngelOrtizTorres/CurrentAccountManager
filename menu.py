class Menu:

    def __init__(self, *options, title="Menú de opciones"):
        self.__options = list(options)
        self.__title = title

    def choose(self):
        self.__print_menu()
        return self.__chosen_option()

    def __print_menu(self):
        print(self.__title)
        print()
        for n in range(len(self.__options)):
            print(f"{n + 1}. {self.__options[n]}")

    def __chosen_option(self):
        while True:
            try:
                option = int(input(f"\nIntroduce una opción (1 - {len(self.__options)}): "))
                if 1 <= option <= len(self.__options):
                    return option
                else:
                    print(f"Introduce un número entre 1 y {len(self.__options)}")
            except ValueError:
                print("Has introducido una opción incorrecta.")

main_menu = Menu("Gestionar Clientes", "Gestionar Cuentas Corrientes", "Operaciones en una Cuenta Corriente", "Salir", 
                 title = "Gestión de Cuentas Bancarias")

customer_menu = Menu("Añadir cliente", "Reactivar un cliente", "Dar de baja un cliente", "Modificar datos de cliente", 
                     "Ver todos los clientes", "Volver al menú principal", title = "Gestión de Clientes")

account_menu = Menu("Crear cuenta corriente", "Reabrir cuenta corriente", "Cerrar cuenta corriente", "Ver ingresos", "Ver salidas", 
                    "Ver transferencias", "Ver todas las cuentas corrientes", "Volver al menú principal", 
                    title = "Gestión de Cuentas Corrientes")

movements_menu = Menu("Consultar saldo", "Ver movimientos entre fechas", "Ingresar dinero", "Retirar dinero", 
                      "Hacer transferencia", "Volver al menú principal", title = "Gestión de movimientos")