from datetime import datetime

from locales import local_data
from objects import Cycle
from objects.mixins import TimerMixin, NameMixin
from validators import validate_type, validate_is_not_empty_string
from utils.translater import get_text as _


class Place(NameMixin, TimerMixin):
    """Place"""

    def __init__(self, name: str, expiry: datetime, cycles: tuple[Cycle], current_cycle: str):
        NameMixin.__init__(self, name)
        self._cycles = None
        self._current_cycle = None
        self._next_cycle = None

        self._set_cycles(cycles)
        self._set_current_cycle_for_init(current_cycle)
        self._set_next_cycle()

        if expiry < datetime.utcnow():
            expiry += self._cycles[self._next_cycle].duration
        TimerMixin.__init__(self, expiry)

    @property
    def current_cycle(self) -> str:
        return self._cycles[self._current_cycle].name

    @property
    def next_cycle(self) -> str:
        return self._cycles[self._next_cycle].name

    def _set_cycles(self, value: tuple[Cycle]):
        validate_type(value, tuple)
        if len(value) < 2:
            raise ValueError('Cycles must have 2 items minimal.')
        if any(not isinstance(cycle, Cycle) for cycle in value):
            raise TypeError('Each item in cycles tuple must be Cycle.')
        self._cycles = value

    def _set_current_cycle_for_init(self, value: str):
        validate_is_not_empty_string(value)
        for i, cycle in enumerate(self._cycles):
            if value == cycle.name:
                self._current_cycle = i
                return
        raise ValueError('Current cycle must be name of Cycle from cycles tuple.')

    def _set_current_cycle(self):
        self._current_cycle = (self._current_cycle + 1) % len(self._cycles)

    def _set_next_cycle(self):
        self._next_cycle = (self._current_cycle + 1) % len(self._cycles)

    def update(self):
        if self.timer.total_seconds == 0:
            self.timer.expiry += self._cycles[self._next_cycle].duration
            self._set_current_cycle()
            self._set_next_cycle()

    def get_info(self) -> tuple[str, ...]:
        return (
            _('Name: {}').format(local_data.PLACES[self.name]),
            _('Current cycle: {}').format(local_data.CYCLES[self.current_cycle]),
            _('Next cycle: {}').format(local_data.CYCLES[self.next_cycle]),
            _('Left time: {}').format(self.timer.get_str_time()),
        )
