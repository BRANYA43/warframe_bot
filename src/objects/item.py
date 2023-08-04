from objects.mixins import NameMixin
from validators import validate_type


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
