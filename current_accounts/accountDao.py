from __future__ import annotations
from abc import ABC, abstractmethod

class AccountDAO(ABC):

    @abstractmethod
    def open_account(self, account_number: int):
        pass

    @abstractmethod
    def close_account(self, account_number: int):
        pass

    @abstractmethod
    def is_account_active(self, account_number: int):
        pass

    @abstractmethod
    def deposit(self, amount: float):
        pass

    @abstractmethod
    def withdraw(self, amount: float):
        pass

    @abstractmethod
    def get_balance(self, account_number: int):
        pass

    @abstractmethod
    def transfer_to(self, target_account, amount: float):
        pass
