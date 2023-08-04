from datetime import datetime

from objects.mixins import TimerMixin, NameMixin
from validators import validate_type, validate_types


class Item(NameMixin):
    """Item of inventory"""

    def __init__(self, name: str, cost: int):
        super().__init__(name)

        self._set_cost(cost)

    @property
    def cost(self):
        return self._cost

    def _set_cost(self, value: int):
        validate_type(value, int)
        if value < 0:
            raise ValueError('Cost cannot be less 0.')
        self._cost = value


class Inventory:
    """Inventory"""

    def __init__(self, items: list[Item] | tuple[Item] = None):
        if items is None:
            items = []
        self.items = items

    @property
    def items(self) -> list[Item] | tuple[Item]:
        return self._items.copy()

    @items.setter
    def items(self, value: list | tuple):
        validate_types(value, list | tuple)
        if any(not isinstance(item, Item) for item in value):
            raise TypeError('Each item of items must be Item type.')
        self._items = value


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
