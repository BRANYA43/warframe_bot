import datetime

from .base import Base
from .inventory import Inventory


class Trader(Base):
    """Trader"""

    def __init__(self, key: str, name: str, expiry: datetime.datetime, inventory: Inventory):
        super().__init__(key, name, expiry)
        self.inventory = inventory

    @property
    def inventory(self):
        return self._inventory

    @inventory.setter
    def inventory(self, value):
        self.check_instance(value, Inventory, 'inventory')
        self._inventory = value
