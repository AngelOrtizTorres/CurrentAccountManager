from __future__ import annotations
from abc import ABC, abstractmethod

class CustomerDAO(ABC):

    @abstractmethod
    def add_customer(self, customer):
        pass

    @abstractmethod
    def update_customer(self, customer):
        pass

    @abstractmethod
    def get_customer(self, dni):
        pass

    @abstractmethod
    def release(self, dni):
        pass

    @abstractmethod
    def deregister(self, dni):
        pass