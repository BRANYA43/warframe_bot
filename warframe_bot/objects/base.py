from abc import ABC, abstractmethod

from objects.mixins import CheckMixin
from objects.timer import Timer


class Base(CheckMixin, ABC):
    def __init__(self, name: str, timer: Timer):
        self.name = name
        self.timer = timer

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value):
        self.check_instance(value, str, 'name')
        self.check_empty_string(value, 'name')
        self._name = value

    @property
    def timer(self) -> Timer:
        return self._timer

    @timer.setter
    def timer(self, value):
        self.check_instance(value, Timer, 'timer')
        self._timer = value

    @abstractmethod
    def get_info(self):
        raise NotImplementedError
