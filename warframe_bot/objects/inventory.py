from warframe_bot.objects.base import CheckMixin
from warframe_bot.objects.item import Item


class Inventory(CheckMixin):
    """Inventory for Item"""

    def __init__(self, items: list[Item] = None):
        self.items = items

    @property
    def items(self):
        return self._items

    @items.setter
    def items(self, value: list[Item] | None):
        self.check_instance(value, list | None, 'Items')
        if value is not None:
            if len(value) == 0:
                raise ValueError('Items cannot be empty.')
            if any(not isinstance(item, Item) for item in value):
                raise TypeError('Items of items must be Item.')
        self._items = value