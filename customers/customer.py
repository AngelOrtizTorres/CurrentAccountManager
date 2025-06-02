from typeguard import typechecked
import re
from utils.customer_exception import *

@typechecked
class Customer:

    def __init__(self, dni: str, name: str, lastname: str, phone: str, address: str, active: bool = True):
        self._dni = dni
        self.name = name
        self.lastname = lastname
        self.phone = phone
        self.address = address
        self.active = active

    @staticmethod
    def _validate_format_dni(dni: str):
        expression = r'^\d{8}[A-HJ-NP-TV-Z]$'
        try:
            re.match(expression, dni)
            Customer._validate_letter(dni)
        except:
            raise FormatErrorDNI()

    @staticmethod
    def _validate_letter(dni: str):
        letters_valors = "TRWAGMYFPDXBNJZSQVHLCKE"
        dni_numbers = dni[:8]
        
        number = int(dni_numbers) % 23
        if dni[8].upper() != letters_valors[number]:
            raise LetterErrorDNI()

    @staticmethod
    def _validate_phone(phone: str):
        if len(phone) != 9 or phone[0] not in '679':
            raise FormatErrorPhone()
