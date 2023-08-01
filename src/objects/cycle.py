from datetime import timedelta

from validators import validate_type
from .mixins import NameMixin


class Cycle(NameMixin):
    """Cycle"""

    def __init__(self, name: str, duration: timedelta):
        super().__init__(name)
        self._set_duration(duration)

    @property
    def duration(self) -> timedelta:
        return self._duration

    def _set_duration(self, value: timedelta):
        validate_type(value, timedelta)
        if value.total_seconds() < 60:
            raise ValueError('Duration cannot be less 1 minute.')
        self._duration = value
