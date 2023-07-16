from .base import CheckMixin


class Item(CheckMixin):
    """Item of Inventory"""

    def __init__(self, title: str, cost: int):
        self.title = title
        self.cost = cost

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self.check_instance(value, str, 'Title')
        self.check_empty_string(value, 'Title')
        self._title = value

    @property
    def cost(self):
        return self._cost

    @cost.setter
    def cost(self, value):
        self.check_instance(value, int, 'Cost')
        if value < 0:
            raise ValueError('Cost cannot be negative.')
        self._cost = value
