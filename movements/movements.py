from datetime import datetime
from typeguard import typechecked
from typing import Optional

@typechecked
class Movements:

    def __init__(self, number_account: int, amount: float, movement_type: str, transfer_account: Optional[int] = None, description: str = "Sin concepto"):
        self._number_account = number_account
        self._amount = amount
        self._timestamp = datetime.now()
        self._movement_type = movement_type
        self._transfer_account = transfer_account
        self._description = description