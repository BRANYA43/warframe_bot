from datetime import datetime

from objects.mixins import TimerMixin, NameMixin
from validators import validate_type, validate_types, validate_is_not_empty_string, validate_is_not_negative_number


class Item(NameMixin):
    """Item of inventory"""

    def __init__(self, name: str, cost: int):
        super().__init__(name)

        validate_type(cost, int)
        if cost < 0:
            raise ValueError('Cost cannot be less 0.')
        self._cost = cost

    @property
    def cost(self):
        return self._cost

    def get_info(self) -> tuple[str, ...]:
        return (
            f'Name: {self.name}',
            f'Cost: {self.cost}',
        )


class Inventory:
    """Inventory"""

    def __init__(self):
        self._items = []

    @property
    def items(self) -> list[Item]:
        return self._items.copy()

    def add_item(self, item: Item):
        validate_type(item, Item)
        self._items.append(item)

    def add_item_from_values(self, name: str, cost: int):
        item = Item(name, cost)
        self._items.append(item)

    def add_items(self, items: list[Item, ...]):
        validate_type(items, list)
        self._items += items

    def add_items_from_values(self, items_values: list[tuple[str, int]]):
        validate_type(items_values, list)
        items = [Item(*values) for values in items_values]
        self._items += items

    def clear(self):
        self._items.clear()

    def get_info(self) -> tuple[tuple[str, ...]]:
        return tuple([item.get_info() for item in self.items])


class Trader(NameMixin, TimerMixin):
    """Trader"""

    def __init__(self, name: str, expiry: datetime):
        NameMixin.__init__(self, name)
        TimerMixin.__init__(self, expiry)
        self._inventory = Inventory()

    @property
    def inventory(self) -> Inventory:
        return self._inventory

    def get_info(self) -> tuple[str, ...]:
        return (
            f'Name: {self.name}',
            f'Left Time: {self.timer.get_str_time()}',
        )
