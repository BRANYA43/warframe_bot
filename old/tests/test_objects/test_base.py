import unittest

from objects.timer import Timer
from test_objects.base_test import BaseTest
from objects.base import Base


class TestBase(BaseTest):
    """Test Base"""

    def setUp(self) -> None:
        class BaseT(Base):
            def get_info(self):
                raise NotImplementedError

        self.name = 'name'
        self.timer = Timer(Timer.DAY+Timer.HOUR+Timer.MINUTE)
        self.base = BaseT(name=self.name, timer=self.timer)

    def test_create_base_with_correct_values(self):
        """Test: create base with correct attrs"""
        self.assertEqual(self.base.name, self.name)
        self.assertEqual(self.base.timer, self.timer)

    def test_not_create_base_with_incorrect_values(self):
        """Test: not create base with incorrect attrs"""
        with self.assertRaises((TypeError, ValueError)):
            Base(name=None, timer=None)
            Base(name='', timer=None)

    def test_raise_errors_of_title_property(self):
        """Test: raise ValueError if name is empty string, raise TypeError if name isn't str."""
        with self.assertRaises(TypeError) as e:
            self.base.name = None
        self.check_error_message(e, 'name must be str.')

        with self.assertRaises(ValueError) as e:
            self.base.name = ''
        self.check_error_message(e, 'name cannot be empty string.')

    def test_raise_errors_of_timer_property(self):
        """Test: raise TypeError if timer isn't Timer."""
        with self.assertRaises(TypeError) as e:
            self.base.timer = None
        self.check_error_message(e, 'timer must be Timer.')


if __name__ == '__main__':
    unittest.main()
