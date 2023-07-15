import datetime


class Base:
    def __init__(self, name: str, title: str, expiry: datetime.datetime):
        self.name = name
        self.title = title
        self.expiry = expiry

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if not isinstance(value, str):
            raise TypeError('Name must be str.')
        if value == '':
            raise ValueError('Name cannot be empty string.')
        self._name = value

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value):
        if not isinstance(value, str):
            raise TypeError('Title must be str.')
        if value == '':
            raise ValueError('Title cannot be empty string.')
        self._title = value

    @property
    def expiry(self) -> datetime.datetime:
        return self._expiry

    @expiry.setter
    def expiry(self, value):
        if not isinstance(value, datetime.datetime):
            raise TypeError('Expiry must be datetime.')
        self._expiry = value
