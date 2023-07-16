import datetime

from .base import Base


class Cycle(Base):
    def __init__(self, key: str, name: str, expiry: datetime.datetime, cycles: list['str'], current_cycle: str):
        super().__init__(key, name, expiry)
        self.cycles = cycles
        self.current_cycle = current_cycle

    @property
    def cycles(self) -> list[str]:
        return self._cycles

    @cycles.setter
    def cycles(self, value: list[str]):
        if not isinstance(value, list):
            raise TypeError('cycles must be list.')
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
        self.check_instance(value, str, 'current_cycle')
        self.check_empty_string(value, 'current_cycle')
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
