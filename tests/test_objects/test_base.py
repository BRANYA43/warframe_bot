import datetime
import unittest

from tests.test_objects.base_test import BaseTest
from warframe_bot.objects.base import Base


class TestBase(BaseTest):
    """Test Base"""

    def setUp(self) -> None:
        class BaseT(Base):
            def get_info(self):
                raise NotImplementedError

        self.name = 'name'
        self.left_time = '1d 1m'
        self.base = BaseT(name=self.name, left_time=self.left_time)

    def test_create_base_with_correct_values(self):
        """Test: create base with correct attrs"""
        self.assertEqual(self.base.name, self.name)
        self.assertEqual(self.base.left_time, self.left_time)

    def test_not_create_base_with_incorrect_values(self):
        """Test: not create base with incorrect attrs"""
        with self.assertRaises((TypeError, ValueError)):
            Base(name=None, left_time=None)
            Base(name='', left_time=None)

    def test_raise_errors_of_title_property(self):
        """Test: raise ValueError if title is empty string, raise TypeError if title isn't str."""
        with self.assertRaises(TypeError) as e:
            self.base.name = None
        self.check_error_message(e, 'name must be str.')

        with self.assertRaises(ValueError) as e:
            self.base.name = ''
        self.check_error_message(e, 'name cannot be empty string.')

    def test_raise_errors_of_expiry_property(self):
        """Test: raise TypeError if expiry isn't datetime."""
        with self.assertRaises(TypeError) as e:
            self.base.left_time = None
        self.check_error_message(e, 'left_time must be str.')

        with self.assertRaises(ValueError) as e:
            self.base.left_time = ''
        self.check_error_message(e, 'left_time cannot be empty string.')


if __name__ == '__main__':
    unittest.main()
