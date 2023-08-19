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


class FissureStorage:
    """Fissure Storage"""

    def __init__(self):
        self._simple_fissures, \
            self._storm_fissures, \
            self._hard_fissures = ({tier.lower(): [] for tier in data.TIERS[:-1]} for i in range(3))
        self._kuva_fissures = []

    def add(self, fissure: Fissure):
        if not fissure.is_storm and not fissure.is_hard and fissure.tier != data.TIERS[-1]:
            self._simple_fissures[fissure.tier.lower()].append(fissure)
        elif fissure.is_storm and fissure.tier != data.TIERS[-1]:
            self._storm_fissures[fissure.tier.lower()].append(fissure)
        elif fissure.is_hard and fissure.tier != data.TIERS[-1]:
            self._hard_fissures[fissure.tier.lower()].append(fissure)
        elif fissure.tier == data.TIERS[4] and fissure.location == data.LOCATIONS[-8]:
            self._kuva_fissures.append(fissure)

    def get_all_fissure_list(self) -> list[Fissure, ...]:
        ret = []
        for key in self._simple_fissures.keys():
            ret += self._simple_fissures[key]
            ret += self._storm_fissures[key]
            ret += self._hard_fissures[key]
        ret += self._kuva_fissures
        return ret

    def get_all_ids(self) -> list[str, ...]:
        return [fissure.id for fissure in self.get_all_fissure_list()]

    def delete_fissure(self, fissure: Fissure):
        if not fissure.is_storm and not fissure.is_hard and fissure.tier != data.TIERS[-1]:
            self._simple_fissures[fissure.tier.lower()].remove(fissure)
        elif fissure.is_storm and fissure.tier != data.TIERS[-1]:
            self._storm_fissures[fissure.tier.lower()].remove(fissure)
        elif fissure.is_hard and fissure.tier != data.TIERS[-1]:
            self._hard_fissures[fissure.tier.lower()].remove(fissure)
        elif fissure.tier == data.TIERS[4] and fissure.location == data.LOCATIONS[-8]:
            self._kuva_fissures.remove(fissure)

    def get_fissures(self, type: str) -> dict[str: list[Fissure, ...], ...] | list[Fissure, ...]:
        match type:
            case 'simple':
                ret = self._simple_fissures
            case 'storm':
                ret = self._storm_fissures
            case 'hard':
                ret = self._hard_fissures
            case 'kuva':
                ret = self._kuva_fissures
            case _:
                raise NameError('Type can be only simple, storm, hard or kuva.')
        return ret
