from abc import ABC, abstractmethod

from objects.mixins import NameMixin
from objects.timer import Timer
from validators.validators import *


class Base(ABC, NameMixin):
    def __init__(self, name: str, timer: Timer):
        super().__init__(name)
        self.timer = timer

    @property
    def timer(self) -> Timer:
        return self._timer

    @timer.setter
    def timer(self, value):
        validate_type(value, Timer, 'timer')
        self._timer = value

    @abstractmethod
    def get_info(self):
        raise NotImplementedError
