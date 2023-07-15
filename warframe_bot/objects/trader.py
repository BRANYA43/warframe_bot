import datetime

from warframe_bot.objects.base import Base
from warframe_bot.objects.inventory import Inventory


class Trader(Base):
    """Trader"""

    def __init__(self, name: str, title: str, expiry: datetime.datetime, inventory: Inventory):
        super().__init__(name, title, expiry)
        self.inventory = inventory

    @property
    def inventory(self):
        return self._inventory

    @inventory.setter
    def inventory(self, value):
        self.check_instance(value, Inventory, 'Inventory')
        self._inventory = value
