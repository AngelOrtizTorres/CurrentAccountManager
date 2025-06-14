class ValidationException(Exception):
    pass

class FormatErrorDNI(ValidationException):
    def __init__(self):
        super().__init__("El DNI debe contener 8 dígitos y 1 letra")

class LetterErrorDNI(ValidationException):
    def __init__(self):
        super().__init__("La letra del DNI no es válida")

class FormatErrorPhone(ValidationException):
    def __init__(self):
        super().__init__("El número es incorrecto, debe contener 9 dígitos")

class DNINotFoundError(ValidationException):
    def __init__(self):
        super().__init__("El DNI no se ha encontrado")

class CustomerInactiveError(ValidationException):
    def __init__(self, *args):
        super().__init__("El cliente se encuentra inactivo en este momento")