from datetime import datetime

from objects import Inventory
from objects.mixins import TimerMixin, NameMixin
from validators import validate_type


class Trader(NameMixin, TimerMixin):
    """Trader"""

    def __init__(self, name: str, expiry: datetime, inventory: Inventory, *, active=False):
        NameMixin.__init__(self, name)
        TimerMixin.__init__(self, expiry)
        validate_type(inventory, Inventory)
        self._inventory = inventory
        self.active = active

    @property
    def inventory(self) -> Inventory:
        return self._inventory

    @property
    def active(self) -> bool:
        return self._active

    @active.setter
    def active(self, value: bool):
        validate_type(value, bool)
        self._active = value

