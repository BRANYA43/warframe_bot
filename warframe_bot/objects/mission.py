from data import *
from objects.mixins import NameMixin
from validators.validators import *
from translater import get_text as _


class Mission(NameMixin):
    """Mission"""

    locations = list(LOCATIONS.keys())
    enemies = list(ENEMIES.keys())
    types = list(TYPES.keys())

    def __init__(self, name: str, location: str, enemy: str, type: str, is_storm: bool, is_hard: bool):
        super().__init__(name)
        self.location = location
        self.enemy = enemy
        self.type = type
        self.is_storm = is_storm
        self.is_hard = is_hard

    @property
    def location(self) -> str:
        return self.locations[self._location]

    @location.setter
    def location(self, value: str):
        validate_type(value, str, 'location')
        validate_not_empty_string(value, 'location')
        try:
            self._location = self.locations.index(value)
        except ValueError:  # TODO fix it. When value isn't within LOCATIONS
            self.locations.append(value)
            self._location = self.locations.index(value)
            print('Location:', value)

    @property
    def enemy(self) -> str:
        return self.enemies[self._enemy]

    @enemy.setter
    def enemy(self, value: str):
        validate_type(value, str, 'enemy')
        validate_not_empty_string(value, 'enemy')
        try:
            self._enemy = self.enemies.index(value)
        except ValueError:  # TODO fix it. When value isn't within ENEMIES
            self.enemies.append(value)
            self._enemy = self.enemies.index(value)
            print('Enemy:', value)

    @property
    def type(self) -> str:
        return self.types[self._type]

    @type.setter
    def type(self, value: str):
        validate_type(value, str, 'type')
        validate_not_empty_string(value, 'type')
        try:
            self._type = self.types.index(value)
        except ValueError:  # TODO fix it. When value isn't within TYPES
            self.types.append(value)
            self._type = self.types.index(value)
            print('Type:', value)

    @property
    def is_storm(self) -> bool:
        return self._is_storm

    @is_storm.setter
    def is_storm(self, value: bool):
        validate_type(value, bool, 'is_storm')
        self._is_storm = value

    @property
    def is_hard(self) -> bool:
        return self._is_hard

    @is_hard.setter
    def is_hard(self, value: bool):
        validate_type(value, bool, 'is_hard')
        self._is_hard = value

    def get_info(self):
        ret = _('Name: {}\n').format(self.name) + \
              _('Type: {}\n').format(TYPES[self.type]) + \
              _('Location: {}\n').format(LOCATIONS[self.location])

        return ret
