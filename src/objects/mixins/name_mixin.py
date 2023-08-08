from validators import validate_is_not_empty_string


class NameMixin:
    """Name Mixin"""

    def __init__(self, name: str):
        validate_is_not_empty_string(name)
        self._name = name

    @property
    def name(self) -> str:
        return self._name
