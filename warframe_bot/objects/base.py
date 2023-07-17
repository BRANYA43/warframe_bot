from abc import ABC, abstractmethod

from objects.mixins import CheckMixin


class Base(CheckMixin, ABC):
    def __init__(self, name: str, left_time: datetime.datetime):
        self.name = name
        self.left_time = left_time

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value):
        self.check_instance(value, str, 'name')
        self.check_empty_string(value, 'name')
        self._name = value

    @property
    def left_time(self) -> datetime.datetime:
        return self._left_time

    @left_time.setter
    def left_time(self, value):
        self.check_instance(value, str, 'left_time')
        self.check_empty_string(value, 'left_time')
        self._left_time = value

    @abstractmethod
    def get_info(self):
        raise NotImplementedError
