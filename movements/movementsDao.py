from __future__ import annotations
from abc import ABC, abstractmethod

class MovementsDAO(ABC):

    @abstractmethod
    def create_movement(self, movement):
        pass

    @abstractmethod
    def get_deposit(self):
        pass

    @abstractmethod
    def get_withdraw(self):
        pass

    @abstractmethod
    def get_transfer(self):
        pass

    @abstractmethod
    def get_movements_between_date(self):
        pass