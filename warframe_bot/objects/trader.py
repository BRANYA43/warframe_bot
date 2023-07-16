import datetime

from .base import Base
from .inventory import Inventory


class Trader(Base):
    """Trader"""

    def __init__(self, key: str, name: str, expiry: datetime.datetime, inventory: Inventory = None):
        super().__init__(key, name, expiry)
        if inventory is not None:
            self.inventory = inventory
        else:
            self.inventory = Inventory()

    @property
    def inventory(self):
        return self._inventory

    @inventory.setter
    def inventory(self, value):
        self.check_instance(value, Inventory, 'inventory')
        self._inventory = value
