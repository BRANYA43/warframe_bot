from data import *
from validators.validators import *
from .base import Base
from .timer import Timer
from translater import get_text as _


class Cycle(Base):
    def __init__(self, name: str, timer: Timer, cycles: list['str'], current_cycle: str):
        super().__init__(name, timer)
        self.cycles = cycles
        self.current_cycle = current_cycle

    @property
    def cycles(self) -> list[str]:
        return self._cycles

    @cycles.setter
    def cycles(self, value: list[str]):
        validate_type(value, list, 'cycles')
        if len(value) < 2:
            raise ValueError('cycles cannot have less 2 items.')
        if any(not isinstance(item, str) for item in value):
            raise TypeError('items of cycles must be str.')
        if any(item == '' for item in value):
            raise ValueError('items of cycles cannot be empty string.')
        self._cycles = value

    @property
    def current_cycle(self) -> str:
        return self._current_cycle

    @current_cycle.setter
    def current_cycle(self, value):
        validate_type(value, str, 'current_cycle')
        validate_not_empty_string(value, 'current_cycle')
        if not value in self.cycles:
            raise ValueError('current_cycle must be within in cycles.')
        self._current_cycle = value
        self._set_next_cycle()

    @property
    def next_cycle(self):
        return self._next_cycle

    def _set_next_cycle(self):
        index = self.cycles.index(self._current_cycle)
        self._next_cycle = self.cycles[(index + 1) % len(self.cycles)]

    def get_info(self):
        ret = _('Name: {}\n').format(LOCATIONS[self.name]) + \
              _('Current cycle: {}\n').format(CYCLES[self.current_cycle]) + \
              _('Next cycle: {}\n').format(CYCLES[self.next_cycle]) + \
              _('Left time: {}\n').format(self.timer.get_str_time())
        return ret
