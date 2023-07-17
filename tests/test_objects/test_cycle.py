import datetime
import unittest

from tests.test_objects.base_test import BaseTest
from warframe_bot.objects.cycle import Cycle


class TestBase(BaseTest):

    def setUp(self) -> None:
        self.cycle_key = 'key'
        self.cycle_name = 'name'
        self.current_cycle = 'cycle_1'
        self.expiry = datetime.datetime.utcnow()
        self.cycle = Cycle(key=self.cycle_key, name=self.cycle_name, expiry=self.expiry,
                           current_cycle=self.current_cycle, cycles=['cycle_1', 'cycle_2'])

    def test_create_cycle_with_correct_values(self):
        """Test: create cycle with correct attrs."""
        self.assertEqual(self.cycle.key, self.cycle_key)
        self.assertEqual(self.cycle.name, self.cycle_name)
        self.assertEqual(self.cycle.current_cycle, self.current_cycle)
        self.assertEqual(self.cycle.cycles, ['cycle_1', 'cycle_2'])

    def test_not_create_cycle_with_incorrect_values(self):
        """Test: not create cycle with incorrect attrs"""
        with self.assertRaises((TypeError, ValueError)):
            Cycle(key=self.cycle_key, name=self.cycle_name, expiry=self.expiry, current_cycle=None,
                  cycles=['cycle_1', 'cycle_2'])
            Cycle(key=self.cycle_key, name=self.cycle_name, expiry=self.expiry, current_cycle='',
                  cycles=['cycle_1', 'cycle_2'])
            Cycle(key=self.cycle_key, name=self.cycle_name, expiry=self.expiry, current_cycle='None',
                  cycles=['cycle_1', 'cycle_2'])
            Cycle(key=self.cycle_key, name=self.cycle_name, expiry=self.expiry, current_cycle='cycle_1', cycles=[])
            Cycle(key=self.cycle_key, name=self.cycle_name, expiry=self.expiry, current_cycle='cycle_1', cycles=[None])
            Cycle(key=self.cycle_key, name=self.cycle_name, expiry=self.expiry, current_cycle='cycle_1', cycles=[''])
            Cycle(key=self.cycle_key, name=self.cycle_name, expiry=self.expiry, current_cycle='cycle_1',
                  cycles=['cycle_1'])
            Cycle(key=self.cycle_key, name=self.cycle_name, expiry=self.expiry, current_cycle='cycle_1',
                  cycles=[None, 'cycle_1'])
            Cycle(key=self.cycle_key, name=self.cycle_name, expiry=self.expiry, current_cycle='cycle_1',
                  cycles=['', 'cycle_1'])

    def test_raise_errors_of_current_cycle_property(self):
        """
        Test: raise TypeError if current_cycle isn't str, raise ValueError if current_cycle is empty string, raise
        ValueError if current_cycle isn't in list of cycles.
        """
        with self.assertRaises(TypeError) as e:
            self.cycle.current_cycle = None
        self.check_error_message(e, 'current_cycle must be str.')

        with self.assertRaises(ValueError) as e:
            self.cycle.current_cycle = ''
        self.check_error_message(e, 'current_cycle cannot be empty string.')

        with self.assertRaises(ValueError) as e:
            self.cycle.current_cycle = 'None'
        self.check_error_message(e, 'current_cycle must be within in cycles.')

    def test_raise_errors_of_cycles_property(self):
        """
        Test: raise TypeError if cycles isn't list, raise ValueError if cycles is empty, raise ValueError if cycles
        has one item, raise ValueError if items of cycles aren't str.
        """
        with self.assertRaises(TypeError) as e:
            self.cycle.cycles = None
        self.check_error_message(e, 'cycles must be list.')

        with self.assertRaises(ValueError) as e:
            self.cycle.cycles = []
            self.cycle.cycles = ['cycle_1']
        self.check_error_message(e, 'cycles cannot have less 2 items.')

        with self.assertRaises(TypeError) as e:
            self.cycle.cycles = [None, None]
            self.cycle.cycles = ['cycle_1', None]
        self.check_error_message(e, 'items of cycles must be str.')

        with self.assertRaises(ValueError) as e:
            self.cycle.cycles = ['', '']
            self.cycle.cycles = ['cycle_1', '']
        self.check_error_message(e, 'items of cycles cannot be empty string.')

    def test_set_next_cycle_when_setting_current_cycle(self):
        """Test: set next_cycle when setting current_cycle."""
        self.assertEqual(self.cycle.next_cycle, 'cycle_2')

    def test_change_next_cycle_when_setting_current_cycle(self):
        """Test: change next_cycle when setting another current_cycle."""
        self.cycle.current_cycle = 'cycle_2'
        self.assertEqual(self.cycle.next_cycle, 'cycle_1')

    def test_get_info(self):
        """Test: get_info return correct info"""

        correct_info = f'Name: {self.cycle.name}\n' \
                       f'Current cycle: {self.cycle.current_cycle}\n' \
                       f'Next cycle: {self.cycle.next_cycle}\n' \
                       f'Left time: {self.cycle.expiry}\n'
        info = self.cycle.get_info()

        self.assertEqual(info, correct_info)


if __name__ == '__main__':
    unittest.main()
