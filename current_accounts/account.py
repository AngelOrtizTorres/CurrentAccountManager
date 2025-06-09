from customers.customer import *
from exceptions.account_exception import *

class Account:
    _account_counter = 0

    def __init__(self, dni: str, balance: float, state: bool = True):
        self._account_number = self._create_number_account()
        self._balance = balance
        self._dni = dni
        self.state = state

    def _create_number_account(self):
        Account._account_counter += 1
        return Account._account_counter
    
    @staticmethod
    def _validate_balance(balance: float):
        if balance < 0:
            raise NegativeBalanceError()