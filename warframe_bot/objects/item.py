from .base import CheckMixin


class Item(CheckMixin):
    """Item of Inventory"""

    def __init__(self, name: str, cost: int):
        self.name = name
        self.cost = cost

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self.check_instance(value, str, 'name')
        self.check_empty_string(value, 'name')
        self._name = value

    @property
    def cost(self):
        return self._cost

    @cost.setter
    def cost(self, value):
        self.check_instance(value, int, 'cost')
        if value < 0:
            raise ValueError('cost cannot be negative.')
        self._cost = value
