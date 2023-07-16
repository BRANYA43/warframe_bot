import datetime
import unittest

from tests.test_objects.base_test import BaseTest
from warframe_bot.objects.base import Base


class TestBase(BaseTest):
    """Test Base"""

    def setUp(self) -> None:
        self.key = 'key'
        self.name = 'name'
        self.expiry = datetime.datetime.utcnow()
        self.base = Base(key=self.key, name=self.name, expiry=self.expiry)

    def test_create_base_with_correct_values(self):
        """Test: create base with correct attrs"""
        self.assertEqual(self.base.key, self.key)
        self.assertEqual(self.base.name, self.name)
        self.assertEqual(self.base.expiry, self.expiry)

    def test_not_create_base_with_incorrect_values(self):
        """Test: not create base with incorrect attrs"""
        with self.assertRaises((TypeError, ValueError)):
            Base(key=None, name=None, expiry=None)
            Base(key='', name='', expiry=None)

    def test_raise_errors_of_name_property(self):
        """Test: raise ValueError if name is empty string, raise TypeError if name isn't str."""
        with self.assertRaises(TypeError) as e:
            self.base.key = None
        self.check_error_message(e, 'key must be str.')

        with self.assertRaises(ValueError) as e:
            self.base.key = ''
        self.check_error_message(e, 'key cannot be empty string.')

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
            self.base.expiry = None
        self.check_error_message(e, 'expiry must be datetime.')


if __name__ == '__main__':
    unittest.main()
