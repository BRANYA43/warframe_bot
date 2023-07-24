from data import TIERS
from objects.mission import Mission
from objects.mixins import TimerMixin
from objects.timer import Timer
from validators.validators import *
from translater import get_text as _


class Fissure(TimerMixin):
    """Fissure"""

    tiers = list(TIERS.keys())

    def __init__(self, id: str, timer: Timer, mission: Mission, tier: str):
        super().__init__(timer)
        self._id: str
        self._mission: Mission
        self._tier: int

        self._set_id(id)
        self._set_mission(mission)
        self._set_tier(tier)

    @property
    def id(self) -> str:
        return self._id

    def _set_id(self, value: str):
        validate_type(value, str, 'id')
        validate_not_empty_string(value, 'id')
        self._id = value

    @property
    def mission(self) -> Mission:
        return self._mission

    def _set_mission(self, value: Mission):
        validate_type(value, Mission, 'mission')
        self._mission = value

    @property
    def tier(self) -> str:
        return self.tiers[self._tier]

    def _set_tier(self, value: str):
        validate_type(value, str, 'tier')
        validate_not_empty_string(value, 'tier')
        self._tier = self.tiers.index(value)

    def get_info(self):
        ret = f'{self._mission.get_info()}' + \
              _('Relic Tier: {}\n').format(TIERS[self.tier]) + \
              _('Left time: {}\n').format(self.timer.get_str_time())
        return ret
