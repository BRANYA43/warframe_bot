from objects import Item
from validators import validate_types


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

