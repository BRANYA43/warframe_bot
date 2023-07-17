from objects.timer import Timer
from validators.validators import *


class NameMixin:
    def __init__(self, name: str):
        self.name = name

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value):
        validate_type(value, str, 'name')
        validate_not_empty_string(value, 'name')
        self._name = value


class TimerMixin:
    def __init__(self, timer: Timer):
        self.timer = timer

    @property
    def timer(self) -> Timer:
        return self._timer

    @timer.setter
    def timer(self, value):
        validate_type(value, Timer, 'timer')
        self._timer = value
