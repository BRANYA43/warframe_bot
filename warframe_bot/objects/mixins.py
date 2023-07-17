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
