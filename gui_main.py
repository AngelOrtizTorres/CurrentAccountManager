import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton,
    QFormLayout, QLineEdit, QMessageBox, QDialog, QInputDialog
)
from PySide6.QtCore import Qt
from customers.customer import Customer
from customers.customer_mysql import MySQLCustomerDAO
from exceptions.customer_exception import LetterErrorDNI, FormatErrorDNI, ValidationException


class CustomerDialog(QDialog):
    def __init__(self, parent = None, customer = None):
        super().__init__(parent)
        self.mysql_customer = MySQLCustomerDAO()
        self.customer = customer
        self.setWindowTitle("Añadir Cliente" if not customer else "Modificar Cliente")
        self.setup_customer_form()

    def setup_customer_form(self):
        layout = QFormLayout()

        self.dni_input = QLineEdit(self.customer.dni if self.customer else "")
        self.dni_input.setPlaceholderText("Ej: 12345678Z")
        layout.addRow("DNI:", self.dni_input)

        self.name_input = QLineEdit(self.customer.name if self.customer else "")
        layout.addRow("Nombre:", self.name_input)

        self.lastname_input = QLineEdit(self.customer.lastname if self.customer else "")
        layout.addRow("Apellido:", self.lastname_input)

        self.phone_input = QLineEdit(self.customer.phone if self.customer else "")
        self.phone_input.setPlaceholderText("Ej: 604395284")
        layout.addRow("Teléfono:", self.phone_input)

        self.address_input = QLineEdit(self.customer.address if self.customer else "")
        layout.addRow("Dirección:", self.address_input)

        if self.customer:
            self.dni_input.setDisabled(True)  # Desactivar edición de DNI en modo modificación

        save_button = QPushButton("Guardar")
        save_button.clicked.connect(self.save_customer)

        cancel_button = QPushButton("Cancelar")
        cancel_button.clicked.connect(self.reject)

        layout.addRow(save_button, cancel_button)
        self.setLayout(layout)

    def save_customer(self):
        try:
            dni = self.dni_input.text().strip()
            Customer._validate_format_dni(dni)

            name = self.name_input.text().strip()
            lastname = self.lastname_input.text().strip()
            phone = self.phone_input.text().strip()
            address = self.address_input.text().strip()

            if phone:
                Customer._validate_phone(phone)

            if self.customer:
                name = name or self.customer.name
                lastname = lastname or self.customer.lastname
                phone = phone or self.customer.phone
                address = address or self.customer.address

                self.mysql_customer.update_customer(name, lastname, phone, address, dni)
                QMessageBox.information(self, "Éxito", "Cliente actualizado correctamente.")
            else:
                if not all([dni, name, lastname, phone, address]):
                    QMessageBox.warning(self, "Error", "Por favor, complete todos los campos.")
                    return
                customer = Customer(dni, name, lastname, phone, address)
                self.mysql_customer.add_customer(customer)
                QMessageBox.information(self, "Éxito", "Cliente añadido correctamente.")

            self.accept()

        except (LetterErrorDNI, FormatErrorDNI, ValidationException) as e:
            QMessageBox.critical(self, "Error", f"Error: {str(e)}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error inesperado: {str(e)}")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Cuentas Bancarias")
        self.setMinimumSize(300, 400)
        self.mysql_customer = MySQLCustomerDAO()
        self.setup_main_window_ui()

    def setup_main_window_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        title = QPushButton("Gestión de Cuentas Bancarias")
        title.setEnabled(False)
        title.setStyleSheet("font-weight: bold; font-size: 16px; padding: 10px;")
        layout.addWidget(title)

        customer_button = QPushButton("Gestionar Clientes")
        customer_button.clicked.connect(self.show_customer_menu)
        layout.addWidget(customer_button)

        accounts_button = QPushButton("Gestionar Cuentas Corrientes")
        accounts_button.setEnabled(False)
        layout.addWidget(accounts_button)

        movements_button = QPushButton("Operaciones en una Cuenta Corriente")
        movements_button.setEnabled(False)
        layout.addWidget(movements_button)

        exit_button = QPushButton("Salir")
        exit_button.clicked.connect(self.close)
        layout.addWidget(exit_button)

        layout.addStretch()

    def show_customer_menu(self):
        customer_menu = QDialog(self)
        customer_menu.setWindowTitle("Gestión de Clientes")
        layout = QVBoxLayout()

        add_button = QPushButton("Añadir cliente")
        add_button.clicked.connect(self.add_customer)
        layout.addWidget(add_button)

        release_button = QPushButton("Reactivar un cliente")
        release_button.clicked.connect(self.release_customer)
        layout.addWidget(release_button)

        deregister_button = QPushButton("Dar de baja un cliente")
        deregister_button.clicked.connect(self.deregister_customer)
        layout.addWidget(deregister_button)

        update_button = QPushButton("Modificar datos de cliente")
        update_button.clicked.connect(self.update_customer)
        layout.addWidget(update_button)

        back_button = QPushButton("Volver al menú principal")
        back_button.clicked.connect(customer_menu.accept)
        layout.addWidget(back_button)

        layout.addStretch()
        customer_menu.setLayout(layout)
        customer_menu.exec()

    def add_customer(self):
        dialog = CustomerDialog(self)
        dialog.exec()

    def update_customer(self):
        dni, ok = QInputDialog.getText(self, "Modificar Cliente", "Ingresa el DNI del cliente a modificar:")
        if ok and dni.strip():
            try:
                dni = dni.strip()
                Customer._validate_format_dni(dni)

                customer = self.mysql_customer.get_customer(dni)
                if not customer:
                    QMessageBox.warning(self, "Error", "No se encontró ningún cliente con ese DNI.")
                    return

                if not customer.active:
                    QMessageBox.warning(self, "Error", "El cliente está dado de baja. Debe reactivarlo primero.")
                    return

                dialog = CustomerDialog(self, customer)
                dialog.exec()
            except (LetterErrorDNI, FormatErrorDNI) as e:
                QMessageBox.critical(self, "Error", f"Formato de DNI inválido: {str(e)}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al modificar el cliente: {str(e)}")

    def release_customer(self):
        dni, ok = QInputDialog.getText(self, "Reactivar Cliente", "Ingresa el DNI del cliente a reactivar:")
        if ok and dni:
            try:
                Customer._validate_format_dni(dni)
                customer = self.mysql_customer.get_customer(dni)
                if not customer:
                    QMessageBox.warning(self, "Error", "No se encontró ningún cliente con ese DNI.")
                    return
                self.mysql_customer.release(dni)
                QMessageBox.information(self, "Éxito", "Cliente reactivado correctamente.")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def deregister_customer(self):
        dni, ok = QInputDialog.getText(self, "Dar de Baja Cliente", "Ingresa el DNI del cliente a dar de baja:")
        if ok and dni:
            try:
                Customer._validate_format_dni(dni)
                customer = self.mysql_customer.get_customer(dni)
                if not customer:
                    QMessageBox.warning(self, "Error", "No se encontró ningún cliente con ese DNI.")
                    return
                self.mysql_customer.deregister(dni)
                QMessageBox.information(self, "Éxito", "Cliente dado de baja correctamente.")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
