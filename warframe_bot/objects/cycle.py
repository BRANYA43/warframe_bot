import datetime

from warframe_bot.objects.base import Base


class Cycle(Base):
    def __init__(self, name: str, title: str, expiry: datetime.datetime, cycles: list['str'], current_cycle: str):
        super().__init__(name, title, expiry)
        self.cycles = cycles
        self.current_cycle = current_cycle

    @property
    def cycles(self) -> list[str]:
        return self._cycles

    @cycles.setter
    def cycles(self, value: list[str]):
        if not isinstance(value, list):
            raise TypeError('Cycles must be list.')
        if len(value) < 2:
            raise ValueError('Cycles cannot have less 2 items.')
        if any(not isinstance(item, str) for item in value):
            raise TypeError('Items of cycles must be str.')
        if any(item == '' for item in value):
            raise ValueError('Items of cycles cannot be empty string.')
        self._cycles = value

    @property
    def current_cycle(self) -> str:
        return self._current_cycle

    @current_cycle.setter
    def current_cycle(self, value):
        if not isinstance(value, str):
            raise TypeError('Current cycle must be str.')
        if value == '':
            raise ValueError('Current cycle cannot be empty string.')
        if not value in self.cycles:
            raise ValueError('Current cycle must be in list of cycles.')
        self._current_cycle = value
        self._set_next_cycle()

    @property
    def next_cycle(self):
        return self._next_cycle

    def _set_next_cycle(self):
        index = self.cycles.index(self._current_cycle)
        self._next_cycle = self.cycles[(index + 1) % len(self.cycles)]
