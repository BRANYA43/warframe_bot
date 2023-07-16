import datetime
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


class Base(CheckMixin):
    def __init__(self, key: str, name: str, expiry: datetime.datetime):
        self.key = key
        self.name = name
        self.expiry = expiry

    @property
    def key(self) -> str:
        return self._key

    @key.setter
    def key(self, value: str):
        self.check_instance(value, str, 'key')
        self.check_empty_string(value, 'key')
        self._key = value

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value):
        self.check_instance(value, str, 'name')
        self.check_empty_string(value, 'name')
        self._name = value

    @property
    def expiry(self) -> datetime.datetime:
        return self._expiry

    @expiry.setter
    def expiry(self, value):
        self.check_instance(value, datetime.datetime, 'expiry')
        self._expiry = value
