import data
from objects.mixins import NameMixin
from validators import validate_is_not_empty_string


class Mission(NameMixin):
    """Mission"""

    def __init__(self, name: str, location: str, type: str, enemy: str):
        super().__init__(name)
        validate_is_not_empty_string(location)
        if location not in data.LOCATIONS:
            raise ValueError('No such a location in locations data.')
        self._location = data.LOCATIONS.index(location)

        validate_is_not_empty_string(type)
        if type not in data.TYPES:
            raise ValueError('No such a type in types data.')
        self._type = data.TYPES.index(type)

        validate_is_not_empty_string(enemy)
        if enemy not in data.ENEMIES:
            raise ValueError('No such a enemy in enemies data.')
        self._enemy = data.ENEMIES.index(enemy)

    @property
    def location(self) -> str:
        return data.LOCATIONS[self._location]

    @property
    def type(self) -> str:
        return data.TYPES[self._type]

    @property
    def enemy(self) -> str:
        return data.ENEMIES[self._enemy]
