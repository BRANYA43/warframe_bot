from objects.mixins import NameMixin
from validators.validators import *


class Mission(NameMixin):
    """Mission"""

    LOCATIONS = [
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
    ]
    ENEMIES = [
        'Corpus',
        'Grineer',
        'Orokin',
        'Infested',
        'Crossfire',
    ]

    TYPES = [
        'Assault',
        'Capture',
        'Defense',
        'Disruption',
        'Excavation',
        'Extermination',
        'Interception',
        'Mobile Defense',
        'Rescue',
        'Sabotage',
        'Skirmish',
        'Spy',
        'Survival',
        'Volatile',
        'Orphix',
    ]

    def __init__(self, name: str, location: str, enemy: str, type: str, is_storm: bool, is_hard: bool):
        super().__init__(name)
        self.location = location
        self.enemy = enemy
        self.type = type
        self.is_storm = is_storm
        self.is_hard = is_hard

    @property
    def location(self) -> str:
        return self.LOCATIONS[self._location]

    @location.setter
    def location(self, value: str):
        validate_type(value, str, 'location')
        validate_not_empty_string(value, 'location')
        try:
            self._location = self.LOCATIONS.index(value)
        except ValueError:  # TODO fix it. When value isn't within LOCATIONS
            self.LOCATIONS.append(value)
            self._location = self.LOCATIONS.index(value)
            print('Location:', value)

    @property
    def enemy(self) -> str:
        return self.ENEMIES[self._enemy]

    @enemy.setter
    def enemy(self, value: str):
        validate_type(value, str, 'enemy')
        validate_not_empty_string(value, 'enemy')
        try:
            self._enemy = self.ENEMIES.index(value)
        except ValueError:  # TODO fix it. When value isn't within ENEMIES
            self.ENEMIES.append(value)
            self._enemy = self.ENEMIES.index(value)
            print('Enemy:', value)

    @property
    def type(self) -> str:
        return self.TYPES[self._type]

    @type.setter
    def type(self, value: str):
        validate_type(value, str, 'type')
        validate_not_empty_string(value, 'type')
        try:
            self._type = self.TYPES.index(value)
        except ValueError:  # TODO fix it. When value isn't within TYPES
            self.TYPES.append(value)
            self._type = self.TYPES.index(value)
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
        ret = ''
        ret += f'Type: {self.type}\n' \
               f'Location: {self.location}\n' \
               f'Name: {self.name}\n'
        return ret
