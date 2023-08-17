from datetime import datetime

import data
from objects import Mission
from objects.mixins import TimerMixin
from validators import validate_is_not_empty_string, validate_type


class Fissure(Mission, TimerMixin):
    """Fissure"""

    def __init__(self, id: str, name: str, location: str, type: str, enemy: str, tier: str, expiry: datetime,
                 is_storm=False, is_hard=False):
        Mission.__init__(self, name, location, type, enemy)
        TimerMixin.__init__(self, expiry)

        validate_is_not_empty_string(id)
        self._id = id

        validate_is_not_empty_string(tier)
        if tier not in data.TIERS:
            raise ValueError('No such a tier in tiers data.')
        self._tier = data.TIERS.index(tier)

        if is_storm and is_hard:
            raise ValueError('Only one optional attr can be True.')

        validate_type(is_storm, bool)
        self._is_storm = is_storm

        validate_type(is_hard, bool)
        self._is_hard = is_hard

        self._active = True

    @property
    def id(self) -> str:
        return self._id

    @property
    def tier(self) -> str:
        return data.TIERS[self._tier]

    @property
    def active(self) -> bool:
        return self._active

    @property
    def is_storm(self) -> bool:
        return self._is_storm

    @property
    def is_hard(self) -> bool:
        return self._is_hard

    def update(self):
        if self.timer.total_seconds == 0:
            self._active = False

    def get_info(self):
        return (
            f'Node: {self.name}',
            f'Location: {self.location}',
            f'Type: {self.type}',
            f'Enemy: {self.enemy}',
            f'Tier: {self.tier}',
            f'Left time: {self.timer.get_str_time()}',
        )