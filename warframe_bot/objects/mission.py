from objects.base import Base
from objects.mixins import NameMixin
from objects.timer import Timer
from validators.validators import *


class Mission(NameMixin):
    """Mission"""

    LOCATIONS = (
        'Mercury',
        'Venus',
        'Earth',
        'Mars',
        'Phobos',
        'Deimos',
        'Ceres',
        'Jupiter',
        'Europa',
        'Saturn',
        'Uranus',
        'Neptune',
        'Pluto',
        'Pluto',
        'Sedna',
        'Eris',
        'Void',
        'Lua',
        'Kuva Fortress',
        'Earth Proxima',
        'Venus Proxima',
        'Saturn Proxima',
        'Neptune Proxima',
        'Pluto Proxima',
        'Veil Proxima',
    )
    ENEMIES = (
        'Corpus',
        'Grineer',
        'Orokin',
    )

    TYPES = (
        'Capture',
        'Defence',
        'Disruption',
        'Excavation',
        'Extermination',
        'Interception',
        'Mobile Defence',
        'Rescue',
        'Sabotage',
        'Skirmish',
        'Spy',
        'Survival',
        'Volatile',
    )

    def __init__(self, name: str, location: str, enemy: str, type_: str):
        super().__init__(name)
        self.location = location
        self.enemy = enemy
        self.type = type_

    @property
    def location(self) -> str:
        return self.LOCATIONS[self._location]

    @location.setter
    def location(self, value: str):
        validate_type(value, str, 'location')
        validate_not_empty_string(value, 'location')
        self._location = self.LOCATIONS.index(value)

    @property
    def enemy(self) -> str:
        return self.ENEMIES[self._enemy]

    @enemy.setter
    def enemy(self, value: str):
        validate_type(value, str, 'enemy')
        validate_not_empty_string(value, 'enemy')
        self._enemy = self.ENEMIES.index(value)

    @property
    def type(self) -> str:
        return self.TYPES[self._type]

    @type.setter
    def type(self, value: str):
        validate_type(value, str, 'type')
        validate_not_empty_string(value, 'type')
        self._type = self.TYPES.index(value)

    def get_info(self):
        return f'Type: {self.type}\n' \
               f'Location: {self.location}\n' \
               f'Name: {self.name}\n'