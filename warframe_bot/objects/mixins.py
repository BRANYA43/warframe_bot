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