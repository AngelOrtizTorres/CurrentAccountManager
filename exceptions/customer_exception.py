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