from types import UnionType


def validate_type(value, type_, attr_name: str):
    if not isinstance(value, type_):
        raise TypeError(f'{attr_name} must be {type_.__name__}.')


def validate_several_type(value, types_: UnionType, attr_name: str):
    if not isinstance(value, types_):
        raise TypeError(f'{attr_name} must be {str(types_).replace("|", "or")}')


def validate_not_empty_string(value, attr_name: str):
    if value == '':
        raise ValueError(f'{attr_name} cannot be empty string.')


def validate_not_negative(value, attr_name: str):
    if value < 0:
        raise ValueError(f'{attr_name} cannot be negative.')
