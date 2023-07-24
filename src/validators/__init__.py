def validate_type(value, type_):
    if not isinstance(value, type_):
        raise TypeError(f'Expected {type_.__name__}, but got {type(value).__name__}.')
    return True


def validate_types(value, types_):
    if not isinstance(value, types_):
        raise TypeError(f'Expected {str(types_).replace("|", "or")}, but got {type(value).__name__}.')
    return True


def validate_is_not_empty_string(value: str):
    validate_type(value, str)
    if value == '':
        raise ValueError('Value cannot be empty string.')
    return True


def validate_is_not_negative_number(value: int):
    validate_type(value, int)
    if value < 0:
        raise ValueError('Value cannot be negative number.')
    return True
