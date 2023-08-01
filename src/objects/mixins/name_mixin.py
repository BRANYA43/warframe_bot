from validators import validate_is_not_empty_string


class NameMixin:
    """Name Mixin"""

    def __init__(self, name: str):
        self.name = name

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        validate_is_not_empty_string(value)
        self._name = value
