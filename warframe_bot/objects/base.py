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
    def __init__(self, id: str, title: str, expiry: datetime.datetime):
        self.id = id
        self.title = title
        self.expiry = expiry

    @property
    def id(self) -> str:
        return self._name

    @id.setter
    def id(self, value: str):
        self.check_instance(value, str, 'Name')
        self.check_empty_string(value, 'Name')
        self._name = value

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value):
        self.check_instance(value, str, 'Title')
        self.check_empty_string(value, 'Title')
        self._title = value

    @property
    def expiry(self) -> datetime.datetime:
        return self._expiry

    @expiry.setter
    def expiry(self, value):
        self.check_instance(value, datetime.datetime, 'Expiry')
        self._expiry = value
