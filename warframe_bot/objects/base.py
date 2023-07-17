from abc import ABC, abstractmethod

from objects.mixins import NameMixin, TimerMixin
from objects.timer import Timer


class Base(ABC, NameMixin, TimerMixin):
    def __init__(self, name: str, timer: Timer):
        NameMixin.__init__(self, name)
        TimerMixin.__init__(self, timer)

    @abstractmethod
    def get_info(self):
        raise NotImplementedError
