import unittest

from src.validators import *


class TestValidators(unittest.TestCase):
    """Test Validators"""

    def test_raise_of_validate_type(self):
        """Test: raise TypeError with the message: 'Expected _, but got _.'."""
        self.assertRaisesRegex(TypeError, r'^Expected (.+), but got (.+).$', validate_type, None, int)

    def test_not_raise_of_validate_type(self):
        """Test: not raise TypeError if value is correct."""
        self.assertTrue(validate_types(1, int))

    def test_raise_of_validate_types(self):
        """Test: raise TypeError with the message: 'Expected _ or _, but got _.'."""
        self.assertRaisesRegex(TypeError, r'^Expected (.+) or (.+), but got (.+).$', validate_types, None, int | str)

    def test_not_raise_of_validate_types(self):
        """Test: not raise TypeError if value is correct."""
        self.assertTrue(validate_types(1, int | str))
        self.assertTrue(validate_types('1', int | str))

    def test_raise_of_validate_is_not_empty_string(self):
        """
        Test: raise ValueError with the message: 'Value cannot be empty string.'
        and raise TypeError if value type is not str.
        """
        self.assertRaisesRegex(ValueError, r'^Value cannot be empty string.$', validate_is_not_empty_string, '')
        self.assertRaisesRegex(TypeError, r'^Expected str, but got (.+).$', validate_is_not_empty_string, None)

    def test_not_raise_of_validate_is_not_empty_string(self):
        """Test: not raise ValueError and TypeError if value is correct."""
        self.assertTrue(validate_is_not_empty_string('not empty string'))

    def test_raise_of_validate_is_not_negative_number(self):
        """
        Test: raise ValueError with the message: 'Value cannot be negative number.'
        and raise TypeError if value type is not int.
        """
        self.assertRaisesRegex(ValueError, r'^Value cannot be negative number.$', validate_is_not_negative_number, -1)
        self.assertRaisesRegex(TypeError, r'^Expected int, but got (.+).$', validate_is_not_negative_number, None)

    def test_not_raise_of_validate_is_not_negative_number(self):
        """Test: not raise ValueError and TypeError if value is correct."""
        self.assertTrue(validate_is_not_negative_number(0))


if __name__ == '__main__':
    unittest.main()
