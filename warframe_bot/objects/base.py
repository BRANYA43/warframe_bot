import datetime
from abc import ABC, abstractmethod
from types import UnionType


class CheckMixin:
    @staticmethod
    def check_instance(value, type_, attr_name: str):
        if not isinstance(value, type_):
            raise TypeError(f'{attr_name} must be '
                            f'{type_.__name__ if type(type_) is not UnionType else str(type_).replace("|", "or")}.')

    @staticmethod
    def check_empty_string(value, attr_name: str):
        if value == '':
            raise ValueError(f'{attr_name} cannot be empty string.')
        
    @staticmethod
    def check_negative(value, attr_name: str):
        if value < 0:
            raise ValueError(f'{attr_name} cannot be negative.')


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
